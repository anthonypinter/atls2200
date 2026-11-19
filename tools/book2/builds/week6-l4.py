import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
def sub(s, a, b, n=1):
    assert a in s, a
    return s.replace(a, b) if n == 0 else s.replace(a, b, n)
ri = Src("responsive-images"); pic = Src("picture")
pg_shrink = ri.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="cw">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Fit it to a shape')
pg_srcset = ri.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="dw">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
pg_srcset = sub(sub(pg_srcset, 'id="dpr"', 'id="ri-dpr"'), 'id="cands"', 'id="ri-cands"')
pg_sizes = pic.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="vw">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Change the crop')
pg_art = pic.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="aw">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Skip what')
pg_lazy = pic.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label>loading</label>', '  <div class="section-title"><span class="eyebrow">Practice</span>')

ri_js = ri.first_script()
ri_js = sub(ri_js, '$("img1").src = PHOTO; $("img2").src = PHOTO;', '$("img1").src = PHOTO;')
i = ri_js.index("  let shape = { w: 260, h: 260 };"); j = ri_js.index("  const CANDS")
ri_js = ri_js[:i] + ri_js[j:]
ri_js = sub(ri_js, '$("dpr")', '$("ri-dpr")', 0)
ri_js = sub(ri_js, '"#dpr button"', '"#ri-dpr button"', 0)
ri_js = sub(ri_js, '$("cands")', '$("ri-cands")', 0)
pic_js = pic.first_script()

h = head("Responsive Images", ri.css() + "\n" + pic.css(), """
  .dx-row { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }
  .dx-row img { display: block; width: 160px; height: 100px; border-radius: 8px; }
  .dx-tbl { border-collapse: collapse; font: 0.85rem var(--font-code); font-variation-settings: "MONO" 1; }
  .dx-tbl td { padding: 3px 10px; border-bottom: 1px solid var(--line); }
  .dx-tbl tr.pick td { color: var(--cobalt); font-weight: 700; }
""")
b = top("Responsive Images", "CSS can make an image fit any screen, but it can't change which file the browser downloads. HTML can: offer several sizes with <code>srcset</code> and <code>sizes</code>, a different crop with <code>&lt;picture&gt;</code>, and skip images nobody scrolls to with <code>loading=\"lazy\"</code>.", [
  "Explain the two problems responsive images solve: resolution switching and art direction.",
  "Offer several file sizes with <code>srcset</code> and <code>w</code> descriptors, and describe the layout with <code>sizes</code>.",
  "Offer sharper copies for high-density screens with <code>x</code> descriptors.",
  "Change the crop on small screens with <code>&lt;picture&gt;</code> and <code>&lt;source&gt;</code>, and lazy-load images further down the page.",
])
b += ST("Read", "Why responsive images?") + prose("""
    <p>Say your page has a big, wide photo of a trail. On a laptop it looks great. On a phone, two things go wrong:</p>
    <ul>
      <li><strong>The file is too big.</strong> CSS like <code>max-width: 100%</code> shrinks how the image is <em>displayed</em>, but the phone still downloads the full 1600px file, which wastes data and time. Sending a smaller file to smaller screens is called <strong>resolution switching</strong>.</li>
      <li><strong>The picture doesn't work small.</strong> A wide landscape shrunk to phone size turns the interesting part into a speck. Showing a different crop is called <strong><span class="term">art direction</span></strong>.</li>
    </ul>
    <p>For simple graphics like logos and icons, an SVG solves both: it's small and sharp at any size. For photos, HTML gives you <code>srcset</code>, <code>sizes</code> and <code>&lt;picture&gt;</code>.</p>""")
b += ST("Play", "CSS can shrink an image, but…", "This photo is 800 × 500 pixels. Make the container narrower and see what each setting does. However small it shows, the browser downloaded all 800 pixels.") + pg_shrink
b += ST("Read", "How do you create responsive images?") + prose("""
    <h3>Resolution switching: Different sizes</h3>
    <p>Make several copies of the image at different widths, and list them in <span class="term">srcset</span>. Each entry is a file name and its real width in pixels, written with a <code>w</code>:</p>
    <pre class="snippet" data-lang="html">&lt;img src="arch-800.jpg"
     srcset="arch-400.jpg 400w, arch-800.jpg 800w, arch-1600.jpg 1600w"
     alt="The sandstone arch at the top of the trail"&gt;</pre>
    <p>The browser works out how many real pixels it needs (including the screen's pixel density) and downloads the smallest file that will look sharp. <code>src</code> stays as the fallback for very old browsers.</p>""")
