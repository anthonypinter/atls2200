import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("display")
sw = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">.box (three of them)', '  <div class="section-title"><span class="eyebrow">Hiding things</span>')
hide = src.between('  <section class="playground even">\n    <div class="stage-col">\n      <div class="seg" id="hide"', '  <div class="section-title"><span class="eyebrow">Practice</span>')
extra = """
  .nf-stage { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 14px; font: 0.95rem/1.5 Georgia, serif; overflow: hidden; }
  .nf-wrap { border: 2px dashed #9aa2bf; padding: 8px; min-height: 160px; }
  .nf-wrap .k { background: #9ec2e6; border: 2px solid #2f5680; padding: 8px; margin: 4px; font: 600 0.85rem var(--font-code); font-variation-settings: "MONO" 1; }
  .nf-wrap .k:nth-child(2) { background: #f0b37a; border-color: #8a5228; }
  .nf-wrap .k:nth-child(3) { background: #b9d99a; border-color: #4b6b2f; }
  .nf-flow { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 6px 14px; font: 1rem/1.6 Georgia, serif; }
  .nf-flow > * { outline: 1px dashed #2f5680; outline-offset: 1px; }
  .nf-flow span, .nf-flow strong { outline-color: #b4410c; }
  .nf-flow h1 { font-size: 1.4rem; margin: 0.4em 0; }
  .nf-flow img { display: inline; vertical-align: middle; }
"""
h = head("Display and Normal Flow", src.css(), extra)
b = top("Display and Normal Flow", "Before you write any layout CSS, the browser already has a plan for where every box goes: normal flow. Understanding it, and the ways CSS can override it, is the foundation for every layout you'll build.", [
  "Describe normal flow: how block and inline boxes are placed by default.",
  "Change an element's box type with <code>display</code>, and see which properties it then obeys.",
  "Name the main ways CSS overrides normal flow: display, floats, positioning, flexbox and grid.",
  "Hide content with <code>display: none</code>, <code>visibility: hidden</code> or <code>opacity: 0</code>, and know the difference."])
b += ST("Read", "Normal layout flow") + prose("""
    <p><span class="term">Normal flow</span> is how the browser lays out a page when you haven't told it otherwise. It puts elements on the page in the same order as your HTML, one after another. Because of that, a well-structured HTML document is already readable before any layout CSS. Start from good HTML and change the flow only where you need to.</p>""")
b += ST("Read", "How are elements laid out by default?") + prose("""
    <p>Each element's content sits inside its padding, border and margin: the box model from the last lesson. Then:</p>
    <ul>
      <li><strong>Block boxes</strong> stack one below another, in the <em>block direction</em> (top to bottom for English). Each fills the width of its parent, and is as tall as its content. Their vertical margins collapse where they touch.</li>
      <li><strong>Inline boxes</strong> sit side by side in the <em>inline direction</em> (left to right for English), like words. When a line runs out of room, they wrap onto the next line.</li>
    </ul>""")
b += ST("Play", "Normal flow example", "Every block box has a blue dashed outline; inline boxes have orange ones. Change the width of the container.") + """  <div class="panel" style="display:grid;gap:10px">
    <div class="control"><label for="nf-w">body width</label><input id="nf-w" type="range" min="240" max="640" step="20" value="480"><span class="readout" id="nf-w-out"></span></div>
    <div class="nf-flow" id="nf-flow">
      <h1>Basic document flow</h1>
      <p>I am a basic block level element. My adjacent block level elements sit on new lines below me.</p>
      <p>By default we span 100% of the width of our parent element, and we are as tall as our child content. Our total width and height is our content + padding + border width/height.</p>
      <p>Inline elements <span>like this one</span> and <strong>this one</strong> sit on the same line as each other and adjacent text nodes, if there is space on the same line. Overflowing inline elements <span>wrap onto a new line if possible, like this one containing text</span>.</p>
    </div>
  </div>

"""
b += prose("""
    <p>The <code>display</code> property changes which kind of box an element generates: <code>block</code>, <code>inline</code>, or <code>inline-block</code> (inline in the flow, but sized like a block). That decides which properties it listens to.</p>""")
