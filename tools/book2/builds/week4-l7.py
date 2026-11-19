import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("transitions")
note = src.between('  <p class="motion-note" id="motion-note" hidden>', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Transitions</h2>')
tr = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="kind">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Keyframe')
kf = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="name">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Transitions", src.css(), """
  .can-list { display: grid; gap: 10px; }
  .can-row { display: grid; grid-template-columns: 11em 1fr auto; gap: 12px; align-items: center; }
  .can-row code { font-size: 0.85rem; }
  .can-track { height: 54px; background: var(--stage); border-radius: 8px; display: flex; align-items: center; padding: 0 8px; overflow: hidden; }
  .can-box { width: 70px; height: 38px; border-radius: 6px; background: #2340d9; color: #fff; display: grid; place-items: center; padding: 0 8px; font: 700 0.9rem system-ui, sans-serif; white-space: nowrap; transition: all 0.8s ease; }
  .sd-panel { margin-top: 10px; padding: 14px; border-radius: 8px; background: #0b6b5e; color: #fff; transition: opacity 0.6s, translate 0.6s, display 0.6s allow-discrete; opacity: 0; translate: 0 -12px; display: none; }
  .sd-panel.showing { opacity: 1; translate: 0 0; display: block; }
  @starting-style { .sd-panel.showing { opacity: 0; translate: 0 -12px; } }
  .ev-track { position: relative; height: 70px; background: var(--stage); border-radius: 8px; cursor: pointer; }
  .ev-ball { position: absolute; top: 15px; left: 10px; width: 40px; height: 40px; border-radius: 50%; background: #b4410c; transition: transform 1s ease-in-out; }
  .ev-log { margin: 0; padding: 10px 12px; background: var(--stage); border-radius: 8px; font: 0.85rem/1.6 var(--font-code); font-variation-settings: "MONO" 1; min-height: 110px; white-space: pre-wrap; }
""")
b = top("Transitions", "By default a style change is instant: hover a button and its colour snaps. A transition tells the browser to blend from the old value to the new one over time, so the change feels smooth instead of abrupt.", [
  "Write transitions with <code>transition</code> and its four longhand properties.",
  "Know which properties can be transitioned, and which animate smoothly.",
  "Transition several properties, a menu, and even <code>display</code>.",
  "Respect visitors who ask for reduced motion, and react to transition events in JavaScript."])
b += ST("Read", "Which CSS properties can be transitioned?") + prose("""
    <p>A transition works by calculating the in-between values, so the property needs values that <em>have</em> an in-between: colours, lengths, numbers, transforms, opacity. Properties with on/off values, like <code>display</code> or <code>font-family</code>, just switch. And <code>auto</code> can't be transitioned: <code>height: 0</code> to <code>height: auto</code> jumps.</p>""")
b += ST("Play", "Does it animate?", "Each box has <code>transition: all 0.8s</code>. Toggle each property.") + """  <div class="panel can-list" id="can"></div>

"""
b += ST("Read", "Defining transitions") + prose("""
    <p>The <span class="term">transition</span> shorthand takes the property, the duration, a timing function and a delay:</p>
    <pre class="snippet" data-lang="css">.btn {
  background: #0b6b5e;
  transition: background-color 200ms ease, transform 200ms ease;
}
.btn:hover {
  background: #084c43;
  transform: translateY(-2px);
}</pre>
    <ul>
      <li><code>transition-property</code>: which properties to animate. Name them, rather than <code>all</code>, so nothing unexpected moves.</li>
      <li><code>transition-duration</code>: how long, in <code>s</code> or <code>ms</code>. About 150 to 400ms feels right for interface changes.</li>
      <li><code>transition-timing-function</code>: the speed curve, like <code>ease</code>, <code>linear</code>, <code>ease-out</code>.</li>
      <li><code>transition-delay</code>: how long to wait before starting.</li>
    </ul>
    <p>Put the transition on the element's normal state, not on <code>:hover</code>, so it animates on the way in <em>and</em> the way out.</p>""")
b += note
b += ST("Play", "Transitions", "Change the duration, curve and delay, then change state.") + tr
b += ST("Read", "Examples") + prose("""
    <h3>Multiple animated properties</h3>
    <p>List several transitions with commas: <code>transition: width 2s, height 2s, background-color 2s, rotate 2s;</code>.</p>
    <h3>When property value lists are of different lengths</h3>
    <p>With the longhands, the lists are matched up by position. If <code>transition-duration</code> has fewer values than <code>transition-property</code>, its values repeat to fill the gap; extra values are ignored.</p>
    <pre class="snippet" data-lang="css">transition-property: opacity, left, top, height;
transition-duration: 3s, 5s;   /* = 3s, 5s, 3s, 5s */</pre>
    <h3>Using transitions when highlighting menus</h3>
    <p>A short transition on menu links, <code>transition: background-color 0.3s ease-out, color 0.3s ease-out;</code>, makes hover and focus states feel smooth.</p>
    <h3>Transitioning display</h3>
    <p>Normally an element switching from <code>display: none</code> to <code>display: block</code> can't fade in: it doesn't exist until the switch. Two newer features fix that. <code>allow-discrete</code> lets <code>display</code> take part in the transition, and <code>@starting-style</code> says what the element looks like the moment it appears, so it has something to transition <em>from</em>:</p>
    <pre class="snippet" data-lang="css">.panel {
  opacity: 0;
  display: none;
  transition: opacity 0.6s, display 0.6s allow-discrete;
}
.panel.showing {
  opacity: 1;
  display: block;
}
@starting-style {
  .panel.showing { opacity: 0; }
}</pre>""")
b += ST("Play", "Fade in from display: none", "This uses <code>@starting-style</code> and <code>allow-discrete</code>, in browsers that support them.") + """  <div class="panel"><button class="btn" type="button" id="sd-btn" aria-expanded="false">Show trail alert</button><div class="sd-panel" id="sd-panel">Royal Arch is closed above the switchbacks after today's rockfall.</div></div>

"""
b += ST("Practice", "Smooth menu links", "Add transitions to a navigation menu.") + '  <div id="ex-menu"></div>\n\n'
b += ST("Read", "Keyframe animations and reduced motion") + prose("""
    <p>A transition needs a trigger, like a hover or a class change. An <span class="term">animation</span> runs by itself, through steps you describe with <code>@keyframes</code>:</p>
    <pre class="snippet" data-lang="css">@keyframes pulse {
  from { transform: scale(1); }
  to   { transform: scale(1.08); }
}
.new-badge {
  animation: pulse 800ms ease-in-out infinite alternate;
}</pre>
    <p>Some people get dizzy or sick from motion on screen, and set their device to reduce it. Wrap big or looping motion in <code>@media (prefers-reduced-motion: no-preference) { … }</code>, so it only runs for people who haven't asked for less.</p>""")
b += ST("Play", "Keyframe animations") + kf
b += ST("Practice", "Add motion carefully", "Smooth a hover, add a pulse, and respect visitors who've asked for less motion.") + '  <div id="ex-motion"></div>\n\n'
b += ST("Read", "JavaScript examples") + prose("""
    <h3>Using transitions to make JavaScript functionality smooth</h3>
    <p>When JavaScript changes a style, a transition in the CSS animates it, with no animation code in your script. Set <code>transition: transform 1s</code> on a ball, and every time JavaScript sets a new <code>transform</code>, the ball glides there.</p>
    <h3>Detecting the start and completion of a transition</h3>
    <p>Transitions fire events you can listen for: <code>transitionrun</code> (it's set up), <code>transitionstart</code> (after any delay), and <code>transitionend</code> (finished). Each tells you the <code>propertyName</code> and the <code>elapsedTime</code>.</p>""")
b += ST("Play", "Click to move the ball", "JavaScript sets the transform; the CSS transition animates it. The log shows the events.") + """  <section class="playground even">
    <div class="ev-track" id="ev-track" role="button" tabindex="0" aria-label="Move the ball"><div class="ev-ball" id="ev-ball"></div></div>
    <pre class="ev-log" id="ev-log" aria-live="polite">Click the track.</pre>
  </section>

"""
b += notes([
  "Transitions blend between two states; animations run through keyframes on their own.",
  "Only properties with in-between values animate; <code>auto</code> and <code>display</code> normally snap.",
  "Put <code>transition</code> on the normal state, name the properties, and keep it to 150–400ms.",
  "<code>transform</code> and <code>opacity</code> animate most smoothly.",
  "Respect <code>prefers-reduced-motion</code>.",
], [
  "<code>transition</code> only on <code>:hover</code>, so it snaps back.",
  "<code>transition: all</code>, which animates things you didn't mean to.",
  "Trying to transition <code>height</code> to <code>auto</code>.",
  "Slow, bouncy motion on every interaction.",
  "Looping animations with no reduced-motion fallback.",
])
first = src.first_script()
js = r'''
  // --- Does it animate? ---
  const CAN = [
    ["background-color", (b, on) => (b.style.backgroundColor = on ? "#b4410c" : ""), "✓ animates: colours have in-between values"],
    ["margin-left", (b, on) => (b.style.marginLeft = on ? "220px" : "0px"), "✓ animates, but makes the browser redo the layout every frame"],
    ["transform", (b, on) => (b.style.transform = on ? "translateX(220px) rotate(20deg)" : ""), "✓ animates smoothly"],
    ["width → auto", (b, on) => (b.style.width = on ? "auto" : ""), "✗ snaps to the text's width: auto has no in-between"],
    ["font-family", (b, on) => (b.style.fontFamily = on ? "Georgia, serif" : ""), "✗ snaps: there's no halfway font"],
  ];
  $("can").innerHTML = CAN.map(([p], i) => `<div class="can-row"><code>${p}</code><div class="can-track"><div class="can-box" id="can-${i}">Aa</div></div><button class="btn" type="button" data-i="${i}" aria-pressed="false">Toggle</button></div><p class="hint" id="can-note-${i}" style="margin:-6px 0 0"></p>`).join("");
  $("can").addEventListener("click", (e) => {
    const b = e.target.closest("[data-i]"); if (!b) return;
    const i = +b.dataset.i, on = b.getAttribute("aria-pressed") !== "true";
    b.setAttribute("aria-pressed", String(on)); CAN[i][1]($("can-" + i), on); $("can-note-" + i).textContent = CAN[i][2];
  });

  // --- display transition ---
  $("sd-btn").addEventListener("click", () => {
    const on = !$("sd-panel").classList.contains("showing");
    $("sd-panel").classList.toggle("showing", on); $("sd-btn").setAttribute("aria-expanded", String(on));
    $("sd-btn").textContent = on ? "Hide trail alert" : "Show trail alert";
  });

  // --- Transition events ---
  let evX = 0, evT0 = 0;
  const evLog = (s) => { $("ev-log").textContent += "\n" + s; };
  function evMove(x) {
    const w = $("ev-track").clientWidth - 60;
    evX = Math.max(0, Math.min(w, x)); evT0 = performance.now();
    $("ev-log").textContent = `ball.style.transform = "translateX(${Math.round(evX)}px)"`;
    $("ev-ball").style.transform = `translateX(${evX}px)`;
  }
  $("ev-track").addEventListener("click", (e) => evMove(e.clientX - $("ev-track").getBoundingClientRect().left - 30));
  $("ev-track").addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); evMove(evX > 100 ? 0 : 1000); } });
  ["transitionrun", "transitionstart", "transitionend"].forEach((t) => $("ev-ball").addEventListener(t, (e) => evLog(`${t}: ${e.propertyName}, elapsedTime ${e.elapsedTime}s`)));
'''
ex_m = src.block('  makeExercise(document.getElementById("ex-motion"), {')
ex_menu = r'''  makeExercise(document.getElementById("ex-menu"), {
    title: "Menu highlights",
    task: `<ol>
      <li>Give <code>nav a</code> a transition of <code>background-color 0.3s ease-out</code> <em>and</em> <code>color 0.3s ease-out</code>, on the normal state.</li>
      <li>Add one rule for <code>nav a:hover</code> and <code>nav a:focus-visible</code>: <code>background-color: #0b6b5e</code> and <code>color: white</code>.</li>
    </ol>
    <p>Then hover over the links to see them fade.</p>`,
    html: `<nav>
  <a href="#">Trails</a>
  <a href="#">Events</a>
  <a href="#">Join</a>
</nav>`,
    css: `body { font-family: system-ui, sans-serif; }
nav a { display: inline-block; padding: 10px 16px; color: #0b6b5e; text-decoration: none; border-radius: 6px; }
`,
    solution: { css: `body { font-family: system-ui, sans-serif; }
nav a { display: inline-block; padding: 10px 16px; color: #0b6b5e; text-decoration: none; border-radius: 6px; transition: background-color 0.3s ease-out, color 0.3s ease-out; }
nav a:hover,
nav a:focus-visible { background-color: #0b6b5e; color: white; }
` },
    hints: ["Separate the two transitions with a comma.", "The transition goes on nav a, not on :hover."],
    checks: [
      { label: "Links transition background-color and color", test: ({ style }) => { const p = style("nav a", "transition-property").split(", "); return p.includes("background-color") && p.includes("color"); } },
      { label: "Both take 0.3s, ease-out", test: ({ style }) => style("nav a", "transition-duration").split(", ").every((d) => d === "0.3s") && style("nav a", "transition-timing-function").split(", ").every((t) => t === "ease-out") },
      { label: "A hover + focus-visible rule sets the colours", test: ({ doc }) => [...doc.styleSheets[0].cssRules].some((r) => /:hover/.test(r.selectorText || "") && /:focus-visible/.test(r.selectorText || "") && r.style.backgroundColor === "rgb(11, 107, 94)" && r.style.color === "white") },
    ],
  });
'''
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Why does height: 0 to height: auto snap instead of animating?", opts: ["auto has no in-between value to calculate", "height can't be transitioned", "The duration is too short"], a: 0, why: "The browser can't interpolate to auto." },
    { id: "q6", q: "Which event fires when a transition finishes?", opts: ["transitionend", "transitiondone", "animationend"], a: 0, why: "transitionend fires once per finished property." },
  ]);
''')
write("core-transitions.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + ex_menu + "\n" + ex_m + "\n" + quiz + "</script>\n")
