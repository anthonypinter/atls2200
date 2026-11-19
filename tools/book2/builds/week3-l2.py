import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("selectors")
css = src.css(); css = css[:css.index("  .calc {")]
pg = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="sel-input">', '  <div class="section-title"><span class="eyebrow">Reference</span>')
ref = src.between('  <div class="ref-grid">', '  <div class="section-title"><span class="eyebrow">Specificity</span>')
extra = """
  .attr-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .attr-list li { padding: 8px 12px; border-radius: 6px; border: 1.5px solid var(--line); background: var(--panel); font: 0.92rem var(--font-code); font-variation-settings: "MONO" 1; }
  .attr-list li.hit { background: var(--cobalt-soft); border-color: var(--cobalt); box-shadow: 0 0 0 2px var(--cobalt); }
  .attr-list li .why { display: block; font: 0.8rem var(--font-body); color: var(--muted); margin-top: 2px; }
"""
h = head("Selectors", css, extra)
b = top("Selectors", "Every CSS rule starts with a selector: the part that says which elements to style. Choose them by type, by class or id, by attribute, or by where they sit in the page.", [
  "Select elements by type, class and id, and combine them in a selector list.",
  "Use the universal selector and chain classes onto one element.",
  "Select elements by attribute, including the start, end or middle of its value.",
  "Use descendant, child and sibling combinators to target elements by position."])
b += ST("Read", "What is a selector?") + prose("""
    <p>A <span class="term">selector</span> is the first part of a rule, before the braces. The elements it matches are called its <em>subject</em>, and those are the elements the declarations style.</p>
    <pre class="snippet" data-lang="css">h1 { color: navy; }   /* subject: every h1 */
.box { padding: 1em; } /* subject: every element with class="box" */</pre>""")
b += ST("Read", "Type, class and ID selectors") + prose("""
    <h3>Type selectors</h3>
    <p>A <span class="term">type selector</span> is just an element name: <code>span</code>, <code>strong</code>, <code>em</code>. It matches every element of that type.</p>
    <h3>Class selectors</h3>
    <p>A <span class="term">class</span> selector is a dot followed by a class name. <code>.highlight</code> matches every element with <code>class="highlight"</code>, whatever its type. Classes are reusable, so they're what you'll use most.</p>
    <ul>
      <li><strong>On a particular element:</strong> <code>span.highlight</code> matches only spans with that class; <code>h1.highlight</code> only headings.</li>
      <li><strong>More than one class:</strong> an element can have several, separated by spaces: <code>class="notebox warning"</code>. Chain them with no space to match elements with both: <code>.notebox.warning</code>.</li>
    </ul>
    <h3>ID selectors</h3>
    <p>An <span class="term">ID</span> selector is a hash followed by an id: <code>#one</code> matches the element with <code>id="one"</code>. An id should appear only once per page, so an ID selector styles one element. Classes are usually the better choice: they're reusable and easier to override.</p>""")
b += ST("Read", "Selector lists") + prose("""
    <p>When several selectors share the same declarations, list them with commas instead of repeating the rule:</p>
    <pre class="snippet" data-lang="css">h1,
.special {
  color: blue;
}</pre>
    <p>Careful: if any selector in a list is invalid, the whole rule is thrown away. <code>h1, ..special { }</code> styles nothing at all, not even the <code>h1</code>s.</p>""")
b += ST("Read", "The universal selector") + prose("""
    <p>An asterisk, <code>*</code>, matches everything. On its own, <code>* { margin: 0; }</code> removes the margin from every element. Inside a selector it can make your meaning clearer: <code>article :first-child</code> (with a space) and <code>article *:first-child</code> mean the same thing, "any first child inside an article", but the second is much harder to misread as <code>article:first-child</code>.</p>""")
