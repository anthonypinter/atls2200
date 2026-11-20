-- Instructor enrollment: instructors create the accounts (tools/enroll.mjs) with a temporary password and assign
-- each student's recitation. On first sign-in a student must choose their own password, then give their first and
-- last name. Until both are done the database stores none of their progress or activity (as 0003 did for details).
-- Run after 0001, 0002 and 0003.

-- Recitations are assigned on the roster now, not picked by students.
alter table public.roster
  add column recitation text references public.recitations (code) on update cascade on delete set null;
revoke update (recitation) on public.profiles from authenticated;

-- Set when an instructor creates the account or resets its password; cleared by the database itself (trigger below)
-- once the password really changes, so a student can't skip the step by editing their profile.
alter table public.profiles
  add column must_change_password boolean not null default false;

-- New account: role, section and recitation from the roster; the flag from the account's app metadata, which only
-- the service role (the enrollment script) can set.
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, email, role, course_section, recitation, must_change_password)
  select new.id, lower(new.email), coalesce(r.role, 'student'), r.course_section, r.recitation,
         coalesce((new.raw_app_meta_data ->> 'must_change_password')::boolean, false)
  from (select 1) one left join public.roster r on r.email = lower(new.email);
  return new;
end $$;

-- Roster changes (including recitation) reach people who already have an account.
create or replace function public.apply_roster() returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
  if tg_op = 'DELETE' then
    update public.profiles set role = 'student' where email = old.email;
    return old;
  end if;
  update public.profiles set role = new.role, course_section = new.course_section, recitation = new.recitation
  where email = new.email;
  return new;
end $$;

-- The student chose a password: clear the flag. (tools/enroll.mjs --reset sets it again after it changes one.)
create function public.password_changed() returns trigger
language plpgsql security definer set search_path = ''
as $$
begin
  update public.profiles set must_change_password = false where id = new.id and must_change_password;
  return new;
end $$;
create trigger users_password_changed after update of encrypted_password on auth.users
  for each row when (old.encrypted_password is distinct from new.encrypted_password)
  execute function public.password_changed();

-- Complete = own password chosen, and (for students) a first and last name. Recitation is the instructor's job, so a
-- student without one isn't blocked.
create or replace function public.profile_complete() returns boolean
language sql stable security definer set search_path = ''
as $$
  select exists (
    select 1 from public.profiles p
    where p.id = auth.uid()
      and not p.must_change_password
      and (p.role = 'instructor' or (p.first_name is not null and p.last_name is not null))
  )
$$;
