import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-arrays")
pg = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="item">', '  <div class="section-title"><span class="eyebrow">Try it</span>')
rnd = src.between('  <div class="runner"><textarea aria-label="Code editor">const names = [', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Arrays", src.css())
b = top("Arrays", "When you have a list of related values, like every trail in a guide, an array keeps them in order under one name. You can read any item, add and remove items, loop through them all, and convert between arrays and strings.", [
  "Create arrays, read their length, and read or change items by index.",
  "Add and remove items with <code>push</code>, <code>pop</code>, <code>unshift</code>, <code>shift</code> and <code>splice</code>.",
  "Do something with every item using <code>for...of</code>, <code>map()</code> and <code>filter()</code>.",
  "Convert between strings and arrays with <code>split()</code> and <code>join()</code>.",
])
b += ST("Read", "What is an array?") + prose("""
    <p>An <span class="term">array</span> is a single variable that stores a list of values, in order. Instead of <code>trail1</code>, <code>trail2</code>, <code>trail3</code>, you have one <code>trails</code> list that can hold three items or three thousand, and code that works the same either way.</p>""")
b += ST("Read", "Creating arrays") + prose("""
    <p>Put the items in square brackets, separated by commas. An array can hold any type, a mix of types, or even other arrays:</p>""")
b += runner("""const trails = ["Mesa", "Royal Arch", "Chautauqua"];
const miles = [6.7, 3.4, 1.2];
const mixed = ["Mesa", 6.7, true];
const nested = [["Mesa", 6.7], ["Royal Arch", 3.4]];

console.log(trails);
console.log(trails.length);       // how many items
console.log(nested[1][0]);        // item 0 of item 1""")
b += ST("Read", "Finding the length of an array") + prose("""
    <p><code>trails.length</code> is the number of items. It's a property, so no parentheses.</p>""")
b += ST("Read", "Accessing and modifying array items") + prose("""
    <p>Each item has an <span class="term">index</span>, its position, counted from 0. So the first item is <code>trails[0]</code> and the last is <code>trails[trails.length - 1]</code>. Asking for an index that doesn't exist gives <code>undefined</code>, not an error. To change an item, assign to its index: <code>trails[1] = "Flagstaff"</code>. For an array inside an array, use two indexes: <code>nested[1][0]</code>.</p>""")
b += ST("Read", "Finding the index of items in an array") + prose("""
    <p><code>indexOf("Royal Arch")</code> returns an item's position, or <code>-1</code> if it isn't in the array. <code>includes("Mesa")</code> just answers <code>true</code> or <code>false</code>.</p>""")
b += ST("Read", "Adding items") + prose("""
    <p><code>push()</code> adds one or more items to the end; <code>unshift()</code> adds them to the start. Both change the array, and return its new length.</p>""")
b += ST("Read", "Removing items") + prose("""
    <p><code>pop()</code> removes the last item and <code>shift()</code> removes the first; both return the item they removed. To remove from the middle, find the index and use <code>splice(index, howMany)</code>:</p>
    <pre class="snippet" data-lang="js">const index = trails.indexOf("Royal Arch");
if (index !== -1) {
  trails.splice(index, 1);   // remove 1 item at that index
}</pre>
    <p>Some methods change the array itself (<code>push</code>, <code>pop</code>, <code>splice</code>); others leave it alone and hand you an answer (<code>includes</code>, <code>indexOf</code>, <code>slice</code>, <code>join</code>). Knowing which kind you're using saves a lot of confusion.</p>""")
b += ST("Play", "Change the array", "Try each method and watch which ones change the array and which just return a value.") + pg
b += ST("Read", "Accessing every item") + prose("""
    <p>Often you want to do something with every item. A <code>for...of</code> loop runs its code once per item:</p>""")
b += runner("""const trails = ["Mesa", "Royal Arch", "Chautauqua"];

for (const trail of trails) {
  console.log(`Hike the ${trail} trail`);
}""")
b += prose("""
    <p>Two methods build a new array from an old one. <code>map()</code> runs a function on every item and collects the results. <code>filter()</code> keeps only the items for which a function returns <code>true</code>. You'll learn more about the functions inside them in <a href="core-loops.html">Loops</a> and <a href="core-functions.html">Functions</a>.</p>""")
b += runner("""const miles = [6.7, 3.4, 1.2, 8.1];

const km = miles.map((m) => (m * 1.609).toFixed(1));
console.log(km);

const long = miles.filter((m) => m > 5);
console.log(long);
console.log(miles);   // unchanged""")
b += ST("Read", "Converting between strings and arrays") + prose("""
    <p><code>split()</code> breaks a string into an array at a separator. <code>join()</code> does the opposite, joining items with a separator you choose. (<code>toString()</code> also joins, but always with commas.)</p>""")
b += runner("""const data = "Mesa,Royal Arch,Chautauqua,Bear Peak";
const trails = data.split(",");
console.log(trails);
console.log(trails.length);

console.log(trails.join(" · "));
console.log(trails.toString());""")
b += ST("Try it", "Pick something at random", "<code>Math.random()</code> gives a number from 0 up to 1. Multiply it by the length and round down to get a valid index.") + rnd
b += ST("Practice", "Change the list", "Add and remove trails with array methods, then read from the end of the list.") + '  <div id="ex-arrays"></div>\n\n'
b += ST("Practice", "Printing those products", "From MDN's arrays lesson: turn \"name:price\" strings into receipt lines and a total.") + '  <div id="ex-products"></div>\n\n'
b += ST("Practice", "Storing the previous 5 searches", "Keep a search history with the newest first, and never more than five items.") + '  <div id="ex-history"></div>\n\n'
b += notes([
  "An array is an ordered list under one name: <code>[\"Mesa\", \"Royal Arch\"]</code>. <code>length</code> is how many items.",
  "Indexes start at 0; the last item is at <code>length - 1</code>. <code>indexOf()</code> returns <code>-1</code> when not found.",
  "<code>push</code>/<code>pop</code> work at the end, <code>unshift</code>/<code>shift</code> at the start, <code>splice</code> in the middle.",
  "<code>for...of</code> visits every item; <code>map()</code> transforms them; <code>filter()</code> keeps some.",
  "<code>split()</code> turns a string into an array; <code>join()</code> turns an array into a string.",
], [
  "Reading <code>trails[trails.length]</code> for the last item. It's <code>length - 1</code>.",
  "Expecting <code>slice()</code> or <code>map()</code> to change the original array.",
  "Calling <code>splice(index, 1)</code> when <code>indexOf</code> returned <code>-1</code>, which removes the last item.",
  "Forgetting that a <code>const</code> array can still be changed with <code>push</code> and <code>pop</code>.",
])
first, items = split_quiz(src.first_script())
ex_a = src.block('  makeExercise(document.getElementById("ex-arrays"), {')
ex_p = r'''  makeExercise(document.getElementById("ex-products"), {
    title: "A receipt",
    task: `<ol>
      <li><code>formatProduct(entry)</code> takes text like <code>"Underpants:6.99"</code>. Split it at the <code>:</code> and return <code>"Underpants: $6.99"</code>.</li>
      <li><code>totalPrice(products)</code> takes an array of those strings. Loop through it with <code>for...of</code>, add up the prices (convert them with <code>Number()</code>), and return <code>"Total: $"</code> followed by the total with two decimal places.</li>
    </ol>`,
    js: `const products = ["Underpants:6.99", "Socks:5.99", "T-shirt:14.99", "Trousers:31.99", "Shoes:23.99"];

function formatProduct(entry) {
  // split(":") gives [name, price]
}

function totalPrice(products) {
  let total = 0;
  // for...of, split, Number, +=
  return "Total: $" + total;
}

for (const p of products) console.log(formatProduct(p));
console.log(totalPrice(products));`,
    solution: `const products = ["Underpants:6.99", "Socks:5.99", "T-shirt:14.99", "Trousers:31.99", "Shoes:23.99"];

function formatProduct(entry) {
  const parts = entry.split(":");
  return \`\${parts[0]}: $\${parts[1]}\`;
}

function totalPrice(products) {
  let total = 0;
  for (const p of products) {
    const parts = p.split(":");
    total += Number(parts[1]);
  }
  return "Total: $" + total.toFixed(2);
}

for (const p of products) console.log(formatProduct(p));
console.log(totalPrice(products));`,
    expose: ["formatProduct", "totalPrice"],
    hints: [
      "entry.split(\":\") returns an array: item 0 is the name, item 1 the price.",
      "Inside the loop: total += Number(parts[1]);",
      "total.toFixed(2) gives two decimal places.",
    ],
    checks: [
      { label: "formatProduct makes “Underpants: $6.99”", test: ({ fns }) => fns.formatProduct("Underpants:6.99") === "Underpants: $6.99" && fns.formatProduct("Hat:12.5") === "Hat: $12.5" },
      { label: "totalPrice adds up the prices", test: ({ fns }) => fns.totalPrice(["Underpants:6.99", "Socks:5.99", "T-shirt:14.99", "Trousers:31.99", "Shoes:23.99"]) === "Total: $83.95" },
      { label: "The total always has two decimals", test: ({ fns }) => fns.totalPrice(["A:1.5", "B:2.5"]) === "Total: $4.00" && fns.totalPrice([]) === "Total: $0.00" },
    ],
  });

  makeExercise(document.getElementById("ex-history"), {
    title: "Search history",
    task: `<p><code>addSearch(history, term)</code> receives the history array and a new search term.</p>
    <ol>
      <li>Add <code>term</code> to the <strong>start</strong> of the array, so the newest search is first.</li>
      <li>If the array now has more than 5 items, remove the last (oldest) one.</li>
      <li>Return the array.</li>
    </ol>`,
    js: `function addSearch(history, term) {
  // unshift, then maybe pop
  return history;
}

const history = [];
for (const t of ["Mesa", "Royal Arch", "Bear Peak", "Sanitas", "Flagstaff", "Green Mountain"]) {
  addSearch(history, t);
}
console.log(history);`,
    solution: `function addSearch(history, term) {
  history.unshift(term);
  if (history.length > 5) {
    history.pop();
  }
  return history;
}

const history = [];
for (const t of ["Mesa", "Royal Arch", "Bear Peak", "Sanitas", "Flagstaff", "Green Mountain"]) {
  addSearch(history, t);
}
console.log(history);`,
    expose: ["addSearch"],
    hints: [
      "unshift() adds to the start; pop() removes from the end.",
      "if (history.length > 5) { history.pop(); }",
    ],
    checks: [
      { label: "The newest search goes first", test: ({ fns }) => fns.addSearch(["Mesa"], "Royal Arch").join() === "Royal Arch,Mesa" },
      { label: "Never more than 5 items", test: ({ fns }) => { const h = []; for (const t of "abcdefgh") fns.addSearch(h, t); return h.length === 5; } },
      { label: "The oldest item is the one dropped", test: ({ fns }) => { const h = []; for (const t of "abcdef") fns.addSearch(h, t); return h.join("") === "fedcb"; } },
    ],
  });
'''
items += '''    { id: "q90", q: "const t = [\\"Mesa\\", \\"Arch\\"]; t.unshift(\\"Sanitas\\"); What is t[0]?", opts: ["\\"Mesa\\"", "\\"Sanitas\\"", "\\"Arch\\""], a: 1, why: "unshift adds to the start." },
    { id: "q91", q: "[6.7, 3.4, 8.1].filter((m) => m > 5) returns…", opts: ["[6.7, 8.1]", "[true, false, true]", "2"], a: 0, why: "filter keeps the items where the function returns true." },
    { id: "q92", q: "\\"a-b-c\\".split(\\"-\\").join(\\"+\\") gives…", opts: ["\\"a+b+c\\"", "[\\"a\\", \\"b\\", \\"c\\"]", "\\"a-b-c\\""], a: 0, why: "split makes an array, join glues it back with +." },
'''
write("core-arrays.html", h, b, "\n" + RUNNER + "<script>" + first + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_a + "\n" + ex_p + "</script>\n")
