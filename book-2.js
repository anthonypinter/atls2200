/* Book 2's manifest: Core Web Development, a textbook for ATLS 2200 that follows the 9-week plan in CURRICULUM.md and
   uses MDN Web Docs as its source material. Each week is a part. Each lesson takes its outline from the MDN page(s) in
   its mdn list and teaches them the Field Guide way: short reading, playgrounds, graded exercises and a quiz. from is
   the Field Guide lesson it replaces, whose playgrounds and exercises it adapts.

   Book 2 pages load this file instead of book.js; js/chrome.js reads it the same way (sidebar, breadcrumbs, prev/next,
   progress). Slugs start with "core-" so saved progress never mixes with the Field Guide's.
   Each week's lessons are in reading order. Lessons still to write are made with plan() and marked planned: true;
   js/chrome.js leaves them out of the sidebar and prev/next, and book-2.html shows them as "coming soon".
   When one is written, replace its plan() line with a full lesson entry in the same position. */
(function () {
  const MDN = "https://developer.mozilla.org/en-US/docs/";
  const L = MDN + "Learn_web_development/";
  const HTML = L + "Core/Structuring_content/", CSS = L + "Core/Styling_basics/", TEXT = L + "Core/Text_styling/",
    LAYOUT = L + "Core/CSS_layout/", JS = L + "Core/Scripting/", A11Y = L + "Core/Accessibility/";
  const plan = (title, from, ...mdn) => ({ title, from, mdn, planned: true });

  window.BOOK = {
    title: "Core Web Development",
    short: "Core Web Dev",
    home: "book-2.html",
    partLabel: "Week",
    search: false,          // search-index.js only covers the Field Guide so far
    index: "search-index-2.js",   // built by scripts/check.mjs --write; the instructor dashboard reads it to know what each lesson holds
    autoComplete: true,     // no Mark complete button: each lesson shows how much is done, and is complete at 100% (js/chrome.js)
    backend: { url: "https://ptbpvlpgkeexeravimyb.supabase.co", anonKey: "sb_publishable_XIPvbndBK5H6lbaNd5sDNg_66iyiHGy", emailDomain: "colorado.edu" },
    parts: [
      { title: "How the web works + HTML basics", deliverable: "A one-page site live on GitHub Pages",
        blurb: "What happens when a page loads, the grammar of HTML, and the elements for text, lists and links. Then put a page online.",
        lessons: [
          { slug: "core-how-the-web-works", title: "How the Web Works", from: "how-the-web-works", desc: "Clients and servers, DNS, HTTP and URLs: what happens between typing an address and seeing a page. Plus how to organize a site's files.", props: ["client", "DNS", "HTTP 404", "URL"], mdn: [L + "Getting_started/Web_standards/How_the_web_works", L + "Getting_started/Environment_setup/Dealing_with_files"] },
          { slug: "core-basic-html-syntax", title: "Basic HTML Syntax", from: "html-syntax",
            desc: "Elements, attributes and documents: the grammar every page is written in, and the characters that need escaping.",
            props: ["<p>", "attributes", "<!doctype html>", "&lt;"], mdn: [HTML + "Basic_HTML_syntax"] },
          { slug: "core-webpage-metadata", title: "What's in the Head?", from: "head-metadata",
            desc: "Titles, character sets, descriptions, icons, stylesheets and scripts: the page information nobody sees.",
            props: ["<title>", "<meta>", "<link>", "defer"], mdn: [HTML + "Webpage_metadata"] },
          { slug: "core-headings-paragraphs", title: "Headings and Paragraphs", from: "text-semantics", desc: "The six heading levels, building an outline that never skips a level, and why structure matters to readers and screen readers.", props: ["<h1>–<h6>", "<p>", "outline", "semantics"], mdn: [HTML + "Headings_and_paragraphs"] },
          { slug: "core-emphasis-advanced-text", title: "Emphasis and Advanced Text", from: "text-semantics", desc: "Emphasis and importance, then quotes, abbreviations, code, superscripts and dates: an element for every kind of text.", props: ["<em>", "<strong>", "<blockquote>", "<time>"], mdn: [HTML + "Emphasis_and_importance", HTML + "Advanced_text_features"] },
          { slug: "core-lists", title: "Lists", from: "lists", desc: "Unordered, ordered and description lists, nesting a list the right way, and the attributes that change how a list counts.", props: ["<ul>", "<ol>", "<li>", "<dl>"], mdn: [HTML + "Lists"] },
          { slug: "core-creating-links", title: "Creating Links", from: "links-paths", desc: "Links to pages, sites, spots on a page, files and email, with paths that find their target and text that says where it goes.", props: ["<a href>", "../", "#fragment", "mailto:"], mdn: [HTML + "Creating_links"] },
          { slug: "core-publishing", title: "Publishing Your Website", from: "publishing", desc: "Ways to put a site online, the Git words you need, a pre-flight check for broken paths, and publishing with GitHub Pages.", props: ["hosting", "commit", "GitHub Pages", "index.html"], mdn: [L + "Getting_started/Your_first_website/Publishing_your_website", L + "Core/Version_control"] },
          { slug: "core-debugging-html", title: "Debugging HTML", from: "validation", desc: "Syntax and logic errors, how browsers repair broken HTML, the DOM inspector, and reading a validator's messages.", props: ["DOM inspector", "validator", "nesting", "stray end tag"], mdn: [HTML + "Debugging_HTML"] },
        ] },
      { title: "HTML content", deliverable: "HTML review project (trail page)",
        blurb: "Page structure, images, tables, forms and media: the elements that carry a page's real content.",
        lessons: [
          { slug: "core-structuring-documents", title: "Structuring Documents", from: "semantic-elements", desc: "Header, nav, main, article, section, aside and footer: say what each part of the page is.", props: ["<header>", "<nav>", "<main>", "<article>"], mdn: [HTML + "Structuring_documents"] },
          { slug: "core-images", title: "HTML Images", from: "images", desc: "src paths, alt text, width and height, captions, and where images may come from.", props: ["<img>", "alt", "<figure>", "<figcaption>"], mdn: [HTML + "HTML_images"] },
          { slug: "core-image-formats", title: "Image File Formats", from: "image-formats", desc: "JPEG, PNG, WebP, AVIF, SVG and GIF: which to use when, and how to offer a fallback.", props: ["WebP", "SVG", "<picture>", "lossy"], mdn: [MDN + "Web/Media/Guides/Formats/Image_types"] },
          { slug: "core-table-basics", title: "Table Basics", from: "tables", desc: "Rows, cells and headers; spanning cells; styling columns; and when not to use a table.", props: ["<table>", "<tr>", "<td>", "colspan"], mdn: [HTML + "HTML_table_basics"] },
          { slug: "core-table-accessibility", title: "Accessible Tables", from: "tables", desc: "Captions, scope, headers and id, and row groups, so every cell makes sense out loud.", props: ["<caption>", "scope", "headers", "<thead>"], mdn: [HTML + "Table_accessibility"] },
          { slug: "core-forms", title: "Forms and Buttons", from: "forms", desc: "Button types, the anatomy of a form, labelled controls, and client-side validation.", props: ["<button>", "<form>", "<label>", "<input>"], mdn: [HTML + "HTML_forms"] },
          { slug: "core-video-audio", title: "Video and Audio", from: "video-audio", desc: "The video and audio elements, multiple sources, playback attributes and captions.", props: ["<video>", "<audio>", "<source>", "<track>"], mdn: [HTML + "HTML_video_and_audio"] },
          { slug: "core-svg-embeds", title: "SVG and Embedded Content", from: "embeds", desc: "Vector graphics with SVG, and iframes for videos, maps and other pages, safely.", props: ["<svg>", "viewBox", "<iframe>", "sandbox"], mdn: [HTML + "Including_vector_graphics_in_HTML", HTML + "General_embedding_technologies"] },
        ] },
      { title: "How CSS works", deliverable: "Style the Week 2 page",
        blurb: "Rules and selectors, the cascade, the box model and units, DevTools, and setting type.",
        lessons: [
          { slug: "core-what-is-css", title: "What is CSS?", from: "css-basics", desc: "Browser defaults, the parts of a rule, three places CSS can live, and a first look at selectors, @rules and shorthands.", props: ["selector", "property", "<link>", "/* */"], mdn: [CSS + "What_is_CSS", CSS + "Getting_started"] },
          { slug: "core-selectors", title: "Selectors", from: "selectors", desc: "Type, class and ID selectors, selector lists, attribute selectors and combinators: picking exactly the elements you mean.", props: [".class", "#id", "[href$=\".pdf\"]", "ul > li"], mdn: [CSS + "Basic_selectors", CSS + "Attribute_selectors", CSS + "Combinators"] },
          { slug: "core-cascade", title: "The Cascade", from: "cascade", desc: "Source order, specificity and inheritance: how CSS settles conflicts, and how to win without !important.", props: ["specificity", "inherit", "!important", "source order"], mdn: [CSS + "Handling_conflicts"] },
          { slug: "core-debugging-css", title: "Debugging CSS", from: "devtools", desc: "DevTools: the DOM versus view source, the Styles pane, live edits, and a checklist for CSS that will not apply.", props: ["DevTools", "Inspect", "Styles pane", "CSS.supports()"], mdn: [CSS + "Debugging_CSS"] },
          { slug: "core-box-model", title: "The Box Model", from: "box-model", desc: "Block and inline boxes, content, padding, border and margin, box-sizing, margin collapsing and inline-block.", props: ["padding", "margin", "box-sizing", "inline-block"], mdn: [CSS + "Box_model"] },
          { slug: "core-display-flow", title: "Display and Normal Flow", from: "display", desc: "How the browser lays out boxes by default, changing box types with display, and the tools that override normal flow.", props: ["normal flow", "display", "inline-block", "display: none"], mdn: [LAYOUT + "Introduction"] },
          { slug: "core-values-units", title: "Values and Units", from: "colors-units", desc: "Lengths, ems and rems, percentages, colours in every format, images, positions and math functions.", props: ["rem", "%", "hsl()", "calc()"], mdn: [CSS + "Values_and_units"] },
          { slug: "core-text-styling", title: "Fundamental Text Styling", from: "typography", desc: "Font stacks, size, weight, style and decoration; alignment, line height and spacing; and the font shorthand.", props: ["font-family", "line-height", "text-transform", "font"], mdn: [TEXT + "Fundamentals"] },
          { slug: "core-web-fonts", title: "Web Fonts", from: "web-fonts", desc: "@font-face, self-hosting and Google Fonts, font-display, fallbacks, and keeping font downloads small.", props: ["@font-face", "woff2", "font-display", "fallback"], mdn: [TEXT + "Web_fonts"] },
        ] },
      { title: "Visual styling & states", deliverable: "CSS review project (trail card)",
        blurb: "Hover and focus states, generated content, variables, backgrounds, shadows, motion, and styling forms.",
        lessons: [
          { slug: "core-pseudo-classes", title: "Pseudo-classes and Link States", from: "pseudo-classes", desc: "Position and user-action pseudo-classes, the five link states in order, and turning links into a menu.", props: [":hover", ":focus-visible", ":nth-child()", "a:visited"], mdn: [CSS + "Pseudo_classes_and_elements", TEXT + "Styling_links"] },
          { slug: "core-pseudo-elements", title: "Pseudo-elements", from: "pseudo-elements", desc: "Style parts of elements with ::first-line, ::first-letter and ::marker, and add decoration with ::before and ::after.", props: ["::before", "::after", "content", "::first-letter"], mdn: [CSS + "Pseudo_classes_and_elements"] },
          { slug: "core-custom-properties", title: "CSS Custom Properties", from: "css-variables", desc: "Store values once with --name and var(), override them per section, add fallbacks, and register typed properties.", props: ["--brand", "var()", ":root", "@property"], mdn: [MDN + "Web/CSS/Guides/Cascading_variables/Using_custom_properties"] },
          { slug: "core-backgrounds-borders", title: "Backgrounds and Borders", from: "backgrounds-borders", desc: "Background colours, images, gradients and layers; repeat, size, position and attachment; borders and rounded corners.", props: ["background", "linear-gradient()", "border", "border-radius"], mdn: [CSS + "Backgrounds_and_borders"] },
          { slug: "core-shadows-effects", title: "Shadows and Effects", from: "shadows", desc: "Box and text shadows, filters, blend modes, CSS shapes and gradient text.", props: ["box-shadow", "filter", "mix-blend-mode", "shape-outside"], mdn: [CSS + "Advanced_styling_effects"] },
          { slug: "core-transforms", title: "Transforms", from: "transforms", desc: "Translate, rotate, scale and skew; transform-origin and order; individual transform properties; and 3D perspective.", props: ["transform", "rotate", "transform-origin", "perspective"], mdn: [MDN + "Web/CSS/Guides/Transforms/Using"] },
          { slug: "core-transitions", title: "Transitions", from: "transitions", desc: "Smooth changes between states: transition properties, what can animate, display transitions, reduced motion and transition events.", props: ["transition", "ease-out", "@starting-style", "transitionend"], mdn: [MDN + "Web/CSS/Guides/Transitions/Using"] },
          { slug: "core-styling-lists-tables-forms", title: "Styling Lists, Tables and Forms", from: "form-styling", desc: "List markers and spacing, readable data tables, images that fit their boxes, and form controls that match the page.", props: ["list-style", "border-collapse", "object-fit", "font: inherit"], mdn: [TEXT + "Styling_lists", CSS + "Tables", CSS + "Images_media_forms", L + "Extensions/Forms/Styling_web_forms"] },
        ] },
      { title: "Layout", deliverable: "Layout review project",
        blurb: "Sizing and overflow, then laying boxes out with flexbox, grid, positioning and floats.",
        lessons: [
          { slug: "core-sizing", title: "Sizing", from: "sizing", desc: "Intrinsic and extrinsic sizes, percentages (including margins and padding), min- and max- sizes, images that fit, and viewport units.", props: ["max-width", "min-height", "padding: 10%", "vh"], mdn: [CSS + "Sizing"] },
          { slug: "core-overflow", title: "Overflow", from: "overflow", desc: "Why CSS shows overflow by default, the overflow values, each axis on its own, hidden vs clip, and finding the element that makes a page scroll sideways.", props: ["overflow: auto", "overflow: clip", "overflow-x", "text-overflow"], mdn: [CSS + "Overflow"] },
          { slug: "core-flexbox", title: "Flexbox", from: "flexbox", desc: "The flex model, direction and wrapping, sharing space with the flex shorthand, alignment, ordering, and nested flex containers.", props: ["display: flex", "flex: 1", "justify-content", "align-self"], mdn: [LAYOUT + "Flexbox"] },
          { slug: "core-grid", title: "Grid", from: "grid", desc: "Tracks, fr and gaps, explicit and implicit grids, minmax(), placing items by line number and by named areas, and subgrid.", props: ["grid-template-columns", "minmax()", "grid-column: 1 / -1", "grid-template-areas"], mdn: [LAYOUT + "Grids"] },
          { slug: "core-flex-or-grid", title: "Flexbox or Grid?", from: "flex-vs-grid", desc: "One dimension or two, content out or layout in: choosing the right tool for a layout, and nesting flex containers inside a grid.", props: ["1D vs 2D", "content out", "layout in", "margin-top: auto"], mdn: [LAYOUT + "Flexbox", LAYOUT + "Grids"] },
          { slug: "core-positioning", title: "Positioning", from: "positioning", desc: "Static, relative, absolute, fixed and sticky; positioning contexts and z-index; and practical examples: stacked tab panels and a sliding panel.", props: ["position: absolute", "position: sticky", "z-index", "top / left"], mdn: [LAYOUT + "Positioning", LAYOUT + "Practical_positioning_examples"] },
          { slug: "core-floats", title: "Floats (optional)", from: "floats", desc: "Wrapping text around an image, why text runs behind a float, clearing floats, and containing them with display: flow-root.", props: ["float", "clear", "shape-outside", "display: flow-root"], mdn: [LAYOUT + "Floats"] },
        ] },
      { title: "Responsive + quality", deliverable: "Midterm: responsive multi-page site, accessibility-checked and published",
        blurb: "Pages that work on any screen, images that load the right size, accessibility, and CSS you can maintain.",
        lessons: [
          { slug: "core-media-queries", title: "Media Queries", from: "media-queries", desc: "Media types and features, range syntax, and/or/not logic, choosing breakpoints, mobile-first queries, and when you need no query at all.", props: ["@media", "(width >= 600px)", "(hover: hover)", "viewport meta"], mdn: [LAYOUT + "Media_queries"] },
          { slug: "core-mobile-first", title: "Responsive Design and Mobile First", from: "mobile-first", desc: "Fluid layouts, flexible media and media queries; flexbox and grid that adapt; the viewport meta tag; and building a page mobile first.", props: ["fluid layout", "flex: 1", "viewport meta", "min-width"], mdn: [LAYOUT + "Responsive_Design", LAYOUT + "Mobile-first_challenge"] },
          { slug: "core-fluid-sizing", title: "Fluid Sizing", from: "fluid-sizing", desc: "Responsive typography with media queries and viewport units, why vw alone breaks zoom, and clamp(), min(), max() and calc().", props: ["clamp()", "calc()", "min()", "vw + rem"], mdn: [LAYOUT + "Responsive_Design", CSS + "Values_and_units"] },
          { slug: "core-responsive-images", title: "Responsive Images", from: "responsive-images", desc: "Resolution switching with srcset and sizes, x descriptors for fixed-size images, art direction with picture, and lazy loading.", props: ["srcset", "sizes", "<picture>", "loading=\"lazy\""], mdn: [MDN + "Web/HTML/Guides/Responsive_images"] },
          { slug: "core-accessibility", title: "Accessibility Essentials", from: "accessibility", desc: "Who accessibility is for, WCAG and the accessibility tree, semantic HTML, contrast, focus, hiding content properly, and keyboard-friendly JavaScript.", props: ["semantic HTML", "alt", "4.5 : 1", ":focus-visible"], mdn: [A11Y + "What_is_accessibility", A11Y + "HTML", A11Y + "CSS_and_JavaScript"] },
          { slug: "core-organizing-css", title: "Organizing CSS", from: "organizing-css", desc: "Style guides, formatting and comments, logical sections, low specificity, splitting stylesheets, BEM and other methodologies, and build tools like Sass.", props: ["/* || */", "BEM", "low specificity", "Sass"], mdn: [CSS + "Organizing"] },
        ] },
      { title: "JS fundamentals I", deliverable: "Small console exercises",
        blurb: "What JavaScript is, fixing it when it breaks, and the first building blocks: variables, numbers, strings, arrays and decisions.",
        lessons: [
          { slug: "core-what-is-javascript", title: "What is JavaScript?", from: "js-intro", desc: "What JavaScript adds to a page, how the browser runs it, adding scripts with defer or modules, and a first look at a small program.", props: ["<script defer>", "addEventListener", "running order", "// comments"], mdn: [JS + "What_is_JavaScript", JS + "A_first_splash"] },
          { slug: "core-troubleshooting-js", title: "Troubleshooting JavaScript", from: "js-errors", desc: "Syntax, runtime and logic errors; reading the console; linting, the Console API and the debugger; and handling errors with throw and try...catch.", props: ["console.log()", "TypeError", "debugger", "try...catch"], mdn: [JS + "What_went_wrong", JS + "Debugging_JavaScript"] },
          { slug: "core-variables", title: "Variables", from: "js-variables", desc: "Declaring, initializing and updating variables, naming rules, why to avoid var, the main types of value, typeof, and choosing const or let.", props: ["let", "const", "typeof", "camelCase"], mdn: [JS + "Variables"] },
          { slug: "core-numbers-strings", title: "Numbers and Strings", from: "js-strings-numbers", desc: "Arithmetic, precedence, increment, assignment and comparison operators; template literals and conversion; and the most useful string methods.", props: ["% and **", "===", "`${}`", "slice()"], mdn: [JS + "Math", JS + "Strings", JS + "Useful_string_methods"] },
          { slug: "core-arrays", title: "Arrays", from: "js-arrays", desc: "Creating arrays, indexes and length, adding and removing items, for...of, map() and filter(), and converting with split() and join().", props: ["[0]", "push()", "map()", "split()"], mdn: [JS + "Arrays"] },
          { slug: "core-conditionals", title: "Conditionals", from: "js-conditionals", desc: "if, else if and else; truthy and falsy; nesting; &&, || and !; switch statements; and the ternary operator.", props: ["if / else", "&& ||", "switch", "? :"], mdn: [JS + "Conditionals"] },
        ] },
      { title: "JS fundamentals II + the DOM", deliverable: "JS review project (trail stats)",
        blurb: "Loops, functions and objects, then reaching into the page with the DOM.",
        lessons: [
          { slug: "core-loops", title: "Loops", from: "js-loops", desc: "for...of, map() and filter(), the standard for loop, break and continue, while and do...while, and choosing the right loop.", props: ["for...of", "for (let i…)", "break", "while"], mdn: [JS + "Loops"] },
          { slug: "core-functions", title: "Functions", from: "js-functions", desc: "Built-in functions and methods, parameters and defaults, anonymous and arrow functions, scope, building your own function and return values.", props: ["function", "parameters", "=>", "return"], mdn: [JS + "Functions", JS + "Build_your_own_function", JS + "Return_values"] },
          { slug: "core-objects-json", title: "Objects and JSON", from: "js-objects-json", desc: "Object literals, dot and bracket notation, setting members, this, constructors, JSON structure and rules, and JSON.parse() and JSON.stringify().", props: ["{ key: value }", "this", "new", "JSON.parse"], mdn: [JS + "Object_basics", JS + "JSON"] },
          { slug: "core-dom-scripting", title: "DOM Scripting", from: "js-dom", desc: "window, navigator and document, the DOM tree, querySelector() and textContent, creating, moving and removing nodes, and changing styles with classList and style.", props: ["querySelector()", "textContent", "appendChild()", "classList"], mdn: [JS + "DOM_scripting"] },
        ] },
      { title: "Interactive pages", deliverable: "Final: add interactivity to the midterm site",
        blurb: "Responding to clicks and typing, building elements from data, and loading data from a server.",
        lessons: [
          { slug: "core-events", title: "Events", from: "js-events", desc: "addEventListener() and removing listeners, other events, event objects, preventDefault(), bubbling and capture, and event delegation.", props: ["addEventListener()", "e.target", "preventDefault()", "bubbling"], mdn: [JS + "Events", JS + "Event_bubbling"] },
          { slug: "core-creating-elements", title: "Creating Elements", from: "js-create-elements", desc: "createElement(), appendChild() and remove(), textContent versus innerHTML, MDN's dynamic shopping list, and an image gallery built from data.", props: ["createElement()", "appendChild()", "remove()", "tabIndex"], mdn: [JS + "DOM_scripting", JS + "Image_gallery"] },
          { slug: "core-fetching-data", title: "Fetching Data", from: "js-fetch", desc: "The Fetch API, promises and .then(), fetching text and JSON, response.ok and error handling, async and await, and XMLHttpRequest.", props: ["fetch()", ".then()", "response.json()", "await"], mdn: [JS + "Network_requests"] },
        ] },
    ],
  };
})();
