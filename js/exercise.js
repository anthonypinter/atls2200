/* Graded exercises: a task, starter code, hidden checks, hints and a solution. Work in progress and passes are saved
   through window.Progress, so a student can leave and come back. Put <div class="exercise" id="ex-something"></div>
   in the page, then call makeExercise() from the page's script (js/chrome.js queues the call until this file loads):

   HTML/CSS: checks look at the live preview.
     makeExercise(document.getElementById("ex-nav"), {
       title: "Spread out the nav", task: "<p>Use Flexbox on <code>nav</code>…</p>",   task is HTML
       html: "…", css: "…",                     starter code (leave a language out to hide its tab)
       solution: { css: "…" },                  merged over the student's code when they ask for it
       hints: ["…", "…"],                       revealed one at a time (plain text)
       checks: [{ label: "nav is a flex container", test: ({ $, style }) => style("nav", "display") === "flex" }],
     });
     A check's test gets { doc, $, $$, style(selectorOrElement, property), code } and returns true to pass.
     Throwing counts as a fail, so tests can assume elements exist.

   JavaScript: checks look at what the code logged and at the functions it defined.
     makeExercise(el, { title, task, js: "…", solution: "…", expose: ["total"], hints, checks: [
       { label: "total([1, 2]) returns 3", test: ({ fns }) => fns.total([1, 2]) === 3 },
       { label: "logs 6", test: ({ logs }) => logs.includes("6") },
     ]});
     A check's test gets { logs (text of each console.log), fns (the names listed in expose), error, code }.

   Give every exercise element a stable id: saved work is stored under "<page>/<id>". */
