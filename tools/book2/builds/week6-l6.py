import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("organizing-css")
steps = src.between('  <div class="steps" id="steps"', '  <div class="section-title"><span class="eyebrow">Practice</span><h2>Where does')
h = head("Organizing CSS", src.css(), """
  .fm-pre { margin: 0; background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); padding: 14px 16px; font: 0.86rem/1.6 var(--font-code); font-variation-settings: "MONO" 1; overflow-x: auto; white-space: pre; min-height: 220px; }
  .bem-card { background: #fff; color: #1d2133; border: 2px solid #e3e6ef; border-radius: 10px; padding: 12px; display: grid; gap: 8px; max-width: 320px; font-family: var(--font-body); transition: border-color 0.2s, box-shadow 0.2s; }
  .bem-card.featured { border-color: #b4410c; box-shadow: 0 6px 18px rgb(180 65 12 / 25%); }
  .bem-card [data-bem] { cursor: pointer; border-radius: 4px; outline: 2px dashed transparent; outline-offset: 2px; }
  .bem-card [data-bem]:hover, .bem-card [data-bem]:focus-visible { outline-color: #9aa2bf; }
  .bem-card [data-bem].picked { outline-color: #2340d9; }
  .bem-card .img { height: 90px; background: linear-gradient(170deg, #f4a261 0 45%, #7d5a7a 45% 70%, #3e4a61 70%); }
  .bem-card h4 { margin: 0; font: 800 1.1rem var(--font-display); }
  .bem-card p { margin: 0; font-size: 0.9rem; }
  .bem-card .b { justify-self: start; background: #2340d9; color: #fff; padding: 5px 12px; border-radius: 5px; font-size: 0.85rem; }
  .bem-out { font: 700 1.1rem var(--font-code); font-variation-settings: "MONO" 1; color: var(--cobalt); }
""")
b = top("Organizing CSS", "CSS doesn't care how your stylesheet is arranged. You do, the next time you need to change something and can't find it. A few habits, and a naming system or two, keep a stylesheet easy to work with as it grows.", [
  "Format and comment a stylesheet so it's easy to read and search.",
  "Group rules into sections in a consistent order, and keep specificity low.",
  "Name classes with a methodology like BEM.",
  "Describe what preprocessors like Sass and build tools do.",
])
b += ST("Read", "Tips to keep your CSS tidy") + prose("""
    <h3>Does your project have a coding style guide?</h3>
    <p>If you're working with a team, or on an existing project, check whether there's a style guide first. Following the team's conventions matters more than your own preferences: a stylesheet written five different ways is harder to work with than one written any single way.</p>
    <h3>Keep it consistent</h3>
    <p>Whatever rules you choose, use them everywhere: the same way of naming classes, the same color format (all hex, or all <code>rgb()</code>), the same indentation. Consistency means you can predict where things are and how they're written.</p>
    <h3>Formatting readable CSS</h3>
    <p>Some people write each rule on one line; most put each declaration on its own line, which is easier to scan and gives cleaner diffs in version control. Either is fine as long as you're consistent.</p>""")
b += ST("Play", "The same CSS, three ways", "Switch between formats. The browser reads them all the same way.") + """  <section class="playground">
    <div class="panel controls">
      <div class="seg" id="fm-seg" role="group" aria-label="Format">
        <button class="btn" data-f="one" aria-pressed="false">One line per rule</button>
        <button class="btn" data-f="multi" aria-pressed="true">One declaration per line</button>
        <button class="btn" data-f="cmt" aria-pressed="false">With section comments</button>
      </div>
      <p class="hint" id="fm-out" aria-live="polite"></p>
    </div>
    <pre class="fm-pre" id="fm-pre"></pre>
  </section>

"""
b += prose("""
    <h3>Comment your CSS</h3>
    <p>Comments help the next person, including you in six months. Use them for two things. First, section headings, written in a way that's easy to search for. MDN suggests <code>||</code>, which rarely appears anywhere else, so searching for <code>||</code> jumps from section to section:</p>
    <pre class="snippet" data-lang="css">/* || General styles */
/* || Utilities */
/* || Site-wide */</pre>
    <p>Second, explain anything surprising, like why a rule exists:</p>
    <pre class="snippet" data-lang="css">.box {
  background-color: red; /* fallback for browsers without gradients */
  background-image: linear-gradient(to right, #ff0000, #aa0000);
}</pre>
    <h3>Create logical sections in your stylesheet</h3>
    <p>A good order runs from general to specific:</p>
    <ol>
      <li><strong>General styles</strong> for plain elements: <code>body</code>, <code>p</code>, headings, lists, links, tables.</li>
      <li><strong>Utility classes</strong>: tiny one-job classes like <code>.no-bullets</code> or <code>.text-center</code>.</li>
      <li><strong>Site-wide components</strong>: things on every page, like <code>.main-nav</code> and <code>.logo</code>.</li>
      <li><strong>Specific components and pages</strong>: cards, the trail page, the sign-up form.</li>
    </ol>
    <p>Because later rules win ties, this order also means the specific stuff naturally overrides the general.</p>""")
