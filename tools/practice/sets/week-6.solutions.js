{
  "ex-mf": { css: `.cols {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cols > section {
  flex: 1;
  padding: 16px;
  background: #eef4fb;
}

@media (min-width: 700px) {
  .cols {
    flex-direction: row;
  }
}
` },
  "ex-fluid": { css: `h1 {
  font-size: clamp(2rem, 1rem + 4vw, 3.5rem);
  line-height: 1.1;
}
` },
  "ex-rimg": { html: `<img src="images/flatirons-800.jpg"
  srcset="images/flatirons-400.jpg 400w, images/flatirons-800.jpg 800w, images/flatirons-1600.jpg 1600w"
  sizes="(min-width: 900px) 50vw, 100vw"
  alt="The Flatirons' tilted rock slabs above a green meadow"
  width="1600" height="1067" loading="lazy">
` },
  "ex-a11y": { html: `<div class="brand"><img src="images/logo.svg" width="160" height="40" alt="Boulder Trail Club"></div>

<p class="faint">Trail reports are updated every Friday.</p>

<label for="q">Search trails</label>
<input type="search" id="q">
<button type="button" class="go">Search</button>
`, css: `body {
  background: white;
}

.faint {
  color: #6b6b6b;
}

.go {
  display: inline-block;
  padding: 6px 12px;
  background: #1a5fb4;
  color: white;
  border: 0;
  font: inherit;
}
` },
}
