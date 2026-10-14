// NaCl crystal around a reference ion: grow the summation region and compare ways of adding it up.
// Runs with `d3` and the container element `el` in scope (see explorable() in the setup cell).
const W = 900, H = 330;
const Lmax = 6;
const methods = {
  sphere: "sphere",
  cube: "cube",
  neutral: "neutral cube",
};
const exact = 1.7476;

// Weight of ion (i,j,k) in the region of size L, or 0 if outside.
// Neutral cube (Evjen): ions on a face, edge or corner are shared with the next cube.
function weight(method, L, i, j, k) {
  const a = [i, j, k].map(Math.abs);
  if (method === "sphere") return Math.hypot(i, j, k) <= L ? 1 : 0;
  if (Math.max(...a) > L) return 0;
  if (method === "cube") return 1;
  return a.reduce((w, v) => w * (v === L ? 0.5 : 1), 1);
}

// Madelung sum M = -Σ' (±1)/d, reference ion positive; positive M means binding.
function madelung(method, L) {
  let M = 0;
  for (let i = -L; i <= L; i++)
    for (let j = -L; j <= L; j++)
      for (let k = -L; k <= L; k++) {
        if (!i && !j && !k) continue;
        const w = weight(method, L, i, j, k);
        if (w) M -= (w * ((i + j + k) % 2 ? -1 : 1)) / Math.hypot(i, j, k);
      }
  return M;
}
const sums = {};
for (const m in methods) sums[m] = d3.range(1, Lmax + 1).map((L) => madelung(m, L));

const lattice = [];
for (let i = -Lmax; i <= Lmax; i++)
  for (let j = -Lmax; j <= Lmax; j++)
    for (let k = -Lmax; k <= Lmax; k++) lattice.push({i, j, k, pos: (i + j + k) % 2 === 0});

const root = d3.create("div").style("font-family", "sans-serif");
const controls = root.append("div").style("display", "flex").style("align-items", "center")
  .style("gap", "12px").style("font-size", "18px").style("flex-wrap", "wrap");
controls.append("span").text("region size L");
const slider = controls.append("input").attr("type", "range").attr("min", 1).attr("max", Lmax)
  .attr("step", 1).attr("value", 1).style("width", "160px");
let method = "neutral";
const buttons = Object.entries(methods).map(([m, name]) =>
  controls.append("button").text(name).style("font-size", "15px").style("cursor", "pointer")
    .on("click", () => { method = m; update(); }).datum(m));
const rowBox = controls.append("label").style("font-size", "15px");
const showRow = rowBox.append("input").attr("type", "checkbox");
rowBox.append("span").text(" show a row");

const svg = root.append("svg").attr("viewBox", [0, 0, W, H]).style("width", "100%");

// 3D view on the left: orthographic projection, drag to rotate.
const view = {cx: 205, cy: 165, size: 150};
let yaw = 0.6, pitch = -0.45;
// Keep the rotating cube inside its panel.
svg.append("clipPath").attr("id", "crystal-clip").append("rect").attr("width", 410).attr("height", H);
const scene = svg.append("g").attr("clip-path", "url(#crystal-clip)");
svg.append("rect").attr("x", 0).attr("y", 0).attr("width", 410).attr("height", H)
  .attr("fill", "transparent").style("cursor", "grab")
  .call(d3.drag().on("drag", (ev) => {
    yaw += ev.dx * 0.01;
    pitch = Math.max(-1.5, Math.min(1.5, pitch + ev.dy * 0.01));
    draw();
  }));
svg.append("text").attr("x", 10).attr("y", H - 8).attr("font-size", 13).attr("fill", "#999").text("drag to rotate");

