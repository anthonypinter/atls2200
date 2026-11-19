#!/bin/bash
# Usage: testlesson.sh <repo-dir> <lesson.html> [screenshot]
# 1. Live Server safety: exactly one </head>, </body>, </html>; no </script inside scripts.
# 2. Every inline <script> parses (node --check).
# 3. Exercises: starter fails at least one check, solution passes all (rendered in a real iframe, so style() works).
# 4. Page smoke test on a local server with a Live Server-style injection: uncaught errors, raw text after </main>,
#    quiz rendered, playground controls clicked without errors.
set -u
REPO="$1"; F="$2"; SHOT="${3:-}"
S="${TMPDIR:-/tmp}/book2-test"; mkdir -p "$S"
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cd "$REPO" || exit 1
PORT=$((8800 + RANDOM % 100))
python3 - "$F" "$S" <<'EOF'
import re, sys, subprocess, json
f, S = sys.argv[1], sys.argv[2]
s = open(f).read()
for t in ("</head>", "</body>", "</html>"):
    n = s.count(t)
    if n != 1: print(f"FAIL live-server: {t} appears {n} times")
blocks = re.findall(r'<script>([\s\S]*?)</script>', s)
for i, b in enumerate(blocks):
    p = f"{S}/_blk{i}.js"; open(p, "w").write(b)
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
    if r.returncode: print(f"FAIL syntax in script {i}:", r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "")
open(f"{S}/_ex.js", "w").write("\n".join(b for b in blocks if "makeExercise(" in b or "makeQuiz(" in b))
EOF
# Exercise checker page (served from the repo so it can be same-origin with nothing else).
cat > "_ext_$PORT.html" <<EOF
<!doctype html><html><body><pre id="out"></pre><script>
const defs=[]; let quiz=null; window.makeExercise=(el,d)=>defs.push(d); window.makeQuiz=(el,q)=>{quiz=q};
const realGet=document.getElementById.bind(document); document.getElementById=(id)=>realGet(id)||{id};
</script><script src="/js/runner.js"></script><script src="/_ex_$PORT.js"></script><script>
const render=(code)=>new Promise((res)=>{const f=document.createElement("iframe");f.style.cssText="width:900px;height:700px";
  f.srcdoc='<!doctype html><html lang="en"><head><meta charset="utf-8"><style>'+(code.css||"")+'</style></head><body>'+(code.html||"")+'</body></html>';
  f.onload=()=>res(f);document.body.append(f);});
(async()=>{const out=[];
 for(const d of defs){ if(typeof d.js==="string"){
   for(const [label,src] of [["starter",d.js],["solution",typeof d.solution==="string"?d.solution:(d.solution||{}).js]]){
    if(typeof src!=="string"){out.push("FAIL "+d.title+" | no JS solution");continue;}
    const r=window.Runner.exec(src,d.expose||[]);
    const ctx={logs:r.lines.filter(l=>l.cls==="log").map(l=>l.text),fns:r.values,error:r.error,code:{js:src}};
    const res=[];for(const c of d.checks){try{let v=c.test(ctx);if(v&&typeof v.then==="function")v=await v;res.push(!!v)}catch(e){res.push(false)}}
    const ok= label==="starter" ? res.some(x=>!x) : res.every(x=>x);
    out.push((ok?"ok  ":"FAIL ")+d.title+" | js "+label+" | "+res.map(x=>x?"P":"f").join("")+(label==="solution"&&r.error?" | error: "+r.error.message:""));}
   continue;}
  for(const [label,code] of [["starter",{html:d.html,css:d.css}],["solution",{html:d.solution.html??d.html,css:d.solution.css??d.css}]]){
   const f=await render(code),doc=f.contentDocument,w=f.contentWindow;
   const ctx={doc,\$:(s)=>doc.querySelector(s),\$\$:(s)=>[...doc.querySelectorAll(s)],style:(s,p)=>w.getComputedStyle(typeof s==="string"?doc.querySelector(s):s).getPropertyValue(p),code:{html:code.html||"",css:code.css||""}};
   const r=d.checks.map(c=>{try{return !!c.test(ctx)}catch(e){return false}});
   const ok= label==="starter" ? r.some(x=>!x) : r.every(x=>x);
   out.push((ok?"ok  ":"FAIL ")+d.title+" | "+label+" | "+r.map(x=>x?"P":"f").join(""));
   f.remove();}}
 if(quiz){const ids=quiz.map(q=>q.id);const bad=quiz.filter(q=>!q.id||!(q.a>=0&&q.a<q.opts.length));
  out.push((bad.length||new Set(ids).size!==ids.length?"FAIL ":"ok  ")+"quiz: "+quiz.length+" questions");}
 realGet("out").textContent=out.join("\\n");})();
