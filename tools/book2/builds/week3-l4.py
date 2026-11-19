import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("devtools")
lab = src.between('  <div class="missions" id="missions"></div>', '  <div class="section-title"><span class="eyebrow">The real thing</span>')
shortcuts = src.between('  <div class="shortcuts">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
extra = """
  .dt .tree { background: none; border-radius: 0; font: inherit; font-variation-settings: inherit; min-height: 0; margin: 0; list-style: none; }
  .dtree { margin: 0; padding: 10px 12px; background: var(--stage); border-radius: 8px; font: 0.88rem/1.7 var(--font-code); font-variation-settings: "MONO" 1; white-space: pre; overflow-x: auto; min-height: 120px; }
  .dtree .added { color: var(--good); font-weight: 700; }
  .sup-row { display: grid; gap: 8px; }
  .sup-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .sup-list li { padding: 8px 10px; border-radius: 6px; background: var(--stage); font: 0.9rem var(--font-code); font-variation-settings: "MONO" 1; display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; }
  .sup-list li.ok b { color: var(--good); } .sup-list li.no b { color: var(--bad); }
</style>
<style id="pvstyle">"""
h = head("Debugging CSS", src.css(), extra)
b = top("Debugging CSS", "When CSS doesn't do what you expect, don't guess and reload. Your browser's developer tools show exactly which rules apply to each element, which lost, and why, and let you try fixes live.", [
  "Open DevTools and inspect any element.",
  "Explain why the DOM in DevTools can differ from your source code.",
  "Read the Styles pane: find crossed-out declarations, edit values and add properties.",
  "Work through a checklist when CSS doesn't apply: validity, support, overrides and a reduced test case."])
b += ST("Read", "How to access browser DevTools") + prose("""
    <p>Every desktop browser has <span class="term">DevTools</span> built in. You'll use them every day from now on.</p>""") + shortcuts
b += ST("Read", "The DOM versus view source") + prose("""
    <p><strong>View source</strong> (<kbd>Ctrl</kbd>/<kbd>Cmd</kbd>+<kbd>U</kbd>) shows the HTML file exactly as the server sent it. DevTools' Elements panel shows something different: the DOM, the tree the browser actually built. They can differ, because the browser repairs mistakes, adds elements the rules require (like <code>&lt;tbody&gt;</code> in a table), and JavaScript can change the page after it loads. When debugging, the DOM is the truth: it's what your CSS is matched against.</p>""")
b += ST("Play", "Source in, DOM out", "Pick an example. Green lines are things the browser added that aren't in the source.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:8px;align-content:start">
      <div class="presets" id="dom-presets" role="group" aria-label="Examples">
        <button class="btn" type="button" data-p="table">A table</button>
        <button class="btn" type="button" data-p="p">Unclosed paragraphs</button>
        <button class="btn" type="button" data-p="nest">A list in a paragraph</button>
      </div>
      <span class="eyebrow">View source</span><pre class="dtree" id="dom-src"></pre>
    </div>
    <div class="panel" style="display:grid;gap:8px;align-content:start"><span class="eyebrow">DOM (Elements panel)</span><pre class="dtree" id="dom-out"></pre><p class="verdict" id="dom-note" aria-live="polite"></p></div>
  </section>

"""
b += ST("Read", "Inspecting the applied CSS") + prose("""
    <p>Right-click an element and choose <strong>Inspect</strong>. On the right of the Elements panel, the <strong>Styles</strong> pane (called <strong>Rules</strong> in Firefox) lists every rule that matches the selected element, most specific at the top, with the file name and line number of each. Declarations that lost are <strong>crossed out</strong>; look higher up to find what beat them. Rules marked <em>user agent stylesheet</em> are the browser's defaults: you can't edit them, but your CSS can override them. Shorthands like <code>margin</code> can be expanded to see their longhands.</p>
    <p>Each declaration has a checkbox: untick it to switch it off and see what changes.</p>
    <h3>Editing values</h3>
    <p>Click any value to edit it. Colours open a colour picker. Changes apply instantly, but only in your browser, until you reload.</p>
    <h3>Adding a new property</h3>
    <p>Click just inside the closing brace of a rule (or in the <code>element.style</code> box at the top) to add a declaration. DevTools autocompletes property names and values as you type.</p>
    <h3>Understanding the box model</h3>
    <p>The <strong>Computed</strong> or <strong>Layout</strong> tab shows a diagram of the selected element's content, padding, border and margin, with real pixel sizes. It's the fastest way to find out where unexpected space comes from (more on that in the next lesson).</p>
    <h3>Solving specificity issues</h3>
    <p>If a declaration is crossed out, the rule above it won. Compare the two selectors' specificity, then fix your CSS: a more specific selector, a later rule, or less specific competition. Don't reach for <code>!important</code>.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p>Changes made in DevTools disappear when you reload. Once a fix works, copy it into your real CSS file.</p></div>""")
b += ST("Play", "Fix the trail card", "This practice panel works like the real Elements panel. Complete the three missions.") + lab
b += ST("Read", "Debugging problems in CSS") + prose("""
    <p>When something won't work, work through these in order:</p>
    <h3>Take a step back from the problem</h3>
    <p>Stuck for a while? Take a break, or explain the problem out loud to someone (or something). The fix is often obvious with fresh eyes.</p>
    <h3>Do you have valid HTML and CSS?</h3>
    <p>Browsers silently ignore CSS they don't understand: a misspelled property, a missing unit, a missing semicolon. Nothing turns red on the page. Run your files through the W3C <a href="https://validator.w3.org/">HTML validator</a> and <a href="https://jigsaw.w3.org/css-validator/">CSS validator</a>, and look for declarations DevTools shows with a warning icon.</p>
    <h3>Are the property and value supported?</h3>
    <p>Newer features may not work in every browser. Check the browser compatibility table at the bottom of any MDN property page. DevTools also flags unsupported declarations.</p>
    <h3>Is something else overriding your CSS?</h3>
    <p>Look for your declaration crossed out in the Styles pane, and see which rule beat it.</p>
    <h3>Make a reduced test case</h3>
    <p>If you still can't find it, rebuild the problem from scratch in as little code as possible:</p>
    <ol>
      <li>Copy just the HTML that shows the problem into a new file, or a playground like CodePen.</li>
      <li>Add only the CSS that affects it.</li>
      <li>Remove things one at a time until the problem disappears. The last thing you removed is involved.</li>
      <li>If it's still a mystery, you now have a tiny example to ask someone about.</li>
    </ol>""")
b += ST("Play", "Does this browser understand it?", "Type a declaration. Your browser's own <code>CSS.supports()</code> says whether it would apply it, or silently ignore it.") + """  <section class="playground even">
    <div class="panel sup-row">
      <label class="eyebrow" for="sup-in">Declaration</label>
      <input class="src" id="sup-in" value="colour: red" spellcheck="false" autocomplete="off">
      <p class="verdict" id="sup-note" aria-live="polite"></p>
    </div>
    <div class="panel sup-row"><span class="eyebrow">Common culprits</span><ul class="sup-list" id="sup-list"></ul></div>
  </section>

"""
b += ST("Practice", "Debug it with DevTools", "Three styles aren't applying. Right-click the preview and choose Inspect to find out why.") + '  <div id="ex-devtools"></div>\n\n'
b += ST("Practice", "Silently ignored", "Every declaration here is valid-looking but ignored. Fix them.") + '  <div id="ex-invalid"></div>\n\n'
b += notes([
  "The DOM in DevTools is what your CSS matches against, not your source file.",
  "The Styles pane lists every matching rule; crossed-out declarations lost.",
  "The file name and line number next to each rule tell you where to make the fix.",
  "Browsers silently ignore invalid or unsupported CSS. Validate, and check MDN's compatibility tables.",
  "A reduced test case isolates a bug, and makes it easy to ask for help.",
], [
  "Fixing the problem in DevTools and forgetting to copy the fix into the real file.",
  "Searching your CSS for a rule that's actually the browser's default.",
  "A rule that's missing completely, from a selector typo or a stylesheet that didn't load.",
  "Typos the browser ignores without complaint: <code>colour</code>, <code>16 px</code>, a missing semicolon.",
  "Debugging the wrong element. Check which element is selected in the tree.",
])
first = src.first_script()
js = r'''
  // --- Source in, DOM out ---
  const DOMS = {
    table: ["<table>\n  <tr><td>Mesa</td><td>6.7</td></tr>\n</table>", "The browser added a <tbody>, because every table row must sit in one. A selector like table > tr matches nothing."],
    p: ["<p>Mesa Trail\n<p>Royal Arch\n<h2>Gear</h2>", "The browser closed each paragraph for you, at the next <p> and before the heading."],
    nest: ["<p>Bring:\n  <ul><li>Water</li></ul>\n</p>", "A list can't go inside a paragraph, so the browser closed the <p> before the <ul> and turned the stray </p> into a new empty paragraph."],
  };
  function domTree(node, depth, srcHas) {
    let out = "";
    for (const n of node.childNodes) {
      if (n.nodeType === 3) { if (n.textContent.trim()) out += "  ".repeat(depth) + '"' + n.textContent.trim() + '"\n'; continue; }
      if (n.nodeType !== 1) continue;
      const t = n.tagName.toLowerCase();
      const line = "  ".repeat(depth) + "<" + t + ">";
      const added = srcHas[t] <= 0;
      srcHas[t] = (srcHas[t] || 0) - 1;
      out += (added ? "\u0001" : "") + line + (added ? "\u0002" : "") + "\n" + domTree(n, depth + 1, srcHas);
    }
    return out;
  }
  function domShow(k) {
    const [code, note] = DOMS[k];
    $("dom-src").textContent = code;
    const body = new DOMParser().parseFromString(code, "text/html").body;
    const counts = {};
    (code.match(/<([a-z0-9]+)/g) || []).forEach((m) => { const t = m.slice(1); counts[t] = (counts[t] || 0) + 1; });
    const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
    $("dom-out").innerHTML = esc(domTree(body, 0, counts)).replace(/\u0001/g, '<span class="added">').replace(/\u0002/g, "</span>");
    $("dom-note").textContent = note;
    document.querySelectorAll("#dom-presets .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.p === k)));
  }
  $("dom-presets").addEventListener("click", (e) => { const b = e.target.closest("[data-p]"); if (b) domShow(b.dataset.p); });
  domShow("table");

  // --- CSS.supports ---
  const CULPRITS = ["colour: red", "color: red", "font-size: 16 px", "font-size: 16px", "padding: 10", "padding: 10px", "background-color: #12345", "display: flex", "text-wrap: balance", "grid-template-columns: subgrid"];
  function supports(decl) {
    const m = decl.trim().replace(/;$/, "").match(/^([\w-]+)\s*:\s*(.+)$/);
    return m ? CSS.supports(m[1], m[2]) : null;
  }
  function supCheck() {
    const v = $("sup-in").value, s = supports(v);
    $("sup-note").className = "verdict " + (s ? "ok" : "bad");
    $("sup-note").textContent = s === null ? "Write it as property: value" : s ? "✓ This browser understands it and would apply it." : "✗ This browser doesn't understand it, so it would skip it silently. Check the spelling, the units and MDN's compatibility table.";
  }
  $("sup-list").innerHTML = CULPRITS.map((c) => { const s = supports(c); return `<li class="${s ? "ok" : "no"}"><span>${c}</span><b>${s ? "✓ applied" : "✗ ignored"}</b></li>`; }).join("");
  $("sup-list").addEventListener("click", (e) => { const li = e.target.closest("li"); if (li) { $("sup-in").value = li.firstChild.textContent; supCheck(); } });
  $("sup-in").addEventListener("input", supCheck);
  supCheck();
'''
ex_dt = src.block('  makeExercise(document.getElementById("ex-devtools"), {')
ex_inv = r'''  makeExercise(document.getElementById("ex-invalid"), {
    title: "Four silent failures",
    task: `<p>The browser skips each of these declarations without an error. Make each one valid, keeping its intended value.</p>
    <ol>
      <li>The heading's colour.</li>
      <li>The paragraph's size: 18 pixels.</li>
      <li>The card's padding: 12 pixels.</li>
      <li>The card's background: light grey <code>#eeeeee</code>.</li>
    </ol>`,
    html: `<div class="card">
  <h2>Bear Peak</h2>
  <p>A long, steep climb with the best views in Boulder.</p>
</div>`,
    css: `h2 {
  colour: darkgreen;
}

p {
  font-size: 18 px;
}

.card {
  padding: 12;
  backround-color: #eeeeee;
}`,
    solution: { css: `h2 {
  color: darkgreen;
}

p {
  font-size: 18px;
}

.card {
  padding: 12px;
  background-color: #eeeeee;
}` },
    hints: ["CSS uses American spelling: color.", "No space between a number and its unit, and lengths other than 0 need a unit."],
    checks: [
      { label: "The heading is dark green", test: ({ style }) => style("h2", "color") === "rgb(0, 100, 0)" },
      { label: "The paragraph is 18px", test: ({ style }) => style("p", "font-size") === "18px" },
      { label: "The card has 12px padding", test: ({ style }) => style(".card", "padding-top") === "12px" },
      { label: "The card is #eeeeee", test: ({ style }) => style(".card", "background-color") === "rgb(238, 238, 238)" },
    ],
  });
'''
quiz = r'''  makeQuiz(document.getElementById("quiz"), [
    { id: "q1", q: "Your table > tr selector matches nothing, though the source has <tr>s directly in the table. Why?", opts: ["The browser added a <tbody> in the DOM", "tr can't be selected", "The > combinator is wrong"], a: 0, why: "CSS matches the DOM, and the DOM has a tbody between them." },
    { id: "q2", q: "In the Styles pane, a declaration is crossed out. What does that mean?", opts: ["Another rule overrode it", "It has a typo", "The file didn't load"], a: 0, why: "Crossed out means it lost to a more specific or later rule." },
    { id: "q3", q: "You fix a bug by editing in DevTools, then reload. What happens?", opts: ["The fix is gone: copy it into your CSS file", "It's saved automatically", "The browser asks to save"], a: 0, why: "DevTools edits are temporary." },
    { id: "q4", q: "font-size: 16 px; What does the browser do?", opts: ["Ignores the declaration silently", "Shows an error on the page", "Uses 16px anyway"], a: 0, why: "Invalid declarations are skipped without any visible error." },
    { id: "q5", q: "Where do you check whether a CSS feature works in older browsers?", opts: ["The compatibility table on its MDN page", "View source", "The CSS validator"], a: 0, why: "MDN's browser compatibility tables list support per browser." },
    { id: "q6", q: "What's a reduced test case?", opts: ["The smallest code that still shows the bug", "A test with fewer users", "Deleting your CSS"], a: 0, why: "Stripping everything else away isolates the cause." },
  ]);
'''
write("core-debugging-css.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_dt + "\n" + ex_inv + "\n" + quiz + "</script>\n")
