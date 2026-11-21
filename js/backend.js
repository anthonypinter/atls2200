/* Accounts: sign-in, progress sync and instructor notes, on top of the Supabase project set in book.js (backend).
   js/chrome.js loads this file only when a backend is configured. The book never depends on it: signed out (or
   offline, or if Supabase is down) everything still works and progress stays in this browser, as before.

   - Sign in: an Account button in the top bar opens a dialog. Students sign in with their university email and a
     password. Instructors create the accounts (tools/enroll.mjs) with a temporary password and the student's
     recitation; there's no self sign-up. "Forgot your password?" emails a reset link that opens a new-password step.
   - First sign-in: the dialog makes the student choose their own password (profiles.must_change_password, cleared by
     the database when the password really changes), then give their first and last name. The database won't store
     a student's progress or activity before both are done (supabase/migrations/0003, 0004), so nothing syncs until
     then; work stays in the browser.
   - Sync: once signed in, this browser's progress (js/progress.js) is merged with the account's copy using
     Progress.merge, saved back to both, and kept in step after every change. The queued activity log is uploaded to
     the events table and removed from the browser once stored. The attempts list isn't uploaded (the log has every
     attempt), which keeps the synced copy small. Work done signed out is added to the
     account the first time its owner signs in. Signing out clears this browser's copy (it's safe in the account), so
     the next person on a shared computer starts fresh.
   - Instructors: notes from the instructor_notes table appear in the lesson, marked as visible only to instructors,
     and the dialog links to the dashboard (instructor.html). Students' requests for notes return nothing: the
     database refuses them (supabase/migrations), so the notes never reach a student's browser.

   The Supabase library (about 110 KB) loads only for someone who is signing in or already signed in.
   window.Backend, for instructor.html: ready() resolves to the Supabase client once a session is known (or null),
   user and profile are the signed-in person, onChange(fn) runs fn after sign-in, sign-out and each sync,
   openDialog() shows the Account dialog. */
