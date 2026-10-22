# Interactive Textbook — Implementation Plan

Turn the **HTML, CSS & JS Field Guide** (60 standalone lesson pages) into an interactive textbook: a book you read in order, with chapters, a persistent table of contents, saved progress, inline exercises, and end-of-chapter checks. The goal is to keep what already works (hand-built playgrounds, plain HTML that students can view-source) and add a reading structure around it.

## Where things stand

| Area | Current state | Gap for a textbook |
| --- | --- | --- |
| Content | 60 lesson pages in 7 units (HTML Foundations → JavaScript), each with a playground, "Key ideas" and "Common mistakes" | Lessons are reference-style. They have no learning objectives, no longer explanatory prose, and no summary or exercises |
| Navigation | `index.html` card grid. Prev/next links are **hand-written in each page footer**. The unit/topic list lives only inside `index.html`'s `<script>` (`UNITS`) | No sidebar ToC, no chapter numbers, no "where am I", and three places to edit to reorder a lesson |
| Shared code | `style.css` (tokens, light/dark), `runner.js` (JS editor + console, `makeQuiz`) | Each page copies the `<head>`, crumbs and footer. Only 13 JS pages load `runner.js`, and there is no live HTML/CSS editor |
| Assessment | Multiple-choice quizzes on 12 pages, score not saved | Nothing persists. Most lessons have no checks, and there are no coding exercises with tests |
| Infra | No build step, ready for GitHub Pages. README is empty | No link checking, no a11y checks, no deploy workflow |

Known defect: `index.html` starts with a stray wrapper (`<!doctype html><html><head><meta charset=utf8>…<style>:root{color-scheme:light}…` with `<title>` inside `<body>`), probably left over from exporting it out of an artifact. That wrapper forces light mode and breaks the dark theme. Fix it first.

## Architecture decisions

1. **Stay buildless.** Pages remain plain `.html` files served as-is from GitHub Pages. Students can view-source any page and learn from it, and that's part of the course. Shared chrome gets injected at runtime by one script. Moving to a static site generator (Eleventy) is only worth it if the runtime approach starts to strain. See Phase 6.
2. **One source of truth for the book's structure:** `book.js` exports the ordered parts, chapters and lessons, with titles, slugs, objectives and estimated time. The index, the sidebar, prev/next and progress all read from it.
3. **Progressive enhancement.** Every page must still read correctly with JS off. Injected chrome (sidebar, prev/next, progress) adds to the page and never replaces content.
4. **Progress is per-browser.** It is stored in `localStorage` (wrapped in try/catch) with no accounts or backend. Export/import of progress as JSON covers the case of a student switching machines.
5. **Reusable components live as small vanilla-JS modules** under `js/`, each driven by markup (`<div class="runner">`, `<div class="sandbox">`, `<div class="exercise">`). Pages opt in by using the class, the same way `runner.js` already works.

### Proposed file layout

```
index.html            → book cover + table of contents (rendered from book.js)
book.js               → the manifest: parts → chapters → lessons
js/
  chrome.js           → injects sidebar ToC, breadcrumbs, prev/next, progress bar, theme toggle
  progress.js         → localStorage read/write, "mark complete", quiz scores, export/import
  runner.js           → (moved) JS editor + console
  sandbox.js          → NEW: live HTML/CSS editor with an iframe preview
  quiz.js             → makeQuiz split out of runner.js, now saves results
  exercise.js         → NEW: coding exercise with hidden checks + hints
  glossary.js         → NEW: auto-link/hover definitions for glossary terms
style.css             → + sidebar layout, callouts, objectives, print styles
templates/lesson.html → copy-and-fill starter for new lessons
scripts/check.mjs     → link + manifest consistency checker (Node, no deps)
```

## Lesson anatomy (target)

Every lesson moves toward the same order. The existing playground stays at the center of it:

1. **Header**: chapter number, title, time estimate, *"You'll be able to…"* objectives (2–4)
2. **Read**: short explanatory prose with callouts (`.callout.note / .tip / .warn`)
3. **Play**: the existing playground
4. **Try it**: one or more `sandbox` (HTML/CSS) or `runner` (JS) editors with a task
5. **Key ideas / Common mistakes**: existing panels
6. **Check yourself**: quiz (saved), plus an optional graded `exercise`
7. **Footer**: "Mark complete", prev/next, "Related chapters", glossary terms used

---

## To-do list

### Phase 0 — Cleanup & foundations
- [x] Remove the stray wrapper from the top of `index.html` and give it a proper `<head>`
- [x] Write `README.md`: what this is, how to run locally (`python3 -m http.server`), how to add a lesson
- [x] Add `scripts/check.mjs` to find broken internal links, pages missing `<title>`/`lang`/viewport, and orphan pages not in the manifest
- [x] Add a GitHub Actions workflow that runs the checker on PRs and deploys to GitHub Pages on `main` (`.github/workflows/site.yml`; needs Settings → Pages → Source: GitHub Actions)

### Phase 1 — Book structure (single source of truth)
- [x] Create `book.js` from the `UNITS` array in `index.html`: parts → lessons with `slug`, `title`, `desc`, `props`, `mini` (`minutes` and `objectives` are documented as optional and get filled in during Phase 5)
- [x] Settle numbering: units map 1:1 to parts, and lessons are numbered `<part>.<position>` (e.g. 3.1 Flexbox), computed from `book.js`
- [x] Render the `index.html` ToC from `book.js` instead of the inline `UNITS`
- [x] Have `check.mjs` confirm every manifest slug exists and every lesson file is in the manifest

