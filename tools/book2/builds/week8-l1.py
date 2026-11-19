import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-loops")
pg_step = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="mode">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>map() and filter()')
pg_mf = src.between('  <section class="playground">\n    <div class="panel controls"><div class="seg" id="arrm"', '  <div class="section-title"><span class="eyebrow">Try it</span>')
brk = src.between('  <div class="runner"><textarea aria-label="Code editor">const trails = ["Mesa", "Royal Arch", "Flagstaff", "Chautauqua", "Bear Peak"];', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Loops", src.css(), """
  .cv-wrap { display: grid; gap: 8px; }
  .cv-wrap canvas { width: 100%; max-width: 520px; height: auto; aspect-ratio: 520 / 260; background: #fff; border: 1px solid var(--line); border-radius: 8px; }
""")
b = top("Loops", "Computers are good at doing the same thing over and over. A loop runs a block of code again and again: once for every item in a list, a set number of times, or until something changes.", [
  "Loop through an array with <code>for...of</code>, and transform or filter it with <code>map()</code> and <code>filter()</code>.",
  "Count with a standard <code>for</code> loop, and use the index.",
  "Leave a loop early with <code>break</code>, and skip an item with <code>continue</code>.",
  "Use <code>while</code> and <code>do...while</code>, and pick the right loop for the job.",
])
b += ST("Read", "Why are loops useful?") + prose("""
    <p>Say you have a list of 50 trails and want to show each name. You could write <code>console.log()</code> 50 times, or write it once and let a <span class="term">loop</span> repeat it. Loops are how programs work through lists: every product in a shop, every photo in a gallery, every guess in a game.</p>
    <h3>Looping code example</h3>
    <p>MDN's example draws 100 random circles on a canvas. The drawing code is written once, inside a loop that runs it 100 times:</p>
    <pre class="snippet" data-lang="js">for (let i = 0; i &lt; 100; i++) {
  ctx.beginPath();
  ctx.fillStyle = "rgb(255 0 0 / 50%)";
  ctx.arc(random(WIDTH), random(HEIGHT), random(50), 0, 2 * Math.PI);
  ctx.fill();
}</pre>
    <h3>With and without a loop</h3>
    <p>Without the loop you'd need the four drawing lines 100 times over: 400 lines instead of 6. And changing "100" to "1000" would mean 3,600 more lines instead of editing one number.</p>""")
b += ST("Play", "Draw with a loop", "Change how many times the loop runs, and redraw.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="cv-n">loop runs</label><input id="cv-n" type="range" min="1" max="500" value="100"><span class="readout" id="cv-n-out"></span></div>
      <button class="btn run" type="button" id="cv-go">Redraw</button>
      <p class="hint">Each pass through the loop draws one circle at a random position and size.</p>
    </div>
    <div class="cv-wrap"><canvas id="cv" width="520" height="260" role="img" aria-label="Randomly placed translucent red circles"></canvas></div>
  </section>

"""
b += ST("Read", "Looping through a collection") + prose("""
    <p>Most of the time you'll loop over a collection, usually an <span class="term">array</span>.</p>
    <h3>The for...of loop</h3>
    <p><code>for...of</code> runs its block once per item. Each time round, the variable (here <code>trail</code>) holds the current item. Each pass is one <em>iteration</em>.</p>
    <pre class="snippet" data-lang="js">const trails = ["Mesa", "Royal Arch", "Flagstaff"];
for (const trail of trails) {
  console.log(trail);
}</pre>
    <h3>map() and filter()</h3>
    <p>Arrays also have methods that do the looping for you. <code>map()</code> calls a function on every item and collects the results in a new array. <code>filter()</code> calls a function on every item and keeps only the items where it returns <code>true</code>.</p>""")
b += ST("Play", "map() and filter()", "Pick a method and watch each item go through the function.") + pg_mf
b += ST("Read", "The standard for loop") + prose("""
    <p>A standard <code>for</code> loop counts. It has three parts, separated by semicolons:</p>
    <pre class="snippet" data-lang="js">for (let i = 0; i &lt; 10; i++) {
  // runs with i = 0, 1, 2 … 9
}</pre>
    <ol>
      <li>An <strong>initializer</strong>, <code>let i = 0</code>: a counter, run once at the start.</li>
      <li>A <strong>condition</strong>, <code>i &lt; 10</code>: checked before each pass; the loop stops when it's false.</li>
      <li>A <strong>final expression</strong>, <code>i++</code>: run after each pass.</li>
    </ol>
    <h3>Calculating squares</h3>""")
b += runner("""let results = "";
for (let i = 1; i < 10; i++) {
  results += `${i} x ${i} = ${i * i}, `;
}
console.log(results);""")
b += prose("""
    <h3>Looping through collections with a for loop</h3>
    <p>A <code>for</code> loop can walk an array too, using the counter as the <span class="term">index</span>. Use it when you need the position, for example to treat the last item differently:</p>""")
b += runner("""const cats = ["Pete", "Biggles", "Jasmine"];
let myFavoriteCats = "My cats are called ";

for (let i = 0; i < cats.length; i++) {
  if (i === cats.length - 1) {
    myFavoriteCats += `and ${cats[i]}.`;
  } else {
    myFavoriteCats += `${cats[i]}, `;
  }
}
console.log(myFavoriteCats);""")
b += ST("Play", "Step through a loop", "Pick a loop and press Step to run it one piece at a time. The two \"bug\" versions show the most common loop mistakes.") + pg_step
b += ST("Read", "Exiting loops with break") + prose("""
    <p><code>break</code> stops the loop immediately, even if there are items left. Use it when you've found what you were looking for.</p>""")
b += ST("Read", "Skipping iterations with continue") + prose("""
    <p><code>continue</code> skips the rest of the current pass and moves on to the next one.</p>""")
b += ST("Try it", "break and continue", "Change the names and run it again.") + brk
b += ST("Read", "while and do...while") + prose("""
    <p>A <code>while</code> loop repeats as long as its condition is true. It's like a <code>for</code> loop with the initializer before it and the final expression inside it, and it's handy when you don't know in advance how many times to go round.</p>
    <p><code>do...while</code> checks the condition at the <em>end</em>, so its block always runs at least once.</p>""")
b += runner("""let i = 0;
while (i < 3) {
  console.log("while, pass", i);
  i++;
}

let j = 10;
do {
  console.log("do...while runs once even though", j, "isn't < 3");
  j++;
} while (j < 3);""")
b += prose("""
    <div class="callout warn"><p class="callout-title">Watch out</p><p>Every loop needs a way to stop. Forget the <code>i++</code> in a <code>while</code> loop and its condition never becomes false: it runs forever and freezes the page. If that happens, close the tab, then check what changes the condition.</p></div>""")
b += ST("Practice", "Add up the miles", "Start a total at 0, then add each item to it.") + '  <div id="ex-total"></div>\n\n'
b += ST("Practice", "Implementing a launch countdown", "From MDN: count down from 10 with a while loop.") + '  <div id="ex-count"></div>\n\n'
b += ST("Practice", "Filling in a guest list", "From MDN: sort guests into admitted and refused.") + '  <div id="ex-guests"></div>\n\n'
b += ST("Read", "Which loop type should you use?") + prose("""
    <p>For going through every item in an array, use <code>for...of</code>: it's the simplest and hardest to get wrong. If you need the index, or to count a set number of times, use a standard <code>for</code> loop. To build a new array from an old one, reach for <code>map()</code> or <code>filter()</code>. Use <code>while</code> when you don't know how many passes you'll need, and keep <code>do...while</code> for the rare "at least once" case.</p>""")
b += notes([
  "A loop runs a block repeatedly; each pass is an iteration.",
  "<code>for...of</code> visits every item; <code>map()</code> transforms them; <code>filter()</code> keeps some.",
  "<code>for (let i = 0; i &lt; n; i++)</code>: initializer, condition, final expression.",
  "<code>break</code> stops the loop; <code>continue</code> skips to the next pass.",
  "<code>while</code> repeats while a condition is true; <code>do...while</code> always runs once.",
], [
  "<code>i &lt;= arr.length</code>, which runs one pass too many and reads <code>undefined</code>.",
  "A <code>while</code> loop with nothing that makes its condition false: an infinite loop.",
  "Declaring the total inside the loop, so it resets every pass.",
  "Expecting <code>map()</code> to change the original array.",
])
first, items = split_quiz(src.first_script())
js = r'''
  // --- canvas circles ---
  function cvDraw() {
    const c = $("cv"), ctx = c.getContext("2d"), n = +$("cv-n").value, W = c.width, H = c.height;
    const random = (x) => Math.floor(Math.random() * x);
    $("cv-n-out").textContent = n + (n === 1 ? " time" : " times");
    ctx.clearRect(0, 0, W, H);
    for (let i = 0; i < n; i++) {
      ctx.beginPath();
      ctx.fillStyle = "rgb(255 0 0 / 50%)";
      ctx.arc(random(W), random(H), random(50), 0, 2 * Math.PI);
      ctx.fill();
    }
  }
  $("cv-n").addEventListener("input", cvDraw);
  $("cv-go").addEventListener("click", cvDraw);
  cvDraw();
'''
ex_t = src.block('  makeExercise(document.getElementById("ex-total"), {')
ex_n = r'''  makeExercise(document.getElementById("ex-count"), {
    title: "Countdown",
    task: `<p><code>countdown(start)</code> returns an array of messages. Use a <code>while</code> loop that counts down from <code>start</code> to 0:</p>
    <ul>
      <li>For every number above 0, add <code>"Countdown 10"</code>, <code>"Countdown 9"</code> and so on.</li>
      <li>For 0, add <code>"Blast off!"</code> instead.</li>
    </ul>`,
    js: `function countdown(start) {
  const messages = [];
  let i = start;
  // while loop here

  return messages;
}

console.log(countdown(10));`,
    solution: `function countdown(start) {
  const messages = [];
  let i = start;
  while (i >= 0) {
    if (i === 0) {
      messages.push("Blast off!");
    } else {
      messages.push(\`Countdown \${i}\`);
    }
    i--;
  }
  return messages;
}

console.log(countdown(10));`,
    expose: ["countdown"],
    hints: [
      "while (i >= 0) { … } keeps going down to and including 0.",
      "Inside, an if checks for 0; messages.push() adds a message.",
      "Don't forget i-- at the end of the loop, or it never stops.",
    ],
    checks: [
      { label: "Uses a while loop", test: ({ code }) => /while\s*\(/.test(code.js) },
      { label: "countdown(3) gives four messages ending in “Blast off!”", test: ({ fns }) => fns.countdown(3).join("|") === "Countdown 3|Countdown 2|Countdown 1|Blast off!" },
      { label: "countdown(10) starts at “Countdown 10”", test: ({ fns }) => { const m = fns.countdown(10); return m.length === 11 && m[0] === "Countdown 10" && m[10] === "Blast off!"; } },
    ],
  });

  makeExercise(document.getElementById("ex-guests"), {
    title: "Admit or refuse",
    task: `<p><code>guestList(people)</code> returns an object with two strings. Phil and Lola aren't allowed in; everyone else is.</p>
    <ul>
      <li><code>admitted</code>: <code>"Admit: Chris, Anne, Colin, Terri, Sam, Kay, Bruce"</code></li>
      <li><code>refused</code>: <code>"Refuse: Phil, Lola"</code></li>
    </ul>
    <p>Loop through the people, add each name and <code>", "</code> to the right string, then trim the final <code>", "</code> off each with <code>slice(0, -2)</code>.</p>`,
    js: `function guestList(people) {
  let admitted = "Admit: ";
  let refused = "Refuse: ";
  // loop, if, +=

  return { admitted, refused };
}

const people = ["Chris", "Anne", "Colin", "Terri", "Phil", "Lola", "Sam", "Kay", "Bruce"];
console.log(guestList(people));`,
    solution: `function guestList(people) {
  let admitted = "Admit: ";
  let refused = "Refuse: ";
  for (const person of people) {
    if (person === "Phil" || person === "Lola") {
      refused += \`\${person}, \`;
    } else {
      admitted += \`\${person}, \`;
    }
  }
  admitted = admitted.slice(0, -2);
  refused = refused.slice(0, -2);
  return { admitted, refused };
}

const people = ["Chris", "Anne", "Colin", "Terri", "Phil", "Lola", "Sam", "Kay", "Bruce"];
console.log(guestList(people));`,
    expose: ["guestList"],
    hints: [
      "for (const person of people) { … }",
      "if (person === \"Phil\" || person === \"Lola\") decides which string to add to.",
      "slice(0, -2) returns everything except the last two characters.",
    ],
    checks: [
      { label: "Admits everyone but Phil and Lola", test: ({ fns }) => fns.guestList(["Chris", "Anne", "Colin", "Terri", "Phil", "Lola", "Sam", "Kay", "Bruce"]).admitted === "Admit: Chris, Anne, Colin, Terri, Sam, Kay, Bruce" },
      { label: "Refuses Phil and Lola", test: ({ fns }) => fns.guestList(["Chris", "Anne", "Colin", "Terri", "Phil", "Lola", "Sam", "Kay", "Bruce"]).refused === "Refuse: Phil, Lola" },
      { label: "Works for a different list", test: ({ fns }) => { const r = fns.guestList(["Lola", "Ada"]); return r.admitted === "Admit: Ada" && r.refused === "Refuse: Lola"; } },
    ],
  });
'''
items += '''    { id: "q90", q: "How many times does for (let i = 0; i < 5; i++) run?", opts: ["4", "5", "6"], a: 1, why: "i is 0, 1, 2, 3 and 4." },
    { id: "q91", q: "Which loop always runs its block at least once?", opts: ["while", "do...while", "for...of"], a: 1, why: "do...while checks its condition at the end." },
'''
write("core-loops.html", h, b, "\n" + RUNNER + "<script>" + first + js + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_t + "\n" + ex_n + "</script>\n")
