// Draggable test charge: force arrows from each fixed charge and their vector sum.
// Runs with `d3` and the container element `el` in scope (see explorable() in the setup cell).
const W = 900, H = 285, s = 40; // viewBox size; px per Å
const lB = 7.1; // Bjerrum length of water at 298 K, Å
const fscale = 400, fmax = 110; // px per kT/Å; arrow length cap so close approach stays on screen
const fixed = [{z: +1, x: -4, y: 0}, {z: -1, x: 4, y: 0}];
const test = {z: +1, x: -1.5, y: 2.5};
const X = (x) => W / 2 + s * x;
const Y = (y) => H * 0.72 - s * y;
const color = (z) => (z > 0 ? "#1f77b4" : "#ff7f0e");
const sign = (z) => (z > 0 ? "+" : "−");

const svg = d3.create("svg").attr("viewBox", [0, 0, W, H])
  .style("width", "100%").style("user-select", "none").style("font-family", "sans-serif");
const defs = svg.append("defs");
for (const [id, c] of [["grey", "#888"], ["red", "#d62728"]])
  defs.append("marker").attr("id", `arr-${id}`).attr("viewBox", "0 0 10 10")
    .attr("refX", 8).attr("refY", 5).attr("markerWidth", 4).attr("markerHeight", 4)
    .attr("orient", "auto").append("path").attr("d", "M0,0L10,5L0,10z").attr("fill", c);

const charge = (g, z) => {
  g.append("circle").attr("r", 18).attr("fill", color(z));
  g.append("text").attr("text-anchor", "middle").attr("dy", "0.35em")
    .attr("fill", "white").attr("font-size", 24).text(sign(z));
};
for (const q of fixed) charge(svg.append("g").attr("transform", `translate(${X(q.x)},${Y(q.y)})`), q.z);

const arrow = (stroke, width, marker) => svg.append("line").attr("stroke", stroke)
  .attr("stroke-width", width).attr("marker-end", `url(#arr-${marker})`);
const parts = fixed.map(() => arrow("#888", 3, "grey"));
const labels = fixed.map((q) => svg.append("text").attr("fill", "#666").attr("font-size", 16).text(`from ${sign(q.z)}`));
const total = arrow("#d62728", 5, "red");
const totalLabel = svg.append("text").attr("fill", "#d62728").attr("font-size", 16).text("total");
const readout = svg.append("text").attr("x", 10).attr("y", H - 10).attr("font-size", 18).attr("fill", "#333");
svg.append("text").attr("x", W - 10).attr("y", H - 10).attr("text-anchor", "end")
  .attr("font-size", 15).attr("fill", "#888").text("drag the test charge · click it to flip its sign");

const tg = svg.append("g").style("cursor", "grab");
const tc = tg.append("circle").attr("r", 18).attr("stroke", "#333").attr("stroke-width", 2);
const tt = tg.append("text").attr("text-anchor", "middle").attr("dy", "0.35em").attr("fill", "white").attr("font-size", 24);

// Arrow from the test charge along f, length capped; returns the tip.
const place = (line, f) => {
  const n = Math.hypot(f[0], f[1]);
  const len = Math.min(fscale * n, fmax);
  const tip = [X(test.x) + (len * f[0]) / n, Y(test.y) - (len * f[1]) / n];
  line.attr("x1", X(test.x)).attr("y1", Y(test.y)).attr("x2", tip[0]).attr("y2", tip[1]);
  return tip;
};

function update() {
  let sum = [0, 0];
  fixed.forEach((q, i) => {
    const dx = test.x - q.x, dy = test.y - q.y, r = Math.hypot(dx, dy);
    const f = [(lB * test.z * q.z * dx) / r ** 3, (lB * test.z * q.z * dy) / r ** 3]; // kT/Å
    sum = [sum[0] + f[0], sum[1] + f[1]];
    const tip = place(parts[i], f);
    labels[i].attr("x", tip[0] + 6).attr("y", tip[1] + 5);
  });
  const tip = place(total, sum);
  totalLabel.attr("x", tip[0] + 6).attr("y", tip[1] + 5);
  tg.attr("transform", `translate(${X(test.x)},${Y(test.y)})`);
  tc.attr("fill", color(test.z));
  tt.text(sign(test.z));
  readout.text(`|f| = ${Math.hypot(...sum).toFixed(2)} kT/Å  (water, Bjerrum length ${lB} Å)`);
}

tg.call(d3.drag().clickDistance(4).on("drag", (ev) => {
  let x = (ev.x - W / 2) / s, y = (H * 0.72 - ev.y) / s;
  for (const q of fixed) { // keep the test charge from sitting on a fixed one
    const dx = x - q.x, dy = y - q.y, r = Math.hypot(dx, dy);
    if (r < 1) { x = q.x + dx / r; y = q.y + dy / r; }
  }
  test.x = Math.max(-10, Math.min(10, x));
  test.y = Math.max(-1.6, Math.min(4.6, y));
  update();
}));
tg.on("click", () => { test.z = -test.z; update(); });

update();
el.append(svg.node());
