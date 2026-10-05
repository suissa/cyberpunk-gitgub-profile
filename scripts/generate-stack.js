#!/usr/bin/env node
const fs = require("node:fs");

function calculateCardWidth(label, fontSize = 13, padding = 26, minWidth = 48, maxWidth = 180) {
  const monoGlyph = fontSize * 0.6;
  const measured = [...label].reduce(
    (w, ch) => w + (/[^\\x00-\\x7F]/.test(ch) ? monoGlyph * 1.1 : monoGlyph),
    0
  );
  return Math.max(minWidth, Math.min(maxWidth, Math.ceil(measured + padding)));
}

function generateCard(label, x, y) {
  const width = calculateCardWidth(label);
  return [
    `<rect x="${x.toFixed(1)}" y="${y}" width="${width.toFixed(1)}" height="30" fill="#00d9ff" fill-opacity=".06" stroke="#00d9ff" stroke-opacity=".55"/>`,
    `<path d="M${x.toFixed(1)} ${y + 8}V${y}H${(x + 8).toFixed(1)}" fill="none" stroke="#00d9ff" stroke-width="2"/>`,
    `<text x="${(x + 13).toFixed(1)}" y="${y + 20}" font-weight="700" class="cy" style="font-size:13px">${label}</text>`
  ].join("\\n");
}

function generateRow(delay, category, y, items) {
  let x = 176;
  const cards = items.map(label => {
    const result = generateCard(label, x, y);
    x += calculateCardWidth(label) + 10;
    return result;
  }).join("\\n");
  return [
    `<g class="ln" style="animation-delay:${delay}">`,
    `<text x="52" y="${y + 20}" class="dim" style="font-size:13px">${category}</text>`,
    `<text x="156" y="${y + 20}" class="cy" style="font-size:13px">›</text>`,
    cards,
    "</g>"
  ].join("\\n");
}

// The function above is deliberately called before every card is emitted,
// so long labels receive enough horizontal space instead of overflowing.
const file = "assets/stack.svg";
let svg = fs.readFileSync(file, "utf8");
const rows = [
  generateRow("0.25s", "languages", 126, ["TypeScript", "JavaScript", "Python", "Go", "Zig"]),
  generateRow("0.35s", "frameworks", 170, ["Node.js", "FastAPI", "LangGraph"]),
  generateRow("0.45s", "data", 214, ["PostgreSQL", "Redis", "MongoDB", "Cozo", "JSONB"]),
  generateRow("0.55s", "security", 258, ["Passkeys", "WebAuthn"]),
  generateRow("0.65s", "architecture", 302, ["FullAgenticStack", "AllasCode", "DDD", "Event-Driven"])
];
svg = svg.replace(/<g class="ln" style="animation-delay:(?:0\\.25s|0\\.35s|0\\.45s|0\\.55s|0\\.65s)">[\\s\\S]*?<\\/g>/g, () => rows.shift());
fs.writeFileSync(file, svg);
