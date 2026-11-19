import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-fetch")
pg_watch = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">What happens on the server</span>', '  <div class="section-title"><span class="eyebrow">Play</span><h2>The file being fetched')
pg_file = src.between('  <section class="playground even">\n    <div class="stage-col"><span class="eyebrow">trails.json', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Fetching Data", src.css(), """
  #nc-code { white-space: pre-wrap; }
  .nc-out { min-height: 90px; padding: 12px 14px; border: 1px solid var(--line); border-radius: 8px; background: var(--paper, transparent); }
  .nc-out.err { border-color: #b4410c; color: #b4410c; }
""")
b = top("Fetching Data", "Many pages update part of themselves without reloading: new search results, the latest weather, more posts as you scroll. They ask a server for data with <code>fetch()</code>, then use the DOM to show it.", [
  "Explain why pages fetch data instead of reloading, and what a promise is.",
  "Fetch text and JSON with <code>fetch()</code>, <code>.then()</code> and <code>async</code>/<code>await</code>.",
  "Check <code>response.ok</code> and handle errors with <code>.catch()</code> or <code>try...catch</code>.",
  "Recognise older <code>XMLHttpRequest</code> code.",
])
b += ST("Read", "What is the problem here?") + prose("""
    <p>Traditionally, every click on a link loaded a whole new page from the server, even if only one small part changed. That's slow and wasteful. Instead, JavaScript can request just the data it needs and update part of the page with the DOM. This is sometimes called <em>Ajax</em>, and today it's done with the <span class="term" data-term="fetch()">Fetch API</span>.</p>
    <p>Fetching also saves bandwidth: the browser can cache files, and only the new data travels over the network.</p>""")
b += ST("Read", "The Fetch API") + prose("""
    <p>The answer to a request takes time to arrive, from a few milliseconds to several seconds. JavaScript doesn't stop and wait; the code after <code>fetch()</code> keeps running right away. Instead, <code>fetch()</code> returns a <span class="term">promise</span>: a placeholder for a value that will arrive later.</p>
    <h3>Fetching text content</h3>
    <p>MDN's first example loads a text file and shows it. You pass a function to the promise's <code>.then()</code> method, and it runs when the response arrives:</p>
    <pre class="snippet" data-lang="js">fetch(url)
  .then((response) =&gt; {
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.text();
  })
  .then((text) =&gt; {
    poemDisplay.textContent = text;
  })
  .catch((error) =&gt; {
    poemDisplay.textContent = `Could not fetch verse: ${error}`;
  });</pre>
    <p>The first <code>.then()</code> gets a <code>Response</code> object. Reading its body with <code>response.text()</code> takes time too, so it returns another promise, which the second <code>.then()</code> waits for. <code>.catch()</code> runs if anything along the chain fails.</p>""")
b += ST("Play", "Trail notes", "These are real requests for small text files in this site's <code>data/notes</code> folder. Try the missing one too.") + """  <section class="playground">
    <div class="panel controls">
      <div class="control"><label for="nc-pick">Choose a trail</label><select id="nc-pick"><option value="mesa">Mesa Trail</option><option value="royal-arch">Royal Arch</option><option value="bear-peak">Bear Peak</option><option value="flagstaff">Flagstaff (no file)</option></select></div>
      <p class="hint">Open DevTools' Network tab to see each request.</p>
    </div>
    <div class="stage-col">
      <pre class="snippet" id="nc-code" data-lang="js"></pre>
      <div class="nc-out" id="nc-out" aria-live="polite"></div>
    </div>
  </section>

"""
b += prose("""
    <div class="callout warn"><p class="callout-title">Watch out</p><p>A 404 "not found" is a <em>completed</em> request as far as <code>fetch()</code> is concerned, so it won't land in <code>.catch()</code> by itself. Check <code>response.ok</code> and throw an error when it's false. And pages opened by double-clicking the file (<code>file://</code>) can't fetch: use a local server such as VS Code's Live Server, or test on GitHub Pages.</p></div>""")
b += ST("Play", "Watch a request happen", "Send a request and follow it to the server and back. Try a slow network and a missing file.") + pg_watch
b += ST("Read", "Fetching JSON") + prose("""
    <p>MDN's second example, the "can store", fetches a JSON list of products and builds the page from it. The only difference is the method that reads the body: <code>response.json()</code> reads it <em>and</em> parses it, so you get an array of objects instead of text.</p>""")
b += runner("""fetch("data/trails.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();
  })
  .then((trails) => {
    for (const trail of trails) {
      console.log(`${trail.name}: ${trail.miles} miles`);
    }
  })
  .catch((error) => console.error(`Could not fetch trails: ${error}`));

console.log("This line runs first: fetch doesn't wait.");""")
b += ST("Look", "The file being fetched", "The server sends back plain text in JSON format. <code>response.json()</code> parses it into an array of objects, which the code loops over to build the list.") + pg_file
b += ST("Read", "async and await") + prose("""
    <p>Chains of <code>.then()</code> work, but there's a tidier way to write the same thing. Inside a function marked <code>async</code>, <code>await</code> pauses <em>that function</em> until a promise settles, and gives you its value. Errors are caught with an ordinary <code>try...catch</code>:</p>""")
b += runner("""async function loadTrails() {
  try {
    const response = await fetch("data/trails.json");
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
    const trails = await response.json();
    const easy = trails.filter((t) => t.difficulty === "easy");
    console.log("Easy trails:", easy.map((t) => t.name));
  } catch (error) {
    console.error(`Could not fetch trails: ${error}`);
  }
}

loadTrails();""")
b += prose("""
    <p>Both styles do the same thing. You'll see both in code online, and MDN's <a href="https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Async_JS">Asynchronous JavaScript</a> module goes further.</p>
    <h3>Fetching other kinds of data</h3>
    <p><code>response.blob()</code> reads the body as raw data, like an image file. <code>URL.createObjectURL(blob)</code> then gives you a URL you can put in an <code>&lt;img&gt;</code>'s <code>src</code>.</p>""")
b += ST("Read", "The XMLHttpRequest API") + prose("""
    <p>Before <code>fetch()</code>, requests were made with <code>XMLHttpRequest</code> (often "XHR"). You'll still find it in older code and tutorials. It does the same job with more ceremony: create the object, attach listeners, then <code>open()</code> and <code>send()</code>. Use <code>fetch()</code> for new code.</p>""")
b += runner("""const request = new XMLHttpRequest();

request.addEventListener("load", () => {
  console.log(request.status, JSON.parse(request.responseText).length, "trails");
});
request.addEventListener("error", () => console.error("Request failed"));

request.open("GET", "data/trails.json");
request.send();""")
b += ST("Practice", "Handle the response", "Write the pieces a fetch needs: a check for failed responses, and a function that pulls out the data you want.") + '  <div id="ex-fetch"></div>\n\n'
b += ST("Practice", "Fetch a trail note", "A real request: fetch a text file, and fall back to a message if it's missing.") + '  <div id="ex-note"></div>\n\n'
b += notes([
  "<code>fetch(url)</code> returns a promise for a <code>Response</code>; the code after it keeps running.",
  "Read the body with <code>response.text()</code>, <code>response.json()</code> or <code>response.blob()</code>, each a promise too.",
  "A 404 doesn't reject: check <code>response.ok</code> and throw.",
  "Handle failures with <code>.catch()</code>, or <code>try...catch</code> inside an <code>async</code> function with <code>await</code>.",
  "<code>XMLHttpRequest</code> is the older way; prefer <code>fetch()</code>.",
], [
  "Using the data on the line after <code>fetch()</code>, before it has arrived.",
  "Forgetting that <code>response.json()</code> needs its own <code>.then()</code> or <code>await</code>.",
  "Not checking <code>response.ok</code>, so a 404 page gets parsed as data.",
  "Opening the page as <code>file://</code>, where fetch is blocked.",
])
first, items = split_quiz(src.first_script())
js = r'''
  // --- trail notes (real fetch) ---
  function ncLoad() {
    const name = $("nc-pick").value, url = `data/notes/${name}.txt`, out = $("nc-out");
    $("nc-code").textContent = `fetch("${url}")\n  .then((response) => {\n    if (!response.ok) throw new Error(\`HTTP error: \${response.status}\`);\n    return response.text();\n  })\n  .then((text) => { notes.textContent = text; })\n  .catch((error) => { notes.textContent = \`Could not fetch note: \${error}\`; });`;
    out.classList.remove("err");
    out.textContent = "Loading…";
    fetch(url)
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
        return response.text();
      })
      .then((text) => { if ($("nc-pick").value === name) out.textContent = text; })
      .catch((error) => { if ($("nc-pick").value === name) { out.classList.add("err"); out.textContent = `Could not fetch note: ${error.message}`; } });
  }
  $("nc-pick").addEventListener("change", ncLoad);
  ncLoad();
'''
ex_f = src.block('  makeExercise(document.getElementById("ex-fetch"), {')
ex_n = r'''  makeExercise(document.getElementById("ex-note"), {
    title: "loadNote()",
    task: `<p><code>loadNote(url)</code> fetches a text file and returns a promise for its text. The starter works for files that exist, but for a missing file it returns the server's 404 page.</p>
    <ol>
      <li>In the first <code>.then()</code>, throw an <code>Error</code> when <code>response.ok</code> is false.</li>
      <li>Add a <code>.catch()</code> that returns <code>"Couldn't load that note."</code></li>
    </ol>
    <p class="hint">The checks really fetch <code>data/notes/mesa.txt</code> and a file that doesn't exist.</p>`,
    js: `function loadNote(url) {
  return fetch(url)
    .then((response) => {
      return response.text();
    });
}

loadNote("data/notes/mesa.txt").then((text) => console.log(text));`,
    solution: `function loadNote(url) {
  return fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(\`HTTP error: \${response.status}\`);
      }
      return response.text();
    })
    .catch(() => "Couldn't load that note.");
}

loadNote("data/notes/mesa.txt").then((text) => console.log(text));`,
    expose: ["loadNote"],
    hints: [
      "if (!response.ok) { throw new Error(\"HTTP error\"); }",
      "Chain .catch(() => \"Couldn't load that note.\") after the .then().",
      "Return the whole chain, so callers get the promise.",
    ],
    checks: [
      { label: "Loads mesa.txt", test: async ({ fns }) => { const t = await fns.loadNote("data/notes/mesa.txt"); return typeof t === "string" && t.startsWith("Mesa Trail runs"); } },
      { label: "A missing file gives “Couldn't load that note.”", test: async ({ fns }) => { try { return (await fns.loadNote("data/notes/no-such-trail.txt")) === "Couldn't load that note."; } catch { return false; } } },
      { label: "Checks response.ok", test: ({ code }) => /response\.ok/.test(code.js) },
    ],
  });
'''
items += '''    { id: "q90", q: "Does fetch() reject its promise on a 404?", opts: ["Yes", "No, you check response.ok", "Only for JSON"], a: 1, why: "The request completed, so fetch resolves; response.ok is false." },
    { id: "q91", q: "Which method reads a response body as parsed JSON?", opts: ["response.text()", "response.json()", "JSON.parse(response)"], a: 1, why: "response.json() reads and parses the body, and returns a promise." },
'''
write("core-fetching-data.html", h, b, "\n" + RUNNER + "<script>" + first + js + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_f + "\n" + ex_n + "</script>\n")