b += ST("Play", "Switch the display type", "Change display on three boxes, then give them a width, height, margin and padding to see which ones listen.") + sw
b += ST("Read", "Overriding normal flow") + prose("""
    <p>Normal flow can't put things side by side in columns, or pin a header to the top of the screen. For that, CSS has several layout tools, each covered in a later week:</p>
    <ul>
      <li><strong>The <code>display</code> property</strong>: besides block and inline, <code>display: flex</code> and <code>display: grid</code> switch on whole layout systems for an element's children.</li>
      <li><strong><span class="term" data-term="Float">Floats</span></strong>: <code>float: left</code> moves a box to one side and lets text wrap around it, like an image in a magazine.</li>
      <li><strong><span class="term" data-term="position">Positioning</span></strong>: <code>position</code> moves a box from where normal flow put it, or pins it to the screen.</li>
      <li><strong><span class="term">Flexbox</span></strong> (Week 5): lays items out in one direction, a row or a column, and shares space between them.</li>
      <li><strong><span class="term">Grid</span></strong> (Week 5): lays items out in rows and columns at once.</li>
      <li><strong><span class="term">Responsive design</span></strong> (Week 6): changes the layout to suit the screen size.</li>
    </ul>
    <h3>Other layout techniques</h3>
    <p>Two more exist but are less common: <strong>table layout</strong> (<code>display: table</code>, from before flexbox existed) and <strong>multi-column layout</strong> (<code>column-count: 3</code>), which flows text into columns like a newspaper.</p>""")
