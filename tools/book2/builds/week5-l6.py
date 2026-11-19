import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("positioning")
pg = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">#box</span>', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Positioning", src.css(), """
  .zi-stage { position: relative; height: 230px; background: var(--stage); border-radius: 8px; }
  .zi-card { position: absolute; width: 150px; height: 100px; border-radius: 8px; color: #fff; padding: 8px; font: 700 0.85rem var(--font-code); font-variation-settings: "MONO" 1; box-shadow: 0 4px 12px rgb(0 0 0 / 25%); }
  .zi-card small { display: block; font-weight: 400; }
  #zi-a { top: 20px; left: 20px; background: var(--item-1); } #zi-b { top: 60px; left: 90px; background: var(--item-2); } #zi-c { top: 100px; left: 160px; background: var(--item-3); }
  .st-box { height: 230px; overflow-y: auto; border: 2px solid var(--line); border-radius: 8px; background: #fff; color: #1d2133; }
  .st-box dl { margin: 0; }
  .st-box dt { background: #2340d9; color: #fff; font: 700 0.9rem var(--font-code); padding: 4px 10px; }
  .st-box dd { margin: 0; padding: 6px 10px; border-bottom: 1px solid #e3e6ef; font-size: 0.9rem; }
  .tb-box { width: 100%; max-width: 420px; border: 2px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; color: #1d2133; }
  .tb-list { display: flex; background: #1d2a3a; }
  .tb-list button { flex: 1; border: 0; background: transparent; color: #fff; font: 600 0.9rem system-ui, sans-serif; padding: 0 1rem; line-height: 2.6rem; cursor: pointer; }
  .tb-list button[aria-selected="true"] { background: #fff; color: #1d2133; }
  .tb-panels { position: relative; height: 150px; }
  .tb-panels [role="tabpanel"] { position: absolute; top: 0; left: 0; width: 100%; height: 100%; padding: 12px; box-sizing: border-box; background: #fff; }
  .tb-panels [role="tabpanel"] h4 { margin: 0 0 6px; }
  .tb-panels [role="tabpanel"] p { margin: 0; font-size: 0.9rem; }
  .tb-panels.fan [role="tabpanel"] { opacity: 0.85; border: 2px dashed #2340d9; }
  .tb-panels.fan [role="tabpanel"]:nth-child(2) { transform: translate(14px, 14px); } .tb-panels.fan [role="tabpanel"]:nth-child(3) { transform: translate(28px, 28px); }
  .is-hidden { display: none; }
  .sp-frame { position: relative; height: 240px; overflow: clip; border: 2px solid var(--line); border-radius: 8px; background: #fff; color: #1d2133; padding: 12px 70px 12px 12px; }
  .sp-frame p { margin: 0 0 8px; font-size: 0.9rem; }
  .sp-btn { position: absolute; top: 8px; right: 8px; z-index: 1; border: 0; background: #2340d9; color: #fff; border-radius: 6px; padding: 6px 10px; cursor: pointer; font: 600 0.85rem system-ui, sans-serif; }
  .sp-panel { position: absolute; top: 0; right: -220px; width: 200px; height: 100%; box-sizing: border-box; padding: 44px 12px 12px; background: #1d2a3a; color: #fff; transition: right 0.6s ease-out; font-size: 0.9rem; }
  .sp-panel.open { right: 0; }
""")
b = top("Positioning", "The <code>position</code> property takes an element out of the normal flow and puts it somewhere else: nudged a little, pinned to a corner of its card, stuck to the window, or stuck to the top while you scroll.", [
  "Explain what static, relative, absolute, fixed and sticky are each positioned against.",
  "Place an element inside a positioning context with <code>position: relative</code> and <code>absolute</code>.",
  "Control which overlapping element is on top with <code>z-index</code>.",
  "Build sticky headers, stacked tab panels and a sliding panel.",
])
b += ST("Read", "Introducing positioning") + prose("""
    <p>Normally every element sits where the <span class="term">normal flow</span> puts it, one after another. The <span class="term">position</span> property lets you move an element from there, for things that normal flow, Flexbox and Grid can't do: a badge over the corner of a photo, a header that stays at the top of the window, a menu that slides in over the page.</p>
    <p>Once an element is positioned, the offset properties <code>top</code>, <code>right</code>, <code>bottom</code> and <code>left</code> move it. The question each <code>position</code> value answers is: measured from where? Try them all first, then we'll go through each one.</p>""")
