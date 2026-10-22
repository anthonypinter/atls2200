/* Live HTML/CSS editor. Write it in a page like this (js/chrome.js loads this file when it finds one):
     <div class="sandbox" data-title="Trail card">
       <textarea data-lang="html">…</textarea>
       <textarea data-lang="css">…</textarea>
       <textarea data-solution="css" hidden>…</textarea>      optional: adds a Show solution button
     </div>
   Either language can be left out. data-height sets the preview height in px (default 260).
   The preview is an iframe that runs no scripts, and links and forms inside it don't navigate.
   window.Sandbox.mount(el, { html, css, solution, title, height, onChange }) builds one from code (js/exercise.js uses it)
   and returns { get(), set(code), update(), frame }; update() resolves once the preview shows the current code. */
(function () {
  let uid = 0;
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const LANGS = { html: "HTML", css: "CSS" };

  function page({ html = "", css = "" }) {
    return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style>${css.replace(/<\/style/gi, "<\\/style")}</style></head><body>${html}</body></html>`;
  }

  function mount(el, opts) {
    const id = ++uid;
    const langs = Object.keys(LANGS).filter((l) => typeof opts[l] === "string");
    const start = Object.fromEntries(langs.map((l) => [l, opts[l]]));
    const title = opts.title || "Sandbox";
    const tabs = langs.length > 1
      ? `<div class="sb-tabs" role="tablist" aria-label="${esc(title)} code">${langs.map((l, i) => `<button class="sb-tab" type="button" role="tab" id="sb${id}-tab-${l}" aria-controls="sb${id}-${l}" aria-selected="${i === 0}" tabindex="${i === 0 ? 0 : -1}">${LANGS[l]}</button>`).join("")}</div>`
      : `<span class="eyebrow">${LANGS[langs[0]]}</span>`;
    el.classList.add("sb");
    el.innerHTML = `<div class="sb-code">${tabs}${langs.map((l, i) => `<div class="sb-panel" id="sb${id}-${l}"${langs.length > 1 ? ` role="tabpanel" aria-labelledby="sb${id}-tab-${l}"` : ""}${i ? " hidden" : ""}><textarea class="sb-editor" aria-label="${esc(title)}: ${LANGS[l]}">${esc(start[l])}</textarea></div>`).join("")}
        <div class="sb-bar"><button class="btn" type="button" data-act="reset">Reset</button>${opts.solution ? `<button class="btn" type="button" data-act="solution" aria-pressed="false">Show solution</button>` : ""}<span class="hint">The preview updates as you type.</span></div>
      </div>
      <div class="sb-preview"><span class="eyebrow">Preview</span><iframe sandbox="allow-same-origin" title="${esc(title)}: preview" style="height:${opts.height || 260}px"></iframe></div>`;

    const areas = Object.fromEntries(langs.map((l) => [l, el.querySelector(`#sb${id}-${l} textarea`)]));
    const frame = el.querySelector("iframe");
    const fits = langs.map((l) => window.Runner.enhance(areas[l]));
    const get = () => Object.fromEntries(langs.map((l) => [l, areas[l].value]));

    // Each render replaces the iframe document; ready resolves when it has loaded.
    let ready = Promise.resolve();
    function render() {
      const scroll = frame.contentWindow ? frame.contentWindow.scrollY : 0;
      ready = new Promise((resolve) => {
        frame.addEventListener("load", () => {
          const doc = frame.contentDocument;
          doc.addEventListener("click", (e) => { const a = e.target.closest("a[href]"); if (a && !a.getAttribute("href").startsWith("#")) e.preventDefault(); });
          doc.addEventListener("submit", (e) => e.preventDefault());
          frame.contentWindow.scrollTo(0, scroll);
          resolve();
        }, { once: true });
      });
      frame.srcdoc = page(get());
      return ready;
    }
    let timer, dirty = false;
    let typed = false;
    function changed(e) {
      // Typing in the editor (not Reset or Show solution) is what counts as using it, once per editor.
      if (e?.isTrusted && !typed && window.Progress) { typed = true; window.Progress.used(el, "edit"); }
      dirty = true;
      clearTimeout(timer);
      timer = setTimeout(() => { dirty = false; render(); }, 250);
      if (opts.onChange) opts.onChange(get());
    }
    function set(code) {
      langs.forEach((l, i) => { if (typeof code[l] === "string") { areas[l].value = code[l]; fits[i](); } });
      clearTimeout(timer);
      dirty = false;
      if (opts.onChange) opts.onChange(get());
      return render();
    }
    langs.forEach((l) => areas[l].addEventListener("input", changed));

    // Tabs: click or arrow keys, following the ARIA tabs pattern.
    const tabEls = [...el.querySelectorAll(".sb-tab")];
    function select(tab) {
      tabEls.forEach((t) => {
        const on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        el.querySelector("#" + t.getAttribute("aria-controls")).hidden = !on;
      });
    }
    tabEls.forEach((t, i) => {
      t.addEventListener("click", () => select(t));
      t.addEventListener("keydown", (e) => {
        const step = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (!step) return;
        const next = tabEls[(i + step + tabEls.length) % tabEls.length];
        select(next);
        next.focus();
      });
    });

    // Show solution swaps in the answer; pressing it again brings back what was there before.
    let mine = null;
    const solBtn = el.querySelector('[data-act="solution"]');
    if (solBtn) solBtn.addEventListener("click", () => {
      if (mine) { set(mine); mine = null; }
      else { mine = get(); set({ ...mine, ...opts.solution }); }
      solBtn.setAttribute("aria-pressed", String(!!mine));
      solBtn.textContent = mine ? "Back to my code" : "Show solution";
    });
    el.querySelector('[data-act="reset"]').addEventListener("click", () => {
      mine = null;
      if (solBtn) { solBtn.setAttribute("aria-pressed", "false"); solBtn.textContent = "Show solution"; }
      set(start);
    });

    render();
    return {
      frame, get, set,
      update() {
        if (!dirty) return ready;
        clearTimeout(timer);
        dirty = false;
        return render();
      },
    };
  }

  function setup(box) {
    if (box.dataset.ready) return;
    box.dataset.ready = "1";
    const opts = { title: box.dataset.title, height: box.dataset.height };
    box.querySelectorAll("textarea[data-lang]").forEach((t) => { opts[t.dataset.lang] = t.value; });
    const sol = box.querySelectorAll("textarea[data-solution]");
    if (sol.length) opts.solution = Object.fromEntries([...sol].map((t) => [t.dataset.solution, t.value]));
    mount(box, opts);
  }

  window.Sandbox = { mount };
  loadScript("js/runner.js").then(() => document.querySelectorAll(".sandbox").forEach(setup));
})();
