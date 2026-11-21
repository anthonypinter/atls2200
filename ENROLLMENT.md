# Enrolling students

How student accounts work on the course site, and how you create them. Set up the backend first (`BACKEND-SETUP.md`): this assumes the Supabase project exists, all six migrations have run (including `supabase/migrations/0004_enrollment.sql`, `0005_roster_names.sql` and `0006_any_email.sql`) and `book.js` has the backend `url`.

## How it works

- **You create every account.** Students can't sign themselves up. Each account gets a random temporary password, the recitation you assign and, if you give it, the student's name.
- **First sign-in has two required steps.** The student signs in with the temporary password, then:
  1. chooses their own password (at least 8 characters, and not the temporary one);
  2. gives their first and last name, unless you already put it in the CSV (then this step is skipped).

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

The CSV needs a header row. `email` is required, `recitation` is what you assign, and `section` (the course section), `first_name` and `last_name` are optional. Any other columns are ignored, so a trimmed export from Canvas or the registrar works. Column order doesn't matter, and the headers are forgiving: `First Name`, `first`, `Last Name`, `last` and `surname` all work.

```csv
email,first_name,last_name,recitation,section
ab1234@colorado.edu,Ada,Byron,101,001
cd5678@colorado.edu,Grace,Hopper,102,001
```

- **Names** show on the dashboard straight away, even before the student signs in. Students can still change theirs (to a preferred name, say) with **Edit your name**, and re-running the script won't undo that. A name reaches an existing account only if you change it in the CSV, for example to fix a typo. Don't put commas inside a name: the script splits on every comma.

- Any email address works, not only `@colorado.edu`. The script stops and lists any lines that aren't an email address, before changing anything.
- A recitation code is 1–12 letters, numbers, spaces, `-` or `_`. You don't have to add recitations in advance, because the script creates any it hasn't seen. To give them descriptions, such as "Tue 9:00, ATLS 104", use the dashboard: Roster → Recitations.

Keep the CSV outside the repo, for example on your Desktop.

### 2. Get the secret key

In **Project Settings → API Keys**, copy the **secret** key (called `service_role` on older projects).

> This key bypasses every access rule in the database. Use it only in your terminal. Never put it in the repo, a web page, an email or a chat.

### 3. Run the script

From the repo folder:

```sh
SUPABASE_SECRET_KEY='paste-the-key-here' node tools/enroll.mjs ~/Desktop/students.csv
```

It does three things:

1. adds any new recitations;
2. puts everyone on the roster with their name, recitation and section;
3. creates an account for each student who doesn't have one yet.

It prints how many accounts it created, and lists anyone who already had one.

### 4. Hand out the passwords

The temporary passwords are written next to your CSV, as `students-passwords-<date>.csv`:

```csv
email,first_name,last_name,recitation,temporary_password
ab1234@colorado.edu,Ada,Byron,101,5WEu-aRpE-CDM2
```

- Give each student their own password privately: a printed slip in recitation or an individual Canvas message. Don't post the list where others can see it.
- The passwords avoid characters that are easy to confuse (`0`/`O`, `1`/`l`/`I`), so they're safe to copy from paper.
- **Delete the file** once the passwords are handed out. Only your user account can open it, and git ignores it (`.gitignore`: `*-passwords-*.csv`), but don't keep it around.

Tell students: "Go to the course site, press **Sign in**, use the email I enrolled you with and this temporary password. You'll be asked to choose your own password (and enter your name, if I didn't)."

## Later in the term

### Adding students

Add them to the CSV, or make a new CSV with only the new students, and run the script again. Re-running is safe:

- students who already have an account keep their password;
- only new students get an account and a temporary password, in a new passwords file;
- everyone's recitation and section are updated to match the CSV, and so are names you've changed in it.

### Changing a recitation or section

You can do this any of these ways:

- edit the CSV and re-run the script;
- on the dashboard, use Roster → People and re-add the line as `email, section, recitation` (optionally followed by `first, last`);
- in the SQL Editor, run `update public.roster set recitation = '102' where email = 'ab1234@colorado.edu';`

The student's profile follows the roster automatically.

Note: a CSV with no `section` column clears the section for everyone in it. Include the column if you use sections. (A CSV with no name columns leaves names alone.)

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
| password only | Chose a password but has no name yet (you didn't give one and they haven't either) |
| yes | Done; progress is being saved |

The People table also has a **Name** column, and the class grid lists students by name (Last, First) when there is one, including students who haven't signed in yet. Students with no name show their email, and signed-in ones are marked "(no details yet)".

## Troubleshooting

| Problem | Fix |
|---|---|
| `Set SUPABASE_SECRET_KEY…` | The key wasn't passed. Put `SUPABASE_SECRET_KEY='…'` before `node` on the same line. |
| `No project URL` | `book.js` has no backend `url` yet. Finish `BACKEND-SETUP.md` step 8, or add `SUPABASE_URL='https://xxxx.supabase.co'` to the command. |
| `Stopped: Invalid API key` or a 401 | You pasted the publishable/anon key. Use the **secret** key. |
| `Not email addresses…` | Fix or remove those lines; nothing was changed. |
| A student's sign-in says the email and password don't match | Check for typos (passwords are case-sensitive). Otherwise use `--reset`. |
| "Choose a new password, not the one you were given" | The student typed the temporary password again as their new one. |

## What's where

| File | Role |
|---|---|
| `tools/enroll.mjs` | The enrollment and `--reset` script (works on Node 16 and newer) |
| `supabase/migrations/0004_enrollment.sql` | Recitation on the roster, the must-change-password flag and the trigger that clears it, and the rule that nothing saves until setup is done |
| `supabase/migrations/0005_roster_names.sql` | First and last name on the roster, copied onto the student's profile |
| `supabase/migrations/0006_any_email.sql` | Removes the @colorado.edu-only rule, so any address can have an account |
| `js/backend.js` | The Account dialog: sign-in, forced password change, name, change password, forgot password |
| `instructor.html` | Dashboard roster with the Name, Recitation and Set up columns |
| `BACKEND-SETUP.md`, `supabase/README.md` | Full backend setup and who-can-see-what |
