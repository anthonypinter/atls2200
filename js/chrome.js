/* Book chrome: reads window.BOOK (book.js) and adds the textbook's reading layout to every page.
   - Theme: applies the saved light/dark choice right away (this file loads in <head>, so there's no flash),
     then adds a toggle that cycles System → Light → Dark.
   - Top bar: Contents button, breadcrumbs (Home › Part › Lesson), Search and a glossary link. Replaces the static
     .crumbs nav. Search (js/search.js) also opens with Ctrl/⌘ + K, or / on pages without their own filter box.
   - Components: loadScript() loads js/runner.js, js/sandbox.js and the glossary pop-ups only on pages that use them,
     and queues makeExercise() calls until js/exercise.js arrives.
   - Sidebar: the table of contents with the current lesson highlighted and its sections listed under it.
     Docked beside the page on wide screens (open/closed is remembered), a drawer on narrow ones.
   - Footer: fills <footer data-book-nav> with a Mark complete button and previous/next links in reading order.
   - Progress (js/progress.js): records the visit, then shows checkmarks and per-part counts in the sidebar.
     Each section's active reading time is recorded, and whether the student did what it asks (see trackSections);
     "On this page" ticks off finished sections.
   - Accounts: when book.js has a backend configured, loads js/backend.js (sign-in, sync, instructor notes).
   - Print: opens every <details> while printing.
   Without JavaScript the static crumbs and footer still link back to the contents. */
