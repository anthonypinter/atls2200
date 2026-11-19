import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-dom")
pg_sel = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="method">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>The DOM tree')
pg_tree = src.between('  <section class="playground even">\n    <div class="dom" id="dom"', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Change what you selected')
pg_act = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="actions" id="actions"', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("DOM Scripting", src.css())
b = top("DOM Scripting", "When the browser reads your HTML, it builds a tree of objects in memory. JavaScript can find any element in that tree and change its text, its attributes, its classes and its styles, and the page updates immediately.", [
  "Name the main parts of the browser JavaScript can reach: <code>window</code>, <code>navigator</code> and <code>document</code>.",
  "Read the DOM as a tree of parents, children and siblings.",
  "Find elements with <code>querySelector()</code> and <code>querySelectorAll()</code>, and change their text and attributes.",
  "Create, move and remove elements, and change styles with <code>classList</code> and <code>style</code>.",
])
b += ST("Read", "The important parts of a web browser") + prose("""
    <p>JavaScript in a web page can reach several objects the browser provides:</p>
    <ul>
      <li><code>window</code> is the browser tab the page is loaded into. It knows things like the window's size (<code>window.innerWidth</code>) and can run code when it's resized.</li>
      <li><code>navigator</code> represents the browser itself: its preferred language, the user's location (with permission), and more.</li>
      <li><code>document</code> is the page loaded into the window. It's your way into the <span class="term">DOM</span>, the Document Object Model, and the object you'll use most.</li>
    </ul>""")
b += ST("Read", "The document object model") + prose("""
    <p>The DOM is a tree of objects, one for each element (and each piece of text) in the page. JavaScript can't change your HTML file, but it can change the DOM, and the page updates immediately.</p>
    <p>The DOM uses the same family words as CSS. Each object in the tree is a <span class="term">node</span>. The top one, <code>&lt;html&gt;</code>, is the <em>root</em>. A <span class="term">parent</span> node directly contains its <span class="term" data-term="Child">children</span>; children of the same parent are <span class="term">siblings</span>; and anything inside a node, at any depth, is a <span class="term">descendant</span>.</p>""")
b += ST("Read", "Basic DOM manipulation") + prose("""
    <p>To change an element, first find it and store a reference to it in a variable. <span class="term">querySelector()</span> takes any CSS <span class="term">selector</span> and returns the first match:</p>
    <pre class="snippet" data-lang="js">const link = document.querySelector("a");
link.textContent = "Mozilla Developer Network";
link.href = "https://developer.mozilla.org";</pre>
    <p><span class="term">textContent</span> reads or replaces an element's text, and attributes like <code>href</code> and <code>src</code> are properties you can set directly.</p>
    <p><code>querySelectorAll()</code> returns every match as a list you can loop over. Older code uses <code>getElementById()</code> and <code>getElementsByTagName()</code>; they still work, but <code>querySelector()</code> handles any selector.</p>
    <div class="callout warn"><p class="callout-title">Watch out</p><p>If nothing matches, <code>querySelector()</code> returns <code>null</code>, and using it gives the error "Cannot read properties of null." That almost always means a typo in your selector, or a script that ran before the element existed.</p></div>""")
b += ST("Play", "Select elements", "Pick a method, type a selector and see what it matches.") + pg_sel
b += ST("Play", "The DOM tree", "This is the mini page above as the browser sees it. Matches from your selector are highlighted. Click any node to see how it relates to the others.") + pg_tree
b += ST("Read", "Creating and placing new nodes") + prose("""
    <p><code>document.createElement()</code> makes a new element in memory. It doesn't appear anywhere until you add it to the page, usually with <code>appendChild()</code>, which places it as the last child of a parent:</p>""")
b += runner("""const section = document.createElement("section");
section.innerHTML = "<p>We hope you enjoyed the ride.</p>";

const para = document.createElement("p");
para.textContent = "This was made in JavaScript.";
section.appendChild(para);

const text = document.createTextNode(" Plain text works too.");
para.appendChild(text);

console.log(section.outerHTML);""")
b += prose("""
    <p>You'll do much more of this, including a shopping list, in Creating Elements.</p>""")
b += ST("Read", "Moving and removing elements") + prose("""
    <p>Appending an element that's already in the page <em>moves</em> it rather than copying it. To make a copy, use <code>cloneNode()</code>. To take an element out, call its <code>remove()</code> method (older code calls <code>parent.removeChild(child)</code>).</p>""")
b += runner("""const box = document.createElement("div");
box.innerHTML = "<p id='a'>A</p><p id='b'>B</p><p id='c'>C</p>";

const a = box.querySelector("#a");
box.appendChild(a);            // moves A to the end
console.log(box.innerHTML);

box.querySelector("#b").remove();
console.log(box.innerHTML);

box.appendChild(a.cloneNode(true));   // a copy this time
console.log(box.innerHTML);""")
b += ST("Read", "Manipulating styles") + prose("""
    <p>There are two ways to change how an element looks. The first sets inline styles through the <code>style</code> property. CSS properties with hyphens become camelCase, because hyphens aren't allowed in JavaScript names:</p>
    <pre class="snippet" data-lang="js">para.style.color = "white";
para.style.backgroundColor = "black";
para.style.padding = "10px";</pre>
    <p>The second, usually better, adds a class and keeps the styles in your CSS file, where they belong. <span class="term">classList</span> has <code>add()</code>, <code>remove()</code> and <code>toggle()</code>:</p>
    <pre class="snippet" data-lang="js">para.classList.add("highlight");</pre>
    <div class="callout tip"><p class="callout-title">Tip</p><p>Write the selector in your CSS file first and make sure it styles the right element. Then use the same selector in JavaScript.</p></div>""")
b += ST("Play", "Change what you selected", "These act on whatever your selector matched above. Try them on <code>.featured</code>, then on <code>h2</code> with querySelectorAll.") + pg_act
b += ST("Practice", "Change a card with the DOM", "Write a function that finds parts of a trail card and updates them.") + '  <div id="ex-dom"></div>\n\n'
b += ST("Practice", "Fix the link", "From MDN's basic DOM manipulation: change a link, then add a paragraph after it.") + '  <div id="ex-link"></div>\n\n'
b += notes([
  "<code>window</code> is the tab, <code>navigator</code> the browser, and <code>document</code> the page and its DOM.",
  "<code>querySelector()</code> returns the <b>first</b> match, or <code>null</code>; <code>querySelectorAll()</code> returns <b>every</b> match.",
  "Change text with <code>textContent</code> and attributes like <code>href</code> directly.",
  "<code>createElement()</code> makes an element; <code>appendChild()</code> places it (or moves it); <code>remove()</code> takes it out.",
  "Prefer <code>classList</code> over <code>style</code>, so styles stay in CSS.",
], [
  "A script that runs before the elements exist, so <code>querySelector()</code> returns <code>null</code>. Use <code>defer</code>.",
  "Treating the list from <code>querySelectorAll()</code> as one element: <code>cards.classList</code> is <code>undefined</code>. Loop over it.",
  "Writing <code>el.style.background-color</code>. Use camelCase: <code>backgroundColor</code>.",
  "Using <code>innerHTML</code> with text people typed. Use <code>textContent</code>.",
])
first, items = split_quiz(src.first_script())
ex_d = src.block('  makeExercise(document.getElementById("ex-dom"), {')
ex_l = r'''  makeExercise(document.getElementById("ex-link"), {
    title: "Update the link",
    task: `<p><code>fixLink(box)</code> receives an element containing one link: <code>&lt;a href="#"&gt;link&lt;/a&gt;</code>.</p>
    <ol>
      <li>Set the link's text to <code>Mozilla Developer Network</code> and its <code>href</code> to <code>https://developer.mozilla.org/</code>.</li>
      <li>Create a <code>&lt;p&gt;</code> with the text <code>We hope you enjoyed the ride.</code>, give it the class <code>note</code>, and append it to <code>box</code>.</li>
    </ol>`,
    js: `function fixLink(box) {
  const link = box.querySelector("a");
  // Your code here
}

const test = document.createElement("div");
test.innerHTML = '<a href="#">link</a>';
fixLink(test);
console.log(test.innerHTML);`,
    solution: `function fixLink(box) {
  const link = box.querySelector("a");
  link.textContent = "Mozilla Developer Network";
  link.href = "https://developer.mozilla.org/";

  const para = document.createElement("p");
  para.textContent = "We hope you enjoyed the ride.";
  para.classList.add("note");
  box.appendChild(para);
}

const test = document.createElement("div");
test.innerHTML = '<a href="#">link</a>';
fixLink(test);
console.log(test.innerHTML);`,
    expose: ["fixLink"],
    hints: [
      "link.textContent = \"…\"; link.href = \"…\";",
      "const para = document.createElement(\"p\");",
      "para.classList.add(\"note\"); then box.appendChild(para);",
    ],
    checks: (() => {
      const make = () => { const d = document.createElement("div"); d.innerHTML = '<a href="#">link</a>'; return d; };
      return [
        { label: "The link's text and href are updated", test: ({ fns }) => { const d = make(); fns.fixLink(d); const a = d.querySelector("a"); return a.textContent === "Mozilla Developer Network" && a.getAttribute("href") === "https://developer.mozilla.org/"; } },
        { label: "A new paragraph is appended after the link", test: ({ fns }) => { const d = make(); fns.fixLink(d); const p = d.lastElementChild; return p && p.tagName === "P" && p.textContent === "We hope you enjoyed the ride."; } },
        { label: "The paragraph has the class note", test: ({ fns }) => { const d = make(); fns.fixLink(d); const p = d.querySelector("p"); return !!p && p.classList.contains("note"); } },
      ];
    })(),
  });
'''
items += '''    { id: "q90", q: "Which object represents the page loaded in the tab?", opts: ["window", "navigator", "document"], a: 2, why: "document is the page, and your way into the DOM." },
    { id: "q91", q: "What happens if you appendChild() an element that's already on the page?", opts: ["It's copied", "It moves", "Nothing"], a: 1, why: "An element can only be in one place; use cloneNode() for a copy." },
'''
write("core-dom-scripting.html", h, b, "\n" + RUNNER + "<script>" + first + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_d + "\n" + ex_l + "</script>\n")
