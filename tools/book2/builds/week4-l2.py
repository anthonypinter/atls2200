import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("pseudo-elements")
h = head("Pseudo-elements", src.css(), """
  .pe-stage { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 14px 18px; font: 1rem/1.6 Georgia, serif; }
  .pe-stage p { margin: 0 0 10px; }
  #cb-stage.on-all p::first-line { color: #b4410c; font-weight: 700; }
  #cb-stage.on-first p:first-child::first-line { color: #b4410c; font-weight: 700; }
  .gc-box { background: #eef1fb; color: #1d2133; border: 2px solid #2340d9; border-radius: 8px; padding: 14px; font: 1.1rem system-ui, sans-serif; }
""")
b = top("Pseudo-elements", "Pseudo-elements select a part of an element, like its first line or first letter, or add something that isn't in the HTML at all, like a decorative icon. They're written with two colons.", [
  "Style part of an element with <code>::first-line</code>, <code>::first-letter</code>, <code>::marker</code> and <code>::selection</code>.",
  "Combine a pseudo-class and a pseudo-element in one selector.",
  "Generate content with <code>::before</code> and <code>::after</code> and the <code>content</code> property.",
  "Use generated content for icons and shapes, and know when not to."])
b += ST("Read", "What is a pseudo-element?") + prose("""
    <p>A <span class="term">pseudo-element</span> acts as if you'd wrapped part of the content in a new element and styled that. It's written with <strong>two colons</strong>, which is how you tell it apart from a pseudo-class.</p>
    <p>For example, to style the first line of a paragraph, you can't wrap it in a <code>&lt;span&gt;</code>: where the line ends depends on the screen width. <code>::first-line</code> always finds it:</p>
    <pre class="snippet" data-lang="css">article p::first-line {
  font-size: 120%;
  font-weight: bold;
}</pre>
    <p>Others select different parts:</p>
    <ul>
      <li><code>::first-letter</code>: the first letter, for a drop cap.</li>
      <li><code>::marker</code>: a list item's bullet or number.</li>
      <li><code>::selection</code>: text the visitor highlights.</li>
      <li><code>::placeholder</code>: the hint text in an input.</li>
    </ul>""")
