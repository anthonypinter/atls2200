import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("flex-vs-grid")
duel = src.between('  <div class="panel" style="display:grid;gap:12px">\n    <div class="scen"', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Flexbox or Grid?", src.css(), """
  .so-list { display: grid; gap: 8px; }
  .so-row { display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: center; padding: 8px 10px; border: 1px solid var(--line); border-radius: 8px; background: var(--panel); }
  .so-row p { margin: 0; }
  .so-row .seg .btn[aria-pressed="true"] { outline: 2px solid var(--cobalt); }
  .so-row .fb { grid-column: 1 / -1; font-size: 0.9rem; margin: 0; }
  .so-row .fb.ok { color: var(--good); } .so-row .fb.bad { color: var(--bad); }
  @media (max-width: 560px) { .so-row { grid-template-columns: 1fr; } }
""")
b = top("Flexbox or Grid?", "Both can build most layouts, but each has a sweet spot. Flexbox arranges items along one line and lets their content decide their size. Grid lays out rows and columns together. Real pages use both, often one inside the other.", [
  "Explain the difference between one-dimensional and two-dimensional layout.",
  "Choose Flexbox or Grid for a given layout, and say why.",
  "Combine the two, with flex containers inside grid items.",
])
b += ST("Read", "One dimension or two?") + prose("""
    <p>You can build most layouts with either <span class="term">Flexbox</span> or <span class="term">Grid</span>, which is why people argue about which is better. They're not competitors. Each has a sweet spot.</p>
    <p>The key difference is dimensions. Flexbox is <strong>one-dimensional</strong>: it arranges items along a single row or column. When flex items wrap onto a second line, that line is laid out on its own, so items in different lines don't line up with each other. Grid is <strong>two-dimensional</strong>: you define columns and rows, and items line up in both directions at once.</p>
    <p>The classic sign you picked wrong is a card gallery built with Flexbox: the last row has two cards, and they stretch to fill the whole width. With Grid, they keep the same width as the cards above.</p>""")
b += ST("Read", "Content out, or layout in?") + prose("""
    <p>A second way to decide is to ask where the sizes come from.</p>
    <ul>
      <li><strong>Content out:</strong> the items' own sizes should decide the layout. A row of buttons, a logo next to a nav, tags that wrap like words. That's <strong>Flexbox</strong>.</li>
      <li><strong>Layout in:</strong> you draw the rows and columns first and place content into them. A card gallery, a page with a sidebar, a photo layout where one item spans several cells. That's <strong>Grid</strong>.</li>
    </ul>
    <p>A few things only one of them can do. Only Grid can make an item span several rows, and only Grid keeps columns lined up across wrapped rows. Flexbox is simpler for a single row whose items are different sizes, and for pushing one item to the end with <code>margin-left: auto</code>.</p>
    <div class="callout tip"><p class="callout-title">Tip</p><p>Ask yourself: "Do I care about columns lining up?" If yes, use Grid. If you just need things in a row, spaced nicely, use Flexbox.</p></div>""")
b += ST("Play", "Compare the same layout", "Pick a layout and see it built both ways. Change the container width to see where each one struggles.") + duel
b += ST("Practice", "Sort the layouts", "For each layout, pick the tool that fits best.") + """  <div class="so-list" id="so-list"></div>
  <p class="verdict" id="so-score" aria-live="polite"></p>

"""
b += ST("Read", "Using them together") + prose("""
    <p>Most real pages use both. A common pattern: Grid for the overall structure (the page, a gallery of cards), and Flexbox inside each piece (the card's header, its row of buttons).</p>
    <pre class="snippet" data-lang="css">.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}
.card {
  display: flex;
  flex-direction: column;
}
.card .btn {
  margin-top: auto;   /* push the button to the bottom of the card */
}</pre>
    <p>Grid makes every card in a row the same height. Inside each card, a flex column with <code>margin-top: auto</code> on the button pushes the button to the bottom, so the buttons line up even when the text above them is different lengths.</p>""")
b += ST("Practice", "Grid outside, flex inside", "The cards are already a grid. Lay out each card with Flexbox.") + '  <div id="ex-nest"></div>\n\n'
b += ST("Practice", "Pick the right tool", "This page uses Flexbox for everything. One part should be Grid.") + '  <div id="ex-choose"></div>\n\n'
b += notes([
  "Flexbox is one-dimensional: a row <em>or</em> a column. Wrapped lines don't line up with each other.",
  "Grid is two-dimensional: columns line up from row to row.",
  "Content out (sizes from the items) → Flexbox. Layout in (tracks first, then content) → Grid.",
  "Only Grid can make one item span several rows and columns.",
  "It's normal to put a flex container inside a grid item, or a grid inside a flex item.",
], [
  "Building a card gallery with Flexbox and getting a stretched last row.",
  "Adding lots of wrapper divs to fake a two-dimensional layout with Flexbox.",
  "Using Grid for a simple row of buttons and fighting fixed column widths.",
  "Thinking one is \"better.\" They solve different problems.",
])
first = src.first_script()
js = r'''
  // --- Sort the layouts ---
  const SO = [
    ["A site header: logo on the left, four nav links on the right", "flex", "One row of items sized by their content."],
    ["A gallery of 20 product cards in equal columns", "grid", "The columns should line up from row to row, including the last row."],
    ["Tags under a blog post that wrap like words", "flex", "Each tag should be as wide as its text."],
    ["A page with a header, sidebar, main content and footer", "grid", "Rows and columns at once: grid-template-areas draws it in one place."],
    ["Three buttons at the bottom of a dialog, pushed to the right", "flex", "A single row; justify-content: flex-end does it."],
    ["A photo layout where one photo covers two rows and two columns", "grid", "Only Grid can span rows as well as columns."],
    ["An icon next to a line of text, centered vertically", "flex", "Two items in a row with align-items: center."],
    ["A calendar month: 7 columns, 5 or 6 rows", "grid", "A true grid: repeat(7, 1fr) with rows that line up."],
  ];
  const soAns = {};
  $("so-list").innerHTML = SO.map(([q], i) => `<div class="so-row"><p>${q}</p><div class="seg" role="group" aria-label="Tool for: ${q}"><button class="btn" data-i="${i}" data-v="flex" aria-pressed="false">Flexbox</button><button class="btn" data-i="${i}" data-v="grid" aria-pressed="false">Grid</button></div><p class="fb" id="so-fb${i}"></p></div>`).join("");
  $("so-list").addEventListener("click", (e) => {
    const x = e.target.closest("button[data-v]"); if (!x) return;
    const i = +x.dataset.i, [, right, why] = SO[i], ok = x.dataset.v === right;
    soAns[i] = ok;
    x.parentElement.querySelectorAll("button").forEach((y) => y.setAttribute("aria-pressed", String(y === x)));
    const fb = $("so-fb" + i); fb.className = "fb " + (ok ? "ok" : "bad");
    fb.textContent = (ok ? "Yes. " : `Better with ${right === "flex" ? "Flexbox" : "Grid"}. `) + why;
    const done = Object.keys(soAns).length, score = Object.values(soAns).filter(Boolean).length;
    $("so-score").textContent = `${score} of ${done} right` + (done === SO.length ? (score === SO.length ? ". All eight!" : ". Try the ones you missed again.") : ".");
  });
'''
ex_c = src.block('  makeExercise(document.getElementById("ex-choose"), {')
ex_n = r'''  makeExercise(document.getElementById("ex-nest"), {
    title: "Cards with aligned buttons",
    task: `<ol>
      <li>Make each <code>.card</code> a flex container that stacks its children in a column.</li>
      <li>Push each card's <code>.btn</code> to the bottom of the card, so the buttons line up across the row.</li>
      <li>Make each <code>.card-head</code> a flex row with its icon and title centered vertically, 8px apart.</li>
    </ol>`,
    html: `<div class="cards">
  <article class="card">
    <div class="card-head"><span class="icon">⛰</span><h3>Mesa</h3></div>
    <p>Rolling and shady.</p>
    <a class="btn" href="#">Details</a>
  </article>
  <article class="card">
    <div class="card-head"><span class="icon">⛰</span><h3>Royal Arch</h3></div>
    <p>A steep climb through ponderosa pine to a sandstone arch, with over 200 stone steps at the end.</p>
    <a class="btn" href="#">Details</a>
  </article>
  <article class="card">
    <div class="card-head"><span class="icon">⛰</span><h3>Bear Peak</h3></div>
    <p>Big climb, bigger views.</p>
    <a class="btn" href="#">Details</a>
  </article>
</div>`,
    css: `body { font-family: system-ui, sans-serif; }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.card { padding: 10px; background: #eef1fb; border-radius: 8px; }
.card h3 { margin: 0; font-size: 1rem; }
.icon { font-size: 1.6rem; }
.btn { align-self: flex-start; background: #2340d9; color: white; padding: 6px 12px; border-radius: 6px; text-decoration: none; }`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.card { padding: 10px; background: #eef1fb; border-radius: 8px; display: flex; flex-direction: column; }
.card-head { display: flex; align-items: center; gap: 8px; }
.card h3 { margin: 0; font-size: 1rem; }
.icon { font-size: 1.6rem; }
.btn { align-self: flex-start; margin-top: auto; background: #2340d9; color: white; padding: 6px 12px; border-radius: 6px; text-decoration: none; }` },
    hints: [
      "display: flex; flex-direction: column; on .card.",
      "In a flex column, margin-top: auto on the button takes up all the spare space above it.",
      "display: flex; align-items: center; gap: 8px; on .card-head.",
    ],
    checks: [
      { label: "Each card is a flex column", test: ({ style }) => style(".card", "display") === "flex" && style(".card", "flex-direction") === "column" },
      { label: "The buttons line up at the bottom of the cards", test: ({ $$ }) => { const b = $$(".btn").map((x) => x.getBoundingClientRect().bottom), c = $$(".card").map((x) => x.getBoundingClientRect().bottom); return Math.max(...b) - Math.min(...b) < 1 && b.every((y, i) => Math.abs(c[i] - 10 - y) < 1); } },
      { label: "Each card head is a flex row", test: ({ style }) => style(".card-head", "display") === "flex" && style(".card-head", "flex-direction") === "row" },
      { label: "Icon and title are centered vertically, 8px apart", test: ({ $ }) => { const i = $(".icon").getBoundingClientRect(), t = $(".card h3").getBoundingClientRect(); return Math.abs((i.top + i.bottom) / 2 - (t.top + t.bottom) / 2) < 1.5 && Math.abs(t.left - i.right - 8) < 1; } },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "\\"Content out\\" means the items' sizes decide the layout. Which tool fits that?", opts: ["Flexbox", "Grid", "Floats"], a: 0, why: "Flexbox sizes items from their content. Grid is layout in: tracks first." },
    { id: "q6", q: "In a flex column card, how do you push the button to the bottom?", opts: ["margin-top: auto on the button", "align-items: end on the card", "position: absolute on the card"], a: 0, why: "An auto margin in a flex container takes up all the spare space on that side." },
  ]);
''')
write("core-flex-or-grid.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_n + "\n" + ex_c + "</script>\n")
