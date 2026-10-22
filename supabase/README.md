# Backend: student accounts and instructor notes

The book works without any of this. Until `book.js` has a backend `url`, nobody can sign in and each browser keeps its own progress.

With the backend:

- **Students** sign in with their @colorado.edu email. They get a one-time link and a 6-digit code, and there are no passwords. Their progress syncs to their account: lessons visited and completed, every section seen and used, quiz answers and best scores, exercise drafts and passes. Signed out, the book works as before, and that work is added to their account the first time they sign in.
- **Instructors** see notes inside the lessons and use the dashboard at `instructor.html`. The dashboard has class progress by part and lesson, one student's progress section by section, CSV export, a notes editor and the roster.
- **Instructor content stays private.** The notes live only in the database, and the database refuses them to anyone who isn't an instructor. The public pages and `instructor.html` contain no data.

## One-time setup

1. **Create a project** at [supabase.com](https://supabase.com) (the free tier is enough for a course). Pick a US region.
2. **Run the schema.** Open SQL Editor → New query, paste all of `migrations/0001_accounts_progress_notes.sql`, and press Run. Then do the same with `migrations/0002_events_and_time.sql` and `migrations/0003_student_details.sql`, in that order. You can also run `supabase db push` if you use the Supabase CLI.
3. **Make yourself an instructor.** In the SQL editor:
   ```sql
   insert into public.roster (email, role) values ('you@colorado.edu', 'instructor');
   ```
   You can add other instructors and TAs the same way, or later from the dashboard's Roster section.
4. **Add your recitations** before students sign in, either on the dashboard (Roster → Recitations) or here:
   ```sql
   insert into public.recitations (code, label, sort) values ('101', 'Tue 9:00', 1), ('102', 'Wed 14:00', 2);
   ```
   The first time a student signs in, they must give their first and last name and pick their recitation from this list. Until they do, nothing they do is saved to the server; it stays in their browser and uploads once they've finished. Students can change their details later in the Account dialog. If the list is empty, students give only their name.
5. **Allow the sign-in links.** Go to Authentication → URL Configuration:
   - Site URL: `https://anthonypinter.com/atls2200/`
   - Redirect URLs: `https://anthonypinter.com/atls2200/**` and, for testing, `http://localhost:8765/**`
6. **Add the code to the email.** Go to Authentication → Email Templates → Magic Link and add a line such as `Or enter this code: {{ .Token }}`. With the code, a student can open the email on a phone and still sign in on a lab computer.
7. **Set up email sending (needed for a class).** Supabase's built-in email sends only a handful of messages an hour, which isn't enough when 30 students sign in at once. Under Authentication → Emails → SMTP Settings, connect a provider such as Resend, Postmark, SendGrid or Amazon SES, or a university relay if OIT provides one.
8. **Connect the book.** In Project Settings → API (or Data API), copy the Project URL and the `anon` `public` key into `book.js`:
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
| Own profile | read; change own first name, last name and recitation only | read | — |
| Recitations list | read | read and write | — |
| Roster | — | read and write | — |
| Instructor notes | — | read and write | — |

Roles come from the roster. If an email is on it as `instructor`, that person becomes an instructor right away, or as soon as they first sign in. Everyone else with a university email is a student, and other addresses can't create an account. To use a different email domain, change it in both the migration (`check_email_domain`) and `book.js`.

## What is tracked

There are two records for each student.

**Progress** (one row in `progress`): the same object `js/progress.js` keeps in the browser. It's fast, works offline, and drives the checkmarks and the dashboard grid.
- **lessons:** first visit, and when the student pressed Mark complete
- **sections:** for every heading under "On this page":
  - **reading time:** counted only while the tab is visible, the section is on screen, and the student has scrolled, typed or moved the pointer in the last minute
  - **seen:** when that time reached the section's bar, which is about 30% of the time it takes to read at 200 words a minute (5 to 90 seconds), or 5 seconds for sections that ask the student to do something
  - **used:** when the student first did what the section asks
- **quizzes:** current answers and best score
- **exercises:** latest code and when it first passed

**Activity log** (`events`): one row for each thing that happened: visit, section seen, reading time, section used, code run (edited or not), quiz answer, quiz finished, Check pressed (with the code when it passed), lesson marked complete. Students can add rows for themselves but can't edit or delete them, and the server stamps each row with the time it arrived. Events are queued in the browser while offline or signed out, then uploaded at the next sign-in.

"Used" means:

| Section | Used when… |
|---|---|
| Play | changed two different playground controls (or the only one) |
| Try it | ran the code after editing it, or typed in a live editor |
| Practice | pressed Check (the exercise column shows whether it passed) |
| Check yourself | answered every question |
| Read, notes and the rest | nothing to do; reading time decides |

A section is **done** when it's seen, and for the four kinds above also used. The dashboard's percentage for a lesson is the share of its sections done, quizzes finished and exercises passed.

The dashboard also shows reading time, the number of Checks before a pass, and an activity log for each student. It flags a pass after under 2 minutes in the lesson, and 5 or more Checks without a pass. To change those, edit `FAST_MS` and `STUCK_CHECKS` in `instructor.html`. The reading thresholds are at the top of `trackSections` in `js/chrome.js`. Once there's real data, compare reading times with section lengths and adjust.

For your own queries in the SQL editor, use the views `lesson_progress`, `section_progress` (with `active_seconds`), `check_results` and `exercise_attempts`.

**Treat it as a signal, not proof.** Exercise checks run in the student's browser, and a determined student could fake progress. The log makes that harder to hide and keeps the code that passed for spot checks. Use it to find who is stuck or rushing, and keep grading in Canvas.

Students are told what's tracked in the sign-in dialog and the Account dialog.

## Privacy

This is student education data (FERPA). Keep the project's dashboard access limited to course staff. Don't export the CSV anywhere public. Delete the project, or the rows, after the term according to department policy. If a student asks, you can delete their account in Authentication → Users, which also removes their profile and progress.
