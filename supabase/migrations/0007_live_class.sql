-- Class is Live: in-class questions. Run after 0001–0006 (SQL editor, or `supabase db push`).
--
-- The instructor starts a session at the start of class (live-host.html) and ends it at the end. While it's open they
-- ask one question at a time: multiple choice, word cloud or a 1–N scale. Students answer on live.html and, once
-- they've answered (or the instructor closes the question), see the class's results. The projector view shows the same
-- results. Every session is kept, so the dashboard can show who answered in which class (attendance).
--
-- Who can see what:
--   signed out   only whether class is live right now (live_now(), for the landing page's button)
--   student      the open session and its questions; their own answers; everyone's answers only as totals
--                (live_results()), never who gave them; answers only through live_answer(), which checks them
--   instructor   everything, including who answered what, the correct answer and hidden word-cloud words
-- A session left open is treated as over after 4 hours, so a forgotten End class doesn't leave it live overnight.

-- Tables ----------------------------------------------------------------------------------------------------------
create table public.live_sessions (
  id               bigint generated always as identity primary key,
  title            text check (title is null or char_length(btrim(title)) between 1 and 120),
  started_at       timestamptz not null default now(),
  ended_at         timestamptz,
  started_by       uuid default auth.uid() references public.profiles (id) on delete set null,
  current_question bigint                                   -- what students see now; set by live_ask / the host page
);

create table public.live_questions (
  id          bigint generated always as identity primary key,
  session_id  bigint not null references public.live_sessions (id) on delete cascade,
  kind        text not null check (kind in ('choice', 'words', 'scale')),
  prompt      text not null check (char_length(btrim(prompt)) between 1 and 500),
  -- choice: {"choices": ["…", …]}   words: {"max": 1–3 per student}   scale: {"min": 0|1, "max": 2–10, "low": "…", "high": "…"}
  options     jsonb not null default '{}'::jsonb check (octet_length(options::text) < 4000),
  status      text not null default 'open' check (status in ('open', 'closed')),
  reveal      boolean not null default false,               -- show the correct choice to students and on screen
  created_at  timestamptz not null default now(),
  closed_at   timestamptz
);
create index live_questions_session on public.live_questions (session_id);
alter table public.live_sessions
  add constraint live_sessions_current foreign key (current_question) references public.live_questions (id) on delete set null;

-- What students must not read before the instructor reveals it: the correct choice, and words hidden from the cloud.
create table public.live_private (
  question_id bigint primary key references public.live_questions (id) on delete cascade,
  correct     int,
  hidden      text[] not null default '{}'
);

-- One answer per student per question; they can change it while the question is open.
--   choice: {"choice": 2}   words: {"words": ["flexbox", "grid"]}   scale: {"n": 4}
create table public.live_answers (
  question_id bigint not null references public.live_questions (id) on delete cascade,
  user_id     uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  value       jsonb not null check (octet_length(value::text) < 1000),
  at          timestamptz not null default now(),
  primary key (question_id, user_id)
);
create index live_answers_user on public.live_answers (user_id);

-- Questions written ahead of class, kept between sessions (and devices). Instructors only.
create table public.live_bank (
  id         bigint generated always as identity primary key,
  kind       text not null check (kind in ('choice', 'words', 'scale')),
  prompt     text not null check (char_length(btrim(prompt)) between 1 and 500),
  options    jsonb not null default '{}'::jsonb check (octet_length(options::text) < 4000),
  correct    int,
  sort       double precision not null default extract(epoch from now()),
  created_at timestamptz not null default now()
);

-- Helpers ---------------------------------------------------------------------------------------------------------
create function public.live_open_session() returns bigint
language sql stable security definer set search_path = ''
as $$
  select id from public.live_sessions
  where ended_at is null and started_at > now() - interval '4 hours'
  order by started_at desc limit 1
$$;

-- For the landing page, signed in or not: is class live, and its title.
create function public.live_now() returns jsonb
language sql stable security definer set search_path = ''
as $$
  select coalesce(
    (select jsonb_build_object('live', true, 'title', s.title, 'started_at', s.started_at)
     from public.live_sessions s where s.id = public.live_open_session()),
    '{"live": false}'::jsonb)
$$;

-- Options checked and rebuilt from known keys, so nothing else rides along to students' browsers.
create function public.live_clean_options(p_kind text, p_options jsonb) returns jsonb
language plpgsql immutable set search_path = ''
as $$
declare
  o jsonb := coalesce(p_options, '{}'::jsonb);
  choices jsonb;
  lo int; hi int;
begin
  if p_kind = 'choice' then
    select coalesce(jsonb_agg(btrim(c) order by i), '[]'::jsonb) into choices
    from jsonb_array_elements_text(case jsonb_typeof(o -> 'choices') when 'array' then o -> 'choices' else '[]' end) with ordinality as t(c, i)
    where btrim(c) <> '';
    if jsonb_array_length(choices) not between 2 and 6 then raise exception 'A multiple-choice question needs 2 to 6 choices.'; end if;
    if exists (select 1 from jsonb_array_elements_text(choices) c where char_length(c) > 200) then raise exception 'Keep each choice under 200 characters.'; end if;
    return jsonb_build_object('choices', choices);
  elsif p_kind = 'words' then
    return jsonb_build_object('max', least(3, greatest(1, coalesce((o ->> 'max')::int, 1))));
  elsif p_kind = 'scale' then
    lo := coalesce((o ->> 'min')::int, 1);
    hi := coalesce((o ->> 'max')::int, 5);
    if lo not in (0, 1) or hi not between 2 and 10 then raise exception 'A scale runs from 0 or 1 up to 2–10.'; end if;
    return jsonb_build_object('min', lo, 'max', hi,
      'low', left(nullif(btrim(o ->> 'low'), ''), 40), 'high', left(nullif(btrim(o ->> 'high'), ''), 40));
  end if;
  raise exception 'Unknown question type %', p_kind;
end $$;

-- Word-cloud entries: lower case, single spaces, no punctuation at either end, 1–30 characters.
create function public.live_word(w text) returns text
language sql immutable set search_path = ''
as $$ select nullif(left(regexp_replace(regexp_replace(lower(btrim(w)), '\s+', ' ', 'g'), '^[[:punct:][:space:]]+|[[:punct:][:space:]]+$', '', 'g'), 30), '') $$;

-- Instructor actions ----------------------------------------------------------------------------------------------
create function public.live_start(p_title text default null) returns bigint
language plpgsql security definer set search_path = ''
as $$
declare s bigint;
begin
  if not public.is_instructor() then raise exception 'Only instructors can start class.'; end if;
  s := public.live_open_session();
  if s is not null then return s; end if;
  -- A session forgotten from an earlier class ends now.
  update public.live_questions set status = 'closed', closed_at = now()
  where status = 'open' and session_id in (select id from public.live_sessions where ended_at is null);
  update public.live_sessions set ended_at = least(now(), started_at + interval '4 hours') where ended_at is null;
  insert into public.live_sessions (title) values (nullif(btrim(p_title), '')) returning id into s;
  return s;
end $$;

create function public.live_end() returns void
language plpgsql security definer set search_path = ''
as $$
begin
  if not public.is_instructor() then raise exception 'Only instructors can end class.'; end if;
  update public.live_questions set status = 'closed', closed_at = now()
  where status = 'open' and session_id in (select id from public.live_sessions where ended_at is null);
  update public.live_sessions set ended_at = now(), current_question = null where ended_at is null;
end $$;

-- Ask a question now: the one before it closes, and this one is what everyone sees.
create function public.live_ask(p_kind text, p_prompt text, p_options jsonb, p_correct int default null) returns bigint
language plpgsql security definer set search_path = ''
as $$
declare s bigint; q bigint; opts jsonb;
begin
  if not public.is_instructor() then raise exception 'Only instructors can ask questions.'; end if;
  s := public.live_open_session();
  if s is null then raise exception 'Start class first.'; end if;
  opts := public.live_clean_options(p_kind, p_options);
  if p_correct is not null and (p_kind <> 'choice' or p_correct not between 0 and jsonb_array_length(opts -> 'choices') - 1) then
    raise exception 'The correct answer must be one of the choices.';
  end if;
  update public.live_questions set status = 'closed', closed_at = now() where session_id = s and status = 'open';
  insert into public.live_questions (session_id, kind, prompt, options) values (s, p_kind, btrim(p_prompt), opts) returning id into q;
  insert into public.live_private (question_id, correct) values (q, p_correct);
  update public.live_sessions set current_question = q where id = s;
  return q;
end $$;

-- Hide (or bring back) a word in a word cloud, e.g. something not fit for the projector.
create function public.live_hide_word(p_question bigint, p_word text, p_hide boolean default true) returns void
language plpgsql security definer set search_path = ''
as $$
declare w text := public.live_word(p_word);
begin
  if not public.is_instructor() then raise exception 'Only instructors can hide words.'; end if;
  if w is null then return; end if;
  insert into public.live_private (question_id) values (p_question) on conflict do nothing;
  update public.live_private
  set hidden = case when p_hide then array(select distinct x from unnest(hidden || w) x) else array_remove(hidden, w) end
  where question_id = p_question;
end $$;

-- Student actions -------------------------------------------------------------------------------------------------
-- Answer (or change an answer to) the question on screen. Returns the results, which the student may now see.
create function public.live_answer(p_question bigint, p_value jsonb) returns jsonb
language plpgsql security definer set search_path = ''
as $$
declare
  q public.live_questions;
  v jsonb;
  n int;
  words text[];
begin
  if auth.uid() is null then raise exception 'Sign in to answer.'; end if;
  if not public.profile_complete() then raise exception 'Finish setting up your account (Account button) before answering.'; end if;
  select * into q from public.live_questions where id = p_question;
  if q.id is null or q.session_id is distinct from public.live_open_session()
     or q.id is distinct from (select current_question from public.live_sessions where id = q.session_id) then
    raise exception 'That question isn''t on screen any more.';
  end if;
  if q.status <> 'open' then raise exception 'Answers to this question are closed.'; end if;

  if q.kind = 'choice' then
    n := (p_value ->> 'choice')::int;
    if n is null or n not between 0 and jsonb_array_length(q.options -> 'choices') - 1 then raise exception 'Pick one of the choices.'; end if;
    v := jsonb_build_object('choice', n);
  elsif q.kind = 'scale' then
    n := (p_value ->> 'n')::int;
    if n is null or n not between (q.options ->> 'min')::int and (q.options ->> 'max')::int then raise exception 'Pick a number on the scale.'; end if;
    v := jsonb_build_object('n', n);
  else
    select array_agg(distinct w) into words from (
      select public.live_word(x) as w
      from jsonb_array_elements_text(case jsonb_typeof(p_value -> 'words') when 'array' then p_value -> 'words' else '[]' end) x
    ) t where w is not null;
    if coalesce(cardinality(words), 0) = 0 then raise exception 'Type a word or short phrase.'; end if;
    if cardinality(words) > (q.options ->> 'max')::int then raise exception 'Up to % entries.', q.options ->> 'max'; end if;
    v := jsonb_build_object('words', to_jsonb(words));
  end if;

  insert into public.live_answers (question_id, user_id, value) values (q.id, auth.uid(), v)
  on conflict (question_id, user_id) do update set value = excluded.value, at = now();
  return public.live_results(q.id);
end $$;

-- Results as totals only. Students get them once they've answered or the question is closed (otherwise just the
-- count), and only for the open session. The correct choice appears for students once it's revealed.
create function public.live_results(p_question bigint) returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
  q public.live_questions;
  instr boolean := public.is_instructor();
  priv public.live_private;
  mine jsonb;
  n int;
  res jsonb;
