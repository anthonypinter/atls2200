import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("typography")
tune = src.between('  <section class="playground" id="tester">', '  <div class="section-title"><span class="eyebrow">Type scale</span>')
scale = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="base">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
extra = """
  .generic { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 8px; }
  .generic div { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; display: grid; gap: 4px; }
  .generic code { font-size: 0.78rem; color: var(--muted); }
  .generic span { font-size: 1.35rem; }
  .ts-sample { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 18px; font: 1.6rem Georgia, serif; min-height: 90px; display: grid; place-items: center; text-align: center; }
  .longhands { margin: 0; padding: 0; list-style: none; font: 0.88rem/1.8 var(--font-code); font-variation-settings: "MONO" 1; }
  .longhands b { color: var(--prop); font-weight: 600; }
"""
h = head("Fundamental Text Styling", src.css(), extra)
b = top("Fundamental Text Styling", "Most of what's on a web page is text, so how it reads matters more than almost any other design choice. CSS splits text styling in two: the font itself, and how the text is laid out.", [
  "Write a font stack that always falls back to something sensible.",
  "Set font size, style, weight, case, decoration and shadows.",
  "Lay text out with alignment, line height, letter and word spacing, and a readable line length.",
  "Read and write the <code>font</code> shorthand."])
b += ST("Read", "What is involved in styling text in CSS?") + prose("""
    <p>Text sits inside its element's content box and flows from the start of the line to the end, wrapping onto new lines. You can't select a single word or line with CSS, only whole elements (with two exceptions, <code>::first-line</code> and <code>::first-letter</code>). The properties fall into two groups:</p>
    <ul>
      <li><strong>Font styles</strong> change the letters themselves: which font, how big, bold, italic, colour.</li>
      <li><strong>Text layout styles</strong> change the space around them: alignment, line spacing, letter and word spacing.</li>
    </ul>""")
b += ST("Read", "Fonts") + prose("""
    <h3>Color</h3>
    <p><code>color</code> sets the colour of the text (and of text decorations like underlines). It's named <code>color</code>, not <code>font-color</code> or <code>text-color</code>.</p>
    <h3>Font families</h3>
    <p><code>font-family</code> names the font to use. It only works if the font is available: installed on the visitor's computer, or downloaded as a web font (next lesson). A few <em>web safe fonts</em>, like Arial, Verdana, Georgia and Times New Roman, are on nearly every computer.</p>
    <p>Because you can't be sure, list several fonts in order of preference. That's a <span class="term">font stack</span>: the browser uses the first one it has. Always end with a <strong>generic family</strong> name, which every browser maps to some font it does have:</p>
    <pre class="snippet" data-lang="css">p {
  font-family: "Trebuchet MS", Verdana, sans-serif;
}</pre>
    <p>Quote names with spaces in them. The generic families look like this in your browser:</p>""")