b += ST("Play", "Clean up a stylesheet", "Step through four cleanups. The page looks identical at every step; only the stylesheet changes.") + steps
b += ST("Practice", "Where does this rule go?", "Base styles for plain elements, then layout, then components, then small utility classes.") + '  <div class="panel quiz" id="quiz1"></div>\n\n'
b += ST("Read", "Avoid overly-specific selectors") + prose("""
    <p>A selector like <code>article.main p.box</code> only works in one exact place, and its high <span class="term">specificity</span> makes it hard to override. Then the override needs an even longer selector, and eventually <code>!important</code>. Style with single classes instead: <code>.box</code> works wherever you put it.</p>""")
b += ST("Read", "Break large stylesheets into multiple smaller ones") + prose("""
    <p>On a big site, one huge file gets hard to navigate. You can split it, for example into a global stylesheet and one per section, and link them in order. Rules in later files win ties, just as later rules in one file do:</p>
    <pre class="snippet" data-lang="html">&lt;link rel="stylesheet" href="global.css"&gt;
&lt;link rel="stylesheet" href="trails.css"&gt;</pre>""")
b += ST("Read", "Other tools that can help") + prose("""
    <h3>CSS methodologies</h3>
    <p>Some teams follow a published set of rules for writing CSS, called a methodology. Two well-known ones:</p>
    <ul>
      <li><strong>OOCSS</strong> (Object-Oriented CSS) separates reusable patterns into classes. A common "media object", an image beside some text, gets one <code>.media</code> class reused everywhere, instead of being styled again in each place.</li>
      <li><span class="term">BEM</span> (Block, Element, Modifier) is a naming system. A <strong>block</strong> is a standalone component (<code>.card</code>). An <strong>element</strong> is a part of it, joined with two underscores (<code>.card__title</code>). A <strong>modifier</strong> is a variation, joined with two hyphens (<code>.card--featured</code>). The names are long, but you can tell from a class alone what it belongs to.</li>
    </ul>
    <p>Others include SMACSS, ITCSS and Atomic CSS. You don't need one for a small project, but you'll meet them on bigger ones.</p>""")
b += ST("Play", "Name the parts with BEM", "Click each part of the card to see its BEM class. Then turn on the modifier.") + """  <section class="playground">
    <div class="panel controls">
      <span class="bem-out" id="bem-out">.card</span>
      <p class="hint" id="bem-why"></p>
      <label class="toggle"><input type="checkbox" id="bem-mod"> add a modifier</label>
      <pre class="snippet" id="bem-code"></pre>
    </div>
    <div class="stage-col">
      <div class="bem-card" id="bem-card" data-bem="block" tabindex="0">
        <div class="img" data-bem="image" tabindex="0"></div>
        <h4 data-bem="title" tabindex="0">Royal Arch</h4>
        <p data-bem="text" tabindex="0">A steep climb to a sandstone arch.</p>
        <span class="b" data-bem="button" tabindex="0">Details</span>
      </div>
    </div>
  </section>

"""
b += ST("Practice", "Pick the better class name", "Name classes for what something <em>is</em>, not how it looks.") + '  <div class="panel quiz" id="quiz2"></div>\n\n'
b += prose("""
    <h3>Build systems for CSS</h3>
    <p>Larger projects often run CSS through tools before it reaches the browser.</p>
    <p>A <strong>preprocessor</strong> like Sass adds features to CSS and compiles your files into plain CSS. Sass variables (<code>$brand: #2340d9;</code>) came before CSS had its own; today native <span class="term">CSS variables</span> do the same job in the browser. Sass is still popular for splitting styles into small <em>partial</em> files and combining them with <code>@use</code>:</p>
    <pre class="snippet" data-lang="scss">// main.scss
@use "base";
@use "layout";
@use "components/card";</pre>
    <p>A <strong>post-processor</strong> works on the finished CSS: for example, cssnano strips comments and spaces to make the file smaller. Your readable, commented source stays readable; the browser gets the small version.</p>""")
