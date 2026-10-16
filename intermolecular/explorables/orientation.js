// A dipole tumbling in the field of an ion: Boltzmann distribution of its angle, and the averaged free energy.
// Runs with `d3` and the container element `el` in scope (see explorable() in the setup cell).
// x = u0/kT is the coupling, u = -u0 cosθ; θ = 0 is the favourable orientation.
const W = 900, H = 340;
const m = {top: 14, bottom: 52, left: 70, right: 16};
const split = 470; // left panel: p(θ); right panel: |w|/kT against x
const sinhc = (x) => Math.sinh(x) / x;
const coth = (x) => Math.cosh(x) / Math.sinh(x);

const root = d3.create("div").style("font-family", "sans-serif");
const controls = root.append("div").style("display", "flex").style("align-items", "center")
  .style("gap", "14px").style("font-size", "20px").style("margin-bottom", "4px");
controls.append("span").html("u<sub>0</sub>/k<sub>B</sub>T");
const slider = controls.append("input").attr("type", "range").attr("min", -1.3).attr("max", 1.3)
  .attr("step", 0.001).attr("value", 0).style("width", "300px");
const readout = controls.append("span");
const readout2 = root.append("div").style("font-size", "18px").style("margin-bottom", "2px");

const svg = root.append("svg").attr("viewBox", [0, 0, W, H]).style("width", "100%");
const axisLabel = (x, y, text, rot) => svg.append("text").attr("text-anchor", "middle").attr("font-size", 17)
  .attr("transform", `translate(${x},${y})${rot ? " rotate(-90)" : ""}`).text(text);

// Left: angle distribution
const xa = d3.scaleLinear([0, 180], [m.left, split - 30]);
const ya = d3.scaleLinear([0, 3], [H - m.bottom, m.top]);
svg.append("g").attr("transform", `translate(0,${H - m.bottom})`)
  .call(d3.axisBottom(xa).tickValues([0, 45, 90, 135, 180])).style("font-size", "15px");
svg.append("g").attr("transform", `translate(${m.left},0)`).call(d3.axisLeft(ya).ticks(5)).style("font-size", "15px");
axisLabel((m.left + split - 30) / 2, H - 10, "angle θ to the field (degrees)");
axisLabel(22, (H - m.bottom) / 2, "probability density", true);
const thetas = d3.range(0, 180.5, 1);
const lineA = d3.line(([t, p]) => xa(t), ([t, p]) => ya(Math.min(p, 3)));
const deg = Math.PI / 180;
svg.append("path").attr("d", lineA(thetas.map((t) => [t, Math.sin(t * deg) / 2]))) // free rotation: sinθ/2
  .attr("stroke", "#aaa").attr("stroke-width", 3).attr("stroke-dasharray", "6 4").attr("fill", "none");
svg.append("text").attr("x", xa(120)).attr("y", ya(0.62)).attr("font-size", 15).attr("fill", "#888").text("free rotation");
const boltz = svg.append("path").attr("stroke", "#1f77b4").attr("stroke-width", 4).attr("fill", "none");

// Right: |w|/kT, exact and small-x approximation
const xb = d3.scaleLog([0.05, 20], [split + 60, W - m.right]);
const yb = d3.scaleLog([1e-4, 100], [H - m.bottom, m.top]);
svg.append("g").attr("transform", `translate(0,${H - m.bottom})`).call(d3.axisBottom(xb).ticks(4, "~g"))
  .style("font-size", "15px");
svg.append("g").attr("transform", `translate(${split + 60},0)`).call(d3.axisLeft(yb).ticks(4, "~g"))
  .style("font-size", "15px");
axisLabel((split + 60 + W - m.right) / 2, H - 10, "u₀/kT");
axisLabel(split + 12, (H - m.bottom) / 2, "−w / kT", true);
const xs = d3.range(Math.log10(0.05), Math.log10(20) + 0.01, 0.02).map((l) => 10 ** l);
const lineB = d3.line(([x, w]) => xb(x), ([x, w]) => yb(w));
svg.append("path").attr("d", lineB(xs.map((x) => [x, Math.log(sinhc(x))])))
  .attr("stroke", "#1f77b4").attr("stroke-width", 3).attr("fill", "none");
svg.append("path").attr("d", lineB(xs.filter((x) => x * x / 6 < 100).map((x) => [x, x * x / 6])))
  .attr("stroke", "#ff7f0e").attr("stroke-width", 3).attr("stroke-dasharray", "6 4").attr("fill", "none");
svg.append("text").attr("x", xb(0.07)).attr("y", yb(30)).attr("font-size", 15).attr("fill", "#1f77b4")
  .text("exact: ln(sinh x / x)");
svg.append("text").attr("x", xb(0.07)).attr("y", yb(9)).attr("font-size", 15).attr("fill", "#ff7f0e")
  .text("high T: x²/6");
const dot = svg.append("circle").attr("r", 7).attr("fill", "#1f77b4");

function update() {
  const x = 10 ** +slider.property("value");
  // p(θ) = sinθ e^{x cosθ} / (2 sinh x / x), normalised over θ in radians; plotted per radian
  boltz.attr("d", lineA(thetas.map((t) => [t, Math.sin(t * deg) * Math.exp(x * Math.cos(t * deg) - Math.log(2 * sinhc(x)))])));
  const w = -Math.log(sinhc(x));
  dot.attr("cx", xb(x)).attr("cy", yb(-w));
  readout.html(`= ${x.toPrecision(2)}`);
  readout2.html(`⟨cos θ⟩ = ${(coth(x) - 1 / x).toFixed(2)} &nbsp;·&nbsp; w/k<sub>B</sub>T = ${w.toPrecision(2)}`
    + ` (high-T formula ${(-x * x / 6).toPrecision(2)}) &nbsp;·&nbsp; ⟨u⟩/k<sub>B</sub>T = ${(-x * (coth(x) - 1 / x)).toPrecision(2)}`);
}

slider.on("input", update);
update();
el.append(root.node());
