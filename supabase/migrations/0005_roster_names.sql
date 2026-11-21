-- Names on the roster: instructors can give each student's first and last name when they enroll them
-- (tools/enroll.mjs, or the dashboard's Roster → People). The name is copied onto the student's profile, so it shows on
-- the dashboard right away, and a student whose name is already there skips the name step at first sign-in.
-- Run after 0001–0004.
--
-- Students can still edit their name in the Account dialog (e.g. to a preferred name). Re-running the enrollment
-- script doesn't undo that: a roster name reaches the profile only when the account is created, or when the roster's
-- name itself changes (say you fix a typo in the CSV). A blank roster name never clears a profile name.

alter table public.roster
  add column first_name text check (first_name is null or char_length(btrim(first_name)) between 1 and 60),
  add column last_name  text check (last_name is null or char_length(btrim(last_name)) between 1 and 60);

-- New account: role, section, recitation and name from the roster; the flag from the account's app metadata.
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, email, role, course_section, recitation, must_change_password, first_name, last_name)
  select new.id, lower(new.email), coalesce(r.role, 'student'), r.course_section, r.recitation,
         coalesce((new.raw_app_meta_data ->> 'must_change_password')::boolean, false),
         nullif(btrim(r.first_name), ''), nullif(btrim(r.last_name), '')
  from (select 1) one left join public.roster r on r.email = lower(new.email);
  return new;
end $$;

-- Roster changes reach people who already have an account. Names only when the roster's name is new or changed.
create or replace function public.apply_roster() returns trigger
language plpgsql security definer set search_path = ''
as $$
declare
  first_changed boolean;
  last_changed  boolean;
begin
  if tg_op = 'DELETE' then
    update public.profiles set role = 'student' where email = old.email;
    return old;
  end if;
  first_changed := new.first_name is not null and (tg_op = 'INSERT' or new.first_name is distinct from old.first_name);
  last_changed  := new.last_name  is not null and (tg_op = 'INSERT' or new.last_name  is distinct from old.last_name);
  update public.profiles
  set role = new.role, course_section = new.course_section, recitation = new.recitation,
      first_name = case when first_changed then btrim(new.first_name) else first_name end,
      last_name  = case when last_changed  then btrim(new.last_name)  else last_name  end
  where email = new.email;
  return new;
end $$;