b += ST("Play", "Try every position value", "Change the position value and offsets, then scroll inside the window to see how each one behaves.") + pg
b += ST("Read", "Static positioning") + prose("""
    <p><code>position: static</code> is the default. The element sits in the normal flow, and <code>top</code>, <code>left</code> and <code>z-index</code> have no effect. You'll rarely write it, except to undo another position value.</p>""")
b += ST("Read", "Relative positioning") + prose("""
    <p><code>position: relative</code> keeps the element in the normal flow, then lets you nudge it from there. Its original space stays reserved, so nothing around it moves; the element can end up overlapping its neighbours.</p>
    <h3>Introducing top, bottom, left, and right</h3>
    <p>The offsets can feel backwards. <code>top: 30px</code> pushes the element 30px <em>away from</em> its top edge, so it moves down. <code>left: 30px</code> moves it right. To move up or left, use <code>bottom</code> and <code>right</code>, or a negative value.</p>
    <pre class="snippet" data-lang="css">.positioned {
  position: relative;
  top: 30px;    /* 30px down */
  left: 30px;   /* 30px right */
}</pre>
    <p>On its own, relative positioning is mostly used for small nudges. Its big job is the next one: being the reference point for absolutely positioned children.</p>""")
b += ST("Read", "Absolute positioning") + prose("""
    <h3>Setting position: absolute</h3>
    <p><code>position: absolute</code> takes the element out of the normal flow completely. It no longer takes up space: the elements after it close up as if it weren't there. It still has its own margins, but they don't collapse with anything.</p>
    <h3>Positioning contexts</h3>
    <p>An absolute element's offsets are measured from its <strong>containing block</strong>: the nearest ancestor that is itself positioned (anything but <code>static</code>). If there isn't one, it's the <em>initial containing block</em>, roughly the size of the window at the top of the page.</p>
    <p>That's why you'll see this pattern everywhere. To pin a badge to a card's corner, make the card the positioning context:</p>
    <pre class="snippet" data-lang="css">.card { position: relative; }   /* the context */
.card .badge {
  position: absolute;
  top: 8px;
  right: 8px;
}</pre>
    <p>Without <code>position: relative</code> on the card, the badge looks for the next positioned ancestor up the page and often ends up in the corner of the whole page.</p>""")
b += ST("Practice", "Pin a badge to a card", "Place a badge in each card's corner, so it stays put whatever the card's size.") + '  <div id="ex-badge"></div>\n\n'
b += prose("""
    <h3>Introducing z-index</h3>
    <p>Positioned elements can overlap. By default, the one that comes later in the HTML is drawn on top. <span class="term">z-index</span> changes that: higher numbers come forward. It takes whole numbers with no unit, including negatives; the default, <code>auto</code>, acts like 0.</p>
    <p><code>z-index</code> only works on positioned elements (and on flex and grid items). On a static element it does nothing.</p>""")