b += ST("Play", "Same HTML, different layouts", "Three boxes in one container. Each button applies a different layout tool to the same HTML.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="presets" id="nf-lay" role="group" aria-label="Layout"></div>
      <pre class="snippet" id="nf-code"></pre>
      <p class="verdict" id="nf-note" aria-live="polite"></p>
    </div>
    <div class="nf-stage"><div class="nf-wrap" id="nf-wrap"><div class="k">Box 1: some text that runs a little longer</div><div class="k">Box 2</div><div class="k">Box 3</div><span style="font-size:0.85rem">Trailing text in the container, flowing after the boxes. It shows how other content reacts to each layout.</span></div></div>
  </section>

"""
b += ST("Read", "Hiding things") + prose("""
    <p><code>display: none</code> is the most drastic display value: the element isn't drawn at all, and normal flow closes up the space it would have taken. Two other properties hide elements but keep their place in the flow.</p>""")
b += ST("Play", "display: none vs visibility: hidden vs opacity: 0", "All three make card 2 invisible. Watch what happens to the space it took up.") + hide
b += ST("Practice", "Change how boxes flow", "Three elements, three different display values.") + '  <div id="ex-display"></div>\n\n'
b += ST("Practice", "A first layout", "Use one display value to put the cards side by side.") + '  <div id="ex-layout"></div>\n\n'
b += notes([
  "Normal flow places elements in source order: blocks stack, inline boxes sit side by side and wrap.",
  "Good HTML in normal flow is already readable; layout CSS changes it only where needed.",
  "<code>display</code> chooses block, inline or inline-block, and switches on flex and grid.",
  "Floats, positioning, flexbox and grid all override normal flow in different ways.",
  "<code>display: none</code> removes the box; <code>visibility: hidden</code> and <code>opacity: 0</code> keep its space.",
], [
  "Setting <code>width</code> on an inline element and wondering why it's ignored.",
  "Reaching for floats or positioning to build a whole layout: use flexbox or grid.",
  "Changing the visual order so it no longer matches the HTML order, confusing keyboard and screen reader users.",
  "Hiding with <code>opacity: 0</code> when you meant to remove: it's still clickable and still read aloud.",
])
first = src.first_script()
js = r'''
  // --- Normal flow example ---
  function nfw() { const w = $("nf-w").value; $("nf-flow").style.width = w + "px"; $("nf-flow").style.maxWidth = "100%"; $("nf-w-out").textContent = w + "px"; }
  $("nf-w").addEventListener("input", nfw);
  nfw();

  // --- Same HTML, different layouts ---
  const LAY = {
    "normal flow": ["", "", "Blocks stack in source order, each filling the width. The text flows after them."],
    "display: flex": [".wrap { display: flex; }", "display:flex", "The boxes sit in a row and share the width. (The text becomes a fourth flex item.)"],
    "display: grid": [".wrap {\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n}", "display:grid;grid-template-columns:1fr 1fr", "Two equal columns: the items fill the grid cells in order, row by row."],
    "float: left": [".k { float: left; width: 30%; }", "", "Each box floats to the left as far as it can; the text wraps around them."],
    "position": [".k:nth-child(2) {\n  position: relative;\n  left: 60px;\n  top: 20px;\n}", "", "Box 2 is nudged from where normal flow put it. Its old space stays reserved; it can overlap other boxes."],
    "columns": [".wrap { column-count: 2; }", "column-count:2", "Multi-column layout flows the content into two columns, like a newspaper."],
  };
  $("nf-lay").innerHTML = Object.keys(LAY).map((k) => `<button class="btn" type="button">${k}</button>`).join("");
  function lay(k) {
    const [code, wrapCss, note] = LAY[k];
    const wrap = $("nf-wrap"), boxes = wrap.querySelectorAll(".k");
    wrap.style.cssText = wrapCss;
    boxes.forEach((bx, i) => { bx.style.cssText = k === "float: left" ? "float:left;width:30%" : k === "position" && i === 1 ? "position:relative;left:60px;top:20px" : ""; });
    $("nf-code").textContent = code || "/* no layout CSS */";
    $("nf-note").textContent = note;
    document.querySelectorAll("#nf-lay .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.textContent === k)));
  }
  $("nf-lay").addEventListener("click", (e) => { const b = e.target.closest(".btn"); if (b) lay(b.textContent); });
  lay("normal flow");
'''
ex_disp = src.block('  makeExercise(document.getElementById("ex-display"), {')
ex_lay = r'''  makeExercise(document.getElementById("ex-layout"), {
    title: "Cards in a row",
    task: `<ol>
      <li>Give <code>.cards</code> <code>display: flex</code> so the three cards sit side by side.</li>
      <li>Add <code>gap: 12px</code> to <code>.cards</code> for space between them.</li>
    </ol>
    <p>Notice the HTML doesn't change at all: the order is still the order you'd read them in.</p>`,
    html: `<div class="cards">
  <div class="card">Mesa Trail</div>
  <div class="card">Royal Arch</div>
  <div class="card">Bear Peak</div>
</div>`,
    css: `body { font-family: system-ui, sans-serif; }
.card { padding: 16px; background: #eef1fb; border: 2px solid #2340d9; }`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.card { padding: 16px; background: #eef1fb; border: 2px solid #2340d9; }
.cards {
  display: flex;
  gap: 12px;
}` },
    hints: ["display goes on the container (.cards), not the cards."],
    checks: [
      { label: ".cards is a flex container", test: ({ style }) => style(".cards", "display") === "flex" },
      { label: "The three cards share one row", test: ({ $$ }) => new Set($$(".card").map((c) => Math.round(c.getBoundingClientRect().top))).size === 1 },
      { label: "There's a 12px gap", test: ({ $$ }) => { const [a, b] = $$(".card").map((c) => c.getBoundingClientRect()); return Math.abs(b.left - a.right - 12) < 0.5; } },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "In normal flow, in what order are elements placed?", opts: ["The order they appear in the HTML", "Largest first", "Alphabetical by tag"], a: 0, why: "Normal flow follows source order." },
    { id: "q6", q: "Which tool lets text wrap around a box, like an image in a magazine?", opts: ["float", "position", "display: grid"], a: 0, why: "Floats take a box out to one side and let content wrap around it." },
  ]);
''')
write("core-display-flow.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_disp + "\n" + ex_lay + "\n" + quiz + "</script>\n")
