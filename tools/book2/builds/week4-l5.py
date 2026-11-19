import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("shadows")
bs = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="presets" id="presets">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>text-shadow')
ts = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="tb">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>box-shadow vs')
cmp = src.between('  <div class="compare">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Other filters')
flt = src.between('  <section class="playground filters">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Shadows and Effects", src.css(), """
  .bl-stage { position: relative; height: 220px; border-radius: 8px; overflow: hidden; border: 1px solid var(--line); background: #fff; }
  .bl-a { position: absolute; inset: 20px 30% 20px 20px; border-radius: 10px; background-color: #3fa66b; background-image: repeating-linear-gradient(45deg, #fff 0 12px, #1d2133 12px 24px); }
  .bl-b { position: absolute; inset: 60px 20px 40px 40%; border-radius: 50%; background: #8a3ffc; display: grid; place-items: center; color: #fff; font: 800 1.4rem system-ui, sans-serif; }
  .sh-stage { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 14px; font: 0.95rem/1.6 Georgia, serif; }
  .sh-stage .ball { float: left; width: 130px; height: 130px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #f0b37a, #b4410c); margin: 0 14px 6px 0; }
  .clip-h { font: 900 clamp(2rem, 7vw, 3.6rem)/1.1 system-ui, sans-serif; margin: 0; background-image: linear-gradient(90deg, #0b6b5e, #2340d9, #b4410c); }
  .clip-h.on { -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
""")
b = top("Shadows and Effects", "Shadows add depth, filters change how an element is drawn, and blend modes mix layers like a photo editor. Used lightly, they give a page polish; overdone, they make it hard to read.", [
  "Add soft, layered and inset box shadows, and text shadows that keep text readable.",
  "Apply filters like <code>blur()</code>, <code>grayscale()</code> and <code>drop-shadow()</code>.",
  "Mix layers with <code>background-blend-mode</code> and <code>mix-blend-mode</code>.",
  "Wrap text around a shape, and fill text with a gradient."])
b += ST("Read", "Box shadows") + prose("""
    <h3>A simple box shadow</h3>
    <p><code>box-shadow</code> takes up to five values: horizontal offset, vertical offset, blur, spread, and a colour.</p>
    <pre class="snippet" data-lang="css">.simple {
  box-shadow: 5px 5px 5px rgb(0 0 0 / 70%);
}</pre>
    <p>The best shadows are barely noticeable. Use a semi-transparent colour rather than solid black, and let it fall slightly downward, as if lit from above. A shadow is painted, not laid out: it takes no space and never pushes other boxes away.</p>
    <h3>Multiple box shadows</h3>
    <p>Separate several shadows with commas. Stacking a tight, darker one with a wide, faint one looks much more natural than either alone:</p>
    <pre class="snippet" data-lang="css">.card {
  box-shadow:
    0 1px 2px rgb(0 0 0 / 12%),
    0 8px 24px rgb(0 0 0 / 10%);
}</pre>
    <h3>Other box shadow features</h3>
    <p>The <code>inset</code> keyword draws the shadow inside the box, which makes it look pressed in. Swapping an outer shadow for an inset one on <code>:active</code> is a classic "pressed button" effect.</p>""")
b += ST("Play", "box-shadow", "A shadow has an x offset, a y offset, a blur, a spread and a colour. Try the presets, then adjust them yourself.") + bs
b += prose("""
    <h3>Text shadows</h3>
    <p><code>text-shadow</code> works the same way, without spread or inset. Its best use is keeping big headings readable on a busy photo; on body text it just looks blurry.</p>""")
b += ST("Play", "text-shadow for readable text on images") + ts
b += ST("Practice", "Add depth with shadows", "Make the card float with a soft, natural shadow, and lift the heading off the photo.") + '  <div id="ex-shadow"></div>\n\n'
b += ST("Read", "Filters") + prose("""
    <p>The <code>filter</code> property changes how an element is drawn, like a photo editor: <code>blur(10px)</code>, <code>grayscale(60%)</code>, <code>brightness()</code>, <code>contrast()</code>, <code>invert()</code>, <code>hue-rotate()</code>, <code>sepia()</code>. It applies to the whole element, text and children included.</p>
    <p><code>filter: drop-shadow()</code> is a shadow that follows the element's actual shape, including transparent areas of an image, where <code>box-shadow</code> always follows the rectangle.</p>""")
b += ST("Look", "box-shadow vs filter: drop-shadow()", "box-shadow follows the element's rectangle. drop-shadow follows the shape you can see.") + cmp
b += ST("Play", "Other filters") + flt
b += ST("Read", "Blend modes") + prose("""
    <p>Blend modes decide how overlapping colours mix, as in Photoshop: <code>multiply</code> darkens, <code>screen</code> lightens, <code>overlay</code> boosts contrast, <code>difference</code> inverts.</p>
    <h3>background-blend-mode</h3>
    <p>Blends an element's own background layers together, like a background image with its background colour: <code>background-blend-mode: multiply</code> tints the image with the colour.</p>
    <h3>mix-blend-mode</h3>
    <p>Blends a whole element with whatever is behind it on the page.</p>""")
b += ST("Play", "Try each blend mode", "The striped box has a green background colour under a stripe image; the purple circle overlaps it.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="control"><label for="bl-bg">background-blend-mode (striped box)</label><select id="bl-bg"><option>normal</option><option>multiply</option><option>screen</option><option>overlay</option><option>difference</option><option>luminosity</option></select></div>
      <div class="control"><label for="bl-mix">mix-blend-mode (circle)</label><select id="bl-mix"><option>normal</option><option>multiply</option><option>screen</option><option>overlay</option><option>difference</option><option>exclusion</option></select></div>
      <pre class="snippet" id="bl-code"></pre>
    </div>
    <div class="bl-stage"><div class="bl-a" id="bl-a"></div><div class="bl-b" id="bl-b">Mix</div></div>
  </section>

"""
b += ST("Read", "CSS shapes") + prose("""
    <p>Text normally wraps around a floated element's rectangle. <code>shape-outside</code> makes it wrap around a shape instead, such as a circle:</p>
    <pre class="snippet" data-lang="css">img {
  float: left;
  shape-outside: circle(50%);
}</pre>""")
b += ST("Play", "Wrap text around a circle", "Switch <code>shape-outside</code> on and off.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <label class="toggle"><input type="checkbox" id="shape-on" checked> <code>shape-outside: circle(50%)</code></label>
    </div>
    <div class="sh-stage"><div class="ball" id="ball"></div>The sun sets behind the Flatirons around eight in midsummer, painting the sandstone orange. Hikers on the Mesa Trail stop to watch the light change, then hurry down before dark. Notice how these lines hug the curve of the circle when the shape is on, and stay square when it's off.</div>
  </section>

"""
b += ST("Read", "-webkit-background-clip: text") + prose("""
    <p><code>background-clip</code> decides how far a background reaches. Its <code>text</code> value clips the background to the letters, so a gradient or image fills the text. Make the text itself transparent to see it:</p>
    <pre class="snippet" data-lang="css">h2 {
  background-image: linear-gradient(90deg, #0b6b5e, #2340d9, #b4410c);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}</pre>
    <p>The <code>-webkit-</code> prefix is a <em>vendor prefix</em>: a browser-specific version from before the feature was standardised. Some browsers still need it here, so write both. Check that the text stays readable, and that a colour shows if the effect isn't supported.</p>""")
b += ST("Play", "Gradient text", "Switch clipping on.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start"><label class="toggle"><input type="checkbox" id="clip-on" checked> <code>background-clip: text</code> and transparent text</label></div>
    <div class="panel" style="background:#fff"><h2 class="clip-h on" id="clip-h">Above Treeline</h2></div>
  </section>

"""
b += ST("Practice", "Effects on a trail card", "A pressed button, a grayscale photo and gradient text.") + '  <div id="ex-effects"></div>\n\n'
b += notes([
  "<code>box-shadow</code>: x, y, blur, spread, colour; stack several with commas.",
  "Shadows take no space; <code>inset</code> draws them inside.",
  "<code>filter</code> edits how a whole element is drawn; <code>drop-shadow()</code> follows its shape.",
  "<code>background-blend-mode</code> mixes an element's own layers; <code>mix-blend-mode</code> mixes it with the page.",
  "<code>background-clip: text</code> fills letters with a background; keep a readable fallback.",
], [
  "Solid black shadows, or shadows so big they look like smudges.",
  "<code>text-shadow</code> on body text.",
  "Relying on a shadow alone to separate a card from its background, especially in dark mode.",
  "Gradient text with no fallback colour, which can vanish entirely.",
  "Blend modes that destroy text contrast.",
])
first = src.first_script()
js = r'''
  // --- Blend modes ---
  function bl() {
    const bg = $("bl-bg").value, mix = $("bl-mix").value;
    $("bl-a").style.backgroundBlendMode = bg; $("bl-b").style.mixBlendMode = mix;
    $("bl-code").textContent = `.striped {\n  background-color: #3fa66b;\n  background-image: repeating-linear-gradient(…);\n  background-blend-mode: ${bg};\n}\n.circle {\n  mix-blend-mode: ${mix};\n}`;
  }
  ["bl-bg", "bl-mix"].forEach((id) => $(id).addEventListener("input", bl));
  bl();

  // --- Shapes and clip ---
  $("shape-on").addEventListener("change", (e) => { $("ball").style.shapeOutside = e.target.checked ? "circle(50%)" : "none"; });
  $("ball").style.shapeOutside = "circle(50%)";
  $("clip-on").addEventListener("change", (e) => $("clip-h").classList.toggle("on", e.target.checked));
'''
ex_s = src.block('  makeExercise(document.getElementById("ex-shadow"), {')
ex_e = r'''  makeExercise(document.getElementById("ex-effects"), {
    title: "Pressed, grayscale and gradient",
    task: `<ol>
      <li>Add a <code>.btn:active</code> rule with <code>box-shadow: inset 0 2px 4px rgb(0 0 0 / 40%)</code>, so the button looks pressed while clicked.</li>
      <li>Give <code>.photo</code> <code>filter: grayscale(100%)</code>.</li>
      <li>Fill the <code>h2</code> with its gradient: <code>-webkit-background-clip: text</code>, <code>background-clip: text</code> and <code>-webkit-text-fill-color: transparent</code>.</li>
    </ol>`,
    html: `<div class="card">
  <div class="photo"></div>
  <h2>Royal Arch</h2>
  <button class="btn">Save trail</button>
</div>`,
    css: `body { font-family: system-ui, sans-serif; }
.photo { height: 100px; border-radius: 8px; background: linear-gradient(160deg, #f0b37a, #b4410c 60%, #0b6b5e); }
h2 { font-size: 2.2rem; color: #0b6b5e; background-image: linear-gradient(90deg, #0b6b5e, #2340d9); }
.btn { padding: 10px 18px; border: 0; border-radius: 6px; background: #0b6b5e; color: white; box-shadow: 0 2px 4px rgb(0 0 0 / 25%); }
`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.photo { height: 100px; border-radius: 8px; background: linear-gradient(160deg, #f0b37a, #b4410c 60%, #0b6b5e); filter: grayscale(100%); }
h2 { font-size: 2.2rem; color: #0b6b5e; background-image: linear-gradient(90deg, #0b6b5e, #2340d9); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
.btn { padding: 10px 18px; border: 0; border-radius: 6px; background: #0b6b5e; color: white; box-shadow: 0 2px 4px rgb(0 0 0 / 25%); }
.btn:active { box-shadow: inset 0 2px 4px rgb(0 0 0 / 40%); }
` },
    hints: [".btn:active is a separate rule after .btn.", "Keep color: #0b6b5e on the h2: it's the fallback if clipping isn't supported."],
    checks: [
      { label: "A .btn:active rule sets an inset shadow", test: ({ doc }) => [...doc.styleSheets[0].cssRules].some((r) => /\.btn:active/.test(r.selectorText || "") && /inset/.test(r.style.boxShadow)) },
      { label: "The photo is grayscale", test: ({ style }) => /grayscale\((1|100%)\)/.test(style(".photo", "filter")) },
      { label: "The heading is clipped to its text", test: ({ style }) => style("h2", "-webkit-background-clip") === "text" && /rgba\(0, 0, 0, 0\)|transparent/.test(style("h2", "-webkit-text-fill-color")) },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "What does the inset keyword do to a box-shadow?", opts: ["Draws it inside the box", "Makes it smaller", "Removes the blur"], a: 0, why: "Inset shadows make a box look pressed in." },
    { id: "q6", q: "Which property makes text wrap around a floated circle instead of its square box?", opts: ["shape-outside", "border-radius", "mix-blend-mode"], a: 0, why: "shape-outside changes the wrap area of a float." },
  ]);
''')
write("core-shadows-effects.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_s + "\n" + ex_e + "\n" + quiz + "</script>\n")
