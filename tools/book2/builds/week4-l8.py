import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("form-styling")
fpg = src.between('  <section class="playground even">\n    <div class="stage-col">\n      <div class="steps" id="steps"', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Styling Lists, Tables and Forms", src.css(), """
  .ls-stage { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 14px 18px; font: 1rem/1.5 Georgia, serif; }
  .ls-stage ul, .ls-stage ol { margin: 0 0 10px; border-left: 2px dashed #9aa2bf; }
  .ls-stage li { background: #eef1fb; margin: 2px 0; }
  .tb-wrap { overflow-x: auto; background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 12px; }
  #tb-t { color: #1d2133; }
  #tb-t.font { font-family: system-ui, sans-serif; }
  #tb-t.space { table-layout: fixed; width: 100%; border-collapse: collapse; }
  #tb-t.space th, #tb-t.space td { padding: 0.6em; }
  #tb-t.align th, #tb-t.align td { text-align: left; vertical-align: top; }
  #tb-t.align td:nth-child(2), #tb-t.align th:nth-child(2) { text-align: right; }
  #tb-t.borders thead th { border-bottom: 2px solid #1d2133; }
  #tb-t.borders tfoot td, #tb-t.borders tfoot th { border-top: 1px solid #999; }
  #tb-t.zebra tbody tr:nth-child(odd) { background-color: #eef1fb; }
  #tb-t.cap caption { caption-side: bottom; padding: 8px; font-style: italic; color: #5a6280; text-align: right; }
  .of-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; }
  .of-box { height: 150px; border: 2px dashed #9aa2bf; border-radius: 6px; background: #fff; overflow: hidden; }
  .of-box img { width: 100%; height: 100%; display: block; }
  .of-row figcaption { font: 0.82rem var(--font-code); font-variation-settings: "MONO" 1; color: var(--muted); margin-top: 4px; }
""")
b = top("Styling Lists, Tables and Forms", "Lists, tables, images and form controls each come with their own default styling quirks. This lesson tames them: custom bullets, readable tables, images that fit their boxes, and forms that match the rest of the page.", [
  "Style list markers, spacing and counting.",
  "Make a data table readable with spacing, alignment, borders and zebra stripes.",
  "Fit images into boxes with <code>max-width</code> and <code>object-fit</code>.",
  "Normalise form controls so they inherit fonts and size predictably, then style them."])
# --- Lists
b += ST("Read", "Styling lists") + prose("""
    <h3>Handling list spacing</h3>
    <p>Browsers give lists a top and bottom margin and about 40px of left padding, which is where the bullets sit. Set the spacing yourself so lists line up with your paragraphs: matching <code>line-height</code> and margins on <code>p</code> and <code>li</code> keeps the rhythm even.</p>
    <h3>List-specific styles</h3>
    <ul>
      <li><code>list-style-type</code>: the bullet or numbering style: <code>disc</code>, <code>circle</code>, <code>square</code>, <code>decimal</code>, <code>lower-alpha</code>, <code>upper-roman</code>, <code>none</code>, or any string like <code>"→ "</code>.</li>
      <li><code>list-style-position</code>: <code>outside</code> (the default; the marker hangs in the padding) or <code>inside</code> (the marker sits in the text, which wraps under it).</li>
      <li><code>list-style-image</code>: an image as the bullet. You can't size it, so many people use <code>::marker</code> or a background image instead.</li>
      <li><code>list-style</code>: the shorthand, as in <code>list-style: square inside;</code>.</li>
    </ul>
    <h3>Controlling list counting</h3>
    <p>In the HTML, <code>&lt;ol start="4"&gt;</code> starts counting at 4, <code>reversed</code> counts down, and <code>&lt;li value="2"&gt;</code> sets one item's number.</p>""")
b += ST("Play", "List styles", "Change the marker type and position. Watch where the marker sits relative to the dashed edge of the list.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="control"><label for="ls-type">ul list-style-type</label><select id="ls-type"><option>disc</option><option>circle</option><option>square</option><option value='"→ "'>"→ "</option><option>none</option></select></div>
      <div class="control"><label for="ls-otype">ol list-style-type</label><select id="ls-otype"><option>decimal</option><option>lower-alpha</option><option>upper-roman</option><option>decimal-leading-zero</option></select></div>
      <div class="control"><label for="ls-pos">list-style-position</label><select id="ls-pos"><option>outside</option><option>inside</option></select></div>
      <div class="control"><label for="ls-pad">padding-left</label><input id="ls-pad" type="range" min="0" max="60" step="4" value="40"><span class="readout" id="ls-pad-out"></span></div>
      <pre class="snippet" id="ls-code"></pre>
    </div>
    <div class="ls-stage" id="ls-stage"><ul><li>Water, at least two litres, plus a filter if you're heading somewhere remote</li><li>Layers</li></ul><ol start="1"><li>Park at Chautauqua</li><li>Follow the Bluebell Road</li><li>Turn left at the sign</li></ol></div>
  </section>

"""
b += ST("Practice", "Styling a nested list", "Different markers for each kind of list.") + '  <div id="ex-list"></div>\n\n'
# --- Tables
b += ST("Read", "Styling tables") + prose("""
    <p>A well-structured table (Week 2) is the starting point. Then a handful of rules makes it readable:</p>
    <ul>
      <li><strong>Font:</strong> a clean sans-serif is easiest to scan.</li>
      <li><strong>Spacing:</strong> <code>border-collapse: collapse</code> merges double borders; <code>padding</code> on cells gives the data room; <code>table-layout: fixed</code> with a <code>width</code> makes column widths predictable.</li>
      <li><strong>Alignment:</strong> left-align text, right-align numbers so their digits line up, and <code>vertical-align: top</code> for cells of different heights. <code>:nth-child()</code> picks the column.</li>
      <li><strong>Borders:</strong> a few lines, like one under the header and one above the totals, beat a grid of boxes.</li>
      <li><strong>Zebra striping:</strong> <code>tbody tr:nth-child(odd)</code> shades alternate rows, so eyes don't slip to the wrong row.</li>
      <li><strong>Caption:</strong> <code>caption-side: bottom</code> moves it under the table.</li>
    </ul>""")
b += ST("Play", "Style the table one step at a time", "Turn on each step.") + """  <section class="playground">
    <div class="panel controls" id="tb-steps" style="display:grid;gap:8px;align-content:start">
      <label class="toggle"><input type="checkbox" data-c="font"> Font</label>
      <label class="toggle"><input type="checkbox" data-c="space"> Spacing: fixed layout, collapse, padding</label>
      <label class="toggle"><input type="checkbox" data-c="align"> Alignment: numbers right</label>
      <label class="toggle"><input type="checkbox" data-c="borders"> Borders: header and footer only</label>
      <label class="toggle"><input type="checkbox" data-c="zebra"> Zebra stripes</label>
      <label class="toggle"><input type="checkbox" data-c="cap"> Caption at the bottom</label>
      <button class="btn" type="button" id="tb-all" style="justify-self:start">Turn everything on</button>
    </div>
    <div class="tb-wrap"><table id="tb-t"><caption>Boulder trails, by visits</caption>
      <thead><tr><th scope="col">Trail</th><th scope="col">Visits (2025)</th><th scope="col">Notes</th></tr></thead>
      <tbody><tr><th scope="row">Mesa Trail</th><td>48,200</td><td>Busy on weekends</td></tr><tr><th scope="row">Royal Arch</th><td>30,950</td><td>Steep; closed after storms</td></tr><tr><th scope="row">Bear Peak</th><td>12,400</td><td>Long day</td></tr><tr><th scope="row">Sanitas</th><td>27,800</td><td>Dog friendly</td></tr></tbody>
      <tfoot><tr><th scope="row">Total</th><td>119,350</td><td></td></tr></tfoot>
    </table></div>
  </section>

"""
b += ST("Practice", "A readable data table", "Apply the table-styling basics.") + '  <div id="ex-table"></div>\n\n'
# --- Images and media
b += ST("Read", "Images and media") + prose("""
    <h3>Replaced elements</h3>
    <p>Images and videos are <em>replaced elements</em>: their content comes from an outside file, and CSS can't change what's inside them, only the box they sit in.</p>
    <h3>Sizing images</h3>
    <p>An image is shown at its natural size, so a large photo overflows its container. One rule stops that everywhere:</p>
    <pre class="snippet" data-lang="css">img {
  max-width: 100%;
  height: auto;
}</pre>
    <h3>Handling image display issues with object-fit</h3>
    <p>When you force an image into a box of a different shape, it stretches. <span class="term">object-fit</span> controls how it fills the box instead: <code>cover</code> fills it and crops; <code>contain</code> fits the whole image and leaves gaps; <code>fill</code> (the default) stretches.</p>
    <h3>Replaced elements in layout</h3>
    <p>In layouts like Grid, items normally stretch to fill their area, but images keep their own proportions. Give the image <code>width: 100%; height: 100%; object-fit: cover;</code> if you want it to fill its cell.</p>""")
b += ST("Look", "object-fit", "The same wide image in three square boxes.") + """  <div class="of-row" id="of-row"></div>

"""
b += ST("Practice", "Thumbnails that fit", "Make three images of different shapes into tidy square thumbnails.") + '  <div id="ex-thumbs"></div>\n\n'
# --- Forms
b += ST("Read", "Styling form elements") + prose("""
    <h3>Challenges in styling form widgets</h3>
    <p>Form controls started out drawn by the operating system, not the browser, and some still are. They fall into three groups:</p>
    <ul>
      <li><strong>Easy to style:</strong> text inputs, <code>&lt;textarea&gt;</code>, <code>&lt;button&gt;</code>, <code>&lt;fieldset&gt;</code> and <code>&lt;legend&gt;</code> behave like ordinary boxes.</li>
      <li><strong>Harder:</strong> checkboxes and radio buttons. <code>accent-color</code> recolours them in one line.</li>
      <li><strong>Mostly unstylable inside:</strong> colour and date pickers, range sliders, file inputs, <code>&lt;select&gt;</code> dropdowns, <code>&lt;progress&gt;</code> and <code>&lt;meter&gt;</code>. You can size the box, but not much of what's inside.</li>
    </ul>
    <h3>Normalising form behaviour: a reset</h3>
    <p>Form controls don't inherit the page's font, and their sizing differs between browsers. A short reset fixes both:</p>
    <pre class="snippet" data-lang="css">button, input, select, textarea {
  font-family: inherit;
  font-size: 100%;
  box-sizing: border-box;
}
textarea {
  overflow: auto;
}</pre>
    <h3>Styling text inputs</h3>
    <p>Then style them like any box: <code>border</code>, <code>padding</code>, <code>border-radius</code>. Put each label above its input, make the input full width, and give <code>:focus-visible</code> a clear outline. Keep controls recognisable: an input that doesn't look like an input won't get filled in.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p>Don't show errors with colour alone. Some visitors can't tell red from green. Add a text message next to the field explaining what's wrong.</p></div>""")
b += ST("Play", "Improve the form one layer at a time", "Step through the layers and watch the same form get easier to use. Try the fields at each step.") + fpg
b += ST("Practice", "Style the form", "Fix the fonts, the overflow and the missing focus style.") + '  <div id="ex-formstyle"></div>\n\n'
b += notes([
  "<code>list-style-type</code>, <code>-position</code> and <code>-image</code> (or <code>::marker</code>) style list markers.",
  "Tables: collapse borders, pad cells, right-align numbers, stripe rows with <code>:nth-child(odd)</code>.",
  "<code>img { max-width: 100%; height: auto; }</code> stops images overflowing.",
  "<code>object-fit: cover</code> fills a box without stretching the image.",
  "Form controls need <code>font: inherit</code> and <code>box-sizing: border-box</code> to match the page.",
], [
  "Removing list padding with markers <code>outside</code>, so the bullets disappear off the edge.",
  "Centring numbers in a table, so digits don't line up.",
  "Setting a width and height on an image without <code>object-fit</code>, so it stretches.",
  "Restyling form controls until they no longer look like form controls.",
  "Removing the focus outline from inputs.",
])
first = src.first_script()
js = r'''
  // --- Lists ---
  function ls() {
    const t = $("ls-type").value, o = $("ls-otype").value, p = $("ls-pos").value, pad = $("ls-pad").value;
    const ul = $("ls-stage").querySelector("ul"), ol = $("ls-stage").querySelector("ol");
    ul.style.listStyleType = t; ol.style.listStyleType = o;
    [ul, ol].forEach((l) => { l.style.listStylePosition = p; l.style.paddingLeft = pad + "px"; });
    $("ls-pad-out").textContent = pad + "px";
    $("ls-code").textContent = `ul { list-style-type: ${t}; }\nol { list-style-type: ${o}; }\nul, ol {\n  list-style-position: ${p};\n  padding-left: ${pad}px;\n}`;
  }
  ["ls-type", "ls-otype", "ls-pos", "ls-pad"].forEach((id) => $(id).addEventListener("input", ls));
  ls();

  // --- Tables ---
  function tb() { $("tb-t").className = [...document.querySelectorAll("#tb-steps input:checked")].map((i) => i.dataset.c).join(" "); }
  $("tb-steps").addEventListener("change", tb);
  $("tb-all").addEventListener("click", () => { document.querySelectorAll("#tb-steps input").forEach((i) => (i.checked = true)); tb(); });

  // --- object-fit ---
  const WIDE = "data:image/svg+xml," + encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 200'><rect width='400' height='200' fill='#9ec2e6'/><path d='M0 200 L90 90 L150 140 L230 40 L320 130 L400 80 L400 200Z' fill='#2f5680'/><circle cx='330' cy='45' r='22' fill='#fff6c9'/><text x='12' y='190' font-family='Arial' font-size='16' fill='#fff'>left edge</text><text x='305' y='190' font-family='Arial' font-size='16' fill='#fff'>right edge</text></svg>`);
  $("of-row").innerHTML = ["fill", "contain", "cover"].map((v) => `<figure style="margin:0"><div class="of-box"><img src="${WIDE}" alt="A wide mountain scene" style="object-fit:${v}"></div><figcaption>object-fit: ${v}${v === "fill" ? " (default: stretched)" : v === "contain" ? " (whole image, gaps)" : " (fills, crops the sides)"}</figcaption></figure>`).join("");
'''
ex_fs = src.block('  makeExercise(document.getElementById("ex-formstyle"), {')
ex_more = r'''  makeExercise(document.getElementById("ex-list"), {
    title: "Packing list",
    task: `<ol>
      <li>Make the unordered list's bullets <code>square</code>.</li>
      <li>Make the nested ordered list count with <code>lower-alpha</code>.</li>
      <li>Give list items <code>line-height: 1.5</code>.</li>
    </ol>`,
    html: `<ul>
  <li>Water</li>
  <li>Layers
    <ol>
      <li>Base layer</li>
      <li>Fleece</li>
      <li>Rain shell</li>
    </ol>
  </li>
  <li>Map</li>
</ul>`,
    css: `body { font-family: Georgia, serif; }
`,
    solution: { css: `body { font-family: Georgia, serif; }

ul {
  list-style-type: square;
}

ol {
  list-style-type: lower-alpha;
}

li {
  line-height: 1.5;
}
` },
    hints: ["ul and ol each get their own list-style-type."],
    checks: [
      { label: "ul bullets are square", test: ({ style }) => style("ul", "list-style-type") === "square" },
      { label: "The nested ol uses lower-alpha", test: ({ style }) => style("ol", "list-style-type") === "lower-alpha" },
      { label: "Items have line-height 1.5", test: ({ style }) => Math.abs(parseFloat(style("li", "line-height")) / parseFloat(style("li", "font-size")) - 1.5) < 0.01 },
    ],
  });

  makeExercise(document.getElementById("ex-table"), {
    title: "Elevation table",
    task: `<ol>
      <li>On the table: <code>border-collapse: collapse</code> and <code>font-family: system-ui, sans-serif</code>.</li>
      <li>Give every <code>th</code> and <code>td</code> <code>padding: 0.5em 0.8em</code>.</li>
      <li>Right-align the numbers in the second column with <code>td:nth-child(2)</code>.</li>
      <li>Stripe the body rows: <code>tbody tr:nth-child(odd)</code> gets <code>background-color: #eef1fb</code>.</li>
    </ol>`,
    html: `<table>
  <caption>Summit elevations</caption>
  <thead><tr><th scope="col">Peak</th><th scope="col">Feet</th></tr></thead>
  <tbody>
    <tr><th scope="row">Green Mountain</th><td>8,144</td></tr>
    <tr><th scope="row">Bear Peak</th><td>8,461</td></tr>
    <tr><th scope="row">South Boulder Peak</th><td>8,549</td></tr>
  </tbody>
</table>`,
    css: `th { text-align: left; }
`,
    solution: { css: `th { text-align: left; }

table {
  border-collapse: collapse;
  font-family: system-ui, sans-serif;
}

th, td {
  padding: 0.5em 0.8em;
}

td:nth-child(2) {
  text-align: right;
}

tbody tr:nth-child(odd) {
  background-color: #eef1fb;
}
` },
    hints: ["The numbers are the second child of each row: td:nth-child(2)."],
    checks: [
      { label: "Borders collapse, in a sans-serif font", test: ({ style }) => style("table", "border-collapse") === "collapse" && /system-ui|sans-serif/.test(style("table", "font-family")) },
      { label: "Cells are padded 0.5em 0.8em", test: ({ style }) => style("td", "padding-top") === "8px" && Math.abs(parseFloat(style("td", "padding-left")) - 12.8) < 0.1 },
      { label: "Numbers are right-aligned", test: ({ style }) => style("td", "text-align") === "right" },
      { label: "Rows 1 and 3 are striped, row 2 isn't", test: ({ $$, style }) => { const r = $$("tbody tr"); return style(r[0], "background-color") === "rgb(238, 241, 251)" && style(r[2], "background-color") === "rgb(238, 241, 251)" && style(r[1], "background-color") !== "rgb(238, 241, 251)"; } },
    ],
  });

  makeExercise(document.getElementById("ex-thumbs"), {
    title: "Square thumbnails",
    task: `<p>The images are in a three-column grid. Make each one a 150px-tall thumbnail that fills its column <em>without stretching</em>:</p>
    <ol>
      <li><code>width: 100%</code> and <code>height: 150px</code>.</li>
      <li><code>object-fit: cover</code>.</li>
      <li>Round the corners: <code>border-radius: 8px</code>.</li>
    </ol>`,
    html: `<div class="grid">
  <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 150'%3E%3Crect width='400' height='150' fill='%239ec2e6'/%3E%3Ccircle cx='200' cy='75' r='60' fill='%232f5680'/%3E%3C/svg%3E" alt="Wide view of a lake">
  <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 150 300'%3E%3Crect width='150' height='300' fill='%23b9d99a'/%3E%3Ccircle cx='75' cy='150' r='60' fill='%234b6b2f'/%3E%3C/svg%3E" alt="Tall pine tree">
  <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%23f0b37a'/%3E%3Ccircle cx='100' cy='100' r='60' fill='%238a5228'/%3E%3C/svg%3E" alt="Sandstone arch">
</div>`,
    css: `.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
`,
    solution: { css: `.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }

img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}
` },
    hints: ["The circles in each image should stay round. If they look like ovals, the image is stretched."],
    checks: [
      { label: "Every image is 150px tall and fills its column", test: ({ $, $$ }) => { const col = ($(".grid").clientWidth - 16) / 3; return $$("img").every((i) => Math.abs(i.getBoundingClientRect().height - 150) < 1 && Math.abs(i.getBoundingClientRect().width - col) < 1); } },
      { label: "object-fit: cover, so nothing stretches", test: ({ $$, style }) => $$("img").every((i) => style(i, "object-fit") === "cover") },
      { label: "Corners are rounded 8px", test: ({ style }) => style("img", "border-top-left-radius") === "8px" },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Which selector stripes alternate table rows?", opts: ["tbody tr:nth-child(odd)", "tr:odd", "tbody + tr"], a: 0, why: ":nth-child(odd) picks rows 1, 3, 5…" },
    { id: "q6", q: "A wide photo is forced into a square box and looks squashed. What fixes it?", opts: ["object-fit: cover", "max-width: 100%", "background-size: cover"], a: 0, why: "object-fit: cover fills the box and crops instead of stretching." },
  ]);
''')
write("core-styling-lists-tables-forms.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_more + "\n" + ex_fs + "\n" + quiz + "</script>\n")
