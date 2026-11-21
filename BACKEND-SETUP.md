# Backend setup log

Started: 2026-11-16. Status: **not started.** Neither `book.js` nor `book-2.js` has a backend `url` yet.

This is the checklist for connecting the Supabase backend, which gives students accounts and progress syncing, and gives you the instructor dashboard. Until it's done, each student's progress stays in their own browser, and `instructor.html` has nothing to show. The full reference, including who can see what, is `supabase/README.md`. Tick items off here as you go, and add notes to the log at the bottom.

## Why it matters

Book 2 grades participation as a **percentage of completion** per lesson. Students see a meter at the bottom of each lesson, and you see the same numbers on the dashboard and in its CSV. The tracking is all built and tested, but it needs this backend to get the data from students' browsers to you.

## Checklist

### 1. Create the project
- [ ] Sign up at [supabase.com](https://supabase.com). The free tier is enough for a class.
- [ ] Create a new project in a **US region**. Save the database password somewhere, though this setup doesn't use it.

### 2. Create the database tables
In **SQL Editor → New query**, paste each file's entire contents and press **Run**, in this order:
- [ ] `supabase/migrations/0001_accounts_progress_notes.sql`
- [ ] `supabase/migrations/0002_events_and_time.sql`
- [ ] `supabase/migrations/0003_student_details.sql`
- [ ] `supabase/migrations/0004_enrollment.sql`
- [ ] `supabase/migrations/0005_roster_names.sql`
- [ ] `supabase/migrations/0006_any_email.sql`

### 3. Make yourself an instructor
- [ ] In the SQL Editor, run:
  ```sql
  insert into public.roster (email, role) values ('anpi0510@colorado.edu', 'instructor');
  ```
- [ ] Add TAs the same way, or later from the dashboard's Roster section.

### 4. Recitations (optional now)
The enrollment script (step 9) adds every recitation in your CSV, so you can skip this. To give them descriptions, add them on the dashboard (Roster → Recitations) or run:
  ```sql
  insert into public.recitations (code, label, sort) values ('101', 'Tue 9:00', 1), ('102', 'Wed 14:00', 2);
  ```

### 5. Allow the password-reset links
In **Authentication → URL Configuration**, set:
- [ ] **Site URL:** `https://anthonypinter.com/atls2200/`
- [ ] **Redirect URLs:** `https://anthonypinter.com/atls2200/**` and `http://localhost:8765/**` (for local testing)

That address comes from `supabase/README.md`. If the live site is somewhere else, use that address instead.

### 6. Set up email sending (don't skip)
The only email the site sends is the "Forgot your password?" reset link. Supabase's built-in email only reaches members of your Supabase team, so without a provider, students can't reset their own password and you'd use `--reset` (step 9) for them instead. That's workable for one class, so this step is optional.
- [ ] In **Authentication → Emails → SMTP Settings**, connect an email provider. Options:
  - **Resend:** probably the easiest, with a free tier. You verify a domain you control, such as anthonypinter.com, by adding a few DNS records.
  - Postmark, SendGrid or Amazon SES.
  - A CU email relay, if OIT offers one for course tools.

### 7. Turn off open sign-up and set the password rules
You create every account yourself (step 9), so nobody else should be able to make one.
- [ ] In **Authentication → Sign In / Providers**, turn **off** "Allow new users to sign up". Leave the **Email** provider itself enabled, since that's what password sign-in uses.
- [ ] On the Email provider, set **Minimum password length** to 8 (the dialog asks for 8). Turn on **Prevent use of leaked passwords** if your plan offers it.
- [ ] Create your own account: **Authentication → Users → Add user → Create new user**, with your email, a password, and **Auto Confirm User** ticked. You're on the roster as instructor (step 3), so you become one right away.

### 8. Connect the site
- [ ] In **Project Settings → API**, copy the **Project URL** and the **`anon` `public` key**.
- [ ] Put the same values in **both** `book.js` and `book-2.js`. The two books share accounts, and the dashboard signs in through `book.js`:
  ```js
  backend: { url: "https://xxxx.supabase.co", anonKey: "eyJ…" },
  ```
  Or paste the two values into a Claude session and ask it to do this step and the local test.

> **Never** put the `service_role` key in the repo, a page or a chat. It bypasses every access rule in the database. The `anon` key is safe to commit, because it's meant to be public: the database's access rules decide what each person can see.

### 9. Enroll the students
The full guide, including handing out passwords, changes during the term and troubleshooting, is `ENROLLMENT.md`.
- [ ] Make a CSV with a header row: `email,recitation,section` (section is optional), one student per line.
- [ ] In **Project Settings → API Keys**, copy the **secret** (`service_role`) key. Then, in the repo:
  ```sh
  SUPABASE_SECRET_KEY='paste-it-here' node tools/enroll.mjs ~/Desktop/students.csv
  ```
  It creates each account with a random temporary password and the recitation, puts everyone on the roster, and writes `students-passwords-<date>.csv` next to your CSV. Hand each password out privately, then delete that file.
- [ ] Running it again with an updated CSV is safe: only new students get accounts, and everyone's recitation and section are updated.
- [ ] A student who's locked out: `SUPABASE_SECRET_KEY=… node tools/enroll.mjs --reset ab1234@colorado.edu` prints a new temporary password, and they'll have to replace it again.

On first sign-in, each student must choose their own password, then give their first and last name. Nothing is saved to their account until both are done. The dashboard's Roster table shows who has finished ("Set up").

### 10. Test locally
- [ ] Run `python3 -m http.server 8765` in the repo, then open `http://localhost:8765/`.
- [ ] Sign in with your instructor account (step 7).
- [ ] Enroll a test student (a second CU address, if you have one) and sign in with the temporary password. You should be made to choose a new password, then give a name.
- [ ] Open `http://localhost:8765/instructor.html`. It should show **Core Web Development** with your class, and the link at the top switches to the Field Guide.
- [ ] As the test student, do part of a lesson and check that the percentage shows up on the dashboard, with the recitation you gave in the CSV.

### 11. Go live
- [ ] Commit and push. The publish workflow rebuilds `search-index.js` and `search-index-2.js` itself.
- [ ] Before the first class, sign in once on the live site.

## Things to know

- **Completion rule:** a lesson's percentage is items done ÷ items on the page. Each of these is one item:
  - a reading section, once it has had enough active reading time;
  - a hands-on section (Play, Try it, Practice, Check yourself), once it's been used;
  - a quiz, once finished, at any score;
  - an exercise, once passed.

  At 100% the lesson marks itself complete. Book 2 has no Mark complete button.
- **Week percentages** on the dashboard are the share of all that week's items, so a lesson with more items counts for more. A straight average of the lesson percentages is a small change if you'd prefer it.
- **CSV:** one row per student per lesson, with `week` and `percent` columns.
- **Data comes from students' browsers**, so treat it as a strong signal, not proof. Reading time can be gamed, but the hands-on items are hard to fake. The dashboard flags suspicious patterns: an exercise passed very quickly, or many Checks without a pass.
- **Any email address** can have an account (migration 0006). To limit sign-in to one domain again, add `emailDomain: "colorado.edu"` to the backend settings in `book.js` and `book-2.js`; the sign-in form and dashboard then enforce it (the database no longer does).

## Log

Add a dated line for each step and anything that went wrong.

- 2026-11-16: Completion tracking built and tested with a mocked backend (see `BOOK2-LOG.md`, "Completion tracking"). Backend not yet connected.
