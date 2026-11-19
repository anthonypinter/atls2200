import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-errors")
pg_game = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">Test the game</span>', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Error message decoder')
pg_dec = src.between('  <section class="playground">\n    <div class="panel decoder"', '  <div class="section-title"><span class="eyebrow">Practice</span>')
fixit = src.between('  <div class="runner"><textarea aria-label="Code editor">const trail = "Royal Arch";', '  <div class="section-title"><span class="eyebrow">Practice</span><h2>Debug the script')
h = head("Troubleshooting JavaScript", src.css())
b = top("Troubleshooting JavaScript", "Everyone's code breaks. The skill is finding out why, quickly: reading the console's error messages, logging values, using the debugger, and writing code that handles bad input without crashing.", [
  "Tell syntax, runtime and logic errors apart.",
  "Read an error message and its line number, and fix the first error first.",
  "Inspect values with <code>console.log()</code>, <code>console.error()</code> and the debugger.",
  "Handle errors in your own code with checks, <code>throw</code> and <code>try...catch</code>.",
])
b += ST("Read", "Types of error") + prose("""
    <p>When HTML or CSS has a mistake, you can usually see it. When JavaScript breaks, the page often just stops responding, with no message at all. The explanation is waiting in the browser's console: open <span class="term">DevTools</span> and click the Console tab.</p>
    <p>Errors come in three kinds:</p>
    <ul>
      <li>A <span class="term">syntax error</span> is a typo in the grammar of the code, like a missing bracket or quote. The browser can't understand the file, so none of the script runs.</li>
      <li>A <strong>runtime error</strong> happens while the code is running, like calling something that isn't a function. The script runs up to that line, then stops.</li>
      <li>A <strong>logic error</strong> shows no message at all. The code runs fine but does the wrong thing: the score goes down instead of up.</li>
    </ul>""")
b += ST("Read", "Fixing errors reported in the console") + prose("""
    <p>MDN's example is the number guessing game from <a href="core-what-is-javascript.html">What is JavaScript?</a>, with bugs added. Every error message tells you what went wrong and where. <code>game.js:21:13</code> means line 21, character 13; click it and the browser jumps straight to that line.</p>
    <p>Read the message slowly. <code>guessSubmit.addeventListener is not a function</code> means that on that line, the thing you called isn't a function. Here it's a capital-letter typo: JavaScript is case-sensitive, so it's <code>addEventListener</code>. <code>lowOrHi is null</code> means a <code>querySelector()</code> found nothing, usually because the selector is wrong (a class without its dot).</p>
    <p>Fix the first error first. One error stops the code after it from running, so later problems can't even show up yet. Fix it, reload, and see what's next.</p>
    <h3>A logic error</h3>
    <p>MDN's game also has a bug with no message: the "random" number is always 1. To find a logic error, use <span class="term">console.log()</span> to print values as the code runs. Is the number what you expected? Is that line running at all? Each answer narrows down where the bug is hiding.</p>""")
b += ST("Play", "Debug the guessing game", "Play the game, then open the console to find the five bugs.") + pg_game
b += ST("Read", "Other common errors") + prose("""
    <p>A handful of mistakes cause most errors:</p>
    <ul>
      <li><code>=</code> (assign) where you meant <code>===</code> (compare): <code>if (guessCount = 10)</code> sets the count to 10 instead of checking it, so the game ends after one guess.</li>
      <li>A missing <code>)</code>, <code>}</code> or quote: "missing ) after argument list", "missing } after function body", "unterminated string literal".</li>
      <li>A misspelled name: "<em>something</em> is not defined".</li>
    </ul>""")
b += ST("Play", "Error message decoder", "The errors you'll see most often. Browsers word some differently, but the type at the start (<code>SyntaxError</code>, <code>TypeError</code>, <code>ReferenceError</code>) is the same everywhere.") + pg_dec
b += ST("Practice", "Fix it yourself", "This code has three bugs. Run it, read the first error, fix that one, and run it again. When it works, the console prints three lines.") + fixit
b += ST("Practice", "Debug the script", "A syntax error, a runtime error and a logic error. Fix them one at a time, starting with the first message.") + '  <div id="ex-debug"></div>\n\n'
b += ST("Read", "Linting your code") + prose("""
    <p>A <strong>linter</strong> reads your code and points out likely mistakes before you even run it: misspelled names, variables you never use, <code>=</code> inside an <code>if</code>. The most popular one for JavaScript is <strong>ESLint</strong>.</p>
    <h3>Code editor plugins</h3>
    <p>Install the ESLint extension in VS Code and problems get a squiggly underline as you type, like a spell-checker for code.</p>""")
