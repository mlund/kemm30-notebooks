// One row of NaCl through a reference ion: add neighbours pairwise and watch the row sum converge.
// Runs with `d3` and the container element `el` in scope (see explorable() in the setup cell).
const W = 900, H = 275;
const nShow = 12; // ions drawn on each side; the sum continues beyond them
const nMax = 30;
const dx = (W - 60) / (2 * nShow), r0 = 13, yChain = 62;
const cx = (k) => W / 2 + k * dx;
const color = (k) => (k % 2 === 0 ? "#1f77b4" : "#ff7f0e"); // reference is Na+, odd neighbours Cl-
const term = (k) => (k % 2 ? -1 : 1) / k; // in units of e^2/(4πε0 a)
const label = (k) => (k === 1 ? "−1" : `${k % 2 ? "−" : "+"}1/${k}`);
const partial = d3.range(1, nMax + 1).map((n) => 2 * d3.sum(d3.range(1, n + 1), term));
const limit = -2 * Math.log(2);

const root = d3.create("div").style("font-family", "sans-serif");
const controls = root.append("div").style("display", "flex").style("align-items", "center")
  .style("gap", "14px").style("font-size", "19px");
controls.append("span").text("neighbours on each side, n");
const slider = controls.append("input").attr("type", "range").attr("min", 1).attr("max", nMax)
  .attr("step", 1).attr("value", 1).style("width", "300px");
const readout = controls.append("span");

const svg = root.append("svg").attr("viewBox", [0, 0, W, H]).style("width", "100%");
svg.append("line").attr("x1", cx(-nShow) - 20).attr("x2", cx(nShow) + 20).attr("y1", yChain).attr("y2", yChain)
  .attr("stroke", "#ddd").attr("stroke-width", 6);
svg.append("text").attr("x", 8).attr("y", yChain + 5).attr("font-size", 15).attr("fill", "#999").text("…");
svg.append("text").attr("x", W - 8).attr("y", yChain + 5).attr("text-anchor", "end").attr("font-size", 15).attr("fill", "#999").text("…");

const ions = [];
for (let k = -nShow; k <= nShow; k++) {
  const g = svg.append("g").attr("transform", `translate(${cx(k)},${yChain})`);
  g.append("circle").attr("r", r0).attr("fill", color(Math.abs(k)))
    .attr("stroke", k === 0 ? "#000" : "none").attr("stroke-width", 3);
  g.append("text").attr("text-anchor", "middle").attr("dy", "0.35em").attr("fill", "white")
    .attr("font-size", 16).text(Math.abs(k) % 2 ? "−" : "+");
  const t = k === 0 ? null : g.append("text").attr("text-anchor", "middle").attr("y", -r0 - 8)
    .attr("font-size", 12).attr("fill", Math.abs(k) % 2 ? "#2ca02c" : "#d62728").text(label(Math.abs(k)));
  ions.push({k, g, t});
}
svg.append("text").attr("x", cx(0)).attr("y", yChain + r0 + 20).attr("text-anchor", "middle")
  .attr("font-size", 14).text("reference ion");

// Convergence plot below the chain.
const p = {left: 200, right: W - 200, top: 108, bottom: H - 34};
const x = d3.scaleLinear([0, nMax], [p.left, p.right]);
const y = d3.scaleLinear([-2.05, -0.95], [p.bottom, p.top]);
svg.append("g").attr("transform", `translate(0,${p.bottom})`).call(d3.axisBottom(x).ticks(6)).style("font-size", "13px");
svg.append("g").attr("transform", `translate(${p.left},0)`).call(d3.axisLeft(y).ticks(5)).style("font-size", "13px");
svg.append("text").attr("x", (p.left + p.right) / 2).attr("y", H - 4).attr("text-anchor", "middle").attr("font-size", 14).text("n");
svg.append("text").attr("transform", `translate(${p.left - 52},${(p.top + p.bottom) / 2}) rotate(-90)`)
  .attr("text-anchor", "middle").attr("font-size", 14).text("row sum / (e²/4πε₀a)");
svg.append("line").attr("x1", p.left).attr("x2", p.right).attr("y1", y(limit)).attr("y2", y(limit))
  .attr("stroke", "#666").attr("stroke-dasharray", "6 4");
svg.append("text").attr("x", p.right + 6).attr("y", y(limit)).attr("dy", "0.35em").attr("font-size", 14).attr("fill", "#555").text("−2 ln 2");
const path = svg.append("path").attr("fill", "none").attr("stroke", "#1f77b4").attr("stroke-width", 1.5);
const dots = svg.append("g");
const dot = svg.append("circle").attr("r", 6).attr("fill", "#d62728");

function update() {
  const n = +slider.property("value");
  for (const {k, g, t} of ions) {
    const on = k === 0 || Math.abs(k) <= n;
    g.attr("opacity", on ? 1 : 0.15);
    if (t) t.attr("opacity", on ? 1 : 0);
  }
  const pts = partial.slice(0, n).map((s, i) => [i + 1, s]);
  path.attr("d", d3.line((d) => x(d[0]), (d) => y(d[1]))(pts));
  dots.selectAll("circle").data(pts).join("circle").attr("r", 3).attr("fill", "#1f77b4")
    .attr("cx", (d) => x(d[0])).attr("cy", (d) => y(d[1]));
  dot.attr("cx", x(n)).attr("cy", y(partial[n - 1]));
  readout.text(`row sum = 2(−1 + 1/2 − …) = ${partial[n - 1].toFixed(3)}   (limit ${limit.toFixed(3)})`);
}

slider.on("input", update);
update();
el.append(root.node());
