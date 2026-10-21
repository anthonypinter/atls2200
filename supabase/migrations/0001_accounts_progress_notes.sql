-- Field Guide backend: student accounts, synced progress, the class roster and instructor-only notes.
-- Run once in the Supabase SQL editor (or `supabase db push`). See supabase/README.md for the full setup.
--
-- Who can see what (row-level security, enforced by the database for every request made with the public anon key):
--   student     reads and writes only their own profile name and their own progress
--   instructor  reads everyone's profile and progress; reads and writes the roster and instructor notes
--   signed out  nothing at all
-- Roles come from the roster: list an email there as 'instructor' and that person becomes one (now or when they
-- first sign in). Everyone else with an @colorado.edu address is a student. Other addresses can't sign up.

-- Roster ----------------------------------------------------------------------------------------------------------
-- Optional for students (anyone at the university can sign in), required for instructors.
create table public.roster (
  email          text primary key check (email = lower(email)),
  role           text not null default 'student' check (role in ('student', 'instructor')),
  course_section text,                                      -- e.g. '001'; shown and filterable on the dashboard
  added_at       timestamptz not null default now()
);

-- Profiles --------------------------------------------------------------------------------------------------------
-- One per account, created automatically on first sign-in. Students may only change display_name (see grants below).
create table public.profiles (
  id             uuid primary key references auth.users (id) on delete cascade,
  email          text not null,
  display_name   text,
  role           text not null default 'student' check (role in ('student', 'instructor')),
  course_section text,
  created_at     timestamptz not null default now()
);

-- Progress --------------------------------------------------------------------------------------------------------
-- One row per student: the same object js/progress.js keeps in localStorage (lessons, sections, quizzes, exercises,
-- attempts, last). js/backend.js merges it with the browser's copy, so neither side loses work.
create table public.progress (
  user_id    uuid primary key references public.profiles (id) on delete cascade,
  data       jsonb not null default '{}'::jsonb check (octet_length(data::text) < 2000000),
  updated_at timestamptz not null default now()
);

-- Instructor notes ------------------------------------------------------------------------------------------------
-- Teaching notes for a lesson, or for one section of it. Never part of the public pages: js/backend.js fetches them
-- only for instructors, and RLS refuses everyone else.
create table public.instructor_notes (
  id         bigint generated always as identity primary key,
  lesson     text not null,                                 -- lesson slug, e.g. 'flexbox'
  section    text,                                          -- heading id, e.g. 'sec-try-every-setting'; null = whole lesson
  body       text not null,
  author     uuid references public.profiles (id) on delete set null default auth.uid(),
  updated_at timestamptz not null default now()
);
create index instructor_notes_lesson on public.instructor_notes (lesson);

-- Helpers ---------------------------------------------------------------------------------------------------------
create function public.is_instructor() returns boolean
language sql stable security definer set search_path = ''
as $$ select exists (select 1 from public.profiles where id = auth.uid() and role = 'instructor') $$;

create function public.touch_updated_at() returns trigger
language plpgsql set search_path = ''
as $$ begin new.updated_at = now(); return new; end $$;

create trigger progress_touch before update on public.progress for each row execute function public.touch_updated_at();
create trigger notes_touch before update on public.instructor_notes for each row execute function public.touch_updated_at();

-- Only university addresses may create (or move) an account. Change the domain here and in book.js together.
create function public.check_email_domain() returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
  if new.email is null or lower(new.email) not like '%@colorado.edu' then
    raise exception 'Sign in with your @colorado.edu address.';
  end if;
  return new;
end $$;
create trigger users_email_domain before insert or update of email on auth.users
  for each row execute function public.check_email_domain();

-- New account → profile, with the role and section from the roster when the email is listed.
create function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, email, role, course_section)
  select new.id, lower(new.email), coalesce(r.role, 'student'), r.course_section
  from (select 1) one left join public.roster r on r.email = lower(new.email);
  return new;
end $$;
create trigger users_profile after insert on auth.users
  for each row execute function public.handle_new_user();

-- Roster changes reach people who have already signed in.
create function public.apply_roster() returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
  if tg_op = 'DELETE' then
    update public.profiles set role = 'student' where email = old.email;
    return old;
  end if;
  update public.profiles set role = new.role, course_section = new.course_section where email = new.email;
  return new;
