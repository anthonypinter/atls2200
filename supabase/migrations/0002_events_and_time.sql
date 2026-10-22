-- Activity log and reading time. Run after 0001 (SQL editor, or `supabase db push`).
--
-- events: one row per thing a student did, uploaded by js/backend.js from the browser's queue (js/progress.js):
-- visit, seen, time, used, run, answer, quiz-done, check, complete, uncomplete.
-- Students can add rows for themselves but never change or delete them, and the server stamps each row with the time
-- it arrived (at), so the history can't be quietly rewritten. client_at is when the browser says it happened (it
-- differs when work was done offline or signed out, and could be faked; at can't).

create table public.events (
  id         bigint generated always as identity primary key,
  user_id    uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  client_id  text not null,                                -- the browser's id for the event, so a retry isn't stored twice
  at         timestamptz not null default now(),
  client_at  timestamptz,
  lesson     text,
  kind       text not null check (kind in ('visit', 'seen', 'time', 'used', 'run', 'answer', 'quiz-done', 'check', 'complete', 'uncomplete')),
  target     text,                                         -- section, quiz or exercise id ("flexbox/sec-key-ideas")
  detail     jsonb check (detail is null or octet_length(detail::text) < 30000),
  unique (user_id, client_id)
);
create index events_user_at on public.events (user_id, at);
create index events_lesson on public.events (lesson);

-- A browser that's misbehaving (or a student scripting one) can't flood the table.
create function public.limit_events() returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
  if (select count(*) from public.events where user_id = new.user_id and at > now() - interval '10 minutes') >= 3000 then
    raise exception 'Too many activity events; try again later.';
  end if;
  return new;
end $$;
create trigger events_limit before insert on public.events for each row execute function public.limit_events();

alter table public.events enable row level security;
create policy "add own events" on public.events
  for insert to authenticated with check (user_id = auth.uid());
create policy "read own events, instructors read all" on public.events
  for select to authenticated using (user_id = auth.uid() or public.is_instructor());

-- Insert only, and only these columns: id, at and the user are the server's to set.
revoke all on public.events from anon, authenticated;
grant select on public.events to authenticated;
grant insert (client_id, client_at, lesson, kind, target, detail) on public.events to authenticated;

-- Reporting -------------------------------------------------------------------------------------------------------
-- Reading time per section (seconds), from the progress copy.
create or replace view public.section_progress with (security_invoker = true) as
select p.email, p.display_name, p.course_section,
       split_part(s.key, '/', 1) as lesson, split_part(s.key, '/', 2) as section,
       public.as_time(s.value ->> 'seen') as seen, public.as_time(s.value ->> 'interacted') as interacted,
       round(coalesce(public.as_int(s.value ->> 'ms'), 0) / 1000.0) as active_seconds
from public.progress g
join public.profiles p on p.id = g.user_id
cross join lateral jsonb_each(case jsonb_typeof(g.data -> 'sections') when 'object' then g.data -> 'sections' else '{}' end) s
where jsonb_typeof(s.value) = 'object';

-- Exercise attempts from the log: how many Checks, and how many before the first pass.
create view public.exercise_attempts with (security_invoker = true) as
select p.email, p.display_name, p.course_section, e.target as exercise,
       count(*) as checks,
       count(*) filter (where e.at < f.first_pass) as checks_before_pass,
       f.first_pass
from public.events e
join public.profiles p on p.id = e.user_id
left join lateral (
  select min(x.at) as first_pass from public.events x
  where x.user_id = e.user_id and x.target = e.target and x.kind = 'check' and x.detail ->> 'passed' = 'true'
) f on true
where e.kind = 'check'
group by p.email, p.display_name, p.course_section, e.target, f.first_pass;

revoke all on public.exercise_attempts from anon;
