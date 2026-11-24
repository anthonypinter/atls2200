# Enrolling students

How student accounts work on the course site, and how you create them. Set up the backend first (`BACKEND-SETUP.md`): this assumes the Supabase project exists, all four migrations have run (including `supabase/migrations/0004_enrollment.sql`) and `book.js` has the backend `url`.

## How it works

- **You create every account.** Students can't sign themselves up. Each account gets a random temporary password and the recitation you assign.
- **First sign-in has two required steps.** The student signs in with the temporary password, then:
  1. chooses their own password (at least 8 characters, and not the temporary one);
  2. gives their first and last name.

  Until both are done, nothing they do is saved to their account. Their work stays in the browser and uploads once they finish, so nothing is lost.
- **Students see their recitation but can't change it.** If it's wrong, you fix it (see "Changing a recitation or section").
- **After that, they sign in with email and password.** The Account dialog also has **Change password**, **Edit your name** and **Forgot your password?** (the last works only if email sending is set up; see "Locked-out students").

The password step can't be skipped. The database turns the "must change password" flag off only when the password really changes, so tinkering in the browser doesn't get around it.

## One-time Supabase settings

In the Supabase dashboard:

- [ ] **Authentication → Sign In / Providers:** turn **off** "Allow new users to sign up". Leave the **Email** provider enabled, since password sign-in uses it.
- [ ] On the Email provider, set **Minimum password length** to 8. Turn on **Prevent use of leaked passwords** if your plan offers it.
- [ ] **Your own account:** you must be on the roster as `instructor` (step 3 of `BACKEND-SETUP.md`). Then go to **Authentication → Users → Add user → Create new user**, enter your email and a password, and tick **Auto Confirm User**. TAs are set up the same way.

## Enrolling a class

### 1. Make the CSV

The CSV needs a header row. `email` is required, `recitation` is what you assign, and `section` (the course section) is optional. Any other columns are ignored, so a trimmed export from Canvas or the registrar works.

```csv
email,recitation,section
ab1234@colorado.edu,101,001
cd5678@colorado.edu,102,001
```

- Emails must be `@colorado.edu`. The script stops and lists any that aren't, before changing anything.
- A recitation code is 1–12 letters, numbers, spaces, `-` or `_`. You don't have to add recitations in advance, because the script creates any it hasn't seen. To give them descriptions, such as "Tue 9:00, ATLS 104", use the dashboard: Roster → Recitations.

Keep the CSV outside the repo, for example on your Desktop.

### 2. Get the secret key

In **Project Settings → API Keys**, copy the **secret** key (called `service_role` on older projects).

> This key bypasses every access rule in the database. Use it only in your terminal. Never put it in the repo, a web page, an email or a chat.

### 3. Run the script

From the repo folder:

```sh
SUPABASE_SECRET_KEY='...' node tools/enroll.mjs ~/Desktop/students.csv
```

It does three things:

1. adds any new recitations;
2. puts everyone on the roster with their recitation and section;
3. creates an account for each student who doesn't have one yet.

It prints how many accounts it created, and lists anyone who already had one.

### 4. Hand out the passwords

The temporary passwords are written next to your CSV, as `students-passwords-<date>.csv`:

```csv
email,recitation,temporary_password
ab1234@colorado.edu,101,5WEu-aRpE-CDM2
```

- Give each student their own password privately: a printed slip in recitation or an individual Canvas message. Don't post the list where others can see it.
- The passwords avoid characters that are easy to confuse (`0`/`O`, `1`/`l`/`I`), so they're safe to copy from paper.
- **Delete the file** once the passwords are handed out. Only your user account can open it, and git ignores it (`.gitignore`: `*-passwords-*.csv`), but don't keep it around.

Tell students: "Go to the course site, press **Sign in**, use your CU email and this temporary password. You'll be asked to choose your own password and enter your name."

## Later in the term

### Adding students

Add them to the CSV, or make a new CSV with only the new students, and run the script again. Re-running is safe:

- students who already have an account keep their password;
- only new students get an account and a temporary password, in a new passwords file;
- everyone's recitation and section are updated to match the CSV.

### Changing a recitation or section

You can do this any of these ways:

- edit the CSV and re-run the script;
- on the dashboard, use Roster → People and re-add the line as `email, section, recitation`;
- in the SQL Editor, run `update public.roster set recitation = '102' where email = 'ab1234@colorado.edu';`

The student's profile follows the roster automatically.

Note: a CSV with no `section` column clears the section for everyone in it. Include the column if you use sections.

### Locked-out students

```sh
SUPABASE_SECRET_KEY='…' node tools/enroll.mjs --reset ab1234@colorado.edu
```

This prints a new temporary password. When the student signs in with it, they have to choose their own password again.

**Forgot your password?** in the Account dialog emails the student a reset link. That only works once an email provider is connected: Authentication → Emails → SMTP Settings, then Resend, Postmark, SendGrid, Amazon SES or a CU relay. Supabase's built-in email reaches only members of your Supabase team. For one class, `--reset` is enough.

### Removing a student

**Authentication → Users**, then delete the user. Their profile and progress are removed too. Removing them from the dashboard roster alone keeps their account and progress.

## Checking who's set up

The dashboard's **Roster → People** table has a **Set up** column:

| Shows | Meaning |
|---|---|
| no account | On the roster, but no account was created (added on the dashboard, not by the script) |
| not yet | Hasn't signed in and changed the temporary password |
| password only | Chose a password but hasn't given a name yet |
| yes | Done; progress is being saved |

The class grid also marks students with "(no details yet)" until they've given their name.

## Troubleshooting

| Problem | Fix |
|---|---|
| `Set SUPABASE_SECRET_KEY…` | The key wasn't passed. Put `SUPABASE_SECRET_KEY='…'` before `node` on the same line. |
| `No project URL` | `book.js` has no backend `url` yet. Finish `BACKEND-SETUP.md` step 8, or add `SUPABASE_URL='https://xxxx.supabase.co'` to the command. |
| `Stopped: Invalid API key` or a 401 | You pasted the publishable/anon key. Use the **secret** key. |
| `Not @colorado.edu addresses…` | Fix or remove those lines; nothing was changed. |
| A student's sign-in says the email and password don't match | Check for typos (passwords are case-sensitive). Otherwise use `--reset`. |
| "Choose a new password, not the one you were given" | The student typed the temporary password again as their new one. |

## What's where

| File | Role |
|---|---|
| `tools/enroll.mjs` | The enrollment and `--reset` script (works on Node 16 and newer) |
| `supabase/migrations/0004_enrollment.sql` | Recitation on the roster, the must-change-password flag and the trigger that clears it, and the rule that nothing saves until setup is done |
| `js/backend.js` | The Account dialog: sign-in, forced password change, name, change password, forgot password |
| `instructor.html` | Dashboard roster with the Recitation and Set up columns |
| `BACKEND-SETUP.md`, `supabase/README.md` | Full backend setup and who-can-see-what |