begin
  select * into q from public.live_questions where id = p_question;
  if q.id is null or (not instr and q.session_id is distinct from public.live_open_session()) then return null; end if;
  select * into priv from public.live_private where question_id = q.id;
  select value into mine from public.live_answers where question_id = q.id and user_id = auth.uid();
  select count(*) into n from public.live_answers where question_id = q.id;
  res := jsonb_build_object('id', q.id, 'count', n, 'mine', mine, 'status', q.status,
                            'shown', instr or mine is not null or q.status = 'closed');
  if not (res ->> 'shown')::boolean then return res; end if;

  if q.kind = 'choice' then
    res := res || jsonb_build_object('tally', (
      select jsonb_agg(coalesce(c.n, 0) order by i)
      from generate_series(0, jsonb_array_length(q.options -> 'choices') - 1) i
      left join (select (value ->> 'choice')::int k, count(*) n from public.live_answers where question_id = q.id group by 1) c on c.k = i));
    if instr or q.reveal then res := res || jsonb_build_object('correct', priv.correct); end if;
  elsif q.kind = 'scale' then
    res := res || jsonb_build_object(
      'tally', (select jsonb_agg(coalesce(c.n, 0) order by i)
                from generate_series((q.options ->> 'min')::int, (q.options ->> 'max')::int) i
                left join (select (value ->> 'n')::int k, count(*) n from public.live_answers where question_id = q.id group by 1) c on c.k = i),
      'mean', (select round(avg((value ->> 'n')::numeric), 2) from public.live_answers where question_id = q.id));
  else
    res := res || jsonb_build_object('words', coalesce((
      select jsonb_agg(jsonb_build_object('w', w, 'n', c) order by c desc, w)
      from (select w, count(*) c
            from public.live_answers a cross join lateral jsonb_array_elements_text(a.value -> 'words') w
            where a.question_id = q.id and not (w = any (coalesce(priv.hidden, '{}')))
            group by w order by c desc, w limit 80) t), '[]'::jsonb));
    if instr then res := res || jsonb_build_object('hidden', to_jsonb(coalesce(priv.hidden, '{}'))); end if;
  end if;
  return res;
