import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("overflow")
pg_fit = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="ov">', '  <div class="section-title"><span class="eyebrow">Practice</span><h2>Find what')
hunt = src.between('  <div class="hunt">', '  <div class="section-title"><span class="eyebrow">Practice</span><h2>Tame')
hunt = hunt.replace('<div class="phone" id="phone">', '<div class="phone" id="phone" data-use>', 1)  # clicks here count as using the section (js/chrome.js)
h = head("Overflow", src.css(), """
  .ax-stage { background: var(--stage); border-radius: 8px; padding: 20px; min-height: 240px; }
  .ax-box { width: 220px; height: 110px; border: 3px solid var(--cobalt); border-radius: 6px; background: var(--panel); padding: 8px; font-size: 0.9rem; }
  .ax-box p { margin: 0 0 6px; }
  .ax-box .long { font: 0.85rem var(--font-code); font-variation-settings: "MONO" 1; color: var(--cobalt); white-space: nowrap; }
  .hc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
  @media (max-width: 640px) { .hc-grid { grid-template-columns: 1fr; } }
  .hc-col { display: grid; gap: 8px; align-content: start; }
  .hc-col .cap { font: 600 0.85rem var(--font-code); font-variation-settings: "MONO" 1; color: var(--prop); }
  .hc-box { height: 110px; border: 3px solid var(--cobalt); border-radius: 6px; background: var(--panel); padding: 8px; font-size: 0.9rem; }
  .hc-box p { margin: 0 0 6px; }
""")
b = top("Overflow", "Overflow happens when content is bigger than its box. CSS doesn't hide it by default: it lets it spill out so you notice. Here's how to control it on each axis, and how to track down the element that makes a whole page scroll sideways.", [
  "Explain why CSS shows overflowing content by default.",
  "Choose between <code>visible</code>, <code>clip</code>, <code>hidden</code>, <code>scroll</code> and <code>auto</code>, and set each axis separately.",
  "Shorten one-line text with an ellipsis, and let long words and links wrap.",
  "Track down the element that makes a whole page scroll sideways.",
])
b += ST("Read", "What is overflow?") + prose("""
    <p><span class="term">Overflow</span> is what happens when there's too much content to fit in a box: a long paragraph in a card with a fixed height, a giant image in a narrow column, or a long URL with no spaces to break at.</p>
    <p>It only happens when a box's size is constrained. A box with no set height just grows to fit its content, as you saw in <a href="core-sizing.html">Sizing</a>. Set <code>height: 100px</code>, though, and anything beyond 100px has to go somewhere.</p>""")
b += ST("Read", "CSS tries to avoid \"data loss\"") + prose("""
    <p>By default, CSS lets overflowing content spill out of its box, visibly, even when it overlaps whatever comes next. That looks messy, but it's deliberate: if CSS silently hid the extra content, you might never notice that part of your page was missing. A mess is a problem you'll see and fix.</p>
    <p>The lesson for your own CSS: be careful about fixing the height of anything that holds text. Text gets longer when it's translated, when someone sets a bigger default font, or when the screen gets narrower. Let the content decide the height wherever you can.</p>""")
b += ST("Read", "The overflow property") + prose("""
    <p>When you do need to control overflow, the <code>overflow</code> property decides what happens:</p>
    <ul>
      <li><code>visible</code>, the default, lets it spill out.</li>
      <li><code>clip</code> cuts off anything outside the box.</li>
      <li><code>hidden</code> also cuts it off, but the box can still be scrolled by code.</li>
      <li><code>scroll</code> always shows scrollbars.</li>
      <li><code>auto</code> shows scrollbars only when they're needed. It's usually the right choice.</li>
    </ul>""")
