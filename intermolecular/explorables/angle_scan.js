// Every orientation of a dipole next to an ion is a state; the partition sum adds them up with Boltzmann weights.
// Runs with `d3` and the container element `el` in scope (see explorable() in the setup cell).
// u = -u0 cosθ, x = u0/kT; θ is the angle between μ (− to +) and the direction away from the cation, so θ = 0 is favourable.
const W = 900, H = 300;
const N = 500; // dots on the sphere of directions
const sph = {cx: 175, cy: 140, r: 112};
const P = {left: 470, right: W - 20}; // θ panels on the right
const rows = [{top: 6, h: 70}, {top: 96, h: 70}, {top: 186, h: 70}];
const blue = "#1f77b4", red = "#d62728";
const good = red, bad = blue; // favourable: the − end (red) faces the cation (blue)
const deg = Math.PI / 180;

// Evenly spread directions (Fibonacci sphere); the polar axis is +x, towards θ = 0.
const golden = Math.PI * (3 - Math.sqrt(5));
const dots = d3.range(N).map((i) => {
  const c = 1 - (2 * (i + 0.5)) / N, rho = Math.sqrt(1 - c * c), phi = i * golden;
  return {c, v: [c, rho * Math.cos(phi), rho * Math.sin(phi)]};
});

const root = d3.create("div").style("font-family", "sans-serif");
const controls = root.append("div").style("display", "flex").style("align-items", "center")
  .style("gap", "12px").style("font-size", "19px").style("margin-bottom", "2px");
controls.append("span").html("u<sub>0</sub>/k<sub>B</sub>T");
const xSlider = controls.append("input").attr("type", "range").attr("min", -1).attr("max", 1)
  .attr("step", 0.001).attr("value", Math.log10(3)).style("width", "170px");
const xOut = controls.append("span").style("min-width", "44px");
controls.append("span").text("θ");
const tSlider = controls.append("input").attr("type", "range").attr("min", 0).attr("max", 180)
  .attr("step", 0.5).attr("value", 180).style("width", "170px");
const play = controls.append("button").text("▶ scan").style("font-size", "15px").style("cursor", "pointer");
const readout = root.append("div").style("font-size", "17px").style("margin-bottom", "2px");

const svg = root.append("svg").attr("viewBox", [0, 0, W, H]).style("width", "100%").style("user-select", "none");

// Sphere: drag to turn it about its axis (φ) and tilt it.
let yaw = -0.5, pitch = 0.35;
svg.append("circle").attr("cx", sph.cx).attr("cy", sph.cy).attr("r", sph.r)
  .attr("fill", "#f6f6f6").attr("stroke", "#ccc");
const axis = svg.append("line").attr("stroke", "#999").attr("stroke-dasharray", "5 4");
const ion = svg.append("g");
ion.append("circle").attr("r", 16).attr("fill", blue);
ion.append("text").attr("text-anchor", "middle").attr("dy", "0.35em").attr("fill", "white").attr("font-size", 20).text("+");
const dotG = svg.append("g");
const ring = svg.append("path").attr("fill", "none").attr("stroke", "#222").attr("stroke-width", 2.5);
// The dipole μ, centred on the sphere and pointing at one state on the ring, so a dot reads as an orientation.
svg.append("defs").append("marker").attr("id", "scan-arrow").attr("viewBox", "0 0 10 10")
  .attr("refX", 8).attr("refY", 5).attr("markerWidth", 4).attr("markerHeight", 4)
  .attr("orient", "auto").append("path").attr("d", "M0,0L10,5L0,10z").attr("fill", "#222");
const arrowPhi = 150 * deg; // faces the viewer at the initial view
const dipoleG = svg.append("g");
const guide = dipoleG.append("line").attr("stroke", "#222").attr("stroke-width", 1.5).attr("stroke-dasharray", "3 3");
const dipole = dipoleG.append("line").attr("stroke", "#222").attr("stroke-width", 4).attr("marker-end", "url(#scan-arrow)");
const [minus, plus] = ["−", "+"].map((t) => dipoleG.append("text").attr("text-anchor", "middle").attr("dy", "0.35em")
  .attr("font-size", 22).attr("font-weight", "bold").text(t));
svg.append("rect").attr("width", 2 * sph.r + 60).attr("height", H).attr("fill", "transparent").style("cursor", "grab")
  .call(d3.drag().on("drag", (ev) => {
    yaw += ev.dx * 0.01;
    pitch = Math.max(-1.4, Math.min(1.4, pitch + ev.dy * 0.01));
    draw();
  }));
