// Field lines over the electric potential of two draggable point charges; click a charge to flip its sign.
// Runs with `d3` and the container element `el` in scope (see explorable() in the setup cell).
const W = 900, H = 262;
const R = 18; // drawn charge radius, px
const nLines = 16; // field lines per charge
const step = 3, maxSteps = 700;
const charges = [{z: +1, x: 320, y: 131}, {z: -1, x: 580, y: 131}];
const color = (z) => (z > 0 ? "#1f77b4" : "#ff7f0e");
const sign = (z) => (z > 0 ? "+" : "−");

function field(x, y) {
  let ex = 0, ey = 0;
  for (const q of charges) {
    const dx = x - q.x, dy = y - q.y, r3 = Math.hypot(dx, dy) ** 3;
    ex += (q.z * dx) / r3;
    ey += (q.z * dy) / r3;
  }
  return [ex, ey];
}

// Follow the field (dir = +1) or against it (dir = -1) from a seed until the line
// reaches another charge or leaves the view. Midpoint (RK2) steps of fixed length.
function trace(x, y, dir, from) {
  const pts = [[x, y]];
  for (let n = 0; n < maxSteps; n++) {
    let [ex, ey] = field(x, y);
    let e = Math.hypot(ex, ey);
    const mx = x + (dir * step * ex) / e / 2, my = y + (dir * step * ey) / e / 2;
    [ex, ey] = field(mx, my);
    e = Math.hypot(ex, ey);
    x += (dir * step * ex) / e;
    y += (dir * step * ey) / e;
    pts.push([x, y]);
    if (x < -40 || x > W + 40 || y < -40 || y > H + 40) break;
    if (charges.some((q) => q !== from && Math.hypot(x - q.x, y - q.y) < R * 0.6)) break;
  }
  return pts;
}

const root = d3.create("div").style("font-family", "sans-serif");
const svg = root.append("svg").attr("viewBox", [0, 0, W, H]).style("width", "100%").style("user-select", "none");
svg.append("defs").append("marker").attr("id", "field-arrow").attr("viewBox", "0 0 10 10")
  .attr("refX", 5).attr("refY", 5).attr("markerWidth", 7).attr("markerHeight", 7)
  .attr("orient", "auto").append("path").attr("d", "M0,1L10,5L0,9z").attr("fill", "#777");
svg.append("clipPath").attr("id", "field-clip").append("rect").attr("width", W).attr("height", H);

// Potential map: computed on a coarse grid in a canvas, shown as an image under the lines.
// Blue for positive potential, matching the colour of positive charges.
const cell = 3;
const canvas = document.createElement("canvas");
canvas.width = Math.ceil(W / cell);
canvas.height = Math.ceil(H / cell);
const ctx = canvas.getContext("2d");
const potImage = svg.append("image").attr("width", W).attr("height", H)
  .attr("preserveAspectRatio", "none").attr("opacity", 0.75);
function paintPotential() {
  const img = ctx.createImageData(canvas.width, canvas.height);
  for (let j = 0; j < canvas.height; j++)
    for (let i = 0; i < canvas.width; i++) {
      const x = (i + 0.5) * cell, y = (j + 0.5) * cell;
      let phi = 0;
      for (const q of charges) phi += q.z / Math.max(Math.hypot(x - q.x, y - q.y), R);
      const c = d3.rgb(d3.interpolateRdBu(0.5 + 0.5 * Math.tanh(40 * phi))); // tanh compresses the 1/r spike
      const o = 4 * (j * canvas.width + i);
      img.data.set([c.r, c.g, c.b, 255], o);
    }
  ctx.putImageData(img, 0, 0);
  potImage.attr("href", canvas.toDataURL());
}
const lines = svg.append("g").attr("clip-path", "url(#field-clip)");
const arrows = svg.append("g").attr("clip-path", "url(#field-clip)");
svg.append("text").attr("x", W - 10).attr("y", H - 10).attr("text-anchor", "end")
  .attr("font-size", 15).attr("fill", "#555").text("drag the charges · click one to flip its sign");
svg.append("text").attr("x", 10).attr("y", H - 10).attr("font-size", 15).attr("fill", "#555")
  .text("background: potential φ (blue > 0, white = 0, red < 0)");

// Pointer in viewBox units from the bounding box: getScreenCTM (behind d3.pointer) ignores
// reveal.js's CSS scaling in Safari, which offsets the dragged item from the cursor.
const svgPoint = (ev) => {
  const r = svg.node().getBoundingClientRect();
  const e = ev.sourceEvent.changedTouches ? ev.sourceEvent.changedTouches[0] : ev.sourceEvent;
  return [(e.clientX - r.left) * W / r.width, (e.clientY - r.top) * H / r.height];
};
const nodes = charges.map((q) => {
  const g = svg.append("g").style("cursor", "grab");
  g.append("circle").attr("r", R).attr("stroke", "#333").attr("stroke-width", 2);
  g.append("text").attr("text-anchor", "middle").attr("dy", "0.35em").attr("fill", "white").attr("font-size", 24);
  let grab = [0, 0]; // cursor offset from the centre, so the charge doesn't jump
  g.call(d3.drag().clickDistance(4).on("start", (ev) => {
    const [x, y] = svgPoint(ev);
    grab = [q.x - x, q.y - y];
  }).on("drag", (ev) => {
    const [x, y] = svgPoint(ev);
    q.x = Math.max(R, Math.min(W - R, x + grab[0]));
    q.y = Math.max(R, Math.min(H - R, y + grab[1]));
    update();
  }));
  g.on("click", () => { q.z = -q.z; update(); });
  return {q, g};
});

function update() {
  paintPotential();
  // Lines start at positive charges and run with the field; if there are none,
  // start at the negative ones and run against it, so each line is drawn once.
  const pos = charges.filter((q) => q.z > 0);
  const sources = pos.length ? pos : charges;
  const dir = pos.length ? 1 : -1;
  const paths = [];
  for (const q of sources)
    for (let i = 0; i < nLines; i++) {
      const a = (2 * Math.PI * (i + 0.5)) / nLines;
      paths.push(trace(q.x + R * 0.7 * Math.cos(a), q.y + R * 0.7 * Math.sin(a), dir, q));
    }
  lines.selectAll("path").data(paths).join("path").attr("d", d3.line())
    .attr("fill", "none").attr("stroke", "#999").attr("stroke-width", 1.5);
  // One arrowhead per line, a little way out, pointing along the field.
  const heads = paths.filter((p) => p.length > 30).map((p) => {
    const k = Math.min(25, p.length - 2);
    const [a, b] = dir > 0 ? [p[k], p[k + 1]] : [p[k + 1], p[k]];
    return [a, b];
  });
  arrows.selectAll("line").data(heads).join("line")
    .attr("x1", (d) => d[0][0]).attr("y1", (d) => d[0][1]).attr("x2", (d) => d[1][0]).attr("y2", (d) => d[1][1])
    .attr("stroke", "none").attr("marker-end", "url(#field-arrow)");
  for (const {q, g} of nodes) {
    g.attr("transform", `translate(${q.x},${q.y})`);
    g.select("circle").attr("fill", color(q.z));
    g.select("text").text(sign(q.z));
  }
}

update();
el.append(root.node());