b += ST("Play", "Switch each one on", "Turn each pseudo-element on and off to see exactly what it adds.") + '  <div class="grid-demos" id="demos"></div>\n\n'
b += ST("Read", "Combining pseudo-classes and pseudo-elements") + prose("""
    <p>A selector can have both. To make only the first line of the <em>first</em> paragraph bold, put the pseudo-class first and the pseudo-element last:</p>
    <pre class="snippet" data-lang="css">article p:first-child::first-line {
  font-weight: bold;
}</pre>""")
b += ST("Play", "Every paragraph, or only the first?", "Narrow the window to watch <code>::first-line</code> follow the line break.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="seg" id="cb" role="group" aria-label="Selector">
        <button class="btn" type="button" data-v="">(off)</button>
        <button class="btn" type="button" data-v="on-all">p::first-line</button>
        <button class="btn" type="button" data-v="on-first">p:first-child::first-line</button>
      </div>
    </div>
    <div class="pe-stage" id="cb-stage"><p>Royal Arch is a steep 3.4-mile round trip from Chautauqua Park to a sandstone arch with views over the plains.</p><p>Start early in summer: afternoon storms build quickly over the Flatirons, and there's little shade on the upper switchbacks.</p></div>
  </section>

"""
b += ST("Read", "Generating content with ::before and ::after") + prose("""
    <p><code>::before</code> and <code>::after</code> insert a new box at the start or end of an element's content, filled with whatever the <code>content</code> property says:</p>
    <pre class="snippet" data-lang="css">.box::before {
  content: "This should show before the other content. ";
}</pre>
    <p>Every <code>::before</code> and <code>::after</code> needs <code>content</code>, even an empty one, <code>content: ""</code>, or it doesn't appear at all. They go <em>inside</em> the element, as its first and last child, so they don't work on empty elements like <code>&lt;img&gt;</code> or <code>&lt;input&gt;</code>.</p>
    <p>Use them for decoration only. Text in <code>content</code> can't be selected or copied, and screen readers treat it inconsistently, so anything visitors need to read belongs in the HTML.</p>
    <h3>Generated content icons</h3>
    <p>A common use is a small decorative icon: <code>.box::after { content: " ➥"; }</code>.</p>
    <h3>Generated shapes</h3>
    <p>With empty content and <code>display: block</code>, a pseudo-element becomes a box you can size and colour: an underline bar, a coloured dot, a corner ribbon.</p>
    <pre class="snippet" data-lang="css">.box::before {
  content: "";
  display: block;
  width: 100px;
  height: 10px;
  background-color: rebeccapurple;
}</pre>""")
b += ST("Play", "Playing with generated content", "Edit the content, move it before or after, or make it a shape.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="seg" id="gc-where" role="group" aria-label="Pseudo-element">
        <button class="btn" type="button" data-v="before">::before</button>
        <button class="btn" type="button" data-v="after">::after</button>
      </div>
      <div class="control"><label for="gc-content">content:</label><input class="src" id="gc-content" value='" ➥"' spellcheck="false" autocomplete="off"></div>
      <label class="toggle"><input type="checkbox" id="gc-shape"> make it a shape (empty content, block, 100 × 10px)</label>
      <pre class="snippet" id="gc-code"></pre>
    </div>
    <div class="gc-box" id="gc-box">Trail conditions: dry</div>
  </section>
  <style id="gc-style"></style>

"""
b += ST("Practice", "Decorate with ::before and ::after", "Add three decorations with CSS alone. None of them belongs in the HTML.") + '  <div id="ex-pseudo"></div>\n\n'
b += ST("Practice", "Parts of the text", "Style parts that you couldn't select with any element.") + '  <div id="ex-parts"></div>\n\n'
b += notes([
  "Pseudo-elements use two colons; pseudo-classes use one.",
  "<code>::first-line</code>, <code>::first-letter</code>, <code>::marker</code> and <code>::selection</code> style parts of existing content.",
  "Pseudo-class first, pseudo-element last: <code>p:first-child::first-line</code>.",
  "<code>::before</code> and <code>::after</code> need a <code>content</code> property, even an empty one.",
  "Generated content is for decoration; real information goes in the HTML.",
], [
  "Forgetting <code>content</code>, so the pseudo-element never appears.",
  "Adding <code>::before</code> to an <code>&lt;img&gt;</code> or <code>&lt;input&gt;</code>.",
  "Putting important text in <code>content</code>, where it can't be copied and may not be read aloud.",
  "Writing the pseudo-element before the pseudo-class: <code>p::first-line:first-child</code>.",
])
first = src.first_script()
js = r'''
  // --- Combining ---
  function cb(v) { $("cb-stage").className = "pe-stage " + v; document.querySelectorAll("#cb .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.v === v))); }
  $("cb").addEventListener("click", (e) => { const b = e.target.closest("[data-v]"); if (b) cb(b.dataset.v); });
  cb("on-first");

  // --- Generated content ---
  let where = "after";
  function gc() {
    const shape = $("gc-shape").checked;
    const decl = shape ? `content: "";\n  display: block;\n  width: 100px;\n  height: 10px;\n  background-color: rebeccapurple;` : `content: ${$("gc-content").value || '""'};\n  color: #b4410c;`;
    const css = `.box::${where} {\n  ${decl}\n}`;
    $("gc-code").textContent = css;
    $("gc-style").textContent = css.replace(".box", "#gc-box");
    $("gc-content").disabled = shape;
    document.querySelectorAll("#gc-where .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.v === where)));
  }
  $("gc-where").addEventListener("click", (e) => { const b = e.target.closest("[data-v]"); if (b) { where = b.dataset.v; gc(); } });
  ["gc-content", "gc-shape"].forEach((id) => $(id).addEventListener("input", gc));
  gc();
'''
ex_p = src.block('  makeExercise(document.getElementById("ex-pseudo"), {')
ex_parts = r'''  makeExercise(document.getElementById("ex-parts"), {
    title: "Drop cap, markers and highlights",
    task: `<ol>
      <li>Give the first letter of the <code>.intro</code> paragraph <code>font-size: 3em</code>, <code>float: left</code> and <code>color: #b4410c</code>: a drop cap.</li>
      <li>Make the list's bullets <code>color: #0b6b5e</code> with <code>::marker</code>.</li>
      <li>When visitors select text, give it <code>background-color: #ffe08a</code> with <code>::selection</code>.</li>
    </ol>`,
    html: `<p class="intro">Bear Peak is the long way up: 2,800 feet of climbing through ponderosa pine to a jagged summit with views across the whole Front Range.</p>
<ul>
  <li>Water: at least two litres</li>
  <li>Layers for the summit wind</li>
</ul>`,
    css: `body { font: 18px/1.6 Georgia, serif; }
`,
    solution: { css: `body { font: 18px/1.6 Georgia, serif; }

.intro::first-letter {
  font-size: 3em;
  float: left;
  color: #b4410c;
}

li::marker {
  color: #0b6b5e;
}

::selection {
  background-color: #ffe08a;
}
` },
    hints: ["Two colons: .intro::first-letter", "::selection on its own applies to all text on the page."],
    checks: [
      { label: "A drop cap: 3em, floated left, #b4410c", test: ({ $, doc }) => { const s = doc.defaultView.getComputedStyle($(".intro"), "::first-letter"); return s.fontSize === "54px" && s.float === "left" && s.color === "rgb(180, 65, 12)"; } },
      { label: "Bullets are #0b6b5e", test: ({ $, doc }) => doc.defaultView.getComputedStyle($("li"), "::marker").color === "rgb(11, 107, 94)" },
      { label: "Selected text is #ffe08a", test: ({ doc }) => [...doc.styleSheets[0].cssRules].some((r) => /::selection/.test(r.selectorText || "") && r.style.backgroundColor === "rgb(255, 224, 138)") },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Which selector styles the first line of only the first paragraph?", opts: ["p:first-child::first-line", "p::first-line:first-child", "p::first-child"], a: 0, why: "Pseudo-class first, pseudo-element last." },
    { id: "q6", q: "Where should a link's \\"(opens a PDF)\\" warning go?", opts: ["In the HTML, so everyone gets it", "In ::after content", "In a title attribute"], a: 0, why: "Generated content isn't reliably read aloud and can't be copied." },
  ]);
''')
write("core-pseudo-elements.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_p + "\n" + ex_parts + "\n" + quiz + "</script>\n")
