import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adapt import *
src = Src("js-objects-json")
pg_tree = src.between('  <section class="playground even">\n    <div class="stage-col">\n      <span class="eyebrow">Click a key', '  <div class="section-title"><span class="eyebrow">Play</span><h2>Dot or brackets?')
pg_br = src.between('  <section class="playground">\n    <div class="panel controls">\n      <div class="control"><label for="keypick">', '  <div class="section-title"><span class="eyebrow">Play</span><h2>JSON checker')
pg_json = src.between('  <section class="playground">\n    <div class="panel controls">\n      <span class="eyebrow">Break it</span>', '  <div class="section-title"><span class="eyebrow">Try it</span>')
rn_hero = src.between('  <div class="runner"><textarea aria-label="Code editor">const text = `{', '  <div class="section-title"><span class="eyebrow">Practice</span>')
h = head("Objects and JSON", src.css())
b = top("Objects and JSON", "An array is a list in order. An object groups related values under names, like everything you know about one trail. JSON is the same idea written as text, and it's how most data travels around the web.", [
  "Create an object, and read and change its members with dot and bracket notation.",
  "Write methods, and use <code>this</code> inside them.",
  "Create many similar objects with a function or a constructor.",
  "Read JSON's rules, and convert between JSON text and objects with <code>JSON.parse()</code> and <code>JSON.stringify()</code>.",
])
b += ST("Read", "Object basics") + prose("""
    <p>An <span class="term">object</span> is a collection of related data and functionality, written as <code>key: value</code> pairs inside curly braces. Each pair is a <b>member</b>. A member whose value is data is a <span class="term">property</span>; a member whose value is a function is a <span class="term">method</span>.</p>
    <pre class="snippet" data-lang="js">const person = {
  name: ["Bob", "Smith"],
  age: 32,
  bio: function () {
    console.log(`${this.name[0]} ${this.name[1]} is ${this.age} years old.`);
  },
  introduceSelf() {
    console.log(`Hi! I'm ${this.name[0]}.`);
  },
};</pre>
    <p><code>introduceSelf() { … }</code> is a shorter way to write <code>introduceSelf: function () { … }</code>. An object written out like this, with braces, is an <span class="term">object literal</span>. Separate members with commas.</p>""")
b += ST("Read", "Dot notation") + prose("""
    <p>To read a member, write the object's name, a dot, and the member's name. Call methods with parentheses:</p>
    <pre class="snippet" data-lang="js">person.age          // 32
person.name[0]      // "Bob"
person.bio();       // logs "Bob Smith is 32 years old."</pre>
    <h3>Objects as object properties</h3>
    <p>A value can itself be an object. Then you chain dots, one step at a time:</p>
    <pre class="snippet" data-lang="js">const person = {
  name: { first: "Bob", last: "Smith" },
};
person.name.first   // "Bob"</pre>""")
b += ST("Play", "Read the object", "Click any key to see the code that reads it.") + pg_tree
b += ST("Read", "Bracket notation") + prose("""
    <p>Square brackets with the key as a string do the same thing as a dot: <code>person["age"]</code> is <code>person.age</code>. You need brackets when the key is in a variable, because a dot always looks for a key with that exact name.</p>
    <pre class="snippet" data-lang="js">function logProperty(propertyName) {
  console.log(person[propertyName]);
}
logProperty("age");   // 32</pre>""")
b += ST("Play", "Dot or brackets?", "When the key is chosen from a dropdown, it's in a variable, so you have to use brackets.") + pg_br
b += ST("Read", "Setting object members") + prose("""
    <p>Change a member by assigning to it, with either notation. If the member doesn't exist yet, assigning creates it:</p>""")
b += runner("""const person = { name: "Bob", age: 32 };

person.age = 45;                  // change
person["eyes"] = "hazel";         // add, with brackets
person.farewell = function () {   // add a method
  console.log("Bye everybody!");
};

const myDataName = "height";
person[myDataName] = "1.75m";     // add, with a key from a variable

console.log(person);
person.farewell();""")
b += ST("Read", "What is \"this\"?") + prose("""
    <p>Inside a method, <code>this</code> means the object the method was called on. That's why <code>bio()</code> above uses <code>this.age</code> and not <code>person.age</code>: the same method will then work on any object that has it.</p>""")
