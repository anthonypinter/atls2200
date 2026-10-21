/* The book manifest: the single source of truth for the reading order.
   index.html (table of contents), js/chrome.js (sidebar, breadcrumbs, prev/next) and scripts/check.mjs all read it.
   To add a lesson: create <slug>.html (start from an existing lesson), then add one line below in reading order.
   Lesson fields: slug (file name without .html), title, desc (one sentence for the contents card),
   props (3–4 code chips), mini (diagram key in index.html). Optional, added as lessons move to the textbook format
   (templates/lesson.html): minutes, the time to read and work through the whole lesson. Learning objectives live in
   each lesson page, in its header.
   related (optional): slugs of lessons to suggest under "Related lessons". List each pair once: the link appears on
   both lessons. The last entry in each part is its review page (a recap, a mini project and a mixed quiz).
   Lessons are numbered <part>.<position>, e.g. 3.1 is the first lesson in Part 3.
   backend: the Supabase project for student accounts and instructor notes (see supabase/README.md). Leave url empty
   and the book runs with no accounts, saving progress in each browser only. The anon key is meant to be public:
   row-level security decides what each person can read. Never put the service_role key here. */
window.BOOK = {
  title: "HTML, CSS & JS Field Guide",
  backend: { url: "", anonKey: "", emailDomain: "colorado.edu" },
  parts: [
    { title: "HTML Foundations", blurb: "Structure and meaning before any styling.", lessons: [
      { slug: "how-the-web-works", title: "How the Web Works", minutes: 20, mini: "web", desc: "Browsers, servers and URLs, what happens when a page loads, and setting up your editor.", props: ["URL", "404", "file://"], related: ["links-paths", "publishing"] },
      { slug: "html-syntax", title: "HTML Syntax", minutes: 20, mini: "syntax", desc: "Elements, tags and attributes, plus how whitespace and special characters behave.", props: ["<tag>", "attribute", "&amp;"], related: ["document-structure", "validation"] },
      { slug: "document-structure", title: "Document Structure", minutes: 15, mini: "doc", desc: "The skeleton every page needs: doctype, head, body, and how they nest.", props: ["<!DOCTYPE>", "<head>", "<meta>"], related: ["head-metadata"] },
      { slug: "head-metadata", title: "The Head & Metadata", minutes: 20, mini: "head", desc: "Page titles, favicons, meta descriptions, and the preview card when a link is shared.", props: ["<title>", "favicon", "og:image"], related: ["media-queries"] },
      { slug: "text-semantics", title: "Text Semantics", minutes: 20, mini: "textsem", desc: "Headings, strong vs b, em vs i, quotes, code and more, chosen for meaning.", props: ["<h1>–<h6>", "<strong>", "<blockquote>"], related: ["semantic-elements", "typography", "accessibility"] },
      { slug: "lists", title: "Lists", minutes: 20, mini: "lists", desc: "Unordered, ordered and description lists, nesting, and styling markers.", props: ["<ul>", "<ol>", "<dl>"], related: ["semantic-elements", "pseudo-classes"] },
      { slug: "semantic-elements", title: "Semantic Elements", minutes: 20, mini: "sem", desc: "When to use header, nav, main, section, and article instead of div.", props: ["<main>", "<nav>", "<section>"], related: ["accessibility"] },
      { slug: "links-paths", title: "Links & Paths", minutes: 20, mini: "links", desc: "Relative paths, ../, and why a link works on your laptop but not online.", props: ["href", "../", "#anchor"], related: ["publishing", "backgrounds-borders"] },
      { slug: "tables", title: "Tables", minutes: 20, mini: "table", desc: "Header cells, spanning cells and footers for real data, and when not to use a table.", props: ["<th>", "colspan", "scope"], related: ["overflow"] },
      { slug: "forms", title: "Forms & Inputs", minutes: 30, mini: "form", desc: "Labels, input types, fieldsets, validation rules, and where the data goes.", props: ["<label>", "<fieldset>", "method"], related: ["form-styling", "js-events"] },
      { slug: "images", title: "Images & Alt Text", minutes: 20, mini: "img", desc: "Adding images, writing useful alt text, and captioning with figure and figcaption.", props: ["<img>", "alt", "<figure>"], related: ["image-formats", "responsive-images", "accessibility"] },
      { slug: "image-formats", title: "Image Formats", minutes: 20, mini: "fmt", desc: "JPG vs PNG vs SVG vs WebP, real file sizes, and resizing before you upload.", props: ["JPG", "SVG", "WebP"], related: ["responsive-images", "picture"] },
      { slug: "video-audio", title: "Video & Audio", minutes: 15, mini: "video", desc: "Player attributes, why autoplay gets blocked, and adding captions.", props: ["<video>", "controls", "<track>"], related: ["embeds", "sizing"] },
      { slug: "embeds", title: "Embeds & iframes", minutes: 20, mini: "embed", desc: "Put YouTube videos and Google Maps on your page, and make them fit on phones.", props: ["<iframe>", "title", "aspect-ratio"], related: ["sizing"] },
      { slug: "review-html", title: "Review: HTML Foundations", minutes: 45, mini: "review", desc: "Build a trail page from plain text. Then a mixed quiz on the whole part.", props: ["recap", "mini project", "10 questions"] },
    ]},
    { title: "CSS Basics", blurb: "How the browser decides what each element looks like.", lessons: [
      { slug: "css-basics", title: "How CSS Is Applied", minutes: 15, mini: "cssbasics", desc: "The parts of a rule, and external vs internal vs inline styles.", props: ["selector", "declaration", "<link>"], related: ["selectors", "cascade", "devtools"] },
      { slug: "selectors", title: "Selectors & Specificity", minutes: 25, mini: "sel", desc: "Classes, IDs, combinators and attribute selectors, and why one rule beats another.", props: [".class", "h2 + p", "[href]"], related: ["cascade", "pseudo-classes", "organizing-css", "js-dom"] },
      { slug: "pseudo-classes", title: "Pseudo-classes & States", minutes: 25, mini: "pseudo", desc: "Hover, focus and link states, nth-child, and building a nav menu.", props: [":hover", ":focus-visible", ":nth-child"], related: ["pseudo-elements", "transitions", "form-styling"] },
      { slug: "pseudo-elements", title: "Pseudo-elements", minutes: 15, mini: "pseudoel", desc: "Decorate with ::before and ::after, drop caps, placeholders and selections.", props: ["::before", "content", "::first-letter"] },
      { slug: "cascade", title: "Cascade & Inheritance", minutes: 20, mini: "cascade", desc: "Which styles pass down to children, and how the browser settles conflicts.", props: ["inherit", "!important", "order"], related: ["css-variables", "devtools"] },
      { slug: "box-model", title: "The Box Model", minutes: 20, mini: "box", desc: "Content, padding, border, margin, and why your 300px box is 352px wide.", props: ["padding", "margin", "box-sizing"], related: ["display", "sizing", "devtools"] },
      { slug: "display", title: "Display Types", minutes: 20, mini: "display", desc: "Block vs inline vs inline-block, and why width does nothing on a span.", props: ["block", "inline", "inline-block"], related: ["flexbox", "grid"] },
      { slug: "sizing", title: "Sizing Items", minutes: 20, mini: "sizing", desc: "Fixed vs flexible widths, min and max limits, aspect-ratio and vh.", props: ["max-width", "min-height", "aspect-ratio"], related: ["fluid-sizing", "overflow", "colors-units"] },
      { slug: "overflow", title: "Overflow", minutes: 20, mini: "overflow", desc: "Content that doesn't fit, and hunting down sideways scrolling.", props: ["overflow", "text-overflow", "overflow-wrap"] },
      { slug: "colors-units", title: "Colors & Units", minutes: 20, mini: "color", desc: "px, rem, %, vw, and the many ways to write a color.", props: ["rem", "vw", "hsl()"], related: ["css-variables", "fluid-sizing", "typography"] },
      { slug: "css-variables", title: "CSS Variables", minutes: 20, mini: "vars", desc: "Store a value once and reuse it everywhere, including a dark theme.", props: ["--brand", "var()", ":root"], related: ["organizing-css"] },
      { slug: "backgrounds-borders", title: "Backgrounds & Borders", minutes: 20, mini: "bg", desc: "Gradients, background images, layering, borders and rounded corners.", props: ["linear-gradient", "background-size", "border-radius"], related: ["shadows"] },
      { slug: "shadows", title: "Shadows & Filters", minutes: 15, mini: "shadow", desc: "box-shadow, text-shadow on photos, drop-shadow, and other filters.", props: ["box-shadow", "text-shadow", "filter"], related: ["transforms"] },
      { slug: "typography", title: "Typography", minutes: 20, mini: "type", desc: "Fonts, sizes, line height, and making text easy to read.", props: ["font-family", "line-height"], related: ["web-fonts"] },
      { slug: "web-fonts", title: "Web Fonts", minutes: 20, mini: "fonts", desc: "Loading fonts from Google Fonts, fallbacks, and what happens while they load.", props: ["@font-face", "font-display", "fallback"] },
      { slug: "review-css", title: "Review: CSS Basics", minutes: 45, mini: "review", desc: "Style a trail card with variables, states and the box model. Then a mixed quiz on the whole part.", props: ["recap", "mini project", "10 questions"] },
    ]},
    { title: "Layout", blurb: "Putting boxes where you want them.", lessons: [
      { slug: "flexbox", title: "Flexbox", minutes: 25, mini: "flex", desc: "Line items up in a row or column, then space and align them.", props: ["display: flex", "justify-content", "align-items", "gap"], related: ["grid", "flex-vs-grid"] },
      { slug: "grid", title: "CSS Grid", minutes: 25, mini: "grid", desc: "Rows and columns at the same time, with items that span cells.", props: ["grid-template-columns", "fr", "span"], related: ["flex-vs-grid", "media-queries"] },
      { slug: "flex-vs-grid", title: "Flexbox vs Grid", minutes: 15, mini: "fvg", desc: "Six real layouts built both ways, and which one fits each job.", props: ["flex", "grid", "when to use"] },
      { slug: "floats", title: "Floats", minutes: 15, mini: "float", desc: "Wrap text around an image, clear floats, and fix collapsing parents.", props: ["float", "clear", "flow-root"], related: ["images", "flex-vs-grid"] },
      { slug: "positioning", title: "Positioning", minutes: 20, mini: "pos", desc: "relative, absolute, fixed, and sticky, and what each one is relative to.", props: ["position", "top", "z-index"], related: ["transforms"] },
      { slug: "review-layout", title: "Review: Layout", minutes: 45, mini: "review", desc: "Lay out a trail guide page with Flexbox, Grid and positioning. Then a mixed quiz on the whole part.", props: ["recap", "mini project", "10 questions"] },
    ]},
    { title: "Responsive Design", blurb: "One page that works on a phone and a laptop.", lessons: [
      { slug: "media-queries", title: "Media Queries", minutes: 20, mini: "mq", desc: "Change a layout at specific screen widths with breakpoints.", props: ["@media", "min-width", "breakpoints"], related: ["mobile-first", "fluid-sizing"] },
      { slug: "responsive-images", title: "Responsive Images", minutes: 20, mini: "rimg", desc: "Images that shrink to fit and never overflow their container.", props: ["max-width", "srcset", "object-fit"], related: ["picture"] },
      { slug: "picture", title: "Picture & Lazy Loading", minutes: 25, mini: "pic", desc: "The sizes attribute, different crops with picture, and loading images only when needed.", props: ["sizes", "<picture>", "loading=\"lazy\""] },
      { slug: "mobile-first", title: "Mobile-First Workflow", minutes: 20, mini: "mf", desc: "Write the phone layout first, then add complexity as screens grow.", props: ["min-width", "viewport meta"], related: ["devtools"] },
      { slug: "fluid-sizing", title: "Fluid Sizing", minutes: 20, mini: "fluid", desc: "Sizes that scale smoothly between limits with clamp(), min(), max() and calc().", props: ["clamp()", "min()", "calc()"] },
      { slug: "review-responsive", title: "Review: Responsive Design", minutes: 45, mini: "review", desc: "Build a responsive profile card. Then a mixed quiz on the whole part.", props: ["recap", "mini project", "10 questions"] },
    ]},
    { title: "Polish & Workflow", blurb: "Finishing touches, debugging, and getting your site online.", lessons: [
      { slug: "transforms", title: "Transforms", minutes: 15, mini: "tf", desc: "Move, rotate, scale and skew elements without disturbing the layout around them.", props: ["translate", "rotate", "transform-origin"], related: ["transitions"] },
      { slug: "transitions", title: "Transitions & Animations", minutes: 20, mini: "motion", desc: "Smooth state changes and keyframe animations, with timing curves.", props: ["transition", "@keyframes", "ease"] },
      { slug: "form-styling", title: "Styling Forms", minutes: 20, mini: "fstyle", desc: "Turn a default form into a polished one, one layer at a time.", props: ["font: inherit", "accent-color", ":user-invalid"], related: ["accessibility"] },
      { slug: "accessibility", title: "Accessibility Basics", minutes: 25, mini: "a11y", desc: "Seven common problems on one page, and how to find and fix them.", props: ["keyboard", "focus", "contrast"] },
      { slug: "organizing-css", title: "Organizing CSS", minutes: 20, mini: "organize", desc: "Sections, comments, purposeful class names and BEM, and variables.", props: ["comments", "BEM", "naming"] },
      { slug: "devtools", title: "Debugging with DevTools", minutes: 25, mini: "devtools", desc: "Read the Styles pane, spot crossed-out rules, and fix three real bugs.", props: ["Inspect", "Styles", "box model"] },
      { slug: "validation", title: "Validating Your Code", minutes: 15, mini: "valid", desc: "Use the W3C validators, spot common errors, and see how browsers repair bad HTML.", props: ["W3C", "errors", "Elements panel"], related: ["devtools", "js-errors"] },
      { slug: "publishing", title: "Project Structure & Publishing", minutes: 25, mini: "publish", desc: "Name and organize files, then publish with GitHub Pages.", props: ["index.html", "folders", "GitHub Pages"] },
      { slug: "review-polish", title: "Review: Polish & Workflow", minutes: 45, mini: "review", desc: "Polish a sign-up section until it's accessible, consistent and smooth. Then a mixed quiz on the whole part.", props: ["recap", "mini project", "10 questions"] },
    ]},
    { title: "JavaScript Basics", blurb: "The core language: storing values, making decisions, repeating work and reusing code.", lessons: [
      { slug: "js-intro", title: "What Is JavaScript?", minutes: 15, mini: "jsintro", desc: "What JavaScript adds to HTML and CSS, and where the script tag goes so your code can find the page.", props: ["<script>", "defer", "type=\"module\""], related: ["js-errors", "js-dom"] },
      { slug: "js-errors", title: "The Console & Errors", minutes: 20, mini: "jserr", desc: "Read error messages, find the line that's really broken, and debug with console.log().", props: ["console.log()", "TypeError", "SyntaxError"], related: ["devtools"] },
      { slug: "js-variables", title: "Variables & Data Types", minutes: 20, mini: "jsvar", desc: "let vs const, naming rules, and the difference between 42 and \"42\".", props: ["let", "const", "typeof"], related: ["js-strings-numbers", "js-functions"] },
      { slug: "js-strings-numbers", title: "Numbers & Strings", minutes: 20, mini: "jsstr", desc: "Math operators, why \"5\" + 5 is \"55\", template literals and string methods.", props: ["+", "`${ }`", ".slice()"] },
      { slug: "js-arrays", title: "Arrays", minutes: 20, mini: "jsarr", desc: "Lists of values with zero-based indexes, and the methods that add, remove and search.", props: ["[0]", ".push()", ".length"], related: ["js-loops", "js-objects-json"] },
      { slug: "js-conditionals", title: "Conditionals", minutes: 20, mini: "jsif", desc: "if, else if and else, comparing with ===, combining with && and ||, and truthy values.", props: ["if / else", "===", "&&"], related: ["js-loops"] },
      { slug: "js-loops", title: "Loops", minutes: 30, mini: "jsloop", desc: "Step through for, for...of and while loops, then let map() and filter() do the looping.", props: ["for...of", "for", ".map()"] },
      { slug: "js-functions", title: "Functions", minutes: 25, mini: "jsfn", desc: "Parameters, arguments and return values, arrow functions, and where variables can be seen.", props: ["function", "return", "=>"], related: ["js-events"] },
      { slug: "js-objects-json", title: "Objects & JSON", minutes: 25, mini: "jsobj", desc: "Group values under named keys, read nested data, and spot invalid JSON.", props: ["{ key: value }", "obj.key", "JSON.parse()"], related: ["js-fetch"] },
      { slug: "review-js", title: "Review: JavaScript Basics", minutes: 50, mini: "review", desc: "Write the functions behind a trail stats panel. Then a mixed quiz on the whole part.", props: ["recap", "mini project", "10 questions"] },
    ]},
    { title: "JavaScript in the Browser", blurb: "Find, change, build and load parts of a page while people use it.", lessons: [
      { slug: "js-dom", title: "Selecting & Changing Elements", minutes: 25, mini: "jsdom", desc: "Find elements with CSS selectors, explore the DOM tree, and change text, classes and styles.", props: ["querySelector()", "classList", "textContent"], related: ["js-events", "js-create-elements"] },
      { slug: "js-events", title: "Events", minutes: 25, mini: "jsevent", desc: "React to clicks, typing and form submits, and see how events bubble up to parents.", props: ["addEventListener", "preventDefault()", "event.target"], related: ["js-create-elements"] },
      { slug: "js-create-elements", title: "Creating & Removing Elements", minutes: 20, mini: "jscreate", desc: "Build MDN's shopping list: create elements, add them to the page, and remove them.", props: ["createElement()", "append()", "remove()"] },
      { slug: "js-fetch", title: "Fetching Data", minutes: 25, mini: "jsfetch", desc: "Load JSON from a server with fetch(), handle 404s and failures, and update the page.", props: ["fetch()", "async / await", "response.ok"], related: ["publishing"] },
      { slug: "review-browser", title: "Review: JavaScript in the Browser", minutes: 50, mini: "review", desc: "Build an interactive trail list: render, filter and mark items done. Then a mixed quiz on the whole part.", props: ["recap", "mini project", "10 questions"] },
    ]},
  ],
};
