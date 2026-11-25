/* Class is Live: what live.html (students) and live-host.html (instructor and projector) share.

   - Live.start(render): loads js/backend.js and calls render(state) whenever who's signed in changes. state is
     { B, db, user, profile } (db and user are null when signed out).
   - Live.watch(db, onChange, { every, answers }): calls onChange() when the open session or its questions change
     (Supabase Realtime), and also every `every` ms in case Realtime is blocked or drops. answers: also hear about
     new answers (only instructors receive other people's). Returns a stop function.
   - Live.results(question, results, opts): HTML for a question's results. results comes from the database
     (live_results / live_state in supabase/migrations/0007_live_class.sql) and is totals only, never names.
     opts.correct: mark the correct choice (when results include it). opts.mine: tag the student's own answer.
     opts.hideable: word-cloud words are buttons (data-word) the instructor can press to hide.
   The database decides what each person may see; these pages only draw it. */
(function () {
  const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const LETTERS = "ABCDEF";
  const KINDS = { choice: "Multiple choice", words: "Word cloud", scale: "Scale" };

  function start(render) {
    if (!window.BOOK?.backend?.url) { render({ B: null, db: null, user: null, profile: null, offline: true }); return; }
    loadScript("js/backend.js").then(async () => {
      const B = window.Backend;
      if (!B) return render({ B: null, db: null, user: null, profile: null, offline: true });
      let shown;
      const update = () => {
        // Redraw when the person changes or finishes account setup, not on every background sync.
        const who = B.user ? `${B.user.id}:${B.profile?.role}:${B.status === "details"}` : "out";
        if (who === shown || (B.user && !B.profile)) return;
        shown = who;
        render({ B, db: B.user ? B.client : null, user: B.user, profile: B.profile });
      };
      B.onChange(update);
      await B.ready();
      update();
    });
  }

  function watch(db, onChange, { every = 5000, answers = false } = {}) {
    let timer = null, waiting = null;
    // Many changes at once (a burst of answers) become one refresh.
    const soon = () => { if (!waiting) waiting = setTimeout(() => { waiting = null; onChange(); }, 400); };
    const channel = db.channel("live-" + Math.random().toString(36).slice(2))
      .on("postgres_changes", { event: "*", schema: "public", table: "live_sessions" }, soon)
      .on("postgres_changes", { event: "*", schema: "public", table: "live_questions" }, soon);
    if (answers) channel.on("postgres_changes", { event: "*", schema: "public", table: "live_answers" }, soon);
    channel.subscribe();
    const tick = () => { if (document.visibilityState === "visible") onChange(); };
    timer = setInterval(tick, every);
    const onVis = () => { if (document.visibilityState === "visible") onChange(); };
    document.addEventListener("visibilitychange", onVis);
    return () => { clearInterval(timer); clearTimeout(waiting); document.removeEventListener("visibilitychange", onVis); db.removeChannel(channel); };
  }

  const pct = (n, total) => (total ? Math.round((n / total) * 100) : 0);
  const plural = (n, one, many = one + "s") => `${n} ${n === 1 ? one : many}`;

  function choiceResults(q, r, opts) {
    const tally = r.tally || [];
    const total = tally.reduce((a, b) => a + b, 0);
    const correct = opts.correct && Number.isInteger(r.correct) ? r.correct : null;
    const mine = r.mine?.choice;
    return `<ol class="lv-bars" aria-label="Results">${q.options.choices.map((c, i) => {
      const n = tally[i] || 0, p = pct(n, total);
      const tags = [i === correct ? `<span class="lv-tag ok">✓ Correct</span>` : "", opts.mine && i === mine ? `<span class="lv-tag">Your answer</span>` : ""].join("");
      return `<li class="lv-bar${i === correct ? " is-correct" : ""}" title="${esc(c)}: ${plural(n, "answer")} (${p}%)">
        <div class="lv-bar-label"><span class="lv-letter">${LETTERS[i]}</span><span class="lv-bar-text">${esc(c)}</span>${tags}</div>
        <div class="lv-bar-row"><div class="lv-track"><div class="lv-fill" style="width:${p}%"></div></div><span class="lv-num">${n} <span class="lv-pct">${p}%</span></span></div>
      </li>`;
    }).join("")}</ol>`;
  }

  function scaleResults(q, r, opts) {
    const { min, max, low, high } = q.options;
    const tally = r.tally || [];
    const top = Math.max(1, ...tally);
    const mine = r.mine?.n;
    const cols = [];
    for (let v = min; v <= max; v++) {
      const n = tally[v - min] || 0;
      cols.push(`<li class="lv-col${opts.mine && v === mine ? " is-mine" : ""}" title="${v}: ${plural(n, "answer")}">
        <span class="lv-col-n">${n}</span><div class="lv-col-track"><div class="lv-col-fill" style="height:${(n / top) * 100}%"></div></div><span class="lv-col-v">${v}</span>
      </li>`);
    }
    const mean = r.mean != null ? `<p class="lv-mean">Average <strong>${Number(r.mean).toFixed(1)}</strong> on ${min}–${max}${opts.mine && mine != null ? ` · you said ${mine}` : ""}</p>` : "";
    return `${mean}<ol class="lv-cols" style="--n:${max - min + 1}" aria-label="Results">${cols.join("")}</ol>
      ${low || high ? `<div class="lv-ends"><span>${esc(low ? `${min} = ${low}` : "")}</span><span>${esc(high ? `${max} = ${high}` : "")}</span></div>` : ""}`;
  }

  function wordResults(q, r, opts) {
    const words = r.words || [];
    if (!words.length) return `<p class="lv-empty">No words yet.</p>`;
    const top = words[0].n;
    // Biggest in the middle: alternate the sorted words to the left and right.
    const placed = [];
    words.forEach((w, i) => (i % 2 ? placed.unshift(w) : placed.push(w)));
    const mine = new Set(r.mine?.words || []);
    const cloud = placed.map((w) => {
      const t = Math.sqrt(w.n / top);
      const style = `font-size:${(1 + 2.2 * t).toFixed(2)}em;font-weight:${Math.round(500 + 300 * t)}`;
      const cls = `lv-word${w.n === top ? " is-top" : ""}${opts.mine && mine.has(w.w) ? " is-mine" : ""}`;
      const label = `${w.w}: ${plural(w.n, "person", "people")}`;
      return opts.hideable
        ? `<button type="button" class="${cls}" style="${style}" data-word="${esc(w.w)}" title="${esc(label)}. Press to hide it from the cloud">${esc(w.w)}</button>`
        : `<span class="${cls}" style="${style}" title="${esc(label)}">${esc(w.w)}</span>`;
    }).join(" ");
    return `<div class="lv-cloud" aria-label="Word cloud">${cloud}</div>`;
  }

  function results(q, r, opts = {}) {
    if (!q || !r) return "";
    if (!r.shown) return `<p class="lv-empty">Results appear once you answer.</p>`;
    if (!r.count) return `<p class="lv-empty">No answers yet.</p>`;
    return q.kind === "choice" ? choiceResults(q, r, opts) : q.kind === "scale" ? scaleResults(q, r, opts) : wordResults(q, r, opts);
  }

  // A student's answer as text, for the instructor's who-answered-what list.
  function answerText(q, v) {
    if (!v) return "";
    if (q.kind === "choice") return `${LETTERS[v.choice] || "?"}. ${q.options.choices[v.choice] ?? ""}`;
    if (q.kind === "scale") return String(v.n);
    return (v.words || []).join(", ");
  }

  const errText = (e) => (e?.message || String(e)).replace(/^.*?exception:\s*/i, "");

  // Reviewing a class (instructors only: the database returns other people's answers only to them) ------------------
  // loadSession(db, id) → { session, questions: [{ …question, correct, hidden, answers: [{ value, at, person }] }], people }
  // people: everyone who answered at least one question in that class.
  async function loadSession(db, id) {
    const [s, q] = await Promise.all([
      db.from("live_sessions").select("id, title, started_at, ended_at").eq("id", id).maybeSingle(),
      db.from("live_questions").select("id, kind, prompt, options, status, reveal, created_at").eq("session_id", id).order("id"),
    ]);
    if (s.error || q.error) throw s.error || q.error;
    const questions = q.data || [];
    const ids = questions.map((x) => x.id);
    let priv = [], answers = [];
    if (ids.length) {
      const [p, a] = await Promise.all([
        db.from("live_private").select("question_id, correct, hidden").in("question_id", ids),
        db.from("live_answers").select("question_id, user_id, value, at, profiles(first_name, last_name, email, recitation, course_section)").in("question_id", ids).order("at"),
      ]);
      if (p.error || a.error) throw p.error || a.error;
      priv = p.data || []; answers = a.data || [];
    }
    const people = new Map();
    for (const a of answers) people.set(a.user_id, { id: a.user_id, ...(a.profiles || {}) });
    questions.forEach((x) => {
      const pr = priv.find((p) => p.question_id === x.id) || {};
      Object.assign(x, { correct: pr.correct ?? null, hidden: pr.hidden || [], answers: answers.filter((a) => a.question_id === x.id).map((a) => ({ ...a, person: people.get(a.user_id) })) });
    });
    return { session: s.data, questions, people: [...people.values()] };
  }

  // The same shape live_results gives, worked out from the answers themselves.
  function summarize(q) {
    const ans = q.answers, r = { id: q.id, count: ans.length, shown: true, status: q.status };
    if (q.kind === "choice") { r.tally = q.options.choices.map((_, i) => ans.filter((a) => a.value?.choice === i).length); r.correct = q.correct; }
    else if (q.kind === "scale") {
      r.tally = []; for (let v = q.options.min; v <= q.options.max; v++) r.tally.push(ans.filter((a) => a.value?.n === v).length);
      r.mean = ans.length ? ans.reduce((n, a) => n + (a.value?.n || 0), 0) / ans.length : null;
    } else {
      const c = new Map();
      ans.forEach((a) => (a.value?.words || []).forEach((w) => { if (!q.hidden.includes(w)) c.set(w, (c.get(w) || 0) + 1); }));
      r.words = [...c].map(([w, n]) => ({ w, n })).sort((a, b) => b.n - a.n || a.w.localeCompare(b.w));
    }
    return r;
  }

  const personName = (p) => (p?.first_name && p?.last_name ? `${p.last_name}, ${p.first_name}` : p?.email || "Unknown");
  const clock = (t) => new Date(t).toLocaleTimeString([], { hour: "numeric", minute: "2-digit", second: "2-digit" });
  const classLabel = (s) => `${s.title ? s.title + " · " : ""}${new Date(s.started_at).toLocaleDateString([], { weekday: "short", month: "short", day: "numeric" })}`;
  const isRight = (q, v) => (q.kind === "choice" && Number.isInteger(q.correct) ? v?.choice === q.correct : null);

  // Each question: its results, then who answered what (and who in the class didn't answer it).
  function reviewHTML(data) {
    const { session, questions, people } = data;
    if (!questions.length) return `<p class="lv-empty">No questions were asked in this class.</p>`;
    const byName = (a, b) => personName(a.person || a).localeCompare(personName(b.person || b));
    return `<p class="lv-meta"><strong>${esc(classLabel(session))}</strong><span>${plural(questions.length, "question")} · ${plural(people.length, "student")} answered at least one</span></p>
      <ol class="lv-review">${questions.map((q, i) => {
        const r = summarize(q);
        const done = new Set(q.answers.map((a) => a.user_id));
        const missing = people.filter((p) => !done.has(p.id)).sort(byName);
        const graded = q.kind === "choice" && Number.isInteger(q.correct);
        const right = graded ? q.answers.filter((a) => isRight(q, a.value)).length : 0;
        return `<li class="lv-review-q">
          <div class="lv-meta"><span class="eyebrow">Q${i + 1} · ${KINDS[q.kind]}</span><span>${plural(q.answers.length, "answer")}${graded ? ` · ${right} correct` : ""}</span></div>
          <h3 class="lv-review-prompt">${esc(q.prompt)}</h3>
          ${results(q, r, { correct: true })}
          ${q.hidden.length ? `<p class="lv-msg">Hidden from the cloud in class: ${q.hidden.map(esc).join(", ")}</p>` : ""}
          <details class="lv-who"><summary>Who answered what (${q.answers.length})</summary>
            ${q.answers.length ? `<div class="lv-who-scroll"><table class="lv-who-table"><thead><tr><th>Student</th><th>Recitation</th><th>Answer</th>${graded ? "<th>Correct</th>" : ""}<th>At</th></tr></thead><tbody>${[...q.answers].sort(byName).map((a) =>
              `<tr><td>${esc(personName(a.person))}</td><td>${esc(a.person?.recitation || "")}</td><td>${esc(answerText(q, a.value))}</td>${graded ? `<td>${isRight(q, a.value) ? "✓ yes" : "no"}</td>` : ""}<td class="mono">${clock(a.at)}</td></tr>`).join("")}</tbody></table></div>` : `<p class="lv-empty">Nobody answered.</p>`}
            ${missing.length ? `<p class="lv-msg">In class but didn't answer this one: ${missing.map((p) => esc(personName(p))).join("; ")}</p>` : ""}
          </details>
        </li>`;
      }).join("")}</ol>`;
  }

  // One row per answer. A leading = + - @ would run as a formula in a spreadsheet.
  function downloadCsv(data) {
    const { session, questions } = data;
    const rows = [["class_date", "class_title", "question", "type", "prompt", "email", "first_name", "last_name", "recitation", "course_section", "answer", "correct", "answered_at"]];
    const date = new Date(session.started_at).toISOString().slice(0, 10);
    questions.forEach((q, i) => q.answers.forEach((a) => {
      const p = a.person || {}, right = isRight(q, a.value);
      rows.push([date, session.title || "", i + 1, KINDS[q.kind], q.prompt, p.email || "", p.first_name || "", p.last_name || "", p.recitation || "", p.course_section || "", answerText(q, a.value), right == null ? "" : right ? "yes" : "no", new Date(a.at).toISOString()]);
    }));
    const cell = (v) => { let s = String(v ?? ""); if (/^[=+\-@]/.test(s)) s = "'" + s; return `"${s.replace(/"/g, '""')}"`; };
    const link = document.createElement("a");
    link.href = URL.createObjectURL(new Blob([rows.map((r) => r.map(cell).join(",")).join("\n")], { type: "text/csv" }));
    link.download = `class-answers-${date}${session.title ? "-" + session.title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") : ""}.csv`;
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  }

  window.Live = { start, watch, results, answerText, esc, plural, errText, LETTERS, KINDS, loadSession, summarize, reviewHTML, downloadCsv, classLabel };
})();
