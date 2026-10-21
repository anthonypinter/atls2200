/* Search across every lesson section and glossary term, using search-index.js (built by scripts/check.mjs --write, which the publish workflow runs before every deploy).
   js/chrome.js loads both files the first time someone opens search: the Search button, Ctrl/⌘ + K, or / on pages
   that don't have their own filter box. Results link straight to the section. Enter opens the top result, and the
   arrow keys move between results. */
(function () {
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const { lessons, terms } = window.SEARCH_INDEX;

  // One searchable document per lesson, per section and per glossary term. "key" is what a title match is tested on.
  const docs = [];
  for (const l of lessons) {
    const href = l.slug + ".html";
    docs.push({ kind: "Lesson", lesson: l.slug, href, title: `${l.num} ${l.title}`, text: l.desc + " " + l.intro, more: l.more, key: `${l.title} ${l.props.join(" ")}` });
    for (const s of l.sections) docs.push({ kind: "Section", lesson: l.slug, href: `${href}#${s.id}`, title: `${l.num} ${l.title} › ${s.title}`, text: s.text, key: s.title });
  }
  for (const t of terms) docs.push({ kind: "Glossary", href: `glossary.html#${t.id}`, title: t.term, text: `${t.def} ${t.ex}`, key: t.term });
  // text is shown as the snippet; more (playground labels) only counts toward matching.
  for (const d of docs) { d.hay = `${d.title} ${d.key} ${d.text} ${d.more || ""}`.toLowerCase(); d.keyL = d.key.toLowerCase(); }

  function search(query) {
    const q = query.trim().toLowerCase();
    const words = q.split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    const scored = [];
    for (const d of docs) {
      if (!words.every((w) => d.hay.includes(w))) continue;
      let score = 0;
      if (d.keyL === q) score += 40;
      if (d.keyL.includes(q)) score += 20;
      for (const w of words) if (d.keyL.includes(w)) score += 6;
      if (d.hay.includes(q)) score += 4;
      if (d.kind === "Lesson") score += 2;
      scored.push({ d, score });
    }
    scored.sort((a, b) => b.score - a.score);
    // At most three results from any one lesson, so one long page can't fill the list.
    const per = {};
    return scored.filter(({ d }) => !d.lesson || (per[d.lesson] = (per[d.lesson] || 0) + 1) <= 3).slice(0, 25).map((r) => r.d);
  }

  function snippet(text, words) {
    const lower = text.toLowerCase();
    const at = Math.max(0, ...words.map((w) => lower.indexOf(w)).filter((i) => i >= 0).slice(0, 1));
    const start = Math.max(0, at - 50);
    const piece = (start ? "…" : "") + text.slice(start, start + 150) + (start + 150 < text.length ? "…" : "");
    const re = new RegExp(words.map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|"), "gi");
    let out = "", last = 0;
    piece.replace(re, (m, i) => { out += esc(piece.slice(last, i)) + "<mark>" + esc(m) + "</mark>"; last = i + m.length; return m; });
    return out + esc(piece.slice(last));
  }

  const dialog = document.createElement("dialog");
  dialog.className = "search-dialog";
  dialog.setAttribute("aria-label", "Search the book");
  dialog.innerHTML = `<form method="dialog" class="search-head">
      <label class="sr-only" for="search-q">Search lessons and glossary</label>
      <input id="search-q" type="search" placeholder="Search lessons and glossary, e.g. gap" autocomplete="off" spellcheck="false">
      <button class="btn" value="close" type="submit" formnovalidate aria-label="Close search">Esc</button>
    </form>
    <p class="search-status" role="status"></p>
    <ol class="search-results"></ol>`;
  document.body.append(dialog);
  const input = dialog.querySelector("input"), list = dialog.querySelector(".search-results"), status = dialog.querySelector(".search-status");

  let timer;
  function update() {
    const q = input.value.trim();
    const words = q.toLowerCase().split(/\s+/).filter(Boolean);
    const found = search(q);
    list.innerHTML = found.map((d) => `<li><a href="${d.href}"><span class="search-kind">${d.kind}</span><span class="search-title">${esc(d.title)}</span><span class="search-snip">${snippet(d.text, words)}</span></a></li>`).join("");
    status.textContent = !q ? "Search every lesson section and glossary term." : found.length ? `${found.length}${found.length === 25 ? "+" : ""} result${found.length === 1 ? "" : "s"}` : `No results for “${q}”. Try a property like gap or a term like specificity.`;
  }
  input.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(update, 80); });

  // Enter in the box opens the top result; the close button just closes.
  dialog.querySelector("form").addEventListener("submit", (e) => {
    if (e.submitter && e.submitter.value === "close") return;
    e.preventDefault();
    clearTimeout(timer);
    update();
    const first = list.querySelector("a");
    if (first) { dialog.close(); location.href = first.href; }
  });
  dialog.addEventListener("keydown", (e) => {
    if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
    const links = [...list.querySelectorAll("a")];
    if (!links.length) return;
    e.preventDefault();
    const i = links.indexOf(document.activeElement);
    if (e.key === "ArrowDown") links[Math.min(i + 1, links.length - 1)].focus();
    else if (i <= 0) input.focus();
    else links[i - 1].focus();
  });
  list.addEventListener("click", (e) => { if (e.target.closest("a")) dialog.close(); });
  dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });   // click on the backdrop

  window.Search = {
    open(prefill = "") {
      if (prefill) input.value = prefill;
      update();
      dialog.showModal();
      input.focus();
      input.select();
    },
    search,
  };
})();