b += ST("Play", "Send the right file with srcset", "Change how wide the image shows and the screen's pixel density. The browser picks the smallest file that's big enough.") + pg_srcset
b += prose("""
    <p>There's a catch. The browser picks the file <em>before</em> your CSS has loaded, so it doesn't know your layout. Unless you say otherwise, it assumes the image fills the whole window. The <span class="term">sizes</span> attribute tells it how wide the image will really be:</p>
    <pre class="snippet" data-lang="html">&lt;img srcset="mesa-400.jpg 400w, mesa-800.jpg 800w, mesa-1600.jpg 1600w"
     sizes="(width &lt;= 600px) 100vw, 33vw"
     src="mesa-800.jpg" alt="Mesa Trail at sunrise"&gt;</pre>
    <p>Each part of <code>sizes</code> is a media condition and a width (a length or <code>vw</code>, never a percentage). The first condition that matches wins, and the last value, with no condition, is the default. Here: full width on screens up to 600px, a third of the window otherwise.</p>""")
b += ST("Play", "Tell the browser the size with sizes", "This layout shows 1, 2 or 3 cards per row. Without sizes, the browser assumes each card is the full window wide.") + pg_sizes
b += prose("""
    <h3>Resolution switching: Same size, different resolutions</h3>
    <p>Some images always show at the same size, like a 160px-wide logo. They don't need <code>sizes</code>; they just need sharper copies for high-density screens, where each CSS pixel is made of 2 or 3 real pixels. Use <code>x</code> descriptors:</p>
    <pre class="snippet" data-lang="html">&lt;img srcset="logo-160.png, logo-320.png 2x, logo-480.png 3x"
     src="logo-160.png" alt="Trailhead"&gt;</pre>
    <p>The first entry has no descriptor, so it counts as <code>1x</code>. Keep the display size fixed in CSS (<code>width: 160px</code>).</p>""")
b += ST("Play", "Which copy gets picked?", "This image has 1x, 2x and 3x copies. Start with your own screen, then try other densities. (Zooming the page changes your pixel density, too.)") + """  <section class="playground">
    <div class="panel" style="display:grid;gap:8px;align-content:start">
      <span class="eyebrow">Pixel density</span>
      <div class="seg" id="dx-seg" role="group" aria-label="Pixel density"><button class="btn" data-d="real">your screen</button><button class="btn" data-d="1">1x</button><button class="btn" data-d="2">2x</button><button class="btn" data-d="3">3x</button></div>
      <p id="dx-out" aria-live="polite"></p>
      <table class="dx-tbl" id="dx-tbl"></table>
    </div>
    <div class="dx-row"><img id="dx-img" alt="A sample logo; its text says which copy loaded"><pre class="snippet" style="margin:0">&lt;img srcset="logo-1x.svg,
             logo-2x.svg 2x,
             logo-3x.svg 3x"
     src="logo-1x.svg" alt="…"&gt;</pre></div>
  </section>

"""
b += prose("""
    <h3>Art direction</h3>
    <p>When a smaller copy isn't enough and you need a different crop, wrap the image in <span class="term">picture</span>. Each <code>&lt;source&gt;</code> has a <code>media</code> condition and a <code>srcset</code>; the browser uses the first one that matches, and falls back to the <code>&lt;img&gt;</code>:</p>
    <pre class="snippet" data-lang="html">&lt;picture&gt;
  &lt;source media="(width &lt; 800px)" srcset="arch-square.jpg"&gt;
  &lt;source media="(width &gt;= 800px)" srcset="arch-wide.jpg"&gt;
  &lt;img src="arch-wide.jpg" alt="Royal Arch above the trees"&gt;
&lt;/picture&gt;</pre>
    <p>The <code>&lt;img&gt;</code> is required: it's what actually shows the picture, it holds the <code>alt</code> text, and your CSS targets it. Use <code>media</code> on sources only for art direction; for plain size switching, <code>srcset</code> and <code>sizes</code> let the browser make smarter choices.</p>""")
b += ST("Play", "Change the crop with &lt;picture&gt;", "Change the window width and watch which source the browser uses.") + pg_art
b += prose("""
    <h3>Why can't we just do this using CSS or JavaScript?</h3>
    <p>Because they're too late. To show pages quickly, browsers start downloading images as soon as they see an <code>&lt;img&gt;</code> tag, using a <em>preload scanner</em>, before the CSS and JavaScript have even arrived. By the time a script could choose a smaller file, the big one is already downloading. Putting the choices in the HTML lets the browser choose right the first time.</p>""")
b += ST("Read", "Lazy loading") + prose("""
    <p>One more HTML attribute saves data on long pages. <code>loading="lazy"</code> waits to download an image until the visitor scrolls near it. On a long gallery, people who never scroll to the bottom never download the images there. This is called <span class="term">lazy loading</span>.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p>Don't lazy-load the big image at the top of the page. It's the first thing visitors see, so it should start downloading as early as possible. And keep <code>width</code> and <code>height</code> on lazy images so the page doesn't jump when they arrive.</p></div>""")
b += ST("Play", "Skip what nobody sees with loading=\"lazy\"", "Scroll the page on the left and watch the network log.") + pg_lazy
b += ST("Read", "Implementing your own responsive images") + prose("""
    <p>For your own projects: export each photo at two or three widths (for example 400, 800 and 1600 pixels), list them in <code>srcset</code>, and add <code>sizes</code> if the image isn't full width. If a photo needs a different crop on phones, make a tighter crop and offer it with <code>&lt;picture&gt;</code>. In CSS, keep <code>img { max-width: 100%; height: auto; }</code>.</p>""")