b += ST("Read", "Common JavaScript problems") + prose("""
    <p>Beyond typos, a few problems trip up everyone at some point: using a variable outside the block or function where it was created (<em>scope</em>), confusing <code>let</code> and <code>var</code>, and code that runs before the data it needs has arrived (like using the result of <code>fetch()</code> before it's finished). You'll meet each of these in later lessons.</p>""")
b += ST("Read", "The Console API") + prose("""
    <p><code>console.log()</code> is one of several console methods. <code>console.error()</code> prints in red, and shows the <strong>call stack</strong>: the chain of function calls that led to that line, most recent first. That tells you not just where something happened, but how the code got there.</p>""")
b += runner("""function getTrail(trails, name) {
  const trail = trails.find((t) => t.name === name);
  if (!trail) console.error("No trail called", name);
  return trail;
}

function showMiles(name) {
  const trail = getTrail([{ name: "Mesa", miles: 6.7 }], name);
  console.log("trail:", trail);
  console.log(trail.miles);   // crashes if trail is undefined
}

showMiles("Mesa");
showMiles("Mesa Trial");      // a typo in the name""")
b += prose("""
    <p>The second call logs an error, then crashes. The log right before the crash, <code>trail: undefined</code>, shows why: the lookup found nothing. In the browser's own console, the red error also lists the call stack: <code>getTrail</code>, called from <code>showMiles</code>, called from the top of the script.</p>""")
b += ST("Read", "Using the JavaScript debugger") + prose("""
    <p>For trickier bugs, the debugger lets you pause the code and look around. In the Sources tab (Chrome) or Debugger tab (Firefox), click a line number to set a <strong>breakpoint</strong>. When the code reaches that line, it pauses. The <strong>Scope</strong> panel shows every variable's current value, the <strong>Call Stack</strong> panel shows how you got there, and the step buttons run one line at a time.</p>
    <p>You can also pause from your code by writing <code>debugger;</code> on a line. It does nothing unless DevTools is open.</p>""")
b += ST("Read", "Handling JavaScript errors in your code") + prose("""
    <p>Some errors aren't your typos: they come from bad input, like a user typing "ten" where you expected a number. Good code expects them.</p>
    <h3>Conditionals</h3>
    <p>Check values before you use them, and return early if they're wrong:</p>""")
b += runner("""function toMiles(km) {
  if (typeof km !== "number" || Number.isNaN(km)) {
    return undefined;   // bad input: give up politely
  }
  return km * 0.621;
}

console.log(toMiles(10));
console.log(toMiles("ten"));
console.log(toMiles(Number("ten")));   // Number("ten") is NaN""")
b += prose("""
    <h3>Throwing custom errors</h3>
    <p>Sometimes it's better to stop with a clear message than to carry on with a bad value. <code>throw new Error("message")</code> creates your own error, which stops the function just like a built-in one.</p>
    <h3>try...catch</h3>
    <p>Code that might throw can go in a <code>try</code> block. If anything inside throws, the code jumps to <code>catch</code>, where you can handle it, and the rest of the script keeps running:</p>""")
b += runner("""function toMiles(km) {
  if (typeof km !== "number" || Number.isNaN(km)) {
    throw new Error("km must be a number");
  }
  return km * 0.621;
}

try {
  console.log(toMiles(10));
  console.log(toMiles("ten"));
  console.log("This line is skipped");
} catch (error) {
  console.log("Something went wrong:", error.message);
}

console.log("The script carries on.");""")
b += prose("""
    <h3>Feature detection</h3>
    <p>Some browser features aren't available everywhere. Check before you use one, and offer something else if it's missing:</p>
    <pre class="snippet" data-lang="js">if ("geolocation" in navigator) {
  navigator.geolocation.getCurrentPosition(showNearbyTrails);
} else {
  showAllTrails();
}</pre>""")
b += ST("Practice", "Handle bad input", "Make a conversion function that refuses bad input, and a caller that copes when it does.") + '  <div id="ex-handle"></div>\n\n'
b += ST("Read", "Finding help") + prose("""
    <p>When you're stuck, search for the exact error message. MDN's <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors">JavaScript error reference</a> explains every message; Stack Overflow probably has someone who hit the same problem; and <a href="https://caniuse.com/">caniuse.com</a> tells you which browsers support a feature. When you ask a person, include the code, the full error and what you've already tried.</p>""")
