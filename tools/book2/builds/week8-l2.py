import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-functions")
pg_follow = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">Arguments</span>', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Three ways')
pg_ways = '  <div class="ways" id="ways"></div>\n\n'
pg_scope = src.between('  <section class="playground even">\n    <pre class="snippet" id="scope-code">', '  <div class="section-title"><span class="eyebrow">Try it</span>')
rn_build = src.between('  <div class="runner"><textarea aria-label="Code editor">function greet(name = "friend")', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Functions", src.css(), """
  #dm-code { white-space: pre-wrap; }
  .msg-stage { position: relative; min-height: 160px; padding: 14px; border: 1px dashed var(--line); border-radius: 8px; display: grid; place-items: center; }
  .msg-box { width: min(100%, 320px); border-radius: 8px; color: #fff; background: #3a5a7a; padding: 12px 14px 12px 44px; position: relative; box-shadow: 0 4px 14px rgb(0 0 0 / 20%); }
  .msg-box.warning { background: #b5651d; }
  .msg-box.chat { background: #2e7d4f; }
  .msg-box::before { position: absolute; left: 14px; top: 11px; font-size: 1.2em; content: "i"; font-weight: 700; font-style: italic; font-family: Georgia, serif; }
  .msg-box.warning::before { content: "!"; font-style: normal; font-family: inherit; }
  .msg-box.chat::before { content: "…"; font-style: normal; }
  .msg-box p { margin: 0; padding-right: 20px; }
  .msg-box button { position: absolute; right: 8px; top: 6px; background: none; border: 0; color: inherit; font-size: 1.1em; cursor: pointer; }
""")
b = top("Functions", "A function is a named block of code you can run whenever you need it. You'll use the browser's built-in functions, write your own, pass values in and get values back.", [
  "Tell built-in functions, methods and your own functions apart, and call them.",
  "Use parameters, arguments and default parameters.",
  "Write anonymous and arrow functions, and pass functions to other functions.",
  "Return a value from a function and use it, and explain function scope.",
])
b += ST("Read", "Functions: reusable blocks of code") + src.between('  <div class="prose">\n    <p>A <span class="term">function</span>', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Follow the values')
b += ST("Read", "Built-in browser functions") + prose("""
    <p>You've been using functions since your first line of JavaScript. Every time you write something with parentheses after it, you're calling one:</p>
    <pre class="snippet" data-lang="js">const myText = "I am a string";
const newString = myText.replace("string", "sausage");   // "I am a sausage"

const myArray = ["I", "love", "chocolate", "frogs"];
const madeAString = myArray.join(" ");                   // "I love chocolate frogs"

const myNumber = Math.random();                          // between 0 and 1</pre>
    <p>These are built into the language or the browser. Someone wrote them once so you don't have to.</p>
    <h3>Functions versus methods</h3>
    <p>A function that belongs to an object is called a <span class="term">method</span>. <code>replace()</code> belongs to strings, <code>join()</code> to arrays, <code>random()</code> to the <code>Math</code> object. You'll learn more about objects in the next lesson. For now, a method is just a function you call with a dot in front of it.</p>
    <h3>Custom functions</h3>
    <p>The functions you write yourself, with the <code>function</code> keyword and a name of your choosing, are <b>custom functions</b>. <code>hikeTime()</code> above is one.</p>
    <h3>Invoking functions</h3>
    <p>Defining a function doesn't run it. You run it (call or <em>invoke</em> it) by writing its name followed by parentheses. You can call it as many times as you like.</p>""")
b += runner("""function myFunction() {
  console.log("hello");
}

myFunction();   // runs it
myFunction();   // and again
console.log(myFunction);   // no () — just refers to the function""")
b += ST("Read", "Function parameters") + prose("""
    <p>Some functions need information to do their job. <code>Math.random()</code> needs nothing; <code>myText.replace("string", "sausage")</code> needs two things: what to find and what to put in its place. Those values are <span class="term">arguments</span>; the names that receive them inside the definition are <span class="term">parameters</span>.</p>
    <h3>Optional parameters</h3>
    <p>Some built-in parameters are optional. <code>join()</code> without an argument uses a comma: <code>["a", "b"].join()</code> gives <code>"a,b"</code>.</p>
    <h3>Default parameters</h3>
    <p>In your own functions, you make a parameter optional by giving it a <span class="term" data-term="Parameter">default</span> with <code>=</code>:</p>""")
b += runner("""function hello(name = "Chris") {
  console.log(`Hello ${name}!`);
}

hello("Ari");   // Hello Ari!
hello();        // Hello Chris!""")
b += ST("Play", "Follow the values", "Change the arguments and follow each value through the function. Then try the two common mistakes.") + pg_follow
b += ST("Read", "Anonymous functions and arrow functions") + prose("""
    <p>A function doesn't need a name. An <span class="term">anonymous function</span> is usually passed straight into another function that will call it later. Here, <code>addEventListener()</code> calls it whenever a key is pressed:</p>
    <pre class="snippet" data-lang="js">textBox.addEventListener("keydown", function (event) {
  console.log(`You pressed "${event.key}".`);
});</pre>
    <p>An <span class="term">arrow function</span> is a shorter way to write the same thing: drop <code>function</code> and put <code>=&gt;</code> after the parameters:</p>
    <pre class="snippet" data-lang="js">textBox.addEventListener("keydown", (event) =&gt; {
  console.log(`You pressed "${event.key}".`);
});</pre>
    <p>With exactly one parameter, the parentheses are optional. If the body is a single <code>return</code> line, the braces and the word <code>return</code> can go too:</p>""")
b += runner("""const originals = [1, 2, 3];

const doubled = originals.map(function (item) {
  return item * 2;
});
const doubledArrow = originals.map((item) => item * 2);

console.log(doubled);
console.log(doubledArrow);""")
b += ST("Look", "Three ways to write a function", "All three do the same thing. You'll see all of them in code online. MDN recommends arrow functions for short functions, especially ones you pass to another function.") + pg_ways
b += ST("Read", "Function scope and conflicts") + prose("""
    <p>Variables created inside a function only exist inside it: that's the function's <span class="term">scope</span>. Code outside can't see them. Variables declared outside every function are in the <span class="term" data-term="Scope">global scope</span> and can be seen everywhere.</p>
    <p>That's useful. If two scripts on the same page both had a global <code>name</code>, one would overwrite the other. Inside functions, each can have its own <code>total</code> or <code>name</code> without clashing.</p>""")
b += ST("Play", "Scope: where can a variable be seen?", "Click a cell to try using that variable from that place.") + pg_scope
b += ST("Read", "Build your own function") + prose("""
    <p>MDN's walkthrough builds a <code>displayMessage()</code> function that pops up a message box. It starts with no parameters, always showing the same text, then gains a <code>msgText</code> parameter for the message and a <code>msgType</code> parameter for the style. That's the general pattern: get it working for one case, then turn whatever changes into a parameter.</p>
    <pre class="snippet" data-lang="js">function displayMessage(msgText, msgType) {
  const panel = document.createElement("div");
  panel.setAttribute("class", "msg-box");
  html.appendChild(panel);

  const msg = document.createElement("p");
  msg.textContent = msgText;
  panel.appendChild(msg);
  // … a close button, and a class for msgType
}

btn.addEventListener("click", () =&gt; displayMessage("Brr, it's cold!", "warning"));</pre>
    <p>Notice the last line: <code>addEventListener</code> needs a function to call later, so you wrap the call in an arrow function. Writing <code>displayMessage(…)</code> directly would run it immediately.</p>""")
b += ST("Play", "displayMessage()", "Fill in the two arguments and call the function.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="dm-text">msgText</label><input class="text-in" id="dm-text" type="text" value="Your inbox is almost full"></div>
      <div class="control"><label for="dm-type">msgType</label><select id="dm-type"><option value="">(none)</option><option value="warning" selected>warning</option><option value="chat">chat</option></select></div>
      <button class="btn run" type="button" id="dm-go">Call displayMessage()</button>
    </div>
    <div class="stage-col">
      <pre class="snippet" id="dm-code" data-lang="js"></pre>
      <div class="msg-stage" id="dm-stage"><p class="hint">Nothing shown yet.</p></div>
    </div>
  </section>

"""
b += ST("Try it", "Write your own", "Change the arguments, add a default, or write a new function that calls these.") + rn_build
b += ST("Read", "Function return values") + prose("""
    <h3>What are return values?</h3>
    <p>Some functions hand a value back when they finish: <code>myText.replace("string", "sausage")</code> returns the new string, which you can store in a variable. Others, like <code>displayMessage()</code>, just do something and return nothing (strictly, they return <code>undefined</code>).</p>
    <h3>Using return values in your own functions</h3>
    <p>Use the <code>return</code> keyword. It sends a value back to the place the function was called, and ends the function there. That value can be stored, printed or passed straight into another function:</p>""")
b += runner("""function squared(num) {
  return num * num;
}

function cubed(num) {
  return num * num * num;
}

function factorial(num) {
  if (num < 0) return undefined;
  if (num === 0) return 1;
  let x = num - 1;
  while (x > 1) {
    num *= x;
    x--;
  }
  return num;
}

const input = "5";
if (isNaN(input)) {
  console.log("Please enter a number.");
} else {
  console.log(`${input} squared is ${squared(input)}.`);
  console.log(`${input} cubed is ${cubed(input)}.`);
  console.log(`${input} factorial is ${factorial(input)}.`);
}""")
b += prose("""
    <p><code>isNaN()</code> ("is Not a Number") is another built-in: it returns <code>true</code> if its argument can't be turned into a number. Try changing <code>input</code> to <code>"hello"</code>.</p>""")
b += ST("Practice", "Write functions that return", "Fix a function that forgets to return, give it a default, and write a second one as an arrow function.") + '  <div id="ex-func"></div>\n\n'
b += ST("Practice", "Functions that use functions", "Write small functions that each do one job, then combine them.") + '  <div id="ex-math"></div>\n\n'
b += notes([
  "A function is a named, reusable block of code. A method is a function that belongs to an object.",
  "<b>Parameters</b> are the names in the definition; <b>arguments</b> are the values you pass in.",
  "Default parameters fill in missing arguments: <code>function greet(name = \"friend\")</code>.",
  "Anonymous and arrow functions are often passed to other functions, like <code>map()</code> or <code>addEventListener()</code>.",
  "<code>return</code> sends a value back and ends the function. Variables declared inside a function stay inside it.",
], [
  "Using <code>console.log()</code> where you meant <code>return</code>. The value is printed, but the caller gets <code>undefined</code>.",
  "Passing a call instead of a function: <code>btn.addEventListener(\"click\", go())</code> runs <code>go</code> right away.",
  "Using a variable declared inside a function from outside it: <code>ReferenceError</code>.",
  "Putting code after <code>return</code> and expecting it to run.",
])
first, items = split_quiz(src.first_script())
js = r'''
  // --- displayMessage ---
  function dmCall() {
    const text = $("dm-text").value, type = $("dm-type").value;
    $("dm-code").textContent = type ? `displayMessage("${text}", "${type}");` : `displayMessage("${text}");`;
    const stage = $("dm-stage");
    stage.innerHTML = "";
    const panel = document.createElement("div");
    panel.setAttribute("class", "msg-box" + (type ? " " + type : ""));
    stage.appendChild(panel);
    const msg = document.createElement("p");
    msg.textContent = text;
    panel.appendChild(msg);
    const closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.textContent = "×";
    closeBtn.setAttribute("aria-label", "Close message");
    panel.appendChild(closeBtn);
    closeBtn.addEventListener("click", () => { stage.innerHTML = '<p class="hint">Closed. Call it again.</p>'; });
  }
  $("dm-go").addEventListener("click", dmCall);
  ["dm-text", "dm-type"].forEach((id) => $(id).addEventListener("input", () => {
    const text = $("dm-text").value, type = $("dm-type").value;
    $("dm-code").textContent = type ? `displayMessage("${text}", "${type}");` : `displayMessage("${text}");`;
  }));
  $("dm-type").dispatchEvent(new Event("input"));
'''
ex_f = src.block('  makeExercise(document.getElementById("ex-func"), {')
ex_m = r'''  makeExercise(document.getElementById("ex-math"), {
    title: "Squares, cubes and a label",
    task: `<ol>
      <li>Write <code>squared(num)</code> and <code>cubed(num)</code>, each returning the result.</li>
      <li>Write <code>describe(num, power = "squared")</code>. It returns <code>"3 squared is 9"</code>, or <code>"3 cubed is 27"</code> when <code>power</code> is <code>"cubed"</code>. Call your other two functions to get the numbers.</li>
      <li>If <code>num</code> isn't a number (use <code>isNaN()</code>), <code>describe</code> returns <code>"Please enter a number"</code>.</li>
    </ol>`,
    js: `function squared(num) {
  console.log(num * num);
}

// cubed

// describe

console.log(squared(3));`,
    solution: `function squared(num) {
  return num * num;
}

function cubed(num) {
  return num * num * num;
}

function describe(num, power = "squared") {
  if (isNaN(num)) {
    return "Please enter a number";
  }
  const result = power === "cubed" ? cubed(num) : squared(num);
  return \`\${num} \${power} is \${result}\`;
}

console.log(describe(3));
console.log(describe(3, "cubed"));`,
    expose: ["squared", "cubed", "describe"],
    hints: [
      "squared logs its answer but doesn't return it. Swap console.log for return.",
      "The default goes in the parameter list: function describe(num, power = \"squared\").",
      "Return early: if (isNaN(num)) { return \"Please enter a number\"; }",
    ],
    checks: [
      { label: "squared(4) returns 16 and cubed(2) returns 8", test: ({ fns }) => fns.squared(4) === 16 && typeof fns.cubed === "function" && fns.cubed(2) === 8 },
      { label: "describe(3) returns “3 squared is 9”", test: ({ fns }) => typeof fns.describe === "function" && fns.describe(3) === "3 squared is 9" },
      { label: "describe(3, \"cubed\") returns “3 cubed is 27”", test: ({ fns }) => typeof fns.describe === "function" && fns.describe(3, "cubed") === "3 cubed is 27" },
      { label: "describe(\"hello\") asks for a number", test: ({ fns }) => typeof fns.describe === "function" && fns.describe("hello") === "Please enter a number" },
    ],
  });
'''
items += '''    { id: "q90", q: "Which of these is a method?", opts: ["alert()", "myArray.join()", "function go() {}"], a: 1, why: "join() belongs to arrays, so it's called with a dot: a method." },
    { id: "q91", q: "What does a function with no return statement return?", opts: ["0", "null", "undefined"], a: 2, why: "Without return, the caller gets undefined." },
'''
write("core-functions.html", h, b, "\n" + RUNNER + "<script>" + first + js + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_f + "\n" + ex_m + "</script>\n")
