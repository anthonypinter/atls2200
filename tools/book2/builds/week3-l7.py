import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("colors-units")
hsl = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="h">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Units:')
units = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="root">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
extra = """
  .em-demo { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  @media (max-width: 640px) { .em-demo { grid-template-columns: 1fr; } }
  .em-demo .panel { background: #fff; color: #1d2133; overflow: hidden; }
  .em-demo ul { margin: 0; padding-left: 1.2em; font-family: Georgia, serif; }
  .em-demo li { line-height: 1.3; }
  .ip-box { height: 200px; border-radius: 8px; border: 1px solid var(--line); background-color: #fff; background-repeat: no-repeat; }
  .calc-wrap { border: 2px dashed #9aa2bf; padding: 8px; background: var(--stage); border-radius: 6px; max-width: 100%; }
  .calc-wrap div { background: #9ec2e6; color: #1d2133; padding: 6px 8px; margin: 4px 0; font: 600 0.82rem var(--font-code); font-variation-settings: "MONO" 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .calc-wrap div:nth-child(2) { background: #f0b37a; } .calc-wrap div:nth-child(3) { background: #b9d99a; }
"""
h = head("Values and Units", src.css(), extra)
b = top("Values and Units", "Every declaration ends in a value: a colour, a length, a percentage, an image, a function. Knowing the kinds of value CSS accepts, and what each unit is measured against, is what makes a layout adapt instead of break.", [
  "Read value types like <code>&lt;length&gt;</code> and <code>&lt;color&gt;</code> on MDN reference pages.",
  "Choose between absolute and relative units, and explain how <code>em</code> and <code>rem</code> differ.",
  "Write colours as keywords, hex, <code>rgb()</code> and <code>hsl()</code>, with transparency.",
  "Use images, positions, strings and math functions like <code>calc()</code> and <code>clamp()</code> as values."])
b += ST("Read", "What is a CSS value?") + prose("""
    <p>On MDN's reference pages, the kinds of value a property accepts are written in angle brackets: <code>&lt;color&gt;</code>, <code>&lt;length&gt;</code>, <code>&lt;percentage&gt;</code>. These are <strong>value types</strong>, not HTML elements. So when the page for <code>color</code> says it accepts a <code>&lt;color&gt;</code>, any of the colour formats below will work:</p>
    <pre class="snippet" data-lang="css">h1 {
  color: black;                      /* a keyword */
  background-color: rgb(197 93 161); /* a function */
}</pre>""")
b += ST("Read", "Numbers, lengths, and percentages") + prose("""
    <h3>Lengths</h3>
    <p>A length is a number with a <span class="term">unit</span>, with no space between them. There are two families:</p>
    <ul>
      <li><strong>Absolute units</strong> are always the same size: <code>px</code> (pixels) is the one you'll use. Print units like <code>cm</code>, <code>in</code> and <code>pt</code> exist, but don't belong on screens.</li>
      <li><strong>Relative units</strong> are measured from something else, so they adapt:
        <ul>
          <li><code>em</code>: the font size of the element itself (for <code>font-size</code>, the parent's).</li>
          <li><code>rem</code>: the font size of the root element, <code>&lt;html&gt;</code>, usually 16px.</li>
          <li><code>vw</code> and <code>vh</code>: 1% of the browser window's width and height.</li>
        </ul>
      </li>
    </ul>""")
b += ST("Play", "Units: how big is “12”?", "Each bar below is the same number with a different unit. Change the settings and watch which bars move.") + units
b += prose("""
    <h3>ems and rems</h3>
    <p><code>em</code> sizes compound. In a nested list where each <code>li</code> is <code>1.3em</code>, every level is 1.3 times its parent, so text grows as you go deeper. <code>rem</code> always measures from the root, so every level is the same size.</p>""")
