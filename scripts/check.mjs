// Site checker: node scripts/check.mjs  (no dependencies; exits 1 if anything is wrong)
//               node scripts/check.mjs --write  also rebuilds search-index.js. The publish workflow does this before
//               every deploy, so running it locally is optional: it only refreshes search when testing on your machine.
// - book.js: every lesson has the required fields, a unique slug, a matching .html file and a known diagram key,
//   and its related lessons exist
// - every .html page is in book.js (except index and glossary)
// - every page has a doctype, lang, charset, viewport and title, loads the shared scripts in order, and wraps its
//   content in one <main class="wrap">
// - every quiz question (a line starting "{ q:" or "{ id:") has a stable id, and ids are unique within the page
// - every local href/src points at a file that exists; links to #ids on other pages are checked when the id is static
// - glossary-terms.js: unique terms, known categories, lesson links that exist
// - every <span class="term"> in a lesson matches a glossary term (the same matching js/glossary.js uses)
// - lessons in the textbook format (templates/lesson.html) have objectives, a Read section and minutes in book.js;
//   the summary counts how many lessons are in that format so far
// - search-index.js is up to date with the lessons and glossary (a warning only: the live site gets a fresh one)
import { readFileSync, readdirSync, existsSync, writeFileSync } from "node:fs";
import { dirname, join, normalize, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { buildSearchIndex } from "./search-index.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const read = (f) => readFileSync(join(root, f), "utf8");
const errors = [];
const warnings = [];
const err = (file, msg) => errors.push(`${file}: ${msg}`);
const HEAD_SCRIPTS = ["book.js", "js/progress.js", "js/chrome.js", "js/quiz.js"].map((src) => `<script src="${src}"></script>`).join("\n");
// Playground markup that links to a pretend file on purpose (the [href$=".pdf"] selector demo).
const DEMO_LINKS = new Set(["selectors.html trail-map.pdf"]);

// Load the manifest the same way the browser does.
const win = {};
new Function("window", read("book.js"))(win);
const book = win.BOOK;
const index = read("index.html");
const slugs = new Set();
book.parts.forEach((part, p) => {
  if (!part.title || !Array.isArray(part.lessons) || !part.lessons.length) err("book.js", `part ${p + 1} needs a title and lessons`);
  for (const l of part.lessons || []) {
    for (const k of ["slug", "title", "desc", "mini"]) if (!l[k]) err("book.js", `${l.slug || "lesson"} is missing "${k}"`);
    if (!Array.isArray(l.props)) err("book.js", `${l.slug} needs a props array`);
    if (slugs.has(l.slug)) err("book.js", `duplicate slug "${l.slug}"`);
    slugs.add(l.slug);
    if (!existsSync(join(root, l.slug + ".html"))) err("book.js", `${l.slug}.html does not exist`);
    if (!new RegExp(`\\b${l.mini}:`).test(index)) err("book.js", `${l.slug}: no diagram "${l.mini}" in index.html minis`);
    if (l.minutes !== undefined && !(Number.isInteger(l.minutes) && l.minutes > 0)) err("book.js", `${l.slug}: minutes must be a whole number`);
  }
});
// Related lessons must exist (checked once every slug is known).
for (const l of book.parts.flatMap((p) => p.lessons)) {
  if (l.related !== undefined && !Array.isArray(l.related)) err("book.js", `${l.slug}: related must be an array of slugs`);
  for (const r of l.related || []) if (!slugs.has(r) || r === l.slug) err("book.js", `${l.slug}: related lesson "${r}" isn't another lesson in book.js`);
}

const formatted = [];
const pages = readdirSync(root).filter((f) => f.endsWith(".html")).sort();
const ids = new Map(pages.map((f) => [f, new Set([...read(f).matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]))]));