b += ST("Play", "Make the content fit", "Change overflow and the box's height, then fix the long title and the long link.") + pg_fit
b += ST("Read", "Hiding overflowing content") + prose("""
    <p><code>overflow: clip</code> cuts content off at the edge of the box (its padding edge, just inside the border). The cut-off part can't be reached at all, so only use it for things nobody needs to read, like a decorative shape that pokes out of a banner.</p>
    <p>If clipping right at the edge looks too tight, <code>overflow-clip-margin</code> lets the content spill a little way past the edge before it's cut:</p>
    <pre class="snippet" data-lang="css">.banner {
  overflow: clip;
  overflow-clip-margin: 10px;
}</pre>""")
b += ST("Read", "Scrolling overflowing content") + prose("""
    <p><code>overflow: auto</code> keeps everything reachable: if the content doesn't fit, the box gets a scrollbar; if it does, there's no scrollbar at all. It's the safe choice for a box that has to stay a fixed size, like a chat window or a long list in a sidebar.</p>
    <pre class="snippet" data-lang="css">.trail-log {
  height: 200px;
  overflow: auto;
}</pre>""")
b += ST("Read", "Controlling overflow on each axis") + prose("""
    <p><code>overflow</code> is a shorthand for two properties: <code>overflow-x</code> (side to side) and <code>overflow-y</code> (up and down). You can set them separately, or give <code>overflow</code> two values, x first:</p>
    <pre class="snippet" data-lang="css">.code-sample { overflow-x: auto; }   /* scroll sideways only */
.strip { overflow: clip auto; }      /* clip x, scroll y */</pre>
    <p>One combination isn't allowed: a box can't scroll in one direction and spill visibly in the other. If one axis is <code>scroll</code>, <code>auto</code> or <code>hidden</code>, a <code>visible</code> on the other axis is quietly turned into <code>auto</code>.</p>""")
b += ST("Play", "Two axes", "This box has a long line (too wide) and several paragraphs (too tall). Set each axis and watch what the browser actually uses.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="ax-x">overflow-x</label><select id="ax-x"><option>visible</option><option>clip</option><option>hidden</option><option>scroll</option><option selected>auto</option></select></div>
      <div class="control"><label for="ax-y">overflow-y</label><select id="ax-y"><option selected>visible</option><option>clip</option><option>hidden</option><option>scroll</option><option>auto</option></select></div>
      <pre class="snippet" id="ax-code"></pre>
    </div>
    <div class="stage-col">
      <div class="ax-stage"><div class="ax-box" id="ax-box">
        <p class="long">https://example.org/trails/boulder/mesa-trail-full-map.pdf</p>
        <p>The Mesa Trail runs 6.7 miles along the foot of the Flatirons.</p>
        <p>It links a dozen side trails, so you can make a loop of almost any length.</p>
      </div></div>
      <p class="verdict" id="ax-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += prose("""
    <h3>Long words and one-line titles</h3>
    <p>Two text problems come up constantly. A long URL or word has no spaces to break at, so it pushes past its box. <code>overflow-wrap: anywhere</code> lets it break where it needs to. And a title that must stay on one line can end in an ellipsis (…) instead of spilling:</p>
    <pre class="snippet" data-lang="css">.title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}</pre>""")
b += ST("Read", "Always displaying scrollbars") + prose("""
    <p><code>overflow: scroll</code> shows scrollbars even when there's nothing to scroll, on systems that show scrollbars all the time. That's rarely what you want, but it does stop the layout jumping sideways when content grows and a scrollbar suddenly appears.</p>
    <p>A better way to get that stability is <code>overflow: auto</code> plus <code>scrollbar-gutter: stable</code>, which reserves room for the scrollbar without drawing an empty one.</p>
    <pre class="snippet" data-lang="css">.panel {
  overflow: auto;
  scrollbar-gutter: stable;
}</pre>""")
b += ST("Read", "The hidden value") + prose("""
    <p><code>overflow: hidden</code> looks just like <code>clip</code>: extra content is cut off and there are no scrollbars. The difference is that a <code>hidden</code> box is still a <em>scroll container</em>. JavaScript can scroll it, and so can keyboard focus moving to a link inside the hidden part. That can leave the box scrolled to an odd position with no way for the user to scroll it back.</p>
    <p>Use <code>clip</code> when you just want to cut content off, and <code>hidden</code> only when you're going to scroll the box with code (a carousel, for example).</p>""")
