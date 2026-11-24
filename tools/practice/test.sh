#!/bin/bash
# Usage, from the repo root: tools/practice/test.sh [week …]
# Rebuilds each practice page, then runs the Book 2 lesson harness on a copy with the solutions merged in
# (starter fails, solution passes, quiz renders, no console errors), and deletes the copy.
cd "$(dirname "$0")/../.." || exit 1
weeks=("$@"); [ ${#weeks[@]} -eq 0 ] && weeks=($(ls tools/practice/sets/week-*.solutions.js | sed -E 's/.*week-([0-9]+).*/\1/' | sort -n))
python3 tools/practice/build.py --test "${weeks[@]}" || exit 1
for w in "${weeks[@]}"; do
  tools/book2/testlesson.sh "$PWD" "_test-practice-week-$w.html" 2>&1 | grep -v "Terminated"
  rm -f "_test-practice-week-$w.html"
done
