-- Student details: first name, last name and recitation, asked for the first time a student signs in.
-- Run after 0001 and 0002.
--
-- Recitations come from a list instructors keep (the recitations table, edited on the dashboard's Roster section or
-- with an insert here), so every student picks from the same set. Until a student has filled in their details, the
-- database won't store their progress or activity: js/backend.js shows the form and keeps their work in the browser
-- until it's done. Instructors don't need details. If the recitations list is empty, recitation isn't required.

create table public.recitations (
  code  text primary key check (code ~ '^[A-Za-z0-9 _-]{1,12}$'),   -- what students pick, e.g. '101' or 'R03'
  label text,                                                      -- optional, e.g. 'Tue 9:00, ATLS 104'
  sort  int not null default 0
);
alter table public.recitations enable row level security;
create policy "signed-in people read recitations" on public.recitations
  for select to authenticated using (true);
create policy "instructors manage recitations" on public.recitations
  for all to authenticated using (public.is_instructor()) with check (public.is_instructor());
revoke all on public.recitations from anon;

alter table public.profiles
  add column first_name text check (first_name is null or char_length(btrim(first_name)) between 1 and 60),
  add column last_name  text check (last_name is null or char_length(btrim(last_name)) between 1 and 60),
  add column recitation text references public.recitations (code) on update cascade on delete set null;

-- Students may set their own details (and still nothing else: role and course section stay the roster's).
grant update (first_name, last_name, recitation) on public.profiles to authenticated;

create function public.profile_complete() returns boolean
language sql stable security definer set search_path = ''
as $$
  select exists (
    select 1 from public.profiles p
    where p.id = auth.uid()
      and (p.role = 'instructor'
           or (p.first_name is not null and p.last_name is not null
               and (p.recitation is not null or not exists (select 1 from public.recitations))))
  )
$$;

-- Progress and activity are stored only once the details are in.
drop policy "insert own progress" on public.progress;
drop policy "update own progress" on public.progress;
create policy "insert own progress" on public.progress
  for insert to authenticated with check (user_id = auth.uid() and public.profile_complete());
create policy "update own progress" on public.progress
  for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid() and public.profile_complete());

drop policy "add own events" on public.events;
create policy "add own events" on public.events
  for insert to authenticated with check (user_id = auth.uid() and public.profile_complete());

-- Reporting views gain the new columns (added at the end, which `create or replace view` allows).
create or replace view public.lesson_progress with (security_invoker = true) as
select p.email, p.display_name, p.course_section, l.key as lesson,
       public.as_time(l.value ->> 'visited') as visited, public.as_time(l.value ->> 'completed') as completed,
       p.first_name, p.last_name, p.recitation
from public.progress g
join public.profiles p on p.id = g.user_id
cross join lateral jsonb_each(case jsonb_typeof(g.data -> 'lessons') when 'object' then g.data -> 'lessons' else '{}' end) l
where jsonb_typeof(l.value) = 'object';

create or replace view public.section_progress with (security_invoker = true) as
select p.email, p.display_name, p.course_section,
       split_part(s.key, '/', 1) as lesson, split_part(s.key, '/', 2) as section,
       public.as_time(s.value ->> 'seen') as seen, public.as_time(s.value ->> 'interacted') as interacted,
       round(coalesce(public.as_int(s.value ->> 'ms'), 0) / 1000.0) as active_seconds,
       p.first_name, p.last_name, p.recitation
from public.progress g
join public.profiles p on p.id = g.user_id
cross join lateral jsonb_each(case jsonb_typeof(g.data -> 'sections') when 'object' then g.data -> 'sections' else '{}' end) s
where jsonb_typeof(s.value) = 'object';

create or replace view public.check_results with (security_invoker = true) as
select p.email, p.display_name, p.course_section, 'quiz' as kind, q.key as id,
       public.as_int(q.value -> 'best' ->> 'score') as score, public.as_int(q.value -> 'best' ->> 'total') as total, null::timestamptz as passed,
       p.first_name, p.last_name, p.recitation
from public.progress g
join public.profiles p on p.id = g.user_id
cross join lateral jsonb_each(case jsonb_typeof(g.data -> 'quizzes') when 'object' then g.data -> 'quizzes' else '{}' end) q
where jsonb_typeof(q.value) = 'object'
union all
select p.email, p.display_name, p.course_section, 'exercise', e.key, null, null, public.as_time(e.value ->> 'passed'),
       p.first_name, p.last_name, p.recitation
from public.progress g
join public.profiles p on p.id = g.user_id
cross join lateral jsonb_each(case jsonb_typeof(g.data -> 'exercises') when 'object' then g.data -> 'exercises' else '{}' end) e
where jsonb_typeof(e.value) = 'object';

create or replace view public.exercise_attempts with (security_invoker = true) as
select p.email, p.display_name, p.course_section, e.target as exercise,
       count(*) as checks,
       count(*) filter (where e.at < f.first_pass) as checks_before_pass,
       f.first_pass,
       p.first_name, p.last_name, p.recitation
from public.events e
join public.profiles p on p.id = e.user_id
left join lateral (
  select min(x.at) as first_pass from public.events x
  where x.user_id = e.user_id and x.target = e.target and x.kind = 'check' and x.detail ->> 'passed' = 'true'
) f on true
where e.kind = 'check'
group by p.email, p.display_name, p.course_section, e.target, f.first_pass, p.first_name, p.last_name, p.recitation;
