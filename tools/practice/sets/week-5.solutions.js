{
  "ex-flexnav": { css: `.bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: #eef4fb;
}

.logo {
  font-size: 1.4rem;
  font-weight: 700;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.bar ul {
  display: flex;
  gap: 16px;
}
` },
  "ex-gallery": { css: `.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.photo {
  aspect-ratio: 4 / 3;
  display: grid;
  place-items: center;
  background: #cfe3d4;
  border-radius: 8px;
}
` },
  "ex-areas": { css: `.page {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-areas:
    "head head"
    "side main"
    "foot foot";
  gap: 8px;
}

header { grid-area: head; }
aside { grid-area: side; }
main { grid-area: main; }
footer { grid-area: foot; }

.page > * {
  padding: 12px;
  background: #eef4fb;
  border: 1px solid #b8cde6;
}
` },
  "ex-badge": { css: `.top {
  position: sticky;
  top: 0;
  padding: 8px 16px;
  background: #1a5fb4;
  color: white;
}

.card {
  position: relative;
  max-width: 320px;
  margin: 16px;
  padding: 16px;
  border: 1px solid #ccc;
}

.badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 2px 8px;
  background: #f97316;
  color: white;
  border-radius: 999px;
}
` },
}
