{
  "ex-toggle": `function setupToggle(button, panel) {
  panel.hidden = true;
  button.setAttribute("aria-expanded", "false");
  button.textContent = "Show details";
  button.addEventListener("click", () => {
    panel.hidden = !panel.hidden;
    button.setAttribute("aria-expanded", String(!panel.hidden));
    button.textContent = panel.hidden ? "Show details" : "Hide details";
  });
}
`,
  "ex-build": `function renderTrails(list, trails) {
  for (const trail of trails) {
    const li = document.createElement("li");
    li.textContent = trail.name + " · " + trail.miles + " mi";
    list.append(li);
  }
  return list.children.length;
}
`,
  "ex-delegate": `function setupVotes(list, output) {
  list.addEventListener("click", (e) => {
    const button = e.target.closest("button");
    if (!button) {
      return;
    }
    output.textContent = "You picked " + button.dataset.trail;
  });
}
`,
  "ex-fetch": `async function dogTrails(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      return [];
    }
    const trails = await response.json();
    return trails.filter((t) => t.dogs).map((t) => t.name);
  } catch (err) {
    return [];
  }
}
`,
}