(function () {
  const cfg = window.BOOK?.backend;
  const P = window.Progress;
  if (!cfg?.url || !cfg.anonKey || !P) return;

  const LIB = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js";
  const OWNER = "book:owner";        // whose progress this browser holds, so one student's work never joins another's
  const SYNC_DELAY = 4000;           // wait this long after a change, so a burst of changes is one sync
  const SYNC_EVERY = 30000;          // and sync at most this often while reading (reading time changes constantly)
  const EVENT_BATCH = 200;
  const KINDS = new Set(["visit", "seen", "time", "used", "run", "answer", "quiz-done", "check", "complete", "uncomplete"]);
  const domain = (cfg.emailDomain || "").toLowerCase();
  const PROFILE_COLS = "email, display_name, role, course_section, first_name, last_name, recitation, must_change_password";
  const ref = new URL(cfg.url).hostname.split(".")[0];
  const store = {
    get: (k) => { try { return localStorage.getItem(k); } catch { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch {} },
    del: (k) => { try { localStorage.removeItem(k); } catch {} },
  };
  const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  // Key order differs between the browser and Postgres (jsonb sorts keys), so compare with sorted keys.
  const canon = (v) => JSON.stringify(v, (k, x) => (x && typeof x === "object" && !Array.isArray(x) ? Object.fromEntries(Object.entries(x).sort()) : x));

  const B = window.Backend = { client: null, user: null, profile: null, status: "signed-out", lastSync: null };
  const listeners = new Set();
  B.onChange = (fn) => { listeners.add(fn); return () => listeners.delete(fn); };
  const changed = () => { paintButton(); paintDialog(false); listeners.forEach((fn) => fn(B)); };

  // Only load the library when it's needed: a saved session, a confirmation or reset link just opened, or a click on Account.
  const hasSession = () => !!store.get(`sb-${ref}-auth-token`);
  const fromLink = () => /[#&](access_token|error_description)=/.test(location.hash);
  let starting = null;
  function start() {
    return starting ||= loadScript(LIB).then(() => {
      const db = B.client = window.supabase.createClient(cfg.url, cfg.anonKey, {
        auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, flowType: "implicit" },
      });
      return new Promise((resolve) => {
        db.auth.onAuthStateChange((event, session) => {
          if (event === "PASSWORD_RECOVERY") { recovering = true; setTimeout(openDialog); }
          // Supabase holds a lock during this callback, so database calls wait for the next tick.
          setTimeout(async () => {
            if (session?.user && session.user.id !== B.user?.id) await signedIn(session.user);
            else if (!session && B.user) signedOut(false);
            if (event === "INITIAL_SESSION") resolve(db);
          });
        });
      });
    }).catch((e) => { console.warn("Accounts unavailable:", e.message); B.status = "error"; changed(); return null; });
  }
  B.ready = () => (hasSession() || fromLink() || starting ? start() : Promise.resolve(null));

  async function signedIn(user) {
    B.user = user;
    B.status = "syncing";
    changed();
    const { data } = await B.client.from("profiles").select(PROFILE_COLS).eq("id", user.id).maybeSingle();
    B.profile = data || { email: user.email, role: "student" };
    // Progress from a different account (say a session that expired without signing out) stays out of this one.
    const owner = store.get(OWNER);
    if (owner && owner !== user.id) P.replace(null);
    store.set(OWNER, user.id);
    if (fromLink()) history.replaceState(null, "", location.pathname + location.search);
    if (needsSetup()) { B.status = "details"; changed(); openDialog(); return; }
    await sync();
    if (B.profile.role === "instructor") showNotes();
  }
  // clear: an explicit Sign out. A session that ends on its own (expired, revoked) leaves the work in place: if the
  // same person signs in again it's merged, and if someone else does, OWNER keeps it out of their account.
  function signedOut(clear) {
    B.user = B.profile = null;
    B.status = "signed-out";
    if (clear) { store.del(OWNER); P.replace(null); }
    document.querySelectorAll(".inst-note").forEach((n) => n.remove());
    changed();
  }

  // Sync: read the account's copy, merge, write whichever side is behind. Every change schedules one; they never overlap.
  let timer = null, running = null, again = false, applying = false;
  // Before anything is saved: their own password in place of the temporary one, then (students) their name.
  const needsPassword = () => !!B.profile?.must_change_password;
  function needsDetails() {
    const p = B.profile;
    return !!p && p.role !== "instructor" && (!p.first_name || !p.last_name);
  }
  const needsSetup = () => needsPassword() || needsDetails();
  async function saveDetails(form) {
    const val = (n) => form.elements[n]?.value.trim().replace(/\s+/g, " ") || null;
    const row = { first_name: val("first"), last_name: val("last") };
    if (!row.first_name || !row.last_name) throw new Error("Please enter your first and last name.");
    const { data, error } = await B.client.from("profiles").update(row).eq("id", B.user.id).select(PROFILE_COLS).single();
    if (error) throw error;
    B.profile = data;
    editing = false;
    B.status = "syncing";
    changed();
    await sync();
  }

  async function sync() {
    if (!B.user || needsSetup()) return;
    if (running) { again = true; return running; }
    running = (async () => {
      try {
        const db = B.client;
        const { data: row, error } = await db.from("progress").select("data").eq("user_id", B.user.id).maybeSingle();
        if (error) throw error;
        const local = P.data();
        const merged = row?.data ? P.merge(local, row.data) : local;
        if (canon(merged) !== canon(local)) { applying = true; P.replace(merged); applying = false; }
        const upload = { ...merged, attempts: [] };
        if (!row || canon(upload) !== canon({ ...row.data, attempts: [] })) {
          const { error: e } = await db.from("progress").upsert({ user_id: B.user.id, data: upload });
          if (e) throw e;
        }
        await sendEvents(db);
        B.status = "synced";
        B.lastSync = new Date();
      } catch (e) {
        console.warn("Progress sync failed:", e.message);
        B.status = "error";
      }
    })();
    await running;
    running = null;
    changed();
    if (again) { again = false; schedule(); }
  }
  B.sync = sync;
  let lastRun = 0;
  function schedule() {
    clearTimeout(timer);
    timer = B.user ? setTimeout(() => { timer = null; lastRun = Date.now(); sync(); }, Math.max(SYNC_DELAY, SYNC_EVERY - (Date.now() - lastRun))) : null;
  }
  // Upload the activity log in batches. A retry of events already stored is ignored by the server (same client_id).
  async function sendEvents(db) {
    const queue = P.events().slice(0, EVENT_BATCH);
    if (!queue.length) return;
    const rows = queue.filter((e) => KINDS.has(e.kind)).map((e) => ({ client_id: e.id, client_at: e.at, lesson: e.lesson, kind: e.kind, target: e.target, detail: e.detail }));
    const { error } = rows.length ? await db.from("events").upsert(rows, { onConflict: "user_id,client_id", ignoreDuplicates: true }) : { error: null };
    // A batch the database rejects as malformed (codes 22xxx/23xxx) would fail forever, so it's dropped; anything
    // else (offline, rate limit) stays queued for the next sync.
    if (error && !/^2[23]/.test(error.code || "")) throw error;
    if (error) console.warn("Activity events dropped:", error.message);
    applying = true; P.dropEvents(queue.map((e) => e.id)); applying = false;
    if (P.events().length) again = true;
  }
  // Throttled, not debounced: steady typing or reading still syncs every SYNC_EVERY.
  P.subscribe(() => { if (!applying && !timer) schedule(); });
  addEventListener("visibilitychange", () => { if (document.visibilityState === "hidden" && timer) { clearTimeout(timer); timer = null; sync(); } });
  addEventListener("online", schedule);

  const here = () => location.origin + location.pathname;
  async function client() {
    const db = await start();
    if (!db) throw new Error("Couldn't reach the sign-in service. Check your connection and try again.");
    return db;
  }
  async function signInPassword(email, password) {
    const { error } = await (await client()).auth.signInWithPassword({ email, password });
    if (error) throw error;
  }
  async function sendReset(email) {
    const { error } = await (await client()).auth.resetPasswordForEmail(email, { redirectTo: here() });
    if (error) throw error;
  }
  async function setPassword(password) {
    const { error } = await B.client.auth.updateUser({ password });
    if (error) throw error;
    // The database clears must_change_password itself when the password changes; read it back rather than assume.
    const { data } = await B.client.from("profiles").select(PROFILE_COLS).eq("id", B.user.id).maybeSingle();
    if (data) B.profile = data;
    if (!needsSetup()) { B.status = "syncing"; changed(); sync(); }
  }
  async function signOut() {
    // Someone who signs out before finishing the first-sign-in steps keeps their work here: none of it is saved yet.
    const keep = needsSetup();
    clearTimeout(timer);
    timer = null;
    await sync();
    for (let i = 0; i < 5 && P.events().length && B.status !== "error"; i++) await sync();   // send the whole log first
    await B.client.auth.signOut();
    signedOut(!keep);
  }

  // Instructor notes: one aside under each section heading they belong to, or under the page header for the lesson.
  async function showNotes() {
    const slug = P.page;
    if (!window.BOOK.lessons?.some((l) => l.slug === slug)) return;
    const { data, error } = await B.client.from("instructor_notes").select("id, section, body, updated_at").eq("lesson", slug).order("id");
    if (error || !data) return;
    document.querySelectorAll(".inst-note").forEach((n) => n.remove());
    for (const n of data) {
      const head = n.section && document.getElementById(n.section);
      const anchor = head ? (head.closest(".section-title") || head) : document.querySelector(".wrap > .page-head");
      if (!anchor) continue;
      const aside = document.createElement("aside");
      aside.className = "inst-note";
      aside.setAttribute("aria-label", "Instructor note");
      aside.innerHTML = `<p class="inst-note-label">Instructor note · only instructors see this <a href="instructor.html?lesson=${encodeURIComponent(slug)}#notes">Edit</a></p>`;
      for (const para of n.body.split(/\n\s*\n/)) {
        const p = document.createElement("p");
        p.textContent = para.trim();
        aside.append(p);
      }
      anchor.after(aside);
    }
  }
  B.showNotes = showNotes;

  // The Account button and dialog.
  // step (signed out): "signin", "forgot" or "reset-sent". recovering: opened a reset link. changingPw: chose to.
  let button = null, dialog = null, step = "signin", sentTo = "", message = "", editing = false, recovering = false, changingPw = false;
  const MIN_PW = 8;
  function paintButton() {
    if (!button) return;
    const label = !B.user ? "Sign in" : B.status === "details" ? "Account · finish signing in" : B.status === "error" ? "Account · not synced" : "Account";
    button.innerHTML = `<span aria-hidden="true">${B.user ? "●" : "○"}</span> ${label}`;
    button.classList.toggle("signed-in", !!B.user);
    button.classList.toggle("sync-error", B.status === "error" || B.status === "details");
  }
  const TRACKED = "What's saved, and seen by your instructors: which sections you read and for how long (only while the page is open and you're active), what you try in the playgrounds and editors, your quiz answers, and your exercise code and Check results.";
  const when = (d) => d ? d.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }) : "";
  // Rebuilds only when the dialog moves to another step (or force), so a background sync doesn't steal focus.
  function paintDialog(force) {
    if (!dialog) return;
    const body = dialog.querySelector(".acct-body");
    const mode = !B.user ? step : recovering || changingPw || needsPassword() ? "new-password" : needsDetails() || editing ? "details" : "account";
    const state = { syncing: "Saving your progress…", synced: `Progress saved to your account at ${when(B.lastSync)}.`, error: "Couldn't reach your account just now. Your progress is safe in this browser and will be saved when the connection is back." }[B.status] || "";
    if (!force && body.dataset.mode === mode) {
      const status = body.querySelector(".acct-status");
      if (status) status.textContent = state;
      return;
    }
    body.dataset.mode = mode;
    const msg = `<p class="acct-msg" role="alert">${esc(message)}</p>`;
    const pw = (id, label, auto) => `<label for="${id}">${label}</label><input id="${id}" name="${id}" type="password" autocomplete="${auto}" minlength="${auto === "current-password" ? 1 : MIN_PW}" required>`;
    const emailField = `<label for="acct-email">${domain ? "University email" : "Email"}</label><input id="acct-email" name="email" type="email" autocomplete="username" required placeholder="you@${esc(domain || "example.com")}" value="${esc(sentTo)}">`;
    if (mode === "new-password") {
      const first = needsPassword() && !recovering;
      body.innerHTML = `<p>${first ? `Welcome! First, replace the temporary password you were given with one of your own for <strong>${esc(B.user.email)}</strong>. Only you will know it.` : `Choose a new password for <strong>${esc(B.user.email)}</strong>.`}</p>
        <form class="acct-form acct-details" data-act="new-password">${pw("acct-pw", `New password (at least ${MIN_PW} characters)`, "new-password")}${pw("acct-pw2", "Type it again", "new-password")}
        <div class="acct-actions"><button class="btn run" type="submit">Save password</button>${first || recovering ? "" : `<button class="btn" type="button" data-act="cancel-pw">Cancel</button>`}</div></form>
        ${msg}${needsSetup() && !changingPw ? `<p class="acct-fine">Until you finish signing in, your work stays in this browser only.</p><div class="acct-actions"><button class="btn" type="button" data-act="out">Sign out</button></div>` : ""}`;
      return;
    }
    if (mode === "details") {
      const p = B.profile || {}, first = needsDetails();
      body.innerHTML = `<p>${first ? "One more step before your progress can be saved: tell us your name. Your instructors see it next to your progress." : "Update your name."}</p>
        <form class="acct-form acct-details" data-act="details">
          <label for="acct-first">First name</label><input id="acct-first" name="first" autocomplete="given-name" maxlength="60" required value="${esc(p.first_name || "")}">
          <label for="acct-last">Last name</label><input id="acct-last" name="last" autocomplete="family-name" maxlength="60" required value="${esc(p.last_name || "")}">
          ${p.recitation ? `<p class="acct-fine">Recitation ${esc(p.recitation)}. If that's wrong, tell your instructor.</p>` : ""}
          <div class="acct-actions"><button class="btn run" type="submit">Save</button>${first ? "" : `<button class="btn" type="button" data-act="cancel-edit">Cancel</button>`}</div>
        </form>
        <p class="acct-msg" role="alert">${esc(message)}</p>
        ${first ? `<p class="acct-fine">Until you save this, your work stays in this browser only.</p><div class="acct-actions"><button class="btn" type="button" data-act="out">Sign out</button></div>` : ""}`;
      return;
    }
    if (B.user) {
      const p = B.profile || {};
      const rec = p.recitation ? ` · Recitation ${esc(p.recitation)}` : "";
      body.innerHTML = `${message ? `<p role="status"><strong>${esc(message)}</strong></p>` : ""}<p>Signed in as <strong>${esc(p.email || B.user.email)}</strong>${p.role === "instructor" ? " (instructor)" : ""}.</p>
        ${p.role === "instructor" ? "" : `<p>${esc([p.first_name, p.last_name].filter(Boolean).join(" "))}${rec} <button class="btn" type="button" data-act="edit">Edit your name</button></p>`}
        <p class="acct-status" role="status">${esc(state)}</p>
        ${p.role === "instructor" ? `<p><a class="btn" href="instructor.html">Open the instructor dashboard</a></p>` : ""}
        <p class="acct-fine">Signing out removes your progress from this browser. It stays in your account for next time.</p>
        <p class="acct-fine">${TRACKED}</p>
        <div class="acct-actions"><button class="btn" type="button" data-act="sync">Save now</button><button class="btn" type="button" data-act="change-pw">Change password</button><button class="btn" type="button" data-act="out">Sign out</button></div>`;
      return;
    }
    if (mode === "reset-sent") {
      body.innerHTML = `<p>If there's an account for <strong>${esc(sentTo)}</strong>, we've emailed it a link to choose a new password. Open it on this device.</p>
        ${msg}<p><button class="btn" type="button" data-act="to-signin">Back to sign in</button></p>`;
      return;
    }
    if (mode === "forgot") {
      body.innerHTML = `<p>Enter your email and we'll send you a link to choose a new password.</p>
        <form class="acct-form acct-details" data-act="forgot">${emailField}<div class="acct-actions"><button class="btn run" type="submit">Email me a reset link</button></div></form>
        ${msg}<p><button class="btn" type="button" data-act="to-signin">Back to sign in</button></p>`;
      return;
    }
    body.innerHTML = `<p>Sign in to save your progress to your account and pick up where you left off on any computer. Reading works without an account.</p>
      <p class="acct-fine">${TRACKED}</p>
      <form class="acct-form acct-details" data-act="signin">${emailField}${pw("acct-pw", "Password", "current-password")}
      <div class="acct-actions"><button class="btn run" type="submit">Sign in</button><button class="btn" type="button" data-act="to-forgot">Forgot your password?</button></div></form>
      ${msg}<p class="acct-fine">No account yet? Your instructor sets them up and gives you a temporary password.</p>`;
  }
  function openDialog() {
    if (!dialog) {
      dialog = document.createElement("dialog");
      dialog.className = "acct-dialog";
      dialog.setAttribute("aria-labelledby", "acct-title");
      dialog.innerHTML = `<div class="acct-head"><h2 id="acct-title">Your account</h2><button class="btn" type="button" data-act="close" aria-label="Close">✕</button></div><div class="acct-body"></div>`;
      document.body.append(dialog);
      dialog.addEventListener("click", onClick);
      dialog.addEventListener("submit", onSubmit);
    }
    message = "";
    paintDialog(true);
    if (!dialog.open) dialog.showModal();
    start();
  }
  B.openDialog = openDialog;
  async function onClick(e) {
    const act = e.target.closest("[data-act]")?.dataset.act;
    if (e.target === dialog || act === "close") dialog.close();
    if (act?.startsWith("to-")) {
      const typed = dialog.querySelector("#acct-email")?.value.trim();
      if (typed) sentTo = typed.toLowerCase();
      step = act.slice(3); message = ""; paintDialog(true); dialog.querySelector("input")?.focus();
    }
    if (act === "sync") sync();
    if (act === "change-pw" || act === "cancel-pw") { changingPw = act === "change-pw"; message = ""; paintDialog(true); dialog.querySelector("input, button")?.focus(); }
    if (act === "edit" || act === "cancel-edit") { editing = act === "edit"; message = ""; paintDialog(true); dialog.querySelector("input, button")?.focus(); }
    if (act === "out") { await signOut(); dialog.close(); }
  }
  async function onSubmit(e) {
    e.preventDefault();
    const form = e.target, btn = form.querySelector("button");
    btn.disabled = true;
    message = "";
    try {
      const act = form.dataset.act, f = form.elements;
      const email = f.email?.value.trim().toLowerCase();
      if (email && domain && !email.endsWith("@" + domain)) throw new Error(`Use your @${domain} address.`);
      if (f["acct-pw2"] && f["acct-pw"].value !== f["acct-pw2"].value) throw new Error("The two passwords don't match.");
      if (act === "details") {
        await saveDetails(form);
      } else if (act === "signin") {
        sentTo = email;
        await signInPassword(email, f["acct-pw"].value);
        step = "signin";
      } else if (act === "forgot") {
        sentTo = email;
        await sendReset(email);
        step = "reset-sent";
      } else if (act === "new-password") {
        await setPassword(f["acct-pw"].value);
        const wasChanging = changingPw;
        recovering = changingPw = false;
        message = wasChanging ? "Password changed." : "";
      }
    } catch (err) {
      const m = err.message || "";
      message = /rate limit/i.test(m) ? "Too many attempts just now. Wait a minute and try again."
        : /invalid login credentials/i.test(m) ? "That email and password don't match. Try again, or use “Forgot your password?”."
        : /should be different/i.test(m) ? "Choose a new password, not the one you were given."
        : /check constraint/i.test(m) ? "Names can be up to 60 characters." : m;
    }
    btn.disabled = false;
    paintDialog(true);
    dialog.querySelector("input")?.focus();
  }

  function addButton() {
    const tools = document.querySelector(".book-bar .book-tools");
    if (!tools || button) return;
    button = document.createElement("button");
    button.type = "button";
    button.className = "btn book-account";
    button.setAttribute("aria-haspopup", "dialog");
    button.addEventListener("click", openDialog);
    tools.prepend(button);
    paintButton();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", addButton);
  else addButton();
  B.ready();
})();
