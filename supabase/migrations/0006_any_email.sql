-- Any email address can have an account, not only @colorado.edu. Run after 0001–0005.
--
-- Self sign-up stays off (Authentication → Sign In / Providers), so the only accounts are the ones you create with
-- tools/enroll.mjs or the Supabase dashboard. Signing in still needs an existing account and its password.

drop trigger if exists users_email_domain on auth.users;
drop function if exists public.check_email_domain();