b += notes([
  "<b>Syntax errors</b> stop the whole script; <b>runtime errors</b> stop it at that line; <b>logic errors</b> give no message.",
  "Every error says what and where: <code>game.js:21:13</code> is line 21, character 13. Fix the first error first.",
  "<code>console.log()</code> checks values; <code>console.error()</code> also shows the call stack; breakpoints pause the code.",
  "Check input with <code>typeof</code> and <code>Number.isNaN()</code>; <code>throw new Error()</code> stops with a clear message.",
  "<code>try...catch</code> handles a thrown error so the rest of the script keeps running.",
], [
  "Assuming the error is on the line it names. The real cause can be earlier, such as a selector that matched nothing.",
  "Wrong capitalization: <code>addeventListener</code>, <code>queryselector</code>. JavaScript is case-sensitive.",
  "Using <code>=</code> when you mean <code>===</code> inside an <code>if</code>.",
  "Forgetting to reload the page after saving, then debugging the old code.",
])
first = src.first_script()
ex_d = src.block('  makeExercise(document.getElementById("ex-debug"), {')
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q90", q: "What happens to the code after a try block when something inside it throws?", opts: ["The whole script stops", "The catch block runs, then the script carries on", "The error is ignored silently"], a: 1, why: "catch handles the error, and code after the try...catch keeps running." },
    { id: "q91", q: "What does a linter like ESLint do?", opts: ["Runs your code faster", "Points out likely mistakes before you run the code", "Minifies your code"], a: 1, why: "It's like a spell-checker for code." },
  ]);
''')
ex_h = r'''  makeExercise(document.getElementById("ex-handle"), {
    title: "Kilometres to miles, safely",
    task: `<ol>
      <li>In <code>toMiles(km)</code>, if <code>km</code> isn't a number (or is <code>NaN</code>), <code>throw new Error("km must be a number")</code>. Otherwise return <code>km * 0.621</code>.</li>
      <li>In <code>describe(km)</code>, call <code>toMiles</code> inside a <code>try</code>. Return <code>\`\${km} km is \${miles} miles\`</code> if it works, and <code>"Error: " + error.message</code> in the <code>catch</code>.</li>
    </ol>`,
    js: `function toMiles(km) {
  return km * 0.621;
}

function describe(km) {
  const miles = toMiles(km);
  return \`\${km} km is \${miles} miles\`;
}

console.log(describe(10));
console.log(describe("ten"));`,
    solution: `function toMiles(km) {
  if (typeof km !== "number" || Number.isNaN(km)) {
    throw new Error("km must be a number");
  }
  return km * 0.621;
}

function describe(km) {
  try {
    const miles = toMiles(km);
    return \`\${km} km is \${miles} miles\`;
  } catch (error) {
    return "Error: " + error.message;
  }
}

console.log(describe(10));
console.log(describe("ten"));`,
    expose: ["toMiles", "describe"],
    hints: [
      "typeof km !== \"number\" catches strings; Number.isNaN(km) catches NaN, which is technically a number.",
      "throw new Error(\"km must be a number\"); stops the function.",
      "Put the toMiles call and the first return inside try { }, and return \"Error: \" + error.message inside catch (error) { }.",
    ],
    checks: [
      { label: "toMiles(10) returns 6.21", test: ({ fns }) => Math.abs(fns.toMiles(10) - 6.21) < 1e-9 },
      { label: "toMiles(\"ten\") throws “km must be a number”", test: ({ fns }) => { try { fns.toMiles("ten"); return false; } catch (e) { return e.message === "km must be a number"; } } },
      { label: "toMiles(NaN) throws too", test: ({ fns }) => { try { fns.toMiles(NaN); return false; } catch (e) { return e instanceof Error; } } },
      { label: "describe handles both cases", test: ({ fns }) => fns.describe(10).startsWith("10 km is 6.21") && fns.describe("ten") === "Error: km must be a number" },
    ],
  });
'''
write("core-troubleshooting-js.html", h, b, "\n" + RUNNER + "<script>" + first + "</script>\n<script>\n" + quiz + "\n" + ex_d + "\n" + ex_h + "</script>\n")
