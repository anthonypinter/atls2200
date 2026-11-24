{
  "ex-describe": `const trailName = "Mesa Trail";
const miles = 6.7;
let visits = 0;

visits++;
visits++;

console.log(\`\${trailName} is \${miles} miles. Visits: \${visits}\`);
`,
  "ex-strings": `function slugify(title) {
  return title.trim().toLowerCase().replaceAll(" ", "-");
}

function shorten(title, max) {
  if (title.length <= max) {
    return title;
  }
  return title.slice(0, max) + "…";
}
`,
  "ex-arrays": `function longOnes(distances) {
  return distances.filter((d) => d > 5);
}

function withUnits(distances) {
  return distances.map((d) => d + " mi");
}

function lastOf(list) {
  return list[list.length - 1];
}
`,
  "ex-decide": `function difficulty(gain) {
  if (gain < 500) {
    return "easy";
  } else if (gain < 1500) {
    return "moderate";
  } else {
    return "hard";
  }
}

function goHiking(weather, hasJacket) {
  switch (weather) {
    case "sunny":
      return true;
    case "rain":
      return hasJacket;
    case "storm":
      return false;
    default:
      return false;
  }
}
`,
}