b += ST("Play", "Which card is on top?", "Three overlapping, absolutely positioned cards. Give them z-index values.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="zi-za">card A z-index</label><select id="zi-za"><option>auto</option><option>0</option><option>1</option><option>2</option><option>3</option><option>-1</option></select></div>
      <div class="control"><label for="zi-zb">card B z-index</label><select id="zi-zb"><option>auto</option><option>0</option><option>1</option><option>2</option><option>3</option><option>-1</option></select></div>
      <div class="control"><label for="zi-zc">card C z-index</label><select id="zi-zc"><option>auto</option><option>0</option><option>1</option><option>2</option><option>3</option><option>-1</option></select></div>
    </div>
    <div class="stage-col">
      <div class="zi-stage"><div class="zi-card" id="zi-a">A<small></small></div><div class="zi-card" id="zi-b">B<small></small></div><div class="zi-card" id="zi-c">C<small></small></div></div>
      <p class="verdict" id="zi-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += ST("Read", "Fixed positioning") + prose("""
    <p><code>position: fixed</code> works like absolute, but it's positioned against the <strong>viewport</strong> (the browser window), not an ancestor. It stays in the same place on screen while the page scrolls under it. That's how headers, chat buttons and cookie banners stay visible.</p>
    <pre class="snippet" data-lang="css">.site-header {
  position: fixed;
  top: 0;
  width: 100%;
}
main { margin-top: 60px; }   /* so the header doesn't cover the start of the page */</pre>
    <p>Because a fixed element is out of the flow, the content underneath doesn't know it's there. Leave room for it, or it will cover the top of your page.</p>""")
b += ST("Read", "Sticky positioning") + prose("""
    <h3>Basic example</h3>
    <p><code>position: sticky</code> is a mix of relative and fixed. The element scrolls with the page normally until it reaches its offset, then it sticks there, until its parent scrolls out of view and takes it away.</p>
    <pre class="snippet" data-lang="css">.positioned {
  position: sticky;
  top: 30px;   /* stick when 30px from the top */
}</pre>
    <p>Sticky needs an offset like <code>top</code>; without one it never sticks.</p>
    <h3>Scrolling index</h3>
    <p>A classic use is an alphabetical list where each letter heading sticks at the top until the next letter pushes it away. Each heading only sticks inside its own section. Sticky also works inside any scrolling box, not just the page: the element sticks to the nearest ancestor that scrolls.</p>""")
b += ST("Play", "A sticky index", "Scroll the list. Then turn sticky off, or change the offset.") + """  <section class="playground">
    <div class="panel controls">
      <label class="toggle"><input type="checkbox" id="st-on" checked> <code>dt { position: sticky; }</code></label>
      <div class="control"><label for="st-top">top</label><select id="st-top"><option>0px</option><option>20px</option><option value="auto">auto (no offset)</option></select></div>
      <p class="hint" id="st-out" aria-live="polite"></p>
    </div>
    <div class="st-box" id="st-box"><dl id="st-dl"></dl></div>
  </section>

"""
b += ST("Practice", "A sticky bar that stays on top", "Make the bar stick, then fix the cards that scroll over it.") + '  <div id="ex-sticky"></div>\n\n'
b += ST("Read", "Practical positioning examples") + prose("""
    <h3>A tabbed info-box</h3>
    <p>A tabbed box shows one panel at a time. A neat way to build it: give the panels' wrapper <code>position: relative</code>, and stack every panel inside it with <code>position: absolute; top: 0; left: 0</code>. They all occupy the same spot, and a small script hides all but the selected one (with a class like <code>.is-hidden { display: none; }</code>) and sets <code>aria-selected</code> on the tabs.</p>""")
b += ST("Play", "Stacked tab panels", "Click the tabs. Then show the hidden panels to see them stacked in the same place.") + """  <section class="playground">
    <div class="panel controls">
      <label class="toggle"><input type="checkbox" id="tb-show"> show the hidden panels (fanned out)</label>
      <p class="hint">Every panel is <code>position: absolute; top: 0; left: 0</code> inside <code>.panels { position: relative; }</code>.</p>
    </div>
    <div class="tb-box">
      <div class="tb-list" role="tablist" aria-label="Trail info" id="tb-list">
        <button role="tab" id="tb-t1" aria-selected="true" aria-controls="tb-p1">Route</button>
        <button role="tab" id="tb-t2" aria-selected="false" aria-controls="tb-p2" tabindex="-1">Weather</button>
        <button role="tab" id="tb-t3" aria-selected="false" aria-controls="tb-p3" tabindex="-1">Parking</button>
      </div>
      <div class="tb-panels" id="tb-panels">
        <div role="tabpanel" id="tb-p1" aria-labelledby="tb-t1"><h4>Route</h4><p>1.7 miles from Chautauqua, climbing 1,400 feet. The last section has over 200 stone steps.</p></div>
        <div role="tabpanel" id="tb-p2" aria-labelledby="tb-t2" class="is-hidden"><h4>Weather</h4><p>Clear in the morning. Afternoon storms are common in summer, so start early.</p></div>
        <div role="tabpanel" id="tb-p3" aria-labelledby="tb-t3" class="is-hidden"><h4>Parking</h4><p>Chautauqua's lot fills by 8am on weekends. Take the free Park to Park shuttle.</p></div>
      </div>
    </div>
  </section>

"""
b += prose("""
    <h3>A fixed position tabbed info-box</h3>
    <p>Change the box to <code>position: fixed; top: 0</code> and it stays on screen while the rest of the page scrolls past. The page content then needs a margin on that side (for example <code>margin-left</code> as wide as the box) so it isn't hidden underneath.</p>
    <h3>A sliding hidden panel</h3>
    <p>A panel can wait just off-screen and slide in when you need it. Give it <code>position: fixed</code> and a negative <code>right</code> equal to its width, so it's hidden past the edge of the window. A class like <code>.open { right: 0; }</code> brings it back, and a <code>transition</code> on <code>right</code> animates the move. The button that opens it is positioned too, with a <code>z-index</code> so it stays above the panel.</p>""")
b += ST("Play", "A sliding panel", "In this demo the panel is absolute inside the frame, standing in for fixed inside a window.") + """  <section class="playground">
    <div class="panel controls">
      <pre class="snippet">.panel {
  position: fixed;
  top: 0;
  right: -220px;
  width: 200px;
  height: 100%;
  transition: right 0.6s ease-out;
}
.panel.open { right: 0; }
.menu-btn {
  position: absolute;
  z-index: 1;
}</pre>
    </div>
    <div class="sp-frame">
      <button class="sp-btn" id="sp-btn" aria-expanded="false" aria-controls="sp-panel">Info</button>
      <p>Royal Arch is one of the most rewarding short hikes near Boulder.</p>
      <p>The trail climbs steeply through ponderosa pine forest, gaining about 1,400 feet in under two miles.</p>
      <p>Park at Chautauqua and follow the Bluebell Road to the trailhead.</p>
      <aside class="sp-panel" id="sp-panel"><strong>Trail info</strong><p>Open sunrise to sunset. Dogs on leash.</p></aside>
    </div>
  </section>

"""
b += notes([
  "<code>static</code> is the default: offsets and <code>z-index</code> do nothing.",
  "<code>relative</code> nudges the element; its original space stays reserved. <code>top: 30px</code> moves it <em>down</em>.",
  "<code>absolute</code> leaves the flow and is placed inside the nearest positioned ancestor, so put <code>position: relative</code> on the parent.",
  "<code>fixed</code> is placed against the viewport; <code>sticky</code> scrolls normally, then sticks at its offset inside its parent.",
  "<code>z-index</code> brings positioned elements forward; with equal values, later in the source is on top.",
], [
  "Using <code>absolute</code> without a positioned parent, so the element flies to the corner of the page.",
  "Building whole layouts with absolute positioning. Use Flexbox or Grid, and save positioning for overlays and badges.",
  "Setting <code>z-index</code> on a static element.",
  "Sticky that never sticks because there's no <code>top</code> value, or a parent has <code>overflow: hidden</code>.",
])
first = src.first_script()
js = r'''
  // --- z-index ---
  function ziUpdate() {
    const cards = ["a", "b", "c"].map((k, i) => ({ k: k.toUpperCase(), i, el: $("zi-" + k), z: $("zi-z" + k).value }));
    cards.forEach((c) => { c.el.style.zIndex = c.z; c.el.querySelector("small").textContent = "z-index: " + c.z; });
    const n = (z) => (z === "auto" ? 0 : +z);
    const order = [...cards].sort((x, y) => n(x.z) - n(y.z) || x.i - y.i).map((c) => c.k);
    const top = order[2], tie = cards.filter((c) => n(c.z) === n(cards.find((d) => d.k === top).z)).length > 1;
    $("zi-out").textContent = `Drawn bottom to top: ${order.join(", ")}. ${top} is on top` + (tie ? `: it shares the highest z-index, and comes latest in the HTML.` : ": it has the highest z-index.") + (cards.some((c) => n(c.z) < 0) ? " A negative z-index sends a card behind the others." : "");
  }
  ["zi-za", "zi-zb", "zi-zc"].forEach((id) => $(id).addEventListener("input", ziUpdate));
  ziUpdate();

  // --- sticky index ---
  const ST_DATA = { A: ["Anemone Hill", "Arapaho Ridge"], B: ["Bear Peak", "Bluebell Mesa", "Boulder Falls"], C: ["Chautauqua", "Crown Rock"], F: ["Flagstaff", "Fern Canyon"], G: ["Green Mountain", "Gregory Canyon"], M: ["Mallory Cave", "Mesa Trail"], R: ["Royal Arch", "Red Rocks"], S: ["Sanitas", "South Boulder Peak"] };
  $("st-dl").innerHTML = Object.entries(ST_DATA).map(([k, v]) => `<dt>${k}</dt>` + v.map((x) => `<dd>${x}</dd>`).join("")).join("");
  function stUpdate() {
    const on = $("st-on").checked, top = $("st-top").value;
    document.querySelectorAll("#st-dl dt").forEach((dt) => { dt.style.position = on ? "sticky" : ""; dt.style.top = top; });
    $("st-out").textContent = !on ? "Without sticky, the letters scroll away with their sections." : top === "auto" ? "position: sticky with no offset behaves like relative: it never sticks." : `Each letter sticks ${top} from the top of the scrolling box, and the next letter slides over it when it arrives. The box is the scrolling ancestor, so that's what they stick to, not the page.`;
  }
  ["st-on", "st-top"].forEach((id) => $(id).addEventListener("input", stUpdate));
  stUpdate();

  // --- tabs ---
  const tabs = [...document.querySelectorAll("#tb-list [role=tab]")];
  function tbSelect(t) {
    tabs.forEach((x) => { const on = x === t; x.setAttribute("aria-selected", String(on)); x.tabIndex = on ? 0 : -1; $(x.getAttribute("aria-controls")).classList.toggle("is-hidden", !on && !$("tb-show").checked); });
  }
  tabs.forEach((t) => t.addEventListener("click", () => tbSelect(t)));
  $("tb-list").addEventListener("keydown", (e) => {
    const i = tabs.indexOf(document.activeElement); if (i < 0) return;
    const j = e.key === "ArrowRight" ? (i + 1) % 3 : e.key === "ArrowLeft" ? (i + 2) % 3 : e.key === "Home" ? 0 : e.key === "End" ? 2 : -1;
    if (j >= 0) { e.preventDefault(); tabs[j].focus(); tbSelect(tabs[j]); }
  });
  $("tb-show").addEventListener("input", () => { $("tb-panels").classList.toggle("fan", $("tb-show").checked); tbSelect(tabs.find((t) => t.getAttribute("aria-selected") === "true")); });

  // --- sliding panel ---
  $("sp-btn").addEventListener("click", () => { const open = $("sp-panel").classList.toggle("open"); $("sp-btn").setAttribute("aria-expanded", String(open)); $("sp-btn").textContent = open ? "Close" : "Info"; });
'''
ex_b = src.block('  makeExercise(document.getElementById("ex-badge"), {')
ex_s = r'''  makeExercise(document.getElementById("ex-sticky"), {
    title: "Sticky trail list",
    task: `<ol>
      <li>Make <code>.bar</code> stick to the top of the scrolling list (<code>top: 0</code>).</li>
      <li>Scroll the list: the cards slide <em>over</em> the bar, because they're positioned too and come later in the HTML. Give the bar a <code>z-index</code> so it stays on top.</li>
    </ol>`,
    html: `<div class="scroller">
  <div class="bar">Boulder trails</div>
  <div class="card">Mesa <span class="badge">Easy</span></div>
  <div class="card">Royal Arch <span class="badge">Hard</span></div>
  <div class="card">Bear Peak <span class="badge">Hard</span></div>
  <div class="card">Sanitas <span class="badge">Moderate</span></div>
  <div class="card">Flagstaff <span class="badge">Moderate</span></div>
  <div class="card">Chautauqua <span class="badge">Easy</span></div>
</div>`,
    css: `body { font-family: system-ui, sans-serif; }
.scroller { height: 180px; overflow-y: auto; border: 2px solid #1d2a3a; }
.bar { background: #1d2a3a; color: white; padding: 10px; font-weight: 700; }
.card { position: relative; margin: 8px; padding: 14px 10px; background: #eef1fb; }
.badge { position: absolute; top: 6px; right: 6px; background: gold; padding: 2px 6px; font-size: 0.8rem; }`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.scroller { height: 180px; overflow-y: auto; border: 2px solid #1d2a3a; }
.bar { background: #1d2a3a; color: white; padding: 10px; font-weight: 700; position: sticky; top: 0; z-index: 1; }
.card { position: relative; margin: 8px; padding: 14px 10px; background: #eef1fb; }
.badge { position: absolute; top: 6px; right: 6px; background: gold; padding: 2px 6px; font-size: 0.8rem; }` },
    hints: [
      "position: sticky needs an offset: top: 0.",
      "The cards are position: relative, so they're drawn above earlier positioned elements with the same z-index. z-index: 1 on the bar lifts it above them.",
    ],
    checks: [
      { label: "The bar is sticky at top: 0", test: ({ style }) => style(".bar", "position") === "sticky" && style(".bar", "top") === "0px" },
      { label: "The bar stays at the top when the list scrolls", test: ({ $ }) => { const s = $(".scroller"); s.scrollTop = 150; const ok = Math.abs($(".bar").getBoundingClientRect().top - s.getBoundingClientRect().top - 2) < 1.5; s.scrollTop = 0; return ok; } },
      { label: "Cards scroll under the bar, not over it", test: ({ $, doc }) => { const s = $(".scroller"), sr = s.getBoundingClientRect(); let ok = true; for (const y of [30, 60, 90, 120, 150]) { s.scrollTop = y; const r = $(".bar").getBoundingClientRect(); for (const x of [r.left + 20, r.right - 20]) { const el = doc.elementFromPoint(x, r.top + r.height / 2); if (!el || !el.closest(".bar")) ok = false; } } s.scrollTop = 0; return ok && sr.height > 0; } },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "position: relative; top: 30px; moves an element which way?", opts: ["Up 30px", "Down 30px", "It doesn't move"], a: 1, why: "top pushes the element away from its top edge, so it moves down." },
    { id: "q6", q: "Two positioned elements overlap, both with z-index: auto. Which is on top?", opts: ["The one later in the HTML", "The one earlier in the HTML", "The bigger one"], a: 0, why: "With equal z-index, later elements in the source are drawn on top." },
    { id: "q7", q: "A sticky heading never sticks. What's the most likely cause?", opts: ["It has no top (or other) offset", "It has a background colour", "It's inside a dl"], a: 0, why: "Sticky needs an offset to know where to stick." },
  ]);
''')
write("core-positioning.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_b + "\n" + ex_s + "</script>\n")
