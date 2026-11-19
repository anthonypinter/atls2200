import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-intro")
pg_layers = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">Layers</span>', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Where does the script tag go?')
pg_place = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="place">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("What is JavaScript?", src.css(), """
  .gg { display: grid; gap: 10px; justify-items: start; background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: 8px; padding: 16px; font-family: var(--font-body); }
  .gg h4 { margin: 0; font: 800 1.2rem var(--font-display); }
  .gg form { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
  .gg input { font: inherit; padding: 6px 8px; width: 6em; border: 1.5px solid #c9cedb; border-radius: 6px; }
  .gg .guesses, .gg .last, .gg .hilo { margin: 0; }
  .gg .last.right { background: #0b6b5e; color: #fff; padding: 2px 8px; border-radius: 4px; }
  .gg .last.wrong { background: #b42318; color: #fff; padding: 2px 8px; border-radius: 4px; }
""")
b = top("What is JavaScript?", "HTML gives a page its structure, CSS gives it style, and JavaScript gives it behavior. Here's what JavaScript can do, how it runs in the browser, how to add it to a page, and a first look at a small program.", [
  "Describe what HTML, CSS and JavaScript each add to a page.",
  "Explain how the browser runs JavaScript: in its own tab, top to bottom.",
  "Add JavaScript to a page with a script tag, and choose a loading strategy.",
  "Break a small program into steps, the way a programmer does.",
])
b += ST("Read", "A high-level definition") + prose("""
    <p>JavaScript is a programming language that lets you make web pages do things: update content as you watch, show a map you can drag around, animate graphics, check a form before it's sent. It's the third layer of the web's layer cake:</p>
    <ul>
      <li><span class="term">HTML</span> gives the page structure and meaning: a heading, a paragraph, a button.</li>
      <li><span class="term">CSS</span> styles it: colors, fonts, layout.</li>
      <li><span class="term">JavaScript</span> adds behavior: what happens when someone clicks the button.</li>
    </ul>
    <pre class="snippet" data-lang="js">const button = document.querySelector("button");

button.addEventListener("click", updateName);

function updateName() {
  const name = prompt("Enter a new name");
  button.textContent = `Player 1: ${name}`;
}</pre>
    <p>Each layer builds on the one before. JavaScript can't add behavior to a button that doesn't exist.</p>
    <div class="callout tip"><p class="callout-title">Tip</p><p>JavaScript has nothing to do with Java. The similar name was a marketing decision in 1995, and it has confused people ever since.</p></div>""")
b += ST("Play", "Peel back the layers", "Turn each layer off and on to see what it adds.") + pg_layers
b += ST("Read", "So what can it really do?") + prose("""
    <p>The core language gives you the basics of programming: store values in <strong>variables</strong>, do math and work with text, and run code when something happens (an <strong>event</strong>, like a click).</p>
    <p>On top of that, browsers provide <strong>APIs</strong>, ready-made toolkits you can use from JavaScript:</p>
    <ul>
      <li>The <strong>DOM API</strong> lets you change the HTML and CSS of the page, which is how pop-ups, menus and live updates work.</li>
      <li>The <strong>Geolocation API</strong> finds where the user is (with permission).</li>
      <li>The <strong>Canvas</strong> and <strong>WebGL</strong> APIs draw 2D and 3D graphics.</li>
      <li>Audio and video APIs play and record media.</li>
    </ul>
    <p>There are also third-party APIs from companies like map and payment services. This course stays with the core language and the DOM.</p>""")
b += ST("Read", "What is JavaScript doing on your page?") + prose("""
    <p>When a page loads, the browser reads the HTML, applies the CSS, and runs the JavaScript. The script can then keep changing the page while it's open.</p>
    <h3>Browser security</h3>
    <p>Each browser tab runs its code in its own separate environment. Code in one tab can't see or change another tab or another site, which stops a malicious site from reaching into your bank's tab.</p>
    <h3>JavaScript running order</h3>
    <p>The browser runs your code from top to bottom, one line at a time. So order matters: you can't use something before the line that creates it. Run this and read the error:</p>""")
b += runner("""console.log("Starting the trail list");
console.log(trail);       // used before it's created
const trail = "Mesa Trail";""")
b += prose("""
    <p>Swap the last two lines and run it again. Reading errors like this one is a skill you'll practise in <a href="core-troubleshooting-js.html">Troubleshooting JavaScript</a>.</p>
    <h3>Interpreted versus compiled code</h3>
    <p>Some languages are <em>compiled</em> into a program before they run. JavaScript is <em>interpreted</em>: the browser takes your code as text and runs it. (Modern browsers compile it on the fly behind the scenes to make it fast, but you never have to.)</p>
    <h3>Server-side versus client-side code</h3>
    <p>JavaScript in a web page is <strong>client-side</strong>: it runs in the visitor's browser. <strong>Server-side</strong> code runs on the web server before the page is sent. JavaScript can run on servers too, with Node.js, but this course is all client-side.</p>
    <h3>Dynamic versus static code</h3>
    <p>A <strong>static</strong> page shows the same content every time. A <strong>dynamic</strong> page can change what it shows, for example by building a list from data or updating a score. JavaScript is what makes a page dynamic in the browser.</p>""")