end $$;
create trigger roster_apply after insert or update or delete on public.roster
  for each row execute function public.apply_roster();

-- Row-level security ----------------------------------------------------------------------------------------------
alter table public.roster enable row level security;
alter table public.profiles enable row level security;
alter table public.progress enable row level security;
alter table public.instructor_notes enable row level security;

create policy "instructors manage the roster" on public.roster
  for all to authenticated using (public.is_instructor()) with check (public.is_instructor());

create policy "read own profile, instructors read all" on public.profiles
  for select to authenticated using (id = auth.uid() or public.is_instructor());
create policy "update own profile" on public.profiles
  for update to authenticated using (id = auth.uid()) with check (id = auth.uid());

create policy "read own progress, instructors read all" on public.progress
  for select to authenticated using (user_id = auth.uid() or public.is_instructor());
create policy "insert own progress" on public.progress
  for insert to authenticated with check (user_id = auth.uid());
create policy "update own progress" on public.progress
  for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());

create policy "instructors manage notes" on public.instructor_notes
  for all to authenticated using (public.is_instructor()) with check (public.is_instructor());

-- Column privileges: RLS picks the rows, these pick the columns. Students can't promote themselves or change section.
revoke all on public.roster, public.profiles, public.progress, public.instructor_notes from anon;
revoke update on public.profiles from authenticated;
grant update (display_name) on public.profiles to authenticated;
revoke insert, delete on public.profiles from authenticated;
revoke delete on public.progress from authenticated;

-- Reporting views -------------------------------------------------------------------------------------------------
-- Flat tables for the SQL editor or a CSV export (the dashboard reads progress directly). security_invoker makes the
-- views obey the RLS above, so a student querying them sees only their own rows. Students write their own progress
-- JSON, so values are cast leniently: anything malformed reads as null instead of breaking the whole view.
create function public.as_time(t text) returns timestamptz
language plpgsql stable set search_path = ''
as $$ begin return t::timestamptz; exception when others then return null; end $$;
create function public.as_int(t text) returns int
language plpgsql immutable set search_path = ''
as $$ begin return t::int; exception when others then return null; end $$;

create view public.lesson_progress with (security_invoker = true) as
select p.email, p.display_name, p.course_section, l.key as lesson,
       public.as_time(l.value ->> 'visited') as visited, public.as_time(l.value ->> 'completed') as completed
from public.progress g
join public.profiles p on p.id = g.user_id
cross join lateral jsonb_each(case jsonb_typeof(g.data -> 'lessons') when 'object' then g.data -> 'lessons' else '{}' end) l
where jsonb_typeof(l.value) = 'object';

create view public.section_progress with (security_invoker = true) as
select p.email, p.display_name, p.course_section,
       split_part(s.key, '/', 1) as lesson, split_part(s.key, '/', 2) as section,
       public.as_time(s.value ->> 'seen') as seen, public.as_time(s.value ->> 'interacted') as interacted
from public.progress g
join public.profiles p on p.id = g.user_id
cross join lateral jsonb_each(case jsonb_typeof(g.data -> 'sections') when 'object' then g.data -> 'sections' else '{}' end) s
where jsonb_typeof(s.value) = 'object';

create view public.check_results with (security_invoker = true) as
select p.email, p.display_name, p.course_section, 'quiz' as kind, q.key as id,
       public.as_int(q.value -> 'best' ->> 'score') as score, public.as_int(q.value -> 'best' ->> 'total') as total, null::timestamptz as passed
from public.progress g
join public.profiles p on p.id = g.user_id
cross join lateral jsonb_each(case jsonb_typeof(g.data -> 'quizzes') when 'object' then g.data -> 'quizzes' else '{}' end) q
where jsonb_typeof(q.value) = 'object'
union all
select p.email, p.display_name, p.course_section, 'exercise', e.key, null, null, public.as_time(e.value ->> 'passed')
from public.progress g
join public.profiles p on p.id = g.user_id
cross join lateral jsonb_each(case jsonb_typeof(g.data -> 'exercises') when 'object' then g.data -> 'exercises' else '{}' end) e
where jsonb_typeof(e.value) = 'object';

revoke all on public.lesson_progress, public.section_progress, public.check_results from anon;
