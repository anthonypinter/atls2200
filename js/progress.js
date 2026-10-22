/* Reading progress: the only code that reads or writes saved progress. Pages, chrome.js and quiz.js all go through
   window.Progress, so a backend can be added later by syncing here without touching any lesson.

   Everything lives under one localStorage key (each access wrapped in try/catch, so a private window just doesn't save):
   {
     v: 1,                                   schema version; bump it and migrate in load() if the shape changes
     lessons:  { [slug]: { visited, completed, updatedAt } },          completed is a timestamp or null
     quizzes:  { [quizId]: { answers: { [questionId]: { choice, correct } }, best: { score, total }, updatedAt } },
     exercises: { [exerciseId]: { code: { html, css } | { js }, passed, updatedAt } },   passed is a timestamp or null
     sections: { [sectionId]: { seen, interacted, ms, updatedAt } },
                 ms: active reading time; seen: when ms first reached the section's bar (js/chrome.js sets it from the
                 section's length); interacted: the first time the student did what the section asks (see used())
     attempts: [ { quiz, q, choice, correct, at } | { exercise, passed, score, total, at } ],   oldest first
     last:     { slug, at }                                           the lesson to continue from
   }
   quizId and exerciseId are "<slug>/<element id>", e.g. "js-arrays/quiz"; question ids come from the quiz data (q1, q2, …).
   sectionId is "<slug>/<heading id>", e.g. "flexbox/sec-try-every-setting" (the ids under "On this page").
   Times are ISO strings. updatedAt on each record lets Progress.merge() combine two copies (say this browser and a
   server) without losing work: the newer record wins, and attempts from both sides are kept.
   js/backend.js does exactly that when a student signs in: it merges this copy with their account's and keeps both
   up to date. Without a backend (or signed out) nothing here changes.

   Activity log: a second key, book:events, queues one small record per thing that happened (a visit, a section
   seen or used, reading time, a code run, a quiz answer, a Check, Mark complete): { id, kind, lesson, target, detail,
   at }. Signed in, js/backend.js uploads the queue to the events table, which students can add to but never change,
   and empties it. The progress object above is the fast, offline copy; the events table is the record to trust. */
