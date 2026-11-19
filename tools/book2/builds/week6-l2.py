import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("mobile-first")
steps = src.between('  <div class="steps" id="steps"', '  <div class="section-title"><span class="eyebrow">Before you hand it in</span>')
checklist = src.between('  <ul class="checklist" id="checklist"></ul>', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Responsive Design and Mobile First", src.css(), """
  #lt-code { white-space: pre-wrap; overflow-wrap: anywhere; }
  .lt-outer { background: var(--stage); border: 2px dashed var(--line); border-radius: var(--radius); padding: 12px; overflow: hidden; }
  .lt-page { background: #fff; color: #1d2133; transform-origin: top left; padding: 14px; font-family: var(--font-body); }
  .lt-page h4 { margin: 0 0 10px; font: 800 1.1rem var(--font-display); color: #0b6b5e; }
  .lt-cols > div { border-radius: 6px; padding: 12px; min-height: 120px; font-size: 0.9rem; }
  .lt-cols .c1 { background: #eef1f8; } .lt-cols .c2 { background: #fff4ec; }
  .vm-wrap { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }
  .vm-dev { display: grid; gap: 6px; justify-items: center; }
  .vm-dev .cap { font: 600 0.8rem var(--font-code); font-variation-settings: "MONO" 1; color: var(--muted); }
  .vm-phone { width: 200px; height: 360px; border: 8px solid #2b2f3d; border-radius: 22px; overflow: hidden; background: #fff; position: relative; }
  .vm-page { position: absolute; top: 0; left: 0; transform-origin: top left; color: #1d2133; font-family: var(--font-body); padding: 12px; box-sizing: border-box; }
  .vm-page h4 { margin: 0 0 6px; font: 800 1.4rem var(--font-display); color: #0b6b5e; }
  .vm-page p { margin: 0 0 8px; font-size: 16px; }
  .vm-page .vm-cards { display: grid; gap: 8px; }
  .vm-page .vm-cards i { display: block; height: 60px; border-radius: 6px; background: #2340d9; opacity: 0.8; }
""")
b = top("Responsive Design and Mobile First", "Responsive design is the idea that one page should work on every screen, by adapting its layout instead of serving a separate mobile site. Mobile first is the way to build it: start with the phone, and add to it as the screen grows.", [
  "Explain what makes a design responsive: fluid layouts, flexible media and media queries.",
  "Use flexbox and grid to build layouts that adapt.",
  "Explain why the viewport meta tag is needed.",
  "Build a page mobile first, adding <code>min-width</code> queries for wider screens.",
])
b += ST("Read", "Precursor to responsive design: mobile web design") + prose("""
    <p>When phones first got web browsers, many companies built a second, separate mobile site (often at an address like <code>m.example.com</code>) and used code on the server to guess which device was asking. Two sites meant twice the work, and the guessing often went wrong: tablets got the phone site, new phones got the desktop one.</p>
    <p>Phones are still different from laptops in ways that matter, like slower connections and battery life. But the answer today is one site that adapts.</p>""")
b += ST("Read", "Introducing responsive web design") + prose("""
    <p>The term <strong>responsive web design</strong> was coined by Ethan Marcotte in 2010. It combines three ideas:</p>
    <ul>
      <li><strong>Fluid layouts</strong>: columns sized in percentages or <code>fr</code>, not fixed pixels, so they stretch and shrink with the window.</li>
      <li><strong>Flexible media</strong>: images and video that shrink to fit, with <code>max-width: 100%</code>.</li>
      <li><strong>Media queries</strong>: rules that change the layout at certain widths.</li>
    </ul>
    <p>Here's a useful fact: HTML is responsive by default. Text wraps, blocks fill the width they're given. Most responsive problems come from CSS that fixes a size, like a <code>width: 960px</code> wrapper from the days when every screen was a desktop.</p>""")
b += ST("Read", "Media Queries") + prose("""
    <p>You met media queries in the <a href="core-media-queries.html">last lesson</a>. In responsive design, each one marks a <span class="term">breakpoint</span> where the layout changes, for example from one column to two:</p>
    <pre class="snippet" data-lang="css">@media screen and (width >= 80rem) {
  .container { margin: 1em 2em; }
}</pre>
    <p>Use relative units like <code>em</code> or <code>rem</code> for breakpoints where you can, and remember that a flexible layout may not need many queries at all.</p>""")
b += ST("Read", "Responsive layout technologies") + prose("""
    <p>Modern layout tools are flexible by design, which is half the work of responsive design.</p>
    <h3>Flexbox</h3>
    <p>Flex items grow and shrink to share the space: <code>flex: 1</code> and <code>flex: 2</code> make the second column twice the width of the first at any window size.</p>
    <pre class="snippet" data-lang="css">@media (width >= 600px) {
  .wrapper { display: flex; }
  .col1 { flex: 1; margin-right: 5%; }
  .col2 { flex: 2; }
}</pre>
    <h3>CSS grid</h3>
    <p>The <code>fr</code> unit does the same in a grid:</p>
    <pre class="snippet" data-lang="css">@media (width >= 600px) {
  .wrapper {
    display: grid;
    grid-template-columns: 1fr 2fr;
    column-gap: 5%;
  }
}</pre>""")
b += ST("Play", "Fixed, flex and grid", "Change the window width. Compare a fixed-width layout with the flexible ones, then let them stack on narrow screens.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="lt-w">window width</label><input id="lt-w" type="range" min="320" max="1200" step="10" value="420"><span class="readout" id="lt-w-out"></span></div>
      <div class="control"><label for="lt-m">layout</label><select id="lt-m"><option value="fixed">fixed: 640px + 320px</option><option value="flex" selected>flex: 1 and flex: 2</option><option value="grid">grid: 1fr 2fr</option></select></div>
      <label class="toggle"><input type="checkbox" id="lt-mq"> only use two columns at <code>width &gt;= 600px</code></label>
      <pre class="snippet" id="lt-code"></pre>
    </div>
    <div class="stage-col">
      <div class="lt-outer" id="lt-outer"><div class="lt-page" id="lt-page"><h4>Trailhead</h4><div class="lt-cols" id="lt-cols"><div class="c1">Sidebar: trail list, filters.</div><div class="c2">Main: the trail description, photos and a map of Royal Arch.</div></div></div></div>
      <p class="verdict" id="lt-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += ST("Read", "Responsive images/media") + prose("""
    <p>Images, video and other embeds have a fixed size, so they need one rule to make them fluid:</p>
    <pre class="snippet" data-lang="css">img, picture, video {
  max-width: 100%;
  height: auto;
}</pre>
    <p>That stops them overflowing, but a phone still downloads the big file. HTML has tools for sending a smaller file or a different crop, which are the subject of <a href="core-responsive-images.html">Responsive Images</a>. And where you can, use CSS gradients and shadows instead of image files: they're tiny and sharp at any size.</p>""")
b += ST("Read", "Responsive typography") + prose("""
    <p>Text should change size too: a heading that looks right on a laptop may be too big for a phone. You can step the size up with media queries:</p>
    <pre class="snippet" data-lang="css">h1 { font-size: 2rem; }
@media (width >= 1200px) {
  h1 { font-size: 4rem; }
}</pre>
    <p>Or make it grow smoothly with the window by mixing in viewport units, as in <code>font-size: calc(1.5rem + 4vw)</code>. Never use <code>vw</code> on its own for text: it doesn't grow when people zoom in. <a href="core-fluid-sizing.html">Fluid Sizing</a> covers this, and <code>clamp()</code>, in detail.</p>""")
b += ST("Read", "The viewport meta tag") + prose("""
    <p>Every responsive page needs this line in its <code>&lt;head&gt;</code>:</p>
    <pre class="snippet" data-lang="html">&lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;</pre>
    <p>When phones first got browsers, most sites were built for desktop widths. So mobile browsers pretend the screen is about 980px wide, lay the page out at that size, then shrink the whole thing to fit. That kept old sites readable, sort of. But it also means your phone layout never switches on, because the browser says it's 980px wide. The viewport meta tag says "this page is built for real device widths", so the browser uses the phone's actual width.</p>""")
b += ST("Play", "With and without the viewport meta tag", "The same page on the same phone. Change the phone's width.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="vm-w">phone width</label><input id="vm-w" type="range" min="320" max="430" step="5" value="375"><span class="readout" id="vm-w-out"></span></div>
      <p class="hint" id="vm-out" aria-live="polite"></p>
    </div>
    <div class="vm-wrap">
      <div class="vm-dev"><span class="cap">no viewport meta</span><div class="vm-phone"><div class="vm-page" id="vm-a"></div></div></div>
      <div class="vm-dev"><span class="cap">with viewport meta</span><div class="vm-phone"><div class="vm-page" id="vm-b"></div></div></div>
    </div>
  </section>

"""
b += ST("Read", "Building mobile first") + prose("""
    <p>Now put it together. There are two ways to make a site responsive. You can design for a laptop and then squeeze it onto a phone, undoing styles as the screen shrinks. Or you can start with the phone and <em>add</em> to it as the screen grows. The second way is <span class="term">mobile first</span>, and it almost always means less CSS and fewer bugs.</p>
    <p>The phone layout is usually the simplest: one column, everything stacked, full width. So your base styles, outside any media query, describe the phone version, and each <code>min-width</code> query adds only what changes on wider screens. You never write a rule just to undo another one.</p>
    <p>Mobile first also applies to content. If something is too much for a phone, ask whether it's needed at all, rather than hiding it on small screens.</p>
    <div class="callout tip"><p class="callout-title">Tip</p><p>Narrowing your browser window is a good first check, but test on a real phone too. Touch targets, real font sizes and the on-screen keyboard only show up on the real thing.</p></div>""")
b += ST("Play", "Build a page step by step", "Step through how one page comes together, and watch it on three screen sizes at once.") + steps
b += ST("Practice", "Flip it to mobile first", "This page is built for the desktop and then undone for phones. Rewrite it to start with the phone.") + '  <div id="ex-mf"></div>\n\n'
b += ST("Practice", "Challenge: a mobile-first layout", "Based on MDN's mobile-first challenge. The phone layout is done; add a middle layout, a wide layout and print styles.") + '  <div id="ex-challenge"></div>\n\n'
b += ST("Before you hand it in", "Responsive checklist", "Tick these off for your own project. Your checks are saved in this browser only.") + checklist
b += notes([
  "Responsive design = fluid layouts + flexible media + media queries.",
  "HTML is responsive by default; fixed widths are what break it.",
  "<code>flex: 1</code> / <code>flex: 2</code> and <code>1fr 2fr</code> give columns that adapt to any width.",
  "Without the viewport meta tag, phones lay pages out at about 980px and shrink them.",
  "Mobile first: base styles are the phone layout; <code>min-width</code> queries only add.",
], [
  "Designing for a laptop, then cramming it onto a phone with lots of <code>max-width</code> overrides.",
  "Fixed widths like <code>width: 960px</code> on a wrapper, which cause sideways scrolling on phones.",
  "Forgetting the viewport meta tag.",
  "Hiding important content on mobile instead of rearranging it.",
])
first = src.first_script()
js = r'''
  // --- Fixed, flex and grid ---
  function ltUpdate() {
    const w = +$("lt-w").value, m = $("lt-m").value, mq = $("lt-mq").checked, page = $("lt-page"), cols = $("lt-cols");
    $("lt-w-out").textContent = w + "px";
    const two = !mq || w >= 600;
    page.style.width = w + "px";
    const [c1, c2] = cols.children;
    cols.style.cssText = ""; c1.style.cssText = ""; c2.style.cssText = "";
    if (m === "fixed") { cols.style.display = "flex"; c1.style.flex = "0 0 320px"; c2.style.flex = "0 0 640px"; cols.style.width = "960px"; if (!two) { cols.style.display = "block"; c1.style.marginBottom = "10px"; } }
    else if (two && m === "flex") { cols.style.display = "flex"; c1.style.flex = "1"; c1.style.marginRight = "5%"; c2.style.flex = "2"; }
    else if (two && m === "grid") { cols.style.display = "grid"; cols.style.gridTemplateColumns = "1fr 2fr"; cols.style.columnGap = "5%"; }
    else c1.style.marginBottom = "10px";
    const avail = $("lt-outer").clientWidth - 24, scale = Math.min(1, avail / w);
    page.style.transform = `scale(${scale})`;
    $("lt-outer").style.height = page.offsetHeight * scale + 28 + "px";
    const rule = m === "fixed" ? ".wrapper { width: 960px; }\n.col1 { width: 320px; }\n.col2 { width: 640px; }" : m === "flex" ? ".wrapper { display: flex; }\n.col1 { flex: 1; margin-right: 5%; }\n.col2 { flex: 2; }" : ".wrapper {\n  display: grid;\n  grid-template-columns: 1fr 2fr;\n  column-gap: 5%;\n}";
    $("lt-code").textContent = mq ? "@media (width >= 600px) {\n" + rule.replace(/^/gm, "  ") + "\n}" : rule;
    const over = cols.scrollWidth > w - 28 + 1 || (m === "fixed" && w < 988);
    let msg;
    if (m === "fixed" && two) msg = w < 988 ? `The layout is 960px wide whatever the window, so at ${w}px it sticks out and the page scrolls sideways.` : "Fits, but only because this window is wider than 960px.";
    else if (m === "fixed") msg = "Stacked below 600px, but each column is still a fixed width, so it can still overflow.";
    else if (!two) msg = "Below 600px the columns stack, which suits a phone.";
    else msg = w < 600 ? "Flexible columns fit at any width, but at this size the sidebar is squeezed very narrow. Turn on the media query." : "The columns share the space in a 1 : 2 ratio at any width.";
    $("lt-out").className = "verdict" + (over || (two && w < 600 && m !== "fixed") ? " bad" : "");
    $("lt-out").textContent = msg;
  }
  ["lt-w", "lt-m", "lt-mq"].forEach((id) => $(id).addEventListener("input", ltUpdate));
  window.addEventListener("resize", ltUpdate);
  ltUpdate();

  // --- viewport meta ---
  const VM = `<h4>Trailhead</h4><p>Weekend hikes near Boulder, with maps and conditions.</p><div class="vm-cards"><i></i><i></i><i></i></div>`;
  $("vm-a").innerHTML = VM; $("vm-b").innerHTML = VM;
  function vmUpdate() {
    const w = +$("vm-w").value, frame = 184;
    $("vm-w-out").textContent = w + "px";
    // Without the tag: laid out at 980px, then shrunk to the phone's width.
    $("vm-a").style.width = "980px"; $("vm-a").querySelector(".vm-cards").style.gridTemplateColumns = "repeat(3, 1fr)";
    $("vm-a").style.transform = `scale(${frame / 980})`;
    // With the tag: laid out at the real width (the phone is drawn at frame px, so scale that).
    $("vm-b").style.width = w + "px"; $("vm-b").querySelector(".vm-cards").style.gridTemplateColumns = "1fr";
    $("vm-b").style.transform = `scale(${frame / w})`;
    $("vm-out").textContent = `Without the tag, the browser lays the page out at 980px and shrinks it to fit ${w}px, so 16px text shows at about ${(16 * w / 980).toFixed(1)}px and a (min-width: 600px) query is true. With it, the layout is ${w}px wide, text is a real 16px, and your phone styles apply.`;
  }
  $("vm-w").addEventListener("input", vmUpdate);
  vmUpdate();
'''
NORM = '\n      const norm = (t) => t.replace(/\\s/g, "").replace(/^\\(width>=(\\d+)px\\)$/, "(min-width:$1px)");'
ex_mf = src.block('  makeExercise(document.getElementById("ex-mf"), {')
ex_mf = ex_mf.replace("checks: (() => {", "checks: (() => {" + NORM, 1).replace('m.conditionText.replace(/\\s/g, "")', "norm(m.conditionText)")
assert 'conditionText.replace(/\\s/g, "")' not in ex_mf
ex_c = r'''  makeExercise(document.getElementById("ex-challenge"), {
    title: "Middle, wide and print layouts",
    task: `<ol>
      <li>Give <code>nav</code>, <code>article</code> and <code>aside</code> the grid areas <code>nav</code>, <code>main</code> and <code>photos</code>.</li>
      <li>At <code>800px</code> and wider: hide the menu button, make <code>nav</code> sticky at <code>top: 0</code>, and lay out <code>.grid</code> with the areas <code>"nav nav" "main photos"</code>, columns <code>3fr 1fr</code> and a <code>20px</code> gap.</li>
      <li>At <code>1300px</code> and wider: change <code>.grid</code> to the areas <code>"nav main photos"</code> with columns <code>1fr 3fr 1fr</code>.</li>
      <li>When printing, hide the <code>nav</code> and the button.</li>
    </ol>
    <p>The preview is narrow, so you'll mostly see the phone layout. The checks read your CSS.</p>`,
    html: `<header><h1>Trailhead</h1><button class="menu-btn" aria-label="Open menu">☰</button></header>
<main class="grid">
  <nav><ul><li><a href="#">Trails</a></li><li><a href="#">Maps</a></li><li><a href="#">Gear</a></li></ul></nav>
  <article><h2>Royal Arch</h2><p>A steep 1.7-mile climb through ponderosa pine to a sandstone arch.</p></article>
  <aside><img src="arch.jpg" alt="Royal Arch" width="300" height="200"></aside>
</main>`,
    css: `* { box-sizing: border-box; }
body { font-family: system-ui, sans-serif; margin: 0 auto; width: 90%; }
img { max-width: 100%; height: auto; }
nav { background: white; }
nav ul { list-style: none; padding: 0; display: flex; gap: 12px; }
.grid { display: grid; gap: 12px; }
`,
    solution: { css: `* { box-sizing: border-box; }
body { font-family: system-ui, sans-serif; margin: 0 auto; width: 90%; }
img { max-width: 100%; height: auto; }
nav { background: white; grid-area: nav; }
article { grid-area: main; }
aside { grid-area: photos; }
nav ul { list-style: none; padding: 0; display: flex; gap: 12px; }
.grid { display: grid; gap: 12px; }

@media (width >= 800px) {
  .menu-btn { display: none; }
  nav { position: sticky; top: 0; }
  .grid {
    grid-template-areas: "nav nav" "main photos";
    grid-template-columns: 3fr 1fr;
    gap: 20px;
  }
}

@media (width >= 1300px) {
  .grid {
    grid-template-areas: "nav main photos";
    grid-template-columns: 1fr 3fr 1fr;
  }
}

@media print {
  nav, .menu-btn { display: none; }
}
` },
    hints: [
      "grid-area goes on each child: nav { grid-area: nav; } and so on. Outside any query is fine.",
      "Each layout is one media query: @media (width >= 800px) { … } then @media (width >= 1300px) { … }.",
      "grid-template-areas takes one quoted string per row: \"nav nav\" \"main photos\".",
      "@media print { nav, .menu-btn { display: none; } }",
    ],
    checks: (() => {
      const all = (doc) => [...doc.styleSheets[0].cssRules];
      const norm = (t) => t.replace(/\s/g, "").replace(/^\(width>=(\d+)px\)$/, "(min-width:$1px)").replace(/^screenand/, "");
      const at = (doc, cond) => all(doc).filter((r) => r.media && norm(r.conditionText) === cond).flatMap((m) => [...m.cssRules]);
      const has = (rules, sel, fn) => rules.some((r) => r.selectorText && r.selectorText.split(",").map((s) => s.trim()).includes(sel) && fn(r.style));
      const areas = (s) => s.gridTemplateAreas.replace(/\s+/g, " ");
      const everywhere = (doc) => all(doc).flatMap((r) => (r.media ? [...r.cssRules] : [r]));
      return [
        { label: "nav, article and aside have grid areas", test: ({ doc }) => [["nav", "nav"], ["article", "main"], ["aside", "photos"]].every(([sel, a]) => has(everywhere(doc), sel, (s) => s.gridArea.split(" / ")[0] === a)) },
        { label: "At 800px: button hidden, nav sticky at top 0", test: ({ doc }) => { const r = at(doc, "(min-width:800px)"); return has(r, ".menu-btn", (s) => s.display === "none") && has(r, "nav", (s) => s.position === "sticky" && s.top === "0px"); } },
        { label: "At 800px: two-column grid with areas and a 20px gap", test: ({ doc }) => has(at(doc, "(min-width:800px)"), ".grid", (s) => areas(s) === '"nav nav" "main photos"' && s.gridTemplateColumns === "3fr 1fr" && s.columnGap === "20px") },
        { label: "At 1300px: three columns, 1fr 3fr 1fr", test: ({ doc }) => has(at(doc, "(min-width:1300px)"), ".grid", (s) => areas(s) === '"nav main photos"' && s.gridTemplateColumns === "1fr 3fr 1fr") },
        { label: "Print hides the nav and the button", test: ({ doc }) => { const r = at(doc, "print"); return has(r, "nav", (s) => s.display === "none") && has(r, ".menu-btn", (s) => s.display === "none"); } },
      ];
    })(),
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "What are the three ingredients of responsive design?", opts: ["Fluid layouts, flexible media and media queries", "JavaScript, cookies and a mobile site", "Pixels, points and inches"], a: 0, why: "Ethan Marcotte's original recipe, still the basis today." },
    { id: "q6", q: "Without the viewport meta tag, how wide does a phone browser lay out the page?", opts: ["Its real width", "About 980px, then shrinks it", "1280px"], a: 1, why: "That's why phone styles never switch on without the tag." },
  ]);
''')
write("core-mobile-first.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_mf + "\n" + ex_c + "</script>\n")