b += ST("Play", "hidden vs clip", "Both boxes cut off their content. Now try scrolling each one with code.") + """  <section class="playground">
    <div class="panel controls">
      <button class="btn" id="hc-go">Scroll both down 40px with JavaScript</button>
      <button class="btn" id="hc-reset">Reset</button>
      <div class="control"><label for="hc-m">overflow-clip-margin (clip box)</label><input id="hc-m" type="range" min="0" max="20" step="2" value="0"><span class="readout" id="hc-m-out"></span></div>
    </div>
    <div class="stage-col">
      <div class="hc-grid">
        <div class="hc-col"><span class="cap">overflow: hidden</span><div class="hc-box" id="hc-h"><p>1. Chautauqua trailhead</p><p>2. Bluebell shelter</p><p>3. Royal Arch junction</p><p>4. The stone steps</p><p>5. Royal Arch</p></div></div>
        <div class="hc-col"><span class="cap">overflow: clip</span><div class="hc-box" id="hc-c" style="overflow:clip"><p>1. Chautauqua trailhead</p><p>2. Bluebell shelter</p><p>3. Royal Arch junction</p><p>4. The stone steps</p><p>5. Royal Arch</p></div></div>
      </div>
      <p class="verdict" id="hc-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += ST("Read", "Unwanted overflow in web design") + prose("""
    <p>Most overflow you meet won't be a box you chose to constrain. It'll be a bug: text spilling out of a card that looked fine with the sample text, or a whole page that scrolls sideways on a phone because one element is wider than the screen (a fixed <code>width: 400px</code>, a big image, a long link).</p>
    <p>To catch these early, test your layouts with much more and much less content than you expect, and with a larger browser font size. When you find overflow, fix the cause instead of hiding it.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p><code>overflow: hidden</code> on the <code>body</code> hides the sideways scroll, but the content is still too wide and now some of it is unreachable. Find the element that's too wide and make it flexible.</p></div>""")
