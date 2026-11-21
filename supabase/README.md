# Backend: student accounts and instructor notes

The book works without any of this. Until `book.js` has a backend `url`, nobody can sign in and each browser keeps its own progress.

With the backend:

- **Students** sign in with the email you enrolled them with (any address) and a password. Instructors create the accounts with `tools/enroll.mjs`, which gives each student a temporary password and their recitation; there's no self sign-up. On first sign-in a student must choose their own password and give their first and last name. "Forgot your password?" emails a reset link (if email sending is set up). Their progress syncs to their account: lessons visited and completed, every section seen and used, quiz answers and best scores, exercise drafts and passes. Signed out, the book works as before, and that work is added to their account the first time they sign in.
- **Instructors** see notes inside the lessons and use the dashboard at `instructor.html`. The dashboard has class progress by part and lesson, one student's progress section by section, CSV export, a notes editor and the roster.
- **Instructor content stays private.** The notes live only in the database, and the database refuses them to anyone who isn't an instructor. The public pages and `instructor.html` contain no data.

## One-time setup

1. **Create a project** at [supabase.com](https://supabase.com) (the free tier is enough for a course). Pick a US region.
2. **Run the schema.** Open SQL Editor → New query, paste all of `migrations/0001_accounts_progress_notes.sql`, and press Run. Then do the same with `migrations/0002_events_and_time.sql`, `migrations/0003_student_details.sql`, `migrations/0004_enrollment.sql`, `migrations/0005_roster_names.sql` and `migrations/0006_any_email.sql`, in that order. You can also run `supabase db push` if you use the Supabase CLI.
3. **Make yourself an instructor.** In the SQL editor:
   ```sql
   insert into public.roster (email, role) values ('you@colorado.edu', 'instructor');
   ```
   You can add other instructors and TAs the same way, or later from the dashboard's Roster section.
4. **Recitations** are assigned by you, on the roster. `tools/enroll.mjs` adds any it finds in your CSV; add descriptions on the dashboard (Roster → Recitations) or here:
   ```sql
   insert into public.recitations (code, label, sort) values ('101', 'Tue 9:00', 1), ('102', 'Wed 14:00', 2);
   ```
   Students see their recitation but can't change it.
5. **Allow the password-reset links.** Go to Authentication → URL Configuration:
   - Site URL: `https://anthonypinter.com/atls2200/`
   - Redirect URLs: `https://anthonypinter.com/atls2200/**` and, for testing, `http://localhost:8765/**`
6. **Set up email sending (optional).** The only email is the "Forgot your password?" link. Supabase's built-in email reaches only members of your Supabase team, so without a provider (Authentication → Emails → SMTP Settings: Resend, Postmark, SendGrid, Amazon SES or a university relay), reset passwords yourself with `node tools/enroll.mjs --reset <email>`.
7. **Close sign-up.** In Authentication → Sign In / Providers, turn off "Allow new users to sign up" (keep the Email provider enabled) and set the minimum password length to 8. Create your own account under Authentication → Users → Add user → Create new user, with **Auto Confirm User** ticked.
8. **Connect the book.** In Project Settings → API (or Data API), copy the Project URL and the `anon` `public` key into `book.js` **and** `book-2.js` (the same values in both: the two books share accounts, and the dashboard signs in through `book.js`):
   ```js
   backend: { url: "https://ptbpvlpgkeexeravimyb.supabase.co", anonKey: "sb_publishable_XIPvbndBK5H6lbaNd5sDNg_66iyiHGy" },
   ```
   Commit and push. The anon key is designed to be public, because the database's row-level security decides what each person can see. **Never put the `service_role` key in the repo or any page.** It bypasses every rule.

9. **Enroll the students.** With a CSV whose header is `email,recitation,section` (section optional), run `SUPABASE_SECRET_KEY='…' node tools/enroll.mjs students.csv` with the secret (`service_role`) key from Project Settings → API Keys. It creates the accounts, fills the roster, and writes the temporary passwords to `students-passwords-<date>.csv` next to your file (gitignored). Hand them out privately and delete the file. Re-running it is safe, and `--reset <email>` gives one student a new temporary password. Keep the secret key in your shell only.

To test locally, run `python3 -m http.server 8765` in the repo, open `http://localhost:8765/`, and sign in.

## Completion in Core Web Development (Book 2)

Book 2 has no Mark complete button. Each lesson shows the student a meter: how many of its items are done, where an item is a section read (and, for Play, Try it, Practice and Check yourself sections, used), a quiz finished (any score) or an exercise passed. At 100% the lesson completes itself and is ticked in the sidebar. The dashboard (`instructor.html`, which opens on Book 2; `?book=1` shows the Field Guide) counts the same items from `search-index-2.js`, so its percentages match what students see. Its CSV has one row per student per lesson, with the week and the percent.

## Who can see what

| | Student | Instructor | Signed out |
|---|---|---|---|
| Own progress | read and write | read and write | — |
| Everyone's progress | — | read | — |
| Own profile | read; change own first name and last name only | read | — |
| Recitations list | read | read and write | — |
| Roster | — | read and write | — |
| Instructor notes | — | read and write | — |

Roles come from the roster. If an email is on it as `instructor`, that person becomes an instructor right away, or as soon as they first sign in. Everyone else is a student. Only you create accounts, for any email address (migration 0006). Self sign-up is off, so an address can sign in only if you made an account for it.

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
