/* Multiple-choice quiz: makeQuiz(el, items). Answers are saved through window.Progress (js/progress.js), so a revisit
   shows what was already answered, and Retry starts a fresh round while keeping the best score.
   items: [{ id, q, opts: [...], a: indexOfRightAnswer, why, pre?, code? }]
   - id: stable per question ("q1", "q2", …). Keep it when you edit or reorder questions and give new questions a new id,
     so saved answers stay attached to the right question.
   - pre: a JavaScript snippet shown under the question (highlighted with hlJS when runner.js is loaded).
   - code: show q itself as code. Question and option text is plain text.
   The quiz id is "<page>/<element id>", so one page can hold more than one quiz.

   makeQuiz(el, items, { once: true }) is a scored quiz (the practice pages): the student picks an answer for every
   question, can change their mind, then presses Submit. Answers lock, feedback appears, and there's no Retry. Picks
   not yet submitted are kept in this browser (book:quizdraft:<quiz id>) so a reload doesn't lose them. */
(function () {
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

  function makeQuiz(el, items, opts = {}) {
    if (opts.once) return makeOnceQuiz(el, items);
    el.quizItems = items;   // print.html reads the questions from here
    const P = window.Progress;
    const quizId = `${P ? P.page : "page"}/${el.id || "quiz"}`;
    items.forEach((x, i) => {
      if (x.id) return;
      console.warn(`Quiz ${quizId}: question ${i + 1} has no id, so its saved answer can move if questions are reordered.`);
      x.id = "q" + (i + 1);
    });
    const hl = (src) => (window.hlJS ? window.hlJS(src) : esc(src));

    // questionId → chosen option. Saved answers whose option no longer exists are dropped.
    let answers = {};
    if (P) {
      const saved = P.quiz(quizId).answers;
      for (const x of items) if (saved[x.id] && saved[x.id].choice < x.opts.length) answers[x.id] = saved[x.id].choice;
    }

    function render() {
      el.innerHTML = `<div class="quiz-top"><p class="score" aria-live="polite"></p><button class="btn quiz-retry" type="button" hidden>↺ Retry quiz</button></div>`
        + items.map((x, i) => `<div class="q"><b>${i + 1}. ${x.code ? `<code>${esc(x.q)}</code>` : esc(x.q)}</b>${x.pre ? `<pre class="snippet">${hl(x.pre)}</pre>` : ""}<div class="opts">${x.opts.map((o, j) => `<button class="btn" type="button" data-q="${i}" data-o="${j}">${esc(o)}</button>`).join("")}</div><div class="feedback" aria-live="polite"></div></div>`).join("");
      items.forEach((x, i) => { if (x.id in answers) show(i); });
      score();
    }

    function show(i) {
      const x = items[i], choice = answers[x.id], q = el.querySelectorAll(".q")[i];
      q.querySelector(".opts").dataset.done = "1";
      q.querySelectorAll(".opts button").forEach((o) => {
        const j = +o.dataset.o;
        o.classList.toggle("right", j === x.a);
        o.classList.toggle("wrong", j === choice && j !== x.a);
      });
      const fb = q.querySelector(".feedback"), right = choice === x.a;
      fb.className = "feedback " + (right ? "right" : "wrong");
      fb.textContent = (right ? "Correct. " : "Not quite. ") + x.why;
    }

    function score() {
      const done = items.filter((x) => x.id in answers);
      const right = done.filter((x) => answers[x.id] === x.a).length;
      const best = P && P.quiz(quizId).best;
      let text = `${right} / ${items.length}`;
      if (done.length === items.length && right === items.length) text += " · All correct!";
      if (best && (done.length < items.length || best.score !== right)) text += ` · Best: ${best.score} / ${best.total}`;
      el.querySelector(".score").textContent = text;
      el.querySelector(".quiz-retry").hidden = !done.length;
    }

    el.addEventListener("click", (ev) => {
      if (ev.target.closest(".quiz-retry")) {
        answers = {};
        if (P) P.retryQuiz(quizId);
        render();
        el.querySelector(".opts button").focus();
        return;
      }
      const b = ev.target.closest("button[data-q]");
      if (!b) return;
      const i = +b.dataset.q, x = items[i];
      if (x.id in answers) return;
      answers[x.id] = +b.dataset.o;
      if (P) {
        P.answer(quizId, x.id, answers[x.id], answers[x.id] === x.a, items.length);
        if (items.every((y) => y.id in answers)) P.used(el, "quiz");
      }
      show(i);
      score();
    });

    render();
  }

  // One attempt: choose, change, submit once. Scored by Progress.score() from the quiz record's first attempt.
  function makeOnceQuiz(el, items) {
    el.quizItems = items;
    const P = window.Progress;
    const quizId = `${P ? P.page : "page"}/${el.id || "quiz"}`;
    const DRAFT = "book:quizdraft:" + quizId;
    const hl = (src) => (window.hlJS ? window.hlJS(src) : esc(src));
    const saved = () => (P ? P.quiz(quizId) : { answers: {} });
    // Submitted: every question has a saved answer (or a first attempt is on record, say from another browser).
    const submitted = () => { const s = saved(); return !!s.first || items.every((x) => x.id in (s.answers || {})); };
    let picks = {};
    try { picks = JSON.parse(localStorage.getItem(DRAFT)) || {}; } catch {}
    const keep = () => { try { localStorage.setItem(DRAFT, JSON.stringify(picks)); } catch {} };

    function render() {
      const done = submitted(), answers = saved().answers || {};
      const first = saved().first;
      const head = done
        ? `<p class="score" tabindex="-1" aria-live="polite">Submitted: ${first ? `${first.score} / ${first.total}` : `${items.filter((x) => answers[x.id]?.choice === x.a).length} / ${items.length}`} points</p>`
        : `<p class="score" aria-live="polite">One attempt. Pick an answer for every question, then press Submit. You can change a pick until you submit.</p>`;
      el.innerHTML = `<div class="quiz-top">${head}</div>`
        + items.map((x, i) => {
          const choice = done ? answers[x.id]?.choice : picks[x.id];
          return `<div class="q"><b>${i + 1}. ${x.code ? `<code>${esc(x.q)}</code>` : esc(x.q)}</b>${x.pre ? `<pre class="snippet">${hl(x.pre)}</pre>` : ""}<div class="opts"${done ? ' data-done="1"' : ""}>${x.opts.map((o, j) => {
            const cls = !done ? (choice === j ? "picked" : "") : [j === x.a ? "right" : "", j === choice && j !== x.a ? "wrong" : ""].join(" ").trim();
            return `<button class="btn ${cls}" type="button" data-q="${i}" data-o="${j}"${done ? " disabled" : ` aria-pressed="${choice === j}"`}>${esc(o)}</button>`;
          }).join("")}</div>${done ? `<div class="feedback ${choice === x.a ? "right" : "wrong"}">${choice === undefined ? "Not answered. " : choice === x.a ? "Correct. " : "Not quite. "}${esc(x.why)}</div>` : ""}</div>`;
        }).join("")
        + (done ? "" : `<div class="quiz-submit"><button class="btn run" type="button" data-act="submit">Submit quiz</button> <span class="hint" aria-live="polite"></span></div>`);
      paintCount();
    }
    function paintCount() {
      const n = items.filter((x) => x.id in picks).length, btn = el.querySelector('[data-act="submit"]');
      if (!btn) return;
      btn.disabled = n < items.length;
      el.querySelector(".quiz-submit .hint").textContent = n < items.length ? `${n} of ${items.length} answered` : "All answered. Submitting locks your answers.";
    }

    el.addEventListener("click", (ev) => {
      if (submitted()) return;
      const b = ev.target.closest("button[data-q]");
      if (b) {
        const x = items[+b.dataset.q];
        picks[x.id] = +b.dataset.o;
        keep();
        b.parentElement.querySelectorAll("button").forEach((o) => { const on = o === b; o.classList.toggle("picked", on); o.setAttribute("aria-pressed", String(on)); });
        paintCount();
        return;
      }
      const sub = ev.target.closest('[data-act="submit"]');
      if (!sub || items.some((x) => !(x.id in picks))) return;
      if (sub.dataset.sure !== "1") { sub.dataset.sure = "1"; sub.textContent = "Press again to submit"; return; }
      if (P) {
        for (const x of items) P.answer(quizId, x.id, picks[x.id], picks[x.id] === x.a, items.length);
        P.used(el, "quiz");
      }
      try { localStorage.removeItem(DRAFT); } catch {}
      render();
      el.querySelector(".score").focus?.();
    });
    // Submitted in another tab, or synced from the account: show the result.
    P?.subscribe(() => { if (submitted() && el.querySelector('[data-act="submit"]')) render(); });
    render();
  }

  window.makeQuiz = makeQuiz;
})();
