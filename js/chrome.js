/* Book chrome: reads window.BOOK (book.js) and adds the textbook's reading layout to every page.
   - Theme: applies the saved light/dark choice right away (this file loads in <head>, so there's no flash),
     then adds a toggle that cycles System → Light → Dark.
   - Top bar: Contents button, breadcrumbs (Contents › Part › Lesson), Search and a glossary link. Replaces the static
     .crumbs nav. Search (js/search.js) also opens with Ctrl/⌘ + K, or / on pages without their own filter box.
   - Components: loadScript() loads js/runner.js, js/sandbox.js and the glossary pop-ups only on pages that use them,
     and queues makeExercise() calls until js/exercise.js arrives.
   - Sidebar: the table of contents with the current lesson highlighted and its sections listed under it.
     Docked beside the page on wide screens (open/closed is remembered), a drawer on narrow ones.
   - Footer: fills <footer data-book-nav> with a Mark complete button and previous/next links in reading order.
   - Progress (js/progress.js): records the visit, then shows checkmarks and per-part counts in the sidebar.
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
  // Pages call makeExercise() inline, before js/exercise.js has loaded; calls wait in a queue until it arrives.
  if (!window.makeExercise) {
    const queue = [];
    window.makeExercise = (...args) => { queue.push(args); loadScript("js/exercise.js"); };
    window.makeExercise.queue = queue;
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
    if (slug !== "glossary" && wrap.querySelector(".term, .page-head strong, .section-title strong, .notes strong")) {
      loadScript("glossary-terms.js").then(() => loadScript("js/glossary.js"));
    }

    const eyebrow = wrap.querySelector(".page-head .eyebrow");
    if (eyebrow && current) eyebrow.prepend(`${current.num} · `);

    const bar = buildBar();
    const crumbs = wrap.querySelector(":scope > .crumbs, :scope > .crumb");
    if (crumbs) crumbs.replaceWith(bar); else wrap.prepend(bar);

    const toc = buildToc(current ? sectionsOf(wrap) : []);
    const backdrop = document.createElement("div");
    backdrop.className = "book-backdrop";
    backdrop.hidden = true;
    const skip = document.createElement("a");
    skip.className = "book-skip";
    skip.href = "#" + wrap.id;
    skip.textContent = "Skip to content";
    document.body.prepend(skip, toc, backdrop);

    fillFooter();
    if (P) {
      if (current) P.visit(slug);
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
  });

  function buildBar() {
    const bar = document.createElement("div");
    bar.className = "book-bar";
    const trail = [`<li><a href="index.html">Contents</a></li>`];
    if (current) trail.push(`<li><a href="index.html#part-${current.part.num}">Part ${current.part.num} · ${esc(current.part.title)}</a></li>`, `<li aria-current="page">${current.num} ${esc(current.title)}</li>`);
    else if (slug === "glossary") trail.push(`<li aria-current="page">Glossary</li>`);
    bar.innerHTML = `<button class="btn book-menu" type="button" aria-controls="book-toc" aria-expanded="false"><span aria-hidden="true">☰</span> Contents</button>`
      + (slug === "index" ? "" : `<nav class="book-crumbs" aria-label="Breadcrumb"><ol>${trail.join("")}</ol></nav>`)
      + `<div class="book-tools"><button class="btn book-search" type="button" aria-haspopup="dialog" aria-keyshortcuts="Control+K Meta+K"><span aria-hidden="true">⌕</span> Search</button>${slug === "glossary" ? "" : `<a class="crumb" href="glossary.html">Glossary</a>`}<button class="btn book-theme" type="button"></button></div>`;
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
      return { id: h.id, text: h.textContent.trim() };
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
        ? `<p class="book-sec-label">On this page</p><ol class="book-sections">${sections.map((s) => `<li><a href="#${s.id}">${esc(s.text)}</a></li>`).join("")}</ol>`
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
