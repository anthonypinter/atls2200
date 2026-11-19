import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("sizing")
pg_w = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="pw">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>height vs min-height')
pg_h = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="paras">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>aspect-ratio')
pg_ar = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="ratio">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Sizing", src.css(), """
  .is-stage { background: var(--stage); border-radius: 8px; padding: 16px; display: grid; gap: 10px; align-content: start; min-height: 220px; }
  .is-box { border: 3px solid var(--cobalt); border-radius: 6px; background: var(--panel); font-size: 0.92rem; }
  .is-box p { margin: 6px 10px; }
  .is-box img { display: block; }
  .is-after { margin: 0; padding: 6px 8px; border-radius: 6px; background: var(--item-3); color: #fff; font-size: 0.85rem; }
  .pc-stage { background: var(--stage); border-radius: 8px; padding: 14px; overflow-x: auto; }
  .pc-parent { border: 2px dashed var(--prop); border-radius: 6px; }
  .pc-child { background: color-mix(in srgb, var(--cobalt) 30%, transparent); outline: 2px solid var(--cobalt); outline-offset: -2px; font: 600 0.85rem var(--font-code); font-variation-settings: "MONO" 1; }
  .pc-child span { display: block; background: var(--panel); padding: 6px; text-align: center; }
  .mw-stage { background: var(--stage); border-radius: 8px; padding: 14px; overflow: hidden; }
  .mw-box { border: 2px dashed var(--prop); border-radius: 6px; padding: 6px; }
  .mw-box img { display: block; }
""")
b = top("Sizing", "Every box has a size, whether it comes from its content or from you. Knowing which, and choosing values that adapt instead of fixed numbers, is the difference between a layout that works on every screen and one that only works on yours.", [
  "Explain the difference between a box's intrinsic size and a size you set.",
  "Size boxes with percentages, and predict what percentage margins and padding resolve against.",
  "Use <code>min-height</code>, <code>max-width</code> and <code>max-width: 100%</code> on images so content can adapt.",
  "Size things relative to the browser window with <code>vw</code> and <code>vh</code>.",
])
b += ST("Read", "The natural or intrinsic size of things") + prose("""
    <p>HTML elements have a natural size before any CSS touches them. An image is as big as the file's pixel dimensions. A paragraph is as tall as its lines of text. This is its <strong>intrinsic size</strong>: it comes from the content.</p>
    <p>An empty <code>&lt;div&gt;</code> has no content, so it has no height at all. Give it a border and you just see a flat line, the top and bottom borders touching. Put some text inside and it grows to fit.</p>""")
b += ST("Play", "Where size comes from", "Put different content in the same box, then give it a fixed height.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="seg" id="is-seg" role="group" aria-label="Box content">
        <button class="btn" data-c="empty">Empty</button><button class="btn" data-c="text">A little text</button><button class="btn" data-c="lots">Lots of text</button><button class="btn" data-c="img">An image</button>
      </div>
      <label class="toggle"><input type="checkbox" id="is-fixed"> add <code>height: 120px</code></label>
      <p class="verdict" id="is-out" aria-live="polite"></p>
    </div>
    <div class="is-stage"><div class="is-box" id="is-box"></div><p class="is-after">The next element</p></div>
  </section>

"""
b += ST("Read", "Setting a specific size") + prose("""
    <p>You can override the intrinsic size with <code>width</code> and <code>height</code>. That's an <strong>extrinsic size</strong>: it comes from outside the content. A box with <code>height: 120px</code> stays 120px tall whatever is inside, and if the text needs more room it overflows. (The next lesson, <a href="core-overflow.html">Overflow</a>, covers what to do about that.)</p>
    <h3>Using percentages</h3>
    <p>A percentage width is a share of the <strong>containing block</strong>, usually the parent. <code>width: 50%</code> is half of whatever contains it, so the box grows and shrinks with its parent. That's much safer than a fixed width like <code>width: 1000px</code>, which sticks out on a 390px phone and makes the whole page scroll sideways.</p>
    <p>The pattern you'll use constantly combines a percentage with a limit:</p>
    <pre class="snippet" data-lang="css">.content {
  width: 100%;
  max-width: 600px;
}</pre>
    <p>On a phone the box fills the screen. On a big screen it stops at 600px, which keeps lines of text short enough to read. Percentage <em>heights</em> are trickier: they only work if the parent has a set height, which it usually doesn't.</p>""")
b += ST("Play", "Width: fixed, flexible and limited", "Drag the parent's width and compare how each box responds. The numbers are measured live.") + pg_w
b += prose("""
    <h3>Percentage margins and padding</h3>
    <p>Here's a surprise: percentage <code>margin</code> and <code>padding</code> are calculated from the containing block's <strong>width</strong>, even on the top and bottom. So <code>padding: 10%</code> gives the same amount of space on all four sides, and that space changes when the parent gets wider, not taller.</p>
    <pre class="snippet" data-lang="css">.box {
  margin: 10%;    /* 10% of the parent's width, on every side */
  padding: 10%;
}</pre>""")
b += ST("Play", "What 10% means", "Change the parent's width. The top and bottom spacing changes too, even though the parent's height hasn't.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="pc-w">parent width</label><input id="pc-w" type="range" min="200" max="600" step="10" value="400"><span class="readout" id="pc-w-out"></span></div>
      <div class="control"><label for="pc-v">margin and padding</label><select id="pc-v"><option>5%</option><option selected>10%</option><option>15%</option></select></div>
      <p class="hint">Dashed: the parent. Solid: the child's border box. The shaded band is its padding.</p>
    </div>
    <div class="stage-col">
      <div class="pc-stage"><div class="pc-parent" id="pc-parent"><div class="pc-child" id="pc-child"><span>content</span></div></div></div>
      <p class="verdict" id="pc-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += ST("Read", "min- and max- sizes") + prose("""
    <p>Instead of a fixed size, you can set a floor or a ceiling and let the content decide the rest. Text wraps onto more lines as the screen narrows, so a box with a fixed <code>height</code> eventually can't hold it. <code>min-height</code> says "at least this tall", and the box still grows when the content needs it.</p>
    <p><code>max-width</code> works the other way: the box can be narrower but never wider. <code>min-width</code> sets a floor for width.</p>""")
b += ST("Play", "height vs min-height", "Add more text and see which box copes.") + pg_h
b += prose("""
    <h3><code>max-width</code> on images</h3>
    <p>An image is drawn at its intrinsic size, so a 1200px photo in a 400px column sticks out. You could set <code>width: 100%</code>, but that also <em>stretches</em> small images past their natural size, and they go blurry. The standard fix is:</p>
    <pre class="snippet" data-lang="css">img {
  max-width: 100%;
  height: auto;   /* keep the shape when it shrinks */
}</pre>
    <p>Now big images shrink to fit their container, and small ones stay at their natural size.</p>""")
b += ST("Play", "width: 100% vs max-width: 100%", "This image is 120px wide. Make the container bigger and smaller than that.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="mw-w">container width</label><input id="mw-w" type="range" min="70" max="460" step="10" value="320"><span class="readout" id="mw-w-out"></span></div>
      <div class="control"><label for="mw-r">rule on the image</label><select id="mw-r"><option value="none">(nothing)</option><option value="w">width: 100%</option><option value="mw" selected>max-width: 100%</option></select></div>
    </div>
    <div class="stage-col">
      <div class="mw-stage"><div class="mw-box" id="mw-box"><img id="mw-img" alt="A small sample image, 120 by 80 pixels"></div></div>
      <p class="verdict" id="mw-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += ST("Practice", "Size boxes that adapt", "Fixed sizes break on other screens. Make each of these flexible.") + '  <div id="ex-sizing"></div>\n\n'
b += ST("Read", "Viewport units") + prose("""
    <p>The <strong>viewport</strong> is the visible part of the page in the browser window. Viewport units size things relative to it, not to the parent:</p>
    <ul>
      <li><code>1vw</code> is 1% of the viewport's width.</li>
      <li><code>1vh</code> is 1% of the viewport's height.</li>
    </ul>
    <p>So <code>min-height: 100vh</code> makes a banner that fills the screen, and <code>width: 50vw</code> is half the window wide whatever its parent is. On phones, where browser toolbars appear and disappear, <code>100dvh</code> adjusts for them.</p>
    <p>A related tool is <code>aspect-ratio</code>. Set a width and <code>aspect-ratio: 16 / 9</code>, and the browser works out the height, which is perfect for video and image placeholders.</p>""")
b += ST("Play", "aspect-ratio and viewport units", "The second box is sized in vh. Resize your browser window to see it change.") + pg_ar
b += ST("Practice", "Percentages, viewport units and images", "A banner sized by the window, padding that scales with the page, and an image that fits.") + '  <div id="ex-vp"></div>\n\n'
b += notes([
  "Without a set size, a box takes its <strong>intrinsic size</strong> from its content. An empty block has no height.",
  "Percentage widths are a share of the containing block. <code>width: 100%; max-width: 600px</code> fills phones and caps big screens.",
  "Percentage margins and padding use the containing block's <em>width</em>, even on the top and bottom.",
  "Prefer <code>min-height</code> to <code>height</code> for boxes with text, and <code>max-width: 100%</code> for images.",
  "<code>vw</code> and <code>vh</code> are 1% of the viewport's width and height.",
], [
  "Big fixed widths like <code>width: 1000px</code> that overflow on phones.",
  "A percentage <code>height</code> that does nothing because the parent has no set height.",
  "Expecting <code>padding-top: 10%</code> to be 10% of the parent's height.",
  "Using <code>width: 100%</code> on images, which stretches small ones until they blur.",
])
first = src.first_script()
js = r'''
  // --- Where size comes from ---
  const IS_IMG = "data:image/svg+xml," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="160" height="100"><rect width="160" height="100" fill="#0b6b5e"/><text x="80" y="56" fill="#fff" font-family="sans-serif" font-size="16" text-anchor="middle">160 × 100</text></svg>');
  const IS = {
    empty: "",
    text: "<p>Royal Arch climbs 1,400 feet.</p>",
    lots: "<p>Royal Arch climbs 1,400 feet in 1.7 miles.</p><p>The last section has over 200 stone steps.</p><p>Start early in summer, because afternoon storms are common.</p>",
    img: `<img src="${IS_IMG}" alt="A sample image, 160 by 100 pixels">`,
  };
  let isCur = "empty";
  function isUpdate() {
    const box = $("is-box"), fixed = $("is-fixed").checked;
    box.innerHTML = IS[isCur]; box.style.height = fixed ? "120px" : "";
    document.querySelectorAll("#is-seg button").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.c === isCur)));
    requestAnimationFrame(() => {
      const hgt = Math.round(box.getBoundingClientRect().height), over = box.scrollHeight > box.clientHeight + 1;
      let msg;
      if (fixed) msg = over ? `Fixed at ${hgt}px (with its border), but the content needs more room, so it spills out over the next element.` : `Fixed at ${hgt}px with its border, whatever the content. This is an extrinsic size.`;
      else if (isCur === "empty") msg = `${hgt}px tall: just the top and bottom borders. An empty block has no content to give it height.`;
      else if (isCur === "img") msg = `${hgt}px tall: the image's intrinsic 100px height plus the border.`;
      else msg = `${hgt}px tall: the box grows to fit its text. This is its intrinsic size.`;
      $("is-out").className = "verdict" + (fixed && over ? " bad" : ""); $("is-out").textContent = msg;
    });
  }
  $("is-seg").addEventListener("click", (e) => { const x = e.target.closest("button"); if (x) { isCur = x.dataset.c; isUpdate(); } });
  $("is-fixed").addEventListener("input", isUpdate);
  isUpdate();

  // --- Percentage margins and padding ---
  function pcUpdate() {
    const w = +$("pc-w").value, v = $("pc-v").value, c = $("pc-child");
    $("pc-w-out").textContent = w + "px";
    $("pc-parent").style.width = w + "px";
    c.style.margin = v; c.style.padding = v;
    const cs = getComputedStyle(c), r = (p) => Math.round(parseFloat(cs[p]));
    $("pc-out").textContent = `${v} of the parent's ${w - 4}px content width = ${r("marginTop")}px. margin-top ${r("marginTop")}px · margin-left ${r("marginLeft")}px · padding-top ${r("paddingTop")}px · padding-left ${r("paddingLeft")}px`;
  }
  ["pc-w", "pc-v"].forEach((id) => $(id).addEventListener("input", pcUpdate));
  pcUpdate();

  // --- max-width on images ---
  const mwCanvas = document.createElement("canvas"); mwCanvas.width = 120; mwCanvas.height = 80;
  const g = mwCanvas.getContext("2d");
  g.fillStyle = "#2340d9"; g.fillRect(0, 0, 120, 80);
  g.fillStyle = "#f4a261"; g.beginPath(); g.arc(90, 24, 12, 0, 7); g.fill();
  g.fillStyle = "#0b6b5e"; g.beginPath(); g.moveTo(0, 80); g.lineTo(40, 34); g.lineTo(70, 62); g.lineTo(88, 46); g.lineTo(120, 80); g.fill();
  g.fillStyle = "#fff"; g.font = "bold 11px sans-serif"; g.fillText("120 × 80", 6, 14);
  $("mw-img").src = mwCanvas.toDataURL();
  function mwUpdate() {
    const w = +$("mw-w").value, r = $("mw-r").value, img = $("mw-img");
    $("mw-w-out").textContent = w + "px";
    $("mw-box").style.width = w + "px";
    img.style.width = r === "w" ? "100%" : ""; img.style.maxWidth = r === "mw" ? "100%" : ""; img.style.height = "auto";
    requestAnimationFrame(() => {
      const iw = Math.round(img.getBoundingClientRect().width), room = w - 16;
      let msg, bad = false;
      if (iw > room + 1) { msg = `The image is ${iw}px wide but there's only ${room}px of room, so it sticks out of its container.`; bad = true; }
      else if (iw > 121) { msg = `Stretched to ${iw}px, ${(iw / 120).toFixed(1)}× its natural width, so it looks blurry.`; bad = true; }
      else if (iw < 120) msg = `Shrunk to ${iw}px to fit the container, keeping its shape.`;
      else msg = "Shown at its natural 120px width.";
      $("mw-out").className = "verdict " + (bad ? "bad" : "ok"); $("mw-out").textContent = msg;
    });
  }
  ["mw-w", "mw-r"].forEach((id) => $(id).addEventListener("input", mwUpdate));
  mwUpdate();
'''
ex_s = src.block('  makeExercise(document.getElementById("ex-sizing"), {')
ex_v = r'''  makeExercise(document.getElementById("ex-vp"), {
    title: "Banner, card and photo",
    task: `<ol>
      <li>Make the banner at least 40% of the window's height, using a viewport unit.</li>
      <li>Give the card <code>5%</code> padding on every side, so its spacing grows with the page.</li>
      <li>The photo is 900px wide and sticks out. Let it shrink to fit the card without stretching or changing shape.</li>
    </ol>`,
    html: `<header class="banner">Boulder Trails</header>
<div class="card">
  <h2>Royal Arch</h2>
  <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='900' height='300'%3E%3Crect width='900' height='300' fill='%230b6b5e'/%3E%3Ccircle cx='720' cy='90' r='50' fill='%23f4a261'/%3E%3C/svg%3E" alt="The arch at sunrise">
  <p>A steep 1.7-mile climb to a sandstone arch.</p>
</div>`,
    css: `body { font-family: system-ui, sans-serif; }
.banner { padding: 20px; background: #1d2a3a; color: white; font-size: 1.5rem; display: grid; place-items: center; }
.card { padding: 16px; margin-top: 12px; background: #eef1fb; }
.card h2 { margin-top: 0; }`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.banner { padding: 20px; min-height: 40vh; background: #1d2a3a; color: white; font-size: 1.5rem; display: grid; place-items: center; }
.card { padding: 5%; margin-top: 12px; background: #eef1fb; }
.card h2 { margin-top: 0; }
img { max-width: 100%; height: auto; }` },
    hints: [
      "vh is 1% of the viewport's height, so 40% of the window is 40vh. min-height lets the banner grow if it needs to.",
      "Percentage padding is worked out from the parent's width, so padding: 5% is the same on all four sides.",
      "max-width: 100% lets an image shrink but never grow. height: auto keeps its shape.",
    ],
    checks: [
      { label: "The banner is at least 40vh tall", test: ({ $, doc }) => $(".banner").getBoundingClientRect().height >= doc.defaultView.innerHeight * 0.4 - 1 && $(".banner").getBoundingClientRect().height > 80 },
      { label: "The card's padding is 5% of its parent's width on every side", test: ({ $, style }) => { const w = $(".card").parentElement.clientWidth * 0.05; return ["padding-top", "padding-right", "padding-bottom", "padding-left"].every((p) => Math.abs(parseFloat(style(".card", p)) - w) < 1); } },
      { label: "The photo fits inside the card", test: ({ $, style }) => { const c = $(".card"), inner = c.clientWidth - parseFloat(style(".card", "padding-left")) - parseFloat(style(".card", "padding-right")); return $("img").getBoundingClientRect().width <= inner + 1; } },
      { label: "The photo keeps its 3:1 shape", test: ({ $ }) => { const r = $("img").getBoundingClientRect(); return Math.abs(r.width / r.height - 3) < 0.05; } },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "A box's parent is 400px wide and 1000px tall. What is padding-top: 10% on the box?", opts: ["100px", "40px", "10px"], a: 1, why: "Percentage padding and margins use the containing block's width, even on the top and bottom." },
    { id: "q6", q: "Why is max-width: 100% better than width: 100% for images?", opts: ["It loads faster", "It shrinks big images but doesn't stretch small ones", "It keeps images square"], a: 1, why: "width: 100% stretches small images past their natural size, so they blur." },
    { id: "q7", q: "What is 50vw?", opts: ["Half the parent's width", "Half the browser window's width", "50 pixels"], a: 1, why: "vw units are a percentage of the viewport, not the parent." },
  ]);
''')
write("core-sizing.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_s + "\n" + ex_v + "</script>\n")
