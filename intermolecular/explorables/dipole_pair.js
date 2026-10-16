// Energy of two water-sized dipoles in vacuum: drag a dipole to move it, drag its blue (+) end to rotate it.
// Runs with `d3` and the container element `el` in scope (see explorable() in the setup cell).
const W = 900, H = 230;
const s = 60; // px per Å
const lB = 557; // Bjerrum length in vacuum at 300 K, Å
const mu = 1.85 / 4.803; // water, eÅ
const d = 1; // drawn ± separation, Å; charges ±mu/d give the same dipole moment
const rMin = 2; // closest approach, Å
const dipoles = [{x: 6, y: 1.9, a: 0}, {x: 9, y: 1.9, a: 0}]; // centre in Å, angle in rad (screen coords)
const presets = {
  "head-to-tail": [[6, 1.9, 0], [9, 1.9, 0]],
  "side-by-side, parallel": [[6, 1.9, -Math.PI / 2], [9, 1.9, -Math.PI / 2]],
  "side-by-side, antiparallel": [[6, 1.9, -Math.PI / 2], [9, 1.9, Math.PI / 2]],
};

const ends = (p) => { // [+ end, − end] in Å
  const ux = Math.cos(p.a) * d / 2, uy = Math.sin(p.a) * d / 2;
  return [[p.x + ux, p.y + uy], [p.x - ux, p.y - uy]];
};

function energies() {
  const [p, q] = dipoles;
  const rx = q.x - p.x, ry = q.y - p.y, r = Math.hypot(rx, ry);
  const [m1x, m1y, m2x, m2y] = [Math.cos(p.a), Math.sin(p.a), Math.cos(q.a), Math.sin(q.a)];
  const point = lB * mu * mu * (m1x * m2x + m1y * m2y
    - 3 * ((m1x * rx + m1y * ry) / r) * ((m2x * rx + m2y * ry) / r)) / r ** 3;
  let exact = 0; // four cross pairs of point charges
  const qd = mu / d;
  ends(p).forEach((a, i) => ends(q).forEach((b, j) => {
    exact += lB * (i === j ? qd * qd : -qd * qd) / Math.hypot(a[0] - b[0], a[1] - b[1]);
  }));
  return {r, point, exact};
}

const root = d3.create("div").style("font-family", "sans-serif");
const controls = root.append("div").style("display", "flex").style("align-items", "center")
  .style("gap", "10px").style("font-size", "18px").style("margin-bottom", "4px").style("flex-wrap", "wrap");
for (const [name, set] of Object.entries(presets))
  controls.append("button").text(name).style("font-size", "15px").style("cursor", "pointer").on("click", () => {
    set.forEach(([x, y, a], i) => Object.assign(dipoles[i], {x, y, a}));
    update();
  });
controls.append("button").text("double r").style("font-size", "15px").style("cursor", "pointer").on("click", () => {
  const [p, q] = dipoles;
  const x = 2 * q.x - p.x, y = 2 * q.y - p.y;
  if (x > 0.3 && x < W / s - 0.3 && y > 0.3 && y < H / s - 0.3) Object.assign(q, {x, y});
  update();
});
const readout = root.append("div").style("font-size", "20px").style("margin", "4px 0");

const svg = root.append("svg").attr("viewBox", [0, 0, W, H]).style("width", "100%").style("user-select", "none")
  .style("border", "1px solid #ddd");
// Pointer in viewBox units from the bounding box: getScreenCTM (behind d3.pointer) ignores
// reveal.js's CSS scaling in Safari, which offsets the dragged item from the cursor.
const svgPoint = (ev) => {
  const r = svg.node().getBoundingClientRect();
  const e = ev.sourceEvent.changedTouches ? ev.sourceEvent.changedTouches[0] : ev.sourceEvent;
  return [(e.clientX - r.left) * W / r.width, (e.clientY - r.top) * H / r.height];
};
const link = svg.append("line").attr("stroke", "#bbb").attr("stroke-dasharray", "4 4").attr("stroke-width", 2);
const rLabel = svg.append("text").attr("font-size", 16).attr("fill", "#777").attr("text-anchor", "middle");
svg.append("text").attr("x", W - 10).attr("y", H - 10).attr("text-anchor", "end").attr("font-size", 15)
  .attr("fill", "#555").text("drag a dipole to move it · drag its + end to rotate it");

const nodes = dipoles.map((p) => {
  const g = svg.append("g");
  const body = g.append("line").attr("stroke", "#444").attr("stroke-width", 14).attr("stroke-linecap", "round")
    .style("cursor", "grab");
  const minus = g.append("circle").attr("r", 13).attr("fill", "#ff7f0e").style("pointer-events", "none");
  const plus = g.append("circle").attr("r", 13).attr("fill", "#1f77b4").style("cursor", "crosshair");
  const labels = [g.append("text"), g.append("text")].map((t) => t.attr("text-anchor", "middle")
    .attr("dy", "0.35em").attr("fill", "white").attr("font-size", 20).style("pointer-events", "none"));
  let grab = [0, 0]; // cursor offset from the centre, so the dipole doesn't jump
  body.call(d3.drag().on("start", (ev) => {
    const [cx, cy] = svgPoint(ev);
    grab = [p.x - cx / s, p.y - cy / s];
  }).on("drag", (ev) => {
    const other = dipoles.find((o) => o !== p);
    const [cx, cy] = svgPoint(ev);
    let x = cx / s + grab[0], y = cy / s + grab[1];
    // Too close: slide along the rMin circle instead of stopping, so the drag never stalls.
    const dx = x - other.x, dy = y - other.y, r = Math.hypot(dx, dy) || 1e-6;
    if (r < rMin) { x = other.x + dx / r * rMin; y = other.y + dy / r * rMin; }
    p.x = Math.max(0.6, Math.min(W / s - 0.6, x));
    p.y = Math.max(0.6, Math.min(H / s - 0.6, y));
    update();
  }));
  plus.call(d3.drag().on("drag", (ev) => {
    const [cx, cy] = svgPoint(ev);
    p.a = Math.atan2(cy / s - p.y, cx / s - p.x);
    update();
  }));
  return {p, body, plus, minus, labels};
});

function update() {
  for (const {p, body, plus, minus, labels} of nodes) {
    const [[px, py], [mx, my]] = ends(p);
    body.attr("x1", mx * s).attr("y1", my * s).attr("x2", px * s).attr("y2", py * s);
    plus.attr("cx", px * s).attr("cy", py * s);
    minus.attr("cx", mx * s).attr("cy", my * s);
    labels[0].attr("x", px * s).attr("y", py * s).text("+");
    labels[1].attr("x", mx * s).attr("y", my * s).text("−");
  }
  const [p, q] = dipoles;
  link.attr("x1", p.x * s).attr("y1", p.y * s).attr("x2", q.x * s).attr("y2", q.y * s);
  const {r, point, exact} = energies();
  rLabel.attr("x", (p.x + q.x) / 2 * s).attr("y", (p.y + q.y) / 2 * s - 14).text(`r = ${r.toFixed(1)} Å`);
  const col = (u) => (u < 0 ? "#2a7d2a" : "#c0392b");
  readout.html(`interaction energy <b style="color:${col(point)}">u = ${point.toFixed(2)} k<sub>B</sub>T</b> (point dipoles)`
    + ` &nbsp;·&nbsp; as ± charges ${d} Å apart: ${exact.toFixed(2)} k<sub>B</sub>T`
    + ` &nbsp;<span style="color:#777">(μ = 1.85 D, vacuum, 300 K)</span>`);
}

update();
el.append(root.node());
