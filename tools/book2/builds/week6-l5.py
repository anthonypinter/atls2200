import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("accessibility")
pg = src.between('  <section class="playground even">', '  <div class="section-title"><span class="eyebrow">Your turn</span>')
checklist = src.between('  <ul class="checklist">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
checklist = checklist.replace("The Colors &amp; Units page can check it.", "Use the contrast checker above.").replace("See the Images &amp; Alt Text page.", 'See <a href="core-images.html">Images</a>.')
assert "contrast checker above" in checklist and "core-images.html" in checklist
h = head("Accessibility Essentials", src.css(), """
  .sim-card { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 10px; padding: 14px; display: grid; gap: 8px; font-family: var(--font-body); transition: filter 0.2s; }
  .sim-card h4 { margin: 0; font: 800 1.15rem var(--font-display); }
  .sim-card .row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .sim-card .dot { width: 14px; height: 14px; border-radius: 50%; }
  .sim-card .fine { color: #a3a8b8; font-size: 0.8rem; margin: 0; }
  .sim-card .ph { height: 90px; border-radius: 6px; background: linear-gradient(170deg, #f4a261 0 45%, #7d5a7a 45% 70%, #3e4a61 70%); }
  .sim-card .ph.off { background: #f3f4f7; border: 1px dashed #b8bdcc; color: #5a6280; font-size: 0.85rem; display: grid; place-items: center; padding: 6px; text-align: center; }
  .sim-card .btns { display: flex; gap: 6px; }
  .sim-card .btns span { background: #0b6b5e; color: #fff; border-radius: 4px; padding: 3px 8px; font-size: 0.75rem; }
  .sim-wrap { background: var(--stage); border-radius: 8px; padding: 14px; overflow: hidden; }
  .cc-sample { border-radius: 8px; padding: 16px; display: grid; gap: 6px; border: 1px solid var(--line); }
  .cc-sample .big { font: 700 1.5rem var(--font-display); } .cc-sample p { margin: 0; }
  .cc-res { font: 800 1.6rem var(--font-display); }
  .cc-tbl { border-collapse: collapse; font: 0.85rem var(--font-code); font-variation-settings: "MONO" 1; }
  .cc-tbl td { white-space: nowrap; padding: 3px 10px; border-bottom: 1px solid var(--line); }
  .cc-tbl .y { color: var(--good); font-weight: 700; } .cc-tbl .n { color: var(--bad); font-weight: 700; }
  .hd-demo { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 14px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; position: relative; overflow: hidden; }
  .hd-demo input { font: inherit; padding: 6px 8px; border: 1.5px solid #c9cedb; border-radius: 6px; }
  .hd-demo .tgt { background: #fff4ec; outline: 2px dashed #b4410c; padding: 4px 6px; border-radius: 4px; font-weight: 700; }
  .vh { position: absolute !important; width: 1px !important; height: 1px !important; padding: 0 !important; margin: -1px !important; overflow: hidden !important; clip-path: inset(50%) !important; white-space: nowrap !important; border: 0 !important; }
""")
b = top("Accessibility Essentials", "An accessible site works for people using a keyboard, a screen reader, zoom, captions, or a phone in bright sun. Most of the work is choosing the right HTML and not breaking it with CSS and JavaScript.", [
  "Describe the main kinds of disability and the assistive technologies people use.",
  "Use semantic HTML so buttons, links, labels, headings and images work for everyone.",
  "Check color contrast, keep focus visible, and hide content without hiding it from screen readers.",
  "Test a page with only the keyboard.",
])
b += ST("Read", "So what is accessibility?") + prose("""
    <p><span class="term">Accessibility</span> is the practice of making your sites usable by as many people as possible: people with disabilities, but also people on slow connections, on small screens, in bright sunlight, or holding a baby in one arm.</p>
    <p>It isn't an extra feature for a few people. An accessible site has clear structure (which also helps search engines), works on any device, and is easier for everyone to use. In many countries it's also a legal requirement for public and commercial sites.</p>""")
b += ST("Read", "What kinds of disability are we looking at?") + prose("""
    <p>Around 1 in 6 people worldwide has a significant disability. Many use <strong>assistive technology</strong> (AT) to browse the web.</p>
    <h3>People with visual impairments</h3>
    <p>This includes blindness, low vision and color blindness. People may use a <span class="term">screen reader</span> that reads the page aloud (JAWS and NVDA on Windows, VoiceOver on Mac and iPhone, TalkBack on Android), a screen magnifier, or simply the browser's zoom.</p>
    <h3>People with hearing impairments</h3>
    <p>Deaf and hard-of-hearing people need text alternatives for audio: captions on video and transcripts for podcasts.</p>
    <h3>People with mobility impairments</h3>
    <p>Some people can't use a mouse. They use the keyboard (especially Tab, Enter and Space), switches, voice control or a head pointer. Everything that works with a mouse must work with a keyboard.</p>
    <h3>People with cognitive impairments</h3>
    <p>This is the widest group, including learning disabilities, memory problems, ADHD and dyslexia. It's helped by plain language, consistent layouts, clear headings, links that look like links, and helpful error messages.</p>""")
b += ST("Play", "See the same card differently", "Turn on each condition and notice what stops working.") + """  <section class="playground">
    <div class="panel controls">
      <label class="toggle"><input type="checkbox" id="sim-blur"> blurred vision</label>
      <label class="toggle"><input type="checkbox" id="sim-gray"> no color vision</label>
      <label class="toggle"><input type="checkbox" id="sim-zoom"> zoomed to 200%</label>
      <label class="toggle"><input type="checkbox" id="sim-img"> images don't load</label>
      <p class="hint" id="sim-out" aria-live="polite"></p>
    </div>
    <div class="sim-wrap"><div class="sim-card" id="sim-card">
      <div class="ph" id="sim-ph"></div>
      <h4>Royal Arch</h4>
      <div class="row"><span class="dot" style="background:#c0392b"></span><span id="sim-st">Trail status</span></div>
      <div class="btns"><span>Map</span><span>Save</span><span>Share</span></div>
      <p class="fine">Closed after dark. Dogs on leash.</p>
    </div></div>
  </section>

"""
b += ST("Read", "Implementing accessibility into your project") + prose("""
    <p>Accessibility is much cheaper to build in from the start than to bolt on at the end. Use the right HTML as you write it, check contrast when you pick colors, and test as you go: with the keyboard, with zoom, with an automated checker, and, if you can, with disabled users. Many organizations publish an <em>accessibility statement</em> saying what they support and how to report problems.</p>""")
b += ST("Read", "Accessibility guidelines and the law") + prose("""
    <p>The main standard is the <strong>Web Content Accessibility Guidelines</strong> (WCAG). It's organized under four principles, often remembered as <strong>POUR</strong>:</p>
    <ul>
      <li><strong>Perceivable</strong>: people can see or hear the content (alt text, captions, contrast).</li>
      <li><strong>Operable</strong>: people can use the controls (keyboard access, enough time, no flashing).</li>
      <li><strong>Understandable</strong>: content and controls are clear (plain language, helpful errors).</li>
      <li><strong>Robust</strong>: it works with many browsers and assistive technologies (valid, semantic HTML).</li>
    </ul>
    <p>Laws in many places, such as Section 508 in the US and EN 301 549 in the EU, point to WCAG.</p>""")
b += ST("Read", "Accessibility APIs") + prose("""
    <p>How does a screen reader know what's on a page? The browser builds an <strong>accessibility tree</strong> from your HTML: every element's <em>role</em> (button, link, heading, text field), its <em>name</em> (the button's text, the image's alt, the input's label) and its <em>state</em> (checked, expanded). The operating system passes that tree to assistive technology.</p>
    <p>That's why HTML matters so much. A <code>&lt;button&gt;</code> arrives in the tree as "button, Sign up". A <code>&lt;div&gt;</code> styled to look the same arrives as plain text. <strong>WAI-ARIA</strong> attributes like <code>role</code> and <code>aria-label</code> can patch the tree when HTML has no suitable element, but the first rule of ARIA is: if a native element does the job, use it.</p>""")
b += ST("Read", "HTML: A good basis for accessibility") + prose("""
    <p>Most accessibility comes from choosing the right element, so <span class="term">semantic HTML</span> brings it with it for free.</p>
    <h3>Good semantics</h3>
    <ul>
      <li><strong>Well-structured text.</strong> Real headings in order (<code>&lt;h1&gt;</code>, <code>&lt;h2&gt;</code>…), paragraphs and lists, not bold <code>&lt;div&gt;</code>s and <code>&lt;br&gt;</code>s. Screen reader users skim by jumping from heading to heading.</li>
      <li><strong>Clear language.</strong> Write "5 to 7" rather than "5–7", and expand abbreviations, or mark them with <code>&lt;abbr&gt;</code>.</li>
      <li><strong>Logical page sections.</strong> <code>&lt;header&gt;</code>, <code>&lt;nav&gt;</code>, <code>&lt;main&gt;</code>, <code>&lt;aside&gt;</code> and <code>&lt;footer&gt;</code> become landmarks people can jump to.</li>
      <li><strong>Semantic UI controls.</strong> A real <code>&lt;button&gt;</code> can be reached with Tab, pressed with Enter or Space, and is announced as a button. A clickable <code>&lt;div&gt;</code> does none of that. Every form control needs a <code>&lt;label&gt;</code>.</li>
    </ul>
    <h3>Accessible data tables</h3>
    <p>Use <code>&lt;th&gt;</code> for headers with a <code>scope</code>, and a <code>&lt;caption&gt;</code>, so a screen reader can say which row and column each cell belongs to.</p>
    <h3>Text alternatives</h3>
    <p>Every meaningful image needs <span class="term">alt text</span> that says what it shows. Decorative images get an empty <code>alt=""</code>, so they're skipped. A <code>&lt;figure&gt;</code> with <code>&lt;figcaption&gt;</code> adds a visible caption.</p>
    <h3>More on links</h3>
    <ul>
      <li>Links should look like links (underlined, or clearly different) and have visible hover and focus styles.</li>
      <li>Link text should make sense on its own: "Royal Arch trail guide", not "click here". Screen reader users often list every link on a page.</li>
      <li>If a link opens a new tab or a file like a PDF, say so in the link text.</li>
      <li>A <strong>skip link</strong> at the top ("Skip to main content") lets keyboard users jump past the navigation.</li>
      <li>Leave space between links and buttons that sit close together, so they're easy to hit.</li>
    </ul>""")
b += ST("Play", "Find the seven problems", "Click into the sample page and press Tab to move through it. Then switch to the fixed version and compare.") + pg
b += ST("Practice", "Fix the barriers", "This sign-up box has four problems that lock people out. Fix each one.") + '  <div id="ex-a11y"></div>\n\n'
b += ST("Read", "CSS and JavaScript accessibility best practices") + prose("""
    <h3>Correct semantics and user expectation</h3>
    <p>CSS can make anything look like anything, which makes it easy to break what people expect. Keep the conventions: links underlined or otherwise obvious, with distinct <code>:hover</code>, <code>:focus</code> and <code>:visited</code> styles; abbreviations with their dotted underline; buttons that look like buttons; comfortable body text with <code>line-height</code> around 1.5. And never remove the <span class="term">focus</span> outline without putting a clear replacement in its place.</p>
    <h3>Color and color contrast</h3>
    <p>Text needs enough <span class="term" data-term="Contrast ratio">contrast</span> with its background: at least <strong>4.5 to 1</strong> for normal text and 3 to 1 for large text (WCAG AA). And never use color alone to carry meaning, like a red dot for "closed": add a word or an icon.</p>""")
b += ST("Play", "Check the contrast", "Pick a text color and a background. The ratio runs from 1 (no contrast) to 21 (black on white).") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="cc-fg">text color</label><input id="cc-fg" type="color" value="#9aa0ad"></div>
      <div class="control"><label for="cc-bg">background</label><input id="cc-bg" type="color" value="#ffffff"></div>
      <span class="cc-res" id="cc-res" aria-live="polite"></span>
      <table class="cc-tbl" id="cc-tbl"></table>
    </div>
    <div class="cc-sample" id="cc-sample"><span class="big">Large heading text</span><p>Normal body text, like the description of a trail or a form's help text.</p><p style="font-size:0.8rem">Small print: closed after dark, dogs on leash.</p></div>
  </section>

"""
b += prose("""
    <h3>Hiding things</h3>
    <p>There are several ways to hide something, and they don't all hide it from screen readers:</p>
    <ul>
      <li><code>display: none</code> and <code>visibility: hidden</code> hide it from <em>everyone</em>, screen readers included. Use them for things nobody should get, like a closed menu.</li>
      <li>A <strong>visually hidden</strong> class shrinks the element to 1px and clips it. It's invisible on screen but still read aloud. Use it for things only screen reader users need, like a label for an icon-only search button.</li>
      <li><code>opacity: 0</code> makes it invisible but still clickable and read aloud, which is usually confusing.</li>
    </ul>
    <pre class="snippet" data-lang="css">.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}</pre>""")
b += ST("Play", "Ways to hide", "Hide the highlighted label in different ways, and see who still gets it.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="hd-m">hide the label with</label><select id="hd-m"><option value="">(not hidden)</option><option value="dn">display: none</option><option value="vis">visibility: hidden</option><option value="op">opacity: 0</option><option value="vh">.visually-hidden</option></select></div>
      <table class="cc-tbl" id="hd-tbl"></table>
    </div>
    <div class="stage-col">
      <div class="hd-demo"><label for="hd-in" class="tgt" id="hd-lbl">Search trails</label><input id="hd-in" type="search" placeholder="e.g. Mesa"><button class="btn" type="button">🔍</button></div>
      <p class="verdict" id="hd-out" aria-live="polite"></p>
    </div>
  </section>

"""
b += prose("""
    <h3>Accept that users can override styles</h3>
    <p>People may zoom to 200% or more, set a larger default font, force high-contrast colors, or use their own stylesheet. Build layouts that cope: sizes in <code>rem</code>, no fixed heights on text, nothing that relies on exact pixel positions.</p>
    <h3>JavaScript</h3>
    <p>JavaScript can make a page more accessible, or much less. Keep it <strong>unobtrusive</strong>: build the page with real HTML first (a real form with labels and a submit button), then add scripts to improve it, such as checking the form before it's sent. Don't build whole interfaces out of <code>&lt;div&gt;</code>s that only work with a script and a mouse.</p>
    <p>Watch out for <strong>mouse-specific events</strong>. Anything that happens on <code>mouseover</code> should also happen on <code>focus</code>; anything on <code>mouseout</code> should also happen on <code>blur</code>. In CSS, the same goes for <code>:hover</code>: pair it with <code>:focus-visible</code> or <code>:focus-within</code>.</p>""")
