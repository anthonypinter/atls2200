import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("media-queries")
lab = src.between('  <section class="lab">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Media Queries", src.css(), """
  .mq-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
  .mq-row input.src { flex: 1 1 260px; }
  .mq-res { font: 800 1.3rem var(--font-display); }
  .mq-res.yes { color: var(--good); } .mq-res.no { color: var(--bad); }
  .mq-dev { width: 100%; border-collapse: collapse; font: 0.85rem var(--font-code); font-variation-settings: "MONO" 1; }
  .mq-dev td { padding: 4px 8px; border-bottom: 1px solid var(--line); }
  .mq-dev td:last-child { text-align: right; font-weight: 700; }
  .mq-dev .y { color: var(--good); } .mq-dev .n { color: var(--muted); }
""")
b = top("Media Queries", "A media query applies CSS only when a condition is true: the screen is at least this wide, the page is being printed, the device has a mouse. It's how one stylesheet adapts to every device.", [
  "Write media queries with media types, feature rules and the newer range syntax.",
  "Combine conditions with <em>and</em>, <em>or</em> (commas) and <em>not</em>.",
  "Choose breakpoints based on your content, and build a layout mobile first.",
  "Recognise when a flexible layout doesn't need a media query at all.",
])
b += ST("Read", "Media query basics") + prose("""
    <p>A <span class="term">media query</span> wraps some CSS in a condition. The rules inside only apply while the condition is true:</p>
    <pre class="snippet" data-lang="css">@media media-type and (media-feature-rule) {
  /* CSS rules go here */
}</pre>
    <h3>Media types</h3>
    <p>The media type says what kind of output the CSS is for: <code>screen</code>, <code>print</code> or <code>all</code>. Leave it out and the query applies to everything. A print stylesheet is a common use:</p>
    <pre class="snippet" data-lang="css">@media print {
  body { font-size: 12pt; }
  nav, .ads { display: none; }
}</pre>
    <h3>Media feature rules</h3>
    <p>Features test something about the device or the window. The one you'll use most is <strong>width</strong>, with a <code>min-</code> or <code>max-</code> prefix:</p>
    <pre class="snippet" data-lang="css">@media (min-width: 600px) { … }   /* 600px or wider */
@media (max-width: 599px) { … }   /* up to 599px */</pre>
    <p>A few others are worth knowing:</p>
    <ul>
      <li><code>(orientation: landscape)</code> or <code>portrait</code>: is the window wider than it is tall?</li>
      <li><code>(hover: hover)</code>: can the main input hover, like a mouse? Touchscreens can't, so hover-only menus fail there.</li>
      <li><code>(pointer: fine)</code> or <code>coarse</code>: is it precise, like a mouse, or a finger? Make targets bigger for <code>coarse</code>.</li>
    </ul>
    <h3>Using ranged syntax</h3>
    <p>Newer browsers let you write width tests as comparisons, which is easier to read than <code>min-</code> and <code>max-</code>:</p>
    <pre class="snippet" data-lang="css">@media (width >= 600px) { … }            /* same as min-width: 600px */
@media (30em <= width <= 50em) { … }     /* between 30em and 50em */</pre>""")
b += ST("Read", "More complex media queries") + prose("""
    <h3>"and" logic in media queries</h3>
    <p>Join conditions with <code>and</code>; all of them must be true:</p>
    <pre class="snippet" data-lang="css">@media screen and (width >= 600px) and (orientation: landscape) { … }</pre>
    <h3>"or" logic in media queries</h3>
    <p>Separate whole queries with commas; any one being true is enough:</p>
    <pre class="snippet" data-lang="css">@media (width >= 600px), (orientation: landscape) { … }</pre>
    <h3>"not" logic in media queries</h3>
    <p><code>not</code> at the start reverses the whole query. <code>not all and (orientation: landscape)</code> matches portrait.</p>""")
b += ST("Play", "Ask your browser", "Type a media query (without @media) or pick one. Your browser tests it right now, against this window and this device.") + """  <section class="playground">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="mq-row"><input class="src" id="mq-q" value="(width >= 600px)" spellcheck="false" aria-label="Media query to test"><span class="mq-res" id="mq-res" aria-live="polite"></span></div>
      <div class="seg" id="mq-pre">
        <button class="btn">(width &gt;= 600px)</button><button class="btn">(max-width: 400px)</button><button class="btn">(600px &lt;= width &lt;= 1000px)</button>
        <button class="btn">print</button><button class="btn">screen and (orientation: landscape)</button><button class="btn">(hover: hover)</button>
        <button class="btn">(pointer: coarse)</button><button class="btn">(max-width: 500px), (orientation: portrait)</button><button class="btn">not all and (hover: hover)</button>
      </div>
      <p class="hint" id="mq-note"></p>
    </div>
    <div class="panel" style="display:grid;gap:8px;align-content:start">
      <span class="eyebrow">This device, right now</span>
      <table class="mq-dev" id="mq-dev"></table>
      <p class="hint">Resize the window, or open this page on your phone, and watch the answers change.</p>
    </div>
  </section>

"""
b += ST("Read", "How to choose breakpoints") + prose("""
    <p>The width where a query kicks in is called a <span class="term">breakpoint</span>. Don't choose breakpoints from a list of phone and tablet sizes: there are thousands of devices, and new ones every year. Instead, start narrow and widen your browser window slowly (or use the responsive design mode in your browser's DevTools). Add a breakpoint wherever your layout starts to look wrong: lines too long, cards too stretched, too much empty space.</p>
    <p>When two queries both match and set the same property, the later one wins, just like any other rule. So list <code>min-width</code> queries from smallest to largest.</p>""")
b += ST("Play", "Change the screen width", "Drag the slider to change the pretend screen width and watch which rules switch on.") + lab
b += ST("Read", "Mobile-first responsive design") + prose("""
    <p>There are two ways to write those queries. You can write the wide-screen layout first and use <code>max-width</code> queries to undo it on small screens. Or you can write the simple, single-column layout first, with no query at all, and use <code>min-width</code> queries to <em>add</em> columns as the screen grows.</p>
    <p>The second approach is called <span class="term">mobile first</span>. It usually means less CSS, because you never write a rule just to cancel another. And because single-column, in source order, is close to what HTML does with no CSS, your base layout is mostly done before you start. The next lesson, <a href="core-mobile-first.html">Responsive Design and Mobile First</a>, builds a whole page this way.</p>""")
b += ST("Read", "Creating your own mobile-first design") + prose("""
    <p>A mobile-first stylesheet has the same shape every time: base styles, then one query per breakpoint.</p>
    <pre class="snippet" data-lang="css">/* Base: one column for every screen */