end $$;

-- Everything a page needs in one request (live.html polls this every few seconds): the open session, the question on
-- screen and its results as live_results gives them to the caller.
create function public.live_state() returns jsonb
language plpgsql stable security definer set search_path = ''
as $$
declare
  s public.live_sessions;
  q public.live_questions;
begin
  if auth.uid() is null then return null; end if;
  select * into s from public.live_sessions where id = public.live_open_session();
  if s.id is null then return jsonb_build_object('live', false); end if;
  select * into q from public.live_questions where id = s.current_question;
  return jsonb_build_object('live', true,
    'session', jsonb_build_object('id', s.id, 'title', s.title, 'started_at', s.started_at),
    'question', case when q.id is null then null else jsonb_build_object('id', q.id, 'kind', q.kind, 'prompt', q.prompt,
      'options', q.options, 'status', q.status, 'reveal', q.reveal) end,
    'results', case when q.id is null then null else public.live_results(q.id) end);
end $$;

-- Row-level security ----------------------------------------------------------------------------------------------
alter table public.live_sessions enable row level security;
alter table public.live_questions enable row level security;
alter table public.live_private enable row level security;
alter table public.live_answers enable row level security;
alter table public.live_bank enable row level security;

create policy "students see the open session, instructors all" on public.live_sessions
  for select to authenticated using (id = public.live_open_session() or public.is_instructor());
