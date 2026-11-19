import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("transforms")
pg = src.between('  <section class="playground">\n    <div class="panel controls" aria-label="Transform settings">', '  <div class="section-title"><span class="eyebrow">Order matters</span>')
order = src.between('  <section class="order">', '  <div class="section-title"><span class="eyebrow">In real sites</span>')
uses = src.between('  <section class="uses">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Transforms", src.css(), """
  .ip-stage { display: flex; gap: 24px; justify-content: center; align-items: center; padding: 30px; background: var(--stage); border-radius: 8px; min-height: 170px; }
  .ip-card { width: 110px; height: 80px; border-radius: 8px; background: #0b6b5e; color: #fff; display: grid; place-items: center; font: 700 0.9rem system-ui, sans-serif; transition: 0.3s; }
  .p3-scene { height: 230px; display: grid; place-items: center; background: var(--stage); border-radius: 8px; }
  .p3-card { width: 150px; height: 110px; border-radius: 10px; background: linear-gradient(135deg, #2340d9, #0b6b5e); color: #fff; display: grid; place-items: center; font: 800 1.1rem system-ui, sans-serif; box-shadow: 0 6px 18px rgb(0 0 0 / 25%); }
""")
b = top("Transforms", "Transforms move, turn, resize and slant an element after the page is laid out, without nudging anything around it. That makes them ideal for hover effects, icons and small bits of motion.", [
  "Use <code>translate</code>, <code>rotate</code>, <code>scale</code> and <code>skew</code>, as functions and as individual properties.",
  "Explain why transforms don't affect layout, and why the order of functions matters.",
  "Move the pivot point with <code>transform-origin</code>.",
  "Add depth to a 3D transform with <code>perspective</code>."])
b += ST("Read", "CSS transforms properties") + prose("""
    <p>The <code>transform</code> property takes one or more functions, separated by spaces:</p>
    <pre class="snippet" data-lang="css">.badge {
  transform: translateY(-4px) rotate(-3deg) scale(1.1);
}</pre>
    <ul>
      <li><code>translate()</code> moves it (<code>translateX()</code>, <code>translateY()</code>).</li>
      <li><code>rotate()</code> turns it, in <code>deg</code> or <code>turn</code>. A number with no unit does nothing.</li>
      <li><code>scale()</code> resizes it: 1 is normal size, 2 double, 0.5 half.</li>
      <li><code>skew()</code> slants it (<code>skewX()</code>, <code>skewY()</code>).</li>
    </ul>
    <p>Transforms are drawn after layout, so the browser keeps the element's original space and <strong>nothing around it moves</strong>. A card can grow on hover without shoving its neighbours.</p>
    <p><code>transform-origin</code> sets the point the element turns and scales around. The default is the centre; <code>transform-origin: top left</code> makes it pivot from the corner, like a door on a hinge.</p>""")
b += ST("Play", "Transform a card", "Drag the sliders and watch the dashed outline: that's the space the card still takes up in the layout.") + pg
b += prose("""
    <h3>Individual transform properties</h3>
    <p>There are also separate <code>translate</code>, <code>rotate</code> and <code>scale</code> <em>properties</em>. They're easier to read, and they don't replace each other. With the <code>transform</code> property, a hover rule that sets <code>transform: scale(1.1)</code> wipes out an earlier <code>rotate(-3deg)</code>. With separate properties, <code>scale: 1.1</code> just adds to <code>rotate: -3deg</code>.</p>
    <pre class="snippet" data-lang="css">.stamp { rotate: -3deg; }
.stamp:hover { scale: 1.1; }   /* still rotated */</pre>""")
b += ST("Play", "transform vs individual properties", "Both cards start tilted. Turn on the hover state.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <label class="toggle"><input type="checkbox" id="ip-hover"> apply the <code>:hover</code> rule</label>
      <pre class="snippet" id="ip-code"></pre>
    </div>
    <div class="ip-stage"><div><div class="ip-card" id="ip-a">transform</div></div><div><div class="ip-card" id="ip-b">rotate + scale</div></div></div>
  </section>

"""
b += ST("Read", "Examples") + prose("""
    <h3>Rotating</h3>
    <p><code>rotate: 90deg; transform-origin: bottom left;</code> swings an element a quarter-turn around its bottom-left corner instead of its centre.</p>
    <h3>Skewing and translating</h3>
    <p>When you combine functions, order matters. Each function works in the space left by the ones before it: rotate first, and "right" now points diagonally, so a following <code>translateX()</code> moves the element diagonally too.</p>""")
b += ST("Play", "Same functions, different order", "Transform functions apply from right to left, and each one changes the direction the next one uses.") + order + "\n"
b += ST("Look", "Four everyday uses") + uses
b += ST("Practice", "Transform without moving the layout", "Tilt a stamp, lift a card on hover, and swing a door from its edge.") + '  <div id="ex-transform"></div>\n\n'
b += ST("Read", "3D specific CSS properties") + prose("""
    <p>Transforms also work in three dimensions: <code>rotateX()</code> and <code>rotateY()</code> tip an element towards or away from you, and <code>translateZ()</code> moves it nearer. Without perspective, though, 3D looks flat.</p>
    <h3>Perspective</h3>
    <p>Set <code>perspective</code> on the <strong>parent</strong>: the distance between the viewer and the page. A small value (250px) is like holding your face close, with dramatic distortion; a large one (1000px) is subtle. <code>perspective-origin</code> moves the viewer's eye: <code>left</code>, <code>top right</code> and so on.</p>
    <pre class="snippet" data-lang="css">.scene { perspective: 600px; }
.card  { transform: rotateY(40deg); }</pre>""")
b += ST("Play", "Perspective", "Turn the card in 3D, then change how close the viewer is.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="control"><label for="p3-rot">rotateY</label><input id="p3-rot" type="range" min="-80" max="80" step="5" value="40"><span class="readout" id="p3-rot-out"></span></div>
      <div class="control"><label for="p3-per">perspective (on the parent)</label><input id="p3-per" type="range" min="150" max="1500" step="50" value="600"><span class="readout" id="p3-per-out"></span></div>
      <div class="control"><label for="p3-org">perspective-origin</label><select id="p3-org"><option>center</option><option>left</option><option>right</option><option>top</option><option>bottom right</option></select></div>
      <label class="toggle"><input type="checkbox" id="p3-none"> remove perspective</label>
      <pre class="snippet" id="p3-code"></pre>
    </div>
    <div class="p3-scene" id="p3-scene"><div class="p3-card" id="p3-card">Trail pass</div></div>
  </section>

"""
b += ST("Practice", "Individual properties and 3D", "A tilted badge that grows, and a card turned in 3D.") + '  <div id="ex-3d"></div>\n\n'
b += notes([
  "Transforms change how an element is drawn, not the space it takes.",
  "Functions in one <code>transform</code> apply right to left, and order changes the result.",
  "A second <code>transform</code> replaces the first; the individual <code>rotate</code>, <code>scale</code> and <code>translate</code> properties combine.",
  "<code>transform-origin</code> moves the pivot point.",
  "3D needs <code>perspective</code> on the parent.",
], [
  "<code>rotate(45)</code> with no unit.",
  "Overriding a rotation by setting <code>transform: scale()</code> on hover.",
  "Using transforms to build layout: the space doesn't move with the element.",
  "Putting <code>perspective</code> on the element being rotated instead of its parent.",
])
first = src.first_script()
js = r'''
  // --- transform vs individual properties ---
  function ip() {
    const on = $("ip-hover").checked;
    $("ip-a").style.transform = on ? "scale(1.25)" : "rotate(-8deg)";
    $("ip-b").style.rotate = "-8deg"; $("ip-b").style.scale = on ? "1.25" : "1";
    $("ip-code").textContent = `.a { transform: rotate(-8deg); }\n.a:hover { transform: scale(1.25); }  /* rotation lost */\n\n.b { rotate: -8deg; }\n.b:hover { scale: 1.25; }  /* still tilted */`;
  }
  $("ip-hover").addEventListener("change", ip);
  ip();

  // --- Perspective ---
  function p3() {
    const r = $("p3-rot").value, p = $("p3-per").value, o = $("p3-org").value, none = $("p3-none").checked;
    $("p3-card").style.transform = `rotateY(${r}deg)`;
    $("p3-scene").style.perspective = none ? "none" : p + "px";
    $("p3-scene").style.perspectiveOrigin = o;
    $("p3-rot-out").textContent = r + "deg"; $("p3-per-out").textContent = p + "px";
    $("p3-code").textContent = `.scene {\n  perspective: ${none ? "none" : p + "px"};\n  perspective-origin: ${o};\n}\n.card {\n  transform: rotateY(${r}deg);\n}`;
  }
  ["p3-rot", "p3-per", "p3-org", "p3-none"].forEach((id) => $(id).addEventListener("input", p3));
  p3();
'''
ex_t = src.block('  makeExercise(document.getElementById("ex-transform"), {')
ex_3 = r'''  makeExercise(document.getElementById("ex-3d"), {
    title: "Badge and pass",
    task: `<ol>
      <li>Tilt <code>.badge</code> with the <code>rotate</code> property: <code>-6deg</code>.</li>
      <li>Make <code>.badge.big</code> larger with the <code>scale</code> property: <code>1.4</code>. It should stay tilted.</li>
      <li>Give <code>.scene</code> <code>perspective: 600px</code>, and turn <code>.pass</code> with <code>transform: rotateY(35deg)</code>.</li>
    </ol>`,
    html: `<p><span class="badge">New</span> <span class="badge big">Hot</span></p>
<div class="scene"><div class="pass">Trail pass</div></div>`,
    css: `body { font-family: system-ui, sans-serif; padding: 20px; }
.badge { display: inline-block; background: #b4410c; color: white; padding: 4px 10px; border-radius: 4px; }
.scene { padding: 20px; }
.pass { width: 160px; height: 100px; display: grid; place-items: center; background: #2340d9; color: white; border-radius: 10px; }
`,
    solution: { css: `body { font-family: system-ui, sans-serif; padding: 20px; }
.badge { display: inline-block; background: #b4410c; color: white; padding: 4px 10px; border-radius: 4px; rotate: -6deg; }
.badge.big { scale: 1.4; }
.scene { padding: 20px; perspective: 600px; }
.pass { width: 160px; height: 100px; display: grid; place-items: center; background: #2340d9; color: white; border-radius: 10px; transform: rotateY(35deg); }
` },
    hints: ["rotate and scale here are properties, not functions: rotate: -6deg;", "perspective goes on the parent (.scene)."],
    checks: [
      { label: "Both badges are rotated -6deg", test: ({ $$, style }) => $$(".badge").every((b) => style(b, "rotate") === "-6deg") },
      { label: "The big badge is scaled 1.4", test: ({ style }) => style(".badge.big", "scale") === "1.4" },
      { label: ".scene has perspective: 600px", test: ({ style }) => style(".scene", "perspective") === "600px" },
      { label: ".pass is turned with rotateY(35deg)", test: ({ style }) => { const m = style(".pass", "transform").match(/matrix3d\(([^)]+)\)/); return !!m && Math.abs(parseFloat(m[1].split(",")[0]) - Math.cos(35 * Math.PI / 180)) < 0.01; } },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: ".stamp { rotate: -3deg } .stamp:hover { scale: 1.1 }. On hover, the stamp is…", opts: ["Rotated and scaled", "Only scaled", "Only rotated"], a: 0, why: "The individual properties combine instead of replacing each other." },
    { id: "q6", q: "Where do you put perspective for a 3D-rotated card?", opts: ["On its parent", "On the card", "On the body only"], a: 0, why: "perspective sets the viewer's distance for the parent's children." },
  ]);
''')
write("core-transforms.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_t + "\n" + ex_3 + "\n" + quiz + "</script>\n")