b += """  <div class="generic" id="generic"></div>

"""
b += ST("Play", "Try a font stack", "Type a font stack. The browser draws the sample in the first font it has.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:8px;align-content:start">
      <label class="eyebrow" for="fst">font-family:</label>
      <input class="src" id="fst" spellcheck="false" autocomplete="off" value='"Trail Sans", Georgia, serif'>
      <div class="presets" id="fst-presets" role="group" aria-label="Examples">
        <button class="btn" type="button">"Trail Sans", Georgia, serif</button>
        <button class="btn" type="button">"Trebuchet MS", Verdana, sans-serif</button>
        <button class="btn" type="button">Courier New, monospace</button>
        <button class="btn" type="button">"Made Up Font"</button>
      </div>
      <p class="verdict" id="fst-note" aria-live="polite"></p>
    </div>
    <div class="ts-sample" id="fst-out">The quick brown fox jumps over the lazy dog</div>
  </section>

"""
b += prose("""
    <h3>Font size</h3>
    <p><code>font-size</code> takes any length. Browsers default to 16px. Set sizes in <code>rem</code> so they follow the visitor's text-size setting (<code>1rem</code> is 16px by default, <code>1.5rem</code> 24px). Watch out for <code>em</code> on font sizes: it's relative to the parent's font size, so it compounds through nested elements.</p>
    <p>Heading sizes look best when they belong together. A <em>type scale</em> multiplies each level by the same ratio.</p>""")
b += ST("Play", "Heading sizes that belong together", "Pick a base size and a ratio.") + scale
b += prose("""
    <h3>Font style, font weight, text transform, and text decoration</h3>
    <ul>
      <li><code>font-style</code>: <code>italic</code> or <code>normal</code>. Use it to un-italicise, say, an <code>&lt;em&gt;</code>.</li>
      <li><code>font-weight</code>: <code>normal</code>, <code>bold</code>, or a number from 100 to 900 (400 is normal, 700 bold), if the font has those weights.</li>
      <li><code>text-transform</code>: <code>uppercase</code>, <code>lowercase</code> or <code>capitalize</code>. It changes how text looks, not the text itself, so a screen reader still reads the original.</li>
      <li><code>text-decoration</code>: <code>underline</code>, <code>overline</code>, <code>line-through</code>, or <code>none</code> (often used on links). It's a shorthand, so <code>underline wavy red</code> works too.</li>
    </ul>
    <h3>Text drop shadows</h3>
    <p><code>text-shadow: 4px 4px 5px red</code> sets the shadow's horizontal offset, vertical offset, blur and colour. Separate several shadows with commas.</p>""")
b += ST("Play", "Style the letters", "Mix and match. The CSS appears below.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="control"><label for="ts-style">font-style</label><select id="ts-style"><option>normal</option><option>italic</option></select></div>
      <div class="control"><label for="ts-weight">font-weight</label><select id="ts-weight"><option>300</option><option selected>400</option><option>700</option><option>900</option></select></div>
      <div class="control"><label for="ts-tt">text-transform</label><select id="ts-tt"><option>none</option><option>uppercase</option><option>lowercase</option><option>capitalize</option></select></div>
      <div class="control"><label for="ts-td">text-decoration</label><select id="ts-td"><option>none</option><option>underline</option><option>underline wavy #b4410c</option><option>line-through</option><option>overline</option></select></div>
      <div class="control"><label for="ts-sh">text-shadow</label><select id="ts-sh"><option>none</option><option>2px 2px 0 #9ec2e6</option><option>4px 4px 5px red</option><option>1px 1px 1px red, 2px 2px 1px red</option><option>0 0 8px #2340d9</option></select></div>
      <pre class="snippet" id="ts-code"></pre>
    </div>
    <div class="ts-sample" id="ts-out">the Royal Arch trail</div>
  </section>

"""
b += ST("Read", "Text layout") + prose("""
    <h3>Text alignment</h3>
    <p><code>text-align</code>: <code>left</code>, <code>right</code>, <code>center</code> or <code>justify</code>. Left-align long paragraphs (in English); centred text is fine for a short heading but hard to read for more than a line or two, and <code>justify</code> can leave rivers of gaps.</p>
    <h3>Line height</h3>
    <p><code>line-height</code> sets the height of each line. Write it without a unit, like <code>1.6</code>, so it's a multiple of the font size and scales with it. Around 1.4 to 1.8 is comfortable for body text.</p>
    <h3>Letter and word spacing</h3>
    <p><code>letter-spacing</code> and <code>word-spacing</code> add (or remove, with negative values) space between letters and words. A little extra letter spacing helps small uppercase text.</p>
    <h3>Line length</h3>
    <p>Not a property of its own, but it matters most: lines of about 45 to 75 characters read best. Limit paragraphs with <code>max-width: 65ch</code>, where <code>ch</code> is roughly one character wide.</p>""")
b += ST("Play", "Tune the text", "Adjust each setting and watch the readability checks respond.") + tune
b += prose("""
    <h3>Other properties worth looking at</h3>
    <p>There are many more: <code>font-variant</code> (small caps), <code>text-indent</code>, <code>text-overflow</code> (an ellipsis for cut-off text), <code>white-space</code> (whether text wraps), <code>word-break</code>, <code>text-wrap: balance</code> (evens out the lines of a heading) and <code>writing-mode</code> (vertical text). Look them up on MDN when you need them.</p>""")
b += ST("Practice", "Make it readable", "The text is set in one long, cramped line. Fix the font, the spacing and the line length.") + '  <div id="ex-type"></div>\n\n'
b += ST("Read", "Font shorthand") + prose("""
    <p>The <code>font</code> shorthand sets most font properties in one line. The order is strict: optional style, variant and weight first, then the required <strong>size</strong> (with an optional <code>/line-height</code>), then the required <strong>family</strong> last:</p>
    <pre class="snippet" data-lang="css">font: italic bold 1.25rem/1.5 Georgia, serif;</pre>
    <p>Leave out the size or the family and the whole declaration is ignored. And anything you leave out is reset to its default, so put <code>font</code> before any longhands you want to keep.</p>""")
b += ST("Play", "Expand the shorthand", "Type a <code>font</code> value. The browser shows the longhands it sets, or ignores it.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:8px;align-content:start">
      <label class="eyebrow" for="fs-in">font:</label>
      <input class="src" id="fs-in" spellcheck="false" autocomplete="off" value="italic bold 1.25rem/1.5 Georgia, serif">
      <div class="presets" id="fs-presets" role="group" aria-label="Examples">
        <button class="btn" type="button">italic bold 1.25rem/1.5 Georgia, serif</button>
        <button class="btn" type="button">1rem system-ui, sans-serif</button>
        <button class="btn" type="button">bold Georgia</button>
        <button class="btn" type="button">300 2rem/1.1 "Trebuchet MS", sans-serif</button>
      </div>
      <ul class="longhands" id="fs-out" aria-live="polite"></ul>
    </div>
    <div class="ts-sample" id="fs-sample">Royal Arch, 3.4 miles</div>
  </section>

"""
b += ST("Practice", "A trail page header", "Style the heading and introduction.") + '  <div id="ex-header"></div>\n\n'
b += notes([
  "End every font stack with a generic family: <code>serif</code>, <code>sans-serif</code> or <code>monospace</code>.",
  "Use <code>rem</code> for font sizes; at least <code>1rem</code> (16px) for body text.",
  "Unitless <code>line-height</code> around 1.4 to 1.8; lines of 45 to 75 characters.",
  "<code>text-transform</code> changes how text looks, not what it says.",
  "The <code>font</code> shorthand needs a size and a family, in that order, and resets what you leave out.",
], [
  "A font name with spaces and no quotes, or a stack with no generic fallback.",
  "<code>font-color</code> or <code>text-color</code>: the property is <code>color</code>.",
  "Centring or justifying long paragraphs.",
  "Typing headings in capitals in the HTML instead of using <code>text-transform</code>.",
  "A <code>font</code> shorthand without a size, which throws the whole declaration away.",
])
first = src.first_script()
js = r'''
  // --- Generic families ---
  $("generic").innerHTML = ["serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui"].map((g) => `<div><code>${g}</code><span style="font-family:${g}">Royal Arch</span></div>`).join("");

  // --- Font stack ---
  function fst() {
    const v = $("fst").value, out = $("fst-out");
    out.style.fontFamily = ""; out.style.fontFamily = v;
    const ok = out.style.fontFamily !== "";
    const generic = /(^|,)\s*(serif|sans-serif|monospace|cursive|fantasy|system-ui)\s*$/.test(v);
    $("fst-note").className = "verdict " + (ok && generic ? "ok" : "bad");
    $("fst-note").textContent = !ok ? "✗ Not a valid font-family value, so it's ignored. Quote names that contain spaces or digits." : generic ? "✓ Ends with a generic family, so there's always a sensible fallback." : "✗ No generic family at the end. If none of these fonts exist, the browser falls back to its default font, whatever that is.";
  }
  $("fst").addEventListener("input", fst);
  $("fst-presets").addEventListener("click", (e) => { const b = e.target.closest(".btn"); if (b) { $("fst").value = b.textContent; fst(); } });
  fst();

  // --- Style the letters ---
  function ts() {
    const p = { "font-style": $("ts-style").value, "font-weight": $("ts-weight").value, "text-transform": $("ts-tt").value, "text-decoration": $("ts-td").value, "text-shadow": $("ts-sh").value };
    const out = $("ts-out");
    Object.entries(p).forEach(([k, v]) => out.style.setProperty(k, v));
    $("ts-code").textContent = "h1 {\n" + Object.entries(p).filter(([k, v]) => !["normal", "none", "400"].includes(v)).map(([k, v]) => `  ${k}: ${v};`).join("\n") + "\n}";
  }
  ["ts-style", "ts-weight", "ts-tt", "ts-td", "ts-sh"].forEach((id) => $(id).addEventListener("input", ts));
  ts();

  // --- Font shorthand ---
  function fsh() {
    const v = $("fs-in").value, s = $("fs-sample");
    s.style.font = ""; s.style.font = v;
    if (!s.style.font) { $("fs-out").innerHTML = "<li>✗ Invalid: the browser ignores the whole declaration. It needs a size, then a family.</li>"; return; }
    $("fs-out").innerHTML = ["font-style", "font-variant", "font-weight", "font-size", "line-height", "font-family"].map((k) => `<li><b>${k}</b>: ${s.style.getPropertyValue(k) || "(reset)"}</li>`).join("");
  }
  $("fs-in").addEventListener("input", fsh);
  $("fs-presets").addEventListener("click", (e) => { const b = e.target.closest(".btn"); if (b) { $("fs-in").value = b.textContent; fsh(); } });
  fsh();
'''
ex_type = src.block('  makeExercise(document.getElementById("ex-type"), {')
ex_head = r'''  makeExercise(document.getElementById("ex-header"), {
    title: "Header text",
    task: `<ol>
      <li>Make the <code>h1</code> <code>text-transform: uppercase</code> with <code>letter-spacing: 0.1em</code>. Leave the HTML text as it is.</li>
      <li>Give the <code>h1</code> <code>text-shadow: 2px 2px 0 #9ec2e6</code>.</li>
      <li>Set the <code>.lede</code> paragraph with one <code>font</code> shorthand: italic, <code>1.25rem</code>, line height <code>1.5</code>, <code>Georgia, serif</code>.</li>
      <li>Remove the underline from the link with <code>text-decoration</code>.</li>
    </ol>`,
    html: `<h1>Royal Arch Trail</h1>
<p class="lede">A steep climb to a sandstone arch above Boulder.</p>
<a href="#">Read the trail report</a>`,
    css: `body { font-family: system-ui, sans-serif; }
`,
    solution: { css: `body { font-family: system-ui, sans-serif; }

h1 {
  text-transform: uppercase;
  letter-spacing: 0.1em;
  text-shadow: 2px 2px 0 #9ec2e6;
}

.lede {
  font: italic 1.25rem/1.5 Georgia, serif;
}

a {
  text-decoration: none;
}
` },
    hints: ["font: italic 1.25rem/1.5 Georgia, serif; (style, then size/line-height, then family).", "text-decoration: none removes the underline."],
    checks: [
      { label: "The h1 is uppercase, spaced 0.1em, and the HTML is unchanged", test: ({ $, style }) => style("h1", "text-transform") === "uppercase" && Math.abs(parseFloat(style("h1", "letter-spacing")) - 3.2) < 0.1 && $("h1").textContent === "Royal Arch Trail" },
      { label: "The h1 has the shadow", test: ({ style }) => /rgb\(158, 194, 230\) 2px 2px 0px/.test(style("h1", "text-shadow")) },
      { label: ".lede is italic Georgia, 20px, line height 30px", test: ({ style }) => style(".lede", "font-style") === "italic" && style(".lede", "font-size") === "20px" && style(".lede", "line-height") === "30px" && style(".lede", "font-family").includes("Georgia") },
      { label: "The link has no underline", test: ({ style }) => style("a", "text-decoration-line") === "none" },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Which font shorthand is valid?", opts: ["font: bold 1rem Georgia, serif;", "font: bold Georgia;", "font: Georgia 1rem bold;"], a: 0, why: "Size and family are required, size first, family last." },
    { id: "q6", q: "text-transform: uppercase. What does a screen reader read?", opts: ["The original text from the HTML", "The text spelled letter by letter", "Nothing"], a: 0, why: "text-transform changes only how the text looks." },
  ]);
''')
write("core-text-styling.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_type + "\n" + ex_head + "\n" + quiz + "</script>\n")