b += runner("""const person1 = {
  name: "Chris",
  introduceSelf() {
    console.log(`Hi! I'm ${this.name}.`);
  },
};

const person2 = {
  name: "Deepti",
  introduceSelf() {
    console.log(`Hi! I'm ${this.name}.`);
  },
};

person1.introduceSelf();
person2.introduceSelf();""")
b += ST("Read", "Introducing constructors") + prose("""
    <p>Writing out every object by hand gets repetitive. A function can build them for you:</p>
    <pre class="snippet" data-lang="js">function createPerson(name) {
  const obj = {};
  obj.name = name;
  obj.introduceSelf = function () {
    console.log(`Hi! I'm ${this.name}.`);
  };
  return obj;
}</pre>
    <p>A <span class="term">constructor</span> is a neater version. Its name starts with a capital letter by convention, it uses <code>this</code> instead of creating and returning an object, and you call it with the <code>new</code> keyword:</p>""")
b += runner("""function Person(name) {
  this.name = name;
  this.introduceSelf = function () {
    console.log(`Hi! I'm ${this.name}.`);
  };
}

const salva = new Person("Salva");
const frankie = new Person("Frankie");

salva.introduceSelf();
frankie.introduceSelf();
console.log(frankie.name);""")
b += ST("Read", "You've been using objects all along") + prose("""
    <p>Strings, arrays, <code>Math</code>, <code>console</code>, <code>document</code>: they're all objects. <code>myString.split(",")</code> calls the <code>split()</code> method of a string object; <code>document.querySelector()</code> calls a method of the <code>document</code> object. That's what all those dots have been.</p>""")
b += ST("Read", "Working with JSON") + prose("""
    <h3>What is JSON?</h3>
    <p><span class="term">JSON</span> (JavaScript Object Notation) is a text format for structured data, based on JavaScript's object literal syntax. Servers send it, APIs return it, and config files are written in it. Because it's just text, any language can read it, but in JavaScript you first convert it into an object.</p>
    <h3>JSON structure</h3>
    <p>JSON looks like an object literal, and can contain strings, numbers, booleans, <code>null</code>, arrays and other objects:</p>
    <pre class="snippet" data-lang="json">{
  "squadName": "Super hero squad",
  "formed": 2016,
  "active": true,
  "members": [
    { "name": "Molecule Man", "age": 29, "powers": ["Radiation resistance", "Turning tiny"] }
  ]
}</pre>
    <p>Once parsed (say into <code>superHeroes</code>), you read it like any object: <code>superHeroes.members[0].powers[1]</code> is <code>"Turning tiny"</code>.</p>
    <h3>Arrays as JSON</h3>
    <p>A JSON file doesn't have to start with <code>{</code>. An array, <code>[ {…}, {…} ]</code>, is valid JSON too, and a common way to send a list of things.</p>
    <h3>Other notes</h3>
    <ul>
      <li>JSON is purely data. It can't contain functions (methods) or comments.</li>
      <li>Property names <em>and</em> strings must use double quotes. Single quotes are invalid.</li>
      <li>No trailing comma after the last item.</li>
      <li>One misplaced comma or colon breaks the whole file. A <a href="https://jsonlint.com/">validator</a> helps find it.</li>
    </ul>""")
b += ST("Play", "JSON checker", "Edit the text, or click a button to make a common mistake. The status uses the browser's own <code>JSON.parse()</code>.") + pg_json
b += ST("Read", "Converting between objects and text") + prose("""
    <p>JSON arrives as a string. Two built-in methods convert it:</p>
    <ul>
      <li><code>JSON.parse(text)</code> turns JSON text into an object you can read with dots.</li>
      <li><code>JSON.stringify(obj)</code> turns an object into JSON text, ready to save or send.</li>
    </ul>
    <p>When you load JSON from a server with <code>fetch()</code>, the response's <code>json()</code> method does the parsing for you. You'll do that in Fetching Data.</p>""")