b += ST("Practice", "Clean up the stylesheet", "Rename a class by its purpose, store the repeated color once, and drop a heavy selector.") + '  <div id="ex-organize"></div>\n\n'
b += ST("Practice", "Sections and BEM", "Put the rules in labeled sections, then rename the card's parts with BEM.") + '  <div id="ex-bem"></div>\n\n'
b += notes([
  "Follow the team's style guide; whatever you choose, be consistent.",
  "Use searchable section comments like <code>/* || Base */</code>, and comment anything surprising.",
  "Order sections from general to specific: base, utilities, site-wide, components.",
  "Keep specificity low: single classes, not long chains or IDs.",
  "BEM: <code>.block</code>, <code>.block__element</code>, <code>.block--modifier</code>.",
], [
  "Adding every new rule to the bottom of the file.",
  "Names like <code>.box2</code>, <code>.new</code> or <code>.left</code> that stop making sense later.",
  "Overriding a long selector with an even longer one, then <code>!important</code>.",
  "Leaving old, unused rules in \"just in case\". That's what version control is for.",
])
first = src.first_script()
cut = first.index("  // Questions without their own opts share the ones passed in.")
sortq = first[cut:].replace("function quiz(el, Q, opts) { makeQuiz($(el),", "function sortQuiz(el, Q, opts) { makeQuiz(document.getElementById(el),").replace('  quiz("quiz', '  sortQuiz("quiz')
assert sortq.count("sortQuiz(") == 3, sortq
first = first[:cut]
js = r'''
  // --- Formatting ---
  const FM = {
    one: `body { margin: 0; font-family: Georgia, serif; color: #1d2133; }
a { color: #2340d9; }
.container { max-width: 960px; margin: 0 auto; }
.card { padding: 16px; border-radius: 10px; }
.card__title { color: #0b6b5e; }`,
    multi: `body {
  margin: 0;
  font-family: Georgia, serif;
  color: #1d2133;
}

a {
  color: #2340d9;
}

.container {
  max-width: 960px;
  margin: 0 auto;
}

.card {
  padding: 16px;
  border-radius: 10px;
}

.card__title {
  color: #0b6b5e;
}`,
  };
  FM.cmt = "/* || General styles */\n\n" + FM.multi.replace("\n\n.container", "\n\n/* || Layout */\n\n.container").replace("\n\n.card {", "\n\n/* || Components */\n\n/* Trail card */\n.card {");
  const FMN = { one: "Compact: you see the whole file at once, but long rules get hard to read.", multi: "Easiest to scan, and a change to one property shows up as one changed line in version control.", cmt: "Search for || to jump between sections." };
  function fmShow(f) {
    $("fm-pre").textContent = FM[f]; $("fm-out").textContent = FMN[f];
    document.querySelectorAll("#fm-seg button").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.f === f)));
  }
  $("fm-seg").addEventListener("click", (e) => { const x = e.target.closest("button"); if (x) fmShow(x.dataset.f); });
  fmShow("multi");

  // --- BEM ---
  const BEM = {
    block: [".card", "The block: a standalone component that makes sense on its own."],
    image: [".card__image", "An element: part of the card, joined with two underscores."],
    title: [".card__title", "An element. It's .card__title, not .card__h4: name it by its job, not its tag."],
    text: [".card__text", "An element. Elements belong to the block, never to another element: no .card__title__text."],
    button: [".card__button", "An element. If buttons appear outside cards too, make .btn its own block instead."],
  };
  let bemCur = "block";
  function bemShow() {
    const mod = $("bem-mod").checked;
    $("bem-card").classList.toggle("featured", mod);
    document.querySelectorAll("#bem-card [data-bem], #bem-card").forEach((el) => el.classList.toggle("picked", el.dataset.bem === bemCur));
    $("bem-out").textContent = BEM[bemCur][0]; $("bem-why").textContent = BEM[bemCur][1];
    $("bem-code").textContent = `<article class="card${mod ? " card--featured" : ""}">\n  <img class="card__image" …>\n  <h3 class="card__title">Royal Arch</h3>\n  <p class="card__text">…</p>\n  <a class="card__button" …>Details</a>\n</article>` + (mod ? "\n\n.card--featured {\n  border-color: #b4410c;\n}" : "");
  }
  $("bem-card").addEventListener("click", (e) => { const el = e.target.closest("[data-bem]"); if (el) { bemCur = el.dataset.bem; bemShow(); } });
  $("bem-card").addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { const el = e.target.closest("[data-bem]"); if (el) { e.preventDefault(); bemCur = el.dataset.bem; bemShow(); } } });
  $("bem-mod").addEventListener("input", bemShow);
  bemShow();
'''
ex_o = src.block('  makeExercise(document.getElementById("ex-organize"), {')
ex_b = r'''  makeExercise(document.getElementById("ex-bem"), {
    title: "Sections and BEM names",
    task: `<ol>
      <li>Add three section comments, in this order: <code>/* || Base */</code>, <code>/* || Layout */</code> and <code>/* || Components */</code>.</li>
      <li>Move the rules under the right headings: <code>body</code> and <code>a</code> in Base, <code>.container</code> in Layout, the card rules in Components.</li>
      <li>Rename with BEM: give the card's <code>h3</code> the class <code>card__title</code> and style that instead of <code>.card h3</code>; rename <code>featured</code> to the modifier <code>card--featured</code>.</li>
    </ol>`,
    html: `<div class="container">
  <article class="card featured"><h3>Royal Arch</h3><p>A steep climb to a sandstone arch.</p></article>
  <article class="card"><h3>Mesa Trail</h3><p>Rolling and shady.</p></article>
</div>`,
    css: `.card { padding: 12px; border: 2px solid #e3e6ef; margin-bottom: 10px; }
a { color: #2340d9; }
.card h3 { margin: 0; color: #0b6b5e; }
.container { max-width: 600px; margin: 0 auto; }
body { font-family: system-ui, sans-serif; }
.card.featured { border-color: #b4410c; }`,
    solution: {
      html: `<div class="container">
  <article class="card card--featured"><h3 class="card__title">Royal Arch</h3><p>A steep climb to a sandstone arch.</p></article>
  <article class="card"><h3 class="card__title">Mesa Trail</h3><p>Rolling and shady.</p></article>
</div>`,
      css: `/* || Base */
body { font-family: system-ui, sans-serif; }
a { color: #2340d9; }

/* || Layout */
.container { max-width: 600px; margin: 0 auto; }

/* || Components */
.card { padding: 12px; border: 2px solid #e3e6ef; margin-bottom: 10px; }
.card__title { margin: 0; color: #0b6b5e; }
.card--featured { border-color: #b4410c; }`,
    },
    hints: [
      "Comments look like /* || Base */. Put each heading above the rules it labels.",
      "BEM elements use two underscores: card__title. Modifiers use two hyphens: card--featured, alongside the block class.",
      "Keep class=\"card\" on both cards; the featured one gets class=\"card card--featured\".",
    ],
    checks: (() => {
      const pos = (css, re) => { const m = re.exec(css); return m ? m.index : -1; };
      return [
        { label: "The three section comments are in order", test: ({ code }) => { const c = code.css, a = c.indexOf("/* || Base */"), l = c.indexOf("/* || Layout */"), k = c.indexOf("/* || Components */"); return a >= 0 && a < l && l < k; } },
        { label: "Each rule is in the right section", test: ({ code }) => { const c = code.css, L = c.indexOf("/* || Layout */"), K = c.indexOf("/* || Components */"); const body = pos(c, /(^|\n)\s*body\s*\{/), a = pos(c, /(^|\n)\s*a\s*\{/), cont = pos(c, /\.container\s*\{/), card = pos(c, /\.card\s*\{/); return L > 0 && body >= 0 && body < L && a >= 0 && a < L && cont > L && cont < K && card > K; } },
        { label: "Titles use .card__title, not .card h3", test: ({ $$, code, style }) => $$("h3").every((h) => h.classList.contains("card__title")) && !/\.card\s+h3/.test(code.css) && style(".card__title", "color") === "rgb(11, 107, 94)" },
        { label: "The featured card uses the card--featured modifier", test: ({ $, code, style }) => !!$(".card.card--featured") && !/\bfeatured\b/.test(code.html.replace(/card--featured/g, "")) && !/\.card\.featured/.test(code.css) && style(".card--featured", "border-top-color") === "rgb(180, 65, 12)" },
      ];
    })(),
  });
'''
quiz = '''  makeQuiz(document.getElementById("quiz"), [
    { id: "q10", q: "Why do MDN's section comments use || ?", opts: ["CSS requires it", "It rarely appears elsewhere, so searching for it jumps between sections", "It makes the comment bold"], a: 1, why: "It's a searchable marker, nothing more." },
    { id: "q11", q: "In BEM, what is .card__title?", opts: ["A block", "An element of the card block", "A modifier"], a: 1, why: "Two underscores join an element to its block." },
    { id: "q12", q: "In BEM, what is .card--featured?", opts: ["A modifier: a variation of the card", "An element", "A new block"], a: 0, why: "Two hyphens mark a modifier, used alongside the block class." },
    { id: "q13", q: "Why avoid selectors like article.main p.box?", opts: ["They're invalid", "They only fit one place and are hard to override", "They're slower to type"], a: 1, why: "High specificity leads to longer and longer overrides." },
    { id: "q14", q: "What does a preprocessor like Sass do?", opts: ["Runs in the browser instead of CSS", "Compiles extra features, like partials, into plain CSS", "Checks accessibility"], a: 1, why: "Sass files are compiled into the CSS the browser loads." },
  ]);
'''
write("core-organizing-css.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + sortq + "\n" + quiz + "\n" + ex_o + "\n" + ex_b + "</script>\n")
