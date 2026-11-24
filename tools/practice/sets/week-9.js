  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const el = (tag, html = "") => { const e = document.createElement(tag); e.innerHTML = html; return e; };

  makeExercise(document.getElementById("ex-toggle"), {
    title: "A show/hide toggle",
    task: `<p><code>setupToggle(button, panel)</code> wires up a disclosure button. The panel starts hidden.</p>
    <ol>
      <li>Straight away, set the button's <code>aria-expanded</code> to <code>"false"</code> and its text to <code>Show details</code>.</li>
      <li>Each click flips the panel's <code>hidden</code> property, sets <code>aria-expanded</code> to <code>"true"</code> or <code>"false"</code> to match, and changes the text to <code>Hide details</code> or <code>Show details</code>.</li>
    </ol>
    <p class="hint">The checks make their own button and panel and click the button.</p>`,
    js: `function setupToggle(button, panel) {
  panel.hidden = true;
  // Your code here
}
`,
    expose: ["setupToggle"],
    hints: [
      "button.setAttribute(\"aria-expanded\", \"false\") sets the attribute; it's always a string.",
      "button.addEventListener(\"click\", () => { … }) runs on every click.",
      "Inside: panel.hidden = !panel.hidden; then set the attribute and text from panel.hidden.",
    ],
    checks: (() => {
      const make = (fns) => { const b = el("button"), p = el("div", "Bring water"); fns.setupToggle(b, p); return { b, p }; };
      return [
        { label: "Starts with aria-expanded=\"false\" and “Show details”", test: ({ fns }) => { const { b, p } = make(fns); return b.getAttribute("aria-expanded") === "false" && b.textContent === "Show details" && p.hidden; } },
        { label: "One click shows the panel", test: ({ fns }) => { const { b, p } = make(fns); b.click(); return p.hidden === false; } },
        { label: "…and sets aria-expanded=\"true\" and “Hide details”", test: ({ fns }) => { const { b } = make(fns); b.click(); return b.getAttribute("aria-expanded") === "true" && b.textContent === "Hide details"; } },
        { label: "A second click hides it again", test: ({ fns }) => { const { b, p } = make(fns); b.click(); b.click(); return p.hidden === true && b.getAttribute("aria-expanded") === "false" && b.textContent === "Show details"; } },
      ];
    })(),
  });

  makeExercise(document.getElementById("ex-build"), {
    title: "Build a list from data",
    task: `<p><code>renderTrails(list, trails)</code> gets an empty <code>&lt;ul&gt;</code> and an array of objects like <code>{ name: "Mesa", miles: 6.7 }</code>.</p>
    <ol>
      <li>For each trail, create an <code>&lt;li&gt;</code> with <code>createElement()</code>, set its text to <code>Mesa · 6.7 mi</code> with <code>textContent</code>, and add it to the list.</li>
      <li>Return how many items the list has.</li>
    </ol>
    <p>Use <code>textContent</code>, not <code>innerHTML</code>, so a trail name with <code>&lt;</code> in it shows as text.</p>`,
    js: `function renderTrails(list, trails) {
  // Your code here
}

const ul = document.createElement("ul");
console.log(renderTrails(ul, [{ name: "Mesa", miles: 6.7 }, { name: "Bear Peak", miles: 7.8 }]));
console.log(ul);
`,
    expose: ["renderTrails"],
    hints: [
      "for (const trail of trails) { … } visits each object.",
      "const li = document.createElement(\"li\"); li.textContent = trail.name + \" · \" + trail.miles + \" mi\";",
      "list.append(li) (or appendChild) adds it. list.children.length counts the items.",
    ],
    checks: [
      { label: "Makes one <li> per trail", test: ({ fns }) => { const ul = el("ul"); fns.renderTrails(ul, [{ name: "Mesa", miles: 6.7 }, { name: "Bear Peak", miles: 7.8 }]); return ul.querySelectorAll(":scope > li").length === 2; } },
      { label: "Each item reads “Mesa · 6.7 mi”", test: ({ fns }) => { const ul = el("ul"); fns.renderTrails(ul, [{ name: "Mesa", miles: 6.7 }, { name: "Royal Arch", miles: 3.4 }]); return [...ul.children].map((li) => li.textContent).join("|") === "Mesa · 6.7 mi|Royal Arch · 3.4 mi"; } },
      { label: "Uses createElement and textContent, so markup in a name stays text", test: ({ fns, code }) => { const ul = el("ul"); fns.renderTrails(ul, [{ name: "<b>Bold</b>", miles: 1 }]); return !ul.querySelector("b") && ul.textContent.includes("<b>") && /createElement\(/.test(code.js) && !/innerHTML\s*[+]?=/.test(String(fns.renderTrails)); } },
      { label: "Returns the number of items", test: ({ fns }) => fns.renderTrails(el("ul"), [{ name: "A", miles: 1 }, { name: "B", miles: 2 }, { name: "C", miles: 3 }]) === 3 },
    ],
  });

  makeExercise(document.getElementById("ex-delegate"), {
    title: "One listener for many buttons",
    task: `<p><code>setupVotes(list, output)</code> gets a list of buttons, each with a <code>data-trail</code> attribute, and an element to write into.</p>
    <ol>
      <li>Add <strong>one</strong> click listener, on <code>list</code> itself, not one on each button (event delegation).</li>
      <li>When a button is clicked, show <code>You picked </code> plus its <code>data-trail</code> in <code>output</code>.</li>
      <li>Ignore clicks that aren't on a button.</li>
    </ol>
    <p class="hint">Delegation also works for buttons added later, and the checks test that.</p>`,
    js: `function setupVotes(list, output) {
  // Your code here
}
`,
    expose: ["setupVotes"],
    hints: [
      "list.addEventListener(\"click\", (e) => { … }) catches clicks that bubble up from the buttons.",
      "const button = e.target.closest(\"button\"); is the button that was clicked, or null.",
      "If there's no button, return early. Otherwise read button.dataset.trail.",
    ],
    checks: (() => {
      const make = (fns) => { const list = el("div", '<button data-trail="Mesa">Mesa</button><button data-trail="Bear Peak">Bear <b>Peak</b></button><p>Pick one</p>'); const out = el("p"); document.body.append(list); fns.setupVotes(list, out); return { list, out }; };
      const done = (list) => list.remove();
      return [
        { label: "Clicking a button shows “You picked …”", test: ({ fns }) => { const { list, out } = make(fns); list.querySelector("button").click(); done(list); return out.textContent === "You picked Mesa"; } },
        { label: "Works when the click lands on an element inside the button", test: ({ fns }) => { const { list, out } = make(fns); list.querySelector("b").click(); done(list); return out.textContent === "You picked Bear Peak"; } },
        { label: "Ignores clicks that aren't on a button", test: ({ fns }) => { const { list, out } = make(fns); list.querySelector("button").click(); list.querySelector("p").click(); done(list); return out.textContent === "You picked Mesa"; } },
        { label: "One listener on the list: a button added later works too", test: ({ fns }) => { const { list, out } = make(fns); const b = el("button", "Flagstaff"); b.dataset.trail = "Flagstaff"; list.append(b); b.click(); done(list); return out.textContent === "You picked Flagstaff"; } },
      ];
    })(),
  });

  makeExercise(document.getElementById("ex-fetch"), {
    title: "Load trails with fetch",
    task: `<p><code>dogTrails(url)</code> loads a JSON list of trails, like <a href="data/trails.json" target="_blank" rel="noopener">data/trails.json</a>, and returns a promise for the <em>names</em> of the trails that allow dogs (<code>dogs: true</code>).</p>
    <ol>
      <li>If the response isn't OK (say, a 404), return an empty array.</li>
      <li>If anything else goes wrong (a bad address, or no network), catch it and return an empty array too.</li>
    </ol>
    <p class="hint">The checks really fetch <code>data/trails.json</code>, and a file that doesn't exist.</p>`,
    js: `async function dogTrails(url) {
  const response = await fetch(url);
  const trails = await response.json();
  // Your code here: return the names of the trails that allow dogs
}

dogTrails("data/trails.json").then((names) => console.log(names));
`,
    expose: ["dogTrails"],
    hints: [
      "trails.filter((t) => t.dogs).map((t) => t.name) keeps the dog-friendly ones, then takes their names.",
      "if (!response.ok) { return []; } goes before response.json().",
      "Wrap the body in try { … } catch (err) { return []; } for network errors.",
    ],
    checks: [
      { label: "Returns the names of the dog-friendly trails", test: async ({ fns }) => same(await fns.dogTrails("data/trails.json"), ["Mesa Trail", "Royal Arch", "Chautauqua Loop"]) },
      { label: "A missing file (404) gives []", test: async ({ fns }) => same(await fns.dogTrails("data/no-such-file.json"), []) },
      { label: "A bad address is caught, and gives []", test: async ({ fns }) => same(await fns.dogTrails("http://[bad-address"), []) },
      { label: "Checks response.ok and uses try...catch", test: ({ fns }) => { const src = String(fns.dogTrails); return /response\.ok/.test(src) && /try\s*\{/.test(src) && /catch\s*(\(|\{)/.test(src); } },
    ],
  });

  makeQuiz(document.getElementById("quiz"), [
    { id: "q1", q: "What's the difference between button.onclick = f and button.addEventListener(\"click\", f)?", opts: ["None", "onclick holds one handler, so a second assignment replaces the first; addEventListener can add several", "addEventListener only works on links", "onclick runs twice"], a: 1, why: "addEventListener keeps every listener you add, and pairs with removeEventListener." },
    { id: "q2", q: "In a click handler, what is e.target?", opts: ["The element the listener is on", "The element that was actually clicked, which may be inside it", "The window", "The previous element clicked"], a: 1, why: "e.target is where the event started. e.currentTarget is the element whose listener is running." },
    { id: "q3", q: "Why call e.preventDefault() in a form's submit handler?", opts: ["To stop the browser submitting and reloading the page, so your code can handle it", "To clear the form", "To stop other listeners running", "To validate the inputs"], a: 0, why: "preventDefault() cancels the browser's built-in action, which here is sending the form and loading a new page." },
    { id: "q4", q: "You click a button inside a <li> inside a <ul>, and all three have click listeners. In what order do they run, by default?", opts: ["ul, li, button", "button, li, ul", "Only the button's runs", "In the order they were added"], a: 1, why: "Events bubble: they start at the target and travel up through its ancestors." },
    { id: "q5", q: "What's the main benefit of event delegation?", opts: ["Faster CSS", "One listener on a parent handles every child, including children added later", "It stops bubbling", "Events fire twice"], a: 1, why: "Because events bubble, a listener on the parent sees clicks on all its children, present and future." },
    { id: "q6", q: "After const li = document.createElement(\"li\"); is the new item on the page?", opts: ["Yes, at the end of the body", "No, not until you add it with append() or appendChild()", "Yes, inside the first list", "Only after a reload"], a: 1, why: "createElement makes a detached element. It appears only when you attach it to something on the page." },
    { id: "q7", q: "How do you remove an element from the page?", opts: ["element.delete()", "element.remove()", "element.hidden = \"removed\"", "document.remove(element)"], a: 1, why: "element.remove() takes it out of the DOM. (hidden only hides it.)" },
    { id: "q8", q: "fetch(\"missing.json\") gets a 404. What does the promise do?", opts: ["Rejects with an error", "Resolves with a response whose ok is false", "Never settles", "Resolves with undefined"], a: 1, why: "fetch rejects only when no response arrives at all, such as a network failure. Check response.ok for HTTP errors." },
    { id: "q9", q: "What does response.json() return?", opts: ["A JavaScript object, immediately", "A promise for the parsed data", "A JSON string", "The response's status"], a: 1, why: "Reading the body takes time, so json() returns a promise. Await it, or use .then()." },
    { id: "q10", q: "Where can you use await?", opts: ["Anywhere", "Inside an async function (or at the top level of a module)", "Only inside loops", "Only with fetch"], a: 1, why: "await pauses an async function until a promise settles. Ordinary functions can't pause." },
  ], { once: true });
