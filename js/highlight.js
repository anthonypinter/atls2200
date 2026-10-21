/* Colors code samples written as <pre class="snippet" data-lang="css|html|js">…</pre>, using the same classes as the
   hand-colored ones (.sel .prop .val .cmt for CSS, .tag-name .attr .str for HTML, hlJS from js/runner.js for JS).
   Write the code as plain text (escape < and & in HTML samples); js/chrome.js loads this file when a page has one. */
(function () {
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Comments, braces, selectors (text before a "{") and declarations (text up to a ";"), in that order.
  const CSS = /(\/\*[\s\S]*?\*\/)|([{}])|((?:[^{};/]|\/(?!\*))+?(?=\{))|((?:[^{};/]|\/(?!\*))+;?)/g;
  function css(src) {
    let out = "", depth = 0, m;
    while ((m = CSS.exec(src))) {
      const [t, cmt, brace, sel, decl] = m;
      const lead = t.match(/^\s*/)[0];
      if (cmt) out += `<span class="cmt">${esc(t)}</span>`;
      else if (brace) { depth += brace === "{" ? 1 : -1; out += t; }
      else if (sel) out += `${lead}<span class="sel">${esc(t.slice(lead.length))}</span>`;
      else {
        const c = decl.indexOf(":");
        if (c < 0 || depth === 0) { out += esc(decl); continue; }
        const semi = decl.endsWith(";") ? ";" : "";
        out += `${lead}<span class="prop">${esc(decl.slice(lead.length, c))}</span>:<span class="val">${esc(decl.slice(c + 1, decl.length - semi.length))}</span>${semi}`;
      }
    }
    return out;
  }

  function html(src) {
    return src.replace(/(<!--[\s\S]*?-->)|(<\/?)([a-zA-Z][\w-]*)([^>]*)(>)|([^<]+|<)/g, (t, cmt, open, name, attrs, close, text) => {
      if (cmt) return `<span class="cmt">${esc(cmt)}</span>`;
      if (text !== undefined) return esc(text);
      const a = attrs.replace(/([\w:@-]+)(=)?("[^"]*"|'[^']*')?|([^\w"':@-]+)/g, (x, n, eq, val, other) =>
        other !== undefined ? esc(other) : `<span class="attr">${esc(n)}</span>${eq || ""}${val ? `<span class="str">${esc(val)}</span>` : ""}`);
      return `${esc(open)}<span class="tag-name">${name}</span>${a}${esc(close)}`;
    });
  }

  const pres = [...document.querySelectorAll("pre[data-lang]")];
  for (const pre of pres) {
    if (pre.dataset.lang === "css") pre.innerHTML = css(pre.textContent);
    if (pre.dataset.lang === "html") pre.innerHTML = html(pre.textContent);
  }
  const js = pres.filter((p) => p.dataset.lang === "js");
  if (js.length) loadScript("js/runner.js").then(() => js.forEach((p) => { p.innerHTML = hlJS(p.textContent); }));
})();