svg.append("text").attr("x", 10).attr("y", H - 8).attr("font-size", 14).attr("fill", "#777")
  .text("each dot: a direction of the dipole μ (arrowhead = + end) · drag to rotate");
const project = ([a, b, c]) => {
  const [cy, sy, cp, sp] = [Math.cos(yaw), Math.sin(yaw), Math.cos(pitch), Math.sin(pitch)];
  const x1 = a * cy - c * sy, z1 = a * sy + c * cy;
  return [sph.cx + sph.r * x1, sph.cy - sph.r * (b * cp - z1 * sp), b * sp + z1 * cp]; // [X, Y, depth]
};

// θ panels: energy, weight of each θ, running partition sum.
const xt = d3.scaleLinear([0, 180], [P.left, P.right]);
const ys = rows.map((r) => d3.scaleLinear([0, 1], [r.top + r.h, r.top]));
const labels = ["u / kT", "e^(−u/kT) · sinθ", "partition sum"];
rows.forEach((r, i) => {
  svg.append("g").attr("transform", `translate(0,${r.top + r.h})`)
    .call(d3.axisBottom(xt).tickValues([0, 45, 90, 135, 180]).tickFormat(i === 2 ? (d) => `${d}°` : ""))
    .style("font-size", "14px");
  svg.append("text").attr("x", P.left - 8).attr("y", r.top + r.h / 2).attr("text-anchor", "end")
    .attr("dy", "0.35em").attr("font-size", 15).text(labels[i]);
});
const zero = svg.append("line").attr("x1", P.left).attr("x2", P.right).attr("stroke", "#bbb");
const uPath = svg.append("path").attr("fill", "none").attr("stroke", "#333").attr("stroke-width", 3);
const states = svg.append("path").attr("fill", "none").attr("stroke", "#999").attr("stroke-dasharray", "5 4").attr("stroke-width", 2);
svg.append("text").attr("x", P.right - 4).attr("y", rows[1].top + 4).attr("text-anchor", "end").attr("font-size", 13)
  .attr("fill", "#888").text("dashed: number of states, sinθ");
svg.append("text").attr("x", P.left - 8).attr("y", rows[0].top + rows[0].h / 2 + 20).attr("text-anchor", "end")
  .attr("font-size", 13).attr("fill", "#888").text("low = aligned");
const fills = [good, bad].map((c) => svg.append("path").attr("fill", c).attr("opacity", 0.55));
const wPath = svg.append("path").attr("fill", "none").attr("stroke", "#333").attr("stroke-width", 2);
const qPaths = [good, bad].map((c) => svg.append("path").attr("fill", "none").attr("stroke", c).attr("stroke-width", 4));
const qLabel = svg.append("text").attr("font-size", 14).attr("text-anchor", "end");
const cursor = svg.append("line").attr("y1", rows[0].top).attr("y2", rows[2].top + rows[2].h).attr("stroke", "#222");