b += ST("Try it", "parse and stringify", "This is MDN's superheroes example.") + rn_hero
b += ST("Practice", "Read and write JSON", "Turn JSON text into an object, pull values out of it, and turn it back into text.") + '  <div id="ex-objects"></div>\n\n'
b += ST("Practice", "Make trails with a constructor", "Write a constructor with a method that uses <code>this</code>.") + '  <div id="ex-ctor"></div>\n\n'
b += notes([
  "An object is a set of <code>key: value</code> members in braces. Data members are properties; function members are methods.",
  "Read with a dot (<code>hike.miles</code>) or brackets (<code>hike[\"miles\"]</code>). Use brackets when the key is in a variable.",
  "Assign to change or add a member: <code>hike.rating = 5;</code>",
  "Inside a method, <code>this</code> is the object it was called on. Constructors use <code>this</code> and are called with <code>new</code>.",
  "JSON is text. <code>JSON.parse(text)</code> makes an object; <code>JSON.stringify(obj)</code> makes text.",
], [
  "<code>hike.key</code> when <code>key</code> is a variable. It looks for a key literally named \"key\". Use <code>hike[key]</code>.",
  "Single quotes, trailing commas or comments in JSON. Any one of them makes it fail to parse.",
  "Using JSON text as if it were an object: <code>text.members</code> is <code>undefined</code> until you parse it.",
  "Forgetting <code>new</code> when calling a constructor.",
])
first, items = split_quiz(src.first_script())
ex_o = src.block('  makeExercise(document.getElementById("ex-objects"), {')
ex_c = r'''  makeExercise(document.getElementById("ex-ctor"), {
    title: "Trail constructor",
    task: `<ol>
      <li>Write a constructor <code>Trail(name, miles)</code> that sets <code>this.name</code> and <code>this.miles</code>.</li>
      <li>Give it a method <code>describe()</code> that returns <code>"Mesa is 6.7 miles"</code>, using <code>this</code>.</li>
      <li>Create <code>mesa</code> with <code>new</code>, and log <code>mesa.describe()</code>.</li>
    </ol>`,
    js: `function Trail(name, miles) {
  // set this.name and this.miles

}

// const mesa = …
`,
    solution: `function Trail(name, miles) {
  this.name = name;
  this.miles = miles;
  this.describe = function () {
    return \`\${this.name} is \${this.miles} miles\`;
  };
}

const mesa = new Trail("Mesa", 6.7);
console.log(mesa.describe());`,
    expose: ["Trail", "mesa"],
    hints: [
      "Inside the constructor: this.name = name;",
      "this.describe = function () { return … };",
      "const mesa = new Trail(\"Mesa\", 6.7);",
    ],
    checks: [
      { label: "new Trail(\"Flagstaff\", 3) has name and miles", test: ({ fns }) => { const t = new fns.Trail("Flagstaff", 3); return t.name === "Flagstaff" && t.miles === 3; } },
      { label: "describe() returns “Flagstaff is 3 miles”", test: ({ fns }) => { const t = new fns.Trail("Flagstaff", 3); return typeof t.describe === "function" && t.describe() === "Flagstaff is 3 miles"; } },
      { label: "mesa is made with new", test: ({ fns, code }) => fns.mesa instanceof fns.Trail && /new\s+Trail\s*\(/.test(code.js) },
      { label: "Logs “Mesa is 6.7 miles”", test: ({ logs }) => logs.includes("Mesa is 6.7 miles") },
    ],
  });
'''
items += '''    { id: "q90", q: "Inside a method, what does this refer to?", opts: ["The window", "The object the method was called on", "The function itself"], a: 1, why: "person1.introduceSelf() runs with this set to person1." },
    { id: "q91", q: "How do you call a constructor named Person?", opts: ["Person(\\"Sam\\")", "new Person(\\"Sam\\")", "Person.new(\\"Sam\\")"], a: 1, why: "new creates the object and sets this to it." },
'''
write("core-objects-json.html", h, b, "\n" + RUNNER + "<script>" + first + "</script>\n<script>\n" + quiz_block(items) + "\n" + ex_o + "\n" + ex_c + "</script>\n")