b += ST("Read", "How do you add JavaScript to your page?") + prose("""
    <p>JavaScript goes in a <code>&lt;script&gt;</code> element.</p>
    <h3>Internal JavaScript</h3>
    <p>You can write the code inside the element, usually just before <code>&lt;/body&gt;</code>, so the elements above it already exist when it runs.</p>
    <h3>External JavaScript</h3>
    <p>Usually, it's better to keep JavaScript in its own file, just as CSS has its own stylesheet, and link it from the <code>&lt;head&gt;</code>:</p>
    <pre class="snippet" data-lang="html">&lt;script defer src="script.js"&gt;&lt;/script&gt;</pre>
    <p>MDN's examples use <code>type="module"</code> instead of <code>defer</code>. Modules wait in the same way, but they only work when the page is served by a web server (GitHub Pages, or a local one like VS Code's Live Server), not when you double-click the file.</p>
    <h3>Inline JavaScript handlers</h3>
    <p>You'll see old code like <code>&lt;button onclick="createParagraph()"&gt;</code>. Don't do this: it mixes behavior into your HTML, and you'd have to add the attribute to every button by hand.</p>
    <h3>Using addEventListener instead</h3>
    <p>Keep the behavior in your script, and attach it from there. This finds every button and gives each one the same behavior:</p>
    <pre class="snippet" data-lang="js">const buttons = document.querySelectorAll("button");

for (const button of buttons) {
  button.addEventListener("click", createParagraph);
}</pre>
    <h3>Script loading strategies</h3>
    <p>The browser reads HTML from top to bottom. A plain <code>&lt;script src&gt;</code> in the head makes it stop, download and run the script <em>before</em> the body exists, so the script can't find the elements it needs. <span class="term">defer</span> (or <code>type="module"</code>) says: download now, but run after the whole page has been read. (<code>async</code> runs as soon as it's downloaded, in any order, which suits independent scripts like analytics.)</p>""")
b += ST("Play", "Where does the script tag go?", "Pick a placement and see what happens as the page loads.") + pg_place
b += ST("Read", "Comments") + prose("""
    <p>Comments are notes the browser ignores. Use them to explain <em>why</em> code does something:</p>""")
