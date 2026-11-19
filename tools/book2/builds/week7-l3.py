import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-variables")
pg_step = src.between('  <section class="playground even">\n    <div class="stage-col">\n      <div class="stepper">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Name checker')
pg_name = src.between('  <section class="playground">\n    <div class="panel namer">', '  <div class="section-title"><span class="eyebrow">Try it</span><h2>typeof')
typeof_runner = src.between('  <div class="runner"><textarea aria-label="Code editor">let zip = "80302";', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Variables", src.css(), """
  .vc { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  @media (max-width: 640px) { .vc { grid-template-columns: 1fr; } }
  .vc .panel { display: grid; gap: 8px; justify-items: start; align-content: start; }
  .vc output { font: 800 1.4rem var(--font-display); }
""")
b = top("Variables", "A program needs to remember things: a score, a name, whether a menu is open. Variables give values a name so you can use and change them later.", [
  "Declare and initialize variables with <code>let</code> and <code>const</code>, and know why to avoid <code>var</code>.",
  "Name variables so they work and read well.",
  "Recognise the main types of value, and check them with <code>typeof</code>.",
  "Choose between <code>const</code> and <code>let</code>.",
])
b += ST("Read", "What is a variable?") + prose("""
    <p>A <span class="term">variable</span> is a container for a value: a name that holds something so you can use it later. Think of a labelled box.</p>
    <h3>Variable example</h3>
    <p>MDN's example counts button presses. The count lives in a variable, and each press adds one to it:</p>
    <pre class="snippet" data-lang="js">const buttonA = document.querySelector("#button_A");
let count = 0;

buttonA.addEventListener("click", () => {
  count += 1;
  headingA.textContent = `${count} clicks so far`;
});</pre>
    <h3>Without a variable</h3>
    <p>Without somewhere to store the count, the program can't remember anything between presses. Try both:</p>""")
b += ST("Play", "With and without a variable") + """  <div class="vc">
    <div class="panel"><span class="eyebrow">With a variable</span><button class="btn run" type="button" id="vc-a">Press me</button><output id="vc-a-out" aria-live="polite">0 clicks so far</output></div>
    <div class="panel"><span class="eyebrow">Without one</span><button class="btn run" type="button" id="vc-b">Press me</button><output id="vc-b-out" aria-live="polite">0 clicks so far</output><p class="hint">This version can't store anything, so every press starts from nothing again.</p></div>
  </div>

"""
b += ST("Read", "Declaring a variable") + prose("""
    <p>To make a variable, <strong>declare</strong> it with <code>let</code> (or <code>const</code>) and a name. A declared variable with no value holds <code>undefined</code>, which is different from a name that doesn't exist at all:</p>""")
b += runner("""let myName;
console.log(myName);       // declared, but empty: undefined

console.log(myAge);        // never declared: ReferenceError""")
b += ST("Read", "Initializing a variable") + prose("""
    <p><strong>Initializing</strong> means giving a variable its first value, with <code>=</code>. You can do it on its own line or, usually, at the same time as declaring:</p>
    <pre class="snippet" data-lang="js">let myName;
myName = "Chris";          // initialize later

let myDog = "Rover";       // declare and initialize at once</pre>""")
b += ST("Read", "A note about var") + prose("""
    <p>Older code uses <code>var</code>. It works, but it has quirks that cause bugs: you can use a <code>var</code> before the line that declares it (it's "hoisted" and quietly holds <code>undefined</code>), and you can declare the same name twice without any error. <code>let</code> and <code>const</code>, added in 2015, catch both mistakes. Use them, and read <code>var</code> as "old code".</p>""")
b += runner("""console.log(oldWay);   // undefined, no error: hoisted
var oldWay = "var";
var oldWay = "declared twice, still no error";
console.log(oldWay);

let newWay = "let";
// Remove the // below and run again: let won't allow it,
// and because it's a syntax error, nothing runs at all.
// let newWay = "declared twice";""")
b += ST("Read", "Updating a variable") + prose("""
    <p>Once a <code>let</code> variable exists, give it a new value with <code>=</code>, without <code>let</code>. Writing <code>let</code> again is an error: you only declare once.</p>
    <pre class="snippet" data-lang="js">let miles = 6.7;
miles = miles + 1;   // now 7.7</pre>""")
b += ST("Play", "Watch the boxes change", "Step through the code one line at a time and watch each variable's value.") + pg_step
b += prose("""
    <h3>An aside on variable naming rules</h3>
    <p>Names can contain letters, numbers, <code>_</code> and <code>$</code>, but can't start with a number, contain spaces, or be one of JavaScript's reserved words like <code>let</code> or <code>function</code>. Use "lower camel case" for multi-word names: <code>trailName</code>, <code>isOpen</code>. Names are case-sensitive, so <code>score</code> and <code>Score</code> are two different variables. Choose names that say what the value is.</p>""")
b += ST("Play", "Name checker", "Some names break your code, and others just make it hard to read. Type a variable name, or try one of the examples.") + pg_name
b += ST("Read", "Variable types") + prose("""
    <p>Every value has a type. The main ones:</p>
    <h3>Numbers</h3>
    <p>Whole numbers or decimals, with no quotes: <code>let miles = 6.7;</code></p>
    <h3>Strings</h3>
    <p>Text, in quotes: <code>let trail = "Mesa";</code> Quotes always make a string, even <code>"42"</code>.</p>
    <h3>Booleans</h3>
    <p>Just <code>true</code> or <code>false</code>, often the result of a comparison: <code>let isLong = miles &gt; 5;</code></p>
    <h3>Arrays</h3>
    <p>A list of values in square brackets, counted from 0: <code>let trails = ["Mesa", "Royal Arch"];</code> then <code>trails[0]</code> is <code>"Mesa"</code>.</p>
    <h3>Objects</h3>
    <p>A group of named values in curly braces: <code>let hike = { name: "Mesa", miles: 6.7 };</code> then <code>hike.name</code> is <code>"Mesa"</code>.</p>""")
b += runner("""const trails = ["Mesa", "Royal Arch", "Bear Peak"];
console.log(trails[0], trails[2]);

const hike = { name: "Mesa", miles: 6.7, isOpen: true };
console.log(hike.name, hike.miles, hike.isOpen);
console.log(hike.miles > 5);""")
b += ST("Read", "Dynamic typing") + prose("""
    <p>JavaScript is <strong>dynamically typed</strong>: you don't say what type a variable holds, and the same <code>let</code> variable can hold a string now and a number later. <span class="term">typeof</span> tells you what type a value is right now.</p>""")
b += ST("Try it", "typeof", "Quotes always make a string, even when the value looks like a number. Change the values and run it again.") + typeof_runner
b += ST("Read", "Constants in JavaScript") + prose("""
    <p><span class="term">const</span> creates a variable that can't be given a new value. It must be initialized when it's declared, and <code>=</code> on it later is an error. But a <code>const</code> holding an object or array can still have its <em>contents</em> changed: the box can't be swapped, but what's inside it can.</p>""")
b += runner("""const hike = { name: "Mesa", miles: 6.7 };
hike.miles = 7;            // fine: changing what's inside
console.log(hike.miles);

const trails = ["Mesa"];
trails.push("Royal Arch"); // fine too
console.log(trails);

hike = { name: "Bear Peak" };   // error: can't assign a new value""")
b += ST("Read", "When to use const and when to use let") + prose("""
    <p>Use <code>const</code> by default, and <code>let</code> only when you know the value will be reassigned, like a counter or a score. That way, anyone reading your code knows which values move, and JavaScript stops you if you change one by accident.</p>""")
b += ST("Practice", "Pick const or let", "Each of these variables is declared the wrong way. Fix them so the code runs and says what it means.") + '  <div id="ex-vars"></div>\n\n'
b += ST("Practice", "One of each type", "Store a trail's details using five different types of value.") + '  <div id="ex-types"></div>\n\n'
b += notes([
  "A variable is a named container for a value. Declare it once, with <code>let</code> or <code>const</code>.",
  "A declared but empty variable is <code>undefined</code>; an undeclared name is a <code>ReferenceError</code>.",
  "Avoid <code>var</code>: it's hoisted and can be redeclared without warning.",
  "Main types: numbers, strings, booleans, arrays and objects. <code>typeof</code> tells you which.",
  "<code>const</code> by default; <code>let</code> when the value will be reassigned. A <code>const</code> object's contents can still change.",
], [
  "Writing <code>let</code> again when updating a variable.",
  "Putting quotes around a number: <code>\"42\"</code> is a string.",
  "Names with spaces or starting with a number, like <code>2ndTrail</code>.",
  "Using <code>const</code> for a counter, then trying to add to it.",
])
first, items = split_quiz(src.first_script())
js = r'''
  // --- With and without a variable ---
  let vcCount = 0;
  $("vc-a").addEventListener("click", () => { vcCount += 1; $("vc-a-out").textContent = `${vcCount} click${vcCount === 1 ? "" : "s"} so far`; });
  $("vc-b").addEventListener("click", () => { $("vc-b-out").textContent = "1 click so far"; });
'''
ex_v = src.block('  makeExercise(document.getElementById("ex-vars"), {')
ex_t = r'''  makeExercise(document.getElementById("ex-types"), {
    title: "Trail details",
    task: `<p>Declare these with <code>const</code>, then run the code to see their types.</p>
    <ol>
      <li><code>trailName</code>: the string <code>"Royal Arch"</code></li>
      <li><code>miles</code>: the number <code>3.4</code> (no quotes)</li>
      <li><code>isOpen</code>: the boolean <code>true</code></li>
      <li><code>tags</code>: an array with <code>"steep"</code> and <code>"views"</code></li>
      <li><code>trail</code>: an object whose <code>name</code> is <code>trailName</code> and whose <code>miles</code> is <code>miles</code></li>
    </ol>`,
    js: `// Declare your five variables here


console.log(typeof trailName, typeof miles, typeof isOpen);
console.log(tags[1], trail.name);`,
    solution: `const trailName = "Royal Arch";
const miles = 3.4;
const isOpen = true;
const tags = ["steep", "views"];
const trail = { name: trailName, miles: miles };

console.log(typeof trailName, typeof miles, typeof isOpen);
console.log(tags[1], trail.name);`,
    expose: ["trailName", "miles", "isOpen", "tags", "trail"],
    hints: [
      "Strings need quotes; numbers and booleans don't.",
      "An array uses square brackets: [\"steep\", \"views\"].",
      "An object uses curly braces with name: value pairs: { name: trailName, miles: miles }.",
    ],
    checks: [
      { label: "trailName is the string “Royal Arch”", test: ({ fns }) => fns.trailName === "Royal Arch" },
      { label: "miles is the number 3.4, and isOpen is true", test: ({ fns }) => fns.miles === 3.4 && fns.isOpen === true },
      { label: "tags is an array of “steep” and “views”", test: ({ fns }) => Array.isArray(fns.tags) && fns.tags.join() === "steep,views" },
      { label: "trail is an object with the same name and miles", test: ({ fns }) => fns.trail && fns.trail.name === "Royal Arch" && fns.trail.miles === 3.4 },
      { label: "All five use const", test: ({ code }) => ["trailName", "miles", "isOpen", "tags", "trail"].every((n) => new RegExp("const\\s+" + n + "\\b").test(code.js)) },
    ],
  });
'''
items += '''    { id: "q90", q: "let myName; console.log(myName); What's logged?", opts: ["undefined", "An error", "An empty string"], a: 0, why: "It's declared but has no value yet. An undeclared name would be a ReferenceError." },
    { id: "q91", q: "Why avoid var?", opts: ["It's slower", "It can be used before its declaration and redeclared without an error", "It can't hold strings"], a: 1, why: "let and const catch both mistakes." },
    { id: "q92", q: "const trails = [\\"Mesa\\"]; trails.push(\\"Royal Arch\\"); What happens?", opts: ["An error: trails is a const", "It works: the array's contents can change", "Nothing"], a: 1, why: "const stops reassignment, not changes to an object's or array's contents." },
'''
write("core-variables.html", h, b, "\n" + RUNNER + "<script>" + first + js + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_v + "\n" + ex_t + "</script>\n")
