# 9-Week Curriculum

A week-by-week plan for teaching ATLS 2200 from the **HTML, CSS & JS Field Guide** (`book.js`). The book's 60 lessons come to about 26 hours of lesson time, roughly 3 hours a week over 9 weeks, so the plan regroups the existing lessons rather than adding new ones.

Lesson names below are slugs: `selectors` is `selectors.html`.

## Schedule

| Week | Theme | Lessons | Deliverable |
| --- | --- | --- | --- |
| **1** | How the web works + HTML basics | how-the-web-works, html-syntax, document-structure, head-metadata, text-semantics, lists, links-paths, **publishing**, validation | A one-page site live on GitHub Pages |
| **2** | HTML content | semantic-elements, images, image-formats, tables, forms, video-audio, embeds, review-html | HTML review project (trail page) |
| **3** | How CSS works | css-basics, selectors, cascade, **devtools**, box-model, display, colors-units, typography, web-fonts | Style the Week 2 page |
| **4** | Visual styling & states | pseudo-classes, pseudo-elements, css-variables, backgrounds-borders, shadows, transforms, transitions, form-styling, review-css | CSS review project (trail card) |
| **5** | Layout | sizing, overflow, flexbox, grid, flex-vs-grid, positioning, floats *(optional)*, review-layout | Layout review project |
| **6** | Responsive + quality | media-queries, mobile-first, fluid-sizing, responsive-images, picture, accessibility, organizing-css, review-responsive | **Midterm:** responsive multi-page site, accessibility-checked and published |
| **7** | JS fundamentals I | js-intro, js-errors, js-variables, js-strings-numbers, js-arrays, js-conditionals | Small console exercises |
| **8** | JS fundamentals II + the DOM | js-loops, js-functions, js-objects-json, review-js, js-dom | JS review project (trail stats) |
| **9** | Interactive pages | js-events, js-create-elements, js-fetch, review-browser | **Final:** add interactivity to the midterm site |

## How this differs from the book's order

- **Publishing moves to Week 1.** If students put their site on GitHub Pages from the start, every assignment after that is a URL you can open, and nobody's first deploy happens in a rush during finals.
- **DevTools moves to Week 3.** In the book it sits in Part 5 (Polish & Workflow), but students need it from their first CSS bug. Validation moves into Week 1 for the same reason.
- **Part 5 (Polish & Workflow) is split across other weeks.** Transforms, transitions and form-styling join visual styling in Week 4. Accessibility and organizing-css go into Week 6 so the midterm is checked against them. With that, `review-polish` becomes optional.
- **sizing and overflow move into Layout.** In the book they're in CSS Basics, but they make more sense next to Flexbox and Grid.

## Trade-offs and trims

At 9 weeks, JavaScript gets 3 weeks, and DOM work happens at the very end. If interactivity matters more than CSS depth, squeeze Weeks 3 and 4 into one and start JS in Week 6.

If lessons need to be trimmed, cut these first:

1. floats
2. picture
3. embeds
4. pseudo-elements
5. js-fetch (make it a stretch goal)

## Book 2

`book-2.js` (Core Web Development) follows MDN's Core module order and is still early, so this plan is built on the Field Guide. If Book 2 replaces it, the same weekly structure carries over. MDN's order matches it closely: Structuring content → CSS basics → text styling → layout → JavaScript.
