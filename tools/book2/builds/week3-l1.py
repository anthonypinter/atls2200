import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("css-basics")
anatomy = src.between('  <section class="playground even">\n    <div class="stage-col">\n      <div class="anatomy"', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Three places')
ways = src.between('  <div class="ways" id="ways"></div>', '  <div class="section-title"><span class="eyebrow">Practice</span>')
extra = """
  .dflt { display: grid; gap: 10px; }
  .dflt iframe { width: 100%; height: 300px; border: 1px solid var(--line); border-radius: 8px; background: #fff; }
  .sh-box { display: grid; place-items: center; padding: 18px; background: var(--stage); border-radius: 8px; }
  .sh-pad { background: color-mix(in srgb, var(--good) 30%, transparent); outline: 2px dashed var(--good); display: inline-block; }
  .sh-pad span { display: block; background: var(--cobalt); color: #fff; padding: 10px 14px; font: 700 0.85rem var(--font-code); }
  .longhands { margin: 0; padding: 0; list-style: none; font: 0.9rem/1.8 var(--font-code); font-variation-settings: "MONO" 1; }
  .longhands b { color: var(--prop); font-weight: 600; }
  .longhands i { color: var(--val); font-style: normal; }
"""
h = head("What is CSS?", src.css(), extra)
b = top("What is CSS?", "HTML says what each part of a page is. CSS (Cascading Style Sheets) says how it looks: colours, fonts, spacing, layout, even animation. This lesson covers how a rule is written and the three places it can live.", [
  "Explain what browsers do with an unstyled page, and what CSS is for.",
  "Name the parts of a CSS rule: selector, declaration, property and value.",
  "Add CSS with an external stylesheet, a <code>&lt;style&gt;</code> element or an inline style, and know which to use.",
  "Recognise functions, @rules, shorthand properties and comments."])
b += ST("Read", "Browser default styles") + prose("""
    <p>Even a page with no CSS at all isn't plain text. Headings are big and bold, lists have bullets, links are blue and underlined. That's because every browser has a built-in <span class="term" data-term="User agent stylesheet">default stylesheet</span> that makes unstyled HTML readable.</p>
    <p>Those defaults are deliberately plain, and they differ slightly between browsers. Your CSS builds on top of them.</p>""")
b += ST("Play", "Turn the stylesheet off", "The same HTML, with and without a stylesheet.") + """  <div class="panel dflt">
    <div class="seg" id="dflt-mode" role="group" aria-label="Stylesheet">
      <button class="btn" type="button" data-m="off" aria-pressed="true">Browser defaults only</button>
      <button class="btn" type="button" data-m="on" aria-pressed="false">With our stylesheet</button>
    </div>
    <iframe id="dflt" title="Example page"></iframe>
  </div>

"""
b += ST("Read", "What is CSS for?") + prose("""
    <p>CSS controls everything about how a page looks:</p>
    <ul>
      <li><strong>Text:</strong> fonts, sizes, colours, spacing between lines and letters.</li>
      <li><strong>Boxes:</strong> backgrounds, borders, rounded corners, shadows and the space around everything.</li>
      <li><strong>Layout:</strong> columns, grids, sidebars, and how all of it rearranges on a phone.</li>
      <li><strong>Movement:</strong> transitions and animations.</li>
    </ul>
    <p>This week covers the language itself. Weeks 4 to 6 use it for styling, layout and responsive design.</p>""")
b += ST("Read", "CSS syntax basics") + prose("""
    <p>A <span class="term">stylesheet</span> is a list of <span class="term" data-term="Rule">rules</span>, and every rule has the same shape:</p>
    <pre class="snippet" data-lang="css">h1 {
  color: navy;
  font-size: 2rem;
}</pre>
    <p>The <span class="term">selector</span>, <code>h1</code>, picks which elements the rule applies to. Inside the braces are <span class="term" data-term="Declaration">declarations</span>, each a <span class="term">property</span> and a <span class="term">value</span> separated by a colon and ending with a semicolon. This rule says: make every <code>h1</code> navy and twice the normal text size.</p>""")
b += ST("Play", "Anatomy of a rule", "Click any part of the rule, or pick a name below.") + anatomy
b += ST("Read", "How is CSS applied to HTML?") + prose("""
    <p>When a browser loads a page, it reads the HTML into a tree of elements (the DOM), reads the CSS, and works out which rules apply to which elements. Then it lays out and paints the result. Every element can be matched by many rules at once, and each rule can match many elements.</p>
    <p>So one rule, <code>p { color: navy; }</code>, colours every paragraph on the page, and adding a paragraph later means it's styled automatically. Try it.</p>""")
b += ST("Play", "Write some CSS", "Edit either side. Add a paragraph, then an <code>h2</code> and a rule for it.") + """  <div class="two">
    <div class="panel" style="display:grid;gap:8px">
      <label class="eyebrow" for="pl-html">HTML</label>
      <textarea class="src" id="pl-html" spellcheck="false" style="min-height:120px"></textarea>
      <label class="eyebrow" for="pl-css">CSS</label>
      <textarea class="src" id="pl-css" spellcheck="false" style="min-height:140px"></textarea>
    </div>
    <div class="panel" style="display:grid;gap:8px;align-content:start"><span class="eyebrow">Result</span><iframe class="preview" id="pl-out" title="Result"></iframe><p class="verdict" id="pl-note" aria-live="polite"></p></div>
  </div>

"""
b += ST("Read", "Adding CSS to our document") + prose("""
    <p>CSS can live in three places:</p>
    <h3>External stylesheets</h3>
    <p>A separate <code>.css</code> file, linked from the <code>&lt;head&gt;</code>:</p>
    <pre class="snippet" data-lang="html">&lt;link rel="stylesheet" href="styles.css"&gt;</pre>
    <p>The <code>href</code> is a path, just like a link's: <code>css/styles.css</code> if it's in a folder, <code>../styles.css</code> from a page one folder down. One file can style every page of a site, so changing a colour once changes it everywhere, and browsers download it only once. Use this for real projects.</p>
    <h3>Internal stylesheets</h3>
    <p>A <code>&lt;style&gt;</code> element in the head. It styles only that one page, so a multi-page site would repeat it in every file.</p>
    <h3>Inline styles</h3>
    <p>A <code>style</code> attribute on a single element: <code>&lt;span style="color: purple"&gt;</code>. It mixes styling into your content, is hard to find later, and beats your stylesheet, which makes it hard to override. Avoid it.</p>""")
b += ST("Play", "Three places to put CSS", "All three try to colour the same heading. Turn them on and off and swap the order of the two in the head.") + ways
b += ST("Practice", "Fix the stylesheet", "One missing character can wipe out a whole rule. Find the three mistakes.") + '  <div id="ex-rules"></div>\n\n'
b += ST("Read", "Using common selectors") + prose("""
    <p>Next lesson covers selectors in depth. Here's a quick tour of the ones you'll use most:</p>
    <ul>
      <li><strong>Elements:</strong> <code>p { }</code> styles every paragraph. List several with commas: <code>p, li { }</code>.</li>
      <li><strong>Classes:</strong> add <code>class="special"</code> in the HTML, then select it with a dot: <code>.special { }</code>.</li>
      <li><strong>Location:</strong> <code>li em { }</code> selects <code>em</code>s inside list items; <code>h1 + p { }</code> selects a paragraph straight after an <code>h1</code>.</li>
      <li><strong>State:</strong> <code>a:hover { }</code> styles a link while the pointer is over it; <code>a:visited { }</code> once it's been visited.</li>
    </ul>""")
b += ST("Practice", "Style the trail page", "Write four rules using the selectors above.") + '  <div id="ex-selectors"></div>\n\n'
b += ST("Read", "Other CSS syntax features") + prose("""
    <h3>Functions</h3>
    <p>Some values are calculated by a function, written as a name and brackets: <code>width: calc(90% - 30px);</code> or <code>transform: rotate(0.8turn);</code>.</p>
    <h3>@rules</h3>
    <p>Rules starting with <code>@</code> give CSS special instructions. The most common, <code>@media</code>, applies styles only when a condition is true, like a wide enough screen (Week 6):</p>
    <pre class="snippet" data-lang="css">@media (width >= 30em) {
  body { background-color: lightblue; }
}</pre>
    <h3>Shorthand properties</h3>
    <p>Some properties set several others at once. <code>padding: 10px 15px 15px 5px;</code> sets the top, right, bottom and left padding, going clockwise from the top.</p>""")
b += ST("Play", "Expand the shorthand", "Type one to four values for <code>padding</code>.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:8px;align-content:start">
      <label class="eyebrow" for="sh-in">padding:</label>
      <input class="src" id="sh-in" value="10px 20px" spellcheck="false" autocomplete="off">
      <div class="presets" id="sh-presets" role="group" aria-label="Examples">
        <button class="btn" type="button">10px</button><button class="btn" type="button">10px 20px</button><button class="btn" type="button">5px 20px 30px</button><button class="btn" type="button">10px 15px 15px 5px</button>
      </div>
      <ul class="longhands" id="sh-out"></ul>
    </div>
    <div class="sh-box"><div class="sh-pad" id="sh-pad"><span>content</span></div></div>
  </section>

"""
b += prose("""
    <h3>Comments</h3>
    <p>Comments are notes the browser ignores, written between <code>/*</code> and <code>*/</code>. Use them to label sections of a stylesheet, or to switch a rule off while you test.</p>
    <pre class="snippet" data-lang="css">/* Trail cards */
.card { padding: 1rem; }</pre>
    <h3>White space</h3>
    <p>CSS ignores extra spaces and line breaks between parts, so put one declaration per line for readability. But spaces <em>inside</em> a property name or between a number and its unit break it: <code>margin: 0auto;</code> and <code>padding- left: 10px;</code> are both invalid.</p>""")
b += notes([
  "Browsers have default styles; your CSS builds on them.",
  "A rule is a selector plus a declaration block; each declaration is <code>property: value;</code>.",
  "Use an external stylesheet for real projects. One file can style every page of the site.",
  "Shorthands like <code>padding</code> go clockwise: top, right, bottom, left.",
  "Comments look like <code>/* like this */</code>.",
], [
  "A <code>&lt;link&gt;</code> with the wrong path, so no styles load at all.",
  "A missing semicolon, colon or brace, which breaks the next declaration or rule.",
  "Using inline <code>style=\"\"</code> everywhere: hard to change, and it beats your stylesheet.",
  "HTML comments (<code>&lt;!-- --&gt;</code>) or <code>//</code> in a CSS file.",
  "A space between a number and its unit: <code>16 px</code>.",
])
first = src.first_script()
js = r'''
  // --- Browser defaults ---
  const PAGE = '<h1>Boulder Trail Club</h1><p>Weekend hikes for every pace. <a href="#">See the schedule</a>.</p><h2>This week</h2><ul><li>Mesa Trail, Saturday</li><li>Royal Arch, Sunday</li></ul><blockquote>Best views in town.</blockquote>';
  const SHEET = 'body{font:17px/1.6 Georgia,serif;margin:0;padding:20px 28px;background:#f7f3ea;color:#2b2a26}h1{font:800 2rem system-ui,sans-serif;color:#0b6b5e;margin:0 0 6px}h2{font:700 1rem system-ui,sans-serif;text-transform:uppercase;letter-spacing:.08em;color:#b4410c}a{color:#0b6b5e}ul{padding-left:1.1em}blockquote{margin:0;border-left:4px solid #0b6b5e;padding-left:12px;font-style:italic}';
  function dflt(m) {
    $("dflt").srcdoc = "<!doctype html><html><head>" + (m === "on" ? "<style>" + SHEET + "</style>" : "") + "</head><body>" + PAGE;
    document.querySelectorAll("#dflt-mode .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.m === m)));
  }
  $("dflt-mode").addEventListener("click", (e) => { const b = e.target.closest("[data-m]"); if (b) dflt(b.dataset.m); });
  dflt("off");

  // --- Write some CSS ---
  $("pl-html").value = "<h1>CSS is great</h1>\n<p>You can style text.</p>\n<p>And change colours.</p>";
  $("pl-css").value = "h1 {\n  color: #0b6b5e;\n  font-size: 2.5em;\n}\n\np {\n  color: navy;\n  padding: 5px;\n}";
  let plTimer;
  function play() {
    $("pl-out").srcdoc = "<!doctype html><html><head><style>body{font-family:system-ui,sans-serif}" + $("pl-css").value + "</style></head><body>" + $("pl-html").value;
    clearTimeout(plTimer);
    plTimer = setTimeout(() => {
      const d = $("pl-out").contentDocument; if (!d || !d.body) return;
      const n = d.querySelectorAll("p").length;
      $("pl-note").textContent = `One p rule is styling ${n} paragraph${n === 1 ? "" : "s"}.`;
    }, 150);
  }
  ["pl-html", "pl-css"].forEach((id) => $(id).addEventListener("input", play));
  play();

  // --- Shorthand ---
  function shorthand() {
    const v = $("sh-in").value.trim().split(/\s+/).filter(Boolean);
    const ok = v.length >= 1 && v.length <= 4 && v.every((x) => /^\d+(\.\d+)?(px|em|rem|%)?$/.test(x));
    if (!ok) { $("sh-out").innerHTML = "<li>Use one to four lengths, like 10px 20px.</li>"; return; }
    const [t, r = t, bt = t, l = r] = v;
    const sides = [["top", t], ["right", r], ["bottom", bt], ["left", l]];
    $("sh-out").innerHTML = sides.map(([s, x]) => `<li><b>padding-${s}</b>: <i>${x}</i>;</li>`).join("");
    const px = (x) => (/^\d/.test(x) && !/(em|rem|%)$/.test(x) ? parseFloat(x) + "px" : x);
    $("sh-pad").style.padding = sides.map(([, x]) => px(x)).join(" ");
  }
  $("sh-in").addEventListener("input", shorthand);
  $("sh-presets").addEventListener("click", (e) => { const b = e.target.closest(".btn"); if (b) { $("sh-in").value = b.textContent; shorthand(); } });
  shorthand();
'''
ex_rules = src.block('  makeExercise(document.getElementById("ex-rules"), {')
ex_sel = r'''  makeExercise(document.getElementById("ex-selectors"), {
    title: "Four selectors",
    task: `<ol>
      <li>Make paragraphs <em>and</em> list items <code>color: #333333</code>, in one rule with a comma.</li>
      <li>Give anything with <code>class="special"</code> <code>color: orange</code> and <code>font-weight: bold</code>.</li>
      <li>Make <code>em</code> elements inside list items <code>color: rebeccapurple</code>.</li>
      <li>Make the paragraph straight after the <code>h1</code> <code>font-size: 150%</code>.</li>
    </ol>`,
    html: `<h1>Royal Arch</h1>
<p>A steep climb to a sandstone arch.</p>
<p class="special">Closed after heavy rain.</p>
<ul>
  <li>Bring <em>plenty</em> of water</li>
  <li>Start early</li>
</ul>`,
    css: `body { font-family: system-ui, sans-serif; }
/* Your rules here */
`,
    solution: { css: `body { font-family: system-ui, sans-serif; }

p, li {
  color: #333333;
}

.special {
  color: orange;
  font-weight: bold;
}

li em {
  color: rebeccapurple;
}

h1 + p {
  font-size: 150%;
}
` },
    hints: ["A dot in front of a name selects a class: .special", "A space means “inside”: li em. A plus means “straight after”: h1 + p."],
    checks: [
      { label: "Paragraphs and list items are #333333", test: ({ style }) => style("li", "color") === "rgb(51, 51, 51)" && style("p", "color") === "rgb(51, 51, 51)" },
      { label: ".special is orange and bold", test: ({ style }) => style(".special", "color") === "rgb(255, 165, 0)" && +style(".special", "font-weight") >= 700 },
      { label: "em inside li is rebeccapurple", test: ({ style }) => style("li em", "color") === "rgb(102, 51, 153)" },
      { label: "The paragraph after h1 is 150%", test: ({ style, $$ }) => { const ps = $$("p"); return parseFloat(style(ps[0], "font-size")) > parseFloat(style(ps[1], "font-size")) * 1.4; } },
    ],
  });
'''
quiz = r'''  makeQuiz(document.getElementById("quiz"), [
    { id: "q1", q: "A page with no CSS still has big bold headings. Why?", opts: ["The browser's default stylesheet", "HTML headings contain their own CSS", "The server adds styles"], a: 0, why: "Every browser applies built-in default styles." },
    { id: "q2", q: "In p { color: navy; }, what is color?", opts: ["The selector", "A value", "A property"], a: 2, why: "color is the property; navy is its value; p is the selector." },
    { id: "q3", q: "Which way of adding CSS can style every page of a site from one file?", opts: ["An external stylesheet", "A <style> element", "Inline style attributes"], a: 0, why: "Every page links the same .css file, so one change updates them all." },
    { id: "q4", q: "padding: 10px 20px; sets which padding to 20px?", opts: ["Left and right", "Top and bottom", "Only the right"], a: 0, why: "Two values: top/bottom, then left/right." },
    { id: "q5", q: "Which comment works in a CSS file?", opts: ["<!-- note -->", "// note", "/* note */"], a: 2, why: "CSS only understands /* */ comments." },
    { id: "q6", q: "What's wrong with margin: 0auto;?", opts: ["There must be a space between the two values", "auto isn't a valid value", "Nothing"], a: 0, why: "0auto is read as one unknown value, so the declaration is ignored." },
  ]);
'''
write("core-what-is-css.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_rules + "\n" + ex_sel + "\n" + quiz + "</script>\n")
