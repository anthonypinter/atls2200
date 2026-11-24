  const text = (el) => (el ? el.textContent.replace(/\s+/g, " ").trim() : "");

  makeExercise(document.getElementById("ex-landmarks"), {
    title: "Name the landmarks",
    task: `<p>This page is built from <code>&lt;div&gt;</code>s, so a screen reader can't jump between its parts. Replace each one with the element that says what it is:</p>
    <ul>
      <li><code>top</code> is the site's header, and <code>menu</code> is its navigation.</li>
      <li><code>content</code> is the page's main content. Inside it, <code>post</code> is a self-contained article and <code>extra</code> is related, secondary content.</li>
      <li><code>bottom</code> is the footer.</li>
    </ul>
    <p>When you're done there should be no <code>&lt;div&gt;</code>s left. You can keep or drop the classes.</p>`,
    html: `<div class="top">
  <h1>Boulder Trail Club</h1>
  <div class="menu">
    <a href="#">Trails</a>
    <a href="#">Events</a>
  </div>
</div>

<div class="content">
  <div class="post">
    <h2>Spring trail cleanup</h2>
    <p>Join us on April 18 to clear winter debris from the Mesa Trail.</p>
  </div>
  <div class="extra">
    <h2>Related</h2>
    <p>Read last year's cleanup report.</p>
  </div>
</div>

<div class="bottom">
  <p>© 2026 Boulder Trail Club</p>
</div>
`,
    css: "",
    hints: [
      "The landmark elements are <header>, <nav>, <main>, <article>, <aside> and <footer>.",
      "Change both the opening and the closing tag: <div class=\"top\"> … </div> becomes <header> … </header>.",
      "The article and the aside both go inside <main>.",
    ],
    checks: [
      { label: "A <header> holds the <h1> and a <nav> with both links", test: ({ $ }) => !!$("header h1") && $("header nav").querySelectorAll("a").length === 2 },
      { label: "One <main> holds an <article> with the cleanup post", test: ({ $$ }) => $$("main").length === 1 && /cleanup/i.test(text($$("main article h2")[0])) },
      { label: "The related content is an <aside> inside <main>", test: ({ $ }) => /Related/.test(text($("main aside"))) },
      { label: "A <footer>, and no <div>s left", test: ({ $, $$ }) => /©/.test(text($("footer"))) && $$("div").length === 0 },
    ],
  });

  makeExercise(document.getElementById("ex-figure"), {
    title: "A captioned photo",
    task: `<p>Replace the placeholder paragraph with a real image and caption:</p>
    <ol>
      <li>An <code>&lt;img&gt;</code> whose <code>src</code> is <code>images/flatirons.jpg</code>.</li>
      <li>Alt text that describes what the photo shows, for someone who can't see it. Don't use the file name or start with “image of”.</li>
      <li><code>width="800"</code> and <code>height="533"</code>, so the page saves the right space before the photo loads.</li>
      <li>The photo and the caption text together in a <code>&lt;figure&gt;</code>, with the caption in a <code>&lt;figcaption&gt;</code>.</li>
    </ol>
    <p class="hint">The photo file doesn't exist here, so you'll see your alt text in its place. That's a good test of the alt text.</p>`,
    html: `<p>[Photo: images/flatirons.jpg]</p>
<p>Sunrise over the Flatirons from the Mesa Trail.</p>
`,
    css: `img { max-width: 100%; height: auto; }
`,
    hints: [
      "<figure> <img …> <figcaption>…</figcaption> </figure>",
      "Describe the scene, e.g. alt=\"Five tilted rock slabs glowing orange at sunrise\".",
      "width and height are plain numbers, with no px: width=\"800\".",
    ],
    checks: [
      { label: "An <img> with src images/flatirons.jpg", test: ({ $ }) => $("img").getAttribute("src") === "images/flatirons.jpg" },
      { label: "Alt text that describes the photo", test: ({ $ }) => { const alt = ($("img").getAttribute("alt") || "").trim(); return alt.length >= 10 && !/\.jpe?g|^(image|picture|photo) of/i.test(alt); } },
      { label: "width=\"800\" and height=\"533\"", test: ({ $ }) => $("img").getAttribute("width") === "800" && $("img").getAttribute("height") === "533" },
      { label: "The image and its <figcaption> are inside a <figure>", test: ({ $ }) => !!$("figure img") && /^Sunrise over the Flatirons/.test(text($("figure figcaption"))) && !$("p img") },
    ],
  });

  makeExercise(document.getElementById("ex-table"), {
    title: "A table that reads aloud",
    task: `<p>Every cell in this table is a <code>&lt;td&gt;</code>, so a screen reader can't tell which cells are headings. Fix it:</p>
    <ol>
      <li>Add the caption <code>Boulder trails by distance</code>.</li>
      <li>Put the first row in a <code>&lt;thead&gt;</code>, with its cells as column headers (<code>&lt;th scope="col"&gt;</code>).</li>
      <li>Put the other rows in a <code>&lt;tbody&gt;</code>, and make each trail's name a row header (<code>&lt;th scope="row"&gt;</code>).</li>
    </ol>`,
    html: `<table>
  <tr><td>Trail</td><td>Miles</td><td>Gain (ft)</td></tr>
  <tr><td>Mesa</td><td>6.7</td><td>1,100</td></tr>
  <tr><td>Royal Arch</td><td>3.4</td><td>1,400</td></tr>
  <tr><td>Flagstaff</td><td>4.1</td><td>1,500</td></tr>
</table>
`,
    css: `table { border-collapse: collapse; }
th, td { border: 1px solid #999; padding: 4px 10px; text-align: left; }
`,
    hints: [
      "The <caption> goes first, right after <table>.",
      "<thead><tr><th scope=\"col\">Trail</th>…</tr></thead>",
      "In each body row, the name cell becomes <th scope=\"row\">Mesa</th> and the numbers stay <td>.",
    ],
    checks: [
      { label: "Caption: Boulder trails by distance", test: ({ $ }) => text($("table > caption")) === "Boulder trails by distance" },
      { label: "The first row is in <thead>, as three <th scope=\"col\">", test: ({ $, $$ }) => $$("thead th[scope=col]").length === 3 && !$("thead td") },
      { label: "Three rows in <tbody>", test: ({ $$ }) => $$("tbody tr").length === 3 },
      { label: "Each trail name is a <th scope=\"row\">", test: ({ $$ }) => $$("tbody th[scope=row]").map(text).join("|") === "Mesa|Royal Arch|Flagstaff" && $$("tbody td").length === 6 },
    ],
  });

  makeExercise(document.getElementById("ex-form"), {
    title: "A sign-up form",
    task: `<ol>
      <li>Give every control a <code>&lt;label&gt;</code> that's tied to it, so clicking the label focuses the control.</li>
      <li>Make the name box a required text input with <code>name="name"</code>.</li>
      <li>Make the email box a required <em>email</em> input with <code>name="email"</code>, so the browser checks the address.</li>
      <li>Give the select <code>name="trail"</code>.</li>
      <li>Replace the <code>&lt;div&gt;</code> with a real submit button that says <code>Sign up</code>.</li>
    </ol>`,
    html: `<form>
  Name <input>
  Email <input>
  Trail
  <select>
    <option>Mesa</option>
    <option>Royal Arch</option>
  </select>
  <div>Sign up</div>
</form>
`,
    css: `form { display: grid; gap: 8px; max-width: 20rem; }
`,
    hints: [
      "<label for=\"email\">Email</label> <input id=\"email\" …>: for matches the control's id.",
      "type=\"email\" makes the browser check the format; required stops an empty submit.",
      "<button type=\"submit\">Sign up</button>",
    ],
    checks: [
      { label: "Every input and the select has a label", test: ({ $$ }) => { const c = $$("input, select"); return c.length === 3 && c.every((el) => el.labels.length > 0); } },
      { label: "Name: a required text input, name=\"name\"", test: ({ $ }) => { const i = $('input[name="name"]'); return i.type === "text" && i.required; } },
      { label: "Email: a required email input, name=\"email\"", test: ({ $ }) => { const i = $('input[name="email"]'); return i.type === "email" && i.required; } },
      { label: "The select has name=\"trail\", and a submit button says Sign up", test: ({ $, $$ }) => !!$('select[name="trail"]') && text($("button")) === "Sign up" && $("button").type === "submit" && $$("div").length === 0 },
    ],
  });

  makeQuiz(document.getElementById("quiz"), [
    { id: "q1", q: "Which element should hold the content that's unique to this page, once per page?", opts: ["<section>", "<main>", "<article>", "<body>"], a: 1, why: "<main> marks the page's main content, and a page has just one." },
    { id: "q2", q: "An image is pure decoration: a squiggle between sections. What alt should it have?", opts: ["alt=\"squiggle\"", "No alt attribute at all", "alt=\"\" (empty)", "alt=\"decorative image\""], a: 2, why: "An empty alt tells screen readers to skip it. Leaving alt out makes many of them read the file name instead." },
    { id: "q3", q: "Which format suits a logo that must stay sharp at any size?", opts: ["JPEG", "GIF", "SVG", "Animated PNG"], a: 2, why: "SVG is vector: it's drawn from shapes, so it scales without blurring and is usually tiny." },
    { id: "q4", q: "You have a large photo for the web. Which is usually the smallest good-looking file?", opts: ["BMP", "PNG", "AVIF or WebP", "SVG"], a: 2, why: "AVIF and WebP compress photos far better than JPEG or PNG, and modern browsers support them." },
    { id: "q5", q: "When is a <table> the right choice?", opts: ["To lay out a page in columns", "For data with rows and columns that relate to each other", "To line up a form's labels", "Whenever you want borders"], a: 1, why: "Tables are for tabular data. Layout belongs to CSS (grid and flexbox)." },
    { id: "q6", q: "What does scope=\"col\" on a <th> tell assistive technology?", opts: ["The header labels every cell in its column", "The column can be sorted", "The cell spans two columns", "The column is hidden"], a: 0, why: "scope says which cells a header belongs to, so each data cell can be read with its headers." },
    { id: "q7", q: "Inside a <form>, what does a <button> with no type do when clicked?", opts: ["Nothing", "Resets the form", "Submits the form", "Opens a dialog"], a: 2, why: "A button's default type is submit. Use type=\"button\" for one that shouldn't submit." },
    { id: "q8", q: "Which attribute gives a <video> the browser's play, pause and volume buttons?", opts: ["autoplay", "controls", "muted", "preload"], a: 1, why: "controls shows the built-in controls. Without it (and without your own), users can't play the video." },
    { id: "q9", q: "How do you add captions to a <video>?", opts: ["A <track kind=\"captions\"> pointing at a WebVTT file", "Put the text in alt", "A <caption> inside the video", "Type them in a <p> under it"], a: 0, why: "<track> loads timed text, a .vtt file, that the player shows in sync with the video." },
    { id: "q10", q: "You embed a page you don't control in an <iframe>. What does the sandbox attribute do?", opts: ["Makes it load faster", "Turns off most of what the page can do (scripts, forms, popups) unless you allow it", "Gives it a border", "Lets it read your page's cookies"], a: 1, why: "sandbox starts from no permissions; allow only what the embed needs, e.g. sandbox=\"allow-scripts\"." },
  ], { once: true });