b += ST("Practice", "Find what's making the page scroll sideways", "This phone-sized page scrolls left and right. Click each part of the page to inspect its width, find the one wider than the screen, then fix it.") + hunt
b += ST("Practice", "Tame the overflow", "Three boxes, three kinds of overflow. Pick the right fix for each.") + '  <div id="ex-overflow"></div>\n\n'
b += ST("Practice", "Clip, scroll one way, and shorten", "A decorative shape, a long line of code and a title that must stay on one line.") + '  <div id="ex-axes"></div>\n\n'
b += notes([
  "Overflow only happens when a box's size is constrained. Let content decide the height where you can.",
  "By default overflow is <code>visible</code>, so you notice the problem instead of losing content.",
  "<code>auto</code> adds scrollbars only when needed; <code>clip</code> cuts content off; <code>hidden</code> cuts it off but can still be scrolled by code.",
  "<code>overflow-x</code> and <code>overflow-y</code> control each axis. A scrolling axis turns <code>visible</code> on the other into <code>auto</code>.",
  "<code>overflow-wrap: anywhere</code> breaks long words; <code>text-overflow: ellipsis</code> shortens one-line text.",
], [
  "Fixed pixel widths, like <code>width: 380px</code>, wider than a phone screen.",
  "Putting <code>overflow: hidden</code> on <code>body</code> to hide the sideways scroll instead of fixing the cause.",
  "Fixed <code>height</code> on a text box that later gets more text, translated text, or larger font settings.",
  "Using <code>overflow: scroll</code>, which shows scrollbars even when nothing overflows.",
])
first = src.first_script()
js = r'''
  // --- Two axes ---
  function axUpdate() {
    const x = $("ax-x").value, y = $("ax-y").value, box = $("ax-box");
    box.style.overflowX = x; box.style.overflowY = y;
    const cs = getComputedStyle(box), cx = cs.overflowX, cy = cs.overflowY;
    $("ax-code").textContent = `.box {\n  overflow-x: ${x};\n  overflow-y: ${y};\n}`;
    const changed = [];
    if (cx !== x) changed.push(`overflow-x: ${x} became ${cx}`);
    if (cy !== y) changed.push(`overflow-y: ${y} became ${cy}`);
    $("ax-out").className = "verdict" + (changed.length ? " bad" : "");
    $("ax-out").textContent = `The browser is using overflow-x: ${cx}; overflow-y: ${cy}.` + (changed.length ? ` ${changed.join(" and ")}, because a box can't scroll one way and spill visibly the other.` : "");
  }
  ["ax-x", "ax-y"].forEach((id) => $(id).addEventListener("input", axUpdate));
  axUpdate();

  // --- hidden vs clip ---
  function hcReport() {
    const hs = $("hc-h").scrollTop, cs = $("hc-c").scrollTop;
    $("hc-out").textContent = `hidden box scrollTop: ${hs}px · clip box scrollTop: ${cs}px.` + (hs ? " The hidden box scrolled, though there's no scrollbar to scroll it back. The clip box can't be scrolled at all." : "");
  }
  $("hc-go").addEventListener("click", () => { $("hc-h").scrollTop += 40; $("hc-c").scrollTop += 40; hcReport(); });
  $("hc-reset").addEventListener("click", () => { $("hc-h").scrollTop = 0; $("hc-c").scrollTop = 0; hcReport(); });
  $("hc-m").addEventListener("input", () => { const m = $("hc-m").value + "px"; $("hc-c").style.overflowClipMargin = m; $("hc-m-out").textContent = m; });
  $("hc-m-out").textContent = "0px";
  hcReport();
'''
ex_o = src.block('  makeExercise(document.getElementById("ex-overflow"), {')
ex_a = r'''  makeExercise(document.getElementById("ex-axes"), {
    title: "Banner, code sample and title",
    task: `<ol>
      <li>The sun shape pokes out of the banner. Cut it off at the banner's edge with the value that can't be scrolled.</li>
      <li>The code sample has one very long line. Let it scroll sideways inside its own box, without the page scrolling.</li>
      <li>Keep the trail title on one line and end it with an ellipsis (…) where it's cut off.</li>
    </ol>`,
    html: `<div class="banner"><div class="sun"></div>Boulder Trails</div>
<pre class="code">fetch("https://example.org/api/trails?city=boulder&amp;difficulty=moderate&amp;dogs=true&amp;sort=distance")</pre>
<h2 class="title">Chautauqua to Royal Arch via the Bluebell Mesa Trail and the Bluebell Road</h2>`,
    css: `body { font-family: system-ui, sans-serif; }
.banner { position: relative; padding: 30px 16px; background: #1d2a3a; color: white; font-size: 1.4rem; }
.sun { position: absolute; top: -40px; right: -40px; width: 120px; height: 120px; border-radius: 50%; background: #f4a261; opacity: 0.8; }
.code { background: #eef1fb; padding: 10px; }
.title { width: 260px; font-size: 1.1rem; }`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.banner { position: relative; padding: 30px 16px; background: #1d2a3a; color: white; font-size: 1.4rem; overflow: clip; }
.sun { position: absolute; top: -40px; right: -40px; width: 120px; height: 120px; border-radius: 50%; background: #f4a261; opacity: 0.8; }
.code { background: #eef1fb; padding: 10px; overflow-x: auto; }
.title { width: 260px; font-size: 1.1rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }` },
    hints: [
      "clip cuts content off and, unlike hidden, the box can't be scrolled at all.",
      "overflow-x: auto on the pre gives it its own sideways scrollbar.",
      "An ellipsis needs three things: white-space: nowrap, overflow: hidden and text-overflow: ellipsis.",
    ],
    checks: [
      { label: "The banner clips with overflow: clip", test: ({ style }) => style(".banner", "overflow-x") === "clip" && style(".banner", "overflow-y") === "clip" },
      { label: "The code sample scrolls sideways in its own box", test: ({ style }) => ["auto", "scroll"].includes(style(".code", "overflow-x")) },
      { label: "The page itself doesn't scroll sideways", test: ({ doc }) => doc.documentElement.scrollWidth <= doc.documentElement.clientWidth },
      { label: "The title is one line ending in an ellipsis", test: ({ $, style }) => style(".title", "white-space") === "nowrap" && style(".title", "text-overflow") === "ellipsis" && style(".title", "overflow-x") !== "visible" && $(".title").scrollWidth > $(".title").clientWidth },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Both overflow: hidden and overflow: clip cut content off. What's the difference?", opts: ["clip is faster to type", "A hidden box can still be scrolled by code or focus; a clip box can't", "hidden keeps the scrollbars"], a: 1, why: "hidden still makes a scroll container. clip just cuts the content off." },
    { id: "q6", q: "You set overflow-x: auto and leave overflow-y as visible. What does the browser use for overflow-y?", opts: ["visible", "auto", "hidden"], a: 1, why: "A box can't scroll one way and spill visibly the other, so visible becomes auto." },
  ]);
''')
write("core-overflow.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_o + "\n" + ex_a + "</script>\n")
