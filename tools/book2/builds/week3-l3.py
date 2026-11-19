import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("cascade"); sel = Src("selectors")
inh = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">Set on article', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Which rule wins?')
win = src.between('  <div class="rules" id="rules"></div>', '  <div class="section-title"><span class="eyebrow">Practice</span>')
calc = sel.between('  <div class="calc">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
calc = (calc.replace('id="ra"', 'id="sp-ra"').replace('id="rb"', 'id="sp-rb"').replace('for="a"', 'for="sp-a"').replace('for="b"', 'for="sp-b"')
  .replace('<input id="a"', '<input id="sp-a"').replace('<input id="b"', '<input id="sp-b"').replace('id="sa"', 'id="sp-sa"').replace('id="sb"', 'id="sp-sb"')
  .replace('<div class="verdict" aria-live="polite"><span class="sample" id="sample">', '<div class="sp-result" aria-live="polite"><span class="sample" id="sp-sample">').replace('<span id="verdict">', '<span id="sp-verdict">'))
scss = sel.css(); scss = scss[scss.index("  .calc {"):]
scss = scss.replace("  .verdict { margin-top", "  .sp-result { margin-top").replace("  .verdict .sample", "  .sp-result .sample")
extra = scss + """
  .ctl-demo { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 14px; display: grid; gap: 10px; }
  .ctl-demo .parent { color: firebrick; font: 1rem Georgia, serif; border: 2px dashed #e0a3a3; padding: 10px; border-radius: 6px; }
  .ctl-demo .parent a { font-weight: 700; }
  .ctl-demo blockquote { margin: 0; }
"""
h = head("The Cascade", src.css(), extra)
b = top("The Cascade", "Several rules often try to style the same element. CSS settles every argument the same way, with three ideas: the cascade, specificity and inheritance. Once you know them, \"why isn't my CSS working?\" usually answers itself.", [
  "Explain how source order, specificity and inheritance decide an element's final style.",
  "Work out a selector's specificity and predict which rule wins.",
  "Control inheritance with <code>inherit</code>, <code>initial</code>, <code>unset</code> and <code>revert</code>.",
  "Explain why inline styles and <code>!important</code> make CSS hard to maintain."])
b += ST("Read", "Conflicting rules") + prose("""
    <h3>Cascade</h3>
    <p>When two rules with equally strong selectors set the same property, the one that comes <em>later</em> wins:</p>
    <pre class="snippet" data-lang="css">h1 { color: red; }
h1 { color: blue; }  /* headings are blue */</pre>
    <h3>Specificity</h3>
    <p>But a more specific selector beats a less specific one, wherever it is. A class is more specific than an element name, so this heading is red even though the <code>h1</code> rule comes later:</p>
    <pre class="snippet" data-lang="css">.main-heading { color: red; }
h1 { color: blue; }</pre>
    <h3>Inheritance</h3>
    <p>Some values set on a parent are passed down to its children. Set <code>color: blue</code> on <code>body</code> and every paragraph and span inside turns blue, unless a rule targets them directly.</p>
    <h3>Understanding how the concepts work together</h3>
    <p>These three ideas together decide every property of every element. The rest of this lesson takes each in turn.</p>""")
b += ST("Read", "Understanding inheritance") + prose("""
    <p><span class="term">Inheritance</span> is why you can set a font once and have the whole page use it. Roughly: <strong>text properties inherit</strong> (<code>color</code>, <code>font-*</code>, <code>line-height</code>, <code>text-align</code>), and <strong>box properties don't</strong> (<code>border</code>, <code>padding</code>, <code>margin</code>, <code>width</code>, <code>background</code>). That's sensible: if a border on a <code>&lt;section&gt;</code> put a border on every paragraph inside it, nobody would use borders.</p>""")
b += ST("Play", "What gets inherited?", "Set a property on the article. The badges read what the browser actually computed for each child.") + inh
b += prose("""
    <h3>Controlling inheritance</h3>
    <p>Every property also accepts special values that control inheritance:</p>
    <ul>
      <li><code>inherit</code>: take the parent's value, even for a property that normally doesn't inherit.</li>
      <li><code>initial</code>: use the property's starting value from the CSS specification (for <code>color</code>, that's black).</li>
      <li><code>revert</code>: go back to the browser's default style for this element (for a link, blue).</li>
      <li><code>unset</code>: act like <code>inherit</code> for properties that inherit, and like <code>initial</code> for the rest.</li>
    </ul>""")
b += ST("Play", "Inheritance control values", "The paragraph is firebrick. Choose a value for the link's <code>color</code>.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="seg" id="ctl" role="group" aria-label="Value for the link's color">
        <button class="btn" type="button" data-v="">(no rule)</button>
        <button class="btn" type="button" data-v="inherit">inherit</button>
        <button class="btn" type="button" data-v="initial">initial</button>
        <button class="btn" type="button" data-v="revert">revert</button>
        <button class="btn" type="button" data-v="unset">unset</button>
      </div>
      <pre class="snippet" id="ctl-code"></pre>
      <p class="verdict" id="ctl-note" aria-live="polite"></p>
    </div>
    <div class="ctl-demo"><p class="parent" id="ctl-p">Read the <a href="#ctl" id="ctl-a">trail report</a> before you go.</p></div>
  </section>

"""
b += prose("""
    <h3>Resetting all property values</h3>
    <p>The shorthand <code>all</code> applies one of those values to (almost) every property at once. <code>blockquote { all: unset; }</code> wipes out every style on the element, so you can start it from scratch.</p>""")
b += ST("Practice", "Let it inherit", "This stylesheet sets the same font and colour three times. Set them once and let inheritance do the rest.") + '  <div id="ex-inherit"></div>\n\n'
b += ST("Read", "Understanding the cascade") + prose("""
    <p>When rules disagree about the same property on the same element, the browser checks three things, in order of importance:</p>
    <ol>
      <li><strong>Importance</strong>: is a declaration marked <code><span class="term">!important</span></code>?</li>
      <li><strong><span class="term">Specificity</span></strong>: which selector is more specific?</li>
      <li><strong><span class="term">Source order</span></strong>: which rule comes later?</li>
    </ol>
    <h3>Source order</h3>
    <p>If importance and specificity tie, later wins. That includes the order of your <code>&lt;link&gt;</code> tags: link a general stylesheet after a specific one, and the general one can win.</p>
    <h3>Specificity</h3>
    <p>The browser scores each selector in three columns:</p>
    <ul>
      <li><strong>IDs:</strong> each <code>#id</code> scores one in the first column.</li>
      <li><strong>Classes, attributes and pseudo-classes:</strong> each <code>.class</code>, <code>[attr]</code> or <code>:hover</code> scores one in the second.</li>
      <li><strong>Elements and pseudo-elements:</strong> each <code>h2</code> or <code>::before</code> scores one in the third.</li>
    </ul>
    <p>Scores are compared column by column, from left to right, so one ID outranks any number of classes, and one class outranks any number of elements. <code>*</code> and combinators score nothing.</p>""")
b += ST("Play", "Score two selectors", "Both rules color the same heading. Type selectors to compare their scores.") + calc
b += prose("""
    <h3>Inline styles</h3>
    <p>A <code>style=""</code> attribute beats every selector in every stylesheet. That's one reason to avoid inline styles: the only way to override them is <code>!important</code>.</p>
    <h3>!important</h3>
    <p>Adding <code>!important</code> to a declaration makes it beat every normal declaration, whatever the specificity. It's tempting as a quick fix, but the next time you need to change that property, only another <code>!important</code> will do, and soon nobody can tell which rule wins. Fix the specificity instead.</p>""")
b += ST("Play", "Which rule wins?", "Three rules try to colour the same heading, <code>&lt;h3 class=\"title\" id=\"top\"&gt;</code>. Change the selectors, reorder the rules, or add <code>!important</code>.") + win
b += ST("Practice", "Win without !important", "Someone forced a rule to win. Undo it properly.") + '  <div id="ex-important"></div>\n\n'
b += ST("Read", "The effect of CSS location") + prose("""
    <p>Your stylesheets aren't the only ones. The browser has its default (user-agent) stylesheet, and users can add their own, for example to force larger text. They're layered in this order, each overriding the ones before:</p>
    <ol>
      <li>Browser defaults</li>
      <li>User styles</li>
      <li>Your styles (the author)</li>
      <li>Your <code>!important</code> styles</li>
      <li>User <code>!important</code> styles</li>
      <li>Browser <code>!important</code> styles</li>
    </ol>
    <p>Notice the flip: for <code>!important</code>, the user beats the author. That's deliberate, so people who need large text or high contrast always get it.</p>""")
b += notes([
  "Later rules beat earlier ones, but only when specificity ties.",
  "Specificity: IDs, then classes/attributes/pseudo-classes, then elements. Compare column by column.",
  "Text properties inherit; box properties don't.",
  "<code>inherit</code>, <code>initial</code>, <code>revert</code> and <code>unset</code> control inheritance for any property.",
  "Inline styles beat selectors, and <code>!important</code> beats both. Avoid them.",
], [
  "Fighting specificity with <code>!important</code> instead of a better selector.",
  "Expecting a border or padding on a parent to apply to its children.",
  "Linking stylesheets in the wrong order, so a general file overrides a specific one.",
  "Styling with IDs, which makes later overrides need even stronger selectors.",
  "Forgetting that buttons and inputs don't inherit the page's font.",
])
first = src.first_script()
sfirst = sel.first_script(); sjs = sfirst[sfirst.index("  // Specificity:"):]
sjs = sjs.replace("function specificity(sel)", "function spScore(sel)").replace("specificity(A)", "spScore(A)").replace("specificity(B)", "spScore(B)").replace("function compare()", "function spCompare()").replace("compare();", "spCompare();")
sjs = sjs.replace('$("a")', '$("sp-a")').replace('$("b")', '$("sp-b")').replace('$("sa")', '$("sp-sa")').replace('$("sb")', '$("sp-sb")').replace('$("ra")', '$("sp-ra")').replace('$("rb")', '$("sp-rb")').replace('$("sample")', '$("sp-sample")').replace('$("verdict")', '$("sp-verdict")').replace("addEventListener(\"input\", compare)", "addEventListener(\"input\", spCompare)")
sjs = sjs.replace("const valid =", "const spValid =").replace("valid(A)", "spValid(A)").replace("valid(B)", "spValid(B)")
js = r'''
  // --- Inheritance control values ---
  const CTL = {
    "": "No rule targets the link, so the browser's default link style applies: blue (or purple once visited).",
    inherit: "inherit takes the parent's value: firebrick, like the rest of the paragraph.",
    initial: "initial uses color's starting value from the specification: black. Not the browser's link blue.",
    revert: "revert goes back to the browser's default for a link: blue.",
    unset: "color normally inherits, so unset acts like inherit: firebrick.",
  };
  function ctl(v) {
    const a = $("ctl-a");
    a.style.color = v;
    $("ctl-code").textContent = v ? `.parent a {\n  color: ${v};\n}` : "/* no rule for the link */";
    $("ctl-note").textContent = CTL[v] + ` (computed: ${getComputedStyle(a).color})`;
    document.querySelectorAll("#ctl .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.v === v)));
  }
  $("ctl").addEventListener("click", (e) => { const b = e.target.closest("[data-v]"); if (b) ctl(b.dataset.v); });
  $("ctl-a").addEventListener("click", (e) => e.preventDefault());
  ctl("inherit");

'''
ex_inh = src.block('  makeExercise(document.getElementById("ex-inherit"), {')
ex_imp = r'''  makeExercise(document.getElementById("ex-important"), {
    title: "The red alert",
    task: `<p>The alert paragraph should be red, but <code>#news p</code> is more specific than <code>.alert</code>, so someone added <code>!important</code>.</p>
    <ol>
      <li>Delete <code>!important</code>.</li>
      <li>Change the <code>.alert</code> selector so it's more specific than <code>#news p</code>, while still matching only the alert.</li>
    </ol>`,
    html: `<section id="news">
  <p>Mesa Trail reopens on Saturday.</p>
  <p class="alert">Royal Arch is closed for repairs.</p>
</section>`,
    css: `body { font-family: system-ui, sans-serif; }

#news p {
  color: gray;
}

.alert {
  color: red !important;
}`,
    solution: { css: `body { font-family: system-ui, sans-serif; }

#news p {
  color: gray;
}

#news .alert {
  color: red;
}` },
    hints: ["#news p scores 1-0-1. You need at least an ID and a class: 1-1-0.", "#news .alert, or #news p.alert, both work."],
    checks: [
      { label: "No !important anywhere", test: ({ code }) => !/!\s*important/i.test(code.css) },
      { label: "The alert is red", test: ({ style }) => style(".alert", "color") === "rgb(255, 0, 0)" },
      { label: "The other paragraph is still gray", test: ({ style }) => style("p:not(.alert)", "color") === "rgb(128, 128, 128)" },
    ],
  });
'''
quiz = r'''  makeQuiz(document.getElementById("quiz"), [
    { id: "q1", q: "Two rules, both h1, set different colours. Which wins?", opts: ["The later one", "The first one", "Neither"], a: 0, why: "Equal specificity, so source order decides." },
    { id: "q2", q: "Which selector is most specific?", opts: ["#main p", ".card .title .tag", "article section div p"], a: 0, why: "1-0-1 beats 0-3-0: one ID outranks any number of classes." },
    { id: "q3", q: "You put a border on a <section>. Do the paragraphs inside get borders?", opts: ["No, border doesn't inherit", "Yes", "Only the first one"], a: 0, why: "Box properties don't inherit." },
    { id: "q4", q: "a { color: inherit; } makes links…", opts: ["the same colour as their parent text", "black", "blue"], a: 0, why: "inherit takes the parent's value." },
    { id: "q5", q: "Why avoid !important as a fix?", opts: ["Only another !important can override it later", "Browsers ignore it", "It slows the page"], a: 0, why: "It short-circuits specificity, so overrides escalate." },
    { id: "q6", q: "What does an inline style=\"\" attribute beat?", opts: ["Every selector in every stylesheet", "Only element selectors", "Nothing"], a: 0, why: "Inline styles beat all normal selectors; only !important beats them." },
  ]);
'''
write("core-cascade.html", h, b, "\n<script>" + first + sjs.rstrip() + "\n" + js + "</script>\n<script>\n" + ex_inh + "\n" + ex_imp + "\n" + quiz + "</script>\n")
