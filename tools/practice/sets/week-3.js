  makeExercise(document.getElementById("ex-selectors"), {
    title: "Pick exactly the right elements",
    task: `<p>Write one rule for each of these, without adding classes or ids to the HTML:</p>
    <ol>
      <li>Paragraphs <em>inside</em> <code>.trail-card</code> are <code>18px</code>. The paragraph outside the card stays as it is.</li>
      <li>The <code>.meta</code> line is <code>#666</code>.</li>
      <li>Links whose <code>href</code> ends in <code>.pdf</code> are bold (<code>font-weight: 700</code>). The other link isn't.</li>
      <li>The <code>h2</code> that is a <em>direct child</em> of <code>.trail-card</code> is <code>#1a5fb4</code>.</li>
    </ol>`,
    html: `<article class="trail-card">
  <h2>Mesa Trail</h2>
  <p class="meta">6.7 miles · moderate</p>
  <p>A long walk along the base of the Flatirons.</p>
  <a href="https://bouldercolorado.gov/osmp">Official page</a>
  <a href="mesa-map.pdf">Trail map (PDF)</a>
</article>

<p>This paragraph is outside the card.</p>
`,
    css: `/* Your rules here */
`,
    hints: [
      "A descendant selector is two selectors with a space: .trail-card p",
      "An attribute selector that matches the end of a value: a[href$=\".pdf\"]",
      "The child combinator is >: .trail-card > h2",
    ],
    checks: [
      { label: "Paragraphs in the card are 18px; the one outside isn't", test: ({ $$, style }) => { const ps = $$("p"); return style(ps[1], "font-size") === "18px" && style(ps[2], "font-size") === "16px"; } },
      { label: ".meta is #666", test: ({ style }) => style(".meta", "color") === "rgb(102, 102, 102)" },
      { label: "Only the PDF link is bold", test: ({ style }) => style('a[href$=".pdf"]', "font-weight") === "700" && style('a[href^="https"]', "font-weight") === "400" },
      { label: "The card's h2 is #1a5fb4", test: ({ style }) => style(".trail-card > h2", "color") === "rgb(26, 95, 180)" },
    ],
  });

  makeExercise(document.getElementById("ex-cascade"), {
    title: "Win the cascade",
    task: `<p>The note should be dark red, but it shows up gray. <code>.panel p</code> is more specific than <code>.note</code> (a class and an element beat a class alone), so its <code>color</code> wins, even though <code>.note</code> comes later.</p>
    <p>Change the <code>.note</code> rule's <strong>selector</strong> so it wins. Don't use <code>!important</code> or an id, and don't change the HTML. The other paragraph must stay gray.</p>`,
    html: `<div class="panel">
  <p>Trail report for Saturday.</p>
  <p class="note">Bring microspikes: the north side is icy.</p>
</div>
`,
    css: `.panel p {
  color: gray;
}

.note {
  color: darkred;
  font-weight: bold;
}
`,
    hints: [
      "Specificity is counted as (ids, classes, elements). .panel p is (0, 1, 1); .note is (0, 1, 0).",
      "Make the selector at least as specific, and keep it after .panel p, so source order breaks the tie.",
      ".panel .note is (0, 2, 0), which beats (0, 1, 1).",
    ],
    checks: [
      { label: "The note is dark red", test: ({ style }) => style(".note", "color") === "rgb(139, 0, 0)" },
      { label: "The other paragraph is still gray", test: ({ style }) => style(".note", "color") === "rgb(139, 0, 0)" && style(".panel p:first-child", "color") === "rgb(128, 128, 128)" },
      { label: "No !important and no id selector", test: ({ code, style }) => style(".note", "color") === "rgb(139, 0, 0)" && !/!\s*important/i.test(code.css) && !/#[a-z_-]/i.test(code.css.replace(/#[0-9a-f]{3,8}\b/gi, "")) },
    ],
  });

  makeExercise(document.getElementById("ex-box"), {
    title: "A box that adds up",
    task: `<ol>
      <li>The card should be exactly <code>300px</code> wide <em>including</em> its padding and border. Don't change the width, padding or border numbers: change how the width is measured.</li>
      <li>Center the card horizontally with <code>auto</code> margins.</li>
      <li>Put <code>24px</code> of space above it.</li>
    </ol>`,
    html: `<div class="card">
  <h2>Royal Arch</h2>
  <p>3.4 miles, steep and rocky.</p>
</div>
`,
    css: `.card {
  width: 300px;
  padding: 20px;
  border: 5px solid #2a6;
}
`,
    hints: [
      "Right now the card is 300 + 2 × 20 + 2 × 5 = 350px wide.",
      "box-sizing: border-box makes width include the padding and border.",
      "margin: 24px auto 0; sets the top, left/right and bottom margins in one line.",
    ],
    checks: [
      { label: "The card is 300px wide on screen", test: ({ $ }) => $(".card").offsetWidth === 300 },
      { label: "Using box-sizing: border-box", test: ({ style }) => style(".card", "box-sizing") === "border-box" },
      { label: "Centered with auto left and right margins", test: ({ style, code }) => /margin(-left|-right|-inline)?\s*:[^;]*\bauto\b/.test(code.css) && style(".card", "margin-left") === style(".card", "margin-right") && parseFloat(style(".card", "margin-left")) > 0 },
      { label: "24px above it", test: ({ style }) => style(".card", "margin-top") === "24px" },
    ],
  });

  makeExercise(document.getElementById("ex-type"), {
    title: "Readable type",
    task: `<ol>
      <li>Give <code>body</code> a font stack: at least one named font, then the generic family <code>sans-serif</code> at the end.</li>
      <li>Make the <code>h1</code> <code>2.5rem</code>.</li>
      <li>Give paragraphs a <em>unitless</em> line height of <code>1.5</code>.</li>
      <li>Make <code>.eyebrow</code> uppercase with CSS (don't retype it), with <code>0.1em</code> of letter spacing.</li>
    </ol>`,
    html: `<p class="eyebrow">Week 3 report</p>
<h1>Trail Notes</h1>
<p>The Mesa Trail dried out mid-week, and the wildflowers along the southern half are starting to open. Expect crowds at the Chautauqua end on Saturday morning, and bring layers: the wind picks up after noon.</p>
`,
    css: `/* Your rules here */
`,
    hints: [
      "font-family: \"Helvetica Neue\", Arial, sans-serif;",
      "rem is relative to the root font size, so 2.5rem is 40px by default.",
      "line-height: 1.5; with no unit scales with each element's own font size.",
      "text-transform: uppercase; letter-spacing: 0.1em;",
    ],
    checks: [
      { label: "body has a font stack ending in sans-serif", test: ({ style, code }) => /,\s*sans-serif\s*$/.test(style("body", "font-family")) && /body\s*\{[^}]*font(-family)?\s*:[^;}]*,/.test(code.css) },
      { label: "The h1 is 2.5rem (40px)", test: ({ style, code }) => style("h1", "font-size") === "40px" && /2\.5rem/.test(code.css) },
      { label: "Paragraphs have a unitless line-height of 1.5", test: ({ style, code }) => style("p:last-child", "line-height") === "24px" && /line-height\s*:\s*1\.5\s*[;}]/.test(code.css) },
      { label: ".eyebrow is uppercase, with 0.1em letter spacing", test: ({ style, $ }) => style(".eyebrow", "text-transform") === "uppercase" && Math.abs(parseFloat(style(".eyebrow", "letter-spacing")) - 0.1 * parseFloat(style(".eyebrow", "font-size"))) < 0.05 && $(".eyebrow").textContent === "Week 3 report" },
    ],
  });

  makeQuiz(document.getElementById("quiz"), [
    { id: "q1", q: "In h1 { color: navy; }, what is color?", opts: ["The selector", "The property", "The value", "The declaration block"], a: 1, why: "h1 is the selector, color the property and navy the value. color: navy together is a declaration." },
    { id: "q2", q: "What's the usual way to add one stylesheet to every page of a site?", opts: ["A <style> element on each page", "A style attribute on each element", "A <link rel=\"stylesheet\" href=\"…\"> in each page's head", "An @import in the HTML"], a: 2, why: "An external stylesheet, linked from each page's head, is shared and cached by the browser." },
    { id: "q3", q: "Which selector is the most specific?", opts: ["#trail", ".card .title", "article p span", "p.note"], a: 0, why: "One id (1, 0, 0) beats any number of classes and elements." },
    { id: "q4", q: "Two rules have the same specificity and set the same property. Which wins?", opts: ["The first one", "The one with more declarations", "Neither: the browser default applies", "The one that comes later"], a: 3, why: "When specificity ties, source order decides: the last rule wins." },
    { id: "q5", q: "You set color on <body>. Why do the paragraphs inside change too, while border wouldn't?", opts: ["color is inherited; border isn't", "body styles apply to every element", "Paragraphs have no color of their own", "border needs !important"], a: 0, why: "Text properties like color and font inherit; box properties like border, padding and margin don't." },
    { id: "q6", q: "In the DevTools Styles pane a declaration is crossed out. What does that mean?", opts: ["It has a typo", "Another rule overrides it", "The browser doesn't support it", "It's commented out"], a: 1, why: "Crossed out means a rule that wins the cascade sets the same property. Invalid declarations show a warning icon instead." },
    { id: "q7", q: "Which statement about inline elements, like <a> and <span>, is true?", opts: ["They always start on a new line", "width and height don't apply to them", "They fill the width of their parent", "Their vertical margins push other lines away"], a: 1, why: "Inline boxes flow inside a line of text. width and height are ignored; use inline-block or block for those." },
    { id: "q8", q: "The root font size is 16px. A <p> inside an element with font-size: 20px has font-size: 2rem. How big is it?", opts: ["40px", "32px", "20px", "36px"], a: 1, why: "rem is relative to the root (html) font size, not the parent: 2 × 16 = 32px. 2em would be 40px." },
    { id: "q9", q: "What does display: none do that visibility: hidden doesn't?", opts: ["Removes the element from the layout, so it takes no space", "Hides it from screen readers only", "Makes it transparent", "Nothing: they're the same"], a: 0, why: "display: none removes the box entirely. visibility: hidden hides it but keeps its space." },
    { id: "q10", q: "What does font-display: swap do for a web font?", opts: ["Swaps fonts between pages", "Shows text in a fallback font right away, then switches when the web font arrives", "Hides text until the web font loads", "Loads the font only on hover"], a: 1, why: "swap avoids invisible text while the font downloads. Pick a fallback that's close in size to reduce the jump." },
  ], { once: true });