// Partial sums on the right: all three methods, the chosen one in bold.
const p = {left: 500, right: W - 20, top: 20, bottom: H - 50};
const x = d3.scaleLinear([1, Lmax], [p.left, p.right]);
const y = d3.scaleLinear([-5, 7], [p.bottom, p.top]);
svg.append("g").attr("transform", `translate(0,${p.bottom})`).call(d3.axisBottom(x).ticks(Lmax)).style("font-size", "13px");
svg.append("g").attr("transform", `translate(${p.left},0)`).call(d3.axisLeft(y).ticks(6)).style("font-size", "13px");
svg.append("text").attr("x", (p.left + p.right) / 2).attr("y", H - 14).attr("text-anchor", "middle").attr("font-size", 14).text("region size L");
svg.append("text").attr("transform", `translate(${p.left - 40},${(p.top + p.bottom) / 2}) rotate(-90)`)
  .attr("text-anchor", "middle").attr("font-size", 14).text("partial Madelung sum");
svg.append("line").attr("x1", p.left).attr("x2", p.right).attr("y1", y(exact)).attr("y2", y(exact))
  .attr("stroke", "#666").attr("stroke-dasharray", "6 4");
svg.append("text").attr("x", p.right).attr("y", y(exact) - 8).attr("text-anchor", "end").attr("font-size", 13).attr("fill", "#555").text("1.7476");
const curves = Object.keys(methods).map((m) => ({m, path: svg.append("path").attr("fill", "none")}));
const marker = svg.append("circle").attr("r", 6).attr("fill", "#d62728");
const readout = svg.append("text").attr("x", p.left + 10).attr("y", p.top + 14).attr("font-size", 16);

function draw() {
  const L = +slider.property("value");
  const row = showRow.property("checked");
  const [cy, sy, cp, sp] = [Math.cos(yaw), Math.sin(yaw), Math.cos(pitch), Math.sin(pitch)];
  const s = view.size / (1.8 * L); // a rotated cube spans up to √3 L
  const pts = lattice
    .filter((a) => Math.max(Math.abs(a.i), Math.abs(a.j), Math.abs(a.k)) <= L)
    .map((a) => {
      const x1 = a.i * cy - a.k * sy, z1 = a.i * sy + a.k * cy; // yaw about the vertical axis
      const y2 = a.j * cp - z1 * sp, z2 = a.j * sp + z1 * cp; // then pitch
      const w = weight(method, L, a.i, a.j, a.k);
      const ref = !a.i && !a.j && !a.k;
      const inRow = row && !a.j && !a.k;
      return {...a, X: view.cx + s * x1, Y: view.cy - s * y2, z: z2, w, ref, inRow};
    })
    .sort((a, b) => a.z - b.z);
  scene.selectAll("circle").data(pts).join("circle")
    .attr("cx", (d) => d.X).attr("cy", (d) => d.Y)
    .attr("r", (d) => (d.ref ? 0.42 : 0.36) * s * (1 + 0.03 * d.z))
    .attr("fill", (d) => (d.pos ? "#1f77b4" : "#ff7f0e"))
    .attr("fill-opacity", (d) => (d.ref || d.inRow ? 1 : row ? 0.1 : 0.15 + 0.85 * d.w))
    .attr("stroke", (d) => (d.ref ? "#000" : d.inRow ? "#333" : "none"))
    .attr("stroke-width", (d) => (d.ref ? 3 : 1.5));
}

function update() {
  const L = +slider.property("value");
  for (const b of buttons) b.style("font-weight", b.datum() === method ? "bold" : null);
  for (const {m, path} of curves)
    path.attr("d", d3.line((v, i) => x(i + 1), (v) => y(v))(sums[m]))
      .attr("stroke", m === method ? "#1f77b4" : "#bbb").attr("stroke-width", m === method ? 3 : 1.5);
  const M = sums[method][L - 1];
  marker.attr("cx", x(L)).attr("cy", y(M));
  readout.text(`${methods[method]}, L = ${L}:  M = ${M.toFixed(3)}`);
  draw();
}

slider.on("input", update);
showRow.on("change", draw);
update();
el.append(root.node());
