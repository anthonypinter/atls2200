// Site checker: node scripts/check.mjs  (no dependencies; exits 1 if anything is wrong)
//               node scripts/check.mjs --write  also rebuilds search-index.js. The publish workflow does this before
//               every deploy, so running it locally is optional: it only refreshes search when testing on your machine.
// - book.js: every lesson has the required fields, a unique slug, a matching .html file and a known diagram key
// - every .html page is in book.js (except index and glossary)
// - every page has a doctype, lang, charset, viewport and title, and loads the shared scripts in order
// - every quiz question (a line starting "{ q:" or "{ id:") has a stable id, and ids are unique within the page
// - every local href/src points at a file that exists; links to #ids on other pages are checked when the id is static
// - glossary-terms.js: unique terms, known categories, lesson links that exist
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
  }
});

const pages = readdirSync(root).filter((f) => f.endsWith(".html")).sort();
const ids = new Map(pages.map((f) => [f, new Set([...read(f).matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]))]));

for (const f of pages) {
  const html = read(f);
  const slug = f.replace(/\.html$/, "");
  if (!["index", "glossary"].includes(slug) && !slugs.has(slug)) err(f, "not listed in book.js");
  if (!/^<!doctype html>/i.test(html)) err(f, "must start with <!doctype html>");
  if (!/<html lang="[^"]+">/.test(html)) err(f, "missing <html lang>");
  if (!/<meta charset="utf-8">/i.test(html)) err(f, "missing <meta charset>");
  if (!/<meta name="viewport"/.test(html)) err(f, "missing viewport meta");
  const head = html.slice(0, html.indexOf("</head>"));
  if (!/<title>[^<]+<\/title>/.test(head)) err(f, "missing <title> in <head>");
  if (!head.includes(HEAD_SCRIPTS)) err(f, "must load these scripts at the end of <head>, in this order:\n" + HEAD_SCRIPTS);

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
console.log(`\n${pages.length} pages, ${slugs.size} lessons: ${errors.length} error(s), ${warnings.length} warning(s)`);
process.exit(errors.length ? 1 : 0);