create policy "instructors manage sessions" on public.live_sessions
  for all to authenticated using (public.is_instructor()) with check (public.is_instructor());

create policy "students see the open session's questions, instructors all" on public.live_questions
  for select to authenticated using (session_id = public.live_open_session() or public.is_instructor());
create policy "instructors manage questions" on public.live_questions
  for all to authenticated using (public.is_instructor()) with check (public.is_instructor());

create policy "instructors only" on public.live_private
  for all to authenticated using (public.is_instructor()) with check (public.is_instructor());
create policy "instructors only" on public.live_bank
  for all to authenticated using (public.is_instructor()) with check (public.is_instructor());

-- Students read their own answers; instructors read everyone's (names come from profiles). Writes go through live_answer.
create policy "read own answers, instructors read all" on public.live_answers
  for select to authenticated using (user_id = auth.uid() or public.is_instructor());
create policy "instructors remove answers" on public.live_answers
  for delete to authenticated using (public.is_instructor());

revoke all on public.live_sessions, public.live_questions, public.live_private, public.live_answers, public.live_bank from anon, authenticated;
grant select, update on public.live_sessions to authenticated;                       -- update: RLS lets only instructors
grant select, update, delete on public.live_questions to authenticated;
grant select, insert, update, delete on public.live_private, public.live_bank to authenticated;
grant select, delete on public.live_answers to authenticated;

revoke execute on function public.live_open_session(), public.live_clean_options(text, jsonb), public.live_word(text),
  public.live_start(text), public.live_end(), public.live_ask(text, text, jsonb, int), public.live_hide_word(bigint, text, boolean),
  public.live_answer(bigint, jsonb), public.live_results(bigint), public.live_state(), public.live_now() from public, anon;
grant execute on function public.live_open_session(), public.live_start(text), public.live_end(), public.live_ask(text, text, jsonb, int),
  public.live_hide_word(bigint, text, boolean), public.live_answer(bigint, jsonb), public.live_results(bigint), public.live_state(), public.live_now() to authenticated;
grant execute on function public.live_now() to anon;

-- Attendance: one row per student per session they answered in.
create view public.live_attendance with (security_invoker = true) as
select s.id as session_id, s.title, s.started_at, p.id as user_id, p.email, p.first_name, p.last_name, p.recitation, p.course_section,
       count(*) as answered,
       (select count(*) from public.live_questions x where x.session_id = s.id) as asked,
       min(a.at) as first_answer
from public.live_answers a
join public.live_questions q on q.id = a.question_id
join public.live_sessions s on s.id = q.session_id
join public.profiles p on p.id = a.user_id
group by s.id, p.id;
revoke all on public.live_attendance from anon;

-- A student's own attendance for their progress page (account.html): every class held, how many questions it had and
-- how many they answered. Students can't read past sessions directly (RLS above), so this returns just these counts.
create function public.live_my_attendance() returns table (session_id bigint, title text, started_at timestamptz, asked bigint, answered bigint)
language sql stable security definer set search_path = ''
as $$
  select s.id, s.title, s.started_at,
         (select count(*) from public.live_questions q where q.session_id = s.id),
         (select count(*) from public.live_answers a join public.live_questions q on q.id = a.question_id
          where q.session_id = s.id and a.user_id = auth.uid())
  from public.live_sessions s
  where auth.uid() is not null
  order by s.started_at
$$;
revoke execute on function public.live_my_attendance() from public, anon;
grant execute on function public.live_my_attendance() to authenticated;

-- Realtime: pages hear about new questions and closed answers straight away (they also check every few seconds).
-- Realtime obeys the policies above, so a student's page hears only about their own answers.
do $$
begin
  if exists (select 1 from pg_publication where pubname = 'supabase_realtime') then
    alter publication supabase_realtime add table public.live_sessions, public.live_questions, public.live_answers;
  end if;
end $$;
