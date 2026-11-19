import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("web-fonts")
fb = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="ff">web font', '  <div class="section-title"><span class="eyebrow">Play</span><h2>What visitors see')
fd = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="fd">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Only load')
wt = src.between('  <section class="playground">\n    <div class="panel controls weights"', '  <div class="section-title"><span class="eyebrow">Practice</span>')
tools = src.between('  <div class="tools"', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Always include')
extra = """
  @font-face { font-family: "Recursive Demo"; src: url("fonts/recursive-300-1000-latin.woff2") format("woff2"); font-weight: 300 1000; font-display: swap; }
  .vf-sample { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 18px; font: 2rem/1.2 "Recursive Demo", system-ui, sans-serif; min-height: 110px; display: grid; align-content: center; }
"""
h = head("Web Fonts", src.css(), extra)
b = top("Web Fonts", "You can only count on a handful of fonts being installed on every computer. Web fonts are downloaded with your page, so every visitor sees the type you chose, as long as you load them carefully.", [
  "Explain why font stacks need fallbacks, and choose a similar one.",
  "Add a web font from Google Fonts, or self-host one with <code>@font-face</code>.",
  "Explain what each <code>@font-face</code> descriptor does, including <code>font-display</code>.",
  "Keep font downloads small: only the weights and styles you use."])
b += ST("Read", "Font families recap") + prose("""
    <p>Last lesson's <code>font-family</code> only works with fonts on the visitor's machine, so a <span class="term">font stack</span> lists alternatives, ending with a generic family:</p>
    <pre class="snippet" data-lang="css">p {
  font-family: "Helvetica", "Trebuchet MS", "Verdana", sans-serif;
}</pre>
    <p>That limits you to the few web safe fonts, unless the font comes with the page.</p>""")
b += ST("Read", "Web fonts") + prose("""
    <p>A <span class="term">web font</span> is a font file the browser downloads along with your CSS. You declare it with an <code>@font-face</code> rule, which gives the font a name and says where the file is, and then use that name like any other:</p>
    <pre class="snippet" data-lang="css">@font-face {
  font-family: "Trail Sans";
  src: url("fonts/trail-sans.woff2") format("woff2");
}

html {
  font-family: "Trail Sans", "Trebuchet MS", sans-serif;
}</pre>
    <p>Two things to know:</p>
    <ul>
      <li><strong>Use WOFF2.</strong> It's the compressed web font format every current browser supports. You don't need older formats like TTF or EOT.</li>
      <li><strong>Fonts have licences.</strong> Fonts are software. A font installed on your computer isn't necessarily licensed for use on the web; check before you upload one. Free fonts from Google Fonts or Font Squirrel are licensed for the web.</li>
    </ul>
    <p>A web font is a download, and downloads take time or fail. Until it arrives, the browser uses the next font in your stack, so pick a fallback that's similar.</p>""")
b += ST("Play", "Always include a fallback", "If the font fails to load, or hasn't loaded yet, the browser uses the next font in your list. Pick one that's similar.") + fb
b += ST("Read", "Adding your own web fonts") + prose("""
    <h3>Finding fonts</h3>
    <p>Free fonts: <a href="https://fonts.google.com">Google Fonts</a>, <a href="https://www.fontsquirrel.com">Font Squirrel</a>, and the open-source fonts many foundries publish. Paid fonts come from foundries and services like MyFonts. Read the licence either way.</p>
    <h3>Generating the required code</h3>
    <p>If you have a font file in another format, a converter like Transfonter turns it into WOFF2 and writes the <code>@font-face</code> rules for you. Download only the weights and styles you'll use.</p>
    <h3>Implementing the code in your demo</h3>
    <ol>
      <li>Put the <code>.woff2</code> files in a <code>fonts/</code> folder in your project.</li>
      <li>Add an <code>@font-face</code> rule for each file at the top of your stylesheet. The <code>src</code> path is relative to the CSS file.</li>
      <li>Use the name in <code>font-family</code>, with fallbacks.</li>
    </ol>
    <pre class="snippet" data-lang="css">@font-face {
  font-family: "Zantroke";
  src: url("fonts/zantroke-webfont.woff2") format("woff2");
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

h1 {
  font-family: "Zantroke", serif;
}</pre>""")
b += ST("Practice", "Self-host a font", "This project has a real font file in its <code>fonts/</code> folder.") + '  <div id="ex-selfhost"></div>\n\n'
b += ST("Read", "Using an online font service") + prose("""
    <p>Services like Google Fonts host the files and write the CSS for you. Choose a font and its weights, copy the <code>&lt;link&gt;</code> tags they give you into your <code>&lt;head&gt;</code> (above your own stylesheet), then use the name in <code>font-family</code>. It's the quickest way to start, though the visitor's browser now contacts another company's server, and the page depends on it being up.</p>""") + tools + "\n"
b += ST("Practice", "Load a web font properly", "The font names and fallbacks here are broken. Fix them so text always shows, in the right font when it arrives.") + '  <div id="ex-fonts"></div>\n\n'
b += ST("Read", "@font-face in more detail") + prose("""
    <ul>
      <li><code>font-family</code>: the name you'll refer to the font by. It can be anything, but must match exactly where you use it.</li>
      <li><code>src</code>: the path to the file, with <code>format("woff2")</code> so the browser can skip formats it doesn't support. List several files, comma-separated, and it uses the first it can.</li>
      <li><code>font-weight</code> and <code>font-style</code>: which weight and style this file contains. To use regular and bold, write two <code>@font-face</code> rules with the same <code>font-family</code> and different <code>font-weight</code>. If you ask for a bold you didn't load, the browser fakes one by smearing the regular letters.</li>
      <li><code>font-display</code>: what to show while the file downloads. <code>swap</code> shows the fallback straight away and swaps when the font arrives; it's the usual choice.</li>
    </ul>""")
b += ST("Play", "What visitors see while it loads", "Pick a <code>font-display</code> setting and simulate a slow connection where the font takes 2.5 seconds.") + fd
b += ST("Play", "Only load what you use", "Every weight and style is a separate file to download. These sizes are rough estimates for a typical font.") + wt
b += prose("""
    <h3>Variable fonts and other descriptors</h3>
    <p>A <strong>variable font</strong> packs a whole range of weights (and sometimes other qualities) into a single file. Its <code>@font-face</code> gives a range, like <code>font-weight: 300 1000</code>, and then any weight in between works. Extra design axes are set with <code>font-variation-settings</code>. Two more descriptors you may meet: <code>font-stretch</code> (condensed to expanded) and <code>unicode-range</code> (download this file only if the page uses these characters).</p>""")
b += ST("Play", "A variable font", "Recursive, the font this book uses for code, is one variable file. Drag the weight, and try its extra axes.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="control"><label for="vf-w">font-weight</label><input id="vf-w" type="range" min="300" max="1000" step="10" value="400"><span class="readout" id="vf-w-out"></span></div>
      <div class="control"><label for="vf-c">"CASL" (casual)</label><input id="vf-c" type="range" min="0" max="1" step="0.1" value="0"><span class="readout" id="vf-c-out"></span></div>
      <div class="control"><label for="vf-m">"MONO" (monospace)</label><input id="vf-m" type="range" min="0" max="1" step="0.1" value="0"><span class="readout" id="vf-m-out"></span></div>
      <pre class="snippet" id="vf-code"></pre>
    </div>
    <div class="vf-sample" id="vf-out">Royal Arch, 3.4 miles</div>
  </section>

"""
b += notes([
  "<code>@font-face</code> names a font and points to its file; then use the name in <code>font-family</code>.",
  "Use WOFF2, and check the licence.",
  "Always keep fallbacks in the stack, similar in style to the web font.",
  "<code>font-display: swap</code> shows text straight away while the font loads.",
  "Every weight and style is another download, unless it's a variable font.",
], [
  "A <code>font-family</code> name that doesn't exactly match the <code>@font-face</code> name: it fails silently.",
  "A <code>src</code> path relative to the HTML page instead of the CSS file.",
  "Using <code>font-weight: 700</code> after loading only 400, so the browser fakes a bold.",
  "Loading every weight a family offers \"just in case\".",
  "Uploading a font you don't have a web licence for.",
])
first = src.first_script()
js = r'''
  // --- Variable font ---
  function vf() {
    const w = $("vf-w").value, c = $("vf-c").value, m = $("vf-m").value, o = $("vf-out");
    o.style.fontWeight = w; o.style.fontVariationSettings = `"CASL" ${c}, "MONO" ${m}`;
    $("vf-w-out").textContent = w; $("vf-c-out").textContent = c; $("vf-m-out").textContent = m;
    $("vf-code").textContent = `h1 {\n  font-family: "Recursive", sans-serif;\n  font-weight: ${w};\n  font-variation-settings: "CASL" ${c}, "MONO" ${m};\n}`;
  }
  ["vf-w", "vf-c", "vf-m"].forEach((id) => $(id).addEventListener("input", vf));
  vf();
'''
ex_fonts = src.block('  makeExercise(document.getElementById("ex-fonts"), {')
ex_self = r'''  makeExercise(document.getElementById("ex-selfhost"), {
    title: "Atkinson Hyperlegible",
    task: `<p>The file <code>fonts/atkinson-hyperlegible-700-latin.woff2</code> holds the bold weight of Atkinson Hyperlegible, a font designed to be easy to read.</p>
    <ol>
      <li>Write an <code>@font-face</code> rule with <code>font-family: "Atkinson"</code>, the <code>src</code> above with <code>format("woff2")</code>, <code>font-weight: 700</code> and <code>font-display: swap</code>.</li>
      <li>Use it on the <code>h1</code>, with <code>Verdana, sans-serif</code> as fallbacks, and <code>font-weight: 700</code>.</li>
    </ol>`,
    html: `<h1>Bear Peak</h1>
<p>A long, steep climb with the best views in Boulder.</p>`,
    css: `body { font-family: Georgia, serif; }
`,
    solution: { css: `@font-face {
  font-family: "Atkinson";
  src: url("fonts/atkinson-hyperlegible-700-latin.woff2") format("woff2");
  font-weight: 700;
  font-display: swap;
}

body { font-family: Georgia, serif; }

h1 {
  font-family: "Atkinson", Verdana, sans-serif;
  font-weight: 700;
}
` },
    hints: ["@font-face goes at the top of the stylesheet, outside any other rule.", "The name in font-family must match the @font-face name exactly, quotes and all."],
    checks: [
      { label: "An @font-face rule named Atkinson points to the woff2 file", test: ({ doc }) => [...doc.styleSheets[0].cssRules].some((r) => r instanceof doc.defaultView.CSSFontFaceRule && /atkinson/i.test(r.style.getPropertyValue("font-family")) && /atkinson-hyperlegible-700-latin\.woff2/.test(r.style.getPropertyValue("src")) && /woff2/.test(r.style.getPropertyValue("src").replace(/\.woff2/, ""))) },
      { label: "It sets font-weight: 700 and font-display: swap", test: ({ doc }) => [...doc.styleSheets[0].cssRules].some((r) => r instanceof doc.defaultView.CSSFontFaceRule && /700|bold/.test(r.style.getPropertyValue("font-weight")) && r.style.getPropertyValue("font-display") === "swap") },
      { label: "The h1 uses \"Atkinson\", Verdana, sans-serif at weight 700", test: ({ style }) => /^"?Atkinson"?,\s*Verdana,\s*sans-serif$/.test(style("h1", "font-family")) && style("h1", "font-weight") === "700" },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Which font format should you use on the web?", opts: ["WOFF2", "TTF", "EOT"], a: 0, why: "WOFF2 is compressed and supported by every current browser." },
    { id: "q6", q: "A font is installed on your laptop. Can you upload it to your site?", opts: ["Only if its licence allows web use", "Yes, always", "Only if you rename it"], a: 0, why: "Fonts are licensed software; check the licence." },
  ]);
''')
write("core-web-fonts.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_self + "\n" + ex_fonts + "\n" + quiz + "</script>\n")