b += ST("Practice", "Type, class, ID and lists", "Write four rules.") + '  <div id="ex-basic"></div>\n\n'
b += ST("Read", "Attribute selectors") + prose("""
    <p>An <span class="term">attribute selector</span> matches elements by their attributes, written in square brackets.</p>
    <h3>Presence and value selectors</h3>
    <table class="mini-table"><tbody>
      <tr><td><code>[attr]</code></td><td>has the attribute at all: <code>a[title]</code></td></tr>
      <tr><td><code>[attr="value"]</code></td><td>the value is exactly this: <code>input[type="email"]</code></td></tr>
      <tr><td><code>[attr~="value"]</code></td><td>one of its space-separated words is exactly this</td></tr>
      <tr><td><code>[attr|="value"]</code></td><td>exactly this, or this followed by a hyphen: <code>[lang|="en"]</code> matches <code>en</code> and <code>en-US</code></td></tr>
    </tbody></table>
    <h3>Substring matching selectors</h3>
    <table class="mini-table"><tbody>
      <tr><td><code>[attr^="value"]</code></td><td>starts with: <code>a[href^="https"]</code></td></tr>
      <tr><td><code>[attr$="value"]</code></td><td>ends with: <code>a[href$=".pdf"]</code></td></tr>
      <tr><td><code>[attr*="value"]</code></td><td>contains anywhere: <code>[class*="card"]</code></td></tr>
    </tbody></table>""")