</script></body></html>
EOF
cp "$S/_ex.js" "_ex_$PORT.js"
python3 - "$F" "$PORT" <<'EOF'
import sys
f, port = sys.argv[1], sys.argv[2]
s = open(f).read(); i = s.find("</body>")
open(f"_inj_{port}.html", "w").write(s[:i] + '<!-- Code injected by live-server --><script>console.log("live")</script>' + s[i:])
open(f"_smoke_{port}.html", "w").write('''<!doctype html><html><body><pre id="out"></pre><script>
const f=document.createElement("iframe");f.style.cssText="width:1280px;height:900px";f.src="_inj_'''+port+'''.html";
const errs=[];
f.addEventListener("load",()=>{const w=f.contentWindow,d=w.document;
 setTimeout(()=>{const out=[];
  w.addEventListener("error",(e)=>errs.push(e.message));
  // Click every playground control and type into every playground input (not exercises or quiz).
  const ctl=[...d.querySelectorAll("main button, main input, main select, main textarea")].filter(el=>!el.closest(".exercise,[id^=ex-],.quiz,.book-bar,.book-foot,footer,.notes"));
  for(const el of ctl){try{ if(el.tagName==="BUTTON"||el.type==="checkbox"||el.type==="radio") el.click(); else { el.dispatchEvent(new w.Event("input",{bubbles:true})); el.dispatchEvent(new w.Event("change",{bubbles:true})); } }catch(e){errs.push("click: "+e.message)}}
  let raw="";for(let n=d.querySelector("main").nextSibling;n;n=n.nextSibling) if(n.nodeType===3) raw+=n.textContent.trim();
  out.push("controls exercised: "+ctl.length);
  out.push((raw?"FAIL raw text after main: "+raw.slice(0,80):"ok  no raw text after main"));
  out.push((d.querySelectorAll("#quiz button").length?"ok  quiz rendered":"FAIL quiz not rendered"));
  out.push((errs.length?"FAIL errors: "+errs.join(" | "):"ok  no errors while clicking"));
  document.getElementById("out").textContent=out.join("\\n");},2500);});
document.body.append(f);
</script></body></html>''')
EOF
python3 -m http.server $PORT >/dev/null 2>&1 & SRV=$!
sleep 1
echo "== $F"
"$C" --headless=new --disable-gpu --virtual-time-budget=20000 --dump-dom "http://localhost:$PORT/_ext_$PORT.html" 2>/dev/null | sed -n '/<pre id="out">/,/<\/pre>/p' | sed 's/<[^>]*>//g' | grep .
"$C" --headless=new --disable-gpu --virtual-time-budget=10000 --dump-dom "http://localhost:$PORT/_smoke_$PORT.html" 2>/dev/null | sed -n '/<pre id="out">/,/<\/pre>/p' | sed 's/<[^>]*>//g' | grep .
# Uncaught errors during load (console goes to stderr with logging on).
"$C" --headless=new --disable-gpu --enable-logging=stderr --v=0 --virtual-time-budget=6000 --dump-dom "http://localhost:$PORT/$F" 2>"$S/_console.txt" >/dev/null
grep -i "uncaught\|SyntaxError\|TypeError\|ReferenceError" "$S/_console.txt" | grep -v "favicon" | sed 's/^/FAIL console: /' | head -5
if [ -n "$SHOT" ]; then "$C" --headless=new --disable-gpu --window-size=1280,${SHOT} --virtual-time-budget=8000 --screenshot="$S/shot.png" "http://localhost:$PORT/$F" 2>/dev/null; echo "screenshot: $S/shot.png"; fi
kill $SRV 2>/dev/null
rm -f "_ext_$PORT.html" "_ex_$PORT.js" "_inj_$PORT.html" "_smoke_$PORT.html"
