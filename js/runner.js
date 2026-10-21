/* Code editors and the JavaScript console.
   - hlJS(code): returns syntax-highlighted HTML for a JS snippet.
   - Any <div class="runner"> with a <textarea> inside becomes an editor with Run / Reset
     and a console that shows console.log output and errors, like the browser's own console.
   - window.Runner, for other components (js/sandbox.js, js/exercise.js):
     enhance(textarea, onRun): Tab indents, Escape then Tab leaves, Ctrl/⌘ + Enter calls onRun, rows grow with the code.
     exec(code, expose, onLine): runs code and returns { lines, error, values }; values holds the top-level names
       listed in expose (e.g. ["add"]) so a check can call the student's function.
     render(lines, out): draws console lines into an <ol class="console">.
   JavaScript lessons load this file with a <script> tag because their own scripts use hlJS. Any other page can just
   use <div class="runner"> and js/chrome.js loads it. */
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

  // onLine also receives lines logged later (after a timer or an await), once exec has returned.
  function exec(code, expose = [], onLine = () => {}) {
    const lines = [];
    const line = (cls, text, args = []) => { const l = { cls, text, args }; lines.push(l); onLine(l); };
    const make = (cls) => (...args) => line(cls, args.map((a) => fmt(a)).join(" "), args);
    const con = { log: make("log"), info: make("log"), warn: make("warn"), error: make("err"), table: make("log") };
    const grab = expose.map((n) => `${JSON.stringify(n)}: typeof ${n} === "undefined" ? undefined : ${n}`).join(", ");
    let error = null, values = {};
    try {
      values = new Function("console", `${code}\n;return { ${grab} };`)(con) || {};
    } catch (err) {
      error = err;
      line("err", `Uncaught ${err.name}: ${err.message}`);
    }
    return { lines, error, values };
  }

  const MUTED = "No output. Use console.log() to print a value.";
  function addLine(out, l) {
    const muted = out.querySelector("li.muted");
    if (muted && l.cls !== "muted") muted.remove();
    const li = document.createElement("li");
    li.className = l.cls;
    li.textContent = l.text;
    out.append(li);
  }
  function render(lines, out) {
    out.innerHTML = "";
    lines.forEach((l) => addLine(out, l));
    if (!lines.length) addLine(out, { cls: "muted", text: MUTED });
  }

  function run(code, out) {
    let live = false;
    const { lines } = exec(code, [], (l) => { if (live) addLine(out, l); });
    render(lines, out);
    live = true;
  }

  function enhance(ta, onRun) {
    ta.spellcheck = false;
    ta.setAttribute("autocapitalize", "off");
    ta.setAttribute("autocomplete", "off");
    const fit = () => { ta.rows = Math.max(3, ta.value.split("\n").length); };
    fit();
    ta.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && (e.metaKey || e.ctrlKey) && onRun) { e.preventDefault(); onRun(); }
      // Tab inserts two spaces; Escape then Tab still moves focus out of the editor.
      if (e.key === "Tab" && !e.shiftKey && !ta.dataset.escaped) {
        e.preventDefault();
        ta.setRangeText("  ", ta.selectionStart, ta.selectionEnd, "end");
        ta.dispatchEvent(new Event("input", { bubbles: true }));
      }
      ta.dataset.escaped = e.key === "Escape" ? "1" : "";
    });
    ta.addEventListener("input", fit);
    return fit;
  }

  function setup(box) {
    if (box.dataset.ready) return;
    box.dataset.ready = "1";
    const ta = box.querySelector("textarea");
    const original = ta.value;
    const bar = document.createElement("div");
    bar.className = "runner-bar";
    bar.innerHTML = `<button class="btn run" type="button">Run ▸</button><button class="btn" type="button">Reset</button><span class="hint">Edit the code, then Run (or Ctrl/⌘ + Enter).</span>`;
    const out = document.createElement("ol");
    out.className = "console";
    out.setAttribute("aria-live", "polite");
    out.setAttribute("aria-label", "Console output");
    box.append(bar, out);
    const [runBtn, resetBtn] = bar.querySelectorAll("button");
    const fit = enhance(ta, () => run(ta.value, out));
    runBtn.addEventListener("click", () => run(ta.value, out));
    resetBtn.addEventListener("click", () => { ta.value = original; fit(); run(ta.value, out); });
    run(ta.value, out);
  }

  window.hlJS = hlJS;
  window.fmtJS = fmt;
  window.Runner = { enhance, exec, render, hlJS, fmt };
  document.querySelectorAll(".runner").forEach(setup);
})();
