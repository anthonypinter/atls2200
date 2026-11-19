import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-create-elements")
fg_prose = src.between('  <div class="prose">\n    <p>So far you', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Build a shopping list')
pg_shop = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">Try a mistake</span>', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Created isn')
pg_mem = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="stepper">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Creating Elements", src.css(), """
  #gal-code { white-space: pre-wrap; }
  .gal { display: grid; gap: 10px; max-width: 560px; }
  .gal-full { position: relative; border-radius: 8px; overflow: hidden; aspect-ratio: 16 / 9; background: #222; }
  .gal-full img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .gal-overlay { position: absolute; inset: 0; background: rgb(0 0 0 / 0%); pointer-events: none; transition: background 0.2s; }
  .gal-full.dark .gal-overlay { background: rgb(0 0 0 / 50%); }
  .gal-full button { position: absolute; top: 10px; left: 10px; }
  .gal-thumbs { display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; }
  .gal-thumbs img { display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 5px; cursor: pointer; border: 2px solid transparent; }
  .gal-thumbs img:hover, .gal-thumbs img:focus-visible { border-color: var(--cobalt); outline: none; }
  .gal-thumbs img.current { border-color: var(--prop); }
""")
b = top("Creating Elements", "So far you've changed elements that were already in the HTML. JavaScript can also build new ones: that's how a to-do list grows when you add an item, how search results appear, and how a gallery fills itself from a list of images.", [
  "Create, fill and attach elements with <code>createElement()</code>, <code>textContent</code> and <code>appendChild()</code>.",
  "Remove elements, and explain why <code>textContent</code> is safer than <code>innerHTML</code>.",
  "Build MDN's dynamic shopping list from a form and a list.",
  "Generate an image gallery from an array of data, with click and keyboard handlers.",
])
b += ST("Read", "Creating and placing new nodes") + fg_prose
b += ST("Play", "Created isn't the same as on the page", "<code>createElement()</code> makes an element in memory. It doesn't show up anywhere until you attach it to something that's already on the page.") + pg_mem
b += ST("Read", "A dynamic shopping list") + prose("""
    <p>MDN's shopping list puts it all together. The HTML is a label, an input, a button and an empty list. The JavaScript, step by step:</p>
    <ol>
      <li>Store references to the list, the input and the button.</li>
      <li>Add a listener to the button (or better, the form's <code>submit</code>).</li>
      <li>In it, store the input's current <code>value</code>, then empty the input.</li>
      <li>Create an <code>&lt;li&gt;</code>, a <code>&lt;span&gt;</code> and a <code>&lt;button&gt;</code>. Append the span and button to the list item, set the span's text to the value and the button's text to "Delete", then append the list item to the list.</li>
      <li>Add a listener to the delete button that removes its list item.</li>
      <li>Finally, call <code>input.focus()</code> so people can type the next item straight away.</li>
    </ol>
    <pre class="snippet" data-lang="js">form.addEventListener("submit", (event) =&gt; {
  event.preventDefault();
  const myItem = input.value;
  input.value = "";

  const listItem = document.createElement("li");
  const listText = document.createElement("span");
  const listBtn = document.createElement("button");

  listItem.appendChild(listText);
  listText.textContent = myItem;
  listItem.appendChild(listBtn);
  listBtn.textContent = "Delete";
  list.appendChild(listItem);

  listBtn.addEventListener("click", () =&gt; {
    list.removeChild(listItem);
  });

  input.focus();
});</pre>""")
b += ST("Play", "Build a shopping list", "Add and delete items and watch which lines of code run. Then try each mistake.") + pg_shop
b += ST("Practice", "Build and remove list items", "Write two functions: one adds an item to a list, the other clears out finished ones.") + '  <div id="ex-create"></div>\n\n'
b += ST("Read", "An image gallery") + prose("""
    <p>MDN's image gallery challenge builds a set of thumbnails from data. Clicking a thumbnail shows it large; a button darkens and lightens the big image.</p>
    <h3>Start from data</h3>
    <p>Instead of writing five <code>&lt;img&gt;</code> elements in the HTML, keep the images in an array of objects. Each object has the file name and the alt text:</p>
    <pre class="snippet" data-lang="js">const images = [
  { filename: "pic1.jpg", alt: "Closeup of a human eye" },
  { filename: "pic2.jpg", alt: "Rock that looks like a wave" },
  // …
];</pre>
    <h3>Looping through the images</h3>
    <p>Loop through the array. For each item, create an <code>&lt;img&gt;</code>, set its <code>src</code> and <code>alt</code>, and append it to the thumbnail bar:</p>
    <pre class="snippet" data-lang="js">for (const image of images) {
  const newImage = document.createElement("img");
  newImage.src = `images/${image.filename}`;
  newImage.alt = image.alt;
  newImage.tabIndex = 0;
  thumbBar.appendChild(newImage);

  newImage.addEventListener("click", updateDisplayedImage);
  newImage.addEventListener("keydown", (e) =&gt; {
    if (e.code === "Enter") updateDisplayedImage(e);
  });
}

function updateDisplayedImage(e) {
  displayedImage.src = e.target.src;
  displayedImage.alt = e.target.alt;
}</pre>
    <p>Images can't normally be focused, so <code>tabIndex = 0</code> puts each one in the tab order, and the <code>keydown</code> listener lets keyboard users press Enter to choose it. (In your own work a <code>&lt;button&gt;</code> around each image gets you both for free.)</p>
    <h3>The darken/lighten button</h3>
    <p>The button's listener checks its own class. If it's <code>dark</code>, it switches to <code>light</code>, changes its text to "Lighten" and shows a translucent black overlay; otherwise it does the reverse. <code>classList.toggle()</code> is a compact way to flip a class on and off.</p>""")
b += ST("Play", "Image gallery", "Built entirely by the loop above. Click a thumbnail, or tab to one and press Enter.") + """  <section class="playground">
    <div class="gal">
      <div class="gal-full" id="gal-full"><img id="gal-img" alt=""><div class="gal-overlay"></div><button class="btn" type="button" id="gal-dark">Darken</button></div>
      <div class="gal-thumbs" id="gal-thumbs" role="group" aria-label="Thumbnails"></div>
    </div>
    <div class="stage-col"><pre class="snippet" id="gal-code" data-lang="js"></pre></div>
  </section>

"""
b += ST("Practice", "Build the thumbnails", "Turn an array of image data into thumbnails that update the big image.") + '  <div id="ex-gallery"></div>\n\n'
b += notes([
  "Three steps: <code>createElement()</code> to make it, fill it in, then <code>appendChild()</code> or <code>append()</code> to attach it.",
  "A created element isn't on the page until it's attached to something that is.",
  "<code>remove()</code> takes an element out; appending one that's already on the page moves it.",
  "Use <code>textContent</code> for anything a visitor typed, never <code>innerHTML</code>.",
  "Keep repeated content in an array of objects and build the elements in a loop.",
], [
  "Creating an element and never attaching it.",
  "Using <code>innerHTML</code> with user input, which can run code.",
  "Adding listeners to elements before they've been created.",
  "Clickable images or divs with no keyboard support.",
])
first, items = split_quiz(src.first_script())
js = r'''
  // --- image gallery ---
  (() => {
    const scenes = [
      ["#f2a65a", "#7a4e8c", "#3d2b4f", "Sunset over a mountain ridge"],
      ["#9ed2f0", "#5a8f4e", "#2f5a2a", "Green hills under a blue sky"],
      ["#1b2a4a", "#3c4f7a", "#0d1424", "Night sky above a dark ridge"],
      ["#e8e2d0", "#b9b2a0", "#8a8476", "Snowy peaks on a cloudy day"],
      ["#f7d06b", "#d9822b", "#8c3b1e", "Red desert cliffs at noon"],
    ];
    const svg = ([sky, far, near]) => "data:image/svg+xml," + encodeURIComponent(
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 90"><rect width="160" height="90" fill="${sky}"/><circle cx="120" cy="24" r="10" fill="#fff8" /><path d="M0 70 L40 30 L70 55 L100 25 L160 65 V90 H0Z" fill="${far}"/><path d="M0 90 L0 75 L50 55 L95 78 L130 62 L160 80 V90Z" fill="${near}"/></svg>`);
    const images = scenes.map((s, i) => ({ filename: `pic${i + 1}.jpg`, src: svg(s), alt: s[3] }));
    const thumbBar = $("gal-thumbs"), displayedImage = $("gal-img");
    function updateDisplayedImage(e) {
      displayedImage.src = e.target.src;
      displayedImage.alt = e.target.alt;
      thumbBar.querySelectorAll("img").forEach((im) => im.classList.toggle("current", im === e.target));
      $("gal-code").textContent = `// updateDisplayedImage(e)\ndisplayedImage.src = e.target.src;   // ${e.target.dataset.file}\ndisplayedImage.alt = "${e.target.alt}";`;
    }
    for (const image of images) {
      const newImage = document.createElement("img");
      newImage.src = image.src;
      newImage.alt = image.alt;
      newImage.dataset.file = image.filename;
      newImage.tabIndex = 0;
      thumbBar.appendChild(newImage);
      newImage.addEventListener("click", updateDisplayedImage);
      newImage.addEventListener("keydown", (e) => { if (e.code === "Enter" || e.key === "Enter") updateDisplayedImage(e); });
    }
    updateDisplayedImage({ target: thumbBar.firstElementChild });
    $("gal-dark").addEventListener("click", (e) => {
      const btn = e.currentTarget, dark = $("gal-full").classList.toggle("dark");
      btn.textContent = dark ? "Lighten" : "Darken";
      $("gal-code").textContent = `btn.textContent = "${btn.textContent}";\noverlay.style.backgroundColor = "rgb(0 0 0 / ${dark ? 50 : 0}%)";`;
    });
  })();
'''
ex_c = src.block('  makeExercise(document.getElementById("ex-create"), {')
ex_g = r'''  makeExercise(document.getElementById("ex-gallery"), {
    title: "Thumbnails from data",
    task: `<p><code>buildThumbs(images, thumbBar, displayedImage)</code> gets an array like <code>[{ src: "a.jpg", alt: "A lake" }, …]</code>, an empty container and the big <code>&lt;img&gt;</code>.</p>
    <ol>
      <li>Loop through <code>images</code>. For each one, create an <code>&lt;img&gt;</code>, set its <code>src</code> and <code>alt</code>, and append it to <code>thumbBar</code>.</li>
      <li>When a thumbnail is clicked, copy its <code>src</code> and <code>alt</code> to <code>displayedImage</code>.</li>
    </ol>`,
    js: `function buildThumbs(images, thumbBar, displayedImage) {
  for (const image of images) {
    // create, fill, append, listen
  }
}`,
    solution: `function buildThumbs(images, thumbBar, displayedImage) {
  for (const image of images) {
    const newImage = document.createElement("img");
    newImage.src = image.src;
    newImage.alt = image.alt;
    thumbBar.appendChild(newImage);

    newImage.addEventListener("click", (e) => {
      displayedImage.src = e.target.src;
      displayedImage.alt = e.target.alt;
    });
  }
}`,
    expose: ["buildThumbs"],
    hints: [
      "const newImage = document.createElement(\"img\");",
      "newImage.src = image.src; newImage.alt = image.alt; thumbBar.appendChild(newImage);",
      "newImage.addEventListener(\"click\", (e) => { displayedImage.src = e.target.src; … });",
    ],
    checks: (() => {
      const data = [{ src: "data:,a", alt: "A lake" }, { src: "data:,b", alt: "A ridge" }, { src: "data:,c", alt: "A field" }];
      const run = (fns) => { const bar = document.createElement("div"), big = document.createElement("img"); fns.buildThumbs(data, bar, big); return { bar, big }; };
      return [
        { label: "Creates one <img> per item", test: ({ fns }) => { const { bar } = run(fns); return bar.querySelectorAll("img").length === 3; } },
        { label: "Each thumbnail has the right src and alt", test: ({ fns }) => { const { bar } = run(fns); const ims = bar.querySelectorAll("img"); return ims.length === 3 && ims[1].getAttribute("src") === "data:,b" && ims[1].alt === "A ridge"; } },
        { label: "Clicking a thumbnail updates the big image", test: ({ fns }) => { const { bar, big } = run(fns); const im = bar.querySelectorAll("img")[2]; if (!im) return false; im.click(); return big.getAttribute("src") === "data:,c" && big.alt === "A field"; } },
      ];
    })(),
  });
'''
items += '''    { id: "q90", q: "Why does the gallery set tabIndex = 0 on each thumbnail?", opts: ["To sort the images", "So keyboard users can focus them", "To make them load faster"], a: 1, why: "Images aren't focusable by default; tabIndex 0 puts them in the tab order." },
    { id: "q91", q: "In the shopping list, what does input.focus() do after adding an item?", opts: ["Clears the input", "Puts the cursor back in the input", "Submits the form"], a: 1, why: "People can type the next item straight away." },
'''
write("core-creating-elements.html", h, b, "\n" + RUNNER + "<script>" + first + js + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_c + "\n" + ex_g + "</script>\n")