function draw() {
  const x = 10 ** +xSlider.property("value"), th = +tSlider.property("value");
  xOut.text(x.toPrecision(2));
  // Sphere: the dot size and darkness follow the Boltzmann weight relative to the best orientation.
  const pts = dots.map((d) => ({d, p: project(d.v), w: Math.exp(x * (d.c - 1))})).sort((a, b) => a.p[2] - b.p[2]);
  dotG.selectAll("circle").data(pts).join("circle")
    .attr("cx", (q) => q.p[0]).attr("cy", (q) => q.p[1]).attr("r", (q) => 1.5 + 4 * q.w)
    .attr("fill", (q) => (q.d.c > 0 ? good : bad))
    .attr("opacity", (q) => (Math.acos(q.d.c) / deg <= th ? 1 : 0.15) * (q.p[2] > 0 ? 1 : 0.5));
  const ringPts = d3.range(0, 361, 6).map((f) => project([Math.cos(th * deg),
    Math.sin(th * deg) * Math.cos(f * deg), Math.sin(th * deg) * Math.sin(f * deg)]));
  ring.attr("d", d3.line()(ringPts.map((q) => [q[0], q[1]])));
  // A fixed azimuth that turns with the sphere; picking the best-looking ring point flips between near-ties.
  const tip = project([Math.cos(th * deg), Math.sin(th * deg) * Math.cos(arrowPhi), Math.sin(th * deg) * Math.sin(arrowPhi)]);
  const dx = tip[0] - sph.cx, dy = tip[1] - sph.cy, d = Math.hypot(dx, dy) || 1;
  const k = 0.55; // half-length of the drawn dipole, as a fraction of the sphere radius
  const [hx, hy, tx, ty] = [sph.cx + k * dx, sph.cy + k * dy, sph.cx - k * dx, sph.cy - k * dy];
  dipoleG.attr("display", d < 12 ? "none" : null).attr("opacity", tip[2] < 0 ? 0.35 : 1); // faded behind the sphere
  dipole.attr("x1", tx).attr("y1", ty).attr("x2", hx).attr("y2", hy);
  guide.attr("x1", hx).attr("y1", hy).attr("x2", tip[0]).attr("y2", tip[1]);
  minus.attr("x", tx - dx / d * 14).attr("y", ty - dy / d * 14);
  plus.attr("x", hx - dy / d * 16).attr("y", hy + dx / d * 16); // beside the head, clear of the guide
  const [a0, a1] = [project([-1.25, 0, 0]), project([1.25, 0, 0])];
  axis.attr("x1", a0[0]).attr("y1", a0[1]).attr("x2", a1[0]).attr("y2", a1[1]);
  const io = project([-1.45, 0, 0]);
  ion.attr("transform", `translate(${io[0]},${io[1]})`);

  // Panels
  const ts = d3.range(0, 180.01, 1);
  const yu = ys[0].copy().domain([-x * 1.1, x * 1.1]);
  zero.attr("y1", yu(0)).attr("y2", yu(0));
  uPath.attr("d", d3.line((t) => xt(t), (t) => yu(-x * Math.cos(t * deg)))(ts));
  const wt = (t) => Math.exp(x * Math.cos(t * deg)) * Math.sin(t * deg);
  const wmax = d3.max(ts, wt), yw = ys[1].copy().domain([0, wmax * 1.05]);
  states.attr("d", d3.line((t) => xt(t), (t) => yw(wmax * 0.5 * Math.sin(t * deg)))(ts));
  wPath.attr("d", d3.line((t) => xt(t), (t) => yw(wt(t)))(ts));
  const area = d3.area((t) => xt(t), yw(0), (t) => yw(wt(t)));
  fills[0].attr("d", area(ts.filter((t) => t <= Math.min(th, 90))));
  fills[1].attr("d", th > 90 ? area(ts.filter((t) => t >= 90 && t <= th)) : null);
  // Q(θ) = ½∫₀^θ e^{x cosθ'} sinθ' dθ', relative to free rotation (Q = 1 at x = 0)
  const Q = (t) => (Math.exp(x) - Math.exp(x * Math.cos(t * deg))) / (2 * x);
  const Qtot = Q(180), yq = ys[2].copy().domain([0, Qtot * 1.05]);
  const qline = d3.line((t) => xt(t), (t) => yq(Q(t)));
  qPaths[0].attr("d", qline(ts.filter((t) => t <= Math.min(th, 90))));
  qPaths[1].attr("d", th > 90 ? qline(ts.filter((t) => t >= 90 && t <= th)) : null);
  qLabel.attr("x", P.right).attr("y", yq(Qtot) - 4).text(`total: sinh x / x = ${Qtot.toPrecision(3)}`);
  cursor.attr("x1", xt(th)).attr("x2", xt(th));

  const L = 1 / Math.tanh(x) - 1 / x, u = -x * L, w = -Math.log(Qtot);
  const share = (Qtot - Q(90)) / Qtot;
  readout.html(`repulsive half (θ > 90°): <b style="color:${bad}">${(100 * share).toPrecision(2)} %</b> of the sum`
    + ` &nbsp;·&nbsp; ⟨u⟩ = ${u.toFixed(2)}, −TS = +${(w - u).toFixed(2)}, w = ${w.toFixed(2)} k<sub>B</sub>T`);
}

let timer = null;
play.on("click", () => {
  if (timer) timer.stop();
  const t0 = performance.now();
  timer = d3.timer(() => {
    const t = Math.min(180, (performance.now() - t0) / 6000 * 180);
    tSlider.property("value", t);
    draw();
    if (t >= 180) { timer.stop(); timer = null; }
  });
});
xSlider.on("input", draw);
tSlider.on("input", () => { if (timer) { timer.stop(); timer = null; } draw(); });
draw();
el.append(root.node());
