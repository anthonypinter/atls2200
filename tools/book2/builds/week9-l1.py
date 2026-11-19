import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-events")
pg_listen = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">Listen for</span>', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Bubbling')
pg_bubble = src.between('  <section class="playground">\n    <div class="panel controls">\n      <label class="check"><input type="checkbox" id="stop">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Event delegation')
pg_deleg = src.between('  <section class="playground">\n    <div class="panel controls">\n      <label class="check"><input type="checkbox" id="guard">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Events", src.css(), """
  .rc-stage { min-height: 140px; border-radius: 8px; border: 1px solid var(--line); display: grid; place-items: center; transition: background-color 0.2s; }
""")
b = top("Events", "Most JavaScript on a page waits for something to happen: a click, a key press, a form being submitted. Events are how your code finds out, so it can respond.", [
  "Listen for events with <code>addEventListener()</code>, and remove listeners again.",
  "Read the event object: <code>target</code>, <code>key</code> and more.",
  "Stop a default action, like a form reloading the page, with <code>preventDefault()</code>.",
  "Explain bubbling and capture, and use event delegation with <code>target</code> and <code>currentTarget</code>.",
])
b += ST("Read", "What is an event?") + prose("""
    <p>An <span class="term">event</span> is a signal the browser sends when something happens: the user clicks, presses a key, submits a form or resizes the window; a video finishes; a page finishes loading. Your code can respond by attaching an <span class="term">event listener</span> (a function that runs when the event fires, also called an <em>event handler</em>).</p>""")
b += ST("Read", "Using addEventListener()") + prose("""
    <p>Give <span class="term">addEventListener()</span> the event's name as a string, then the function to run. MDN's example changes the page's background color every time a button is clicked:</p>
    <pre class="snippet" data-lang="js">const btn = document.querySelector("button");

function random(number) {
  return Math.floor(Math.random() * (number + 1));
}

btn.addEventListener("click", () =&gt; {
  const rndCol = `rgb(${random(255)} ${random(255)} ${random(255)})`;
  document.body.style.backgroundColor = rndCol;
});</pre>""")
b += ST("Play", "Handling a click event", "The same code, aimed at a box instead of the whole page.") + """  <section class="playground">
    <div class="panel controls">
      <button class="btn run" type="button" id="rc-btn">Change color</button>
      <p class="hint">Each click runs the listener once.</p>
    </div>
    <div class="stage-col">
      <div class="rc-stage" id="rc-stage"><code id="rc-out">click the button</code></div>
    </div>
  </section>

"""
b += prose("""
    <h3>Listening for other events</h3>
    <p>There are many events. Some useful ones: <code>click</code> and <code>dblclick</code>; <code>focus</code> and <code>blur</code> when a field gains or loses focus; <code>input</code> on every change to a field; <code>keydown</code>; <code>mouseover</code> and <code>mouseout</code>; and <code>submit</code> on a form. Not every element fires every event: <code>submit</code> only comes from forms.</p>""")
b += ST("Play", "Listen for events", "Pick an event type and interact with the elements to see when it fires.") + pg_listen
b += prose("""
    <h3>Removing listeners</h3>
    <p><code>removeEventListener()</code> takes the same event name and the <em>same</em> function you added. That's one reason to use named functions for listeners you'll remove later: an anonymous function can't be named again.</p>
    <h3>Adding multiple listeners</h3>
    <p>You can add several listeners for the same event on the same element. They all run, in the order you added them.</p>""")
b += runner("""const btn = document.createElement("button");

function first() { console.log("first listener"); }
function second() { console.log("second listener"); }

btn.addEventListener("click", first);
btn.addEventListener("click", second);
btn.click();   // both run

btn.removeEventListener("click", first);
btn.click();   // only second""")
b += ST("Read", "Other event listener mechanisms") + prose("""
    <h3>Event handler properties</h3>
    <p>Elements also have properties like <code>onclick</code> you can set to a function: <code>btn.onclick = bgChange;</code>. It works, but each property holds only one function, so a second assignment replaces the first.</p>
    <h3>Inline event handlers: don't use these</h3>
    <p>Old code sometimes puts JavaScript straight into HTML: <code>&lt;button onclick="bgChange()"&gt;</code>. It mixes JavaScript into your markup, is hard to maintain, and is blocked by many sites' security settings. Keep your JavaScript in your script with <code>addEventListener()</code>.</p>""")
b += ST("Read", "Event objects") + prose("""
    <p>The browser passes your listener an <b>event object</b>, usually named <code>e</code>, <code>evt</code> or <code>event</code>. <span class="term">event.target</span> is the element the event happened on, so one function can handle events from many elements.</p>
    <h3>Extra properties of event objects</h3>
    <p>Different events carry different information. A <code>keydown</code> event's <code>key</code> property tells you which key was pressed:</p>
    <pre class="snippet" data-lang="js">textBox.addEventListener("keydown", (event) =&gt; {
  output.textContent = `You pressed "${event.key}".`;
});</pre>""")
b += ST("Read", "Preventing default behavior") + prose("""
    <p>Some events come with a default action. Submitting a form sends it and reloads the page; clicking a link navigates away. <span class="term">preventDefault()</span> stops that, so your code can handle it instead, for example to check the fields first:</p>
    <pre class="snippet" data-lang="js">form.addEventListener("submit", (e) =&gt; {
  if (fname.value === "" || lname.value === "") {
    e.preventDefault();
    para.textContent = "You need to fill in both names!";
  }
});</pre>
    <div class="callout warn"><p class="callout-title">Watch out</p><p>Listen for <code>submit</code> on the form, not <code>click</code> on its button. Pressing Enter in a field submits the form without clicking anything.</p></div>""")
b += ST("Read", "Event bubbling") + prose("""
    <p>Events travel. A click on a button inside a <code>&lt;div&gt;</code> fires on the button first, then on the div, then on <code>&lt;body&gt;</code>, all the way up to the document. This is <span class="term">event bubbling</span>: the event bubbles up from the innermost element.</p>
    <h3>Stopping propagation</h3>
    <p>Calling <code>event.stopPropagation()</code> in a listener stops the event going any further up. MDN's example is a video inside a box: clicking the video plays it, but without <code>stopPropagation()</code> the click also reaches the box, whose listener hides it.</p>
    <h3>Event capture</h3>
    <p>There's also an earlier <em>capture</em> phase, which goes the other way: from the outside in. Listeners only run during it if you ask, with <code>addEventListener("click", handler, { capture: true })</code>. You'll rarely need it.</p>""")
b += ST("Play", "Bubbling", "Click the button and watch the click bubble up through every ancestor. This is the setup from MDN's bubbling example.") + pg_bubble
b += ST("Read", "Event delegation") + prose("""
    <p>Bubbling makes a powerful trick possible. Instead of adding a listener to each of 50 items, add one to their container and check <code>event.target</code> to see which item was clicked. That's <span class="term">event delegation</span>, and it even works for items added later.</p>
    <h3>target and currentTarget</h3>
    <p><code>event.target</code> is the element the event started on (the innermost one). <code>event.currentTarget</code> is the element whose listener is running now: in delegation, that's the container.</p>""")
b += ST("Play", "Event delegation", "One listener on the container handles clicks on all 16 tiles.") + pg_deleg
b += ST("Practice", "Respond to events", "Wire up a click counter and a form that doesn't reload the page.") + '  <div id="ex-events"></div>\n\n'
b += ST("Practice", "Keys and delegation", "Read a property of the event object, then handle a whole list with one listener.") + '  <div id="ex-keys"></div>\n\n'
b += notes([
  "<code>el.addEventListener(\"click\", fn)</code> runs <code>fn</code> every time the event fires. <code>removeEventListener()</code> needs the same function.",
  "Pass the function itself: <code>fn</code>, not <code>fn()</code>.",
  "The event object tells you what happened: <code>e.target</code>, <code>e.key</code> and more.",
  "<code>e.preventDefault()</code> stops a default action like a form submit.",
  "Events bubble up through ancestors; <code>stopPropagation()</code> stops them. Delegation puts one listener on a container.",
], [
  "<code>addEventListener(\"click\", go())</code>: runs <code>go</code> once, immediately.",
  "Listening for <code>click</code> on a submit button instead of <code>submit</code> on the form.",
  "Inline <code>onclick=\"…\"</code> attributes in HTML.",
  "Using <code>e.target</code> in delegation without checking it's the kind of element you expect.",
])
first, items = split_quiz(src.first_script())
js = r'''
  // --- random color ---
  $("rc-btn").addEventListener("click", () => {
    const random = (n) => Math.floor(Math.random() * (n + 1));
    const rndCol = `rgb(${random(255)} ${random(255)} ${random(255)})`;
    $("rc-stage").style.backgroundColor = rndCol;
    $("rc-out").textContent = rndCol;
  });
'''
_sc = src.scripts(); _i = _sc.index('  makeExercise(document.getElementById("ex-events"), {'); _j = _sc.index("</script>", _i)
ex_e = _sc[_i:_sc.rindex("\n  });\n", _i, _j) + 6]  # block() stops at the solution's inner "  });" 
ex_k = r'''  makeExercise(document.getElementById("ex-keys"), {
    title: "Which key? Which item?",
    task: `<ol>
      <li><code>setupKeys(input, output)</code>: on every <code>keydown</code> in <code>input</code>, show <code>You pressed "a".</code> in <code>output</code>, using the event's <code>key</code>.</li>
      <li><code>setupList(list, output)</code>: add <strong>one</strong> click listener to <code>list</code> (a <code>&lt;ul&gt;</code>). When an <code>&lt;li&gt;</code> inside it is clicked, show its text in <code>output</code>. Ignore clicks that aren't on an <code>&lt;li&gt;</code>.</li>
    </ol>
    <p class="hint">The checks create their own elements and send events to them.</p>`,
    js: `function setupKeys(input, output) {
  // keydown listener here
}

function setupList(list, output) {
  // one click listener on list
}`,
    solution: `function setupKeys(input, output) {
  input.addEventListener("keydown", (e) => {
    output.textContent = \`You pressed "\${e.key}".\`;
  });
}

function setupList(list, output) {
  list.addEventListener("click", (e) => {
    if (e.target.tagName === "LI") {
      output.textContent = e.target.textContent;
    }
  });
}`,
    expose: ["setupKeys", "setupList"],
    hints: [
      "input.addEventListener(\"keydown\", (e) => { … e.key … });",
      "Inside the list's listener, e.target is the element that was clicked.",
      "if (e.target.tagName === \"LI\") skips clicks on the list itself.",
    ],
    checks: (() => {
      const mkList = () => { const ul = document.createElement("ul"); ul.innerHTML = "<li>Mesa</li><li>Royal Arch</li>"; return ul; };
      return [
        { label: "Pressing “a” shows You pressed \"a\".", test: ({ fns }) => { const i = document.createElement("input"), o = document.createElement("p"); fns.setupKeys(i, o); i.dispatchEvent(new KeyboardEvent("keydown", { key: "a", bubbles: true })); return o.textContent === 'You pressed "a".'; } },
        { label: "Clicking the second item shows “Royal Arch”", test: ({ fns }) => { const ul = mkList(), o = document.createElement("p"); fns.setupList(ul, o); ul.children[1].click(); return o.textContent === "Royal Arch"; } },
        { label: "Clicking the list itself changes nothing", test: ({ fns }) => { const ul = mkList(), o = document.createElement("p"); o.textContent = "unchanged"; fns.setupList(ul, o); ul.click(); return o.textContent === "unchanged"; } },
        { label: "Uses one listener on the list, not one per item", test: ({ code }) => /list\.addEventListener\(/.test(code.js) && !/forEach|for\s*\(/.test(code.js) },
      ];
    })(),
  });
'''
items += '''    { id: "q90", q: "Why should a listener you'll remove later be a named function?", opts: ["Named functions run faster", "removeEventListener() needs the same function you added", "Anonymous functions can't be listeners"], a: 1, why: "You have to pass the exact same function, so you need a name to refer to it." },
    { id: "q91", q: "In a delegated listener on a <ul>, what is event.currentTarget?", opts: ["The <li> clicked", "The <ul>", "The document"], a: 1, why: "currentTarget is the element whose listener is running; target is where the click started." },
'''
write("core-events.html", h, b, "\n" + RUNNER + "<script>" + first + js + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_e + "\n" + ex_k + "</script>\n")
