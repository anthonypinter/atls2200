#!/usr/bin/env python3
"""Builds the scored weekly pages (practice-week-N.html) from tools/practice/sets/week-N.js.

Usage, from the repo root:
    python3 tools/practice/build.py          # every week that has a set file
    python3 tools/practice/build.py 3 4      # just weeks 3 and 4

A set file is the page's script: makeExercise(document.getElementById("ex-…"), { title: "…", … }) calls in order,
then makeQuiz(document.getElementById("quiz"), [ … ], { once: true }). Each exercise gets its own Practice section,
titled from its title; the page heading, lede and "covers" links come from practice.js and book-2.js.
Each set has a week-N.solutions.js beside it: { "ex-id": solution, … } (an { html, css } object or a JS string).
It's never put in the published page; --test also writes _test-practice-week-N.html with the solutions merged in,
which tools/practice/test.sh runs through tools/book2/testlesson.sh and then deletes.
Closing </body>, </head>, </html> and </script> inside the script are escaped (Live Server injects at the first
literal </body>, see BOOK2-LOG.md). Test a page with tools/book2/testlesson.sh, like a Book 2 lesson.
"""
import json, re, subprocess, sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETS = ROOT / "tools" / "practice" / "sets"

def manifest(path):
    js = f"const window={{}};{(ROOT / path).read_text()};console.log(JSON.stringify(window.BOOK))"
    return json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)

def escape_closers(js):
    return re.sub(r"</(body|head|html|script)>", r"<\\/\1>", js)

def build(week, practice, lessons):
    part = practice["parts"][week - 1]
    s = part["lessons"][0]
    src = (SETS / f"week-{week}.js").read_text()
    exercises = re.findall(r'makeExercise\(document\.getElementById\("([^"]+)"\), \{\s*title: "([^"]+)"', src)
    questions = len(re.findall(r'^\s*\{ id: "[^"]+", q:', src, re.M))
    assert exercises and questions, f"week {week}: no exercises or quiz questions found"
    assert "{ once: true }" in src, f"week {week}: the quiz must be makeQuiz(…, { once: true })"
    total = questions + 5 * len(exercises)
    covers = " · ".join(f'<a href="{c}.html">{escape(lessons[c])}</a>' for c in s["covers"])
    sections = "\n\n".join(
        f'''  <div class="section-title"><span class="eyebrow">Practice</span><h2>Exercise {i}: {escape(title)}</h2></div>
  <div id="{eid}"></div>''' for i, (eid, title) in enumerate(exercises, 1))
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Week {week}: {escape(s["title"])} · Exercises &amp; Quizzes</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="core.css">
<style>
  .practice-rules {{ display: grid; gap: 8px; }}
  .practice-rules ul {{ margin: 0; padding-left: 1.2em; display: grid; gap: 4px; }}
  .practice-covers {{ font-size: 0.95rem; color: var(--muted); }}
  .practice-signin {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; border-color: var(--cobalt); }}
</style>
<script src="practice.js"></script>
<script src="js/progress.js"></script>
<script src="js/chrome.js"></script>
<script src="js/quiz.js"></script>
</head>
<body>
<main class="wrap">
  <nav class="crumbs" aria-label="Site"><a class="crumb" href="practice.html">← Exercises &amp; Quizzes</a></nav>

  <header class="page-head">
    <span class="eyebrow">Week {week} · {total} points</span>
    <h1>{escape(s["title"])}</h1>
    <p class="lede">{escape(s["desc"])}</p>
    <p class="practice-covers">Covers: {covers}</p>
  </header>

  <div class="panel practice-signin" hidden><span>You're not signed in, so your score stays in this browser and your instructor won't see it.</span><button class="btn run" type="button" data-signin>Sign in</button></div>

  <div class="panel practice-rules">
    <p class="callout-title">How this is scored</p>
    <ul>
      <li><strong>Exercises: 5 points each.</strong> Press Check my work as often as you like. Your best Check counts, with partial credit for each check that passes. Hints are free. There's no Show solution here.</li>
      <li><strong>Quiz: 1 point a question.</strong> You get one attempt. Pick every answer, then press Submit. Your answers lock and you'll see the explanations.</li>
      <li>Your work saves as you go, so you can leave and come back.</li>
    </ul>
  </div>

{sections}

  <div class="section-title"><span class="eyebrow">Check yourself</span><h2>Quiz</h2><p>{questions} questions, one attempt.</p></div>
  <div class="quiz" id="quiz"></div>

  <footer class="page-foot" data-book-nav><a href="practice.html">← Exercises &amp; Quizzes</a></footer>
</main>

<script>
{escape_closers(src.rstrip())}
</script>
</body>
</html>
'''
    out = ROOT / f'{s["slug"]}.html'
    out.write_text(page)
    print(f"wrote {out.name}: {len(exercises)} exercises, {questions} questions, {total} points")
    # A test copy with the solutions merged in, for tools/book2/testlesson.sh (which checks starter vs solution).
    # Solutions live in week-N.solutions.js, never in the published page, so students can't read them in the source.
    sol = SETS / f"week-{week}.solutions.js"
    if TEST:
        assert sol.exists(), f"week {week}: no {sol.name}"
        inject = f"const SOLUTIONS = {sol.read_text().strip().rstrip(';')};\nconst _make = window.makeExercise;\nwindow.makeExercise = (el, d) => _make(el, Object.assign(d, {{ solution: SOLUTIONS[el.id] }}));"
        test = page.replace("<script>\n", "<script>\n" + escape_closers(inject) + "\n", 1)
        (ROOT / f"_test-{out.name}").write_text(test)

TEST = "--test" in sys.argv

if __name__ == "__main__":
    sys.argv = [a for a in sys.argv if a != "--test"]
    practice = manifest("practice.js")
    book2 = manifest("book-2.js")
    lessons = {l["slug"]: l["title"] for p in book2["parts"] for l in p["lessons"] if "slug" in l}
    weeks = [int(a) for a in sys.argv[1:]] or sorted(int(f.stem.split("-")[1]) for f in SETS.glob("week-*.js") if ".solutions" not in f.name)
    for w in weeks:
        build(w, practice, lessons)