(function () {
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const P = window.Progress;

  async function makeExercise(el, def) {
    const isJS = typeof def.js === "string";
    await loadScript("js/runner.js");
    if (!isJS) await loadScript("js/sandbox.js");

    const id = `${P ? P.page : "page"}/${el.id || "exercise"}`;
    if (!el.id) console.warn(`Exercise "${def.title}" has no id, so its saved work can't be told apart from other exercises.`);
    const saved = P ? P.exercise(id) : { code: null, passed: null };
    const starter = isJS ? { js: def.js } : { html: def.html, css: def.css };
    const hints = def.hints || [];

    el.classList.add("panel", "exercise");
    el.innerHTML = `<div class="ex-head"><span class="eyebrow">Exercise</span><h3>${esc(def.title)}</h3><span class="ex-status" hidden>✓ Passed</span></div>
      <div class="ex-task">${def.task || ""}</div>
      <p class="hint ex-restored" hidden>Your saved work was restored. Reset brings back the starting code.</p>
      <div class="ex-work"></div>
      <div class="ex-bar">
        <button class="btn run" type="button" data-act="check">Check my work</button>
        ${hints.length ? `<button class="btn" type="button" data-act="hint">Show a hint (1 of ${hints.length})</button>` : ""}
        ${def.solution ? `<button class="btn" type="button" data-act="solution" hidden>Show solution</button>` : ""}
        <button class="btn" type="button" data-act="reset">Reset</button>
        <button class="btn" type="button" data-act="restore" hidden>↶ Back to my code</button>
      </div>
      <div class="ex-result" aria-live="polite"></div>
      <ol class="ex-hints" aria-label="Hints"></ol>`;
    const $ = (sel) => el.querySelector(sel);
    const work = $(".ex-work");

    // Reset and Show solution both replace the code; "Back to my code" undoes either until the next edit.
    // setting is true while the code is being replaced, so that doesn't count as an edit.
    let mine = null, setting = false;

    // The editor: a sandbox for HTML/CSS, or a textarea with Run and a console for JavaScript.
    let get, set;
    let saveTimer;
    const save = () => { clearTimeout(saveTimer); saveTimer = setTimeout(() => P && P.saveCode(id, get()), 600); };
    if (isJS) {
      work.innerHTML = `<textarea class="ex-js" aria-label="${esc(def.title)}: JavaScript"></textarea><div class="runner-bar"><button class="btn" type="button" data-act="run">Run ▸</button><span class="hint">Run shows what your code logs. Check my work tests it.</span></div><ol class="console" aria-live="polite" aria-label="Console output"></ol>`;
      const ta = work.querySelector("textarea"), out = work.querySelector(".console");
      const run = () => Runner.render(Runner.exec(ta.value).lines, out);
      const fit = Runner.enhance(ta, run);
      work.querySelector('[data-act="run"]').addEventListener("click", run);
      get = () => ({ js: ta.value });
      set = (code) => { ta.value = code.js; fit(); save(); return Promise.resolve(); };
      ta.value = saved.code?.js ?? def.js;
      fit();
      ta.addEventListener("input", () => { edited(); save(); });
    } else {
      const box = document.createElement("div");
      work.append(box);
      const code = { ...starter, ...(saved.code || {}) };
      const sb = Sandbox.mount(box, { ...code, title: def.title, height: def.height, onChange: () => { edited(); save(); } });
      box.querySelector('[data-act="reset"]').remove();   // the exercise has its own Reset
      get = sb.get;
      set = (c) => sb.set(c);
      work.sandbox = sb;
    }
    if (saved.code) $(".ex-restored").hidden = false;

    const replace = async (code) => {
      if (!mine) mine = get();
      setting = true;
      await set(code);
      setting = false;
      $('[data-act="restore"]').hidden = false;
    };
    function edited() {
      if (setting) return;
      mine = null;
      $('[data-act="restore"]').hidden = true;
    }

    function paintStatus() {
      $(".ex-status").hidden = !(P && P.exercise(id).passed);
    }

    async function check() {
      let ctx;
      if (isJS) {
        const r = Runner.exec(get().js, def.expose || []);
        Runner.render(r.lines, work.querySelector(".console"));
        ctx = { logs: r.lines.filter((l) => l.cls === "log").map((l) => l.text), fns: r.values, error: r.error, code: get() };
      } else {
        await work.sandbox.update();
        const doc = work.sandbox.frame.contentDocument, win = work.sandbox.frame.contentWindow;
        const pick = (t) => (typeof t === "string" ? doc.querySelector(t) : t);
        ctx = {
          doc,
          $: (s) => doc.querySelector(s),
          $$: (s) => [...doc.querySelectorAll(s)],
          style: (t, prop) => win.getComputedStyle(pick(t)).getPropertyValue(prop).trim(),
          code: get(),
        };
      }
      const results = def.checks.map((c) => {
        try { return !!c.test(ctx); } catch { return false; }
      });
      const score = results.filter(Boolean).length, total = results.length;
      if (P) { P.checked(id, score, total, get()); P.used(el, "check"); }
      const all = score === total;
      $(".ex-result").className = "ex-result " + (all ? "pass" : "fail");
      $(".ex-result").innerHTML = `<p><strong>${all ? "All checks pass. Nice work!" : `${score} of ${total} checks pass.`}</strong>${!all && ctx.error ? ` Your code stopped with an error: <code>${esc(ctx.error.name + ": " + ctx.error.message)}</code>` : ""}</p>
        <ul class="ex-checks">${def.checks.map((c, i) => `<li class="${results[i] ? "ok" : "no"}"><span aria-hidden="true">${results[i] ? "✓" : "✕"}</span> ${esc(c.label)}<span class="sr-only">: ${results[i] ? "passes" : "not yet"}</span></li>`).join("")}</ul>`;
      const sol = $('[data-act="solution"]');
      if (sol) sol.hidden = false;
      paintStatus();
    }

    let shown = 0;
    el.addEventListener("click", (e) => {
      const act = e.target.closest("button[data-act]")?.dataset.act;
      if (act === "check") check();
      if (act === "hint" && shown < hints.length) {
        const li = document.createElement("li");
        li.textContent = hints[shown++];
        $(".ex-hints").append(li);
        const btn = $('[data-act="hint"]');
        if (shown === hints.length) btn.hidden = true;
        else btn.textContent = `Show another hint (${shown + 1} of ${hints.length})`;
      }
      if (act === "solution") replace(isJS ? { js: def.solution } : { ...get(), ...def.solution });
      if (act === "reset") { replace(starter); $(".ex-restored").hidden = true; }
      if (act === "restore" && mine) {
        const back = mine;
        setting = true;
        set(back).then(() => { setting = false; });
        mine = null;
        $('[data-act="restore"]').hidden = true;
      }
    });

    paintStatus();
  }

  const queued = window.makeExercise?.queue || [];
  window.makeExercise = makeExercise;
  queued.forEach((args) => makeExercise(...args));
})();
