// Dipoles induced in the atoms of N-methylacetamide by a draggable ion or water dipole: both polarize.
// Runs with `d3` and the container element `el` in scope (see explorable() in the setup cell).
// Each atom responds only to the source's field (no mutual polarization); vacuum, 300 K.
const W = 900, H = 370;
const s = 55; // px per Å
const ox = 330, oy = 152; // screen position of the carbonyl carbon
const lB = 557; // Bjerrum length in vacuum at 300 K, Å
const kT = 2.494; // kJ/mol at 300 K
const R = 19; // drawn atom radius, px
const rMin = 1.8; // closest ion–atom distance, Å (about a real Mg–O contact)
const ionR = 25; // drawn ion radius, px
// Positions in Å (y up), polarizability volumes α′ in Å³ (free atoms)
const atoms = [
  {el: "C", x: 0, y: 0, a: 1.76},
  {el: "O", x: 1.23, y: 0, a: 0.80},
  {el: "C", x: -0.75, y: 1.30, a: 1.76},
  {el: "N", x: -0.665, y: -1.152, a: 1.10},
  {el: "H", x: -1.665, y: -1.152, a: 0.67},
  {el: "C", x: 0.06, y: -2.408, a: 1.76},
];
const bonds = [[0, 1, 2], [0, 2, 1], [0, 3, 1], [3, 4, 1], [3, 5, 1]]; // [i, j, order]
const ion = {x: 4.5, y: -1.2, z: 2};
// Water dipole drawn as ±q a distance d apart, so its field near the molecule is not the point-dipole one.
const dip = {x: 4.2, y: 1.2, a: Math.PI}; // a: direction of μ (− to +), radians, y up
const mu = 1.85 / 4.803, d = 1.0; // eÅ, Å
const rMinDip = 2.3; // closest dipole centre–atom distance, Å
let source = "ion";
const charges = () => source === "ion" ? [[ion.x, ion.y, ion.z]]
  : [1, -1].map((sg) => [dip.x + sg * Math.cos(dip.a) * d / 2, dip.y + sg * Math.sin(dip.a) * d / 2, sg * mu / d]);
// Too close: push out to rm instead of stopping, so the item slides around the molecule.
const pushOut = (x, y, rm) => {
  for (let k = 0; k < 4; k++)
    for (const a of atoms) {
      const dx = x - a.x, dy = y - a.y, r = Math.hypot(dx, dy) || 1e-6;
      if (r < rm) { x = a.x + dx / r * rm; y = a.y + dy / r * rm; }
    }
  return [x, y];
};
const px = (p) => [ox + p.x * s, oy - p.y * s];

const root = d3.create("div").style("font-family", "sans-serif");
const bar = root.append("div").style("display", "flex").style("align-items", "center").style("gap", "8px")
  .style("margin-bottom", "4px");
const buttons = [["ion", "ion"], ["dipole", "water dipole"]].map(([key, name]) => bar.append("button").text(name)
  .style("font-size", "15px").style("cursor", "pointer").on("click", () => { source = key; update(); }));
const readout = bar.append("div").style("font-size", "20px").style("margin-left", "8px");
const svg = root.append("svg").attr("viewBox", [0, 0, W, H]).style("width", "100%").style("user-select", "none");
// Pointer in viewBox units from the bounding box: getScreenCTM (behind d3.pointer) ignores
// reveal.js's CSS scaling in Safari, which offsets the dragged item from the cursor.
const svgPoint = (ev) => {
  const r = svg.node().getBoundingClientRect();
  const e = ev.sourceEvent.changedTouches ? ev.sourceEvent.changedTouches[0] : ev.sourceEvent;
  return [(e.clientX - r.left) * W / r.width, (e.clientY - r.top) * H / r.height];
};
svg.append("defs").append("marker").attr("id", "pol-arrow").attr("viewBox", "0 0 10 10")
  .attr("refX", 6).attr("refY", 5).attr("markerWidth", 4).attr("markerHeight", 4)
  .attr("orient", "auto").append("path").attr("d", "M0,0L10,5L0,10z").attr("fill", "#d7301f");
svg.append("text").attr("x", W - 10).attr("y", H - 10).attr("text-anchor", "end").attr("font-size", 15)
  .attr("fill", "#555").text("drag to move · click the ion to change its charge · drag the dipole's + end to rotate it");
svg.append("text").attr("x", W - 10).attr("y", H - 32).attr("text-anchor", "end").attr("font-size", 15).attr("fill", "#555")
  .text("red: induced dipoles μ = α′E · shaded: contact surface for the ion");

// Contact surface: the ion's edge rests here when its centre is rMin from an atom.
// Ball-and-stick atoms are drawn much smaller than that, hence a separate surface.
svg.insert("g", ":first-child").attr("fill", "#e8eef5").selectAll("circle").data(atoms).join("circle")
  .attr("cx", (a) => px(a)[0]).attr("cy", (a) => px(a)[1]).attr("r", rMin * s - ionR);
for (const [i, j, order] of bonds) {
  const [x1, y1] = px(atoms[i]), [x2, y2] = px(atoms[j]);
  const nx = -(y2 - y1) / Math.hypot(x2 - x1, y2 - y1), ny = (x2 - x1) / Math.hypot(x2 - x1, y2 - y1);
  for (let k = 0; k < order; k++) {
    const off = (k - (order - 1) / 2) * 9;
    svg.append("line").attr("x1", x1 + nx * off).attr("y1", y1 + ny * off).attr("x2", x2 + nx * off)
      .attr("y2", y2 + ny * off).attr("stroke", "#222").attr("stroke-width", 5);
  }
}
const atomNodes = atoms.map((a) => {
  const [x, y] = px(a);
  const g = svg.append("g").attr("transform", `translate(${x},${y})`);
  g.append("circle").attr("r", R).attr("fill", "white").attr("stroke", "#222").attr("stroke-width", 3);
  g.append("text").attr("text-anchor", "middle").attr("dy", "0.35em").attr("font-size", 19)
    .attr("font-family", "serif").text(a.el);
  const arrow = g.append("line").attr("stroke", "#d7301f").attr("stroke-width", 4)
    .attr("marker-end", "url(#pol-arrow)");
  return {a, arrow};
});

