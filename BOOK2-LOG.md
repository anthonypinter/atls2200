# Book 2 working log

Read this first when you pick up work on the site or on Book 2 (Core Web Development). It records what's been built, the decisions behind it, and how to keep building without starting from scratch.

Last updated: 2026-11-23 (Exercises & Quizzes added). All 9 weeks written (60 lessons). No `plan()` entries remain.

---

## What the site is

A plain HTML/CSS/JS course site (ATLS 2200). It has no build step. GitHub Actions runs `node scripts/check.mjs`, then publishes to GitHub Pages.

| Page | What it is |
|---|---|
| `index.html` | Landing page with three main buttons: **Field Guide** (→ `book.html`), **Exercises & Quizzes** (→ `practice.html`, the scored weekly sets, see below) and **Class is Live** (inactive). A secondary **Log in** button stays disabled until `BOOK.backend.url` is set. |
| `book.html` | The original textbook, the **Field Guide**, formerly `index.html`. Its manifest is `book.js`. |
| `book-2.html` | Book 2, **Core Web Development**. Its manifest is `book-2.js`. A 9-week course that follows MDN's *Learn web development: Core* module, with lessons built in the Field Guide's style. |
| `mdn-links.html` / `mdn-links.js` | The earlier "links out to MDN" reading list, kept as a separate page. |
| `CURRICULUM.md` | Your 9-week schedule. Book 2's weeks follow it. Its last paragraph, "Book 2", is now out of date. |

## Decisions and preferences (don't re-ask these)

- **Book 2 lessons are real modules, not link lists.** Each one has reading, interactive playgrounds, graded exercises and a quiz, like the Field Guide. MDN is the source material.
- **Each lesson follows its MDN page's section headings**, in MDN's order. It adapts the matching Field Guide lesson (the `from` slug), reusing its playgrounds and exercises where they fit and adding new ones for anything MDN covers that the Field Guide doesn't.
- **No "On MDN" box** in lessons (you asked for it to be removed).
- **No time estimates** on Book 2. `minutes` was removed from `book-2.js` and from the contents cards. `check.mjs` only requires `minutes` for Field Guide lessons. The Field Guide still shows its estimates.
- **No weekly review lessons** in Book 2. The Week 2 review was deleted and the planned "Week N Review" entries were removed. Each week's `deliverable` text, e.g. "CSS review project", is your class assignment, not a lesson.
- Don't commit unless asked. New files have been staged with `git add`.

## How Book 2 is wired

- **`book-2.js`** sets `window.BOOK`.
  - Settings: `home: "book-2.html"`, `short: "Core Web Dev"`, `partLabel: "Week"`, `search: false`. The backend URL is empty.
  - Each week has `title`, `deliverable`, `blurb` and an ordered `lessons` list.
  - A written lesson is `{ slug, title, from, desc, props: [4 short tags], mdn: [urls] }`.
  - A lesson not yet written is `plan("Title", "from-slug", ...mdnUrls)`, which marks it `planned: true`.
  - Constants for building MDN URLs: `MDN`, `L` (Learn), `HTML`, `CSS` (Styling_basics), `TEXT`, `LAYOUT`, `JS`, `A11Y`.
- **`js/chrome.js`** supports both books.
  - It adds the top bar, breadcrumbs (Course home › Core Web Dev › Week N · title › lesson), the sidebar contents, prev/next links and progress.
  - Planned lessons keep their number (`part.all`) but are hidden from navigation (`part.lessons`). Weeks with no written lessons are hidden.
- **`book-2.html`** shows written lessons as cards. Planned ones appear as dashed "N.N · Soon" cards with their MDN links.
- **`core.css`** holds styles shared by Book 2 lessons: `.two`, `textarea.src`/`input.src`, `.rendered`, `iframe.preview`, `.presets`/`.seg`, `.toggle`, `.verdict.ok/.bad`, `.tree`, `.mini-table` and similar. It also adds spacing for a `.prose` block that sits directly after a playground. Lessons load it after `style.css`.
- **`scripts/check.mjs`** validates both manifests.
  - A Book 2 page must load `book-2.js` in place of `book.js`.
  - `DEMO_LINKS` allowlists intentionally missing demo files, such as `trail-map.pdf` in the Selectors playground.
  - A clean run is now **0 errors, 0 warnings** (the old 9-error baseline files are gone). It also checks `practice.js`.

## Lesson page anatomy