b += runner("""// A single-line comment: the browser skips this line

/*
  A multi-line comment.
  Good for a longer explanation.
*/

console.log("Comments don't run, but this does."); // a comment can go at the end of a line too""")
b += ST("Practice", "Your first lines of JavaScript", "Make the console say something. Press Run to see the output, then Check my work.") + '  <div id="ex-first"></div>\n\n'
b += ST("Read", "A first splash: thinking like a programmer") + prose("""
    <p>MDN's first project is a number guessing game. Before writing any code, a programmer breaks the idea into small steps:</p>
    <ol>
      <li>Pick a random number between 1 and 100.</li>
      <li>Let the player guess, and record each guess.</li>
      <li>Say whether the guess was right, too high or too low.</li>
      <li>After 10 wrong guesses, or a right one, end the game and offer to start again.</li>
    </ol>
    <p>Each step becomes a few lines of code using things you'll learn in the next few weeks: <strong>variables</strong> to store the number and the guesses, <strong>conditionals</strong> to compare them, a <strong>function</strong> to check each guess, and an <strong>event</strong> to run it when the button is clicked.</p>
    <pre class="snippet" data-lang="js">let randomNumber = Math.floor(Math.random() * 100) + 1;
let guessCount = 1;

function checkGuess() {
  const userGuess = Number(guessField.value);
  if (userGuess === randomNumber) {
    lastResult.textContent = "Congratulations! You got it right!";
  } else if (guessCount === 10) {
    lastResult.textContent = "!!!GAME OVER!!!";
  } else {
    lastResult.textContent = "Wrong!";
    lowOrHi.textContent = userGuess &lt; randomNumber ? "Last guess was too low!" : "Last guess was too high!";
  }
  guessCount++;
}

guessSubmit.addEventListener("click", checkGuess);</pre>""")
b += ST("Play", "Play the game", "This is that program, running. You don't need to understand every line yet.") + """  <div class="gg" id="gg">
    <h4>Number guessing game</h4>
    <p>I've picked a number between 1 and 100. You have 10 turns.</p>
    <form id="gg-form"><label for="gg-in">Enter a guess:</label><input id="gg-in" type="number" min="1" max="100" required><button class="btn run" id="gg-go">Submit guess</button></form>
    <p class="guesses" id="gg-guesses"></p>
    <p class="last" id="gg-last" aria-live="polite"></p>
    <p class="hilo" id="gg-hilo"></p>
    <button class="btn" type="button" id="gg-new" hidden>Start new game</button>
  </div>

"""
b += ST("Practice", "Check a guess", "Write the heart of the game: the function that compares a guess with the secret number.") + '  <div id="ex-guess"></div>\n\n'
b += notes([
  "HTML is structure, CSS is presentation, JavaScript is behavior.",
  "Browser APIs (like the DOM) let JavaScript change the page, draw graphics and more.",
  "Each tab runs its code separately, from top to bottom; you can't use something before it's created.",
  "Link scripts with <code>&lt;script defer src=\"script.js\"&gt;</code>, or <code>type=\"module\"</code> on a server.",
  "Attach behavior with <code>addEventListener</code>, not <code>onclick</code> attributes.",
], [
  "A plain <code>&lt;script src&gt;</code> in the head with no <code>defer</code>: the elements don't exist yet, so you get <code>null</code> errors.",
  "Writing <code>&lt;script src=\"script.js\" /&gt;</code>. A script tag always needs a closing <code>&lt;/script&gt;</code>.",
  "Expecting <code>type=\"module\"</code> to work from a double-clicked file.",
  "A wrong path in <code>src</code>: nothing happens, and the console shows a 404 for the file.",
])
first, items = split_quiz(src.first_script())
js = r'''
  // --- Number guessing game ---
  let ggNum, ggCount;
  function ggReset() {
    ggNum = Math.floor(Math.random() * 100) + 1; ggCount = 1;
    $("gg-guesses").textContent = ""; $("gg-last").textContent = ""; $("gg-last").className = "last"; $("gg-hilo").textContent = "";
    $("gg-in").disabled = false; $("gg-go").disabled = false; $("gg-new").hidden = true; $("gg-in").value = "";
  }
  function ggEnd() { $("gg-in").disabled = true; $("gg-go").disabled = true; $("gg-new").hidden = false; $("gg-new").focus(); }
  $("gg-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const g = Number($("gg-in").value);
    if (!g) return;
    if (ggCount === 1) $("gg-guesses").textContent = "Previous guesses:";
    $("gg-guesses").textContent += " " + g;
    if (g === ggNum) { $("gg-last").textContent = "Congratulations! You got it right!"; $("gg-last").className = "last right"; $("gg-hilo").textContent = ""; ggEnd(); }
    else if (ggCount === 10) { $("gg-last").textContent = `!!!GAME OVER!!! It was ${ggNum}.`; $("gg-last").className = "last wrong"; $("gg-hilo").textContent = ""; ggEnd(); }
    else { $("gg-last").textContent = "Wrong!"; $("gg-last").className = "last wrong"; $("gg-hilo").textContent = g < ggNum ? "Last guess was too low!" : "Last guess was too high!"; }
    ggCount++; $("gg-in").value = ""; $("gg-in").focus();
  });
  $("gg-new").addEventListener("click", ggReset);
  ggReset();
'''
ex_first = src.block('  makeExercise(document.getElementById("ex-first"), {')
ex_g = r'''  makeExercise(document.getElementById("ex-guess"), {
    title: "Too high, too low or correct",
    task: `<p><code>checkGuess(guess, target)</code> should return one of three messages. The first case is done for you.</p>
    <ol>
      <li>If the guess is bigger than the target, return <code>"Too high!"</code>.</li>
      <li>Otherwise, return <code>"Too low!"</code>.</li>
    </ol>`,
    js: `function checkGuess(guess, target) {
  if (guess === target) {
    return "Correct!";
  }
  // If guess is bigger than target, return "Too high!"

  // Otherwise, return "Too low!"

}

console.log(checkGuess(50, 50));
console.log(checkGuess(70, 50));
console.log(checkGuess(20, 50));`,
    solution: `function checkGuess(guess, target) {
  if (guess === target) {
    return "Correct!";
  }
  if (guess > target) {
    return "Too high!";
  }
  return "Too low!";
}

console.log(checkGuess(50, 50));
console.log(checkGuess(70, 50));
console.log(checkGuess(20, 50));`,
    expose: ["checkGuess"],
    hints: [
      "Copy the shape of the first if: if (guess > target) { return \"Too high!\"; }",
      "Once a return runs, the function stops, so the last line can just be return \"Too low!\";",
    ],
    checks: [
      { label: "A right guess returns “Correct!”", test: ({ fns }) => fns.checkGuess(42, 42) === "Correct!" },
      { label: "A guess that's too big returns “Too high!”", test: ({ fns }) => fns.checkGuess(90, 42) === "Too high!" && fns.checkGuess(43, 42) === "Too high!" },
      { label: "A guess that's too small returns “Too low!”", test: ({ fns }) => fns.checkGuess(1, 42) === "Too low!" && fns.checkGuess(41, 42) === "Too low!" },
    ],
  });
'''
items += '''    { id: "q5", q: "This code logs an error: console.log(trail); const trail = \\"Mesa\\"; Why?", opts: ["Strings can't be logged", "JavaScript runs top to bottom, so trail doesn't exist yet", "const can't hold text"], a: 1, why: "You can't use a variable before the line that creates it." },
    { id: "q6", q: "Where does client-side JavaScript run?", opts: ["On the web server", "In the visitor's browser", "In the code editor"], a: 1, why: "Client-side code runs in the browser; server-side code runs before the page is sent." },
'''
write("core-what-is-javascript.html", h, b, "\n" + RUNNER + "<script>" + first + js + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_first + "\n" + ex_g + "</script>\n")
