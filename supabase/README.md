# Backend: student accounts and instructor notes

The book works without any of this. Until `book.js` has a backend `url`, nobody can sign in and each browser keeps its own progress.

With the backend:

- **Students** sign in with their @colorado.edu email. They get a one-time link and a 6-digit code, and there are no passwords. Their progress syncs to their account: lessons visited and completed, every section seen and used, quiz answers and best scores, exercise drafts and passes. Signed out, the book works as before, and that work is added to their account the first time they sign in.
- **Instructors** see notes inside the lessons and use the dashboard at `instructor.html`. The dashboard has class progress by part and lesson, one student's progress section by section, CSV export, a notes editor and the roster.
- **Instructor content stays private.** The notes live only in the database, and the database refuses them to anyone who isn't an instructor. The public pages and `instructor.html` contain no data.

## One-time setup

1. **Create a project** at [supabase.com](https://supabase.com) (the free tier is enough for a course). Pick a US region.
2. **Run the schema.** Open SQL Editor → New query, paste all of `migrations/0001_accounts_progress_notes.sql`, and press Run. You can also run `supabase db push` if you use the Supabase CLI.
3. **Make yourself an instructor.** In the SQL editor:
   ```sql
   insert into public.roster (email, role) values ('you@colorado.edu', 'instructor');
   ```
   You can add other instructors and TAs the same way, or later from the dashboard's Roster section.
4. **Allow the sign-in links.** Go to Authentication → URL Configuration:
   - Site URL: `https://anthonypinter.com/atls2200/`
   - Redirect URLs: `https://anthonypinter.com/atls2200/**` and, for testing, `http://localhost:8765/**`
5. **Add the code to the email.** Go to Authentication → Email Templates → Magic Link and add a line such as `Or enter this code: {{ .Token }}`. With the code, a student can open the email on a phone and still sign in on a lab computer.
6. **Set up email sending (needed for a class).** Supabase's built-in email sends only a handful of messages an hour, which isn't enough when 30 students sign in at once. Under Authentication → Emails → SMTP Settings, connect a provider such as Resend, Postmark, SendGrid or Amazon SES, or a university relay if OIT provides one.
7. **Connect the book.** In Project Settings → API (or Data API), copy the Project URL and the `anon` `public` key into `book.js`:
   ```js
   backend: { url: "https://xxxx.supabase.co", anonKey: "eyJ…", emailDomain: "colorado.edu" },
   ```
   Commit and push. The anon key is designed to be public, because the database's row-level security decides what each person can see. **Never put the `service_role` key in the repo or any page.** It bypasses every rule.

To test locally, run `python3 -m http.server 8765` in the repo, open `http://localhost:8765/`, and sign in.

## Who can see what

| | Student | Instructor | Signed out |
|---|---|---|---|
| Own progress | read and write | read and write | — |
| Everyone's progress | — | read | — |
| Own profile | read; change display name only | read | — |
| Roster | — | read and write | — |
| Instructor notes | — | read and write | — |

Roles come from the roster. If an email is on it as `instructor`, that person becomes an instructor right away, or as soon as they first sign in. Everyone else with a university email is a student, and other addresses can't create an account. To use a different email domain, change it in both the migration (`check_email_domain`) and `book.js`.

## What is tracked

Each student has one row in `progress`. It holds the same object that `js/progress.js` keeps in the browser:

- **lessons:** first visit, and when the student pressed Mark complete
- **sections:** for every heading under "On this page", when it was first seen (on screen for 3 seconds) and when it was first used (a click, keypress or edit inside it)
- **quizzes:** current answers and best score
- **exercises:** latest code and when it first passed
- **attempts:** every quiz answer and every press of Check, timestamped

A section is **done** when it has been seen. Sections that ask the student to do something (Play, Try it, Practice, Check yourself, Your turn) must also have been used. The dashboard's percentage for a lesson is the share of its sections done, quizzes finished and exercises passed.

For your own queries in the SQL editor, use the views `lesson_progress`, `section_progress` and `check_results`. They give one row per student per lesson, section or quiz/exercise.

**Treat it as engagement data, not proof.** Students' browsers write their own progress, so a determined student could edit it. Use it to spot who is stuck or behind, not as the only basis for a grade.

## Privacy

This is student education data (FERPA). Keep the project's dashboard access limited to course staff. Don't export the CSV anywhere public. Delete the project, or the rows, after the term according to department policy. If a student asks, you can delete their account in Authentication → Users, which also removes their profile and progress.
