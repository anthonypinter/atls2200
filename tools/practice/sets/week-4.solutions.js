{
  "ex-states": { css: `nav a {
  padding: 4px 8px;
}

nav a:hover,
nav a:focus-visible {
  background: #fde68a;
}

.log li:nth-child(even) {
  background: #eef4fb;
}

.log li:first-child {
  font-weight: 700;
}
` },
  "ex-vars": { css: `:root {
  --accent: #c0392b;
}

.winter {
  --accent: #2471a3;
}

h1, h2 {
  color: var(--accent);
}

button {
  background: var(--accent);
  color: white;
  border: 0;
  padding: 8px 14px;
}
` },
  "ex-card": { css: `.card {
  max-width: 300px;
  padding: 16px;
  background: linear-gradient(135deg, #fde68a, #f97316);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgb(0 0 0 / 0.2);
}

.card::before {
  content: "★ Featured";
}
` },
  "ex-motion": { css: `.lift {
  padding: 10px 18px;
  font: inherit;
  transition: transform 0.2s ease-out;
}

.lift:hover {
  transform: translateY(-3px);
}

@media (prefers-reduced-motion: reduce) {
  .lift {
    transition: none;
  }
}
` },
}
