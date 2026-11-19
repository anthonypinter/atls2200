import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-conditionals")
pg_temp = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="temp">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>AND, OR, NOT')
pg_logic = src.between('  <section class="playground">\n    <div class="panel controls">\n      <label class="check"><input type="checkbox" id="weekend"', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Truthy')
pg_truthy = src.between('  <section class="playground">\n    <div class="panel controls"><span class="eyebrow">const value =</span>', '  <div class="section-title"><span class="eyebrow">Try it</span>')
rn = src.between('  <div class="runner"><textarea aria-label="Code editor">console.log(5 === 5,', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Conditionals", src.css())
b = top("Conditionals", "Programs make choices: show the error or don't, say good morning or good evening, pick a color theme. Conditionals run code only when something is true.", [
  "Write <code>if</code>, <code>else if</code> and <code>else</code> chains, in the right order.",
  "Use truthy and falsy values, and combine conditions with <code>&amp;&amp;</code>, <code>||</code> and <code>!</code>.",
  "Match one value against many cases with <code>switch</code>.",
  "Choose between two values with the ternary operator.",
])
b += ST("Read", "if...else statements") + prose("""
    <h3>Basic if...else syntax</h3>
    <p>A <span class="term">conditional</span> runs a block of code only if a condition is true, and (optionally) a different block if it isn't:</p>
    <pre class="snippet" data-lang="js">if (condition) {
  // runs if the condition is true
} else {
  // runs otherwise
}</pre>
    <h3>A real example</h3>
    <p>MDN's example: a child is asked to help their parent. If they did the shopping, they get pocket money; if not, they don't.</p>""")
b += runner("""let shoppingDone = false;
let childsAllowance;

if (shoppingDone === true) {
  childsAllowance = 10;
} else {
  childsAllowance = 5;
}

console.log(`Allowance: $${childsAllowance}`);""")
b += prose("""
    <h3>else if</h3>
    <p>For more than two choices, chain <code>else if</code>s. JavaScript checks each condition from top to bottom, runs the <em>first</em> block whose condition is true, then skips everything else, even if later conditions would also be true. So order matters: put the most specific conditions first.</p>
    <pre class="snippet" data-lang="js">if (temp &gt;= 85) {
  msg = "Hike early. It'll be hot.";
} else if (temp &gt;= 50) {
  msg = "Perfect hiking weather.";
} else {
  msg = "Bring layers.";
}</pre>""")
b += ST("Play", "Change the temperature", "Change the value and watch which branch runs. Then flip the order of the conditions.") + pg_temp
b += prose("""
    <h3>A note on comparison operators</h3>
    <p>Compare with <code>&lt;</code>, <code>&gt;</code>, <code>&lt;=</code>, <code>&gt;=</code>, <span class="term" data-term="=== (strict equality)">===</span> and <code>!==</code>. Always use three equals signs.</p>
    <p>A condition doesn't have to be a comparison: any value works. Six values count as false: <code>false</code>, <code>0</code>, <code>""</code>, <code>null</code>, <code>undefined</code> and <code>NaN</code>. These are called <span class="term" data-term="Truthy / falsy">falsy</span>, and everything else is truthy. So <code>if (name)</code> checks whether someone typed anything.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p><code>if (x = 5)</code> doesn't compare. It sets <code>x</code> to 5, and since 5 is truthy, the block always runs.</p></div>""")
b += ST("Play", "Truthy and falsy", "Pick a value and see whether the if block runs.") + pg_truthy
b += prose("""
    <h3>Nesting if...else</h3>
    <p>You can put an <code>if</code> inside another one, to make a second decision only after the first:</p>""")
b += runner("""const choice = "sunny";
const temperature = 92;

if (choice === "sunny") {
  if (temperature < 86) {
    console.log(`It's ${temperature}°F: nice and sunny. Go hiking!`);
  } else {
    console.log(`It's ${temperature}°F: really hot. Hike early, or find shade.`);
  }
}""")
b += prose("""
    <h3>Logical operators: AND, OR and NOT</h3>
    <p>Often you can avoid nesting by combining conditions:</p>
    <ul>
      <li><code>&amp;&amp;</code> (AND): true only if <em>both</em> sides are true. <code>if (choice === "sunny" &amp;&amp; temperature &lt; 86)</code></li>
      <li><code>||</code> (OR): true if <em>at least one</em> side is true.</li>
      <li><code>!</code> (NOT): flips true and false. <code>if (!isRaining)</code></li>
    </ul>
    <p>A classic mistake: <code>if (x === 5 || 7)</code> doesn't mean "x is 5 or 7". It means "x is 5, or 7 is truthy", and 7 is always truthy, so it always runs. Write both comparisons in full: <code>if (x === 5 || x === 7)</code>.</p>""")
b += ST("Play", "AND, OR, NOT", "Flip the two values and switch the operator.") + pg_logic
b += ST("Read", "switch statements") + prose("""
    <p>When you're checking one value against lots of exact matches, a long <code>else if</code> chain gets repetitive. A <code>switch</code> statement is tidier:</p>
    <h3>A switch example</h3>
    <p>Each <code>case</code> is one possible value. When one matches, its code runs until <code>break</code>. If you leave out <code>break</code>, it carries on into the next case, which is handy for grouping (Saturday and Sunday below) but a bug if you forget. <code>default</code> runs if nothing matches.</p>""")
b += runner("""const choice = "rainy";

switch (choice) {
  case "sunny":
    console.log("It is nice and sunny outside today. Wear shorts!");
    break;
  case "rainy":
    console.log("Rain is falling outside; take a rain coat and an umbrella.");
    break;
  case "snowing":
    console.log("The snow is coming down. Time for a snowball fight!");
    break;
  default:
    console.log("No forecast for that.");
}""")
b += ST("Read", "Ternary operator") + prose("""
    <p>The ternary operator is a one-line <code>if...else</code> that produces a value: <code>condition ? valueIfTrue : valueIfFalse</code>. It's ideal for picking between two things, like two greetings or two themes:</p>
    <h3>Ternary operator example</h3>
    <pre class="snippet" data-lang="js">const greeting = isBirthday
  ? "Happy birthday Mrs. Smith — we hope you have a great day!"
  : "Good morning Mrs. Smith.";</pre>""")
b += ST("Try it", "===, the ternary and switch", "Change the values and run it again.") + rn
b += ST("Practice", "Fix the decision", "This function gives the wrong advice on hot days and ignores the rain. Reorder and add to it.") + '  <div id="ex-cond"></div>\n\n'
b += ST("Practice", "Implementing a basic calendar", "From MDN: how many days does a month have?") + '  <div id="ex-cal"></div>\n\n'
b += ST("Practice", "Adding more color choices", "From MDN: turn a two-way choice into a switch with five themes.") + '  <div id="ex-theme"></div>\n\n'
b += notes([
  "<code>if</code> / <code>else if</code> / <code>else</code> runs the first block whose condition is true, then stops checking.",
  "Compare with <code>===</code> and <code>!==</code>. Falsy values: <code>false</code>, <code>0</code>, <code>\"\"</code>, <code>null</code>, <code>undefined</code>, <code>NaN</code>.",
  "<code>&amp;&amp;</code> needs both, <code>||</code> needs either, <code>!</code> flips.",
  "<code>switch</code> matches one value against exact cases; don't forget <code>break</code>.",
  "<code>condition ? a : b</code> picks a value in one line.",
], [
  "<code>if (x = 5)</code>: one equals sign assigns instead of comparing.",
  "<code>x === 5 || 7</code>, which is always true. Write <code>x === 5 || x === 7</code>.",
  "Putting a general condition (<code>&gt;= 50</code>) before a specific one (<code>&gt;= 85</code>), so the specific one never runs.",
  "Forgetting <code>break</code> in a <code>switch</code>, so the next case runs too.",
])
first, items = split_quiz(src.first_script())
ex_c = src.block('  makeExercise(document.getElementById("ex-cond"), {')
ex_n = r'''  makeExercise(document.getElementById("ex-cal"), {
    title: "Days in a month",
    task: `<p><code>daysInMonth(month)</code> gets a month name like <code>"April"</code>. Ignore leap years.</p>
    <ol>
      <li><code>"February"</code> has 28 days.</li>
      <li><code>"April"</code>, <code>"June"</code>, <code>"September"</code> and <code>"November"</code> have 30. Use <code>||</code> to check all four in one condition.</li>
      <li>Every other month has 31.</li>
    </ol>`,
    js: `function daysInMonth(month) {
  let days = 31;
  // Your if / else if here

  return days;
}

console.log(daysInMonth("February"), daysInMonth("June"), daysInMonth("July"));`,
    solution: `function daysInMonth(month) {
  let days = 31;
  if (month === "February") {
    days = 28;
  } else if (month === "April" || month === "June" || month === "September" || month === "November") {
    days = 30;
  }
  return days;
}

console.log(daysInMonth("February"), daysInMonth("June"), daysInMonth("July"));`,
    expose: ["daysInMonth"],
    hints: [
      "if (month === \"February\") { days = 28; }",
      "Each part of an || needs its own full comparison: month === \"April\" || month === \"June\" || …",
    ],
    checks: [
      { label: "February has 28 days", test: ({ fns }) => fns.daysInMonth("February") === 28 },
      { label: "April, June, September and November have 30", test: ({ fns }) => ["April", "June", "September", "November"].every((m) => fns.daysInMonth(m) === 30) },
      { label: "The other months have 31", test: ({ fns }) => ["January", "March", "May", "July", "August", "October", "December"].every((m) => fns.daysInMonth(m) === 31) },
      { label: "Uses || to combine the 30-day months", test: ({ code }) => /\|\|/.test(code.js) },
    ],
  });

  makeExercise(document.getElementById("ex-theme"), {
    title: "Five themes",
    task: `<p><code>theme(choice)</code> returns an object with a background (<code>bg</code>) and text color (<code>text</code>). Rewrite it with a <code>switch</code> so it handles all five choices:</p>
    <ul>
      <li><code>"white"</code>: bg <code>"white"</code>, text <code>"black"</code></li>
      <li><code>"black"</code>: bg <code>"black"</code>, text <code>"white"</code></li>
      <li><code>"purple"</code>: bg <code>"purple"</code>, text <code>"white"</code></li>
      <li><code>"yellow"</code>: bg <code>"yellow"</code>, text <code>"purple"</code></li>
      <li><code>"psychedelic"</code>: bg <code>"lime"</code>, text <code>"purple"</code></li>
    </ul>
    <p>Anything else: bg <code>"white"</code>, text <code>"black"</code> (the <code>default</code>).</p>`,
    js: `function theme(choice) {
  return choice === "black"
    ? { bg: "black", text: "white" }
    : { bg: "white", text: "black" };
}

console.log(theme("yellow"));`,
    solution: `function theme(choice) {
  switch (choice) {
    case "black":
      return { bg: "black", text: "white" };
    case "purple":
      return { bg: "purple", text: "white" };
    case "yellow":
      return { bg: "yellow", text: "purple" };
    case "psychedelic":
      return { bg: "lime", text: "purple" };
    case "white":
    default:
      return { bg: "white", text: "black" };
  }
}

console.log(theme("yellow"));`,
    expose: ["theme"],
    hints: [
      "switch (choice) { case \"black\": … }",
      "Inside a function, return ends the case, so you don't need break after a return.",
      "default: catches every other value.",
    ],
    checks: [
      { label: "Uses a switch", test: ({ code }) => /switch\s*\(/.test(code.js) },
      { label: "black and purple themes", test: ({ fns }) => JSON.stringify(fns.theme("black")) === '{"bg":"black","text":"white"}' && JSON.stringify(fns.theme("purple")) === '{"bg":"purple","text":"white"}' },
      { label: "yellow and psychedelic themes", test: ({ fns }) => JSON.stringify(fns.theme("yellow")) === '{"bg":"yellow","text":"purple"}' && JSON.stringify(fns.theme("psychedelic")) === '{"bg":"lime","text":"purple"}' },
      { label: "white and anything else fall back to white", test: ({ fns }) => ["white", "beige", ""].every((c) => JSON.stringify(fns.theme(c)) === '{"bg":"white","text":"black"}') },
    ],
  });
'''
items += '''    { id: "q90", q: "x is 3. What does if (x === 5 || 7) do?", opts: ["Skips the block", "Runs the block, because 7 is truthy", "Throws an error"], a: 1, why: "Each side of || is its own condition. Write x === 5 || x === 7." },
    { id: "q91", q: "What happens in a switch case with no break?", opts: ["It carries on into the next case", "It stops anyway", "It's a syntax error"], a: 0, why: "Without break (or return), execution falls through to the next case." },
'''
write("core-conditionals.html", h, b, "\n" + RUNNER + "<script>" + first + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_c + "\n" + ex_n + "</script>\n")
