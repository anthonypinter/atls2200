import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("pseudo-classes")
lab = src.between('  <section class="playground even">\n    <div class="lab" id="lab">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Position:')
nth = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="formula">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Styling links')
menu = src.between('  <section class="playground">\n    <div class="panel controls">\n      <label class="check3"><input type="checkbox" id="n1">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Pseudo-classes and Link States", src.css(), """
  .lk-out { width: 100%; height: 170px; border: 1px solid var(--line); border-radius: 8px; background: #fff; }
""")
b = top("Pseudo-classes and Link States", "Some styles should apply only some of the time: while a link is hovered, when a field is focused, to the first item in a list. Pseudo-classes select elements by their state or position, without adding a single class to your HTML.", [
  "Select elements by position with <code>:first-child</code>, <code>:last-child</code> and <code>:nth-child()</code>.",
  "Style user-action states: <code>:hover</code>, <code>:focus</code>, <code>:focus-visible</code> and <code>:active</code>.",
  "Style the five link states in the right order.",
  "Turn a list of links into a navigation menu."])
b += ST("Read", "What is a pseudo-class?") + prose("""
    <p>A <span class="term">pseudo-class</span> is a keyword after a selector, starting with one colon, that selects elements only when they're in a certain state. It acts as if you'd added a class to the element at exactly the right moment, without touching the HTML.</p>
    <h3>Basic pseudo-class example</h3>
    <p>To make the first paragraph of each article larger, you could add <code>class="first"</code> to it. But then if someone adds a new paragraph at the top, the class is on the wrong one. A pseudo-class always finds the right element:</p>
    <pre class="snippet" data-lang="css">article p:first-child {
  font-size: 120%;
  font-weight: bold;
}</pre>
    <p><code>:first-child</code> and <code>:last-child</code> match an element that's the first or last child of its parent. <code>:nth-child()</code> takes a pattern: <code>odd</code>, <code>even</code>, a number, or a formula like <code>3n+1</code>.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p><code>p:first-child</code> means "a p that is the first child of its parent", not "the first p". If an <code>h2</code> comes first, no paragraph matches.</p></div>""")
b += ST("Play", "Position: :nth-child()", "The formula <code>an+b</code> is calculated for n = 0, 1, 2, 3… and every result picks an item.") + nth
b += ST("Read", "User-action pseudo-classes") + prose("""
    <p>These match only while the visitor is doing something:</p>
    <ul>
      <li><code>:hover</code>: while the pointer is over the element. Touch screens don't have it, so never hide anything important behind a hover.</li>
      <li><code>:focus</code>: when the element is selected for keyboard input, by clicking a field or pressing Tab.</li>
      <li><code>:focus-visible</code>: focus, but only when the browser thinks a visible ring helps, mainly keyboard use.</li>
      <li><code>:active</code>: while it's being pressed.</li>
    </ul>
    <p>Many people use a keyboard instead of a mouse, so give every <code>:hover</code> style a matching <code>:focus-visible</code> one, in the same rule:</p>
    <pre class="snippet" data-lang="css">.btn:hover,
.btn:focus-visible {
  background: #1a2fa8;
}</pre>
    <p>Forms add more: <code>:disabled</code>, <code>:checked</code>, <code>:required</code>, <code>:invalid</code>.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p>Never remove the focus outline with <code>outline: none</code> unless you add a clear <code>:focus-visible</code> style in its place. Without it, keyboard users can't see where they are.</p></div>""")
b += ST("Play", "Interactive states", "Point at, click and tab to each control.") + lab
b += ST("Practice", "Style the states", "Stripes, hover feedback and a first-item highlight, all without adding a single class.") + '  <div id="ex-states"></div>\n\n'
b += ST("Read", "Link states") + prose("""
    <p>Links are the most-styled element with states. They have five:</p>
    <ul>
      <li><code>:link</code>: a link with an <code>href</code> that hasn't been visited.</li>
      <li><code>:visited</code>: one that's in the browser's history.</li>
      <li><code>:hover</code>, <code>:focus</code> and <code>:active</code>, as above.</li>
    </ul>
    <h3>Default styles</h3>
    <p>Browsers underline links, colour them blue (purple once visited, red while active), show a pointer cursor, and draw a focus outline. All of it can be changed. Keep links recognisable, though: if a link looks like normal text, nobody will click it.</p>
    <h3>Styling links</h3>
    <p>Write the state rules in this order, because they have the same specificity and later rules win. If <code>:hover</code> came before <code>:visited</code>, visited links would never show the hover style. Remember it as <strong>LoVe Fears HAte</strong>:</p>
    <pre class="snippet" data-lang="css">a { }          /* every link */
a:link { }
a:visited { }
a:focus { }
a:hover { }
a:active { }</pre>
    <p>For privacy, <code>:visited</code> can only change colours, not size or layout.</p>""")
b += ST("Play", "Style your own links", "Edit the CSS, then hover over, tab to and click the links in the result.") + """  <div class="two">
    <div class="panel" style="display:grid;gap:8px">
      <label class="eyebrow" for="lk-css">CSS</label>
      <textarea class="src" id="lk-css" spellcheck="false" style="min-height:250px"></textarea>
    </div>
    <div class="panel" style="display:grid;gap:8px;align-content:start"><span class="eyebrow">Result</span><iframe class="lk-out" id="lk-out" title="Links"></iframe><p class="verdict" id="lk-note" aria-live="polite"></p></div>
  </div>

"""
b += ST("Practice", "Link states in order", "Style the trail links, with the states in an order that works.") + '  <div id="ex-links"></div>\n\n'
b += ST("Read", "Including icons on links") + prose("""
    <p>A small icon can tell people where a link goes, like an arrow for links to other websites. Combine an attribute selector with the <code>::after</code> pseudo-element (next lesson) to add one without touching the HTML:</p>
    <pre class="snippet" data-lang="css">a[href^="http"]::after {
  content: " ↗";
}</pre>""")
b += ST("Read", "Styling links as buttons") + prose("""
    <p>A navigation menu is just a list of links. Remove the bullets, put the items in a row, give each link padding so the whole box is clickable, and add hover and focus styles. Mark the current page with <code>aria-current="page"</code> in the HTML, and style that attribute.</p>""")
b += ST("Play", "Building a menu", "Turn on each step.") + menu
b += notes([
  "Pseudo-classes start with one colon and select by state or position.",
  "<code>:first-child</code> means \"first child of its parent\", whatever its type.",
  "Pair every <code>:hover</code> style with <code>:focus-visible</code>.",
  "Link states in order: <code>:link</code>, <code>:visited</code>, <code>:focus</code>, <code>:hover</code>, <code>:active</code>.",
  "A nav menu is a styled list of links; mark the current page with <code>aria-current</code>.",
], [
  "Removing the focus outline without a replacement.",
  "Putting <code>:hover</code> before <code>:visited</code>, so visited links never react.",
  "Expecting <code>p:first-child</code> to find the first paragraph after a heading.",
  "Hiding information or menus behind <code>:hover</code> only.",
  "Styling links so they look like plain text.",
])
first = src.first_script()
js = r'''
  // --- Style your own links ---
  $("lk-css").value = `body { font: 18px/1.6 Georgia, serif; padding: 8px 16px; }

a {
  color: #265301;
  text-decoration-thickness: 2px;
}

a:visited {
  color: #437a16;
}

a:focus {
  outline: 3px solid #bae498;
}

a:hover {
  background: #bae498;
}

a:active {
  background: #265301;
  color: #cdfeaa;
}`;
  function lk() {
    $("lk-out").srcdoc = `<!doctype html><html><head><style>${$("lk-css").value}</style></head><body><p>Read about <a href="#mesa">the Mesa Trail</a>, <a href="#arch">Royal Arch</a> and <a href="https://example.com">the city's trail site</a>.</p><p>Press Tab to move between the links.</p>`;
    const order = ["link", "visited", "focus", "hover", "active"].map((s) => $("lk-css").value.indexOf("a:" + s)).filter((i) => i >= 0);
    const sorted = order.every((v, i) => i === 0 || v > order[i - 1]);
    $("lk-note").className = "verdict " + (sorted ? "ok" : "bad");
    $("lk-note").textContent = sorted ? "✓ The states are in a working order." : "✗ The states are out of order, so a later rule can override an earlier state. Use :link, :visited, :focus, :hover, :active.";
  }
  $("lk-css").addEventListener("input", lk);
  lk();
'''
ex_states = src.block('  makeExercise(document.getElementById("ex-states"), {')
ex_links = r'''  makeExercise(document.getElementById("ex-links"), {
    title: "Trail links",
    task: `<ol>
      <li>Make all links <code>color: #265301</code>.</li>
      <li>Add <code>a:visited</code> with <code>color: #437a16</code>.</li>
      <li>Add one rule for <code>a:hover</code> and <code>a:focus-visible</code> that sets <code>background-color: #bae498</code>.</li>
      <li>Add <code>a:active</code> with <code>color: white</code> and <code>background-color: #265301</code>.</li>
    </ol>
    <p>Keep them in that order. Then hover over and tab to the links to try them.</p>`,
    html: `<p>This weekend: <a href="#mesa">Mesa Trail</a>, <a href="#arch">Royal Arch</a> and <a href="#bear">Bear Peak</a>.</p>`,
    css: `body { font: 18px/1.6 Georgia, serif; }
`,
    solution: { css: `body { font: 18px/1.6 Georgia, serif; }

a {
  color: #265301;
}

a:visited {
  color: #437a16;
}

a:hover,
a:focus-visible {
  background-color: #bae498;
}

a:active {
  color: white;
  background-color: #265301;
}
` },
    hints: ["Separate a:hover and a:focus-visible with a comma to share one rule.", "Order: a, a:visited, a:hover/a:focus-visible, a:active."],
    checks: [
      { label: "Links are #265301", test: ({ style }) => style("a", "color") === "rgb(38, 83, 1)" },
      { label: "a:visited, a:hover + a:focus-visible and a:active rules exist", test: ({ doc }) => { const s = [...doc.styleSheets[0].cssRules].map((r) => r.selectorText || ""); return s.some((x) => /a:visited/.test(x)) && s.some((x) => /a:hover/.test(x) && /a:focus-visible/.test(x)) && s.some((x) => /a:active/.test(x)); } },
      { label: "The hover rule sets #bae498, the active rule white on #265301", test: ({ doc }) => { const r = [...doc.styleSheets[0].cssRules]; const hv = r.find((x) => /a:hover/.test(x.selectorText || "")), ac = r.find((x) => /a:active/.test(x.selectorText || "")); return hv && ac && hv.style.backgroundColor === "rgb(186, 228, 152)" && ac.style.color === "white" && ac.style.backgroundColor === "rgb(38, 83, 1)"; } },
      { label: "The states are in order: visited, hover, active", test: ({ code }) => { const i = ["a:visited", "a:hover", "a:active"].map((s) => code.css.indexOf(s)); return i.every((v) => v >= 0) && i[0] < i[1] && i[1] < i[2]; } },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Which pseudo-class matches an input that's selected for typing?", opts: [":focus", ":active", ":checked"], a: 0, why: ":focus applies while an element has keyboard focus." },
    { id: "q6", q: "li:nth-child(3n+1) selects which items?", opts: ["1, 4, 7, 10…", "3, 6, 9…", "Only the 4th"], a: 0, why: "n = 0, 1, 2… gives 1, 4, 7…" },
  ]);
''')
write("core-pseudo-classes.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_states + "\n" + ex_links + "\n" + quiz + "</script>\n")
