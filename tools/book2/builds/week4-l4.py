import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("backgrounds-borders")
pg = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">Background</span>', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Backgrounds and Borders", src.css(), """
  .ml-box { height: 200px; border-radius: 8px; border: 1px solid var(--line); background-color: #fff; }
  .layers-list { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .layers-list li { display: grid; grid-template-columns: 1fr auto auto; gap: 6px; align-items: center; padding: 6px 8px; border-radius: 6px; background: var(--stage); font: 0.82rem var(--font-code); font-variation-settings: "MONO" 1; }
  .layers-list .btn { padding: 2px 8px; min-width: 28px; }
  .att-box { height: 220px; overflow: auto; border-radius: 8px; border: 1px solid var(--line); color: #1d2133; background-color: #fff; background-repeat: no-repeat; background-position: center 20px; background-size: 90px; padding: 12px 16px; font: 0.95rem/1.7 Georgia, serif; }
""")
b = top("Backgrounds and Borders", "Backgrounds fill a box with colour, images or gradients, stacked in as many layers as you like. Borders frame it, and rounded corners soften it. Together they're most of what makes a plain box look designed.", [
  "Set background colours and images, and control their repeat, size and position.",
  "Draw linear and radial gradients, and stack several background layers.",
  "Use <code>background-attachment</code> and the <code>background</code> shorthand.",
  "Style borders on one side or all four, and round the corners."])
b += ST("Read", "Background colors") + prose("""
    <p><code>background-color</code> fills the content and padding of a box (the area inside the border). It works on any element, including inline ones like a <code>&lt;span&gt;</code>. A semi-transparent colour, like <code>rgb(255 255 255 / 50%)</code>, lets whatever's behind show through.</p>""")
b += ST("Read", "Background images") + prose("""
    <p><code>background-image: url("star.png")</code> puts an image behind the content. By default, it's shown at its natural size and tiled to fill the box. A background colour shows through wherever the image is transparent or doesn't reach.</p>
    <h3>Controlling background-repeat</h3>
    <p><code>no-repeat</code>, <code>repeat-x</code> (tile across), <code>repeat-y</code> (tile down), <code>repeat</code> (the default), plus <code>space</code> and <code>round</code>, which fit a whole number of tiles.</p>
    <h3>Sizing the background image</h3>
    <p><code>background-size</code> takes lengths or percentages (<code>80px 10em</code>), or a keyword: <code>cover</code> fills the whole box, cropping the image if needed; <code>contain</code> fits the whole image inside, leaving gaps.</p>
    <h3>Positioning the background image</h3>
    <p><code>background-position</code> takes keywords (<code>top center</code>), lengths and percentages (<code>20px 10%</code>), or edge offsets: <code>top 20px right 10px</code> is 20px from the top and 10px from the right.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p>An empty element has no height, so its background is invisible. Backgrounds fill the box; give the box some content, padding or a height.</p></div>""")
b += ST("Play", "Build a trail card", "Combine a background and a border into a card, then see how size, position and corner radius change it.") + pg
b += ST("Read", "Gradient backgrounds") + prose("""
    <p>A <span class="term">gradient</span> is an image that CSS draws, so it goes in <code>background-image</code>, not <code>background-color</code>:</p>
    <pre class="snippet" data-lang="css">.a { background-image: linear-gradient(105deg, rgb(0 249 255) 39%, rgb(51 56 57) 96%); }
.b { background-image: radial-gradient(circle, rgb(0 249 255) 39%, rgb(51 56 57) 96%); }</pre>
    <p>A linear gradient runs along an angle; a radial one spreads out from a point. Each colour can have a stop position, a percentage along the way.</p>""")
b += ST("Read", "Multiple background images") + prose("""
    <p><code>background-image</code> takes a comma-separated list. The <strong>first layer is drawn on top</strong>. The other background properties take lists too, matched up in the same order:</p>
    <pre class="snippet" data-lang="css">.hero {
  background-image: url("star.svg"), linear-gradient(135deg, #0b6b5e, #2340d9);
  background-repeat: no-repeat, no-repeat;
  background-position: right 12px top 12px, center;
}</pre>
    <p>A classic use: a dark gradient over a photo, so white text on top stays readable.</p>""")
