import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-strings-numbers")
pg_add = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="a">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Useful string methods')
pg_meth = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="txt">', '  <div class="section-title"><span class="eyebrow">Try it</span>')
tmpl = src.between('  <div class="runner"><textarea aria-label="Code editor">const trail = "Mesa";', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Numbers and Strings", src.css())
b = top("Numbers and Strings", "Most of what a program does is work with numbers and text: adding up distances, building messages, checking what someone typed. Here's the math, the operators, and the most useful things you can do with strings.", [
  "Do arithmetic with JavaScript's operators, and predict the order they run in.",
  "Use increment, assignment and comparison operators.",
  "Build strings with quotes, template literals and concatenation, and convert between strings and numbers.",
  "Find, extract and change parts of a string with its methods.",
])
b += ST("Read", "Types of numbers") + prose("""
    <p>In everyday code you'll use two kinds of number, whole numbers (<em>integers</em>, like <code>42</code>) and decimals (<em>floats</em>, like <code>6.7</code>), but JavaScript has just one type for both: <code>Number</code>. (There's also <code>BigInt</code> for enormous whole numbers, which you'll rarely need.)</p>
    <h3>Useful Number methods</h3>
    <p><code>toFixed()</code> rounds a number to a set number of decimal places, for display. It returns a string.</p>
    <h3>Converting to number data types</h3>
    <p>Values that look like numbers can be strings, especially anything a visitor types into a form. <code>Number()</code> converts a string to a number; if it can't, you get <span class="term">NaN</span>, "not a number".</p>""")
b += runner("""const lotsOfDecimal = 1.7665849587;
console.log(lotsOfDecimal.toFixed(2));

const typed = "74";          // like a value from a form field
console.log(typed + 3);      // joins!
console.log(Number(typed) + 3);
console.log(Number("seventy"));
console.log(typeof 6.7, typeof "6.7");""")
b += ST("Read", "Arithmetic operators") + prose("""
    <p>JavaScript has the usual operators, <code>+</code> <code>-</code> <code>*</code> <code>/</code>, plus two more: <code>%</code> (remainder) gives what's left over after dividing, so <code>7 % 2</code> is 1, and <code>**</code> (exponent) raises to a power, so <code>5 ** 2</code> is 25.</p>
    <h3>Operator precedence</h3>
    <p>As in math class, <code>*</code> and <code>/</code> happen before <code>+</code> and <code>-</code>. Use parentheses to change the order, or just to make it clear. Predict each line before you run it:</p>""")
b += runner("""console.log(10 + 4 * 2);
console.log((10 + 4) * 2);
console.log(17 % 5);
console.log(2 ** 3);
console.log(50 + 10 / 8 + 2);
console.log((50 + 10) / (8 + 2));""")
b += ST("Read", "Increment and decrement operators") + prose("""
    <p><code>++</code> adds one to a variable and <code>--</code> takes one away. They're common in counters and loops. You can only use them on a variable, not a plain number.</p>""")
b += ST("Read", "Assignment operators") + prose("""
    <p><code>=</code> assigns a value. Shortcut versions do the math and assign in one step: <code>x += 4</code> means <code>x = x + 4</code>, and there's <code>-=</code>, <code>*=</code> and <code>/=</code> too.</p>""")
b += runner("""let guessCount = 1;
guessCount++;
console.log(guessCount);

let miles = 6.7;
miles += 3.4;      // miles = miles + 3.4
console.log(miles);
miles *= 2;
console.log(miles);""")
b += ST("Read", "Comparison operators") + prose("""
    <p>Comparisons give <code>true</code> or <code>false</code>:</p>
    <ul>
      <li><code>===</code> equal, and <code>!==</code> not equal. They check the type too, so <code>5 === "5"</code> is false.</li>
      <li><code>&lt;</code>, <code>&gt;</code>, <code>&lt;=</code>, <code>&gt;=</code> for less and greater.</li>
    </ul>
    <p>You'll see <code>==</code> and <code>!=</code> in older code. They convert types before comparing, which gives surprises, so use the triple versions.</p>""")
b += runner("""console.log(5 === 5, 5 === "5", 5 == "5");
console.log(6.7 > 5, 3 <= 3);
console.log("Mesa" !== "mesa");""")
b += ST("Read", "Declaring strings") + prose("""
    <p>A <span class="term">string</span> is text in quotes. Without the quotes, JavaScript thinks the word is a variable name and gives an error.</p>
    <h3>Single quotes, double quotes, and backticks</h3>
    <p>You can use <code>'single'</code>, <code>"double"</code> or <code>`backtick`</code> quotes, as long as the start and end match. Pick one style for normal strings and stick with it. Backticks are special: they make a <span class="term">template literal</span>.</p>""")
b += ST("Read", "Embedding JavaScript") + prose("""
    <p>Inside a template literal, <code>${ }</code> inserts the value of any variable or expression:</p>
    <pre class="snippet" data-lang="js">const name = "Chris";
const greeting = `Hello, ${name}`;</pre>
    <h3>Concatenation using "+"</h3>
    <p>The older way is to join strings with <code>+</code>, called <span class="term">concatenation</span>: <code>"Hello, " + name</code>. It works, but long ones get hard to read, with spaces easy to forget.</p>
    <h3>Including expressions in strings</h3>
    <p><code>${ }</code> can hold any expression, not just a variable: <code>`You scored ${(score / highestScore) * 100}%.`</code></p>""")
b += ST("Try it", "Template literals and Math", "Backticks let you put values right inside a string with <code>${ }</code>.") + tmpl
b += ST("Read", "Multiline strings") + prose("""
    <p>Template literals keep line breaks just as you type them. In a normal string, write <code>\\n</code> for a new line.</p>
    <h3>Including quotes in strings</h3>
    <p>To put a quote inside a string, use the other kind around it (<code>"It's steep"</code>), or <em>escape</em> it with a backslash: <code>'It\\'s steep'</code>.</p>""")
b += runner("""const poem = `Up the steps,
past the pines,
to the arch.`;
console.log(poem);

console.log("Line one\\nLine two");
console.log("It's steep");
console.log('She said "go early"');
console.log('It\\'s also fine to escape');""")
b += ST("Read", "Numbers vs. strings") + prose("""
    <p><code>+</code> does two jobs. With two numbers it adds; if either side is a string, it joins them. Other operators like <code>*</code> and <code>-</code> always try to make numbers. Convert on purpose: <code>Number("74")</code> makes a number, and <code>String(74)</code> (or <code>(74).toString()</code>) makes a string.</p>""")
b += ST("Play", "Add or join?", "Change a and b, and switch between numbers and text, to see what each operator does.") + pg_add
b += ST("Practice", "Add, don't join", "A value from a form arrives as text, so + joins instead of adding. Fix the total and tidy the output.") + '  <div id="ex-strings"></div>\n\n'
b += ST("Read", "Useful string methods") + prose("""
    <h3>Strings as objects</h3>
    <p>Strings come with built-in properties and <span class="term">methods</span>, which you use with a dot: <code>text.length</code>, <code>text.toUpperCase()</code>. Methods never change the original string: they return a new one. (Strings can't be changed at all; they're <em>immutable</em>.)</p>
    <h3>Finding the length of a string</h3>
    <p><code>text.length</code> is the number of characters. It's a property, so no parentheses.</p>
    <h3>Retrieving a specific string character</h3>
    <p>Each character has an index, counted from 0: <code>text[0]</code> is the first, and <code>text[text.length - 1]</code> is the last.</p>
    <h3>Testing if a string contains a substring</h3>
    <p><code>includes("Arch")</code>, <code>startsWith("Royal")</code> and <code>endsWith("Trail")</code> return <code>true</code> or <code>false</code>. They're case-sensitive.</p>
    <h3>Finding the position of a substring in a string</h3>
    <p><code>indexOf("Arch")</code> returns where it starts, or <code>-1</code> if it isn't there.</p>
    <h3>Extracting a substring from a string</h3>
    <p><code>slice(start, end)</code> returns the characters from <code>start</code> up to, but not including, <code>end</code>. Leave out <code>end</code> to go to the end of the string.</p>
    <h3>Changing case</h3>
    <p><code>toLowerCase()</code> and <code>toUpperCase()</code>. Handy for comparing what someone typed, whatever capitals they used.</p>
    <h3>Updating parts of a string</h3>
    <p><code>replace("old", "new")</code> changes the first match; <code>replaceAll()</code> changes every match. Remember to store the result: <code>text = text.replace(…)</code>.</p>""")
b += ST("Play", "Try the string methods", "Every character has an index, starting at 0. Pick a method to see what it returns.") + pg_meth
b += ST("Practice", "Learning challenges", "MDN's three string challenges: filter messages, fix capitals, and build a new string from parts.") + '  <div id="ex-methods"></div>\n\n'
b += notes([
  "One <code>Number</code> type for whole numbers and decimals. <code>toFixed(2)</code> rounds for display.",
  "<code>*</code> and <code>/</code> before <code>+</code> and <code>-</code>; <code>%</code> is the remainder, <code>**</code> a power.",
  "<code>++</code>, <code>+=</code> and friends update a variable; <code>===</code> and <code>!==</code> compare value and type.",
  "Template literals: <code>`${value}`</code>. <code>+</code> joins if either side is a string, so convert with <code>Number()</code>.",
  "String methods return new strings: <code>includes</code>, <code>indexOf</code>, <code>slice</code>, <code>toLowerCase</code>, <code>replace</code>.",
], [
  "Adding a form value without <code>Number()</code>: <code>\"10\" + 5</code> is <code>\"105\"</code>.",
  "Using <code>==</code> instead of <code>===</code>.",
  "Forgetting that <code>slice</code>'s end index isn't included.",
  "Calling a method and not storing the result, expecting the original string to change.",
])
first, items = split_quiz(src.first_script())
ex_s = src.block('  makeExercise(document.getElementById("ex-strings"), {')
ex_m = r'''  makeExercise(document.getElementById("ex-methods"), {
    title: "Greetings, cities and stations",
    task: `<ol>
      <li><code>isChristmas(greeting)</code> returns <code>true</code> if the greeting contains <code>"Christmas"</code>.</li>
      <li><code>fixCity(city)</code> takes a badly capitalised name like <code>"manCHESTer"</code> and returns <code>"Manchester"</code>: all lowercase, except a capital first letter.</li>
      <li><code>stationLabel(entry)</code> takes text like <code>"MAN675847583748sjt567654;Manchester Piccadilly"</code> and returns <code>"MAN: Manchester Piccadilly"</code>: the first three characters, then everything after the <code>;</code>.</li>
    </ol>`,
    js: `function isChristmas(greeting) {
  // includes()
}

function fixCity(city) {
  // toLowerCase(), then a capital first letter
}

function stationLabel(entry) {
  // slice() and indexOf(";")
}

console.log(isChristmas("Happy Christmas, one and all!"));
console.log(fixCity("manCHESTer"));
console.log(stationLabel("MAN675847583748sjt567654;Manchester Piccadilly"));`,
    solution: `function isChristmas(greeting) {
  return greeting.includes("Christmas");
}

function fixCity(city) {
  const lower = city.toLowerCase();
  return lower[0].toUpperCase() + lower.slice(1);
}

function stationLabel(entry) {
  const code = entry.slice(0, 3);
  const name = entry.slice(entry.indexOf(";") + 1);
  return \`\${code}: \${name}\`;
}

console.log(isChristmas("Happy Christmas, one and all!"));
console.log(fixCity("manCHESTer"));
console.log(stationLabel("MAN675847583748sjt567654;Manchester Piccadilly"));`,
    expose: ["isChristmas", "fixCity", "stationLabel"],
    hints: [
      "Each function needs a return. greeting.includes(\"Christmas\") is already true or false.",
      "lower[0].toUpperCase() is the first letter; lower.slice(1) is everything after it.",
      "entry.indexOf(\";\") finds the semicolon; slice from one past it.",
    ],
    checks: [
      { label: "isChristmas finds “Christmas”", test: ({ fns }) => fns.isChristmas("Merry Christmas to all") === true && fns.isChristmas("Happy birthday") === false },
      { label: "fixCity fixes the capitals", test: ({ fns }) => fns.fixCity("manCHESTer") === "Manchester" && fns.fixCity("BIRMINGHAM") === "Birmingham" && fns.fixCity("lOndon") === "London" },
      { label: "stationLabel builds “MAN: Manchester Piccadilly”", test: ({ fns }) => fns.stationLabel("MAN675847583748sjt567654;Manchester Piccadilly") === "MAN: Manchester Piccadilly" && fns.stationLabel("GNF576746573fhdg4737dh4;Greenfield") === "GNF: Greenfield" },
    ],
  });
'''
items += '''    { id: "q90", q: "What is 10 + 4 * 2?", opts: ["28", "18", "16"], a: 1, why: "* happens before +: 4 * 2 is 8, plus 10 is 18." },
    { id: "q91", q: "What is 17 % 5?", opts: ["3.4", "2", "3"], a: 1, why: "17 divided by 5 is 3 with 2 left over." },
    { id: "q92", q: "\\"Royal Arch\\".slice(0, 5) returns…", opts: ["\\"Royal\\"", "\\"Royal \\"", "\\"oyal \\""], a: 0, why: "Characters 0 to 4: the end index isn't included." },
    { id: "q93", q: "\\"Mesa\\".indexOf(\\"x\\") returns…", opts: ["0", "undefined", "-1"], a: 2, why: "-1 means not found." },
'''
write("core-numbers-strings.html", h, b, "\n" + RUNNER + "<script>" + first + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_s + "\n" + ex_m + "</script>\n")
