import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("fluid-sizing")
def sub(s, a, b):
    assert a in s, a
    return s.replace(a, b, 1)
pg_clamp = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="vw">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Columns that fit')
pg_clamp = sub(pg_clamp, '<span style="--c:var(--item-2)"><i></i>fixed rem</span>', '<span style="--c:var(--item-2)"><i></i>fixed rem</span><span style="--c:var(--item-3)"><i></i>media query</span>')
pg_minmax = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="pw">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Recipes')
recipes = src.between('  <section class="recipes" id="recipes"></section>', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Fluid Sizing", src.css(), """
  .zm-rows { display: grid; gap: 8px; }
  .zm-row { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 8px 12px; display: grid; gap: 2px; overflow: hidden; }
  .zm-row .s { font-family: var(--font-display); font-weight: 800; line-height: 1.1; white-space: nowrap; }
  .zm-row .px { font: 0.8rem var(--font-code); font-variation-settings: "MONO" 1; color: var(--muted); }
  .zm-row .px.bad { color: var(--bad); } .zm-row .px.ok { color: var(--good); }
""")
b = top("Fluid Sizing", "Media queries change sizes in jumps. Viewport units and the math functions <code>calc()</code>, <code>min()</code>, <code>max()</code> and <code>clamp()</code> let text and spacing change smoothly with the screen, inside limits you set, often with no media query at all.", [
  "Make text responsive with media queries and with viewport units, and explain why <code>vw</code> alone is a problem.",
  "Make text and spacing grow smoothly with <code>clamp()</code>.",
  "Set upper and lower limits with <code>min()</code> and <code>max()</code>, and mix units with <code>calc()</code>.",
])
b += ST("Read", "Using media queries for responsive typography") + prose("""
    <p>A heading that suits a laptop can be far too big for a phone, where a long word might not even fit across the screen. The simplest fix is a media query that steps the size up on wide screens:</p>
    <pre class="snippet" data-lang="css">h1 { font-size: 2rem; }

@media (width >= 1200px) {
  h1 { font-size: 4rem; }
}</pre>
    <p>That works, but it jumps: at 1199px the heading is 32px, at 1200px it doubles. More breakpoints give smaller jumps, at the cost of more CSS.</p>""")
b += ST("Read", "Using viewport units for responsive typography") + prose("""
    <p>Viewport units grow smoothly: <code>font-size: 6vw</code> is 6% of the window's width, so the heading scales continuously as the window changes. But <strong>never size text with <code>vw</code> alone</strong>. A size that depends only on the window ignores the reader's settings. A bigger default text size has no effect on it at all, and zooming in makes the window narrower in CSS pixels, so the <code>vw</code> size shrinks by exactly as much as the zoom enlarges it. People who need larger text can't get it.</p>
    <p>The fix is to mix in a unit that does respond to zoom, with <code>calc()</code>:</p>
    <pre class="snippet" data-lang="css">h1 {
  font-size: calc(1.5rem + 4vw);
}</pre>
    <p>Now the heading still grows with the window, and the <code>1.5rem</code> part grows when someone zooms.</p>""")
b += ST("Play", "Text size when someone zooms", "Pretend the window is 400px wide, then raise the browser's text size, as someone with low vision might.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="zm-z">browser text size</label><input id="zm-z" type="range" min="100" max="200" step="10" value="100"><span class="readout" id="zm-z-out"></span></div>
      <p class="hint">At 100%, 1rem is 16px. At 200%, it's 32px. The window stays 400px wide.</p>
    </div>
    <div class="zm-rows" id="zm-rows"></div>
  </section>

"""
b += ST("Read", "clamp(): grow, within limits") + prose("""
    <p><code>calc(1.5rem + 4vw)</code> still has no limits: on a huge monitor it gets enormous. <span class="term">clamp()</span> adds them. It takes three values, always in this order: a minimum, a preferred value and a maximum.</p>
    <pre class="snippet" data-lang="css">h1 {
  font-size: clamp(1.75rem, 1rem + 3vw, 3.5rem);
}</pre>
    <p>The preferred value, <code>1rem + 3vw</code>, grows as the window widens. <code>clamp()</code> keeps it between 28px and 56px, so the heading is never tiny on a phone or enormous on a big monitor. One line replaces several media queries, and the <code>rem</code> keeps it zoomable.</p>""")
b += ST("Play", "Four ways to size a heading", "Drag the window width and compare a fixed size, a media query, vw alone and clamp().") + pg_clamp
b += ST("Read", "min(), max() and calc()") + prose("""
    <p><span class="term" data-term="min() / max()">min()</span> and <span class="term" data-term="min() / max()">max()</span> pick one of their values. <code>width: min(100%, 600px)</code> uses whichever is smaller, so the box fills the screen on phones but never grows past 600px. It works like <code>max-width</code>. <code>max()</code> sets a floor instead: <code>padding: max(10px, 4vw)</code> is never less than 10px. The names feel backwards at first: <code>min()</code> sets an upper limit.</p>
    <p><span class="term">calc()</span> mixes units: <code>calc(100% - 2rem)</code> means "the full width, minus 32px." Inside <code>clamp()</code>, <code>min()</code> and <code>max()</code> you can do math without writing <code>calc()</code>.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p><code>calc(100%-2rem)</code> is silently ignored. The <code>+</code> and <code>-</code> in <code>calc()</code> need a space on each side: <code>calc(100% - 2rem)</code>.</p></div>""")
b += ST("Play", "Columns that fit with min() and max()", "<code>min()</code> picks the smallest of its values, <code>max()</code> the largest. They're perfect for \"this wide, but never wider than the screen\" and \"at least this much padding.\"") + pg_minmax
b += ST("Look", "Recipes worth keeping", "Copy these into your own stylesheet. Each one replaces a media query or two.") + recipes
b += ST("Practice", "Size with clamp(), min() and calc()", "Replace fixed sizes with ones that grow smoothly, within limits.") + '  <div id="ex-fluid"></div>\n\n'
b += ST("Practice", "Responsive typography", "From MDN's mobile-first challenge: headings that scale without wrapping, and body text that steps up on wide screens.") + '  <div id="ex-type"></div>\n\n'
b += notes([
  "Media queries change text size in steps; viewport units change it smoothly.",
  "Never size text in <code>vw</code> alone: it ignores zoom. Mix in <code>rem</code>: <code>calc(1.5rem + 4vw)</code>.",
  "<code>clamp(1.75rem, 1rem + 3vw, 3.5rem)</code>: grow with the window, but stay between 28px and 56px.",
  "<code>min()</code> sets an upper limit (like <code>max-width</code>), <code>max()</code> a lower limit.",
  "These work anywhere a length works: font sizes, widths, padding, gap and grid tracks.",
], [
  "Leaving out the spaces: <code>calc(100%-2rem)</code> is ignored.",
  "Sizing text in <code>vw</code> alone, so it doesn't grow when people zoom.",
  "Putting <code>clamp()</code>'s values in the wrong order. It's always min, preferred, max.",
  "Using <code>100vw</code> for widths on a page with a scrollbar, which causes sideways scrolling. Use <code>100%</code>.",
])
first = src.first_script()
first = sub(first, "return { fixed: 2.5 * REM,", "return { mq: (w >= 1200 ? 4 : 2) * REM, fixed: 2.5 * REM,")
first = sub(first, '      row("--item-4", "font-size: 6vw"', '      row("--item-3", "2rem, then 4rem at width >= 1200px", s.mq, w >= 1100 && w < 1200 ? "about to jump to double" : "") +\n      row("--item-4", "font-size: 6vw"')
first = sub(first, '<path d="${path("vw")}"', '<path d="${path("mq")}" fill="none" stroke="var(--item-3)" stroke-width="2.5"/><path d="${path("vw")}"')
js = r'''
  // --- zoom ---
  function zmUpdate() {
    const z = +$("zm-z").value / 100, rem = 16 * z, W = 400;
    $("zm-z-out").textContent = Math.round(z * 100) + "%";
    const rows = [
      ["font-size: 6vw", 0.06 * W],
      ["font-size: calc(1.5rem + 4vw)", 1.5 * rem + 0.04 * W],
      ["font-size: clamp(1.75rem, 1rem + 3vw, 3.5rem)", Math.min(3.5 * rem, Math.max(1.75 * rem, rem + 0.03 * W))],
      ["font-size: 2rem", 2 * rem],
    ];
    const base = [24, 40, 28, 32];
    $("zm-rows").innerHTML = rows.map(([code, px], i) => {
      const grew = px > base[i] + 0.5;
      return `<div class="zm-row"><code>${code}</code><span class="s" style="font-size:${px}px">Weekend Hikes</span><span class="px ${z === 1 ? "" : grew ? "ok" : "bad"}">${Math.round(px)}px${z === 1 ? "" : grew ? ` · grew from ${base[i]}px` : " · didn't change at all"}</span></div>`;
    }).join("");
  }
  $("zm-z").addEventListener("input", zmUpdate);
  zmUpdate();
'''
ex_f = src.block('  makeExercise(document.getElementById("ex-fluid"), {')
ex_t = r'''  makeExercise(document.getElementById("ex-type"), {
    title: "Headings that scale",
    task: `<ol>
      <li>Make the <code>h1</code> grow with the window but stay zoomable: <code>calc(1.3rem + 3vw)</code>.</li>
      <li>Make the <code>h2</code> grow too, but keep it between <code>1.25rem</code> and <code>2rem</code> with <code>clamp()</code>, using <code>1rem + 2vw</code> as the preferred value.</li>
      <li>Body text should be <code>1rem</code>, stepping up to <code>1.125rem</code> on screens <code>60em</code> and wider.</li>
    </ol>`,
    html: `<h1>Boulder Trails</h1>
<h2>Royal Arch</h2>
<p>A steep 1.7-mile climb through ponderosa pine to a sandstone arch.</p>`,
    css: `body { font-family: system-ui, sans-serif; }
h1 { font-size: 3rem; margin: 0; }
h2 { font-size: 6vw; margin: 0; }
`,
    solution: { css: `body { font-family: system-ui, sans-serif; font-size: 1rem; }
h1 { font-size: calc(1.3rem + 3vw); margin: 0; }
h2 { font-size: clamp(1.25rem, 1rem + 2vw, 2rem); margin: 0; }

@media (width >= 60em) {
  body { font-size: 1.125rem; }
}
` },
    hints: [
      "calc() mixes rem and vw: calc(1.3rem + 3vw). Spaces around the +.",
      "clamp(min, preferred, max): clamp(1.25rem, 1rem + 2vw, 2rem).",
      "body { font-size: 1rem; } then @media (width >= 60em) { body { font-size: 1.125rem; } }",
    ],
    checks: (() => {
      const rules = (doc) => [...doc.styleSheets[0].cssRules];
      const top = (doc, sel) => rules(doc).find((r) => r.selectorText === sel);
      return [
        { label: "The h1 uses calc(1.3rem + 3vw)", test: ({ doc }) => /^calc\(1\.3rem \+ 3vw\)$/.test(top(doc, "h1").style.fontSize) },
        { label: "The h2 uses clamp(1.25rem, 1rem + 2vw, 2rem)", test: ({ doc, style }) => { const px = parseFloat(style("h2", "font-size")); return /^clamp\(1\.25rem, ?(calc\()?1rem \+ 2vw\)?, ?2rem\)$/.test(top(doc, "h2").style.fontSize) && px >= 20 && px <= 32; } },
        { label: "Body text is 1rem", test: ({ doc }) => top(doc, "body") && top(doc, "body").style.fontSize === "1rem" },
        { label: "At 60em and wider, body text is 1.125rem", test: ({ doc }) => rules(doc).some((m) => m.media && /^\((width>=60em|min-width:60em)\)$/.test(m.conditionText.replace(/\s/g, "")) && [...m.cssRules].some((r) => r.selectorText === "body" && r.style.fontSize === "1.125rem")) },
      ];
    })(),
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Someone sets their browser text size to 200%. A heading with font-size: 6vw…", opts: ["Doubles in size", "Stays exactly the same", "Disappears"], a: 1, why: "vw depends only on the window's width, so zoom doesn't affect it. Mix in rem." },
    { id: "q6", q: "What does a media query do to a font size that clamp() doesn't?", opts: ["It changes the size in jumps at breakpoints", "It keeps the text zoomable", "It sets a maximum"], a: 0, why: "Media queries step the size; clamp() changes it smoothly within limits." },
  ]);
''')
write("core-fluid-sizing.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_f + "\n" + ex_t + "</script>\n")
