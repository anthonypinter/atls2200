#!/usr/bin/env node
// Enroll students: create their accounts with a temporary password and set their recitation (and course section).
// Each student must choose their own password the first time they sign in, and give their name if the CSV didn't.
//
//   SUPABASE_SECRET_KEY=… node tools/enroll.mjs students.csv          create accounts for everyone in the file
//   SUPABASE_SECRET_KEY=… node tools/enroll.mjs --reset ab1234@colorado.edu   new temporary password for one student
//   SUPABASE_SECRET_KEY=… node tools/enroll.mjs --check ab1234@colorado.edu   is the account set up? does a password work?
//
// students.csv has a header row with: email, recitation, and optionally section, first_name and last_name. Extra
// columns are ignored. A name given here goes on the student's profile, so they aren't asked for it at first sign-in.
//   email,first_name,last_name,recitation,section
//   ab1234@colorado.edu,Ada,Byron,101,001
//
// The temporary passwords are written to a new file next to the input, e.g. students-passwords-2026-11-19.csv
// (or printed, for --reset). Hand each one out privately, then delete the file. It's gitignored, but don't commit it.
//
// SUPABASE_SECRET_KEY is the project's secret (service_role) key, from Project Settings → API Keys. It bypasses every
// access rule, so keep it in your shell only: never in the repo, a page or a chat. The project URL is read from
// book.js, or from SUPABASE_URL if set. Running the script again is safe: existing accounts keep their password
// (their roster row and recitation are updated), and only new students get one.

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { randomInt } from "node:crypto";
import { basename, dirname, extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const KEY = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;
const URL_ = (process.env.SUPABASE_URL || readFileSync(join(ROOT, "book.js"), "utf8").match(/backend:\s*\{[^}]*url:\s*"([^"]*)"/)?.[1] || "").replace(/\/$/, "");

const die = (msg) => { console.error(msg); process.exit(1); };
if (!KEY) die("Set SUPABASE_SECRET_KEY to the project's secret (service_role) key first. See the top of this file.");
if (!URL_) die("No project URL: set backend.url in book.js, or SUPABASE_URL.");

const headers = { apikey: KEY, "Content-Type": "application/json", ...(KEY.startsWith("eyJ") ? { Authorization: `Bearer ${KEY}` } : {}) };
// fetch on Node 18+; plain http(s) on older Node.
async function request(url, { method, headers, body }) {
  if (globalThis.fetch) { const r = await fetch(url, { method, headers, body }); return { ok: r.ok, status: r.status, statusText: r.statusText, text: await r.text() }; }
  const lib = url.startsWith("https:") ? await import("node:https") : await import("node:http");
  return new Promise((resolve, reject) => {
    const req = lib.request(url, { method, headers }, (res) => {
      let text = "";
      res.setEncoding("utf8").on("data", (c) => (text += c)).on("end", () => resolve({ ok: res.statusCode < 300, status: res.statusCode, statusText: res.statusMessage, text }));
    });
    req.on("error", reject);
    req.end(body);
  });
}
async function api(method, path, body, extra = {}) {
  const res = await request(URL_ + path, { method, headers: { ...headers, ...extra }, body: body && JSON.stringify(body) });
  const text = res.text;
  const data = text ? JSON.parse(text) : null;
  if (!res.ok) throw Object.assign(new Error(data?.msg || data?.message || data?.error_description || text || res.statusText), { status: res.status, data });
  return data;
}

// Easy to read aloud or copy from paper: no 0/O, 1/l/I. 12 characters ≈ 70 bits.
const ALPHA = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const password = () => Array.from({ length: 12 }, (_, i) => (i === 4 || i === 8 ? "-" : "") + ALPHA[randomInt(ALPHA.length)]).join("");

async function findUser(email) {
  for (let page = 1; ; page++) {
    const { users } = await api("GET", `/auth/v1/admin/users?page=${page}&per_page=1000`);
    const u = users.find((x) => x.email?.toLowerCase() === email);
    if (u || users.length < 1000) return u || null;
  }
}
const flag = (id) => api("PATCH", `/rest/v1/profiles?id=eq.${id}`, { must_change_password: true }, { Prefer: "return=minimal" });

function parseCsv(text) {
  const rows = text.split(/\r?\n/).filter((l) => l.trim()).map((l) => l.split(",").map((c) => c.trim().replace(/^"(.*)"$/, "$1")));
  const head = rows.shift()?.map((h) => h.toLowerCase().replace(/[^a-z]/g, "")) || [];
  const col = (...names) => head.findIndex((h) => names.includes(h));
  const e = col("email"), r = col("recitation", "rec"), s = col("section", "coursesection");
  const f = col("firstname", "first", "givenname", "preferredname"), l = col("lastname", "last", "surname", "familyname");
  if (e < 0) die("The CSV needs a header row with an \"email\" column (and \"recitation\", optionally \"section\", \"first_name\" and \"last_name\").");
  // Name keys only when the CSV has those columns, so a CSV without them leaves names already on the roster alone.
  return rows.map((c) => ({
    email: (c[e] || "").toLowerCase(), recitation: r >= 0 ? c[r] || null : null, course_section: s >= 0 ? c[s] || null : null,
    ...(f >= 0 ? { first_name: c[f] || null } : {}), ...(l >= 0 ? { last_name: c[l] || null } : {}),
  }));
}

async function reset(email) {
  email = email.toLowerCase();
  const u = await findUser(email);
  if (!u) die(`No account for ${email}.`);
  const pw = password();
  await api("PUT", `/auth/v1/admin/users/${u.id}`, { password: pw });
  await flag(u.id);   // after the change, since changing the password clears the flag
  console.log(`${email}  ${pw}\nThey'll be asked to choose a new password when they sign in.`);
}

// Why can't someone sign in? Shows the account's state and, if you type one, tests a password (a real sign-in, so it
// counts as their last sign-in). Passwords are stored hashed, so testing is the only way to know if one is right.
async function check(email) {
  email = email.trim().toLowerCase();
  const u = await findUser(email);
  if (!u) {
    const local = email.split("@")[0];
    const { users } = await api("GET", "/auth/v1/admin/users?page=1&per_page=1000");
    const near = users.map((x) => x.email || "").filter((e) => e.includes(local) || local.includes(e.split("@")[0]));
    die(`No account for ${email}.` + (near.length ? `\nSimilar accounts:\n  ${near.join("\n  ")}` : "")
      + "\nIf the script listed it under \"Failed\" when you enrolled, run the enrollment again (non-CU addresses need migration 0006 first).");
  }
  const [prof] = await api("GET", `/rest/v1/profiles?id=eq.${u.id}&select=role,first_name,last_name,recitation,must_change_password`);
  const [rost] = await api("GET", `/rest/v1/roster?email=eq.${encodeURIComponent(email)}&select=role,recitation`);
  const when = (t) => (t ? new Date(t).toLocaleString() : "never");
  console.log([
    `Account:        ${u.email} (created ${when(u.created_at)})`,
    `Confirmed:      ${u.email_confirmed_at ? "yes" : "NO: they can't sign in until it is (Authentication → Users → Confirm)"}`,
    `Blocked:        ${u.banned_until && new Date(u.banned_until) > new Date() ? `YES, until ${when(u.banned_until)}` : "no"}`,
    `Last sign-in:   ${when(u.last_sign_in_at)}`,
    `Password:       ${!prof ? "(no profile)" : prof.must_change_password ? "still the temporary one" : "they've chosen their own, so the temporary one no longer works"}`,
    `Name:           ${prof && prof.first_name ? `${prof.first_name} ${prof.last_name || ""}` : "not given yet"}`,
    `Roster:         ${rost ? `${rost.role}, recitation ${rost.recitation || "none"}` : "NOT on the roster"}`,
  ].join("\n"));

  const { createInterface } = await import("node:readline");
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const pw = await new Promise((r) => rl.question("\nPassword to test (Enter to skip): ", (a) => { rl.close(); r(a.trim()); }));
  if (!pw) return;
  const anon = readFileSync(join(ROOT, "book.js"), "utf8").match(/anonKey:\s*"([^"]*)"/)?.[1];
  if (!anon) die("No anonKey in book.js, so the password can't be tested.");
  const res = await request(`${URL_}/auth/v1/token?grant_type=password`, { method: "POST", headers: { apikey: anon, "Content-Type": "application/json" }, body: JSON.stringify({ email, password: pw }) });
  if (res.ok) console.log("That password WORKS. Check what they're typing: the email, capitals, the dashes, and that it's on the site's Sign in button.");
  else console.log(`That password does NOT work (${JSON.parse(res.text || "{}").msg || JSON.parse(res.text || "{}").error_description || res.status}).\nGive them a new one with: --reset ${email}`);
}

