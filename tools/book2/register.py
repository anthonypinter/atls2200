#!/usr/bin/env python3
"""Replace a plan("Title", ...) line in book-2.js with a written lesson entry.
Usage: register.py <repo> "<plan title>" '<lesson JS object literal, one line>'"""
import sys, re
repo, title, entry = sys.argv[1], sys.argv[2], sys.argv[3]
p = f"{repo}/book-2.js"
s = open(p).read()
pat = re.compile(r'^(\s*)plan\(' + re.escape(json_title := '"' + title + '"') + r'[^\n]*\),\n', re.M)
m = pat.search(s)
if not m:
    sys.exit(f"plan line for {title!r} not found")
s = s[:m.start()] + m.group(1) + entry.strip().rstrip(",") + ",\n" + s[m.end():]
open(p, "w").write(s)
print("registered", title)
