#!/usr/bin/env node
// Enroll students: create their accounts with a temporary password and set their recitation (and course section).
// Each student must choose their own password, then give their name, the first time they sign in.
//
//   SUPABASE_SECRET_KEY=… node tools/enroll.mjs students.csv          create accounts for everyone in the file
//   SUPABASE_SECRET_KEY=… node tools/enroll.mjs --reset ab1234@colorado.edu   new temporary password for one student
//
// students.csv has a header row with: email, recitation, and optionally section. Extra columns are ignored.
//   email,recitation,section
//   ab1234@colorado.edu,101,001
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
const DOMAIN = "colorado.edu";
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
  if (e < 0) die("The CSV needs a header row with an \"email\" column (and \"recitation\", optionally \"section\").");
  return rows.map((c) => ({ email: (c[e] || "").toLowerCase(), recitation: r >= 0 ? c[r] || null : null, course_section: s >= 0 ? c[s] || null : null }));
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

async function enroll(file) {
  const people = parseCsv(readFileSync(file, "utf8"));
  const bad = people.filter((p) => !/^[^@\s]+@[^@\s]+$/.test(p.email) || !p.email.endsWith("@" + DOMAIN));
  if (bad.length) die(`Not @${DOMAIN} addresses, fix these first:\n  ${bad.map((p) => p.email || "(blank)").join("\n  ")}`);
  const badRec = people.filter((p) => p.recitation && !/^[A-Za-z0-9 _-]{1,12}$/.test(p.recitation));
  if (badRec.length) die(`Recitations must be 1–12 letters, numbers, spaces, - or _:\n  ${badRec.map((p) => `${p.email}: ${p.recitation}`).join("\n  ")}`);

  // Recitations first (the roster refers to them), then the roster, so a new account picks up its row. No role is
  // sent: new rows default to student, and an instructor or TA already on the roster keeps their role.
  const recs = [...new Set(people.map((p) => p.recitation).filter(Boolean))];
  if (recs.length) await api("POST", "/rest/v1/recitations?on_conflict=code", recs.map((code) => ({ code })), { Prefer: "resolution=ignore-duplicates,return=minimal" });
  await api("POST", "/rest/v1/roster?on_conflict=email", people, { Prefer: "resolution=merge-duplicates,return=minimal" });

  const out = [["email", "recitation", "temporary_password"]], existing = [], failed = [];
  for (const p of people) {
    const pw = password();
    try {
      const u = await api("POST", "/auth/v1/admin/users", { email: p.email, password: pw, email_confirm: true, app_metadata: { must_change_password: true } });
      await flag(u.id);   // the new profile has it already; this makes sure, whatever order Supabase writes the account in
      out.push([p.email, p.recitation || "", pw]);
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
  if (existing.length) console.log(`Already had an account (roster and recitation updated, password unchanged): ${existing.length}\n  ${existing.join("\n  ")}\n  Use --reset <email> for a new temporary password.`);
  if (failed.length) { console.error(`Failed:\n  ${failed.join("\n  ")}`); process.exitCode = 1; }
}

const args = process.argv.slice(2);
try {
  if (args[0] === "--reset" && args[1]) await reset(args[1]);
  else if (args[0] && !args[0].startsWith("-")) await enroll(args[0]);
  else die("Usage: node tools/enroll.mjs students.csv   or   node tools/enroll.mjs --reset ab1234@colorado.edu");
} catch (err) { die(`Stopped: ${err.message}`); }