const ionNode = svg.append("g").style("cursor", "grab");
ionNode.append("circle").attr("r", ionR).attr("stroke", "#222").attr("stroke-width", 3);
const ionLabel = ionNode.append("text").attr("text-anchor", "middle").attr("dy", "0.35em")
  .attr("font-size", 17).attr("font-family", "serif").attr("fill", "white");
let grab = [0, 0]; // cursor offset from the ion centre, so the ion doesn't jump
ionNode.call(d3.drag().clickDistance(4).on("start", (ev) => {
  const [cx, cy] = svgPoint(ev), [ix, iy] = px(ion);
  grab = [ix - cx, iy - cy];
}).on("drag", (ev) => {
  const [cx, cy] = svgPoint(ev);
  const [x, y] = pushOut((Math.max(ionR, Math.min(W - ionR, cx + grab[0])) - ox) / s,
    (oy - Math.max(ionR, Math.min(H - ionR, cy + grab[1]))) / s, rMin);
  Object.assign(ion, {x, y});
  update();
}));
ionNode.on("click", () => { ion.z = ion.z > 0 ? -1 : 2; update(); });

const dipNode = svg.append("g");
const dipBody = dipNode.append("line").attr("stroke", "#444").attr("stroke-width", 14).attr("stroke-linecap", "round")
  .style("cursor", "grab");
const dipEnds = ["#1f77b4", "#ff7f0e"].map((c, i) => {
  const g = dipNode.append("g").style("cursor", i === 0 ? "crosshair" : null).style("pointer-events", i === 0 ? null : "none");
  g.append("circle").attr("r", 14).attr("fill", c);
  g.append("text").attr("text-anchor", "middle").attr("dy", "0.35em").attr("fill", "white").attr("font-size", 20)
    .text(i === 0 ? "+" : "−");
  return g;
});
let dgrab = [0, 0];
dipBody.call(d3.drag().on("start", (ev) => {
  const [cx, cy] = svgPoint(ev), [dx, dy] = px(dip);
  dgrab = [dx - cx, dy - cy];
}).on("drag", (ev) => {
  const [cx, cy] = svgPoint(ev);
  const [x, y] = pushOut((Math.max(40, Math.min(W - 40, cx + dgrab[0])) - ox) / s,
    (oy - Math.max(40, Math.min(H - 40, cy + dgrab[1]))) / s, rMinDip);
  Object.assign(dip, {x, y});
  update();
}));
dipEnds[0].call(d3.drag().on("drag", (ev) => {
  const [cx, cy] = svgPoint(ev);
  dip.a = Math.atan2((oy - cy) / s - dip.y, (cx - ox) / s - dip.x);
  update();
}));

function update() {
  let u = 0; // −½ ℓB Σ α′ E² in kT, with E in units of e/(4πε0 Å²)
  const qs = charges();
  const gain = source === "dipole" ? 5 : 1; // a dipole's field is ~10× weaker; keep its arrows visible
  for (const {a, arrow} of atomNodes) {
    let ex = 0, ey = 0;
    for (const [qx, qy, q] of qs) {
      const dx = a.x - qx, dy = a.y - qy, r = Math.hypot(dx, dy);
      ex += q * dx / r ** 3; ey += q * dy / r ** 3;
    }
    const e = Math.hypot(ex, ey);
    const mu = a.a * e; // induced dipole, eÅ
    u += -0.5 * lB * a.a * e * e;
    const len = Math.min(2.6 * R, gain * 300 * mu); // px; μ points along E, from − to +
    const bx = ex / e * len / 2, by = -ey / e * len / 2; // centred on the atom; screen y is flipped
    arrow.attr("x1", -bx).attr("y1", -by).attr("x2", bx).attr("y2", by).attr("display", len < 8 ? "none" : null);
  }
  const [x, y] = px(ion);
  ionNode.attr("transform", `translate(${x},${y})`).attr("display", source === "ion" ? null : "none");
  dipNode.attr("display", source === "dipole" ? null : "none");
  const [[px1, py1], [px2, py2]] = qs.length === 2 ? qs.map((q) => px({x: q[0], y: q[1]})) : [[0, 0], [0, 0]];
  dipBody.attr("x1", px1).attr("y1", py1).attr("x2", px2).attr("y2", py2);
  dipEnds[0].attr("transform", `translate(${px1},${py1})`);
  dipEnds[1].attr("transform", `translate(${px2},${py2})`);
  buttons.forEach((b, i) => b.style("font-weight", ["ion", "dipole"][i] === source ? "bold" : null));
  ionNode.select("circle").attr("fill", ion.z > 0 ? "#1f77b4" : "#ff7f0e");
  ionLabel.text(ion.z > 0 ? "Mg²⁺" : "Cl⁻");
  readout.html(`induction energy −½ Σ α′E² = <b>${u.toPrecision(2)} k<sub>B</sub>T</b> = ${(u * kT).toPrecision(2)} kJ/mol`
    + ` &nbsp;<span style="color:#777">(vacuum, 300 K${gain > 1 ? "; arrows ×5" : ""})</span>`);
}

update();
el.append(root.node());
