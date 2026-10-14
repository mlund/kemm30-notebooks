// |u|/kT for two unit charges against distance, with an ε_r slider and the Bjerrum length marked.
// Runs with `d3` and the container element `el` in scope (see explorable() in the setup cell).
const W = 900, H = 370;
const m = {top: 12, right: 110, bottom: 48, left: 78};
const lB1 = 560.4; // Bjerrum length in vacuum at 298 K, Å
const media = [
  {name: "vacuum", eps: 1},
  {name: "heptane", eps: 1.92},
  {name: "methanol", eps: 33},
  {name: "water", eps: 78.5},
];
const x = d3.scaleLog([1, 1000], [m.left, W - m.right]);
const y = d3.scaleLog([1e-3, 1e3], [H - m.bottom, m.top]);
const curve = (eps) => [[1, lB1 / eps], [1000, lB1 / eps / 1000]]; // straight line on log-log axes

const root = d3.create("div").style("font-family", "sans-serif");
const controls = root.append("div").style("display", "flex").style("align-items", "center")
  .style("gap", "14px").style("font-size", "20px").style("margin-bottom", "4px");
controls.append("span").html("ε<sub>r</sub>");
const slider = controls.append("input").attr("type", "range").attr("min", 0)
  .attr("max", Math.log10(120)).attr("step", 0.001).style("width", "320px");
const readout = controls.append("span").style("min-width", "290px");
for (const md of media)
  controls.append("button").text(md.name).style("font-size", "15px").style("cursor", "pointer")
    .on("click", () => { slider.property("value", Math.log10(md.eps)); update(); });

const svg = root.append("svg").attr("viewBox", [0, 0, W, H]).style("width", "100%");
svg.append("g").attr("transform", `translate(0,${H - m.bottom})`)
  .call(d3.axisBottom(x).ticks(3, "~g")).style("font-size", "15px");
svg.append("g").attr("transform", `translate(${m.left},0)`)
  .call(d3.axisLeft(y).ticks(6, "~g")).style("font-size", "15px");
svg.append("text").attr("x", (m.left + W - m.right) / 2).attr("y", H - 8)
  .attr("text-anchor", "middle").attr("font-size", 17).text("Distance r (Å)");
svg.append("text").attr("transform", `translate(20,${(H - m.bottom) / 2}) rotate(-90)`)
  .attr("text-anchor", "middle").attr("font-size", 17).text("|u| / kT for two unit charges");

const line = d3.line(([r, u]) => x(r), ([r, u]) => y(u));
for (const md of media) { // faint reference lines, labelled at the right edge
  svg.append("path").attr("d", line(curve(md.eps))).attr("stroke", "#ccc").attr("stroke-width", 2).attr("fill", "none");
  svg.append("text").attr("x", W - m.right + 6).attr("y", y(lB1 / md.eps / 1000)).attr("dy", "0.35em")
    .attr("font-size", 14).attr("fill", "#999").text(md.name);
}
svg.append("line").attr("x1", x(1)).attr("x2", x(1000)).attr("y1", y(1)).attr("y2", y(1))
  .attr("stroke", "#666").attr("stroke-dasharray", "6 4");
svg.append("text").attr("x", x(1) + 6).attr("y", y(1) - 8).attr("font-size", 15).attr("fill", "#555").text("|u| = kT");

const active = svg.append("path").attr("stroke", "#1f77b4").attr("stroke-width", 4).attr("fill", "none");
const drop = svg.append("line").attr("stroke", "#1f77b4").attr("stroke-dasharray", "2 4").attr("stroke-width", 2);
const dot = svg.append("circle").attr("r", 7).attr("fill", "#1f77b4");

function update() {
  const eps = 10 ** +slider.property("value");
  const lB = lB1 / eps;
  active.attr("d", line(curve(eps)));
  const inside = lB >= 1 && lB <= 1000; // marker only when ℓB lies on the plotted range
  dot.attr("display", inside ? null : "none").attr("cx", x(lB)).attr("cy", y(1));
  drop.attr("display", inside ? null : "none").attr("x1", x(lB)).attr("x2", x(lB)).attr("y1", y(1)).attr("y2", H - m.bottom);
  readout.html(`ε<sub>r</sub> = ${eps.toPrecision(3)} &nbsp; ℓ<sub>B</sub> = ${lB.toPrecision(3)} Å`);
}

slider.property("value", Math.log10(78.5)).on("input", update);
update();
el.append(root.node());