for (const f of pages) {
  const html = read(f);
  const slug = f.replace(/\.html$/, "");
  if (!["index", "glossary", "print", "instructor"].includes(slug) && !slugs.has(slug)) err(f, "not listed in book.js");
  // A lesson counts as converted once it has objectives; then it needs the rest of the format too.
  if (slugs.has(slug) && html.includes('class="objectives"')) {
    formatted.push(slug);
    if (!/<span class="eyebrow">Read<\/span>/.test(html)) err(f, "has objectives but no Read section (see templates/lesson.html)");
    if (!book.parts.some((p) => p.lessons.some((l) => l.slug === slug && l.minutes))) err(f, "has objectives but no minutes in book.js");
  }
  if (!/^<!doctype html>/i.test(html)) err(f, "must start with <!doctype html>");
  if (!/<html lang="[^"]+">/.test(html)) err(f, "missing <html lang>");
  if (!/<meta charset="utf-8">/i.test(html)) err(f, "missing <meta charset>");
  if (!/<meta name="viewport"/.test(html)) err(f, "missing viewport meta");
  const head = html.slice(0, html.indexOf("</head>"));
  if (!/<title>[^<]+<\/title>/.test(head)) err(f, "missing <title> in <head>");
  if (!head.includes(HEAD_SCRIPTS)) err(f, "must load these scripts at the end of <head>, in this order:\n" + HEAD_SCRIPTS);
  if ((html.match(/<main class="wrap">/g) || []).length !== 1) err(f, 'needs exactly one <main class="wrap"> around the page content (see templates/lesson.html)');

  const qids = [...html.matchAll(/^\s*\{ (id: "([^"]+)", )?q:/gm)];
  const missing = qids.filter((m) => !m[2]).length;
  if (missing) err(f, `${missing} quiz question(s) without an id (add id: "q5" etc., see js/quiz.js)`);
  const dupes = qids.map((m) => m[2]).filter((id, i, all) => id && all.indexOf(id) !== i);
  if (dupes.length) err(f, `duplicate quiz question id(s): ${[...new Set(dupes)].join(", ")}`);

  // Ignore code samples and scripts: their hrefs are examples, not links.
  const markup = html.replace(/<(script|style|textarea|pre|code)\b[\s\S]*?<\/\1>/gi, "").replace(/<!--[\s\S]*?-->/g, "");
  for (const [, attr, url] of markup.matchAll(/\s(href|src)="([^"]*)"/g)) {
    if (!url || /^(https?:|\/\/|mailto:|tel:|data:|javascript:)/.test(url) || DEMO_LINKS.has(`${f} ${url}`)) continue;
    const [path, hash] = url.split("#");
    if (!path) {
      if (hash && !ids.get(f).has(hash)) warnings.push(`${f}: ${attr}="${url}" — no static id="${hash}" on this page`);
      continue;
    }
    const target = normalize(join(dirname(f), path.split("?")[0]));
    if (relative(".", target).startsWith("..") || !existsSync(join(root, target))) { err(f, `${attr}="${url}" points at a missing file`); continue; }
    if (hash && ids.has(target) && !ids.get(target).has(hash)) warnings.push(`${f}: ${attr}="${url}" — no static id="${hash}" in ${target} (fine if JavaScript adds it)`);
  }
}

// Glossary
new Function("window", read("glossary-terms.js"))(win);
const terms = new Set();
for (const [term, cat, def, , page] of win.GLOSSARY) {
  const id = win.glossaryId(term);
  if (terms.has(id)) err("glossary-terms.js", `duplicate term "${term}"`);
  terms.add(id);
  if (!["html", "css", "layout", "js", "workflow"].includes(cat)) err("glossary-terms.js", `"${term}" has unknown category "${cat}"`);
  if (!def) err("glossary-terms.js", `"${term}" has no definition`);
  if (page && !slugs.has(page.replace(/\.html$/, ""))) err("glossary-terms.js", `"${term}" links to ${page}, which isn't a lesson in book.js`);
}

// Glossary terms marked in lessons. Mirrors find() in js/glossary.js: variants, then singular forms.
const norm = (s) => s.toLowerCase().replace(/\s+/g, " ").trim();
const names = new Set();
for (const [term] of win.GLOSSARY) {
  for (const n of [term, term.replace(/\s*\(.*\)\s*$/, ""), ...(term.match(/\(([^)]+)\)/)?.slice(1) || []), ...term.split(" / ")]) names.add(norm(n));
}
const known = (text) => {
  const k = norm(text);
  return names.has(k) || (/[a-z]s$/.test(k) && (names.has(k.slice(0, -1)) || (k.endsWith("es") && names.has(k.slice(0, -2)))));
};
for (const f of pages) {
  for (const [, dataTerm, inner] of read(f).matchAll(/<span class="term"(?: data-term="([^"]+)")?>([\s\S]*?)<\/span>/g)) {
    const t = dataTerm || inner.replace(/<[^>]+>/g, "");
    if (!known(t)) err(f, `<span class="term">${t}</span> isn't a glossary term: use data-term="…" with the glossary's wording, or add the term to glossary-terms.js`);
  }
}

// Search index
const searchIndex = buildSearchIndex(root, book, win.GLOSSARY, win.glossaryId);
const indexPath = join(root, "search-index.js");
if (process.argv.includes("--write")) {
  writeFileSync(indexPath, searchIndex);
  console.log("wrote search-index.js (" + Math.round(searchIndex.length / 1024) + " KB)");
} else if (!existsSync(indexPath) || readFileSync(indexPath, "utf8") !== searchIndex) {
  warnings.push("search-index.js: older than the lessons, so local search may miss recent changes. GitHub rebuilds it when publishing; run node scripts/check.mjs --write to refresh your copy");
}

for (const w of warnings) console.log("warn  " + w);
for (const e of errors) console.log("error " + e);
console.log(`\n${pages.length} pages, ${slugs.size} lessons (${formatted.length} in the textbook format): ${errors.length} error(s), ${warnings.length} warning(s)`);
process.exit(errors.length ? 1 : 0);