async function enroll(file) {
  const people = parseCsv(readFileSync(file, "utf8"));
  const bad = people.filter((p) => !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(p.email));
  if (bad.length) die(`Not email addresses, fix these first:\n  ${bad.map((p) => p.email || "(blank)").join("\n  ")}`);
  const badRec = people.filter((p) => p.recitation && !/^[A-Za-z0-9 _-]{1,12}$/.test(p.recitation));
  if (badRec.length) die(`Recitations must be 1–12 letters, numbers, spaces, - or _:\n  ${badRec.map((p) => `${p.email}: ${p.recitation}`).join("\n  ")}`);
  const badName = people.filter((p) => [p.first_name, p.last_name].some((n) => n && n.length > 60));
  if (badName.length) die(`Names can be at most 60 characters:\n  ${badName.map((p) => p.email).join("\n  ")}`);

  // Recitations first (the roster refers to them), then the roster, so a new account picks up its row. No role is
  // sent: new rows default to student, and an instructor or TA already on the roster keeps their role.
  const recs = [...new Set(people.map((p) => p.recitation).filter(Boolean))];
  if (recs.length) await api("POST", "/rest/v1/recitations?on_conflict=code", recs.map((code) => ({ code })), { Prefer: "resolution=ignore-duplicates,return=minimal" });
  await api("POST", "/rest/v1/roster?on_conflict=email", people, { Prefer: "resolution=merge-duplicates,return=minimal" });

  const out = [["email", "first_name", "last_name", "recitation", "temporary_password"]], existing = [], failed = [];
  for (const p of people) {
    const pw = password();
    try {
      const u = await api("POST", "/auth/v1/admin/users", { email: p.email, password: pw, email_confirm: true, app_metadata: { must_change_password: true } });
      await flag(u.id);   // the new profile has it already; this makes sure, whatever order Supabase writes the account in
      out.push([p.email, p.first_name || "", p.last_name || "", p.recitation || "", pw]);
    } catch (err) {
      if (err.status === 422 || /already/i.test(err.message)) existing.push(p.email);
      else failed.push(`${p.email}: ${err.message}`);
    }
  }

  if (out.length > 1) {
    let dest = join(dirname(file), `${basename(file, extname(file))}-passwords-${new Date().toISOString().slice(0, 10)}.csv`);
    for (let n = 2; existsSync(dest); n++) dest = dest.replace(/(-\d+)?\.csv$/, `-${n}.csv`);
    writeFileSync(dest, out.map((r) => r.join(",")).join("\n") + "\n", { mode: 0o600 });
    console.log(`Created ${out.length - 1} account(s). Temporary passwords: ${dest}\nHand them out privately, then delete the file.`);
  } else console.log("No new accounts.");
  if (existing.length) console.log(`Already had an account (roster updated, password unchanged): ${existing.length}\n  ${existing.join("\n  ")}\n  Use --reset <email> for a new temporary password.`);
  if (failed.length) { console.error(`Failed:\n  ${failed.join("\n  ")}`); process.exitCode = 1; }
}

const args = process.argv.slice(2);
try {
  if (args[0] === "--reset" && args[1]) await reset(args[1]);
  else if (args[0] === "--check" && args[1]) await check(args[1]);
  else if (args[0] && !args[0].startsWith("-")) await enroll(args[0]);
  else die("Usage: node tools/enroll.mjs students.csv   or   --reset ab1234@colorado.edu   or   --check ab1234@colorado.edu");
} catch (err) { die(`Stopped: ${err.message}`); }