```
<head> style.css, core.css, <style>…</style>, then book-2.js, js/progress.js, js/chrome.js, js/quiz.js
<main class="wrap">
  crumbs → page-head (h1, .lede, .objectives "You'll be able to")
  repeated: <div class="section-title"><span class="eyebrow">Read|Play|Practice</span><h2>MDN heading</h2><p>…</p></div>
            + .prose / playground / <div id="ex-…"></div>
  section.notes (Key ideas + Common mistakes) → Check yourself → #quiz → footer.page-foot[data-book-nav]
</main>
<script> playground code </script>
<script> makeExercise(el, {title, task, html, css, solution:{html|css}, hints, checks:[{label, test:({$,$$,style,code,doc})=>…}]}) … makeQuiz(el, [{id, q, opts, a, why}]) </script>
```

- In `checks`, `$$` returns an array, and a check that throws counts as a fail. The starter code must fail at least one check, and the solution must pass them all.
- `span.term` / `data-term` must name an existing entry in `glossary-terms.js`, or `check.mjs` reports an error.
- Write about 6 quiz questions per lesson, with unique ids.

## Gotchas learned the hard way

- **Live Server:** a literal `</body>`, `</head>` or `</html>` inside a JS string makes Live Server inject its script there, which dumps raw JS onto the page. Write them as `<\/body>`. **Never** blanket-replace `</`, because it breaks regexes like `/</g`. `tools/book2/adapt.py` escapes these automatically inside `<script>` blocks.
- `</script>` inside a JS string has to be written `<\/script>` too.
- Reusing class names from `style.css`, such as `.item` or `.tree`, causes style clashes. Use unique names in lesson CSS.
- When a playground copied from the Field Guide is combined with another one, check for clashing element `id`s (`w`, `p`, `b`, `sample`, `verdict` and so on) and rename them with a prefix.
- Some Field Guide pages have a second `<style id="…">` in the head, for example `pvstyle` in DevTools. Copy it across, or the playground breaks.
- A Field Guide script that binds `document.querySelectorAll("select, input")` (or `.controls select`) also catches new playgrounds' controls on the same page. That's harmless as long as its handler only redraws its own demo, but give new playgrounds their own id prefixes and classes (not `.stage`, which some Field Guide pages restyle).
- `testlesson.sh` checks exercises by loading every script block that contains `makeExercise(` or `makeQuiz(`. If a Field Guide playground script also calls `makeQuiz` (e.g. organizing-css's sorting quizzes), move those calls into the exercise script, or the checker crashes and prints raw code.
- Merging two Field Guide pages into one lesson (week6-l4 does responsive-images + picture): wrap each page's script in `(() => { … })();` and rename clashing element ids.
- Media-query exercise checks should accept range syntax too: normalise `(width >= 600px)` to `(min-width:600px)` before comparing `conditionText` (see week6-l1/l2).
- Chrome may use any `srcset` candidate that's already loaded, and data-URI images always are, so don't build a demo that relies on the browser's real `srcset` choice with data URIs.
- Chrome blockifies grid items, so a check like `display === "block"` passes in the starter too. Test the starter.
- JS lessons: a backtick or `${` inside an exercise's `js`/`solution`/`task` template literal must be written `` \` `` and `\${`, or the whole script fails to parse.
- A syntax error anywhere in a `runner()` block stops all of it running, so show "this would be an error" lines commented out, with an instruction to try them.
- `src.block()` ends at the first `\n  });\n`, which can be *inside* an exercise's solution (an event listener at two-space indent). If the page then has a syntax error, cut the block to the last `  });` before `</script>` instead (see week9-l1).
- To screenshot a section, the scratch `shotserver.py` approach works: serve the repo plus a wrapper page that iframes the lesson and scrolls to a heading. Python's `parse_qs` splits on `;`, so encode it as `%3B` in a click script.
- Screenshots in headless Chrome crop at phone width. That's an artifact of the screenshot tool, not a page bug.

## Tools (in `tools/book2/`)

| File | Purpose |
|---|---|
| `adapt.py` | Helpers for building a lesson from a Field Guide page. `Src(slug)` provides `.between(a, b)` to cut out HTML fragments, `.css()`, `.first_script()` and `.block("  makeExercise(…")`. The module also provides `head()`, `top()`, `ST()` (section title), `prose()`, `notes()` and `write()`, plus, for JS lessons, `runner(code)` (an editable code runner), `RUNNER` (the `js/runner.js` tag), `split_quiz(js)` (pulls the Field Guide quiz out of a playground script) and `quiz_block(items)`. `write()` escapes closing tags inside scripts and warns about duplicates. |
| `register.py` | Swaps a `plan("Title", …)` line in `book-2.js` for a full lesson entry. |
| `testlesson.sh` | Lesson test harness. It needs Chrome and node. It checks: Live Server safety; that every script parses; that each exercise's starter fails and its solution passes, in a real iframe; that every playground control can be clicked without errors; that the quiz renders; and that there are no console errors. An optional third argument takes a screenshot of that height. |
| `builds/weekN-lK.py` | The scripts that generated each Week 3–9 lesson. Use them as templates. Re-running one regenerates its page exactly. |

The usual loop for one lesson, run from the repo root:

```bash
python3 tools/book2/builds/week5-l1.py   # write the page
python3 tools/book2/register.py "$PWD" "Sizing" '{ slug: "core-sizing", title: "Sizing", from: "sizing", desc: "…", props: ["…","…","…","…"], mdn: [CSS + "Sizing"] }'
tools/book2/testlesson.sh "$PWD" core-sizing.html
node scripts/check.mjs 2>&1 | tail -1      # expect: 9 error(s)
git add core-sizing.html book-2.js
```

Workflow per week:
1. Ask a web-fetch agent for the MDN pages' h2/h3 outlines. The URLs are in the `plan()` lines.
2. Read the matching Field Guide pages.
3. Write one builder per lesson.
4. Register it, test it, fix it.
5. Screenshot the new playgrounds to check them visually.

## Status

| Week | Title | Lessons (slug) | Status |
|---|---|---|---|
| 1 | How the web works + HTML basics | core-how-the-web-works, core-basic-html-syntax, core-webpage-metadata, core-headings-paragraphs, core-emphasis-advanced-text, core-lists, core-creating-links, core-publishing, core-debugging-html | ✅ written |
| 2 | HTML content | core-structuring-documents, core-images, core-image-formats, core-table-basics, core-table-accessibility, core-forms, core-video-audio, core-svg-embeds | ✅ written (review removed) |
| 3 | How CSS works | core-what-is-css, core-selectors, core-cascade, core-debugging-css, core-box-model, core-display-flow, core-values-units, core-text-styling, core-web-fonts | ✅ written |
| 4 | Visual styling & states | core-pseudo-classes, core-pseudo-elements, core-custom-properties, core-backgrounds-borders, core-shadows-effects, core-transforms, core-transitions, core-styling-lists-tables-forms | ✅ written |
| 5 | Layout | core-sizing, core-overflow, core-flexbox, core-grid, core-flex-or-grid, core-positioning, core-floats | ✅ written |
| 6 | Responsive + quality | core-media-queries, core-mobile-first, core-fluid-sizing, core-responsive-images, core-accessibility, core-organizing-css | ✅ written |
| 7 | JS fundamentals I | core-what-is-javascript, core-troubleshooting-js, core-variables, core-numbers-strings, core-arrays, core-conditionals | ✅ written |
| 8 | JS fundamentals II + the DOM | core-loops, core-functions, core-objects-json, core-dom-scripting | ✅ written |
| 9 | Interactive pages | core-events, core-creating-elements, core-fetching-data | ✅ written |

Each lesson's MDN sources are in its `mdn:` list in `book-2.js`. To add a lesson later, add a `plan()` line and use the usual loop.

JS exercises (`{ js, solution: "…", expose: [names], checks: [{ test: ({ logs, fns, error, code }) => … }] }`) are graded with `Runner.exec()` from `js/runner.js`, and `testlesson.sh` tests them too (it loads `runner.js` into the checker and awaits async checks). The Fetching Data checks make real requests for files in `data/`.

## Completion tracking (participation grading)

The instructor wants a plain **percentage of completion** per lesson, from what students read and do. They handle
points and late work themselves. Built 2026-11-16:

- **No Mark complete button in Book 2** (`autoComplete: true` in `book-2.js`). The footer shows a meter ("7 of 12 done
  (58%)"). An item is a section seen (and, for Play / Try it / Practice / Check yourself, used), a quiz finished at any
  score, or an exercise passed. At 100% the lesson completes itself (`lessonTally()` and `paintProgress()` in
  `js/chrome.js`), and the sidebar ticks it. The Field Guide keeps its button.
- **Dashboard** (`instructor.html`) opens on Book 2. `?book=1` shows the Field Guide, and a `?lesson=` link picks a
  book by its slug. It counts items from `search-index-2.js`, which `check.mjs --write` builds and the publish workflow
  rebuilds. Week cells are the share of *all items* that week, so lessons with more items weigh more. The CSV has one
  row per student per lesson, with `week` and `percent` columns.
- **Every hands-on section must be usable**, or 100% is out of reach. A Play section that's only for looking is
  labelled **Look** instead, and is read-timed. A demo used by clicking things that aren't form controls (links,
  table cells) puts `data-use` on its container. An audit on 2026-11-16 found 11 such sections. They were fixed, and all
  60 lessons were checked: each one's meter total matches the index, and a fully done lesson completes itself.
- **Backend:** still not connected. Step-by-step checklist and setup log: `BACKEND-SETUP.md`. `book.js` and `book-2.js` must both get the same Supabase `url`/`anonKey`
  (steps in `supabase/README.md`). The dashboard signs in through `book.js`.
- **Sign-in uses passwords, and you enroll students** (changed 2026-11-19 from magic links, which you found tedious).
  `tools/enroll.mjs` (needs the secret key in your shell) creates accounts from a CSV with a temporary password and the
  recitation you assign; `--reset <email>` re-issues one. Self sign-up is off in Supabase. First sign-in forces a new
  password (`profiles.must_change_password`, cleared by a trigger on `auth.users` when the password changes, migration
  0004), then first and last name, unless the enrollment CSV gave it (`first_name`/`last_name` columns on the roster, copied to the profile, migration 0005; added 2026-11-20). Students can't change their recitation. Any email address can have an account (0006 dropped the @colorado.edu trigger; `emailDomain` removed from both manifests, 2026-11-21). "Forgot your password?" needs SMTP.
- Gotcha: `Progress.setComplete()` logs an event before it saves, and logging repaints. `paintProgress` has a
  `completing` guard against the resulting infinite loop.

## Exercises & Quizzes (scored weekly sets), built 2026-11-23

Separate from the practice inside lessons. The instructor chose: one set per week, **scored** (not just completion),
all open at once.

- **`practice.js`** is a third manifest (`window.BOOK`, `scored: true`, `home: "practice.html"`, one "lesson" per week,
  slugs `practice-week-N`, `covers` = the Book 2 lessons it draws on). Its `backend` must equal book.js's (check.mjs enforces).
- **Each set: 4 exercises × 5 points + a 10-question quiz × 1 point = 30 points.** Scoring lives in `Progress.score()`
  (js/progress.js), used by the page footer, `practice.html` and the dashboard alike.
  - Exercises: no Show solution on scored pages; partial credit = best Check's passed/total (`exercises[id].best`, new).
    Hints stay. `js/exercise.js` now awaits async checks (Week 9's fetch exercise makes real requests to `data/`).
  - Quiz: `makeQuiz(el, items, { once: true })`: pick, change, Submit (press twice), then locked, no Retry. Counts the
    first finished attempt (`quizzes[id].first`, new; merge keeps the earliest). Unsubmitted picks: `book:quizdraft:*`.
  - The footer shows "X of 30 points · N of 5 parts tried"; the set auto-completes once every part is tried.
    Signed-out students see a "Sign in" nudge.
- **Solutions are never in the published page.** Pages are generated: `python3 tools/practice/build.py [weeks]` from
  `tools/practice/sets/week-N.js` (the page script); solutions in `week-N.solutions.js`. The publish workflow now
  excludes `tools/`. check.mjs errors if a practice page contains `solution:`.
- **Test:** `tools/practice/test.sh [weeks]` builds a temporary copy with solutions merged and runs testlesson.sh.
  As of 2026-11-23 all 36 exercises: starter scores 0 on every check, solution passes all.
- **Dashboard:** `instructor.html?book=3` shows points per week (cells "22.5 / 30"), per-exercise points and the
  quiz's first attempt per student; CSV gained `points`/`max_points`. It reads `search-index-practice.js`
  (built by `check.mjs --write`; index entries now carry `questions`).
- Not yet done: an end-to-end click-through in a real browser (quiz submit → footer score → dashboard with real
  accounts). The automated harness covers exercises and quiz rendering only.

## Open offers / loose ends

- `CURRICULUM.md`: its "Book 2" paragraph still says Book 2 is "early" and built on the Field Guide. It needs updating.
- Landing page: there's no button for Book 2 yet. It's reached from `book-2.html` directly.
- Field Guide pages `document-structure.html`, `head-metadata.html` and `js-create-elements.html` may still have the Live Server `</body>`-in-a-string problem that was fixed in Book 2.
- Book 2's search is off (`search: false`), because `search-index.js` only covers the Field Guide.
- About 73 Field Guide pages have **unstaged** edits from when the Field Guide moved to `book.html`: their "← Field Guide" and "← Contents" links were changed from `index.html` to `book.html`. They're needed, so stage them with the rest when you commit.
- `glossary-terms.js` gained five JS terms in Week 8–9 (Anonymous function, Constructor, Event listener, Node, Object literal). `check.mjs` now warns that `search-index.js` is stale; GitHub rebuilds it on publish, or run `node scripts/check.mjs --write`.
- `data/` (trails.json and three notes/*.txt) is new, for the Fetching Data lesson's real requests.
- Nothing is committed yet. Book 2's files are staged. Your own untracked files (`CURRICULUM.md`, `ica12/13.*`, `week11.html`) were left alone.