b += ST("Play", "ems compound, rems don't", "The same nested list, with <code>li { font-size: 1.3em }</code> on the left and <code>1.3rem</code> on the right. Add levels.") + """  <div class="panel" style="display:grid;gap:10px">
    <div class="control"><label for="em-n">nesting levels</label><input id="em-n" type="range" min="1" max="5" value="3"><span class="readout" id="em-n-out"></span></div>
    <div class="em-demo"><div class="panel"><span class="eyebrow">1.3em</span><div id="em-a"></div></div><div class="panel"><span class="eyebrow">1.3rem</span><div id="em-b"></div></div></div>
  </div>

"""
b += prose("""
    <h3>Percentages</h3>
    <p>A percentage is always a share of something else, usually the parent's size. <code>width: 40%</code> is 40% of the parent's width; <code>font-size: 80%</code> is 80% of the parent's font size.</p>
    <h3>Numbers</h3>
    <p>Some properties take a plain number with no unit: <code>opacity: 0.6</code> (0 is invisible, 1 solid) or <code>line-height: 1.5</code> (1.5 times the font size).</p>
    <div class="callout tip"><p class="callout-title">Which unit?</p><p>Use <span class="term" data-term="rem (unit)">rem</span> for font sizes: people who set a larger default text size in their browser get bigger text, while px ignores that setting. Use <code>%</code> or <code>max-width</code> for widths so boxes fit small screens. Keep <code>px</code> for things that should stay fixed, like borders.</p></div>""")
b += ST("Practice", "Pick better units", "These pixel values ignore the reader's settings and the screen size. Swap in units that adapt.") + '  <div id="ex-units"></div>\n\n'
b += ST("Read", "Color") + prose("""
    <h3>Color keywords</h3>
    <p>CSS has around 150 named colours, like <code>teal</code>, <code>antiquewhite</code> and <code>rebeccapurple</code>. Handy for quick tests, but you can't fine-tune them.</p>
    <h3>Hexadecimal RGB values</h3>
    <p>A <span class="term">hex color</span> like <code>#02798b</code> is three pairs of hexadecimal digits for red, green and blue, each from <code>00</code> to <code>ff</code>. Designers hand you hex codes, so you'll see them everywhere.</p>
    <h3>RGB values</h3>
    <p><code>rgb(2 121 139)</code> is the same idea in decimal: red, green and blue from 0 to 255. Add a slash and a fourth value for transparency (the <em>alpha</em> channel): <code>rgb(2 121 139 / 30%)</code> is 30% opaque.</p>
    <h3>Using hues to specify a color</h3>
    <p>Mixing red, green and blue in your head is hard. Hue-based formats start from a position on the colour wheel, in degrees: 0 is red, 120 green, 240 blue.</p>
    <ul>
      <li><strong><span class="term">HSL</span>:</strong> <code>hsl(188 97% 28%)</code> is hue, saturation (grey to vivid) and lightness (black to white). Keep the hue and change the lightness for a matching darker or lighter shade. Transparency works the same way: <code>hsl(188 97% 28% / 30%)</code>.</li>
      <li><strong>HWB:</strong> <code>hwb(188 0% 45%)</code> is hue, then how much white and black to mix in.</li>
    </ul>""")
b += ST("Play", "Mixing colors with HSL", "Keep the hue and change the lightness to get a darker or lighter version of the same colour. Check the contrast for text.") + hsl
b += ST("Practice", "One colour, many formats", "Write each colour in the format asked for.") + '  <div id="ex-colors"></div>\n\n'
b += ST("Read", "Images, position, and strings") + prose("""
    <h3>Images</h3>
    <p>An <code>&lt;image&gt;</code> value can be a file, with <code>url()</code>, or a gradient that CSS draws for you:</p>
    <pre class="snippet" data-lang="css">background-image: url("images/arch.jpg");
background-image: linear-gradient(90deg, rgb(119 0 255 / 39%), rgb(0 212 255 / 25%));</pre>
    <h3>Position</h3>
    <p>A <code>&lt;position&gt;</code> places something, like a background image, in a box. It takes keywords (<code>top</code>, <code>right</code>, <code>center</code>…), lengths, or both: <code>background-position: right 60px</code> means against the right edge, 60px from the top.</p>
    <h3>Strings and identifiers</h3>
    <p>Keywords like <code>red</code> or <code>center</code> are <em>identifiers</em>: written without quotes. Some places need a <em>string</em> of text in quotes, like generated content: <code>content: "New!";</code>.</p>""")