(function () {
  const KEY = "book:progress";
  const VERSION = 1;
  const MAX_ATTEMPTS = 2000;
  const listeners = new Set();
  const now = () => new Date().toISOString();
  const EVENTS = "book:events";
  const MAX_EVENTS = 1000;
  const empty = () => ({ v: VERSION, lessons: {}, quizzes: {}, exercises: {}, sections: {}, attempts: [], last: null });

  function load() {
    let data = null;
    try { data = JSON.parse(localStorage.getItem(KEY)); } catch {}
    if (!data || data.v !== VERSION) return empty();
    return Object.assign(empty(), data);
  }
  function save(data) {
    try { localStorage.setItem(KEY, JSON.stringify(data)); } catch {}
    listeners.forEach((fn) => fn());
  }
  // Always read fresh before writing, so two open tabs don't overwrite each other.
  function change(fn) {
    const data = load();
    fn(data);
    save(data);
  }

  const page = (decodeURIComponent(location.pathname.split("/").pop()) || "index.html").replace(/\.html?$/, "");

  // Combine two progress objects. Pure: returns a new object and changes neither input.
  function merge(a, b) {
    const out = empty();
    const newer = (x, y) => (!x ? y : !y ? x : (y.updatedAt || "") > (x.updatedAt || "") ? y : x);
    for (const key of ["lessons", "quizzes", "exercises"]) {
      for (const id of new Set([...Object.keys(a[key] || {}), ...Object.keys(b[key] || {})])) {
        out[key][id] = newer(a[key]?.[id], b[key]?.[id]);
      }
    }
    // Keep the best score from either side, even when the newer record was a fresh retry.
    for (const id of Object.keys(out.quizzes)) {
      const best = [a.quizzes?.[id]?.best, b.quizzes?.[id]?.best].filter(Boolean).sort((x, y) => y.score / y.total - x.score / x.total)[0];
      if (best) out.quizzes[id] = { ...out.quizzes[id], best };
    }
    // Likewise a pass on either side survives a newer draft saved on the other.
    for (const id of Object.keys(out.exercises)) {
      const passed = [a.exercises?.[id]?.passed, b.exercises?.[id]?.passed].filter(Boolean).sort()[0];
      if (passed) out.exercises[id] = { ...out.exercises[id], passed };
    }
    // Sections only ever gain a time, so keep the earliest of each.
    const first = (x, y) => [x, y].filter(Boolean).sort()[0] || null;
    for (const id of new Set([...Object.keys(a.sections || {}), ...Object.keys(b.sections || {})])) {
      const x = a.sections?.[id] || {}, y = b.sections?.[id] || {};
      out.sections[id] = { seen: first(x.seen, y.seen), interacted: first(x.interacted, y.interacted), updatedAt: [x.updatedAt, y.updatedAt].filter(Boolean).sort().pop() || null };
    }
    for (const id of Object.keys(out.sections)) {
      const ms = Math.max(a.sections?.[id]?.ms || 0, b.sections?.[id]?.ms || 0);
      if (ms) out.sections[id].ms = ms;
    }
    const seen = new Set();
    out.attempts = [...(a.attempts || []), ...(b.attempts || [])]
      .filter((t) => { const k = `${t.quiz || t.exercise}|${t.q || ""}|${t.at}`; return !seen.has(k) && seen.add(k); })
      .sort((x, y) => (x.at < y.at ? -1 : 1))
      .slice(-MAX_ATTEMPTS);
    out.last = [a.last, b.last].filter(Boolean).sort((x, y) => (x.at < y.at ? 1 : -1))[0] || null;
    return out;
  }

  // The activity log (see the top of this file). Ids let the server ignore an event that two tabs both uploaded.
  const uid = () => (crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2));
  function readEvents() { try { return JSON.parse(localStorage.getItem(EVENTS)) || []; } catch { return []; } }
  function writeEvents(list) {
    try { localStorage.setItem(EVENTS, JSON.stringify(list.slice(-MAX_EVENTS))); } catch {}
    listeners.forEach((fn) => fn());
  }
  function log(kind, target = null, detail = null) {
    writeEvents([...readEvents(), { id: uid(), kind, lesson: page, target, detail, at: now() }]);
  }

  window.Progress = {
    page,
    data: load,
    lesson: (slug) => load().lessons[slug] || null,
    isComplete: (slug) => !!load().lessons[slug]?.completed,
    last: () => load().last,

    visit(slug) {
      log("visit", slug);
      change((d) => {
        const l = d.lessons[slug] || { visited: null, completed: null };
        d.lessons[slug] = { ...l, visited: l.visited || now(), updatedAt: now() };
        d.last = { slug, at: now() };
      });
    },
    setComplete(slug, done) {
      log(done ? "complete" : "uncomplete", slug);
      change((d) => {
        const l = d.lessons[slug] || { visited: now(), completed: null };
        d.lessons[slug] = { ...l, completed: done ? now() : null, updatedAt: now() };
      });
    },

    quiz: (id) => load().quizzes[id] || { answers: {}, best: null },
    answer(quiz, q, choice, correct, total) {
      log("answer", quiz, { q, choice, correct });
      change((d) => {
        const rec = d.quizzes[quiz] || { answers: {}, best: null };
        const answers = { ...rec.answers, [q]: { choice, correct } };
        let best = rec.best;
        const done = Object.values(answers);
        if (done.length === total) {
          const score = done.filter((x) => x.correct).length;
          if (!best || score / total > best.score / best.total) best = { score, total };
          log("quiz-done", quiz, { score, total });
        }
        d.quizzes[quiz] = { answers, best, updatedAt: now() };
        d.attempts.push({ quiz, q, choice, correct, at: now() });
        if (d.attempts.length > MAX_ATTEMPTS) d.attempts.splice(0, d.attempts.length - MAX_ATTEMPTS);
      });
    },
    retryQuiz(quiz) {
      change((d) => {
        const rec = d.quizzes[quiz];
        if (rec) d.quizzes[quiz] = { ...rec, answers: {}, updatedAt: now() };
      });
    },

    exercise: (id) => load().exercises[id] || { code: null, passed: null },
    /** Save the student's work in progress (call it debounced, not on every keystroke). */
    saveCode(id, code) {
      change((d) => {
        const rec = d.exercises[id] || { code: null, passed: null };
        d.exercises[id] = { ...rec, code, updatedAt: now() };
      });
    },
    /** Record one press of Check: score is how many checks passed. Passing once keeps the exercise passed. */
    checked(id, score, total, code) {
      const passed = score === total;
      // The code is kept with a pass (capped), so an instructor can look at what actually passed.
      const kept = passed && code && JSON.stringify(code).length < 20000 ? code : undefined;
      log("check", id, { score, total, passed, ...(kept ? { code: kept } : {}) });
      change((d) => {
        const rec = d.exercises[id] || { code: null, passed: null };
        d.exercises[id] = { ...rec, passed: rec.passed || (passed ? now() : null), updatedAt: now() };
        d.attempts.push({ exercise: id, passed, score, total, at: now() });
        if (d.attempts.length > MAX_ATTEMPTS) d.attempts.splice(0, d.attempts.length - MAX_ATTEMPTS);
      });
    },

    section: (id) => load().sections[id] || null,
    /** Add active reading time: times is { sectionId: ms }, bars is { sectionId: ms needed to count as seen }.
        js/chrome.js calls this every few seconds while the student is reading. */
    addTime(times, bars = {}) {
      const ids = Object.keys(times).filter((id) => times[id] > 0);
      if (!ids.length) return;
      const lesson = {};
      change((d) => {
        for (const id of ids) {
          const s = d.sections[id] || { seen: null, interacted: null };
          const ms = (s.ms || 0) + Math.round(times[id]);
          const seen = s.seen || (ms >= (bars[id] || 0) ? now() : null);
          if (seen && !s.seen) log("seen", id, { ms });
          d.sections[id] = { ...s, ms, seen, updatedAt: now() };
          lesson[id.split("/")[1]] = Math.round(times[id] / 1000);
        }
      });
      log("time", page, lesson);
    },
    /** The student did what the section asks (what: "run", "edit", "controls", "check", "quiz"). Counts as seen too. */
    interact(id, what) {
      const s0 = load().sections[id];
      if (s0?.interacted) return;
      log("used", id, { what });
      change((d) => { const s = d.sections[id] || {}; d.sections[id] = { ...s, seen: s.seen || now(), interacted: now(), updatedAt: now() }; });
    },
    /** Components report activity here: el is the element it happened in. js/chrome.js turns it into section
        progress. what: "run" (Run with edited code), "run-unchanged", "edit" (typed in a live editor), "check"
        (pressed Check), "quiz" (answered every question). */
    used(el, what) { el.dispatchEvent(new CustomEvent("book:use", { bubbles: true, detail: { what } })); },
    log,
    /** The queued activity log, oldest first, and removing the ones a server has stored (by id). */
    events: readEvents,
    dropEvents(ids) { const gone = new Set(ids); writeEvents(readEvents().filter((e) => !gone.has(e.id))); },
    /** Whether a section is finished. kind is its eyebrow ("Read", "Play", "Practice", …) or "notes": sections with
        something to do need an interaction, reading needs only a visit. The instructor dashboard uses this too. */
    sectionDone(rec, kind) {
      if (!rec?.seen) return false;
      return !this.needsUse(kind) || !!rec.interacted;
    },
    /** Sections that ask the student to do something; the rest are read. */
    needsUse: (kind) => /^(play|try it|practice|check yourself)$/i.test(kind || ""),

    merge,
    /** Swap in a whole progress object (js/backend.js uses this after merging with the server). null clears it. */
    replace(data) {
      if (!data) { try { localStorage.removeItem(EVENTS); } catch {} }
      save(Object.assign(empty(), data || {}));
    },
    /** Run fn whenever progress changes, in this tab or another one. Returns an unsubscribe function. */
    subscribe(fn) { listeners.add(fn); return () => listeners.delete(fn); },
  };

  addEventListener("storage", (e) => { if (e.key === KEY || e.key === EVENTS || e.key === null) listeners.forEach((fn) => fn()); });
})();
