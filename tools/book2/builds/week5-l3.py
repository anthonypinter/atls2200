import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("flexbox")
pg = src.between('  <section class="playground">\n    <div class="panel controls" aria-label="Flex container settings">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Flexbox", src.css(), """
  .fx-wrap { background: var(--stage); border-radius: 8px; padding: 14px; overflow-x: auto; }
  .fx-row { display: flex; gap: 8px; border: 2px dashed var(--prop); border-radius: 6px; padding: 6px; }
  .fx-it { min-width: 0; background: var(--item-1); color: #fff; border-radius: 6px; padding: 10px 8px; font: 700 0.8rem var(--font-code); font-variation-settings: "MONO" 1; display: grid; gap: 2px; text-align: center; }
  .fx-it:nth-child(2) { background: var(--item-2); } .fx-it:nth-child(3) { background: var(--item-3); }
  .fx-it small { font-weight: 400; opacity: 0.9; }
  .fx-ctl { display: grid; grid-template-columns: auto 1fr; gap: 6px 10px; align-items: center; font: 0.85rem var(--font-code); font-variation-settings: "MONO" 1; }
  .ao-row { display: flex; gap: 8px; min-height: 170px; align-items: stretch; background: var(--stage); border-radius: 8px; padding: 10px; }
  .ao-it { flex: 1; border: 0; border-radius: 6px; color: #fff; font: 700 0.95rem var(--font-code); font-variation-settings: "MONO" 1; padding: 10px 6px; cursor: pointer; background: var(--item-1); }
  .ao-it:nth-child(2) { background: var(--item-2); } .ao-it:nth-child(3) { background: var(--item-3); } .ao-it:nth-child(4) { background: var(--item-4); }
  .ao-it:focus-visible { outline: 3px solid var(--ink); outline-offset: 2px; }
  .ao-tbl { border-collapse: collapse; font: 0.85rem var(--font-code); font-variation-settings: "MONO" 1; }
  .ao-tbl td, .ao-tbl th { padding: 3px 6px; text-align: left; }
""")
b = top("Flexbox", "Flexbox lays out items in one direction, a row or a column. You set the rules on the container and its children follow them, sharing out space, lining up and wrapping as the room changes.", [
  "Turn a parent into a flex container and name its main and cross axes.",
  "Change direction and wrapping with <code>flex-direction</code>, <code>flex-wrap</code> and <code>flex-flow</code>.",
  "Share out space between items with the <code>flex</code> shorthand.",
  "Align items with <code>justify-content</code>, <code>align-items</code> and <code>align-self</code>, and reorder them with <code>order</code>.",
])
b += ST("Read", "Why flexbox?") + prose("""
    <p>For a long time, CSS had no good way to do some very common things: center a box vertically inside its parent, make several columns share the available width equally, or make columns the same height whatever their content. People used floats and workarounds that broke easily.</p>
    <p><span class="term">Flexbox</span> was designed for exactly these jobs. It lays items out along one line, a row or a column, and gives you control over how they share space and line up.</p>""")
b += ST("Read", "Specifying what elements to lay out as flexible boxes") + prose("""
    <p>Add <code>display: flex</code> to a parent, and its direct children line up in a row:</p>
    <pre class="snippet" data-lang="css">section {
  display: flex;
}</pre>
    <p>The parent becomes the <em>flex container</em>, and its children become <em>flex items</em>. Only direct children: grandchildren are laid out normally unless their own parent is also a flex container. Almost every rule goes on the container, which is also the most common mistake. <code>display: flex</code> goes on the parent, not on the items you want to move.</p>""")
b += ST("Read", "The flex model") + prose("""
    <p>Every flex container has two directions:</p>
    <ul>
      <li>The <span class="term">main axis</span> runs the way items flow. With the default <code>flex-direction: row</code>, that's left to right. Its two ends are the <em>main start</em> and <em>main end</em>, and an item's length along it is its <em>main size</em>.</li>
      <li>The <span class="term">cross axis</span> runs at a right angle to it, so up and down in a row, from <em>cross start</em> to <em>cross end</em>. An item's length along it is its <em>cross size</em>.</li>
    </ul>
    <p>Most flex properties work along one axis or the other, so keep track of which way the main axis runs.</p>""")
b += ST("Read", "Columns or rows?") + prose("""
    <p><code>flex-direction</code> sets the main axis: <code>row</code> (the default), <code>column</code>, or <code>row-reverse</code> and <code>column-reverse</code>, which run backwards. Switch to <code>column</code> and the axes swap: the main axis now runs top to bottom.</p>""")
b += ST("Read", "Wrapping") + prose("""
    <p>Flex items don't wrap by default. When they run out of room they shrink, and if they can't shrink any more, they overflow the container. <code>flex-wrap: wrap</code> lets them move onto a new line instead. Each new line is laid out on its own.</p>""")
b += ST("Read", "flex-flow shorthand") + prose("""
    <p><code>flex-flow</code> sets both at once, direction first:</p>
    <pre class="snippet" data-lang="css">.cards { display: flex; flex-flow: row wrap; }</pre>""")
b += ST("Play", "Try every container setting", "Change one property at a time and watch the items move. Then switch to a column and see which controls swap jobs.") + pg
b += ST("Read", "Flexible sizing of flex items") + prose("""
    <p>Now for the items themselves. The <code>flex</code> property on an item says how much of the container's spare space it should take:</p>
    <pre class="snippet" data-lang="css">article { flex: 1; }               /* every article gets an equal share */
article:nth-child(3) { flex: 2; }   /* this one gets two shares */</pre>
    <p>The number has no unit: it's a proportion. With <code>flex: 1</code>, <code>flex: 1</code> and <code>flex: 2</code>, the space is split into four shares, and the third item gets two of them.</p>
    <p>You can add a starting size too. <code>flex: 1 200px</code> means "start at 200px, then share out whatever space is left". That's useful for items that shouldn't get too narrow.</p>""")
b += ST("Read", "flex: shorthand versus longhand") + prose("""
    <p><code>flex</code> is a shorthand for three properties:</p>
    <ul>
      <li><code>flex-grow</code>: how many shares of spare space the item takes (the unitless number).</li>
      <li><code>flex-shrink</code>: how much it shrinks, compared with the others, when there isn't enough room.</li>
      <li><code>flex-basis</code>: its starting size before space is shared out.</li>
    </ul>
    <p>Use the shorthand: it sets sensible values for the parts you leave out. <code>flex: 1</code> is <code>1 1 0%</code> (grow, shrink, start from nothing), while the initial value is <code>0 1 auto</code> (don't grow, but do shrink, and start from the content's size). <code>flex: none</code> is <code>0 0 auto</code>: a fixed size that neither grows nor shrinks.</p>""")
b += ST("Play", "Share out the space", "Give each item a flex value, then change the container's width.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="fx-w">container width</label><input id="fx-w" type="range" min="260" max="700" step="10" value="560"><span class="readout" id="fx-w-out"></span></div>
      <div class="fx-ctl">
        <label for="fx-0">item A</label><select id="fx-0"></select>
        <label for="fx-1">item B</label><select id="fx-1"></select>
        <label for="fx-2">item C</label><select id="fx-2"></select>
      </div>
    </div>
    <div class="stage-col">
      <div class="fx-wrap"><div class="fx-row" id="fx-row"></div></div>
      <p class="verdict" id="fx-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += ST("Read", "Horizontal and vertical alignment") + prose("""
    <p>You've already met the two container properties in the playground above:</p>
    <ul>
      <li><code>align-items</code> lines items up on the <strong>cross axis</strong>. The default, <code>stretch</code> (its keyword is <code>normal</code>), makes every item as tall as the tallest, which is how flexbox gives you equal-height columns. <code>flex-start</code>, <code>center</code>, <code>flex-end</code> and <code>baseline</code> keep each item's own height.</li>
      <li><code>justify-content</code> spaces items along the <strong>main axis</strong>: <code>flex-start</code>, <code>center</code>, <code>flex-end</code>, <code>space-between</code> (no space at the ends), <code>space-around</code> (half-size space at the ends) and <code>space-evenly</code>.</li>
    </ul>
    <p>To align just one item differently, put <code>align-self</code> on it. It takes the same values as <code>align-items</code>. (There's no <code>justify-self</code> in flexbox: a single item's main-axis position comes from the free space, so use <code>margin-left: auto</code> to push one item to the end.)</p>
    <pre class="snippet" data-lang="css">.row { display: flex; align-items: center; }
.row .tall { align-self: stretch; }</pre>""")
b += ST("Read", "Ordering flex items") + prose("""
    <p>The <code>order</code> property changes where an item appears without changing the HTML. Every item starts at <code>order: 0</code>. Items with lower values come first; items with the same value keep their source order. Negative numbers work too, so <code>order: -1</code> moves an item to the front.</p>
    <p>Use it sparingly. <code>order</code> only changes what people see: keyboard users still tab through the items in source order, and screen readers still read them in source order. If the order matters, change the HTML.</p>""")
b += ST("Play", "align-self and order", "Set an order and alignment for each item, then click the first item and press Tab to see which order the keyboard uses.") + """  <section class="playground">
    <div class="panel controls">
      <table class="ao-tbl"><thead><tr><th></th><th>order</th><th>align-self</th></tr></thead><tbody id="ao-ctl"></tbody></table>
      <pre class="snippet" id="ao-code"></pre>
    </div>
    <div class="stage-col">
      <div class="ao-row" id="ao-row">
        <button class="ao-it" type="button">1</button><button class="ao-it" type="button">2</button><button class="ao-it" type="button">3</button><button class="ao-it" type="button">4</button>
      </div>
      <p class="verdict" id="ao-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += ST("Practice", "Sizing, order and alignment", "A sidebar that keeps its width, a main column and an extra panel that share the rest, in a different visual order.") + '  <div id="ex-flex"></div>\n\n'
b += ST("Read", "Nested flex boxes") + prose("""
    <p>A flex item can be a flex container too. That's how most real layouts are built: a header is a flex row (logo on one side, nav on the other), and the nav inside it is another flex row of links.</p>
    <pre class="snippet" data-lang="css">.site-nav { display: flex; justify-content: space-between; align-items: center; }
.site-nav ul { display: flex; gap: 16px; }</pre>
    <p>Each container only lays out its own direct children, so you can mix rows, columns and wrapping at every level.</p>
    <div class="callout note"><p class="callout-title">Note</p><p>Flexbox handles one direction at a time. For rows and columns that line up together, use <a href="core-grid.html">Grid</a>. <a href="core-flex-or-grid.html">Flexbox or Grid?</a> builds the same layouts both ways.</p></div>""")
b += ST("Practice", "Build a nav bar", "Most site headers are a flex row inside a flex row. Try it on a real nav.") + '  <div id="ex-nav"></div>\n\n'
b += notes([
  "<code>display: flex</code> goes on the parent; its direct children become flex items.",
  "<code>justify-content</code> works along the <strong>main axis</strong>, set by <code>flex-direction</code>; <code>align-items</code> works along the <strong>cross axis</strong>.",
  "Items don't wrap unless you add <code>flex-wrap: wrap</code>. <code>flex-flow</code> sets direction and wrap together.",
  "<code>flex: 1</code> shares out spare space; <code>flex: 1 200px</code> starts at 200px first. <code>flex</code> is shorthand for grow, shrink and basis.",
  "<code>align-self</code> aligns one item; <code>order</code> moves it visually but not for the keyboard.",
], [
  "Putting <code>display: flex</code> on the items instead of their parent.",
  "Expecting <code>align-items: center</code> to center vertically when the container has no extra height.",
  "Forgetting <code>flex-wrap: wrap</code>, so items squish instead of moving to a new line.",
  "Using <code>order</code> to fix content that's in the wrong order in the HTML.",
])
first = src.first_script()
js = r'''
  // --- Share out the space ---
  const FX = ["0 1 auto", "1", "2", "1 200px", "none"];
  const FXN = { "0 1 auto": "0 1 auto (initial)", "1": "1", "2": "2", "1 200px": "1 200px", "none": "none" };
  const FXT = ["Map", "Trail notes and photos", "Gear"];
  ["fx-0", "fx-1", "fx-2"].forEach((id, i) => { $(id).innerHTML = FX.map((v) => `<option value="${v}">${FXN[v]}</option>`).join(""); $(id).value = ["1", "1", "2"][i]; });
  function fxUpdate() {
    const w = +$("fx-w").value, row = $("fx-row");
    $("fx-w-out").textContent = w + "px"; row.style.width = w + "px";
    const vals = [0, 1, 2].map((i) => $("fx-" + i).value);
    row.innerHTML = vals.map((v, i) => `<div class="fx-it" style="flex:${v}"><span>${"ABC"[i]} · ${FXT[i]}</span><small>flex: ${v}</small><small class="m"></small></div>`).join("");
    requestAnimationFrame(() => {
      const its = [...row.children], ws = its.map((el) => Math.round(el.getBoundingClientRect().width));
      its.forEach((el, i) => { el.querySelector(".m").textContent = ws[i] + "px"; });
      const grows = vals.map((v) => ({ "0 1 auto": 0, none: 0, "1 200px": 1 })[v] ?? +v), total = grows.reduce((a, c) => a + c, 0);
      let msg = total ? `Spare space is split into ${total} share${total > 1 ? "s" : ""}: ` + vals.map((v, i) => `${"ABC"[i]} gets ${grows[i]}`).join(", ") + "." : "No item grows, so the spare space stays empty at the end of the row.";
      if (vals.includes("1 200px")) msg += " The 1 200px item starts at 200px before sharing.";
      if (vals.includes("none")) msg += " flex: none keeps an item at its content size: it won't grow or shrink.";
      $("fx-out").textContent = msg;
    });
  }
  ["fx-w", "fx-0", "fx-1", "fx-2"].forEach((id) => $(id).addEventListener("input", fxUpdate));
  fxUpdate();

  // --- align-self and order ---
  const AO_SELF = ["auto", "flex-start", "center", "flex-end", "stretch"];
  $("ao-ctl").innerHTML = [1, 2, 3, 4].map((n) => `<tr><th>item ${n}</th><td><select id="ao-o${n}" aria-label="order for item ${n}">${[-1, 0, 1, 2].map((o) => `<option${o === 0 ? " selected" : ""}>${o}</option>`).join("")}</select></td><td><select id="ao-s${n}" aria-label="align-self for item ${n}">${AO_SELF.map((s) => `<option>${s}</option>`).join("")}</select></td></tr>`).join("");
  const AO_H = [50, 80, 60, 100];
  function aoUpdate() {
    const its = [...$("ao-row").children], rules = [];
    its.forEach((el, i) => {
      const n = i + 1, o = +$("ao-o" + n).value, s = $("ao-s" + n).value;
      el.style.order = o; el.style.alignSelf = s;
      el.style.height = s === "stretch" ? "" : AO_H[i] + "px";
      if (o !== 0 || s !== "auto") rules.push(`.item-${n} {${o !== 0 ? ` order: ${o};` : ""}${s !== "auto" ? ` align-self: ${s};` : ""} }`);
    });
    $("ao-row").style.alignItems = "flex-start";
    $("ao-code").textContent = ".row {\n  display: flex;\n  align-items: flex-start;\n}\n" + (rules.map((r) => r.replace("{ ", "{\n  ").replace("; a", ";\n  a").replace("; }", ";\n}")).join("\n") || "/* every item:\n   order: 0;\n   align-self: auto; */");
    const visual = its.map((el, i) => ({ n: i + 1, x: el.getBoundingClientRect().left })).sort((a, c) => a.x - c.x).map((v) => v.n);
    $("ao-out").textContent = `On screen: ${visual.join(", ")}. Tab order: 1, 2, 3, 4 (source order).` + (visual.join() !== "1,2,3,4" ? " They no longer match, which is confusing for keyboard users." : "");
  }
  $("ao-ctl").addEventListener("input", aoUpdate);
  aoUpdate();
'''
ex_nav = src.block('  makeExercise(document.getElementById("ex-nav"), {')
ex_flex = r'''  makeExercise(document.getElementById("ex-flex"), {
    title: "A three-panel row",
    task: `<ol>
      <li>Make <code>.row</code> a flex container.</li>
      <li>Keep <code>.side</code> exactly 150px wide: it should never grow or shrink.</li>
      <li>Share the rest between <code>.main</code> and <code>.extra</code>, with <code>.main</code> getting twice as much as <code>.extra</code>.</li>
      <li>Show <code>.extra</code> first in the row, without changing the HTML.</li>
      <li>Stop <code>.side</code> stretching: align it to the top of the row.</li>
    </ol>`,
    html: `<div class="row">
  <nav class="side">Trails<br>Maps</nav>
  <main class="main"><h2>Royal Arch</h2><p>A steep climb through ponderosa pine to a sandstone arch. The last section has over 200 stone steps.</p></main>
  <aside class="extra">Weather: clear</aside>
</div>`,
    css: `body { font-family: system-ui, sans-serif; margin: 8px; }
.row { gap: 10px; }
.side { background: #b9c4ef; padding: 8px; }
.main { background: #eef1fb; padding: 8px; }
.extra { background: #ffe7a8; padding: 8px; }
h2 { margin-top: 0; }`,
    solution: { css: `body { font-family: system-ui, sans-serif; margin: 8px; }
.row { display: flex; gap: 10px; }
.side { background: #b9c4ef; padding: 8px; flex: 0 0 150px; align-self: flex-start; }
.main { background: #eef1fb; padding: 8px; flex: 2; }
.extra { background: #ffe7a8; padding: 8px; flex: 1; order: -1; }
h2 { margin-top: 0; }` },
    hints: [
      "flex: 0 0 150px means don't grow, don't shrink, start at 150px.",
      "flex: 2 and flex: 1 split the leftover space into three shares.",
      "Every item starts at order: 0, so order: -1 moves one to the front. align-self: flex-start stops one item stretching.",
    ],
    checks: [
      { label: ".row is a flex container", test: ({ style }) => style(".row", "display") === "flex" },
      { label: ".side is 150px and doesn't grow or shrink", test: ({ style }) => style(".side", "flex-grow") === "0" && style(".side", "flex-shrink") === "0" && style(".side", "flex-basis") === "150px" },
      { label: ".main gets twice as much space as .extra", test: ({ style }) => +style(".main", "flex-grow") === 2 * +style(".extra", "flex-grow") && +style(".extra", "flex-grow") > 0 && style(".main", "flex-basis") === style(".extra", "flex-basis") },
      { label: ".extra appears first", test: ({ $ }) => $(".extra").getBoundingClientRect().left < $(".side").getBoundingClientRect().left },
      { label: ".side is aligned to the top and doesn't stretch", test: ({ $ }) => { const s = $(".side").getBoundingClientRect(), r = $(".row").getBoundingClientRect(); return Math.abs(s.top - r.top) < 1 && s.height < r.height - 10; } },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q6", q: "Three items have flex: 1, flex: 1 and flex: 2. What share of the spare space does the third get?", opts: ["A third", "Half", "Two thirds"], a: 1, why: "That's 4 shares in total, and the third item gets 2 of them." },
    { id: "q7", q: "You move a button to the front with order: -1. What happens when a keyboard user presses Tab?", opts: ["Focus follows the visual order", "Focus still follows the HTML source order", "The button can't be focused"], a: 1, why: "order only changes what's drawn. Tab order and screen readers follow the source." },
  ]);
''')
write("core-flexbox.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_flex + "\n" + ex_nav + "\n" + quiz + "</script>\n")
