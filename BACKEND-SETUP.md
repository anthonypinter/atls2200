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

### 3. Make yourself an instructor
- [ ] In the SQL Editor, run:
  ```sql
  insert into public.roster (email, role) values ('anpi0510@colorado.edu', 'instructor');
  ```
- [ ] Add TAs the same way, or later from the dashboard's Roster section.

### 4. Add recitations (before students sign in)
A student's first sign-in asks for their name and recitation, and nothing they do is saved to the server until they've answered. Recitations can also be added later on the dashboard (Roster → Recitations).
- [ ] Run this with your real numbers and times:
  ```sql
  insert into public.recitations (code, label, sort) values ('101', 'Tue 9:00', 1), ('102', 'Wed 14:00', 2);
  ```

### 5. Allow the sign-in links
In **Authentication → URL Configuration**, set:
- [ ] **Site URL:** `https://anthonypinter.com/atls2200/`
- [ ] **Redirect URLs:** `https://anthonypinter.com/atls2200/**` and `http://localhost:8765/**` (for local testing)

That address comes from `supabase/README.md`. If the live site is somewhere else, use that address instead.

### 6. Set up email sending (don't skip)
Supabase's built-in email only sends a few messages an hour, and only to members of your Supabase team, so a class of 30 signing in at once will get stuck. Supabase also won't let you edit the email templates (step 7) until this is done.
- [ ] In **Authentication → Emails → SMTP Settings**, connect an email provider. Options:
  - **Resend:** probably the easiest, with a free tier. You verify a domain you control, such as anthonypinter.com, by adding a few DNS records.
  - Postmark, SendGrid or Amazon SES.
  - A CU email relay, if OIT offers one for course tools.

### 7. Put the sign-in code in the email
- [ ] In **Authentication → Email Templates → Magic Link**, add a line such as `Or enter this code: {{ .Token }}`. Then a student can open the email on a phone and type the code into a lab computer. If the body won't let you edit it, finish step 6 first.

### 8. Connect the site
- [ ] In **Project Settings → API**, copy the **Project URL** and the **`anon` `public` key**.
- [ ] Put the same values in **both** `book.js` and `book-2.js`. The two books share accounts, and the dashboard signs in through `book.js`:
  ```js
  backend: { url: "https://xxxx.supabase.co", anonKey: "eyJ…", emailDomain: "colorado.edu" },
  ```
  Or paste the two values into a Claude session and ask it to do this step and the local test.

> **Never** put the `service_role` key in the repo, a page or a chat. It bypasses every access rule in the database. The `anon` key is safe to commit, because it's meant to be public: the database's access rules decide what each person can see.

### 9. Test locally
- [ ] Run `python3 -m http.server 8765` in the repo, then open `http://localhost:8765/`.
- [ ] Sign in with your instructor email. The email should arrive, and both the link and the code should work.
- [ ] Open `http://localhost:8765/instructor.html`. It should show **Core Web Development** with your class, and the link at the top switches to the Field Guide.
- [ ] Sign in as a test student with a second CU address, if you have one. Give a name and recitation, do part of a lesson, and check that the percentage shows up on the dashboard.

### 10. Go live
- [ ] Commit and push. The publish workflow rebuilds `search-index.js` and `search-index-2.js` itself.
- [ ] Before the first class, sign in once on the live site to check that the sign-in email arrives.

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
- **Changing the email domain** means changing it in the migration (`check_email_domain`), `book.js` and `book-2.js`.

## Log

Add a dated line for each step and anything that went wrong.

- 2026-11-16: Completion tracking built and tested with a mocked backend (see `BOOK2-LOG.md`, "Completion tracking"). Backend not yet connected.
