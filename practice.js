/* Exercises & Quizzes: the scored weekly sets, separate from the practice inside Book 2's lessons. One set per week of
   Core Web Development (book-2.js), each a page of new graded exercises and a one-attempt quiz on that week's lessons.

   Pages load this file in place of book.js / book-2.js, so js/chrome.js gives them the sidebar, breadcrumbs, prev/next
   and progress like any lesson. scored: true changes three things (js/exercise.js, js/quiz.js, js/chrome.js):
   exercises have no Show solution and show their points; the quiz is makeQuiz(el, items, { once: true }), one
   attempt with Submit; and the footer shows the page's score instead of a progress meter.

   Scoring (Progress.score in js/progress.js): the quiz is worth 1 point a question, counting the first submitted
   attempt. Each exercise is worth 5 points, in proportion to the most checks one press of Check has passed.
   The instructor dashboard (instructor.html?book=3) reads search-index-practice.js, built by
   scripts/check.mjs --write, to know each set's exercises and number of quiz questions.

   covers lists the Book 2 lessons a set draws on; practice.html links to them. Slugs start with "practice-". */
(function () {
  window.BOOK = {
    title: "Exercises & Quizzes",
    short: "Exercises & Quizzes",
    home: "practice.html",
    partLabel: "Week",
    search: false,
    index: "search-index-practice.js",
    scored: true,
    // Must match book.js and book-2.js (scripts/check.mjs checks).
    backend: { url: "https://ptbpvlpgkeexeravimyb.supabase.co", anonKey: "sb_publishable_XIPvbndBK5H6lbaNd5sDNg_66iyiHGy" },
    parts: [
      { title: "How the web works + HTML basics", lessons: [
        { slug: "practice-week-1", title: "HTML Basics", desc: "Mark up a trail page: headings, emphasis and dates, lists and links. Quiz: requests, syntax, the head, publishing and debugging.",
          covers: ["core-how-the-web-works", "core-basic-html-syntax", "core-webpage-metadata", "core-headings-paragraphs", "core-emphasis-advanced-text", "core-lists", "core-creating-links", "core-publishing", "core-debugging-html"] },
      ] },
      { title: "HTML content", lessons: [
        { slug: "practice-week-2", title: "HTML Content", desc: "Landmarks, a captioned image, an accessible table and a labelled form. Quiz: image formats, media, embeds and tables.",
          covers: ["core-structuring-documents", "core-images", "core-image-formats", "core-table-basics", "core-table-accessibility", "core-forms", "core-video-audio", "core-svg-embeds"] },
      ] },
      { title: "How CSS works", lessons: [
        { slug: "practice-week-3", title: "How CSS Works", desc: "Selectors, winning the cascade without !important, a box that adds up, and readable type. Quiz: rules, specificity, units, DevTools and fonts.",
          covers: ["core-what-is-css", "core-selectors", "core-cascade", "core-debugging-css", "core-box-model", "core-display-flow", "core-values-units", "core-text-styling", "core-web-fonts"] },
      ] },
      { title: "Visual styling & states", lessons: [
        { slug: "practice-week-4", title: "Visual Styling and States", desc: "Link states and zebra stripes, a themeable button with custom properties, a decorated card, and motion that respects users. Quiz: states, effects and transitions.",
          covers: ["core-pseudo-classes", "core-pseudo-elements", "core-custom-properties", "core-backgrounds-borders", "core-shadows-effects", "core-transforms", "core-transitions", "core-styling-lists-tables-forms"] },
      ] },
      { title: "Layout", lessons: [
        { slug: "practice-week-5", title: "Layout", desc: "A flex nav bar, a grid gallery, a page laid out with named areas, and a badge pinned to a card. Quiz: sizing, overflow, flex, grid and positioning.",
          covers: ["core-sizing", "core-overflow", "core-flexbox", "core-grid", "core-flex-or-grid", "core-positioning", "core-floats"] },
      ] },
      { title: "Responsive + quality", lessons: [
        { slug: "practice-week-6", title: "Responsive and Accessible", desc: "A mobile-first layout, fluid headings, a responsive image and an accessibility repair job. Quiz: media queries, images, a11y and organizing CSS.",
          covers: ["core-media-queries", "core-mobile-first", "core-fluid-sizing", "core-responsive-images", "core-accessibility", "core-organizing-css"] },
      ] },
      { title: "JS fundamentals I", lessons: [
        { slug: "practice-week-7", title: "JavaScript Fundamentals I", desc: "Variables and template literals, string cleanup, array filtering and a decision function. Quiz: errors, types, operators and conditionals.",
          covers: ["core-what-is-javascript", "core-troubleshooting-js", "core-variables", "core-numbers-strings", "core-arrays", "core-conditionals"] },
      ] },
      { title: "JS fundamentals II + the DOM", lessons: [
        { slug: "practice-week-8", title: "JavaScript Fundamentals II and the DOM", desc: "Loops, functions with defaults and return values, objects and JSON, and changing a page with the DOM. Quiz: loops, scope, objects and the DOM.",
          covers: ["core-loops", "core-functions", "core-objects-json", "core-dom-scripting"] },
      ] },
      { title: "Interactive pages", lessons: [
        { slug: "practice-week-9", title: "Interactive Pages", desc: "A toggle, a list built from data, event delegation and loading JSON with fetch. Quiz: events, creating elements and fetching data.",
          covers: ["core-events", "core-creating-elements", "core-fetching-data"] },
      ] },
    ],
  };
})();
