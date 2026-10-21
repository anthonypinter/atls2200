# HTML, CSS & JS Field Guide

An interactive textbook for ATLS 2200. It has 60 lessons in 7 parts, and each lesson is built around a hands-on playground: change a setting, watch the page respond, then try the idea in your own project.

The site is plain HTML, CSS and JavaScript with no build step and no dependencies, so any page can be opened with View Source and read like the lessons themselves.

## Run it locally

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

Opening `index.html` straight from the file system also works. Use a local server when testing anything that loads files, such as the Fetching Data lesson.

## How it fits together

| File | What it does |
| --- | --- |
| `book.js` | **The table of contents.** Parts and lessons in reading order. Lesson numbers (e.g. 3.1), the contents page, the sidebar, breadcrumbs and previous/next links all come from here. Each part ends with its review page (`review-*.html`), and a lesson's optional `related` list adds "Related lessons" links to both lessons |
| `js/progress.js` | Saved progress (visited and completed lessons, quiz answers, best scores) in `localStorage`. The only code that touches saved data, so a backend can sync it later via `Progress.merge()` |
| `js/chrome.js` | Adds the reading layout to every page: top bar, sidebar contents with "On this page" links and checkmarks, Mark complete, previous/next footer, search, theme toggle and print tweaks. Also loads the components below only on pages that use them |
| `js/quiz.js` | `makeQuiz(el, items)`: multiple-choice quizzes whose answers are saved and restored, with Retry |
| `index.html` | The cover and contents page, rendered from `book.js` (the small card diagrams live in its `minis` map) |
| `style.css` | Shared design tokens (light and dark), playground widgets, book chrome and print styles |
| `fonts/` | The two typefaces (Atkinson Hyperlegible and Recursive), served from the site itself so pages load nothing from Google and work offline once cached |
| `js/runner.js` | The runnable JavaScript editor with a console, plus `hlJS()` and the shared editor behavior. Student code runs with a loop guard: a loop that runs for 1.5 seconds without stopping is stopped with an error instead of freezing the tab |
| `js/sandbox.js` | Live HTML/CSS editor with a preview |
| `js/exercise.js` | `makeExercise(el, def)`: graded exercises with checks, hints and a solution; work and passes are saved. Each one starts when it scrolls near the screen, so pages load fast |
| `js/glossary.js` | Definition pop-ups for glossary terms in lesson text |
| `js/search.js` | The search dialog (Search button, Ctrl/⌘ + K, or /) |
| `glossary-terms.js` | All glossary terms, shared by `glossary.html`, the pop-ups and search |
| `print.html` | Printable chapters: a whole part (or one lesson) on one page, ready to print or save as a PDF, with quiz answers, hints and solutions at the end. Linked from each part on the contents page and from the Print link on every lesson. It only works when the book is served (GitHub Pages or a local server), not opened as a file |
| `glossary.html` | The glossary page. Each term has an anchor, e.g. `glossary.html#term-box-model` |
| `search-index.js` | **Generated.** GitHub rebuilds it every time it publishes, so the live site's search is always current. The copy in the repo is only for searching while testing locally. Don't edit by hand |
| `scripts/check.mjs` | Site checker, and builder for the search index (see below) |
| `PLAN.md` | The roadmap and to-do list for the textbook |

## Add or move a lesson

1. Copy `templates/lesson.html` to the site root as `<slug>.html` and follow the comments in it. `box-model.html`, `flexbox.html` and `js-loops.html` are finished examples. The template already has the shared scripts at the end of `<head>`, which must stay in this order:
   ```html
   <script src="book.js"></script>
   <script src="js/progress.js"></script>
   <script src="js/chrome.js"></script>
   <script src="js/quiz.js"></script>
   ```
   and leave the footer empty for the script to fill:
   ```html
   <footer class="page-foot" data-book-nav><a href="index.html">← Contents</a></footer>
   ```
2. Add one line to `book.js` where it belongs in the reading order. Numbering, the sidebar and previous/next update everywhere.
3. Add a card diagram to `minis` in `index.html` under the lesson's `mini` key.
4. For a quiz, add `<div class="panel quiz" id="quiz"></div>` and call `makeQuiz($("quiz"), [{ id: "q1", q, opts, a, why }, …])`. Give each question an `id` that never changes, even if you edit or reorder questions, so saved answers stay attached to the right question.
5. Run the checker if you have Node, or push and let GitHub run it. You don't need to rebuild the search index: GitHub does that when it publishes.

To reorder lessons, move their lines in `book.js`. Nothing else needs editing.

## Interactive pieces

Drop these into any lesson. Each one loads its own script, so there's nothing to add to `<head>`.

**Live HTML/CSS editor.** Either language can be left out. The solution is optional.
```html
<div class="sandbox" data-title="Trail card">
  <textarea data-lang="html"><p class="card">Mesa Trail</p></textarea>
  <textarea data-lang="css">.card { padding: 16px; }</textarea>
  <textarea data-solution="css" hidden>.card { padding: 16px; border-radius: 10px; }</textarea>
</div>
```

**JavaScript editor with a console:** `<div class="runner"><textarea>console.log("hi");</textarea></div>`

**Graded exercise.** Add `<div id="ex-nav"></div>` and call `makeExercise()` from the page's script. Checks are small functions that return true to pass. For HTML/CSS they inspect the live preview, so prefer measuring the result (positions, sizes, computed styles) over reading the student's CSS: then any working solution passes. Make each check test one step on its own, and try the starter code, the solution and a different correct solution before shipping. See the comment at the top of `js/exercise.js`, and the working examples in `flexbox.html` (HTML/CSS) and `js-loops.html` (JavaScript).

**Glossary term.** Bold text in the lede, section intros or Key ideas / Common mistakes that exactly matches a glossary term becomes a pop-up automatically. To mark one anywhere else, use `<span class="term">main axis</span>`, or `<span class="term" data-term="Box model">box model</span>` when the words differ from the glossary entry.

**Callout.** Kinds: `note`, `tip`, `warn`, `try`.
```html
<div class="callout tip"><p class="callout-title">Tip</p><p>Open DevTools and toggle the property on and off.</p></div>
```

## Check before you push

```sh
node scripts/check.mjs           # check everything
node scripts/check.mjs --write   # optional: also refresh search-index.js so search is current locally
```

The checker makes sure every lesson in `book.js` has a page, every page is in `book.js`, every page has the required `<head>` tags and scripts, every quiz question has a unique id, glossary terms are valid and link to real lessons, and no local link or image points at a missing file. GitHub Actions runs it on every push and pull request (`.github/workflows/site.yml`) and publishes `main` to GitHub Pages when it passes, rebuilding the search index first. Node is only needed for these checks; the site itself is plain files. If the committed search index is older than the lessons, the checker shows a warning rather than failing. For publishing to work, set **Settings → Pages → Source** to **GitHub Actions** once.
