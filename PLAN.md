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
- [ ] Create `templates/lesson.html` in the target lesson anatomy
- [ ] Pilot the full anatomy on 3 lessons, one per kind: `box-model.html` (CSS concept), `flexbox.html` (layout playground), `js-loops.html` (JS stepper), then revise the template from what's learned
- [ ] Add objectives and time estimates to all 60 lessons (in `book.js` and the page header)
- [ ] Add a "Read" prose section to each lesson. Track it per part:
  - [ ] HTML Foundations (14)
  - [ ] CSS Basics (15)
  - [ ] Layout (5)
  - [ ] Responsive Design (5)
  - [ ] Polish & Workflow (8)
  - [ ] JavaScript Basics (9)
  - [ ] JavaScript in the Browser (4)
- [ ] Add a quiz to the 44 lessons that have none
- [ ] Add at least one graded exercise per lesson
- [ ] End-of-part review page: mixed quiz plus a mini project (e.g. "build a responsive profile card")
- [ ] Cross-link related chapters (e.g. Flexbox ↔ Grid ↔ Flex vs Grid)

### Phase 6 — Quality, accessibility & polish
- [ ] Accessibility audit of the chrome and every component (keyboard-only pass, VoiceOver pass, focus order, `aria-live` on results)
- [ ] Respect `prefers-reduced-motion` in playgrounds and transitions
- [ ] Mobile pass at 360px: sidebar drawer, editors, playground controls
- [ ] Self-host the two Google Fonts so the book works offline (optional service worker for full offline reading)
- [ ] Performance check: no page over ~150 KB before fonts, lazy-init editors below the fold
- [ ] Run student JavaScript (runner and exercises) in a Worker with a timeout, so an accidental infinite loop can't freeze the tab
- [ ] Decide whether to move templating to Eleventy (only if header/footer drift or manifest sync becomes painful)

### Phase 7 — Instructor features (optional)
- [ ] Instructor notes toggle (`?instructor=1` reveals `.instructor` blocks with answers and discussion prompts)
- [ ] Map lessons to course weeks/assignments in `book.js` and show a "This week" view on the cover
- [ ] Printable/PDF chapter export for students who need it

---

## Open questions
- **Audience and pacing:** should the reading order follow the ATLS 2200 syllabus week by week, or the current topic order?
- **Grading:** will exercises stay self-check only, or does anything need to report to Canvas? Reporting would mean a backend, which this plan avoids.
- **Prose depth:** roughly how long should a "Read" section be: ~300 words, or closer to a full textbook section (1,000+)?

## Suggested order of work
Phase 0 → 1 → 2 gives a navigable "book" in a few sessions without touching lesson content. Phase 3 and the sandbox from Phase 4 make it interactive. Phase 5 is the long tail and can run in parallel, part by part, once the lesson template has settled after the pilot.
