/* Reading progress: the only code that reads or writes saved progress. Pages, chrome.js and quiz.js all go through
   window.Progress, so a backend can be added later by syncing here without touching any lesson.

   Everything lives under one localStorage key (each access wrapped in try/catch, so a private window just doesn't save):
   {
     v: 1,                                   schema version; bump it and migrate in load() if the shape changes
     lessons:  { [slug]: { visited, completed, updatedAt } },          completed is a timestamp or null
     quizzes:  { [quizId]: { answers: { [questionId]: { choice, correct } }, best: { score, total }, updatedAt } },
     exercises: { [exerciseId]: { code: { html, css } | { js }, passed, updatedAt } },   passed is a timestamp or null
     attempts: [ { quiz, q, choice, correct, at } | { exercise, passed, score, total, at } ],   oldest first
     last:     { slug, at }                                           the lesson to continue from
   }
   quizId and exerciseId are "<slug>/<element id>", e.g. "js-arrays/quiz"; question ids come from the quiz data (q1, q2, …).
   Times are ISO strings. updatedAt on each record lets Progress.merge() combine two copies (say this browser and a
   server) without losing work: the newer record wins, and attempts from both sides are kept. */
(function () {
  const KEY = "book:progress";
  const VERSION = 1;
  const MAX_ATTEMPTS = 2000;
  const listeners = new Set();
  const now = () => new Date().toISOString();
  const empty = () => ({ v: VERSION, lessons: {}, quizzes: {}, exercises: {}, attempts: [], last: null });

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
    const seen = new Set();
    out.attempts = [...(a.attempts || []), ...(b.attempts || [])]
      .filter((t) => { const k = `${t.quiz || t.exercise}|${t.q || ""}|${t.at}`; return !seen.has(k) && seen.add(k); })
      .sort((x, y) => (x.at < y.at ? -1 : 1))
      .slice(-MAX_ATTEMPTS);
    out.last = [a.last, b.last].filter(Boolean).sort((x, y) => (x.at < y.at ? 1 : -1))[0] || null;
    return out;
  }

  window.Progress = {
    page,
    data: load,
    lesson: (slug) => load().lessons[slug] || null,
    isComplete: (slug) => !!load().lessons[slug]?.completed,
    last: () => load().last,

    visit(slug) {
      change((d) => {
        const l = d.lessons[slug] || { visited: null, completed: null };
        d.lessons[slug] = { ...l, visited: l.visited || now(), updatedAt: now() };
        d.last = { slug, at: now() };
      });
    },
    setComplete(slug, done) {
      change((d) => {
        const l = d.lessons[slug] || { visited: now(), completed: null };
        d.lessons[slug] = { ...l, completed: done ? now() : null, updatedAt: now() };
      });
    },

    quiz: (id) => load().quizzes[id] || { answers: {}, best: null },
    answer(quiz, q, choice, correct, total) {
      change((d) => {
        const rec = d.quizzes[quiz] || { answers: {}, best: null };
        const answers = { ...rec.answers, [q]: { choice, correct } };
        let best = rec.best;
        const done = Object.values(answers);
        if (done.length === total) {
          const score = done.filter((x) => x.correct).length;
          if (!best || score / total > best.score / best.total) best = { score, total };
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
    checked(id, score, total) {
      change((d) => {
        const rec = d.exercises[id] || { code: null, passed: null };
        const passed = score === total;
        d.exercises[id] = { ...rec, passed: rec.passed || (passed ? now() : null), updatedAt: now() };
        d.attempts.push({ exercise: id, passed, score, total, at: now() });
        if (d.attempts.length > MAX_ATTEMPTS) d.attempts.splice(0, d.attempts.length - MAX_ATTEMPTS);
      });
    },

    merge,
    /** Run fn whenever progress changes, in this tab or another one. Returns an unsubscribe function. */
    subscribe(fn) { listeners.add(fn); return () => listeners.delete(fn); },
  };

  addEventListener("storage", (e) => { if (e.key === KEY || e.key === null) listeners.forEach((fn) => fn()); });
})();