body { width: 90%; margin: 0 auto; }

/* Medium: two columns */
@media screen and (width >= 40em) {
  article { display: grid; grid-template-columns: 3fr 1fr; column-gap: 20px; }
  nav ul { display: flex; }
}

/* Wide: a third column */
@media screen and (width >= 70em) {
  main { display: grid; grid-template-columns: 3fr 1fr; }
}</pre>
    <p>Notice the breakpoints are in <code>em</code>. If someone sets a larger default text size, an <code>em</code> breakpoint moves with it, so the layout switches to fewer columns when the text needs more room.</p>
    <h3>viewport meta</h3>
    <p>None of this works on phones without one line in your <code>&lt;head&gt;</code>:</p>
    <pre class="snippet" data-lang="html">&lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;</pre>
    <p>Without it, mobile browsers pretend to be about 980px wide and shrink the whole page down, so your phone layout never switches on.</p>""")
b += ST("Practice", "Rewrite the queries mobile first", "These queries start from the desktop and undo it. Flip them to start small and add.") + '  <div id="ex-mq"></div>\n\n'
b += ST("Read", "Do you really need a media query?") + prose("""
    <p>Flexbox and Grid are flexible by design, so many layouts adapt with no breakpoint at all. This grid fits as many 200px-plus columns as there's room for, from one on a phone to five on a monitor:</p>
    <pre class="snippet" data-lang="css">.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}</pre>
    <p>Reach for a media query when something has to <em>change</em> at a size: the nav moves, a sidebar appears, the order of things shifts. For "more columns when there's room", let the layout do it.</p>""")
b += ST("Practice", "Print, hover, orientation and ranges", "Four queries that aren't about a simple minimum width.") + '  <div id="ex-feat"></div>\n\n'
b += notes([
  "<code>@media print</code>, <code>screen</code> or <code>all</code> picks the output; features like <code>(min-width: 600px)</code> test the device.",
  "Range syntax reads naturally: <code>(width &gt;= 600px)</code>, <code>(30em &lt;= width &lt;= 50em)</code>.",
  "<code>and</code> needs every condition; a comma means <em>or</em>; <code>not</code> reverses a whole query.",
  "Mobile first: base styles for phones, then <code>min-width</code> queries, smallest to largest.",
  "Pick breakpoints where <em>your</em> layout starts to look wrong, and don't forget the viewport meta tag.",
], [
  "Forgetting the viewport meta tag, so phones ignore your queries.",
  "<code>@media min-width: 600px</code> without parentheses. Features always go in brackets.",
  "Putting a query <em>above</em> the base rules, so the base rules override it.",
  "Hiding important features behind <code>:hover</code> without checking <code>(hover: hover)</code>.",
])
first = src.first_script()
js = r'''
  // --- Ask your browser ---
  const MQ_DEV = [["(width >= 600px)", "at least 600px wide"], ["(orientation: landscape)", "landscape"], ["(hover: hover)", "main input can hover"], ["(pointer: coarse)", "main input is a finger"], ["(prefers-color-scheme: dark)", "dark mode on"], ["(prefers-reduced-motion: reduce)", "reduced motion on"], ["print", "printing"]];
  function mqTest() {
    const q = $("mq-q").value.trim(), m = window.matchMedia(q), bad = m.media === "not all" && !/^not all/.test(q);
    $("mq-res").className = "mq-res " + (bad ? "no" : m.matches ? "yes" : "no");
    $("mq-res").textContent = bad ? "invalid" : m.matches ? "true" : "false";
    $("mq-note").textContent = bad ? "The browser couldn't read that query, so it treats it as never matching. Check the brackets and colons." : `The browser reads it as: ${m.media}. Your window is ${innerWidth}px wide.`;
    $("mq-dev").innerHTML = MQ_DEV.map(([q2, t]) => { const y = matchMedia(q2).matches; return `<tr><td>${q2}</td><td class="${y ? "y" : "n"}">${y ? "yes" : "no"}</td></tr>`; }).join("");
  }
  $("mq-q").addEventListener("input", mqTest);
  $("mq-pre").addEventListener("click", (e) => { const x = e.target.closest("button"); if (x) { $("mq-q").value = x.textContent; mqTest(); } });
  window.addEventListener("resize", mqTest);
  mqTest();
'''
NORM = '\n      const norm = (t) => t.replace(/\\s/g, "").replace(/^\\(width>=(\\d+)px\\)$/, "(min-width:$1px)");'
def accept_range(block):
    block = block.replace("checks: (() => {", "checks: (() => {" + NORM, 1)
    block = block.replace('r.conditionText.replace(/\\s/g, "")', "norm(r.conditionText)")
    block = block.replace('m.conditionText.replace(/\\s/g, "")', "norm(m.conditionText)")
    assert 'conditionText.replace(/\\s/g, "")' not in block, block
    return block
ex_mq = accept_range(src.block('  makeExercise(document.getElementById("ex-mq"), {'))
ex_mq = ex_mq.replace('"min-width: 600px means “600px or wider”."', '"min-width: 600px (or width >= 600px) means “600px or wider”."')
ex_f = r'''  makeExercise(document.getElementById("ex-feat"), {
    title: "Queries for different situations",
    task: `<ol>
      <li>When the page is printed, hide the <code>nav</code>.</li>
      <li>The <code>.tip</code> says "hover over a photo for details". Only show it (<code>display: block</code>) on devices that can hover.</li>
      <li>In landscape orientation, make <code>.gallery</code> two equal columns.</li>
      <li>Using range syntax, make the <code>h1</code> <code>2.5rem</code> when the width is between <code>30em</code> and <code>50em</code>.</li>
    </ol>`,
    html: `<nav><a href="#">Trails</a> · <a href="#">Maps</a></nav>
<h1>Trail photos</h1>
<p class="tip">Hover over a photo for details.</p>
<div class="gallery"><div>Mesa</div><div>Royal Arch</div></div>`,
    css: `body { font-family: system-ui, sans-serif; }
.tip { display: none; color: #555; }
.gallery { display: grid; gap: 8px; }
.gallery div { padding: 20px; background: #b9c4ef; }
`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.tip { display: none; color: #555; }
.gallery { display: grid; gap: 8px; }
.gallery div { padding: 20px; background: #b9c4ef; }

@media print {
  nav { display: none; }
}
@media (hover: hover) {
  .tip { display: block; }
}
@media (orientation: landscape) {
  .gallery { grid-template-columns: 1fr 1fr; }
}
@media (30em <= width <= 50em) {
  h1 { font-size: 2.5rem; }
}
` },
    hints: [
      "@media print { nav { display: none; } }",
      "(hover: hover) and (orientation: landscape) are features, so they go in brackets.",
      "Range syntax puts width between two values: (30em <= width <= 50em).",
    ],
    checks: (() => {
      const q = (doc, re) => [...doc.styleSheets[0].cssRules].filter((r) => r.media && re.test(r.conditionText.replace(/\s+/g, " ")));
      const inside = (doc, re, sel, test) => q(doc, re).some((m) => [...m.cssRules].some((r) => r.selectorText === sel && test(r.style)));
      return [
        { label: "@media print hides the nav", test: ({ doc }) => inside(doc, /^print$/, "nav", (s) => s.display === "none") },
        { label: "(hover: hover) shows the tip", test: ({ doc }) => inside(doc, /^\(hover: ?hover\)$/, ".tip", (s) => s.display === "block") },
        { label: "(orientation: landscape) makes two equal columns", test: ({ doc }) => inside(doc, /^\(orientation: ?landscape\)$/, ".gallery", (s) => /^(1fr 1fr|repeat\(2, ?1fr\))$/.test(s.gridTemplateColumns)) },
        { label: "(30em <= width <= 50em) sets the h1 to 2.5rem", test: ({ doc }) => inside(doc, /^\(30em ?<= ?width ?<= ?50em\)$/, "h1", (s) => s.fontSize === "2.5rem") },
      ];
    })(),
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Which query matches only when BOTH are true: at least 600px wide and landscape?", opts: ["(width >= 600px), (orientation: landscape)", "(width >= 600px) and (orientation: landscape)", "not (width >= 600px)"], a: 1, why: "and needs every condition; a comma means or." },
    { id: "q6", q: "What does (hover: hover) test?", opts: ["Whether the mouse is over the element right now", "Whether the main input device can hover", "Whether the page is printed"], a: 1, why: "It's about the device: a mouse can hover, a finger can't." },
    { id: "q7", q: "Which is the same as (min-width: 600px)?", opts: ["(width <= 600px)", "(width >= 600px)", "(width = 600px)"], a: 1, why: "Range syntax: width is greater than or equal to 600px." },
  ]);
''')
write("core-media-queries.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_mq + "\n" + ex_f + "</script>\n")