b += ST("Practice", "Accessible CSS", "Hide a label the right way, bring back focus styles, and make a hover-only detail work with the keyboard.") + '  <div id="ex-css"></div>\n\n'
b += ST("Your turn", "Five checks for your own project") + checklist
b += notes([
  "Accessibility helps people with visual, hearing, mobility and cognitive disabilities, and everyone else too.",
  "WCAG's four principles: perceivable, operable, understandable, robust.",
  "The browser builds an accessibility tree from your HTML: role, name and state. The right element gets them right.",
  "Text needs 4.5 : 1 contrast; never use color alone to show meaning.",
  "<code>display: none</code> hides from everyone; a visually-hidden class hides from the screen only.",
], [
  "Clickable <code>div</code>s and <code>span</code>s. They can't be reached with Tab.",
  "<code>outline: none</code> with no replacement focus style.",
  "Placeholder text used as the only label.",
  "Things that only appear on <code>:hover</code> or <code>mouseover</code>, so keyboard users never see them.",
])
first = src.first_script()
js = r'''
  // --- See the same card differently ---
  function simUpdate() {
    const blur = $("sim-blur").checked, gray = $("sim-gray").checked, zoom = $("sim-zoom").checked, noimg = $("sim-img").checked;
    const card = $("sim-card");
    card.style.filter = [blur ? "blur(1.6px)" : "", gray ? "grayscale(1)" : ""].join(" ").trim() || "none";
    card.style.fontSize = zoom ? "200%" : ""; card.style.width = zoom ? "100%" : "";
    $("sim-ph").className = "ph" + (noimg ? " off" : "");
    $("sim-ph").textContent = noimg ? "(no alt text, so: nothing)" : "";
    const notes = [];
    if (blur) notes.push("The pale small print becomes unreadable: low contrast fails first.");
    if (gray) notes.push("The red dot was the only sign the trail is closed. Without color, \"Trail status\" tells you nothing.");
    if (zoom) notes.push("At 200%, the layout must reflow without overlapping or cutting off text.");
    if (noimg) notes.push("With no alt text, people who can't see the image get nothing.");
    $("sim-out").textContent = notes.join(" ") || "Turn on a condition.";
  }
  ["sim-blur", "sim-gray", "sim-zoom", "sim-img"].forEach((id) => $(id).addEventListener("input", simUpdate));
  simUpdate();

  // --- Contrast ---
  const lum = (hex) => { const v = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4)); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
  function ccUpdate() {
    const fg = $("cc-fg").value, bg = $("cc-bg").value, a = lum(fg), c = lum(bg);
    const r = (Math.max(a, c) + 0.05) / (Math.min(a, c) + 0.05);
    $("cc-sample").style.color = fg; $("cc-sample").style.background = bg;
    $("cc-res").textContent = r.toFixed(2) + " : 1";
    const row = (t, min) => `<tr><td>${t}</td><td>${min} : 1</td><td class="${r >= min ? "y" : "n"}">${r >= min ? "pass" : "fail"}</td></tr>`;
    $("cc-tbl").innerHTML = row("Normal (AA)", 4.5) + row("Large (AA)", 3) + row("Normal (AAA)", 7);
  }
  ["cc-fg", "cc-bg"].forEach((id) => $(id).addEventListener("input", ccUpdate));
  ccUpdate();

  // --- Ways to hide ---
  const HD = {
    "": ["yes", "yes", "yes", "Visible to everyone."],
    dn: ["no", "no", "no", "Gone for everyone, screen readers included. The search field now has no name."],
    vis: ["no", "yes", "no", "Invisible and silent, but it still takes up space, leaving a gap."],
    op: ["no", "yes", "yes", "Invisible, but it still takes space and is still read aloud. Confusing for sighted screen reader users."],
    vh: ["no", "no", "yes", "Invisible on screen, but screen readers still announce \"Search trails\" for the field. The right choice here."],
  };
  function hdUpdate() {
    const m = $("hd-m").value, l = $("hd-lbl"), [vis, space, sr, msg] = HD[m];
    l.className = "tgt" + (m === "vh" ? " vh" : "");
    l.style.display = m === "dn" ? "none" : ""; l.style.visibility = m === "vis" ? "hidden" : ""; l.style.opacity = m === "op" ? "0" : "";
    const cell = (v) => `<td class="${v === "yes" ? "y" : "n"}">${v}</td>`;
    $("hd-tbl").innerHTML = `<tr><td>can be seen</td>${cell(vis)}</tr><tr><td>takes up space</td>${cell(space)}</tr><tr><td>read by screen readers</td>${cell(sr)}</tr>`;
    $("hd-out").className = "verdict" + (m === "vh" || m === "" ? "" : " bad");
    $("hd-out").textContent = msg;
  }
  $("hd-m").addEventListener("input", hdUpdate);
  hdUpdate();
'''
ex_a = src.block('  makeExercise(document.getElementById("ex-a11y"), {')
ex_c = r'''  makeExercise(document.getElementById("ex-css"), {
    title: "Hidden labels, focus and hover",
    task: `<ol>
      <li>The search box's label should be invisible on screen but still read by screen readers. Make <code>.label</code> visually hidden: <code>position: absolute</code>, 1px by 1px, <code>overflow: hidden</code> and <code>clip-path: inset(50%)</code>. Don't use <code>display: none</code>.</li>
      <li>Someone removed the focus outline from links. Replace that rule with a visible <code>:focus-visible</code> outline.</li>
      <li>The trail details only appear on <code>:hover</code>. Make them appear when the link has keyboard focus too.</li>
    </ol>`,
    html: `<form class="search">
  <label for="q" class="label">Search trails</label>
  <input id="q" type="search" placeholder="e.g. Mesa">
  <button>Search</button>
</form>
<p><a class="card" href="#">Royal Arch <span class="more">· 1.7 mi · Hard</span></a></p>`,
    css: `body { font-family: system-ui, sans-serif; }
a:focus { outline: none; }
.more { display: none; }
.card:hover .more { display: inline; }`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
.label {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}
a:focus-visible { outline: 3px solid #2340d9; outline-offset: 2px; }
.more { display: none; }
.card:hover .more,
.card:focus-visible .more { display: inline; }` },
    hints: [
      "display: none would hide the label from screen readers too. Shrink and clip it instead.",
      "Delete a:focus { outline: none; } and add a:focus-visible { outline: 3px solid #2340d9; }.",
      "Add .card:focus-visible .more (or .card:focus .more) to the hover rule's selector list.",
    ],
    checks: (() => {
      const rules = (doc) => [...doc.styleSheets[0].cssRules].filter((r) => r.selectorText);
      return [
        { label: "The label is visually hidden, not display: none", test: ({ $, style }) => { const r = $(".label").getBoundingClientRect(); return style(".label", "display") !== "none" && style(".label", "visibility") !== "hidden" && style(".label", "position") === "absolute" && r.width <= 1 && r.height <= 1; } },
        { label: "The input still has its label", test: ({ $ }) => $("#q").labels.length === 1 },
        { label: "No rule removes the focus outline", test: ({ doc }) => !rules(doc).some((r) => /:focus/.test(r.selectorText) && r.style.outlineStyle === "none") },
        { label: "Links get a visible :focus-visible outline", test: ({ doc }) => rules(doc).some((r) => /a:focus-visible|\.card:focus-visible/.test(r.selectorText) && r.style.outlineStyle && r.style.outlineStyle !== "none") },
        { label: "Keyboard focus shows the details too", test: ({ doc }) => rules(doc).some((r) => r.selectorText.split(",").some((s) => /\.card:focus(-visible|-within)?\s+\.more/.test(s.trim())) && r.style.display && r.style.display !== "none") },
      ];
    })(),
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "What does the P in WCAG's POUR stand for?", opts: ["Perceivable", "Programmable", "Portable"], a: 0, why: "Perceivable, operable, understandable, robust." },
    { id: "q6", q: "You want a label only screen reader users get. Which is right?", opts: ["display: none", "visibility: hidden", "A visually-hidden class"], a: 2, why: "display: none and visibility: hidden hide it from screen readers too." },
    { id: "q7", q: "What's the minimum contrast for normal body text (WCAG AA)?", opts: ["2 : 1", "4.5 : 1", "10 : 1"], a: 1, why: "Large text needs 3 : 1; normal text 4.5 : 1." },
    { id: "q8", q: "A tooltip shows on mouseover. What else should show it?", opts: ["Nothing", "focus, so keyboard users get it too", "A double-click"], a: 1, why: "Pair mouse events with focus and blur, and :hover with :focus-visible." },
  ]);
''')
write("core-accessibility.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_a + "\n" + ex_c + "</script>\n")
