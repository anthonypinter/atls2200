  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

  makeExercise(document.getElementById("ex-describe"), {
    title: "Describe a trail",
    task: `<ol>
      <li>Store the trail's name, <code>"Mesa Trail"</code>, in <code>trailName</code>, and its length, <code>6.7</code>, in <code>miles</code>. Neither will change, so declare them that way.</li>
      <li>Store a visit count of <code>0</code> in <code>visits</code>, a variable that <em>can</em> change. Then add 1 to it twice.</li>
      <li>Log this sentence, built with a template literal from the three variables: <code>Mesa Trail is 6.7 miles. Visits: 2</code></li>
    </ol>`,
    js: `// Your code here
`,
    expose: ["trailName", "miles", "visits"],
    hints: [
      "const for values that never change; let for ones that do.",
      "visits++ (or visits += 1) adds 1.",
      "A template literal uses backticks, and \${name} drops a variable in.",
    ],
    checks: [
      { label: "trailName and miles hold the right values, with const", test: ({ fns, code }) => fns.trailName === "Mesa Trail" && fns.miles === 6.7 && /const\s+trailName\b/.test(code.js) && /const\s+miles\b/.test(code.js) },
      { label: "visits is a let that ends at 2", test: ({ fns, code }) => fns.visits === 2 && /let\s+visits\s*=\s*0\b/.test(code.js) },
      { label: "Logs “Mesa Trail is 6.7 miles. Visits: 2”", test: ({ logs }) => logs.includes("Mesa Trail is 6.7 miles. Visits: 2") },
      { label: "The sentence is a template literal using all three variables", test: ({ code }) => /`[^`]*\$\{\s*trailName\s*\}[^`]*\$\{\s*miles\s*\}[^`]*\$\{\s*visits\s*\}[^`]*`/.test(code.js) },
    ],
  });

  makeExercise(document.getElementById("ex-strings"), {
    title: "Tidy up titles",
    task: `<ol>
      <li><code>slugify(title)</code> turns a title into a web address part: trim the spaces at the ends, make it lowercase, and replace each space with a hyphen. <code>slugify("  Royal Arch Trail ")</code> returns <code>"royal-arch-trail"</code>.</li>
      <li><code>shorten(title, max)</code> returns the title unchanged if it's <code>max</code> characters or fewer. Otherwise it returns the first <code>max</code> characters followed by <code>"…"</code>. <code>shorten("Green Mountain West Ridge", 14)</code> returns <code>"Green Mountain…"</code>.</li>
    </ol>`,
    js: `function slugify(title) {
  // Your code here
}

function shorten(title, max) {
  // Your code here
}

console.log(slugify("  Royal Arch Trail "));
console.log(shorten("Green Mountain West Ridge", 14));
console.log(shorten("Mesa", 14));
`,
    expose: ["slugify", "shorten"],
    hints: [
      "Strings have trim(), toLowerCase() and replaceAll(\" \", \"-\"). Each returns a new string, so chain them.",
      "title.length is how many characters it has.",
      "title.slice(0, max) is the first max characters.",
    ],
    checks: [
      { label: "slugify(\"  Royal Arch Trail \") is \"royal-arch-trail\"", test: ({ fns }) => fns.slugify("  Royal Arch Trail ") === "royal-arch-trail" },
      { label: "slugify(\"MESA\") is \"mesa\"", test: ({ fns }) => fns.slugify("MESA") === "mesa" && fns.slugify("Bear Peak") === "bear-peak" },
      { label: "shorten cuts long titles and adds …", test: ({ fns }) => fns.shorten("Green Mountain West Ridge", 14) === "Green Mountain…" && fns.shorten("Flagstaff Summit", 4) === "Flag…" },
      { label: "shorten leaves short titles alone", test: ({ fns }) => fns.shorten("Mesa", 14) === "Mesa" && fns.shorten("Royal Arch", 10) === "Royal Arch" },
    ],
  });

  makeExercise(document.getElementById("ex-arrays"), {
    title: "Filter and label",
    task: `<ol>
      <li><code>longOnes(distances)</code> returns a new array of just the distances over <code>5</code>, using <code>filter()</code>. The original array must not change.</li>
      <li><code>withUnits(distances)</code> returns a new array of strings like <code>"6.7 mi"</code>, using <code>map()</code>.</li>
      <li><code>lastOf(list)</code> returns the last item of any array, using its <code>length</code>.</li>
    </ol>`,
    js: `function longOnes(distances) {
  // Your code here
}

function withUnits(distances) {
  // Your code here
}

function lastOf(list) {
  // Your code here
}

const distances = [6.7, 3.4, 4.1, 12.2, 5];
console.log(longOnes(distances));
console.log(withUnits(distances));
console.log(lastOf(distances));
`,
    expose: ["longOnes", "withUnits", "lastOf"],
    hints: [
      "distances.filter((d) => d > 5) keeps the items for which the function returns true.",
      "distances.map((d) => d + \" mi\") makes a new array from what the function returns.",
      "Indexes start at 0, so the last item is list[list.length - 1].",
    ],
    checks: [
      { label: "longOnes([6.7, 3.4, 4.1, 12.2, 5]) is [6.7, 12.2]", test: ({ fns }) => same(fns.longOnes([6.7, 3.4, 4.1, 12.2, 5]), [6.7, 12.2]) },
      { label: "longOnes uses filter() and doesn't change the original", test: ({ fns, code }) => { const a = [8, 1]; fns.longOnes(a); return same(a, [8, 1]) && /\.filter\(/.test(code.js); } },
      { label: "withUnits([6.7, 3.4]) is [\"6.7 mi\", \"3.4 mi\"], using map()", test: ({ fns, code }) => same(fns.withUnits([6.7, 3.4]), ["6.7 mi", "3.4 mi"]) && /\.map\(/.test(code.js) },
      { label: "lastOf returns the last item", test: ({ fns }) => fns.lastOf([1, 2, 3]) === 3 && fns.lastOf(["Mesa"]) === "Mesa" },
    ],
  });

  makeExercise(document.getElementById("ex-decide"), {
    title: "Should we go?",
    task: `<ol>
      <li><code>difficulty(gain)</code> takes a climb in feet and returns <code>"easy"</code> under 500, <code>"moderate"</code> from 500 up to (not including) 1500, and <code>"hard"</code> from 1500 up.</li>
      <li><code>goHiking(weather, hasJacket)</code> returns <code>true</code> or <code>false</code>: go when it's <code>"sunny"</code>; go in <code>"rain"</code> only with a jacket; never go in a <code>"storm"</code>; and for any other weather, don't go. Use a <code>switch</code> statement.</li>
    </ol>`,
    js: `function difficulty(gain) {
  // Your code here
}

function goHiking(weather, hasJacket) {
  // Your code here
}

console.log(difficulty(300), difficulty(500), difficulty(1500));
console.log(goHiking("rain", true), goHiking("storm", true));
`,
    expose: ["difficulty", "goHiking"],
    hints: [
      "Check from one end: if (gain < 500) … else if (gain < 1500) … else …",
      "switch (weather) { case \"sunny\": return true; … default: return false; }",
      "In the rain case, return hasJacket itself.",
    ],
    checks: [
      { label: "difficulty: 0 and 499 are easy", test: ({ fns }) => fns.difficulty(0) === "easy" && fns.difficulty(499) === "easy" },
      { label: "difficulty: 500 and 1499 are moderate, 1500 and up are hard", test: ({ fns }) => fns.difficulty(500) === "moderate" && fns.difficulty(1499) === "moderate" && fns.difficulty(1500) === "hard" && fns.difficulty(4000) === "hard" },
      { label: "goHiking: sunny yes, storm no, other weather no", test: ({ fns }) => fns.goHiking("sunny", false) === true && fns.goHiking("storm", true) === false && fns.goHiking("fog", true) === false },
      { label: "goHiking: rain only with a jacket, using switch", test: ({ fns, code }) => fns.goHiking("rain", true) === true && fns.goHiking("rain", false) === false && /switch\s*\(/.test(code.js) },
    ],
  });

  makeQuiz(document.getElementById("quiz"), [
    { id: "q1", q: "What does defer do on <script src=\"app.js\" defer>?", opts: ["Runs the script only on click", "Downloads it while the page loads, and runs it after the HTML has been parsed", "Skips the script on slow connections", "Runs it before anything else"], a: 1, why: "With defer, the script can safely use the page's elements, and it doesn't block the HTML from loading." },
    { id: "q2", q: "Your code runs with no errors, but the total comes out wrong. What kind of error is that?", opts: ["Syntax error", "Logic error", "Runtime error", "Network error"], a: 1, why: "A logic error does what you wrote, not what you meant. The console can't spot it; console.log and the debugger help." },
    { id: "q3", q: "The console shows: TypeError: trails.push is not a function. What's most likely?", opts: ["push is spelled wrong in JavaScript", "trails isn't an array (maybe a string, or undefined)", "There's a missing semicolon", "The array is full"], a: 1, why: "A TypeError means a value isn't the type the code expects. Log trails to see what it really is." },
    { id: "q4", q: "What happens when you run: const max = 5; max = 6;", opts: ["max becomes 6", "Nothing", "TypeError: Assignment to constant variable", "max becomes [5, 6]"], a: 2, why: "A const can't be reassigned. Use let for a variable whose value changes." },
    { id: "q5", q: "What is \"5\" + 3?", opts: ["8", "\"53\"", "NaN", "Error"], a: 1, why: "With a string on either side, + joins strings. Convert first with Number(\"5\") to add." },
    { id: "q6", q: "What is 17 % 5?", opts: ["3.4", "2", "3", "85"], a: 1, why: "% gives the remainder: 17 is 3 × 5 with 2 left over." },
    { id: "q7", q: "Why prefer === over ==?", opts: ["=== is faster to type", "=== doesn't convert types first, so \"1\" === 1 is false", "== doesn't work on numbers", "=== also compares variable names"], a: 1, why: "== converts types before comparing, which gives surprises like \"\" == 0 being true." },
    { id: "q8", q: "Which of these is truthy?", opts: ["0", "\"\" (an empty string)", "\"0\" (a string with a zero in it)", "null"], a: 2, why: "Any non-empty string is truthy, even \"0\". The falsy values are false, 0, \"\", null, undefined and NaN." },
    { id: "q9", q: "const trails = [\"Mesa\", \"Bear Peak\", \"Royal Arch\"]; What is trails[3]?", opts: ["\"Royal Arch\"", "undefined", "An error", "\"Mesa\""], a: 1, why: "Indexes are 0, 1 and 2. Reading past the end gives undefined, not an error." },
    { id: "q10", q: "What does const label = miles > 5 ? \"long\" : \"short\"; set when miles is 5?", opts: ["\"long\"", "\"short\"", "true", "undefined"], a: 1, why: "5 > 5 is false, so the ternary takes the value after the colon." },
  ], { once: true });