### Phase 2 — Shared reading chrome
- [x] `js/chrome.js`: collapsible sidebar ToC that highlights the current lesson, closes to a drawer below 1100px, and is keyboard- and screen-reader-friendly
- [x] Generate prev/next and breadcrumbs from `book.js`. Hand-written footers were replaced on all 60 pages with an empty `<footer data-book-nav>`. The static `.crumbs` nav stays as a no-JavaScript fallback (it holds no ordering, so it can't drift) and the script replaces it
- [x] "On this page" links in the sidebar under the current lesson, built from its section and notes headings
- [x] Theme toggle (light/dark/system) using the existing `data-theme` hook in `style.css`
- [x] Sidebar layout CSS in `style.css`, keeping the 1100px reading column
- [x] Print stylesheet: hide chrome, expand all panels, show link URLs

### Phase 3 — Progress & assessment
- [x] `js/progress.js`: lessons (`visited`, `completed`), quizzes (current answers, best score), an attempt log and the last lesson, under one `localStorage` key with every access in try/catch. Every record has `updatedAt`, and `Progress.merge()` combines two copies so a backend can sync later
- [x] "Mark complete" button on each lesson, plus checkmarks and per-part counts in the sidebar, and progress bars on the contents page. Open tabs update live
- [x] Split `makeQuiz` into `js/quiz.js` and persist results. Add "Retry" (keeps the best score) and restore saved answers when the page is revisited. All 16 quizzes use it, including the 4 hand-built ones (Tables, Text Semantics, Semantic Elements, Organizing CSS), and every question has a stable id
- [x] "Continue where you left off" on the cover page (or "Up next" when that lesson is already complete)
- [ ] ~~Export/import progress as a JSON file~~ Deferred: a backend that syncs through `Progress.merge()` replaces this. Revisit only if no backend is built

### Phase 4 — New interactive components
- [x] `js/sandbox.js`: HTML and CSS tabs (keyboard accessible), live preview in an iframe that runs no scripts and can't navigate, Reset, optional Show solution, shared editor behavior from `js/runner.js`
- [x] Moved `runner.js` to `js/runner.js`. `chrome.js` loads it, `js/sandbox.js` and the glossary pop-ups on demand, and queues `makeExercise()` calls until `js/exercise.js` arrives
- [x] `js/exercise.js`: task, starter code, hidden checks (console output and exposed functions for JS; the live preview's DOM, layout and computed styles for HTML/CSS), progressive hints, solution, Reset with undo. Drafts and passes are saved through `progress.js`. First two exercises are live: Flexbox (nav bar) and Loops (total miles)
- [x] `js/glossary.js`: definition pop-ups for bold glossary terms and `<span class="term">`. Terms moved to `glossary-terms.js` (shared with `glossary.html`, which now takes lesson titles from `book.js` and has an anchor per term). Opens on click or tap rather than hover, so it works the same on phones
- [x] Callout styles: note, tip, warn, try
- [x] Search across every lesson section and glossary term: `search-index.js` built by `check.mjs --write`, which the publish workflow runs before every deploy (a stale local copy is only a warning), loaded only when search opens. Search button, Ctrl/⌘ + K, or /; results link to sections

### Phase 5 — Content pass (the bulk of the work)
- [x] Create `templates/lesson.html` in the target lesson anatomy: header with objectives (reading time from `book.js`), Read (~300 words, glossary terms, one callout), Play, Practice, Key ideas / Common mistakes, Check yourself
- [x] Pilot the full anatomy on 3 lessons, one per kind: `box-model.html` (CSS concept), `flexbox.html` (layout playground), `js-loops.html` (JS stepper). Box Model gained an exercise and quiz, Flexbox a quiz, Loops its quiz moved to the end. The checker counts lessons in the format (3 of 60)
- [x] Add objectives (page header) and `minutes` (`book.js`) to the remaining 57 lessons
- [x] Convert each lesson to the template (objectives, Read, section labels, quiz at the end). All 7 parts done; the checker reports 60 of 60 in the format
- [x] Add a quiz to every lesson that had none: 166 new questions, with the correct answer spread across option positions. Organizing CSS keeps its two hand-built quizzes. JS lessons' "Check yourself" quizzes moved to the end
- [x] Add at least one graded exercise per lesson: all 60 have one (47 HTML/CSS, 13 JavaScript). Each was tested in headless Chrome: the starter code fails at least one check and the official solution passes all of them
- [x] End-of-part review page for each of the 7 parts (`review-*.html`, last in each part in `book.js`): a recap linking every lesson, a graded mini project that uses the whole part (Responsive Design's is the profile card), and a 10-question mixed quiz
- [x] Cross-link related chapters: `related` in `book.js` (each pair listed once), shown on both lessons as "Related lessons" above the footer. The checker confirms every related slug exists

### Phase 6 — Quality, accessibility & polish
- [x] Accessibility audit of the chrome and every component. axe-core (WCAG 2.1 A/AA plus best practices) ran on all 69 pages in light and dark themes: about 460 findings went to 0, apart from the deliberate teaching examples listed below. Fixes: one `<main class="wrap">` landmark per page (the checker now requires it), contrast tokens (`--fn` for code function names; darker dark-mode fills behind white text; `--good`), about 20 lesson-specific contrast fixes, dimmed "didn't run" code now uses the muted color instead of opacity, scroll boxes get `tabindex="0"` so they can be scrolled from the keyboard, a list, an ARIA role and a heading level. A scripted keyboard pass on every page checked the skip link, drawer focus in and out, Escape, `inert` behind the drawer, and that every control has a name. Results already used `aria-live`
  - Left on purpose (the lesson is about the mistake): the missing alt in the Images alt-text picker and the Accessibility "broken" sample, that sample's pale text, Forms' unlabeled checkbox, and the `<main>` inside the Selecting & Changing Elements demo page (students select `main > .card`)
  - [ ] VoiceOver pass (needs a person): ⌘F5 on a Mac, then on one lesson try VO + U (rotor) for landmarks and headings, open the drawer, answer a quiz question (feedback should be read), run an exercise check (the result should be read), and open a glossary pop-up
- [x] Respect `prefers-reduced-motion`: the global rule now covers `::before`/`::after` and smooth scrolling. JavaScript timers in playgrounds are user-started step-throughs, not decorative motion, so they stay
- [x] Mobile pass at 360px: no page scrolls sideways (fixed How the Web Works' table and long URLs in quiz questions). The drawer, editors and controls were checked on every page; small buttons in Cascade and DevTools were enlarged to at least 24px
- [x] Self-host the two Google Fonts (`fonts/`, Latin and Latin Extended only). Recursive's variable file is ~300 KB, the same file Google sent before
  - Service worker: not added. Lessons change during the semester, and a cached copy could show students last week's version until they reload twice. Revisit if offline reading becomes a real need
- [x] Performance check: every page loads under 150 KB on a first visit, not counting fonts (largest: Forms, 133 KB). Exercises (and the editors they need) start only when they scroll near the screen; `makeExercise.startAll()` starts them all, and runs before printing
- [x] Stop accidental infinite loops: student JavaScript gets a loop guard instead of a Worker, because many lessons need the page's `document`, which Workers don't have. Every `for`/`while` loop gets a check, inserted on the same line so error line numbers don't move, and a loop that runs 1.5 seconds without stopping throws a RangeError. Recursion was already safe (the browser stops it). If the rewrite ever fails to parse, the original code runs unguarded
- [x] Decide on Eleventy: **not now.** The things it would solve haven't been problems: `book.js` already drives the contents, numbering, sidebar and prev/next, and `scripts/check.mjs` catches head and script drift on every publish. Plain HTML files also keep "view source" useful for students. Reconsider if pages need shared markup that JavaScript can't add (for example, the header has to work without JavaScript), or if the head block changes often enough that editing 70 files is a chore

### Phase 7 — Instructor features (optional)
- [x] Instructor notes, kept in the backend instead of the pages: `instructor_notes` in Supabase, shown in the lesson only to signed-in instructors (row-level security refuses everyone else), edited on `instructor.html`
- [x] Student accounts (Supabase, @colorado.edu one-time link or code): progress syncs via `Progress.merge()`, signed-out use still works and is added on first sign-in, sign-out clears the browser's copy
- [x] Section-level tracking: each "On this page" section records first seen (3 s on screen) and first used (click/keypress/edit); finished sections get a ✓ in the sidebar
- [x] Instructor dashboard (`instructor.html`): class grid by part/lesson, per-student section detail with latest exercise code, CSV export, roster with roles and course sections
- [ ] Set up the Supabase project and paste its URL and anon key into `book.js` (steps in `supabase/README.md`, including custom SMTP)
- [ ] Test the backend end to end with a real project (sign-in on two devices, sync, notes, dashboard)
- [ ] Map lessons to course weeks/assignments in `book.js` and show a "This week" view on the cover
- [x] Printable/PDF chapter export: `print.html?part=N` or `?lesson=slug` builds one document from the finished lessons (header and objectives, Read, exercise tasks with starter code, Key ideas and Common mistakes, quiz), lists each playground under "Try it online" with the lesson's link, and ends with answers, hints and solutions (optional). Each lesson starts on a new page. Linked from the contents page ("Print this part") and each lesson's top bar. Loading lessons for printing doesn't count as a visit

---

## Open questions
- **Audience and pacing:** should the reading order follow the ATLS 2200 syllabus week by week, or the current topic order?
- **Grading:** will exercises stay self-check only, or does anything need to report to Canvas? Reporting would mean a backend, which this plan avoids.
- **Prose depth:** roughly how long should a "Read" section be: ~300 words, or closer to a full textbook section (1,000+)?

## Suggested order of work
Phase 0 → 1 → 2 gives a navigable "book" in a few sessions without touching lesson content. Phase 3 and the sandbox from Phase 4 make it interactive. Phase 5 is the long tail and can run in parallel, part by part, once the lesson template has settled after the pilot.
