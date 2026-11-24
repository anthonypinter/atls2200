{
  "ex-loops": `function totalMiles(distances) {
  let total = 0;
  for (const d of distances) {
    total += d;
  }
  return total;
}

function evensUpTo(max) {
  const evens = [];
  for (let i = 2; i <= max; i += 2) {
    evens.push(i);
  }
  return evens;
}

function firstOver(distances, limit) {
  let found = null;
  for (const d of distances) {
    if (d > limit) {
      found = d;
      break;
    }
  }
  return found;
}
`,
  "ex-functions": `function pace(miles, minutes) {
  return Math.round((minutes / miles) * 10) / 10;
}

function greet(name = "hiker") {
  return "Hello, " + name + "!";
}

const toKm = (miles) => Math.round(miles * 1.609 * 10) / 10;
`,
  "ex-json": `const data = '{"name":"Mesa","miles":6.7,"tags":["loop","views"]}';

const trail = JSON.parse(data);
trail.visited = true;
trail.summary = function () {
  return this.name + " (" + this.miles + " mi)";
};
const saved = JSON.stringify(trail);
`,
  "ex-dom": `function markClosed(list) {
  const closed = list.querySelectorAll('[data-status="closed"]');
  for (const li of closed) {
    li.classList.add("closed");
    li.textContent += " (closed)";
  }
  return closed.length;
}
`,
}