b += ST("Play", "Which items match?", "Each list item has a different <code>class</code> value. Pick a selector.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:8px;align-content:start">
      <div class="presets" id="at-presets" role="group" aria-label="Attribute selectors"></div>
      <p class="verdict" id="at-note" aria-live="polite"></p>
    </div>
    <ul class="attr-list" id="at-list"></ul>
  </section>

"""
b += ST("Practice", "Style links by their address", "Use attribute selectors only: no classes.") + '  <div id="ex-attr"></div>\n\n'
b += ST("Read", "Combinators") + prose("""
    <p>A <span class="term">combinator</span> joins two selectors and says how the elements relate:</p>
    <ul>
      <li><strong>Descendant</strong> (a space): <code>.box p</code> matches a <code>p</code> anywhere inside <code>.box</code>, however deeply nested.</li>
      <li><strong>Child</strong> (<code>&gt;</code>): <code>ul &gt; li</code> matches only <code>li</code>s that are direct children of a <code>ul</code>, not ones in a nested list.</li>
      <li><strong>Next-sibling</strong> (<code>+</code>): <code>h1 + p</code> matches a <code>p</code> that comes straight after an <code>h1</code>, with the same parent.</li>
      <li><strong>Subsequent-sibling</strong> (<code>~</code>): <code>h1 ~ p</code> matches every <code>p</code> anywhere after an <code>h1</code>, with the same parent, even with other elements in between.</li>
    </ul>
    <h3>Combining combinators with selectors</h3>
    <p>Any selector can sit on either side: <code>ul &gt; li.a</code>, <code>.card h2 + p</code>. Read them right to left: "a <code>p</code>, straight after an <code>h2</code>, inside a <code>.card</code>".</p>
    <div class="callout tip"><p class="callout-title">Watch the spaces</p><p><code>.tag .hard</code> (with a space) means "a <code>.hard</code> inside a <code>.tag</code>". <code>.tag.hard</code> (no space) means "one element with both classes". That one space is behind a lot of confusing bugs.</p></div>""")
b += ST("Play", "Type a selector", "Type any selector and the matching elements light up. Try the suggestions, then write your own.") + pg
b += ST("Read", "Quick reference") + ref
b += ST("Practice", "Target exactly the right elements", "The declarations are done. Write a selector for each.") + '  <div id="ex-select"></div>\n\n'
b += notes([
  "Type selectors match an element name; <code>.class</code> matches a class; <code>#id</code> matches one element.",
  "Chain with no space (<code>.a.b</code>) for elements that have both; separate with commas for a list.",
  "Attribute selectors use square brackets: <code>^=</code> starts, <code>$=</code> ends, <code>*=</code> contains.",
  "Combinators: space (inside), <code>&gt;</code> (direct child), <code>+</code> (right after), <code>~</code> (any later sibling).",
  "Prefer classes. IDs and long chains are hard to override later.",
], [
  "A stray space: <code>.tag .hard</code> when you meant <code>.tag.hard</code>.",
  "Forgetting the dot: <code>card { }</code> looks for a <code>&lt;card&gt;</code> element.",
  "One typo in a selector list, which throws away the whole rule.",
  "Reusing an id on several elements instead of using a class.",
  "Expecting <code>h1 + p</code> to match a paragraph that isn't directly after the heading.",
])
first = src.first_script()
first = first[:first.index("  // Specificity:")]
js = r'''
  // --- Attribute matcher ---
  const ITEMS = ["a", "ab", "bca", "a-b", "b a", "cab"];
  const ATTRS = {
    '[class]': "Every item: they all have a class attribute.",
    '[class="a"]': "Only an exact match of the whole value.",
    '[class~="a"]': "Any item where a is one whole word in the value, so “b a” matches too.",
    '[class|="a"]': "Exactly a, or a followed by a hyphen: a and a-b.",
    '[class^="a"]': "Values starting with a.",
    '[class$="a"]': "Values ending with a.",
    '[class*="a"]': "Values containing a anywhere: every item here.",
  };
  $("at-list").innerHTML = ITEMS.map((c) => `<li class="${c}">&lt;li class="${c}"&gt;</li>`).join("");
  $("at-presets").innerHTML = Object.keys(ATTRS).map((s) => `<button class="btn" type="button">li${s}</button>`).join("");
  function attr(sel) {
    $("at-list").querySelectorAll("li").forEach((li) => li.classList.remove("hit"));
    const hits = [...$("at-list").querySelectorAll(sel)];
    hits.forEach((li) => li.classList.add("hit"));
    $("at-note").textContent = `${hits.length} match. ${ATTRS[sel.slice(2)]}`;
    document.querySelectorAll("#at-presets .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.textContent === sel)));
  }
  $("at-presets").addEventListener("click", (e) => { const b = e.target.closest(".btn"); if (b) attr(b.textContent); });
  attr('li[class="a"]');
'''
ex_select = src.block('  makeExercise(document.getElementById("ex-select"), {')
ex_more = r'''  makeExercise(document.getElementById("ex-basic"), {
    title: "Notes and warnings",
    task: `<ol>
      <li>Give every element with the <code>notebox</code> class <code>border: 2px solid gray</code>.</li>
      <li>Make only noteboxes that are <em>also</em> <code>warning</code> <code>background-color: lightyellow</code>.</li>
      <li>Make the element with the id <code>intro</code> <code>font-size: 120%</code>.</li>
      <li>Make <code>h1</code> and <code>h2</code> <code>color: teal</code>, in one rule.</li>
    </ol>`,
    html: `<h1>Trail conditions</h1>
<p id="intro">Updated every morning by rangers.</p>
<h2>Mesa Trail</h2>
<div class="notebox">Dry and clear.</div>
<h2>Royal Arch</h2>
<div class="notebox warning">Icy near the top.</div>
<p class="warning">Check the forecast before you go.</p>`,
    css: `body { font-family: system-ui, sans-serif; }
.notebox, .warning { padding: 8px; margin: 6px 0; }
`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.notebox, .warning { padding: 8px; margin: 6px 0; }

.notebox {
  border: 2px solid gray;
}

.notebox.warning {
  background-color: lightyellow;
}

#intro {
  font-size: 120%;
}

h1, h2 {
  color: teal;
}
` },
    hints: ["No space between .notebox and .warning means one element with both.", "A hash selects an id: #intro."],
    checks: [
      { label: "Both noteboxes have a 2px gray border", test: ({ $$, style }) => $$(".notebox").every((n) => style(n, "border-top-width") === "2px" && style(n, "border-top-color") === "rgb(128, 128, 128)") },
      { label: "Only the warning notebox is light yellow", test: ({ style }) => style(".notebox.warning", "background-color") === "rgb(255, 255, 224)" && style("p.warning", "background-color") !== "rgb(255, 255, 224)" },
      { label: "#intro is 120%", test: ({ style }) => Math.abs(parseFloat(style("#intro", "font-size")) - 19.2) < 0.2 },
      { label: "h1 and h2 are teal", test: ({ $$, style }) => $$("h1, h2").every((h) => style(h, "color") === "rgb(0, 128, 128)") },
    ],
  });

  makeExercise(document.getElementById("ex-attr"), {
    title: "Link types",
    task: `<ol>
      <li>Links whose <code>href</code> starts with <code>https</code>: <code>color: darkgreen</code>.</li>
      <li>Links whose <code>href</code> ends with <code>.pdf</code>: <code>font-weight: bold</code>.</li>
      <li>Links whose <code>href</code> starts with <code>mailto:</code>: <code>font-style: italic</code>.</li>
      <li>Any element with a <code>title</code> attribute: <code>background-color: lavender</code>.</li>
    </ol>`,
    html: `<ul>
  <li><a href="https://www.nps.gov">National Park Service</a></li>
  <li><a href="maps/mesa.pdf">Mesa Trail map</a></li>
  <li><a href="mailto:rangers@example.com">Email the rangers</a></li>
  <li><a href="events.html">Events</a></li>
  <li><abbr title="Rocky Mountain National Park">RMNP</abbr></li>
</ul>`,
    css: `body { font-family: system-ui, sans-serif; }
`,
    solution: { css: `body { font-family: system-ui, sans-serif; }

a[href^="https"] {
  color: darkgreen;
}

a[href$=".pdf"] {
  font-weight: bold;
}

a[href^="mailto:"] {
  font-style: italic;
}

[title] {
  background-color: lavender;
}
` },
    hints: ["^= means “starts with” and $= means “ends with”.", "[title] on its own matches any element that has the attribute."],
    checks: [
      { label: "Only the https link is dark green", test: ({ $, style }) => style('a[href^="https"]', "color") === "rgb(0, 100, 0)" && style('a[href="events.html"]', "color") !== "rgb(0, 100, 0)" },
      { label: "The PDF link is bold", test: ({ style }) => +style('a[href$=".pdf"]', "font-weight") >= 700 && +style('a[href="events.html"]', "font-weight") < 700 },
      { label: "The mailto link is italic", test: ({ style }) => style('a[href^="mailto"]', "font-style") === "italic" },
      { label: "The abbr is lavender", test: ({ style }) => style("abbr", "background-color") === "rgb(230, 230, 250)" },
    ],
  });
'''
quiz = r'''  makeQuiz(document.getElementById("quiz"), [
    { id: "q1", q: "Which selector matches every element with class=\"card\"?", opts: [".card", "#card", "card"], a: 0, why: "A dot selects a class; card on its own looks for a <card> element." },
    { id: "q2", q: "What does .tag.hard match?", opts: ["One element with both classes", "A .hard inside a .tag", "Either class"], a: 0, why: "No space means both at once." },
    { id: "q3", q: "h1, ..intro { color: red; } What gets styled?", opts: ["Nothing: one invalid selector drops the whole rule", "Just the h1s", "The h1s and .intro"], a: 0, why: "An invalid selector in a list invalidates the entire rule." },
    { id: "q4", q: "Which selects links to PDF files?", opts: ["a[href$=\".pdf\"]", "a[href^=\".pdf\"]", "a.pdf"], a: 0, why: "$= matches the end of the value." },
    { id: "q5", q: "Which matches only list items directly inside .trails, not nested ones?", opts: [".trails > li", ".trails li", ".trails + li"], a: 0, why: "> is the child combinator: direct children only." },
    { id: "q6", q: "What does h2 + p match?", opts: ["A p immediately after an h2, with the same parent", "Every p after an h2", "A p inside an h2"], a: 0, why: "+ is the next-sibling combinator. ~ would match every later p." },
  ]);
'''
write("core-selectors.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_more + "\n" + ex_select + "\n" + quiz + "</script>\n")
