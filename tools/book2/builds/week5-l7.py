import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("floats")
pg1 = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="fl">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>The collapsing parent')
pg2 = src.between('  <section class="playground">\n    <div class="panel controls">\n      <label class="check"><input type="checkbox" id="fix">', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Floats", src.css(), """
  .vf-art { background: #fff; color: #1d2133; border: 1px solid var(--line); border-radius: var(--radius); padding: 14px; font: 0.95rem/1.6 Georgia, serif; display: flow-root; }
  .vf-box { float: left; width: 120px; height: 110px; border-radius: 8px; background: var(--item-1); color: #fff; display: grid; place-items: center; font: 700 0.8rem var(--font-code); outline: 2px dashed transparent; }
  .vf-art p { margin: 0 0 10px; }
  .vf-art.show p { background: color-mix(in srgb, var(--item-4) 25%, transparent); outline: 2px dashed var(--item-4); }
  .vf-art.show .vf-box { outline-color: var(--item-1); outline-offset: 0; }
""")
b = top("Floats", "A floated element moves to the left or right, and the text flows around it, like a photo in a magazine. That's still the job floats do best. Before Flexbox and Grid existed they were also used for whole-page layouts, so you'll see them in older code.", [
  "Wrap text around an image with <code>float</code> and a margin.",
  "Explain why margin on the text doesn't move it away from a float.",
  "Start an element below floats with <code>clear</code>.",
  "Fix a parent that doesn't contain its floats with <code>display: flow-root</code>.",
])
b += prose("""
    <div class="callout note"><p class="callout-title">Optional lesson</p><p>You won't need floats for new layouts: <a href="core-flexbox.html">Flexbox</a> and <a href="core-grid.html">Grid</a> do that job better. This lesson is here so you can wrap text around images, and so you can read older CSS.</p></div>""")
b += ST("Read", "The background of floats") + prose("""
    <p>The <span class="term">float</span> property was added to CSS for one job: letting an image sit to one side of a column of text, with the text wrapping around it, the way magazines and newspapers have always done it. It's also used for <em>drop caps</em>, a large first letter that the paragraph wraps around.</p>
    <p>Before Flexbox and Grid, floats were the only way to put boxes side by side, so developers built entire multi-column page layouts out of them, along with workarounds like the "clearfix" hack. That's a legacy technique now, but there's a lot of it in older code and tutorials.</p>""")
b += ST("Read", "A float example") + prose("""
    <h3>Floating the box</h3>
    <p><code>float: left</code> takes the element out of the normal flow and moves it to the left edge of its container. The content that follows wraps around its right side. <code>float: right</code> does the mirror image.</p>
    <pre class="snippet" data-lang="css">.box {
  float: left;
  width: 150px;
  margin-right: 15px;   /* space between the box and the text */
}</pre>
    <p>Give a floated element a width, or it shrinks to fit its content. And put a margin on the side facing the text, so the words don't press right against it.</p>""")
b += ST("Play", "Wrap text around an image", "Float the photo, change its margin, and round it off with shape-outside.") + pg1
b += prose("""
    <h3>Visualizing the float</h3>
    <p>Here's something surprising. The paragraphs beside a float aren't actually narrower: their boxes still run the full width, right <em>behind</em> the float. Only the lines of text inside them are shortened to make room.</p>
    <p>That's why a margin on the float pushes the text away, but a margin on the paragraph doesn't seem to do anything: the paragraph's left edge is already behind the float, so a small <code>margin-left</code> just moves its hidden edge further behind it.</p>""")
b += ST("Play", "Where the paragraph really is", "Outline the paragraphs, then compare a margin on the float with a margin on the text.") + """  <section class="playground">
    <div class="panel controls">
      <label class="toggle"><input type="checkbox" id="vf-show" checked> outline the paragraphs and the float</label>
      <div class="control"><label for="vf-fm">float's margin-right</label><input id="vf-fm" type="range" min="0" max="40" step="5" value="0"><span class="readout" id="vf-fm-out"></span></div>
      <div class="control"><label for="vf-pm">paragraph's margin-left</label><input id="vf-pm" type="range" min="0" max="200" step="10" value="0"><span class="readout" id="vf-pm-out"></span></div>
      <p class="hint" id="vf-out" aria-live="polite"></p>
    </div>
    <div class="vf-art show" id="vf-art">
      <div class="vf-box" id="vf-box">float: left</div>
      <p id="vf-p">The Mesa Trail runs along the foot of the Flatirons for almost seven miles, linking a dozen side trails. You can walk any part of it as an out-and-back, or make a loop with one of the canyons.</p>
      <p>In spring the meadows near NCAR are full of wildflowers.</p>
    </div>
  </section>

"""
b += ST("Read", "Clearing floats") + prose("""
    <p>Everything after a float wraps around it, until you tell an element not to. The <span class="term">clear</span> property moves an element down until it's below the floats:</p>
    <ul>
      <li><code>clear: left</code> clears floats on the left.</li>
      <li><code>clear: right</code> clears floats on the right.</li>
      <li><code>clear: both</code> clears any floats.</li>
    </ul>
    <p>Use it on whatever should start fresh, like the next section's heading. You tried <code>clear: both</code> in the first playground: turn it on there again and watch "Getting there" drop below the photo.</p>""")
b += ST("Read", "Clearing boxes wrapped around a float") + prose("""
    <h3>The problem</h3>
    <p>A floated element doesn't count toward its parent's height. If a box contains a float that's taller than the rest of its content, the box ends before the float does: its background and border stop short, the float hangs out of the bottom, and the next element tries to wrap around it.</p>
    <h3>display: flow-root</h3>
    <p>The modern fix is one line on the parent:</p>
    <pre class="snippet" data-lang="css">.wrapper {
  display: flow-root;
}</pre>
    <p><code>flow-root</code> makes the box a new <em>block formatting context</em>: a self-contained area whose floats stay inside it. Older code used the "clearfix" hack (an <code>::after</code> pseudo-element with <code>clear: both</code>) to do the same thing.</p>""")
b += ST("Play", "The collapsing parent", "This parent only contains a float, so it shrinks to almost nothing and the next element slides up underneath.") + pg2
b += ST("Practice", "Wrap text around a photo", "Float the photo, start the next section below it, and fix a box that collapsed.") + '  <div id="ex-float"></div>\n\n'
b += notes([
  "Floats are for wrapping text around images. For layout, use Flexbox or Grid.",
  "A floated element needs a <code>width</code>, and a margin on the side facing the text.",
  "Text beside a float is shortened, but its box runs behind the float, so margin on the text doesn't push it away.",
  "<code>clear: left</code>, <code>right</code> or <code>both</code> makes an element start below the floats.",
  "<code>display: flow-root</code> on the parent makes it contain its floats.",
], [
  "Building columns with floats, then fighting collapsed parents and uneven heights.",
  "Trying to space text from a float with a margin on the paragraph instead of the float.",
  "Forgetting that floats don't work on flex or grid items. The float is ignored.",
  "On phones, a floated image squeezes the text into a narrow strip. Remove the float on small screens.",
])
first = src.first_script()
js = r'''
  // --- Visualizing the float ---
  function vfUpdate() {
    const fm = +$("vf-fm").value, pm = +$("vf-pm").value;
    $("vf-art").classList.toggle("show", $("vf-show").checked);
    $("vf-box").style.marginRight = fm + "px"; $("vf-p").style.marginLeft = pm + "px";
    $("vf-fm-out").textContent = fm + "px"; $("vf-pm-out").textContent = pm + "px";
    let msg;
    if (pm > 0 && pm <= 120 + fm) msg = `margin-left: ${pm}px moves the paragraph's box, but its edge is still hidden behind the ${120 + fm}px-wide float (with its margin), so the text doesn't move.`;
    else if (pm > 120 + fm) msg = `Only once the paragraph's margin is wider than the float does the text start to move. That's not a useful way to space text.`;
    else if (fm > 0) msg = `margin-right: ${fm}px on the float pushes the text away. This is the way to add space.`;
    else msg = "The outlined paragraph runs the full width, right behind the float. Only its lines of text are shortened.";
    $("vf-out").textContent = msg;
  }
  ["vf-show", "vf-fm", "vf-pm"].forEach((id) => $(id).addEventListener("input", vfUpdate));
  vfUpdate();
'''
ex_f = src.block('  makeExercise(document.getElementById("ex-float"), {')
quiz = src.block('  makeQuiz(document.getElementById("quiz"), [')
quiz = quiz.replace("  ]);\n", '''    { id: "q5", q: "Text is pressed right against a floated photo. Where should the margin go?", opts: ["On the photo, on the side facing the text", "margin-left on the paragraph", "padding on the parent"], a: 0, why: "The paragraph's box runs behind the float, so its margin doesn't push the text away." },
    { id: "q6", q: "An element has clear: left. There's a float on the right above it. What happens?", opts: ["It moves below the right float", "It still wraps beside the right float", "The float disappears"], a: 1, why: "clear: left only clears left floats. Use clear: both for any float." },
  ]);
''')
write("core-floats.html", h, b, "\n<script>" + first + js + "</script>\n<script>\n" + quiz + "\n" + ex_f + "</script>\n")