(function () {
  const book = window.BOOK;
  const root = document.documentElement;
  const store = {
    get: (k) => { try { return localStorage.getItem(k); } catch { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch {} },
  };
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

  // Theme goes first, before anything paints.
  const THEMES = ["system", "light", "dark"];
  let theme = THEMES.includes(store.get("book:theme")) ? store.get("book:theme") : "system";
  const applyTheme = () => { if (theme === "system") delete root.dataset.theme; else root.dataset.theme = theme; };
  applyTheme();

  // Components load only on pages that use them. loadScript runs a script once and resolves when it has run;
  // a script the page already includes with its own <script> tag has run by the time the DOM is ready.
  const loading = {};
  window.loadScript = (src) => loading[src] ||= new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", () => resolve());
      else resolve();
      return;
    }
    const s = document.createElement("script");
    s.src = src;
    s.onload = () => resolve();
    s.onerror = () => reject(new Error("Could not load " + src));
    document.head.append(s);
  });
  // Pages call makeExercise() inline, before js/exercise.js has loaded. Exercises sit below the fold, so each call
  // waits until its exercise is nearly on screen; then js/exercise.js (and the editor it needs) loads and runs the
  // queued calls. exercise.js replaces window.makeExercise with the real one, which has no .queue.
  if (!window.makeExercise) {
    const queue = [];
    const start = (args) => {
      if (!window.makeExercise.queue) return window.makeExercise(...args);
      queue.push(args);
      loadScript("js/exercise.js");
    };
    const waiting = new Map();   // exercise element → its makeExercise() arguments
    const go = (el) => { if (!waiting.has(el)) return; near.unobserve(el); start(waiting.get(el)); waiting.delete(el); };
    const near = "IntersectionObserver" in window && new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) go(e.target);
    }, { rootMargin: "600px 0px" });
    window.makeExercise = (...args) => {
      if (args[0]) args[0].exerciseDef = args[1];   // print.html reads the task, starter code and solution from here
      if (near && args[0]) { waiting.set(args[0], args); near.observe(args[0]); } else start(args);
    };
    window.makeExercise.queue = queue;
    // Start everything now: before printing, and for tests that can't scroll.
    window.makeExercise.startAll = () => [...waiting.keys()].forEach(go);
    addEventListener("beforeprint", () => window.makeExercise.startAll?.());
  }

  if (!book) return;

  // Number every lesson <part>.<position> and keep a flat list in reading order (index.html uses both).
  const lessons = [];
  book.parts.forEach((part, p) => {
    part.num = p + 1;
    part.lessons.forEach((l, i) => {
      Object.assign(l, { num: `${p + 1}.${i + 1}`, part, href: l.slug + ".html" });
      lessons.push(l);
    });
  });
  book.lessons = lessons;
  // Related lessons: book.js lists each pair once, and the link shows on both lessons.
  const related = new Map(lessons.map((l) => [l.slug, new Set()]));
  for (const l of lessons) for (const r of l.related || []) { related.get(l.slug).add(r); related.get(r)?.add(l.slug); }

  const P = window.Progress;
  const slug = P ? P.page : (decodeURIComponent(location.pathname.split("/").pop()) || "index.html").replace(/\.html?$/, "");
  const at = lessons.findIndex((l) => l.slug === slug);
  const current = lessons[at];
  const wide = matchMedia("(min-width: 1100px)");

  document.addEventListener("DOMContentLoaded", () => {
    const wrap = document.querySelector(".wrap");
    if (!wrap) return;
    wrap.id ||= "content";

    if (document.querySelector(".runner")) loadScript("js/runner.js");
    if (document.querySelector(".sandbox")) loadScript("js/sandbox.js");
    if (document.querySelector("pre[data-lang]")) loadScript("js/highlight.js");
    if (slug !== "glossary" && wrap.querySelector(".term, .page-head strong, .section-title strong, .notes strong")) {
      loadScript("glossary-terms.js").then(() => loadScript("js/glossary.js"));
    }

    const eyebrow = wrap.querySelector(".page-head .eyebrow");
    if (eyebrow && current) {
      eyebrow.prepend(`${current.num} · `);
      if (current.minutes) eyebrow.append(` · About ${current.minutes} min`);
    }

    const bar = buildBar();
    const crumbs = wrap.querySelector(":scope > .crumbs, :scope > .crumb");
    if (crumbs) crumbs.replaceWith(bar); else wrap.prepend(bar);

    const sections = current ? sectionsOf(wrap) : [];
    const toc = buildToc(sections);
    const backdrop = document.createElement("div");
    backdrop.className = "book-backdrop";
    backdrop.hidden = true;
    const skip = document.createElement("a");
    skip.className = "book-skip";
    skip.href = "#" + wrap.id;
    skip.textContent = "Skip to content";
    document.body.prepend(skip, toc, backdrop);

    fillFooter();

    // Boxes that scroll (code samples, demo frames) must be reachable with Tab, or keyboard users can't scroll them.
    const focusScrollers = () => {
      for (const el of wrap.querySelectorAll("pre, div, ol, ul, table, section")) {
        if (el.hasAttribute("tabindex") || (el.scrollWidth <= el.clientWidth + 1 && el.scrollHeight <= el.clientHeight + 1)) continue;
        const s = getComputedStyle(el);
        if (!/auto|scroll/.test(s.overflowX + s.overflowY) || el.querySelector("a[href], button, input, select, textarea, [tabindex]")) continue;
        el.tabIndex = 0;
      }
    };
    addEventListener("load", () => { focusScrollers(); setTimeout(focusScrollers, 1500); });
    let resizing;
    addEventListener("resize", () => { clearTimeout(resizing); resizing = setTimeout(focusScrollers, 300); });

    const printing = new URLSearchParams(location.search).has("print");
    if (P) {
      // print.html loads lessons in a hidden frame with ?print; that isn't a visit.
      if (current && !printing) { P.visit(slug); trackSections(wrap, sections); }
      const paint = () => paintProgress(toc);
      P.subscribe(paint);
      paint();
    }

    // Sidebar state: docked (wide screens, remembered) or drawer (narrow screens, always starts closed).
    const menu = bar.querySelector(".book-menu");
    const pref = store.get("book:toc");
    let docked = pref ? pref === "open" : !!current;
    let drawer = false;

    function sync() {
      const show = wide.matches ? docked : drawer;
      toc.hidden = !show;
      backdrop.hidden = wide.matches || !drawer;
      wrap.inert = !wide.matches && drawer;
      root.classList.toggle("toc-docked", wide.matches && docked);
      menu.setAttribute("aria-expanded", String(show));
    }
    function setOpen(open, returnFocus) {
      if (wide.matches) { docked = open; store.set("book:toc", open ? "open" : "closed"); }
      else drawer = open;
      sync();
      if (open && !wide.matches) (toc.querySelector('[aria-current="page"]') || toc.querySelector("a")).focus();
      if (!open && returnFocus) menu.focus();
    }

    menu.addEventListener("click", () => setOpen(menu.getAttribute("aria-expanded") !== "true"));
    toc.querySelector(".book-close").addEventListener("click", () => setOpen(false, true));
    backdrop.addEventListener("click", () => setOpen(false, true));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && drawer && !wide.matches) setOpen(false, true); });
    // Jumping to a section from the drawer should reveal the page underneath.
    toc.addEventListener("click", (e) => { if (e.target.closest('a[href^="#"]') && !wide.matches) setOpen(false); });
    wide.addEventListener("change", () => { drawer = false; sync(); });
    sync();

    const here = toc.querySelector('[aria-current="page"]');
    if (here && !toc.hidden) toc.scrollTop = here.offsetTop - toc.clientHeight / 3;

    // Search loads its index the first time it's opened.
    const openSearch = () => loadScript("search-index.js").then(() => loadScript("js/search.js")).then(() => Search.open());
    bar.querySelector(".book-search").addEventListener("click", openSearch);
    document.addEventListener("keydown", (e) => {
      const typing = e.target.closest?.("input, textarea, select, [contenteditable]");
      if ((e.key === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !typing && !document.getElementById("filter") && !document.getElementById("q"))) {
        e.preventDefault();
        openSearch();
      }
    });

    const themeBtn = bar.querySelector(".book-theme");
    const label = () => { themeBtn.textContent = `◐ Theme: ${theme[0].toUpperCase() + theme.slice(1)}`; };
    themeBtn.addEventListener("click", () => {
      theme = THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length];
      store.set("book:theme", theme);
      applyTheme();
      label();
    });
    label();

    if (book.backend?.url && !printing) loadScript("js/backend.js");
  });

  function buildBar() {
    const bar = document.createElement("div");
    bar.className = "book-bar";
    const trail = [`<li><a href="index.html">Home</a></li>`];
    if (current) trail.push(`<li><a href="index.html#part-${current.part.num}">Part ${current.part.num} · ${esc(current.part.title)}</a></li>`, `<li aria-current="page">${current.num} ${esc(current.title)}</li>`);
    else if (slug === "glossary") trail.push(`<li aria-current="page">Glossary</li>`);
    else if (slug === "instructor") trail.push(`<li aria-current="page">Instructor dashboard</li>`);
    bar.innerHTML = `<button class="btn book-menu" type="button" aria-controls="book-toc" aria-expanded="false"><span aria-hidden="true">☰</span> Contents</button>`
      + (slug === "index" ? "" : `<nav class="book-crumbs" aria-label="Breadcrumb"><ol>${trail.join("")}</ol></nav>`)
      + `<div class="book-tools"><button class="btn book-search" type="button" aria-haspopup="dialog" aria-keyshortcuts="Control+K Meta+K"><span aria-hidden="true">⌕</span> Search</button>${current ? `<a class="crumb" href="print.html?lesson=${current.slug}">Print</a>` : ""}${slug === "glossary" ? "" : `<a class="crumb" href="glossary.html">Glossary</a>`}<button class="btn book-theme" type="button"></button></div>`;
    return bar;
  }

  // The page's section headings become "On this page" links; headings without an id get one.
  // Only real sections count, not h2s inside playground demos (e.g. the trail cards on the Selectors page).
  function sectionsOf(wrap) {
    const heads = [...wrap.querySelectorAll(".section-title > h2, .notes h2")];
    if (heads.length < 2) return [];
    const used = new Set([...document.querySelectorAll("[id]")].map((el) => el.id));
    return heads.map((h) => {
      if (!h.id) {
        const base = "sec-" + (h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "section");
        let id = base, n = 2;
        while (used.has(id)) id = `${base}-${n++}`;
        used.add(id);
        h.id = id;
      }
      // kind is the eyebrow above the heading (Read, Play, Practice, …); notes panels have none.
      const kind = h.closest(".notes") ? "notes" : h.parentElement.querySelector(".eyebrow")?.textContent.trim() || "";
      return { id: h.id, text: h.textContent.trim(), kind };
    });
  }

  function buildToc(sections) {
    const aside = document.createElement("aside");
    aside.id = "book-toc";
    aside.className = "book-toc";
    aside.hidden = true;
    const lessonLink = (l) => {
      const here = l === current;
      const subs = here && sections.length
        ? `<p class="book-sec-label">On this page</p><ol class="book-sections">${sections.map((s) => `<li><a href="#${s.id}" data-sec="${s.id}" data-kind="${esc(s.kind)}">${esc(s.text)}<span class="sr-only book-done-label"></span></a></li>`).join("")}</ol>`
        : "";
      return `<li><a href="${l.href}" data-slug="${l.slug}"${here ? ' aria-current="page"' : ""}><span class="book-num">${l.num}</span><span>${esc(l.title)}<span class="sr-only book-done-label"></span></span><span class="book-check" aria-hidden="true">✓</span></a>${subs}</li>`;
    };
    aside.innerHTML = `<div class="book-toc-head"><a class="book-toc-title" href="index.html">${esc(book.title)}</a><button class="btn book-close" type="button" aria-label="Close contents">✕</button></div>
      <nav aria-label="Table of contents">${book.parts.map((part) => `
        <details class="book-part"${current && current.part === part ? " open" : ""}>
          <summary><span class="book-num">Part ${part.num}</span> ${esc(part.title)} <span class="book-count" data-part="${part.num}"></span></summary>
          <ol>${part.lessons.map(lessonLink).join("")}</ol>
        </details>`).join("")}
        <a class="book-back" href="glossary.html"${slug === "glossary" ? ' aria-current="page"' : ""}>Glossary</a>
      </nav>`;
    return aside;
  }

  // Which section each part of the page belongs to: everything after a section heading up to the next one, and each
  // notes panel on its own. Then two measures per section (stored by js/progress.js):
  // - Reading time: a second counts for every section on screen while the tab is visible and the student has
  //   scrolled, typed or moved the pointer in the last IDLE_MS. A section is seen once that time reaches its bar:
  //   about 30% of the time it takes to read at 200 words a minute (between 5 and 90 seconds), or 5 seconds for
  //   sections that ask the student to do something, since those are judged by what they do.
  // - Used: the components report what happened (Progress.used): Run with edited code, typing in a live editor,
  //   pressing Check, answering a whole quiz. Playground controls count once the student has changed two different
  //   ones (or the only one there is). Glossary terms, links and copy buttons don't count.
  const IDLE_MS = 60000, FLUSH_MS = 15000, MIN_BAR = 5000, MAX_BAR = 90000, MS_PER_WORD = 90;
  const CONTROL = 'button, input, select, textarea, [role="button"], [role="tab"], [role="slider"], [contenteditable="true"]';
  const OWN_SIGNALS = ".runner, .sandbox, .exercise, .quiz, .term, .term-btn, .term-tip, .copy";
  function trackSections(wrap, sections) {
    if (!sections.length) return;
    const owner = new Map();
    let sec = null;
    for (const el of wrap.children) {
      if (el.matches(".section-title")) sec = el.querySelector(":scope > h2")?.id || sec;
      if (el.matches(".notes")) { el.querySelectorAll("h2[id]").forEach((h) => owner.set(h.parentElement, h.id)); continue; }
      if (sec && !el.matches("script, style, footer, nav, .book-bar, .book-related")) owner.set(el, sec);
    }
    const key = (id) => `${slug}/${id}`;
    const ownerOf = (el) => { while (el && !owner.has(el)) el = el.parentElement; return el && owner.get(el); };
    const partsOf = (id) => [...owner].filter(([, s]) => s === id).map(([el]) => el);

    const bars = {}, total = {}, pending = {}, seen = {};
    for (const s of sections) {
      const words = partsOf(s.id).reduce((n, el) => n + (el.textContent.match(/\S+/g) || []).length, 0);
      bars[key(s.id)] = P.needsUse(s.kind) ? MIN_BAR : Math.min(MAX_BAR, Math.max(MIN_BAR, words * MS_PER_WORD));
      const rec = P.section(key(s.id));
      total[s.id] = rec?.ms || 0;
      seen[s.id] = !!rec?.seen;
    }

    const showing = new Map();
    const io = "IntersectionObserver" in window && new IntersectionObserver((entries) => {
      for (const e of entries) {
        const id = owner.get(e.target);
        const set = showing.get(id) || new Set();
        showing.set(id, set);
        if (e.isIntersecting) set.add(e.target); else set.delete(e.target);
      }
    }, { rootMargin: "-15% 0px -15% 0px" });
    if (io) for (const el of owner.keys()) io.observe(el);

    let lastActive = Date.now(), lastTick = Date.now();
    for (const type of ["scroll", "wheel", "pointermove", "pointerdown", "keydown", "touchstart"]) {
      addEventListener(type, () => { lastActive = Date.now(); }, { passive: true, capture: true });
    }
    function flush() {
      const times = {};
      for (const id of Object.keys(pending)) { times[key(id)] = pending[id]; total[id] += pending[id]; delete pending[id]; }
      P.addTime(times, bars);
      for (const id of Object.keys(times)) if (total[id.split("/")[1]] >= bars[id]) seen[id.split("/")[1]] = true;
    }
    setInterval(() => {
      const t = Date.now(), dt = Math.min(t - lastTick, 2000);
      lastTick = t;
      if (document.visibilityState !== "visible" || t - lastActive > IDLE_MS) return;
      let crossed = false;
      for (const [id, set] of showing) {
        if (!set.size) continue;
        pending[id] = (pending[id] || 0) + dt;
        if (!seen[id] && total[id] + pending[id] >= bars[key(id)]) crossed = true;
      }
      if (crossed) flush();   // tick the sidebar as soon as a section is seen, not at the next flush
    }, 1000);
    setInterval(flush, FLUSH_MS);
    addEventListener("pagehide", flush);
    document.addEventListener("visibilitychange", () => { if (document.visibilityState === "hidden") flush(); });

    // Used: signals from the components, and distinct playground controls.
    wrap.addEventListener("book:use", (e) => {
      const id = ownerOf(e.target), what = e.detail?.what;
      if (!id) return;
      if (what === "run" || what === "run-unchanged") P.log("run", key(id), { edited: what === "run" });
      if (what !== "run-unchanged") P.interact(key(id), what);
    });
    const changed = new Map();   // section → controls the student has changed
    const touch = (e) => {
      if (!e.isTrusted) return;
      const ctl = e.target.closest?.(CONTROL);
      if (!ctl || ctl.closest(OWN_SIGNALS)) return;
      const id = ownerOf(ctl);
      if (!id || P.section(key(id))?.interacted) return;
      const set = changed.get(id) || new Set();
      changed.set(id, set);
      set.add(ctl);
      const available = partsOf(id).flatMap((el) => [...el.querySelectorAll(CONTROL)]).filter((c) => !c.closest(OWN_SIGNALS)).length;
      if (set.size >= Math.min(2, Math.max(1, available))) P.interact(key(id), "controls");
    };
    for (const type of ["click", "input", "change"]) wrap.addEventListener(type, touch, true);
  }

  function fillFooter() {
    const foot = document.querySelector("footer[data-book-nav]");
    if (!foot || !current) return;
    const prev = lessons[at - 1], next = lessons[at + 1];
    const step = (l, dir) => {
      if (!l) return `<a class="book-step ${dir}" href="index.html"><span class="eyebrow">${dir === "prev" ? "← Back to" : "Finished! →"}</span><span>Contents</span></a>`;
      const newPart = l.part !== current.part && dir === "next" ? `Part ${l.part.num} · ${esc(l.part.title)} →` : "";
      return `<a class="book-step ${dir}" href="${l.href}"><span class="eyebrow">${dir === "prev" ? "← Previous" : newPart || "Next →"}</span><span>${l.num} ${esc(l.title)}</span></a>`;
    };
    const done = P ? `<div class="book-done"><span>Finished this lesson?</span><button class="btn" type="button" aria-pressed="false">Mark lesson complete</button></div>` : "";
    foot.innerHTML = done + step(prev, "prev") + step(next, "next");
    const rel = lessons.filter((l) => related.get(slug).has(l.slug));
    if (rel.length) foot.insertAdjacentHTML("beforebegin", `<nav class="book-related" aria-label="Related lessons"><h2>Related lessons</h2><ul>${rel.map((l) => `<li><a href="${l.href}"><span class="book-num">${l.num}</span>${esc(l.title)}</a></li>`).join("")}</ul></nav>`);
    foot.classList.add("book-foot");
    const btn = foot.querySelector(".book-done button");
    if (btn) btn.addEventListener("click", () => P.setComplete(slug, btn.getAttribute("aria-pressed") !== "true"));
  }

  // Checkmarks, per-part counts and the Mark complete button, redrawn whenever progress changes (in any tab).
  function paintProgress(toc) {
    const data = P.data().lessons;
    const isDone = (s) => !!data[s]?.completed;
    toc.querySelectorAll("a[data-slug]").forEach((a) => {
      const d = isDone(a.dataset.slug);
      a.classList.toggle("done", d);
      a.querySelector(".book-done-label").textContent = d ? " (completed)" : "";
    });
    book.parts.forEach((part) => {
      const n = part.lessons.filter((l) => isDone(l.slug)).length;
      const el = toc.querySelector(`.book-count[data-part="${part.num}"]`);
      el.innerHTML = `<span aria-hidden="true">${n}/${part.lessons.length}</span><span class="sr-only">, ${n} of ${part.lessons.length} complete</span>`;
      el.classList.toggle("all", n === part.lessons.length);
    });
    const secs = P.data().sections;
    toc.querySelectorAll("a[data-sec]").forEach((a) => {
      const d = P.sectionDone(secs[`${slug}/${a.dataset.sec}`], a.dataset.kind);
      a.classList.toggle("done", d);
      a.querySelector(".book-done-label").textContent = d ? " (done)" : "";
    });
    const btn = document.querySelector(".book-done button");
    if (btn) {
      const d = isDone(slug);
      btn.setAttribute("aria-pressed", String(d));
      btn.textContent = d ? "✓ Completed" : "Mark lesson complete";
    }
  }

  let opened = [];
  addEventListener("beforeprint", () => {
    opened = [...document.querySelectorAll(".wrap details:not([open])")];
    opened.forEach((d) => { d.open = true; });
  });
  addEventListener("afterprint", () => { opened.forEach((d) => { d.open = false; }); });
})();
