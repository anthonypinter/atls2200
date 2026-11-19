"""Helpers for turning a Field Guide lesson into a Book 2 lesson.
Usage in a script:  from adapt import *;  src = Src("css-basics");  ...  write("core-x.html", head, body, scripts)
"""
import re, sys
import os
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) + "/"

class Src:
    def __init__(self, slug):
        self.s = open(REPO + slug + ".html").read()
    def between(self, a, b):
        s = self.s; i = s.index(a); j = s.index(b, i); return s[i:j]
    def css(self):
        s = self.s; return s[s.index("<style>") + 7:s.index("</style>")] if "<style>" in s else ""
    def scripts(self):
        s = self.s; return s[s.index("</main>") + len("</main>\n"):]
    def first_script(self):
        sc = self.scripts(); i = sc.index("<script>") + 8; t = sc[i:sc.index("</script>", i)]
        if "const $ =" not in t: t = "\n  const $ = (id) => document.getElementById(id);" + t
        return t
    def block(self, start):
        """script text from `start` to the end of its makeExercise/makeQuiz call (balanced to '  });' or '  ]);')."""
        sc = self.scripts(); i = sc.index(start)
        ends = ["\n  });\n", "\n});\n"] if "makeExercise" in start else ["\n  ]);\n", "\n]);\n"]
        hits = [(sc.find(e, i), e) for e in ends if sc.find(e, i) >= 0]
        j, e = min(hits); return sc[i:j + len(e)]

def head(title, css_text="", extra_css=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Core Web Development</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="core.css">
<style>{css_text.rstrip()}
{extra_css.rstrip()}
</style>
<script src="book-2.js"></script>
<script src="js/progress.js"></script>
<script src="js/chrome.js"></script>
<script src="js/quiz.js"></script>
</head>
"""

def top(h1, lede, objectives):
    lis = "\n".join(f"        <li>{o}</li>" for o in objectives)
    return f"""<body>
<main class="wrap">
  <nav class="crumbs" aria-label="Site"><a class="crumb" href="book-2.html">← Contents</a><a class="crumb" href="glossary.html">Glossary</a></nav>
  <header class="page-head">
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="objectives">
      <p class="callout-title">You'll be able to</p>
      <ul>
{lis}
      </ul>
    </div>
  </header>

"""

def ST(eb, h2, p="", id=""):
    i = f' id="{id}"' if id else ""
    return f'  <div class="section-title"{i}><span class="eyebrow">{eb}</span><h2>{h2}</h2>{"<p>" + p + "</p>" if p else ""}</div>\n'

def prose(html):
    return f'  <div class="prose">\n{html.strip()}\n  </div>\n\n'

def notes(keys, mistakes):
    k = "\n".join(f"        <li>{x}</li>" for x in keys); m = "\n".join(f"        <li>{x}</li>" for x in mistakes)
    return f"""  <section class="notes">
    <div class="panel">
      <h2>Key ideas</h2>
      <ul>
{k}
      </ul>
    </div>
    <div class="panel mistake">
      <h2>Common mistakes</h2>
      <ul>
{m}
      </ul>
    </div>
  </section>

  <div class="section-title"><span class="eyebrow">Check yourself</span><h2>Quick check</h2></div>
  <div class="panel quiz" id="quiz"></div>

  <footer class="page-foot" data-book-nav><a href="book-2.html">← Contents</a></footer>
</main>
"""

def write(name, *parts):
    text = "".join(parts)
    if not text.rstrip().endswith("</html>"):
        text = text.rstrip() + "\n</body>\n</html>\n"
    # Live Server safety: escape document closing tags inside scripts, then check
    def fix(m):
        body = m.group(2)
        for t in ("</body>", "</head>", "</html>"):
            body = body.replace(t, t.replace("</", "<\/"))
        return m.group(1) + body + m.group(3)
    text = re.sub(r"(<script>)(.*?)(</script>)", fix, text, flags=re.S)
    for t in ("</body>", "</head>", "</html>"):
        n = text.count(t)
        if n != 1: print(f"WARNING {name}: {t} appears {n} times", file=sys.stderr)
    # Field Guide links that should point at Book 2 lessons
    open(REPO + name, "w").write(text)
    print("wrote", name, len(text))

def split_quiz(js):
    """Pull the quiz out of a Field Guide playground script (JS lessons put makeQuiz there).
    Returns (script_without_quiz, item_lines) where item_lines are the '    { id: ... },' lines."""
    if "  const QUIZ = [\n" in js:
        i = js.index("  const QUIZ = [\n"); j = js.index("\n  ];\n", i)
        items = js[i + len("  const QUIZ = [\n"):j + 1]
        js = js[:i] + js[j + len("\n  ];\n"):]
        js = re.sub(r'\n  makeQuiz\([^\n]*QUIZ\);', "", js)
        return js, items
    m = re.search(r'\n  makeQuiz\((\$\("quiz"\)|document\.getElementById\("quiz"\)), \[\n', js)
    if not m:
        return js, ""
    j = js.index("\n  ]);\n", m.end())
    items = js[m.end():j + 1]
    return js[:m.start()] + js[j + len("\n  ]);"):], items

def quiz_block(items):
    return '  makeQuiz(document.getElementById("quiz"), [\n' + items + '  ]);\n'

RUNNER = '<script src="js/runner.js"></script>\n'

def runner(code, label="Code editor"):
    """A runnable JS example (js/runner.js turns it into an editor with Run and a console)."""
    import html as _h
    return f'  <div class="runner"><textarea aria-label="{label}">{_h.escape(code.strip(), quote=False)}</textarea></div>\n\n'
