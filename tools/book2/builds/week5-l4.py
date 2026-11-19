import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("grid")
pg = src.between('  <section class="playground">\n    <div class="panel controls" aria-label="Grid container settings">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Grid", src.css(), """
  .gx-wrap { background: var(--stage); border-radius: 8px; padding: 12px; }
  .ie-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .ie-it { background: var(--item-1); color: #fff; border-radius: 6px; padding: 4px 8px; font: 700 0.85rem var(--font-code); font-variation-settings: "MONO" 1; overflow: hidden; }
  .ie-it.imp { background: transparent; color: var(--ink); border: 2px dashed var(--item-1); }
  .ie-it small { display: block; font-weight: 400; font-size: 0.75rem; }
  .lp-outer { display: grid; grid-template-columns: 22px 1fr; grid-template-rows: 22px auto; gap: 4px; }
  .lp-cols, .lp-grid { display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 8px; }
  .lp-rows { display: grid; grid-template-rows: repeat(3, 60px); row-gap: 8px; }
  .lp-grid { grid-template-rows: repeat(3, 60px); row-gap: 8px; }
  .lp-cols span, .lp-rows span { font: 700 0.75rem var(--font-code); font-variation-settings: "MONO" 1; color: var(--prop); display: flex; justify-content: space-between; }
  .lp-rows span { flex-direction: column; }
  .lp-cell { border: 1px dashed var(--line); border-radius: 4px; }
  .lp-item { background: var(--item-2); color: #fff; border-radius: 6px; display: grid; place-items: center; font: 700 0.85rem var(--font-code); font-variation-settings: "MONO" 1; opacity: 0.92; z-index: 1; }
  .ta-grid { display: grid; grid-template-columns: 110px 1fr 90px; gap: 8px; min-height: 230px; }
  .ta-grid > div { border-radius: 6px; color: #fff; padding: 8px; font: 700 0.85rem var(--font-code); font-variation-settings: "MONO" 1; display: grid; place-items: center; }
  .ta-h { background: var(--item-3); } .ta-n { background: var(--item-2); } .ta-m { background: var(--item-1); } .ta-a { background: var(--item-4); } .ta-f { background: var(--item-3); }
  textarea.ta-src { width: 100%; min-height: 96px; font: 0.85rem var(--font-code); font-variation-settings: "MONO" 1; padding: 8px; border: 1px solid var(--line); border-radius: 6px; background: var(--panel); color: var(--ink); resize: vertical; }
  .sg-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
  .sg-card { display: grid; grid-row: span 3; gap: 6px; align-content: start; background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 10px; }
  .sg-card.on { grid-template-rows: subgrid; }
  .sg-card h4 { margin: 0; font: 700 0.95rem var(--font-display); background: #eef1f8; padding: 4px 6px; border-radius: 4px; }
  .sg-card p { margin: 0; font-size: 0.85rem; }
  .sg-card span { align-self: end; justify-self: start; background: #2340d9; color: #fff; border-radius: 5px; padding: 4px 10px; font-size: 0.8rem; }
""")
b = top("Grid", "Grid controls rows and columns at the same time. Define the tracks on the container, and items fill the cells in order, or go exactly where you place them by line number or by name.", [
  "Define columns and rows with <code>fr</code>, <code>repeat()</code>, <code>gap</code> and <code>minmax()</code>.",
  "Explain the difference between the explicit and the implicit grid.",
  "Place items by line number, and by name with <code>grid-template-areas</code>.",
  "Line up nested content with <code>subgrid</code>.",
])
b += ST("Read", "What is grid layout?") + prose("""
    <p>A grid is a set of horizontal and vertical lines that make columns and rows. Designers have used them on paper for centuries, because they make a page look consistent: things line up from section to section.</p>
    <p>CSS <span class="term">Grid</span> lets you build that structure in the browser. Flexbox lines items up in one direction; Grid handles two at once. The rows and columns are called <strong>tracks</strong>, and the spaces between them are <strong>gutters</strong> (in CSS, <code>gap</code>).</p>""")
b += ST("Read", "Creating your grid in CSS") + prose("""
    <h3>Defining a grid</h3>
    <p><code>display: grid</code> on the container makes its direct children grid items, but on its own it just stacks them in one column. Add columns with <code>grid-template-columns</code>:</p>
    <pre class="snippet" data-lang="css">.container {
  display: grid;
  grid-template-columns: 200px 200px 200px;
}</pre>
    <h3>Flexible grids with the fr unit</h3>
    <p>Fixed pixel columns don't adapt to the screen. The <span class="term" data-term="fr (unit)">fr unit</span> means "a fraction of the available space", so <code>1fr 1fr 1fr</code> makes three equal columns at any width, and <code>2fr 1fr 1fr</code> makes the first twice as wide as the others. You can mix units: in <code>200px 1fr</code>, the 200px column is sized first and the <code>1fr</code> column takes what's left.</p>
    <h3>Gaps between tracks</h3>
    <p><code>column-gap</code> and <code>row-gap</code> add space between tracks, and the <span class="term">gap</span> shorthand sets both. Gaps can be lengths or percentages, but not <code>fr</code>.</p>
    <h3>Repeating track listings</h3>
    <p><code>repeat(3, 1fr)</code> is a shortcut for <code>1fr 1fr 1fr</code>. You can repeat a pattern too: <code>repeat(2, 2fr 1fr)</code> is <code>2fr 1fr 2fr 1fr</code>.</p>""")
b += ST("Play", "Build a grid", "Change the columns, gap and alignment, then make the first item span more cells.") + pg
b += prose("""
    <h3>Implicit and explicit grids</h3>
    <p>The tracks you define with <code>grid-template-columns</code> and <code>grid-template-rows</code> make the <strong>explicit grid</strong>. When there are more items than cells, the browser adds extra rows to hold them: that's the <strong>implicit grid</strong>. Implicit rows are sized <code>auto</code> (as tall as their content) unless you set <code>grid-auto-rows</code>:</p>
    <pre class="snippet" data-lang="css">.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 100px;   /* every implicit row is 100px */
}</pre>
    <h3>The minmax() function</h3>
    <p>A fixed row height has the same problem as any fixed height: content that needs more room overflows. <code>minmax(100px, auto)</code> means "at least 100px, but taller if the content needs it".</p>""")
b += ST("Play", "Explicit, implicit and minmax()", "Solid items sit in explicit rows; dashed ones are in rows the browser added. Turn on the long text and compare row sizes.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="ie-tr">grid-template-rows</label><select id="ie-tr"><option value="none">none</option><option selected>60px 60px</option></select></div>
      <div class="control"><label for="ie-ar">grid-auto-rows</label><select id="ie-ar"><option>auto</option><option selected>40px</option><option>minmax(40px, auto)</option></select></div>
      <div class="control"><label for="ie-n">number of items</label><input id="ie-n" type="range" min="3" max="12" value="9"><span class="readout" id="ie-n-out"></span></div>
      <label class="toggle"><input type="checkbox" id="ie-long"> long text in item 8</label>
    </div>
    <div class="stage-col">
      <div class="gx-wrap"><div class="ie-grid" id="ie-grid"></div></div>
      <p class="verdict" id="ie-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += prose("""
    <h3>As many columns as will fit</h3>
    <p>Put <code>repeat()</code> and <code>minmax()</code> together and you get the most useful line of Grid:</p>
    <pre class="snippet" data-lang="css">.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}</pre>
    <p>Read it as: "fit as many columns as you can, each at least 220px wide, and share any extra space equally." On a phone you get one column, on a laptop four, with no media queries. Pick the last option in the <strong>Build a grid</strong> playground above and resize your window to watch it.</p>""")
b += ST("Read", "Line-based placement") + prose("""
    <p>So far items have filled the cells in order. You can also place an item exactly, using the numbered <strong>lines</strong> between tracks. A grid with 4 columns has 5 column lines, numbered from 1 at the left (in English). Lines also count backwards from the end: <code>-1</code> is always the last line.</p>
    <pre class="snippet" data-lang="css">header {
  grid-column: 1 / -1;   /* from the first line to the last: full width */
  grid-row: 1;
}
article {
  grid-column: 2 / 4;    /* from line 2 to line 4: two columns */
}</pre>
    <p><code>grid-column</code> is shorthand for <code>grid-column-start</code> and <code>grid-column-end</code>; <code>grid-row</code> works the same way. Instead of an end line you can say how many tracks to cover: <code>grid-column: 2 / span 2</code>.</p>""")
b += ST("Play", "Place an item by line number", "Type a value for grid-column and grid-row, or pick a preset. The numbers show the lines.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="lp-c">grid-column</label><input class="src" id="lp-c" value="2 / 4" spellcheck="false"></div>
      <div class="control"><label for="lp-r">grid-row</label><input class="src" id="lp-r" value="1 / 3" spellcheck="false"></div>
      <div class="presets" id="lp-pre">
        <button class="btn" data-c="1 / -1" data-r="1">header</button>
        <button class="btn" data-c="1" data-r="2 / 4">sidebar</button>
        <button class="btn" data-c="2 / span 2" data-r="2">span 2</button>
        <button class="btn" data-c="-2 / -1" data-r="-2 / -1">last cell</button>
      </div>
    </div>
    <div class="stage-col">
      <div class="gx-wrap"><div class="lp-outer">
        <span></span>
        <div class="lp-cols"><span>1</span><span>2</span><span>3</span><span>4<b>5</b></span></div>
        <div class="lp-rows"><span>1</span><span>2</span><span>3<b>4</b></span></div>
        <div class="lp-grid" id="lp-grid"></div>
      </div></div>
      <p class="verdict" id="lp-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += ST("Practice", "Build a photo grid", "Three equal columns, with one featured photo that takes up four cells.") + '  <div id="ex-grid"></div>\n\n'
b += ST("Read", "Positioning with grid-template-areas") + prose("""
    <p>Another way to place items is to draw the layout with names. <code>grid-template-areas</code> takes one quoted string per row, with one name per column. Then each item says which area it goes in with <code>grid-area</code>:</p>
    <pre class="snippet" data-lang="css">.page {
  display: grid;
  grid-template-columns: 1fr 3fr;
  grid-template-areas:
    "header  header"
    "sidebar content"
    "footer  footer";
}
header { grid-area: header; }
aside  { grid-area: sidebar; }
main   { grid-area: content; }
footer { grid-area: footer; }</pre>
    <p>The rules are strict:</p>
    <ul>
      <li>Every row must have the same number of cells, and every cell must be filled.</li>
      <li>Repeat a name to make an area span cells. Use <code>.</code> for an empty cell.</li>
      <li>Each area must be a rectangle: no L-shapes, and no area in two separate places.</li>
    </ul>
    <p>If a rule is broken, the whole declaration is ignored.</p>""")
b += ST("Play", "Draw a layout with names", "Edit the strings, or try a preset. The column widths are 110px 1fr 90px.") + """  <section class="playground">
    <div class="panel controls">
      <label for="ta-src" class="eyebrow">grid-template-areas</label>
      <textarea class="ta-src" id="ta-src" spellcheck="false">"header header header"
"nav    main   aside"
"footer footer footer"</textarea>
      <div class="presets" id="ta-pre">
        <button class="btn" data-v='"header header header"\n"nav main aside"\n"footer footer footer"'>classic</button>
        <button class="btn" data-v='"nav header header"\n"nav main aside"\n"nav footer footer"'>tall nav</button>
        <button class="btn" data-v='"header header header"\n"main main aside"\n"footer . ."'>no nav</button>
        <button class="btn" data-v='"header header nav"\n"nav main aside"\n"footer footer footer"'>broken</button>
      </div>
    </div>
    <div class="stage-col">
      <div class="gx-wrap"><div class="ta-grid" id="ta-grid"><div class="ta-h" style="grid-area:header">header</div><div class="ta-n" style="grid-area:nav">nav</div><div class="ta-m" style="grid-area:main">main</div><div class="ta-a" style="grid-area:aside">aside</div><div class="ta-f" style="grid-area:footer">footer</div></div></div>
      <p class="verdict" id="ta-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += ST("Practice", "Lay out a page with named areas", "A header, a sidebar beside the main content, a footer, and a notice placed by line numbers.") + '  <div id="ex-areas"></div>\n\n'
b += ST("Read", "Nesting grids and subgrid") + prose("""
    <p>A grid item can be a grid container too, just like nested flex boxes. A card in a page grid might use its own grid to lay out its title, text and button.</p>
    <p>The catch is that a nested grid's tracks know nothing about its neighbours. If three cards sit side by side and one has a two-line title, its text starts lower than the others. <code>subgrid</code> fixes this: the nested grid uses its <em>parent's</em> tracks instead of making its own.</p>
    <pre class="snippet" data-lang="css">.card {
  display: grid;
  grid-row: span 3;              /* take three rows of the parent grid */
  grid-template-rows: subgrid;   /* and use those rows for title, text, button */
}</pre>""")
b += ST("Play", "Line up the cards with subgrid", "Each card has a title, some text and a button. Turn subgrid on and off.") + """  <section class="playground">
    <div class="panel controls">
      <label class="toggle"><input type="checkbox" id="sg-on"> use <code>subgrid</code> rows</label>
      <p class="hint" id="sg-out" aria-live="polite"></p>
    </div>
    <div class="gx-wrap"><div class="sg-grid" id="sg-grid">
      <div class="sg-card"><h4>Mesa Trail</h4><p>Rolling and shady.</p><span>Details</span></div>
      <div class="sg-card"><h4>Chautauqua to Royal Arch via Bluebell</h4><p>A steep climb to a sandstone arch, with over 200 stone steps at the end.</p><span>Details</span></div>
      <div class="sg-card"><h4>Bear Peak</h4><p>Big climb, bigger views.</p><span>Details</span></div>
    </div></div>
  </section>

"""
b += ST("Read", "Grid frameworks") + prose("""
    <p>Before CSS Grid, people used <em>grid frameworks</em>: libraries of classes that faked a grid, often with 12 or 16 columns. Grid makes most of them unnecessary. If you want a 12-column design grid, it's one line, and items are placed with line numbers:</p>
    <pre class="snippet" data-lang="css">.page { display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }
header { grid-column: 1 / -1; }   /* all 12 */
aside  { grid-column: 1 / 4; }    /* 3 columns */
main   { grid-column: 4 / -1; }   /* the other 9 */</pre>""")
b += notes([
  "<code>display: grid</code> and the track lists go on the container. <code>fr</code> shares out the available space; <code>repeat()</code> saves typing.",
  "Tracks you define are the explicit grid. Extra rows the browser adds are implicit, sized by <code>grid-auto-rows</code>.",
  "<code>minmax(100px, auto)</code> sets a minimum but lets the track grow. <code>repeat(auto-fit, minmax(220px, 1fr))</code> fits as many columns as there's room for.",
  "Place items by line number (<code>grid-column: 1 / -1</code>) or by name (<code>grid-template-areas</code> + <code>grid-area</code>).",
  "<code>subgrid</code> lets a nested grid share its parent's tracks, so content lines up across cards.",
], [
  "Setting <code>grid-template-columns</code> on the items instead of the container.",
  "A <code>grid-template-areas</code> layout with an uneven row or an L-shaped area, so the whole thing is ignored.",
  "Mixing up lines and tracks: <code>grid-column: 1 / 3</code> covers two columns, not three.",
  "Fixed <code>grid-auto-rows</code> heights that make text overflow. Use <code>minmax()</code>.",
])
first = src.first_script()
js = r'''
  // --- Explicit, implicit and minmax() ---
  function ieUpdate() {
    const tr = $("ie-tr").value, ar = $("ie-ar").value, n = +$("ie-n").value, long = $("ie-long").checked, g = $("ie-grid");
    $("ie-n-out").textContent = n;
    g.style.gridTemplateRows = tr; g.style.gridAutoRows = ar;
    const explicitRows = tr === "none" ? 0 : 2;
    g.innerHTML = Array.from({ length: n }, (_, i) => {
      const imp = Math.floor(i / 3) >= explicitRows;
      return `<div class="ie-it${imp ? " imp" : ""}">${i + 1} · ${imp ? "implicit" : "explicit"}${long && i === 7 ? "<small>This trail has a long description that needs several lines of space.</small>" : ""}</div>`;
    }).join("");
    requestAnimationFrame(() => {
      const rows = getComputedStyle(g).gridTemplateRows;
      let msg = `Row heights: ${rows}.`;
      const it8 = g.children[7];
      if (long && it8 && it8.scrollHeight > it8.clientHeight + 1) msg += " Item 8's text doesn't fit its 40px row. Try minmax(40px, auto).";
      else if (long && n >= 8 && ar.startsWith("minmax")) msg += " minmax() lets item 8's row grow to fit its text.";
      $("ie-out").className = "verdict" + (msg.includes("doesn't fit") ? " bad" : "");
      $("ie-out").textContent = msg;
    });
  }
  ["ie-tr", "ie-ar", "ie-n", "ie-long"].forEach((id) => $(id).addEventListener("input", ieUpdate));
  ieUpdate();

  // --- Line-based placement ---
  $("lp-grid").innerHTML = Array.from({ length: 12 }, (_, i) => `<div class="lp-cell" style="grid-column:${i % 4 + 1};grid-row:${Math.floor(i / 4) + 1}"></div>`).join("") + '<div class="lp-item" id="lp-item">item</div>';
  function lpUpdate() {
    const c = $("lp-c").value.trim(), r = $("lp-r").value.trim(), it = $("lp-item");
    const okC = CSS.supports("grid-column", c), okR = CSS.supports("grid-row", r);
    it.style.gridColumn = okC ? c : ""; it.style.gridRow = okR ? r : "";
    if (!okC || !okR) { $("lp-out").className = "verdict bad"; $("lp-out").textContent = `That isn't a valid ${!okC ? "grid-column" : "grid-row"} value. Try something like 2 / 4 or 1 / span 2.`; return; }
    const cs = getComputedStyle(it);
    $("lp-out").className = "verdict";
    $("lp-out").textContent = `grid-column: ${c}; grid-row: ${r};  →  columns from line ${cs.gridColumnStart} to ${cs.gridColumnEnd}, rows from line ${cs.gridRowStart} to ${cs.gridRowEnd}.`;
  }
  ["lp-c", "lp-r"].forEach((id) => $(id).addEventListener("input", lpUpdate));
  $("lp-pre").addEventListener("click", (e) => { const x = e.target.closest("button"); if (!x) return; $("lp-c").value = x.dataset.c; $("lp-r").value = x.dataset.r; lpUpdate(); });
  lpUpdate();

  // --- grid-template-areas ---
  function taUpdate() {
    const v = $("ta-src").value, g = $("ta-grid");
    g.style.gridTemplateAreas = ""; g.style.gridTemplateAreas = v.replace(/\s*\n\s*/g, " ");
    const ok = g.style.gridTemplateAreas !== "";
    const names = ok ? new Set(v.match(/[A-Za-z][\w-]*/g)) : new Set();
    const missing = ["header", "nav", "main", "aside", "footer"].filter((n) => !names.has(n));
    $("ta-out").className = "verdict " + (ok ? "ok" : "bad");
    $("ta-out").textContent = ok ? "Valid." + (missing.length ? ` No area is named ${missing.join(" or ")}, so ${missing.length > 1 ? "those items are" : "that item is"} placed automatically in an extra row.` : "")
      : "Invalid, so the browser ignores it and the items just fill the cells in order. Check that every row has 3 cells and every area is a rectangle.";
  }
  $("ta-src").addEventListener("input", taUpdate);
  $("ta-pre").addEventListener("click", (e) => { const x = e.target.closest("button"); if (!x) return; $("ta-src").value = x.dataset.v.replace(/\\n/g, "\n"); taUpdate(); });
  taUpdate();

  // --- subgrid ---
  function sgUpdate() {
    const on = $("sg-on").checked;
    document.querySelectorAll(".sg-card").forEach((c) => c.classList.toggle("on", on));
    $("sg-out").textContent = on ? "The cards share the parent's three rows, so every title, text and button lines up across the row." : "Each card lays out its own rows, so the long title pushes that card's text and button out of line with the others.";
  }
  $("sg-on").addEventListener("input", sgUpdate);
  sgUpdate();
'''
ex_g = src.block('  makeExercise(document.getElementById("ex-grid"), {')
ex_a = r'''  makeExercise(document.getElementById("ex-areas"), {
    title: "A page layout",
    task: `<ol>
      <li>Make <code>.page</code> a grid with two columns: <code>150px</code> and <code>1fr</code>, and a 10px gap.</li>
      <li>Use <code>grid-template-areas</code> so the header spans the top, the nav sits left of the main content, and the footer spans the bottom.</li>
      <li>Put each element in its area with <code>grid-area</code>.</li>
      <li>The notice has no area. Use line numbers to make it span the full width (it'll go in a new row at the bottom).</li>
    </ol>`,
    html: `<div class="page">
  <header>Boulder Trails</header>
  <nav>Trails<br>Maps<br>Gear</nav>
  <main>Royal Arch is a steep 1.7-mile climb to a sandstone arch.</main>
  <footer>© Trailhead club</footer>
  <p class="notice">The Mesa Trail is closed for repairs this week.</p>
</div>`,
    css: `body { font-family: system-ui, sans-serif; }
.page > * { margin: 0; padding: 10px; background: #eef1fb; }
header, footer { background: #1d2a3a; color: white; }
.notice { background: #ffe7a8; }`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.page {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 10px;
  grid-template-areas:
    "header header"
    "nav    main"
    "footer footer";
}
.page > * { margin: 0; padding: 10px; background: #eef1fb; }
header { grid-area: header; }
nav { grid-area: nav; }
main { grid-area: main; }
footer { grid-area: footer; }
header, footer { background: #1d2a3a; color: white; }
.notice { background: #ffe7a8; grid-column: 1 / -1; }` },
    hints: [
      "display: grid, grid-template-columns: 150px 1fr and gap: 10px all go on .page.",
      "One quoted string per row: \"header header\" \"nav main\" \"footer footer\". Repeat a name to span both columns.",
      "grid-column: 1 / -1 runs from the first line to the last.",
    ],
    checks: [
      { label: ".page is a grid with a 150px and a 1fr column", test: ({ $, style }) => { const c = style(".page", "grid-template-columns").split(" "); return style(".page", "display") === "grid" && c.length === 2 && c[0] === "150px" && Math.abs(parseFloat(c[1]) - ($(".page").clientWidth - 160)) < 1; } },
      { label: "The header and footer span the full width", test: ({ $ }) => { const p = $(".page").getBoundingClientRect().width; return ["header", "footer"].every((s) => Math.abs($(s).getBoundingClientRect().width - p) < 1); } },
      { label: "The nav is 150px wide, left of the main content", test: ({ $ }) => { const n = $("nav").getBoundingClientRect(), m = $("main").getBoundingClientRect(); return Math.abs(n.width - 150) < 1 && Math.abs(n.top - m.top) < 1 && n.right < m.left; } },
      { label: "The layout uses grid-template-areas", test: ({ style }) => style(".page", "grid-template-areas") !== "none" && style("main", "grid-row-start") !== "auto" },
      { label: "The notice spans the full width below the footer", test: ({ $ }) => { const n = $(".notice").getBoundingClientRect(), f = $("footer").getBoundingClientRect(); return Math.abs(n.width - $(".page").getBoundingClientRect().width) < 1 && n.top >= f.bottom; } },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "A grid has grid-template-rows: 100px and 6 items in 3 columns. How tall is the second row?", opts: ["100px", "auto, unless grid-auto-rows is set", "0"], a: 1, why: "The second row is implicit. Implicit rows are auto unless grid-auto-rows sizes them." },
    { id: "q6", q: "In a 4-column grid, what does grid-column: 1 / -1 do?", opts: ["Covers one column", "Spans from the first line to the last: the full width", "Nothing: negative numbers aren't allowed"], a: 1, why: "-1 is always the last line, so 1 / -1 spans every column." },
    { id: "q7", q: "Which grid-template-areas value is invalid?", opts: ['"a a" "b c"', '"a b" "a c"', '"a b" "c a"'], a: 2, why: "Area a would be in two separate cells. Every area must be one rectangle." },
    { id: "q8", q: "What does grid-template-rows: subgrid do on a nested grid?", opts: ["Uses its parent grid's row tracks", "Creates rows half the parent's height", "Removes all rows"], a: 0, why: "subgrid shares the parent's tracks, so content lines up across sibling items." },
  ]);
''')
write("core-grid.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_g + "\n" + ex_a + "</script>\n")
