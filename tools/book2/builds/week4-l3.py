import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("css-variables")
pg = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">Variables on #site', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("CSS Custom Properties", src.css(), """
  @property --box-color-reg { syntax: "<color>"; inherits: false; initial-value: #9aa2bf; }
  .nest { display: grid; gap: 0; }
  .nest div { border: 2px solid #1d2133; padding: 10px 10px 10px 14px; border-radius: 6px; color: #1d2133; font: 600 0.85rem var(--font-code); font-variation-settings: "MONO" 1; }
  .nest.plain div { background: var(--box-color, #fff); }
  .nest.reg div { background: var(--box-color-reg); }
  .fb-out { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
  .fb-out li { display: grid; grid-template-columns: 1fr auto; gap: 10px; align-items: center; padding: 8px 10px; border-radius: 6px; background: var(--stage); font: 0.86rem var(--font-code); font-variation-settings: "MONO" 1; }
  .fb-out .sw { width: 60px; height: 26px; border-radius: 4px; border: 1px solid var(--line); }
""")
b = top("CSS Custom Properties", "Type a colour forty times and changing it means forty edits. A custom property (often called a CSS variable) stores a value once, under a name, so every rule that uses it updates together.", [
  "Declare custom properties with <code>--name</code> and use them with <code>var()</code>.",
  "Define global values on <code>:root</code>, and override them for one part of the page.",
  "Give <code>var()</code> a fallback, and explain what happens with an invalid value.",
  "Register a typed property with <code>@property</code>, and read or set values from JavaScript."])
b += ST("Read", "Declaring custom properties") + prose("""
    <h3>Using a prefix of two dashes (<code>--</code>)</h3>
    <p>A <span class="term">CSS variable</span> is a property whose name starts with two dashes. You declare it in a rule, like any other property:</p>
    <pre class="snippet" data-lang="css">section {
  --main-bg-color: brown;
}</pre>
    <p>Names are case-sensitive: <code>--Brand</code> and <code>--brand</code> are different.</p>
    <h3>Using the <code>@property</code> at-rule</h3>
    <p>For more control, <code>@property</code> registers a custom property with a type, whether it inherits, and a starting value. More on that below.</p>
    <h3>Referencing custom properties with <code>var()</code></h3>
    <p>To use the value, put its name in <code>var()</code>: <code>background-color: var(--main-bg-color);</code>. Writing <code>color: --brand;</code> does nothing: you always need <code>var()</code>.</p>""")
b += ST("Read", "First steps, and the :root pseudo-class") + prose("""
    <p>The usual pattern is to declare site-wide values once, on <code>:root</code> (the <code>&lt;html&gt;</code> element), so every element can use them:</p>
    <pre class="snippet" data-lang="css">:root {
  --brand: #0b6b5e;
  --space: 16px;
}
.btn {
  background: var(--brand);
  padding: var(--space);
}</pre>
    <p>Change <code>--brand</code> in one place and every button, link and heading that uses it follows. The same trick gives you a dark theme: redefine just the colour variables inside <code>@media (prefers-color-scheme: dark)</code>.</p>""")
b += ST("Play", "Change a variable", "Change one variable and watch every part of the site that uses it update. Then try the dark theme and the override.") + pg
b += ST("Practice", "Use a variable", "One brand colour is typed three times. Store it once, then make a sale card that changes it.") + '  <div id="ex-vars"></div>\n\n'
b += ST("Read", "Inheritance of custom properties") + prose("""
    <p>Custom properties inherit, like <code>color</code>. An element sees the value set on itself or on its nearest ancestor. That's what makes overrides work: set <code>--brand</code> on one <code>.card</code>, and that card and everything inside it use the new value, while the rest of the page doesn't change.</p>
    <h3>Using <code>@property</code> to control inheritance</h3>
    <p>A registered property can switch inheritance off. Then only the element it's set on gets the value; its children get the <code>initial-value</code>:</p>
    <pre class="snippet" data-lang="css">@property --box-color {
  syntax: "&lt;color&gt;";
  inherits: false;
  initial-value: #9aa2bf;
}</pre>""")
b += ST("Play", "Who sees the value?", "Four nested boxes, each with <code>background: var(--box-color)</code>. Set the variable on one of them.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="seg" id="nest-on" role="group" aria-label="Set --box-color on">
        <button class="btn" type="button" data-v="0">box 1</button><button class="btn" type="button" data-v="1">box 2</button><button class="btn" type="button" data-v="2">box 3</button>
      </div>
      <label class="toggle"><input type="checkbox" id="nest-reg"> registered with <code>@property</code>, <code>inherits: false</code></label>
      <p class="verdict" id="nest-note" aria-live="polite"></p>
    </div>
    <div class="nest plain" id="nest"><div>box 1<div>box 2<div>box 3<div>box 4</div></div></div></div></div>
  </section>

"""
b += ST("Read", "Custom property fallback values") + prose("""
    <h3>Defining fallbacks in the <code>var()</code> function</h3>
    <p>Add a second value to <code>var()</code>, after a comma, to use when the variable isn't defined: <code>var(--sale, crimson)</code>. Fallbacks can nest: <code>var(--my-var, var(--my-background, pink))</code>.</p>
    <h3>Fallbacks using the <code>@property</code> initial value</h3>
    <p>A registered property also falls back to its <code>initial-value</code> when it's given a value of the wrong type, like <code>peenk</code> for a <code>&lt;color&gt;</code>.</p>""")
b += ST("Read", "Invalid custom properties") + prose("""
    <p>Normally an invalid declaration is simply skipped. Variables are different: the browser can't know whether <code>var(--text-color)</code> makes sense until it substitutes the value. So with <code>:root { --text-color: 16px; }</code>, the rule <code>p { color: var(--text-color); }</code> isn't skipped. It becomes invalid when used, and <code>color</code> falls back to its inherited value, not to your previous rule. (Registering the property with a <code>&lt;color&gt;</code> syntax prevents that.)</p>""")
b += ST("Play", "What does var() resolve to?", "Choose what <code>--my-var</code> is set to.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="seg" id="fb" role="group" aria-label="--my-var">
        <button class="btn" type="button" data-v="">not defined</button>
        <button class="btn" type="button" data-v="#2340d9">#2340d9</button>
        <button class="btn" type="button" data-v="16px">16px</button>
      </div>
      <p class="hint">The parent's text colour is <code>#b4410c</code>.</p>
    </div>
    <div class="panel"><ul class="fb-out" id="fb-out"></ul></div>
  </section>

"""
b += ST("Practice", "Register a property", "Use <code>@property</code> to make a colour variable safe.") + '  <div id="ex-prop"></div>\n\n'
b += ST("Read", "Values in JavaScript") + prose("""
    <p>JavaScript (Week 7) can read and change custom properties, which is how interactive themes work. Changing one variable restyles everything that uses it:</p>
    <pre class="snippet" data-lang="js">// read
getComputedStyle(element).getPropertyValue("--brand");
// set
element.style.setProperty("--brand", "#b4410c");</pre>""")
b += ST("Play", "Set a variable from JavaScript", "Each button runs <code>document.documentElement.style.setProperty(\"--demo-hue\", …)</code>. Everything below uses <code>hsl(var(--demo-hue) 70% 40%)</code>.") + """  <section class="playground even">
    <div class="panel" style="display:grid;gap:10px;align-content:start">
      <div class="presets" id="js-hue" role="group" aria-label="Hue"><button class="btn" type="button">20</button><button class="btn" type="button">160</button><button class="btn" type="button">225</button><button class="btn" type="button">300</button></div>
      <pre class="snippet" id="js-read"></pre>
    </div>
    <div class="panel" id="js-demo" style="display:grid;gap:8px"><b style="color:hsl(var(--demo-hue, 225) 70% 40%);font-size:1.4rem">Trail Club</b><span style="background:hsl(var(--demo-hue, 225) 70% 40%);color:#fff;padding:8px 12px;border-radius:6px;justify-self:start">Join a hike</span><span style="border-left:6px solid hsl(var(--demo-hue, 225) 70% 40%);padding-left:10px">Next: Saturday at 8am</span></div>
  </section>

"""
b += notes([
  "Custom properties start with <code>--</code> and are read with <code>var()</code>.",
  "Declare global values on <code>:root</code>; override them on any element for that part of the page.",
  "They inherit, unless registered with <code>@property</code> and <code>inherits: false</code>.",
  "<code>var(--x, fallback)</code> covers an undefined variable.",
  "A wrong-type value isn't skipped: the property falls back to inherited or initial.",
], [
  "<code>color: --brand;</code> without <code>var()</code>.",
  "Mismatched case: <code>--Brand</code> versus <code>--brand</code>.",
  "Declaring a variable on one element and expecting a sibling to see it.",
  "A space after <code>var(</code> in the name, or a missing <code>--</code>.",
  "Expecting a bad value in a variable to be ignored like a normal invalid declaration.",
])
first = src.first_script()
js = r'''
  // --- Nested inheritance ---
  let nestOn = 1;
  function nest() {
    const reg = $("nest-reg").checked, boxes = [...$("nest").querySelectorAll("div")];
    $("nest").className = "nest " + (reg ? "reg" : "plain");
    boxes.forEach((d, i) => { d.style.removeProperty("--box-color"); d.style.removeProperty("--box-color-reg"); });
    boxes[nestOn].style.setProperty(reg ? "--box-color-reg" : "--box-color", "#f0b37a");
    $("nest-note").textContent = reg ? `Only box ${nestOn + 1} is orange: with inherits: false, its children get the initial value (grey).` : `Box ${nestOn + 1} and everything inside it are orange: custom properties inherit. Boxes above it don't see the value.`;
    document.querySelectorAll("#nest-on .btn").forEach((x) => x.setAttribute("aria-pressed", String(+x.dataset.v === nestOn)));
  }
  $("nest-on").addEventListener("click", (e) => { const b = e.target.closest("[data-v]"); if (b) { nestOn = +b.dataset.v; nest(); } });
  $("nest-reg").addEventListener("change", nest);
  nest();

  // --- Fallbacks ---
  const FB = ["var(--my-var)", "var(--my-var, crimson)", "var(--my-var, var(--other, pink))"];
  function fb(v) {
    const host = document.createElement("div"); host.style.color = "#b4410c"; document.body.append(host);
    if (v) host.style.setProperty("--my-var", v);
    $("fb-out").innerHTML = FB.map((expr) => {
      const p = document.createElement("p"); p.style.color = expr; host.append(p);
      const c = getComputedStyle(p).color; p.remove();
      return `<li><span>color: ${expr}</span><span class="sw" style="background:${c}" title="${c}"></span></li>`;
    }).join("") + `<li><span>${v === "16px" ? "16px isn't a colour: every rule became invalid at computed time and inherited #b4410c from the parent, even the ones with a fallback (fallbacks only cover undefined)." : v ? "Defined, so every var() uses it and the fallbacks are ignored." : "Not defined: the plain var() inherits the parent's colour; the others use their fallbacks."}</span><span></span></li>`;
    host.remove();
    document.querySelectorAll("#fb .btn").forEach((x) => x.setAttribute("aria-pressed", String(x.dataset.v === v)));
  }
  $("fb").addEventListener("click", (e) => { const b = e.target.closest("[data-v]"); if (b) fb(b.dataset.v); });
  fb("");

  // --- JavaScript ---
  function hue(v) {
    $("js-demo").style.setProperty("--demo-hue", v);
    $("js-read").textContent = `el.style.setProperty("--demo-hue", "${v}");\ngetComputedStyle(el).getPropertyValue("--demo-hue");\n// → "${getComputedStyle($("js-demo")).getPropertyValue("--demo-hue").trim()}"`;
  }
  $("js-hue").addEventListener("click", (e) => { const b = e.target.closest(".btn"); if (b) hue(b.textContent); });
  hue("225");
'''
ex_v = src.block('  makeExercise(document.getElementById("ex-vars"), {')
ex_p = r'''  makeExercise(document.getElementById("ex-prop"), {
    title: "A typed accent colour",
    task: `<ol>
      <li>Register <code>--accent</code> with <code>@property</code>: <code>syntax: "&lt;color&gt;"</code>, <code>inherits: true</code>, <code>initial-value: teal</code>.</li>
      <li>Give <code>.badge</code> <code>background-color: var(--accent)</code>.</li>
      <li>Someone set <code>--accent: peenk</code> on the warning badge. Leave it: with the property registered, that badge falls back to teal instead of breaking.</li>
      <li>Set <code>--accent: #b4410c</code> on <code>.badge.hot</code>.</li>
    </ol>`,
    html: `<span class="badge">Open</span>
<span class="badge warn">Icy</span>
<span class="badge hot">Busy</span>`,
    css: `body { font-family: system-ui, sans-serif; }
.badge { color: white; padding: 4px 10px; border-radius: 99px; }
.badge.warn { --accent: peenk; }
`,
    solution: { css: `@property --accent {
  syntax: "<color>";
  inherits: true;
  initial-value: teal;
}

body { font-family: system-ui, sans-serif; }
.badge { color: white; padding: 4px 10px; border-radius: 99px; background-color: var(--accent); }
.badge.warn { --accent: peenk; }
.badge.hot { --accent: #b4410c; }
` },
    hints: ["@property goes at the top level, like @media, with syntax, inherits and initial-value inside.", "Quote the syntax: \"<color>\"."],
    checks: [
      { label: "The plain badge is teal", test: ({ style }) => style(".badge:not(.warn):not(.hot)", "background-color") === "rgb(0, 128, 128)" },
      { label: "The warning badge falls back to teal", test: ({ style }) => style(".badge.warn", "background-color") === "rgb(0, 128, 128)" },
      { label: "The hot badge is #b4410c", test: ({ style }) => style(".badge.hot", "background-color") === "rgb(180, 65, 12)" },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "What does inherits: false in @property do?", opts: ["Children get the initial-value, not the parent's value", "The property can't be changed", "It stops var() working"], a: 0, why: "Only the element the value is set on uses it." },
    { id: "q6", q: "In JavaScript, how do you change --brand on an element?", opts: ["el.style.setProperty(\\"--brand\\", \\"red\\")", "el.style.brand = \\"red\\"", "el.brand = \\"red\\""], a: 0, why: "Custom properties are set with setProperty and read with getPropertyValue." },
  ]);
''')
write("core-custom-properties.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_v + "\n" + ex_p + "\n" + quiz + "</script>\n")