b += ST("Practice", "Make the images fit", "A big photo breaks the layout and an avatar gets squashed. Fix both, and offer smaller files.") + '  <div id="ex-img"></div>\n\n'
b += ST("Practice", "Send the right image", "Tell the browser how big one image is, swap the crop of another, and lazy-load the third.") + '  <div id="ex-picture"></div>\n\n'
b += notes([
  "CSS shrinks how an image is displayed; only HTML can change which file is downloaded.",
  "<code>srcset</code> with <code>w</code> descriptors (<code>arch-800.jpg 800w</code>) plus <code>sizes</code> lets the browser pick the smallest sharp file.",
  "<code>x</code> descriptors (<code>logo-320.png 2x</code>) suit images that always show at one size.",
  "<code>&lt;picture&gt;</code> with <code>&lt;source media&gt;</code> changes the crop (art direction); the <code>&lt;img&gt;</code> inside is required.",
  "<code>loading=\"lazy\"</code> on images further down the page, never the first one.",
], [
  "Leaving out <code>sizes</code> with <code>w</code> descriptors, so a small card image downloads at full-window size.",
  "Using a percentage in <code>sizes</code>. It takes lengths or <code>vw</code>.",
  "Forgetting the <code>&lt;img&gt;</code> inside <code>&lt;picture&gt;</code>. Without it, nothing shows.",
  "Uploading a 4000px photo straight from a phone for something shown 400px wide.",
])
js = r'''
  // --- x descriptors, for real ---
  const DX = [1, 2, 3].map((d) => "data:image/svg+xml," + encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" width="${160 * d}" height="${100 * d}" viewBox="0 0 160 100"><rect width="160" height="100" rx="8" fill="${["#0b6b5e", "#2340d9", "#b4410c"][d - 1]}"/><text x="80" y="48" fill="#fff" font-family="sans-serif" font-size="26" font-weight="700" text-anchor="middle">${d}x copy</text><text x="80" y="74" fill="#fff" font-family="sans-serif" font-size="12" text-anchor="middle">${160 * d} × ${100 * d} pixels</text></svg>`));
  const dxImg = document.getElementById("dx-img");
  const real = Math.round(window.devicePixelRatio * 100) / 100;
  let dxD = real;
  function dxReport() {
    const pick = dxD <= 1 ? 0 : dxD <= 2 ? 1 : 2;
    dxImg.src = DX[pick];
    document.getElementById("dx-out").textContent = (dxD === real ? `Your screen's pixel density is ${real}` : `Pretending the pixel density is ${dxD}`) + `, so the browser picks the ${pick + 1}x copy: the smallest one with at least ${Math.ceil(dxD) * 160} real pixels across.`;
    document.getElementById("dx-tbl").innerHTML = [1, 2, 3].map((n, k) => `<tr class="${k === pick ? "pick" : ""}"><td>logo-${n}x.svg</td><td>${160 * n} px wide</td><td>${k === pick ? "← chosen" : ""}</td></tr>`).join("");
    document.querySelectorAll("#dx-seg button").forEach((x) => x.setAttribute("aria-pressed", String(+x.dataset.d === dxD)));
  }
  document.getElementById("dx-seg").addEventListener("click", (e) => { const x = e.target.closest("button"); if (x) { dxD = x.dataset.d === "real" ? real : +x.dataset.d; dxReport(); } });
  dxReport();
'''
scripts = "\n<script>\n(() => {" + ri_js + "})();\n(() => {" + pic_js + "})();\n" + js + "</script>\n"
quiz = ri.block('  makeQuiz(document.getElementById("quiz"), [')
pq = pic.block('  makeQuiz(document.getElementById("quiz"), [')
items = pq[pq.index("[\n") + 2:pq.rindex("  ]);")]
for k in (4, 3, 2, 1):
    items = items.replace(f'id: "q{k}"', f'id: "q{k + 4}"')
quiz = quiz.replace("  ]);\n", items + '''    { id: "q9", q: "A logo always shows 160px wide. How should you offer sharper copies?", opts: ["srcset with 1x, 2x and 3x copies", "sizes=\\"160px\\" only", "<picture> with media queries"], a: 0, why: "x descriptors are for fixed-size images; the browser picks by pixel density." },
    { id: "q10", q: "Why can't JavaScript choose the image file instead?", opts: ["JavaScript can't read the window width", "The browser starts downloading images before scripts and CSS have loaded", "It's not allowed"], a: 1, why: "The preload scanner fetches images early, so the choice has to be in the HTML." },
  ]);
''')
ex_i = ri.block('  makeExercise(document.getElementById("ex-img"), {')
ex_p = pic.block('  makeExercise(document.getElementById("ex-picture"), {')
write("core-responsive-images.html", h, b, scripts + "<script>\n" + quiz + "\n" + ex_i + "\n" + ex_p + "</script>\n")