b += ST("Play", "Images and position", "A gradient, positioned in a box.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="control"><label for="ip-img">background-image</label><select id="ip-img"><option value="linear-gradient(90deg, rgb(119 0 255 / 60%), rgb(0 212 255 / 60%))">linear-gradient(…)</option><option value="radial-gradient(circle, #f0b37a, #b4410c)">radial-gradient(…)</option><option value="repeating-linear-gradient(45deg, #9ec2e6 0 10px, #fff 10px 20px)">repeating-linear-gradient(…)</option></select></div>
      <div class="control"><label for="ip-pos">background-position</label><select id="ip-pos"><option>center</option><option>top left</option><option>right 60px</option><option>bottom right</option><option>20px 30px</option></select></div>
      <pre class="snippet" id="ip-code"></pre>
    </div>
    <div class="ip-box" id="ip-box" role="img" aria-label="Positioned gradient"></div>
  </section>

"""
b += ST("Read", "Functions") + prose("""
    <p>A function is a name followed by brackets, which CSS works out for you. You've already met <code>rgb()</code>, <code>hsl()</code>, <code>url()</code> and gradients.</p>
    <h3>Math functions</h3>
    <ul>
      <li><code><span class="term">calc()</span></code> mixes units: <code>width: calc(20% + 100px)</code>.</li>
      <li><code>min()</code> picks the smallest of its values, <code>max()</code> the largest: <code>width: min(100%, 600px)</code> is never wider than 600px or its parent.</li>
      <li><code><span class="term">clamp()</span></code> takes a minimum, a preferred value and a maximum: <code>font-size: clamp(1rem, 4vw, 2rem)</code>.</li>
    </ul>""")
b += ST("Play", "Math functions", "Change the wrapper's width and watch each box recalculate.") + """  <div class="panel" style="display:grid;gap:10px">
    <div class="control"><label for="cw">wrapper width</label><input id="cw" type="range" min="200" max="700" step="10" value="400"><span class="readout" id="cw-out"></span></div>
    <div class="calc-wrap" id="calc-wrap"><div style="width: calc(20% + 100px)" data-f="calc(20% + 100px)"></div><div style="width: min(100%, 300px)" data-f="min(100%, 300px)"></div><div style="width: clamp(150px, 50%, 280px)" data-f="clamp(150px, 50%, 280px)"></div></div>
  </div>

"""
b += notes([
  "Value types like <code>&lt;length&gt;</code> and <code>&lt;color&gt;</code> tell you what a property accepts.",
  "<code>px</code> is fixed; <code>em</code>, <code>rem</code>, <code>%</code>, <code>vw</code> and <code>vh</code> adapt.",
  "<code>em</code> compounds through nested elements; <code>rem</code> always measures from the root.",
  "Hex, <code>rgb()</code> and <code>hsl()</code> can all describe the same colour; add <code>/ 50%</code> for transparency.",
  "<code>calc()</code>, <code>min()</code>, <code>max()</code> and <code>clamp()</code> do the math for you.",
], [
  "A space between number and unit (<code>16 px</code>), or no unit at all on a length.",
  "Font sizes in <code>px</code>, which ignore the reader's text-size setting.",
  "Nested <code>em</code> font sizes that grow (or shrink) out of control.",
  "Low-contrast text, like light grey on white.",
  "<code>calc(20%+100px)</code> without spaces around the <code>+</code>: it's invalid.",
])
first = src.first_script()
js = r'''
  // --- ems compound ---
  function emList(unit, n) {
    let html = "";
    for (let i = n; i >= 1; i--) html = `<ul><li style="font-size:1.3${unit}">Level ${i}${html}</li></ul>`;
    return html;
  }
  function em() { const n = +$("em-n").value; $("em-n-out").textContent = n; $("em-a").innerHTML = emList("em", n); $("em-b").innerHTML = emList("rem", n); }
  $("em-n").addEventListener("input", em);
  em();

  // --- Images and position ---
  function ip() {
    const img = $("ip-img").value, pos = $("ip-pos").value, box = $("ip-box");
    box.style.backgroundImage = img; box.style.backgroundPosition = pos; box.style.backgroundSize = "120px 120px";
    $("ip-code").textContent = `background-image: ${img};\nbackground-size: 120px 120px;\nbackground-position: ${pos};`;
  }
  ["ip-img", "ip-pos"].forEach((id) => $(id).addEventListener("input", ip));
  ip();

  // --- Math functions ---
  function cw() {
    const w = +$("cw").value; $("calc-wrap").style.width = w + "px"; $("cw-out").textContent = w + "px";
    $("calc-wrap").querySelectorAll("div").forEach((d) => (d.textContent = `${d.dataset.f} = ${Math.round(d.getBoundingClientRect().width)}px`));
  }
  $("cw").addEventListener("input", cw);
  cw();
'''
ex_units = src.block('  makeExercise(document.getElementById("ex-units"), {')
ex_col = r'''  makeExercise(document.getElementById("ex-colors"), {
    title: "Four formats",
    task: `<ol>
      <li>Card background: the keyword <code>antiquewhite</code>.</li>
      <li>Heading colour: hex <code>#02798b</code>.</li>
      <li>Card border colour: <code>hsl(188 97% 28%)</code>.</li>
      <li>Badge background: <code>rgb(197 93 161)</code> at 50% opacity, using the slash syntax.</li>
    </ol>`,
    html: `<div class="card">
  <h2>Royal Arch <span class="badge">Hard</span></h2>
  <p>A steep 3.4-mile round trip.</p>
</div>`,
    css: `body { font-family: system-ui, sans-serif; }
.card {
  padding: 16px;
  border: 4px solid black;
  background-color: white;
}
h2 { color: black; }
.badge { font-size: 0.6em; padding: 2px 8px; background-color: gray; }`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.card {
  padding: 16px;
  border: 4px solid hsl(188 97% 28%);
  background-color: antiquewhite;
}
h2 { color: #02798b; }
.badge { font-size: 0.6em; padding: 2px 8px; background-color: rgb(197 93 161 / 50%); }` },
    hints: ["hsl(188 97% 28%) works anywhere a colour does, including in the border shorthand.", "Transparency: rgb(197 93 161 / 50%)."],
    checks: [
      { label: "The card is antiquewhite", test: ({ style }) => style(".card", "background-color") === "rgb(250, 235, 215)" },
      { label: "The heading is #02798b", test: ({ style }) => style("h2", "color") === "rgb(2, 121, 139)" },
      { label: "The border is hsl(188 97% 28%)", test: ({ style }) => { const m = style(".card", "border-top-color").match(/\d+/g).map(Number); return Math.abs(m[0] - 2) <= 2 && Math.abs(m[1] - 121) <= 2 && Math.abs(m[2] - 140) <= 2; } },
      { label: "The badge is half-transparent rgb(197 93 161)", test: ({ style }) => /rgba\(197, 93, 161, 0\.5\)/.test(style(".badge", "background-color")) },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "x1", q: "How do you make a colour 30% opaque?", opts: ["rgb(2 121 139 / 30%)", "rgb(2 121 139 30%)", "opacity-color: 30%"], a: 0, why: "A slash before the fourth value sets the alpha channel." },
    { id: "x2", q: "Which is valid?", opts: ["calc(20% + 100px)", "calc(20%+100px)", "calc(20% 100px)"], a: 0, why: "calc needs spaces around + and -." },
  ]);
''')
write("core-values-units.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_units + "\n" + ex_col + "\n" + quiz + "</script>\n")