b += ST("Play", "Playing with multiple background images", "Reorder the layers. The one at the top of the list is drawn on top.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <ul class="layers-list" id="ml-list"></ul>
      <pre class="snippet" id="ml-code"></pre>
    </div>
    <div class="ml-box" id="ml-box" role="img" aria-label="Layered background"></div>
  </section>

"""
b += ST("Read", "Background attachment") + prose("""
    <p><code>background-attachment</code> decides what the background scrolls with:</p>
    <ul>
      <li><code>scroll</code> (default): fixed to the element; when the <em>page</em> scrolls, it moves with the element, but if the element itself scrolls, the background stays put.</li>
      <li><code>fixed</code>: fixed to the window, so content slides over it. Used for "parallax" effects.</li>
      <li><code>local</code>: fixed to the element's content, so it scrolls along with the text inside.</li>
    </ul>""")
b += ST("Play", "Scroll the box", "Choose a value, then scroll inside the box.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="seg" id="att" role="group" aria-label="background-attachment"><button class="btn" type="button">scroll</button><button class="btn" type="button">local</button><button class="btn" type="button">fixed</button></div>
      <p class="verdict" id="att-note" aria-live="polite"></p>
    </div>
    <div class="att-box" id="att-box"><p>Mesa Trail runs along the base of the Flatirons for 6.7 miles.</p><p>It rolls up and down through meadows and pine forest, crossing several small creeks.</p><p>Spring brings wildflowers; autumn brings golden grass and clear views east across the plains.</p><p>Several side trails climb to the Flatirons themselves.</p><p>Parking at both ends fills early on weekends.</p><p>Dogs are allowed on leash.</p></div>
  </section>

"""
b += ST("Read", "Using the background shorthand property") + prose("""
    <p><code>background</code> sets everything at once, with layers separated by commas. Two rules: the colour can only go in the <strong>last</strong> layer, and a size must come straight after the position, with a slash: <code>center / 80%</code>.</p>
    <pre class="snippet" data-lang="css">.box {
  background:
    url("star.svg") no-repeat right 10px top 10px / 40px,
    linear-gradient(105deg, rgb(255 255 255 / 20%) 39%, rgb(51 56 57 / 100%) 96%) center / 400px 200px no-repeat,
    rebeccapurple;
}</pre>""")
b += ST("Read", "Accessibility considerations with backgrounds") + prose("""
    <p>Text on top of a background image must still have enough contrast, everywhere the text might land, at every screen size. Set a background colour too, so text stays readable if the image doesn't load. And background images are for decoration: screen readers ignore them, so anything that carries meaning belongs in an <code>&lt;img&gt;</code> with alt text.</p>""")
b += ST("Practice", "Layers and the shorthand", "One <code>background</code> declaration, two layers and a colour.") + '  <div id="ex-layers"></div>\n\n'
b += ST("Read", "Borders") + prose("""
    <p>A <span class="term">border</span> needs a width, a style and a colour: <code>border: 1px solid black</code>. Leave out the style and nothing appears, because the default is <code>none</code>. Every part has longhands: one side (<code>border-top</code>), one quality (<code>border-width</code>), or both (<code>border-bottom-style</code>):</p>
    <pre class="snippet" data-lang="css">.box {
  border: 1px solid black;
  border-bottom: 1em double rgb(24 163 78);
}</pre>
    <p>Styles include <code>solid</code>, <code>dashed</code>, <code>dotted</code>, <code>double</code>, <code>groove</code> and <code>ridge</code>.</p>""")
b += ST("Read", "Rounded corners") + prose("""
    <p><code>border-radius: 10px</code> rounds all four corners, even without a border. Each corner has a longhand, like <code>border-top-right-radius</code>, and two values make an elliptical corner: <code>border-top-right-radius: 1em 10%</code>. <code>border-radius: 50%</code> turns a square into a circle.</p>""")
b += ST("Practice", "Backgrounds and borders", "A gradient banner, a round avatar and a rounded card.") + '  <div id="ex-bg"></div>\n\n'
b += notes([
  "<code>background-color</code> fills inside the border; images and gradients go in <code>background-image</code>.",
  "<code>background-size: cover</code> fills and crops; <code>contain</code> fits the whole image.",
  "Multiple backgrounds are comma-separated; the first is on top.",
  "In the <code>background</code> shorthand, the colour goes last and size follows position after a slash.",
  "Borders need a style; <code>border-radius</code> rounds corners, <code>50%</code> makes a circle.",
], [
  "A gradient in <code>background-color</code>, where it's ignored.",
  "A background on an empty element with no height.",
  "Text over a photo with no overlay or fallback colour, so it's unreadable.",
  "<code>border: 2px navy</code> with no style.",
  "Putting meaningful images in CSS backgrounds, where screen readers can't see them.",
])
first = src.first_script()
js = r'''
  // --- Multiple backgrounds ---
  const star = (c) => `url("data:image/svg+xml,${encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='${c}' d='M12 2l3 7h7l-5.5 4.5 2 7.5L12 16.5 5.5 21l2-7.5L2 9h7z'/></svg>`)}")`;
  let layers = [
    ["gold star", star("#f5c400"), "no-repeat", "35% 40% / 90px"],
    ["white star", star("#ffffff"), "no-repeat", "50% 50% / 120px"],
    ["gradient", "linear-gradient(135deg, #0b6b5e, #2340d9)", "no-repeat", "center / cover"],
  ];
  function ml() {
    $("ml-box").style.background = layers.map(([, img, rep, pos]) => `${img} ${rep} ${pos}`).join(", ");
    $("ml-list").innerHTML = layers.map(([n], i) => `<li><span>${i + 1}. ${n}${i === 0 ? " (on top)" : ""}</span><button class="btn" type="button" data-up="${i}" ${i === 0 ? "disabled" : ""} aria-label="Move ${n} up">↑</button><button class="btn" type="button" data-down="${i}" ${i === layers.length - 1 ? "disabled" : ""} aria-label="Move ${n} down">↓</button></li>`).join("");
    $("ml-code").textContent = "background:\n" + layers.map(([n, img, rep, pos]) => `  ${n === "gradient" ? img : `url(${n.replace(" ", "-")}.svg)`} ${rep} ${pos}`).join(",\n") + ";";
  }
  $("ml-list").addEventListener("click", (e) => {
    const u = e.target.closest("[data-up]"), d = e.target.closest("[data-down]");
    if (u) { const i = +u.dataset.up; [layers[i - 1], layers[i]] = [layers[i], layers[i - 1]]; ml(); }
    if (d) { const i = +d.dataset.down; [layers[i + 1], layers[i]] = [layers[i], layers[i + 1]]; ml(); }
  });
  ml();

  // --- Background attachment ---
  $("att-box").style.backgroundImage = star("#f0b37a");
  const ATT = { scroll: "scroll: the star stays put while the text scrolls inside the box.", local: "local: the star is attached to the content, so it scrolls away with the text.", fixed: "fixed: the star is attached to the browser window. Scroll the page itself to see it slide." };
  function att(v) { $("att-box").style.backgroundAttachment = v; $("att-note").textContent = ATT[v]; document.querySelectorAll("#att .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.textContent === v))); }
  $("att").addEventListener("click", (e) => { const b = e.target.closest(".btn"); if (b) att(b.textContent); });
  att("scroll");
'''
ex_bg = src.block('  makeExercise(document.getElementById("ex-bg"), {')
ex_l = r'''  makeExercise(document.getElementById("ex-layers"), {
    title: "The hero banner",
    task: `<p>Give <code>.hero</code> a single <code>background</code> declaration with:</p>
    <ol>
      <li>A top layer: <code>url("star.svg")</code>, <code>no-repeat</code>, positioned <code>right 12px top 12px</code>, sized <code>40px</code>.</li>
      <li>A second layer: <code>linear-gradient(135deg, #0b6b5e, #2340d9)</code>.</li>
      <li>A fallback colour, <code>#0b6b5e</code>, in the right place.</li>
    </ol>
    <p>The star file doesn't exist here, so you'll see just the gradient. The checks read the computed layers.</p>`,
    html: `<div class="hero">
  <h1>Trail Club</h1>
  <p>Weekend hikes for every pace.</p>
</div>`,
    css: `body { font-family: system-ui, sans-serif; margin: 0; }
.hero {
  color: white;
  padding: 40px 24px;
}`,
    solution: { css: `body { font-family: system-ui, sans-serif; margin: 0; }
.hero {
  color: white;
  padding: 40px 24px;
  background:
    url("star.svg") no-repeat right 12px top 12px / 40px,
    linear-gradient(135deg, #0b6b5e, #2340d9),
    #0b6b5e;
}` },
    hints: ["Layers are separated by commas; the first is on top.", "Size goes after position, with a slash: right 12px top 12px / 40px", "The colour can only be in the last layer."],
    checks: [
      { label: "Two layers: the star, then the gradient", test: ({ style }) => /^url\(.*star\.svg.*\),\s*linear-gradient/.test(style(".hero", "background-image")) },
      { label: "The star doesn't repeat and is 40px", test: ({ style }) => style(".hero", "background-repeat").startsWith("no-repeat") && style(".hero", "background-size").startsWith("40px") },
      { label: "The star is 12px from the top right", test: ({ style }) => /^calc\(100% - 12px\) 12px|^right 12px top 12px/.test(style(".hero", "background-position")) || style(".hero", "background-position-x").startsWith("right 12px") || style(".hero", "background-position-x").startsWith("calc(100% - 12px)") },
      { label: "The fallback colour is #0b6b5e", test: ({ style }) => style(".hero", "background-color") === "rgb(11, 107, 94)" },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "background-size: cover does what?", opts: ["Fills the box, cropping the image if needed", "Shows the whole image, leaving gaps", "Tiles the image"], a: 0, why: "contain is the one that fits the whole image." },
    { id: "q6", q: "In the background shorthand, where must the colour go?", opts: ["In the last layer", "In the first layer", "Anywhere"], a: 0, why: "Only the bottom layer can have a colour." },
  ]);
''')
write("core-backgrounds-borders.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_l + "\n" + ex_bg + "\n" + quiz + "</script>\n")
