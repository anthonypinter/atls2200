/* Glossary pop-ups in lessons. A term becomes a button that opens its definition from glossary-terms.js:
   - automatically, when bold text in the lede, a section intro or the Key ideas / Common mistakes panels is exactly a
     glossary term (singular or plural), e.g. <strong>main axis</strong>;
   - explicitly, with <span class="term">flex container</span>, or <span class="term" data-term="Flexbox">flex
     layout</span> when the words differ from the glossary entry.
   Only the first mention of each term on a page gets a pop-up. js/chrome.js loads this file and the terms when a page
   has candidates. The pop-up uses the browser's popover, so Escape and clicking elsewhere close it. */
(function () {
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const CATS = { html: "HTML", css: "CSS", layout: "Layout", js: "JavaScript", workflow: "Workflow" };
  const norm = (s) => s.toLowerCase().replace(/\s+/g, " ").trim();

  // Every way a term can be written: "Truthy / falsy" → "truthy / falsy", "truthy", "falsy".
  const lookup = new Map();
  for (const entry of window.GLOSSARY) {
    const [term] = entry;
    const names = [term, term.replace(/\s*\(.*\)\s*$/, ""), ...(term.match(/\(([^)]+)\)/)?.slice(1) || []), ...term.split(" / ")];
    for (const n of names) {
      const k = norm(n);
      if (k && !lookup.has(k)) lookup.set(k, entry);
    }
  }
  // Also try the singular: "selectors" → "selector", "classes" → "class".
  const find = (text) => {
    const k = norm(text);
    return lookup.get(k) || (/[a-z]s$/.test(k) && (lookup.get(k.slice(0, -1)) || (k.endsWith("es") && lookup.get(k.slice(0, -2)))));
  };

  const here = (decodeURIComponent(location.pathname.split("/").pop()) || "index.html");
  const tip = document.createElement("div");
  tip.className = "term-tip";
  tip.id = "term-tip";
  tip.setAttribute("popover", "auto");
  tip.setAttribute("role", "dialog");
  document.body.append(tip);

  const wrap = document.querySelector(".wrap");
  const auto = [...wrap.querySelectorAll(".page-head strong, .section-title strong, .notes strong")].filter((s) => !s.closest("a, button, code, .term"));
  const explicit = [...wrap.querySelectorAll(".term")];
  const done = new Set();
  let n = 0;
  for (const el of [...explicit, ...auto].sort((a, b) => (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1))) {
    const entry = find(el.dataset.term || el.textContent);
    if (!entry) { if (explicit.includes(el)) console.warn(`No glossary entry for "${el.dataset.term || el.textContent}"`); continue; }
    if (done.has(entry)) continue;
    done.add(entry);
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "term-btn";
    btn.id = "term-btn-" + ++n;
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-controls", "term-tip");
    btn.setAttribute("aria-haspopup", "dialog");
    btn.append(...el.childNodes);
    el.append(btn);
    btn.entry = entry;
  }

  let openBtn = null;
  function place(btn) {
    const r = btn.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight;
    const left = Math.min(Math.max(8, r.left), innerWidth - w - 8);
    const below = r.bottom + 8 + h < innerHeight || r.top - 8 - h < 0;
    tip.style.left = left + scrollX + "px";
    tip.style.top = (below ? r.bottom + 8 : r.top - 8 - h) + scrollY + "px";
  }
  function open(btn) {
    const [term, cat, def, ex, pageHref] = btn.entry;
    const lesson = pageHref && pageHref !== here && window.BOOK?.lessons.find((l) => l.href === pageHref);
    tip.innerHTML = `<p class="term-head"><strong id="term-tip-title">${esc(term)}</strong><span class="eyebrow">${CATS[cat] || cat}</span></p>
      <p>${esc(def)}</p>${ex ? `<code class="term-ex">${esc(ex)}</code>` : ""}
      <p class="term-links">${lesson ? `<a href="${lesson.href}">Lesson ${lesson.num}: ${esc(lesson.title)}</a>` : ""}<a href="glossary.html#${glossaryId(term)}">Glossary →</a></p>`;
    tip.setAttribute("aria-labelledby", "term-tip-title");
    if (tip.matches(":popover-open")) tip.hidePopover();
    tip.showPopover({ source: btn });   // source keeps a click on the term from light-dismissing its own pop-up
    place(btn);
    openBtn = btn;
    btn.setAttribute("aria-expanded", "true");
  }
  tip.addEventListener("toggle", (e) => {
    if (e.newState === "closed" && openBtn) { openBtn.setAttribute("aria-expanded", "false"); openBtn = null; }
  });
  wrap.addEventListener("click", (e) => {
    const btn = e.target.closest(".term-btn");
    if (!btn) return;
    if (openBtn === btn && tip.matches(":popover-open")) tip.hidePopover();
    else open(btn);
  });
  addEventListener("resize", () => { if (openBtn) place(openBtn); });
})();
