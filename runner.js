/* Shared helpers for the JavaScript pages.
   - hlJS(code): returns syntax-highlighted HTML for a JS snippet.
   - Any <div class="runner"> with a <textarea> inside becomes an editor with Run / Reset
     and a console that shows console.log output and errors, like the browser's own console. */
(function () {
  const KEYWORDS = new Set("const let var function return if else for of in while do break continue new true false null undefined typeof async await class this try catch throw switch case default".split(" "));
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  function hlJS(src) {
    const re = /(\/\/[^\n]*|\/\*[\s\S]*?\*\/)|("(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'|`(?:[^`\\]|\\.)*`)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)(?=\s*\()|([A-Za-z_$][\w$]*)/g;
    let out = "", last = 0, m;
    while ((m = re.exec(src))) {
      out += esc(src.slice(last, m.index));
      const [t, cmt, str, num, fn, word] = m;
      if (cmt) out += `<span class="cmt">${esc(t)}</span>`;
      else if (str) out += `<span class="str">${esc(t)}</span>`;
      else if (num) out += `<span class="num">${t}</span>`;
      else if (fn) out += KEYWORDS.has(fn) ? `<span class="kw">${fn}</span>` : `<span class="fn">${fn}</span>`;
      else out += KEYWORDS.has(word) ? `<span class="kw">${word}</span>` : word;
      last = m.index + t.length;
    }
    return out + esc(src.slice(last));
  }

  // Format a value the way the browser console does: strings bare at the top level, quoted inside arrays and objects.
  function fmt(v, nested) {
    if (typeof v === "string") return nested ? JSON.stringify(v) : v;
    if (typeof v === "function") return `ƒ ${v.name || "anonymous"}()`;
    if (v === undefined) return "undefined";
    if (Array.isArray(v)) return nested && nested > 2 ? "[…]" : `[${v.map((x) => fmt(x, (nested || 0) + 1)).join(", ")}]`;
    if (v instanceof Element) return `<${v.tagName.toLowerCase()}${v.id ? "#" + v.id : ""}${v.className ? "." + String(v.className).trim().split(/\s+/).join(".") : ""}>`;
    if (v && typeof v === "object") {
      if (nested && nested > 2) return "{…}";
      const e = Object.entries(v);
      return e.length ? `{ ${e.map(([k, x]) => `${/^[A-Za-z_$][\w$]*$/.test(k) ? k : JSON.stringify(k)}: ${fmt(x, (nested || 0) + 1)}`).join(", ")} }` : "{}";
    }
    return String(v);
  }

  function run(code, out) {
    out.innerHTML = "";
    const line = (cls, text) => { const li = document.createElement("li"); li.className = cls; li.textContent = text; out.append(li); };
    const make = (cls) => (...args) => line(cls, args.map((a) => fmt(a)).join(" "));
    const con = { log: make("log"), info: make("log"), warn: make("warn"), error: make("err"), table: make("log") };
    try {
      new Function("console", code)(con);
    } catch (err) {
      line("err", `Uncaught ${err.name}: ${err.message}`);
    }
    if (!out.children.length) line("muted", "No output. Use console.log() to print a value.");
  }

  function setup(box) {
    const ta = box.querySelector("textarea");
    const original = ta.value;
    ta.spellcheck = false;
    ta.setAttribute("autocapitalize", "off");
    ta.rows = Math.max(3, original.split("\n").length);
    const bar = document.createElement("div");
    bar.className = "runner-bar";
    bar.innerHTML = `<button class="btn run" type="button">Run ▸</button><button class="btn" type="button">Reset</button><span class="hint">Edit the code, then Run (or Ctrl/⌘ + Enter).</span>`;
    const out = document.createElement("ol");
    out.className = "console";
    out.setAttribute("aria-live", "polite");
    out.setAttribute("aria-label", "Console output");
    box.append(bar, out);
    const [runBtn, resetBtn] = bar.querySelectorAll("button");
    runBtn.addEventListener("click", () => run(ta.value, out));
    resetBtn.addEventListener("click", () => { ta.value = original; ta.rows = Math.max(3, original.split("\n").length); run(ta.value, out); });
    ta.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) { e.preventDefault(); run(ta.value, out); }
      // Tab inserts two spaces; Escape then Tab still moves focus out of the editor.
      if (e.key === "Tab" && !e.shiftKey && !ta.dataset.escaped) {
        e.preventDefault();
        const s = ta.selectionStart;
        ta.setRangeText("  ", s, ta.selectionEnd, "end");
      }
      ta.dataset.escaped = e.key === "Escape" ? "1" : "";
    });
    ta.addEventListener("input", () => { ta.rows = Math.max(3, ta.value.split("\n").length); });
    run(ta.value, out);
  }

  // Multiple-choice quiz in the same style as the rest of the Field Guide.
  // items: [{ q, opts: [...], a: indexOfRightAnswer, why }]. Question and option text is plain text.
  function makeQuiz(el, items) {
    let score = 0;
    const e = (s) => esc(String(s));
    el.innerHTML = `<p class="score">0 / ${items.length}</p>` + items.map((x, i) =>
      `<div class="q"><b>${i + 1}. ${x.code ? `<code>${e(x.q)}</code>` : e(x.q)}</b>${x.pre ? `<pre class="snippet">${hlJS(x.pre)}</pre>` : ""}<div class="opts">${x.opts.map((o, j) => `<button class="btn" data-q="${i}" data-o="${j}">${e(o)}</button>`).join("")}</div><div class="feedback"></div></div>`).join("");
    el.addEventListener("click", (ev) => {
      const b = ev.target.closest("button[data-q]"); if (!b) return;
      const x = items[b.dataset.q], group = b.parentElement;
      if (group.dataset.done) return;
      group.dataset.done = "1";
      const right = +b.dataset.o === x.a;
      group.querySelectorAll("button").forEach((o) => { if (+o.dataset.o === x.a) o.classList.add("right"); else if (o === b) o.classList.add("wrong"); });
      if (right) score++;
      el.querySelector(".score").textContent = `${score} / ${items.length}`;
      const fb = group.nextElementSibling; fb.className = "feedback " + (right ? "right" : "wrong"); fb.textContent = (right ? "Correct. " : "Not quite. ") + x.why;
    });
  }

  window.hlJS = hlJS;
  window.makeQuiz = makeQuiz;
  window.fmtJS = fmt;
  document.querySelectorAll(".runner").forEach(setup);
})();
