import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("box-model")
pg = src.between('  <section class="playground">\n    <div class="panel controls" aria-label="Box settings">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
extra = """
  .od-stage { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 14px; font: 1rem/1.6 Georgia, serif; }
  .od-stage ul { list-style: none; padding: 0; margin: 0; border: 2px dashed #2340d9; gap: 6px; }
  .od-stage li { border: 1px solid #0b6b5e; background: #e3f2ee; padding: 2px 8px; }
  .mc-stage { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 14px; display: grid; justify-items: stretch; }
  .mc-stage .blk { background: #9ec2e6; color: #1d2133; padding: 10px; font: 600 0.9rem var(--font-code); font-variation-settings: "MONO" 1; outline: 1px solid #2f5680; }
  .ib-stage { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 20px 14px; font: 1rem/1.5 system-ui, sans-serif; color: #1d2133; }
  .ib-stage ul { list-style: none; margin: 0; padding: 0; }
  .ib-stage li { display: inline; }
  .ib-stage a { background: #2340d9; color: #fff; text-decoration: none; padding: 1em 2em; outline: 1px dashed #b4410c; }
"""
h = head("The Box Model", src.css(), extra)
b = top("The Box Model", "Everything on a web page is a box: headings, paragraphs, links, even a single word in bold. How big each box is, and how much space it takes up, follows a set of rules called the box model.", [
  "Explain the difference between block and inline boxes, and between outer and inner display types.",
  "Name the four parts of a box and calculate its size in the standard and alternative box models.",
  "Use margin, border and padding shorthands, and predict margin collapsing.",
  "Use <code>display: inline-block</code> to give inline elements a usable size."])
b += ST("Read", "Block and inline boxes") + prose("""
    <p>Boxes come in two main kinds, and the kind decides how a box behaves in the page's flow:</p>
    <ul>
      <li>A <span class="term" data-term="Block element">block</span> box starts on a new line, stretches to fill the width of its container, and respects <code>width</code>, <code>height</code>, padding and margin. Headings, paragraphs and <code>&lt;div&gt;</code>s are block by default.</li>
      <li>An <span class="term" data-term="Inline element">inline</span> box flows within a line of text. It doesn't start a new line, and <code>width</code> and <code>height</code> don't apply. <code>&lt;a&gt;</code>, <code>&lt;span&gt;</code>, <code>&lt;em&gt;</code> and <code>&lt;strong&gt;</code> are inline by default.</li>
    </ul>""")
b += ST("Read", "Inner and outer display types") + prose("""
    <p>The <code>display</code> property actually sets two things. The <strong>outer</strong> display type decides how the box behaves among its neighbours: block or inline. The <strong>inner</strong> display type decides how the box lays out its own children. Normally the children just flow, but <code>display: flex</code> makes them a <span class="term">flexbox</span> layout (Week 5).</p>
    <p>So <code>display: flex</code> means "block on the outside, flex on the inside", and <code>display: inline-flex</code> means "inline on the outside, flex on the inside".</p>""")
b += ST("Play", "Examples of different display types", "The list's outer type decides how it sits in the paragraph; its inner type decides how the items sit inside it.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="seg" id="od" role="group" aria-label="display on the ul">
        <button class="btn" type="button" data-v="block">block</button>
        <button class="btn" type="button" data-v="flex">flex</button>
        <button class="btn" type="button" data-v="inline-flex">inline-flex</button>
      </div>
      <p class="verdict" id="od-note" aria-live="polite"></p>
    </div>
    <div class="od-stage">Pack <ul id="od-ul"><li>water</li><li>snacks</li><li>a map</li></ul> before you leave the trailhead.</div>
  </section>

"""
b += ST("Read", "What is the CSS box model?") + prose("""
    <h3>Parts of a box</h3>
    <p>Every block box has four layers, from the inside out:</p>
    <ul>
      <li><strong>Content</strong>: the text or image itself, sized with <code>width</code> and <code>height</code>.</li>
      <li><span class="term">Padding</span>: space between the content and the border. It's inside the box, so it shows the background.</li>
      <li><span class="term">Border</span>: the line around the padding.</li>
      <li><span class="term">Margin</span>: space outside the border that pushes other boxes away. It's always transparent.</li>
    </ul>
    <h3>The standard CSS box model</h3>
    <p>By default, <code>width</code> and <code>height</code> set only the content; padding and border are added on top. Margin isn't counted in the box's size, but it does take up space.</p>
    <pre class="snippet" data-lang="css">.box {
  width: 350px;
  height: 150px;
  margin: 10px;
  padding: 25px;
  border: 5px solid black;
}  /* the box is 350 + 25 + 25 + 5 + 5 = 410px wide, and 210px tall */</pre>
    <h3>The alternative CSS box model</h3>
    <p>With <code><span class="term">box-sizing</span>: border-box</code>, <code>width</code> sets the whole visible box, padding and border included, and the content shrinks to fit. That's much easier to plan with. Many developers switch every element to it at the top of their stylesheet:</p>
    <pre class="snippet" data-lang="css">html {
  box-sizing: border-box;
}
*, *::before, *::after {
  box-sizing: inherit;
}</pre>
    <div class="callout tip"><p class="callout-title">Use DevTools</p><p>Select an element and open the Computed or Layout tab: it draws the box model with the size of every layer. When a box is bigger than you expected, look there first.</p></div>""")
b += ST("Play", "Playing with box models", "Change each layer and watch the math. Then switch <code>box-sizing</code> and see the same settings give a different size.") + pg
b += ST("Read", "Margins, padding, and borders") + prose("""
    <p>Each of the three has a shorthand that sets all four sides, and longhands for one side at a time: <code>margin-top</code>, <code>padding-left</code>, <code>border-bottom</code>. Shorthands with several values go clockwise from the top: <code>margin: 10px 20px</code> is 10px top and bottom, 20px left and right.</p>
    <h3>Margin</h3>
    <p>Margin pushes other boxes away. It can be negative, which pulls things closer or makes boxes overlap. <code>margin: 0 auto</code> on a block with a width centres it: the left and right margins share the leftover space.</p>
    <p><strong>Margin collapsing:</strong> when the bottom margin of one block meets the top margin of the next, they don't add up. They collapse into the larger of the two. A heading with <code>margin-bottom: 30px</code> above a paragraph with <code>margin-top: 20px</code> leaves 30px between them, not 50px.</p>""")
b += ST("Play", "Margin collapsing", "Set each box's margin, and measure the real gap between them.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="control"><label for="mc-a">Box A: margin-bottom</label><input id="mc-a" type="range" min="0" max="60" step="5" value="30"><span class="readout" id="mc-a-out"></span></div>
      <div class="control"><label for="mc-b">Box B: margin-top</label><input id="mc-b" type="range" min="-20" max="60" step="5" value="20"><span class="readout" id="mc-b-out"></span></div>
      <p class="verdict" id="mc-note" aria-live="polite"></p>
    </div>
    <div class="mc-stage"><div class="blk" id="mc-1">Box A</div><div class="blk" id="mc-2">Box B</div></div>
  </section>

"""
b += prose("""
    <h3>Borders</h3>
    <p><code>border: 2px solid teal</code> sets width, style and colour on all four sides. Each side and each part has a longhand: <code>border-top</code>, <code>border-width</code>, <code>border-left-color</code> and so on. Without a style (<code>solid</code>, <code>dashed</code>, <code>dotted</code>…) there's no border at all.</p>
    <h3>Padding</h3>
    <p>Padding is the space inside the border. Unlike margin, it can't be negative. Use it to stop text from touching the edge of a coloured box.</p>""")
b += ST("Practice", "Size and space two cards", "Fix the cards' size without touching their width, padding or border, then space and centre them.") + '  <div id="ex-cards"></div>\n\n'
b += ST("Read", "The box model and inline boxes") + prose("""
    <p>Inline boxes follow only part of the box model. <code>width</code> and <code>height</code> are ignored. Padding, borders and margins do apply, but only left and right ones push other content away: top and bottom padding and borders spread over the lines above and below without moving them.</p>""")
b += ST("Read", "Using display: inline-block") + prose("""
    <p><code>display: inline-block</code> is the middle ground. The box sits in a line of text like a word, doesn't force a new line, but respects <code>width</code>, <code>height</code> and padding, pushing other content out of the way. It's perfect for giving links a bigger, clickable area.</p>""")
b += ST("Play", "Playing with inline-block", "These nav links have <code>padding: 1em 2em</code>. Switch their display.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="seg" id="ib" role="group" aria-label="display on the links">
        <button class="btn" type="button" data-v="inline">inline</button>
        <button class="btn" type="button" data-v="inline-block">inline-block</button>
      </div>
      <p class="verdict" id="ib-note" aria-live="polite"></p>
    </div>
    <div class="ib-stage"><p style="margin:0 0 10px">Trail Club</p><ul id="ib-ul"><li><a href="#ib">Trails</a></li> <li><a href="#ib">Events</a></li> <li><a href="#ib">Join</a></li></ul><p style="margin:10px 0 0">Next hike: Saturday.</p></div>
  </section>

"""
b += ST("Practice", "Bigger link targets", "Turn these links into comfortable, tappable buttons.") + '  <div id="ex-links"></div>\n\n'
b += notes([
  "Block boxes start a new line and fill their container; inline boxes flow in the text and ignore width and height.",
  "<code>display</code> sets an outer type (block or inline) and an inner type (normal flow, flex, grid).",
  "Standard box model: width sets the content; padding and border are added on top.",
  "<code>box-sizing: border-box</code> makes width include padding and border.",
  "Touching vertical margins collapse into the larger one.",
  "<code>inline-block</code> flows like text but respects width, height and padding.",
], [
  "Setting <code>width</code> on a link or span and wondering why nothing happens.",
  "Forgetting that padding and border make a content-box element wider than its <code>width</code>.",
  "Expecting 30px + 20px margins to make a 50px gap.",
  "Using padding where you meant margin: padding fills with the background colour.",
  "A border with a width and colour but no style, so it doesn't appear.",
])
first = src.first_script()
js = r'''
  // --- Outer and inner display ---
  const OD = {
    block: "Block outside: the list breaks the sentence onto new lines. Normal flow inside: each li stacks as a block.",
    flex: "Still block outside, so the sentence is still broken. But flex inside: the items now sit in a row.",
    "inline-flex": "Inline outside: the list sits inside the sentence like a word. Flex inside: the items stay in a row.",
  };
  function od(v) {
    $("od-ul").style.display = v;
    $("od-note").textContent = `display: ${v}. ${OD[v]}`;
    document.querySelectorAll("#od .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.v === v)));
  }
  $("od").addEventListener("click", (e) => { const b = e.target.closest("[data-v]"); if (b) od(b.dataset.v); });
  od("block");

  // --- Margin collapsing ---
  function mc() {
    const a = +$("mc-a").value, bm = +$("mc-b").value;
    $("mc-1").style.marginBottom = a + "px"; $("mc-2").style.marginTop = bm + "px";
    $("mc-a-out").textContent = a + "px"; $("mc-b-out").textContent = bm + "px";
    const gap = Math.round($("mc-2").getBoundingClientRect().top - $("mc-1").getBoundingClientRect().bottom);
    $("mc-note").textContent = bm < 0
      ? `Measured gap: ${gap}px. With a negative margin, the browser adds the largest positive and the most negative: ${a} + (${bm}) = ${a + bm}px.`
      : `Measured gap: ${gap}px, not ${a + bm}px. The margins collapsed into the larger one, ${Math.max(a, bm)}px.`;
  }
  ["mc-a", "mc-b"].forEach((id) => $(id).addEventListener("input", mc));
  mc();

  // --- inline-block ---
  function ib(v) {
    document.querySelectorAll("#ib-ul a").forEach((a) => (a.style.display = v));
    $("ib-note").textContent = v === "inline"
      ? "inline: the padding paints over the lines above and below, but doesn't push them away. The text overlaps."
      : "inline-block: the padding now pushes the surrounding lines away, and the whole coloured area is clickable.";
    document.querySelectorAll("#ib .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.v === v)));
  }
  $("ib").addEventListener("click", (e) => { const b = e.target.closest("[data-v]"); if (b) ib(b.dataset.v); });
  $("ib-ul").addEventListener("click", (e) => { if (e.target.closest("a")) e.preventDefault(); });
  ib("inline");
'''
ex_cards = src.block('  makeExercise(document.getElementById("ex-cards"), {')
ex_links = r'''  makeExercise(document.getElementById("ex-links"), {
    title: "Nav links",
    task: `<ol>
      <li>Make the links <code>display: inline-block</code>.</li>
      <li>Give them <code>padding: 0.75em 1.5em</code>.</li>
      <li>Give them <code>margin-right: 8px</code> so they don't touch.</li>
    </ol>
    <p>The paragraph below should be pushed down, not overlapped.</p>`,
    html: `<nav>
  <a href="#">Trails</a>
  <a href="#">Events</a>
  <a href="#">Join</a>
</nav>
<p>Next hike: Saturday at 8am.</p>`,
    css: `body { font-family: system-ui, sans-serif; }
nav a {
  background: #0b6b5e;
  color: white;
  text-decoration: none;
}`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
nav a {
  background: #0b6b5e;
  color: white;
  text-decoration: none;
  display: inline-block;
  padding: 0.75em 1.5em;
  margin-right: 8px;
}` },
    hints: ["display: inline-block lets top and bottom padding take up real space."],
    checks: [
      { label: "Links are inline-block", test: ({ $$, style }) => $$("nav a").every((a) => style(a, "display") === "inline-block") },
      { label: "Padding is 0.75em 1.5em", test: ({ style }) => style("nav a", "padding-top") === "12px" && style("nav a", "padding-left") === "24px" },
      { label: "8px between links", test: ({ style }) => style("nav a", "margin-right") === "8px" },
      { label: "The paragraph sits below the links", test: ({ $ }) => $("p").getBoundingClientRect().top >= $("nav a").getBoundingClientRect().bottom - 0.5 },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q6", q: "You set width: 200px on a link, and nothing changes. Why?", opts: ["Links are inline, and inline boxes ignore width", "Links can't have a width at all", "200px is too small"], a: 0, why: "Make it inline-block or block and the width applies." },
  ]);
''')
write("core-box-model.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_cards + "\n" + ex_links + "\n" + quiz + "</script>\n")
