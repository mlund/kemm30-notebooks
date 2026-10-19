"""KEMM30 day 4 (ion solvation, Born energy, salt screening teaser) as a Blikfang bundle.

usage: python3 -I tools/day4_deck.py [out bundle]   (default intermolecular/day4.blikfang)

The deck is generated so it can be rebuilt; edit this file, not deck.json.
Units in the scenes: Å and k_BT at 298 K; vacuum Bjerrum length 560.4 Å.
"""

import json
import math
import re
import shutil
import sys
from pathlib import Path

LB0 = 560.4  # Å, vacuum Bjerrum length at 298 K
EPS_W = 78.4

# Explorable 1: R/a from 1 to RA_MAX maps log-linearly onto the handle's sideways run.
CX, R0, SPAN, RA_MAX = 250.0, 30.0, 200.0, 50.0


def hx_of(ra):
    return CX + R0 + SPAN * math.log(ra) / math.log(RA_MAX)


def frame(x, y, w, h):
    return {"x": x, "y": y, "w": w, "h": h}


def text(eid, x, y, w, h, md, **style):
    config = {"text": md}
    if style:
        config["style"] = style
    return {"id": eid, "kind": "text", "frame": frame(x, y, w, h), "config": config}


def title(sid, md):
    return text(f"{sid}-title", 80, 30, 1440, 75, f"## {md}")


def puzzle(eid, x, y, w, h, **config):
    return {"id": eid, "kind": "puzzle", "frame": frame(x, y, w, h), "config": config}


def scene(eid, x, y, w, h, size, script, handles=None):
    config = {"size": size, "script": script.strip()}
    if handles:
        config["handles"] = handles
    return {"id": eid, "kind": "scene", "frame": frame(x, y, w, h), "config": config}


def button(eid, x, y, w, label, run):
    return {
        "id": eid,
        "kind": "button",
        "frame": frame(x, y, w, 48),
        "config": {"label": label, "run": run},
    }


def slider(eid, x, y, w, bind, lo, hi, log=False):
    config = {"bind": bind, "min": lo, "max": hi}
    if log:
        config["log"] = True
    return {"id": eid, "kind": "slider", "frame": frame(x, y, w, 40), "config": config}


def reveal_after(*pairs):
    """Click builds that show each element after its puzzle has been discussed.

    In a presented lecture quizzes are class prompts, so nothing waits on a solved puzzle;
    elements that follow the same puzzle appear together.
    """
    builds, last = [], None
    for el, pz in pairs:
        trigger = "with-previous" if pz == last else "click"
        builds.append({"element": el, "trigger": trigger, "effect": "dissolve"})
        last = pz
    return builds


# --- slides -----------------------------------------------------------------


CONVERGENCE = r"""
let cx = CX_; let cy = 250.0; let r0 = R0_; let span = SPAN_;
let L = RA_MAX_.ln();
let rr = hx - cx;                          // shell radius on screen
let Ra = ((rr - r0) / span * L).exp();     // R/a, log scale
let out = [];
// solvent sphere
out.push(disc(cx, cy, rr).fill("aqua").stroke("aqua").opacity(0.25));
// solvent dipoles on rings, oxygen end (dot) towards a cation, along the field of a dipole
let ring = r0 + 22.0;
if cont > 0.5 {
    out.push(disc(cx, cy, rr).fill("aqua").stroke("none").opacity(0.35));
    out.push(text(cx, cy + r0 + 30.0, "εᵣ = 78").size(21));
    ring = rr;   // no molecules
}
while ring < rr - 10.0 {
    let n = (2.0 * 3.14159 * ring / 34.0).floor();
    let k = 0.0;
    while k < n {
        let t = 2.0 * 3.14159 * k / n + ring * 0.05;
        let ux = t.cos(); let uy = t.sin();
        let dx = 0.0; let dy = 0.0;
        if dip > 0.5 {
            // field of a point dipole along +x: 3 (p·u) u − p
            let pu = ux;
            dx = 3.0 * pu * ux - 1.0; dy = 3.0 * pu * uy;
            let m = (dx * dx + dy * dy).sqrt(); dx /= m; dy /= m;
        } else { dx = ux; dy = uy; }
        // Thermal disorder: alignment falls with the field, E ∝ r⁻² (ion) or r⁻³ (dipole),
        // so the first shell is ordered and far molecules point almost anywhere.
        let order = (r0 + 22.0) / ring;
        order = if dip > 0.5 { order * order * order } else { order * order };
        let h = (k * 12.9898 + ring * 78.233).sin() * 43758.5453;
        let u = h - h.floor();   // pseudo-random in [0, 1), fixed per molecule
        let tilt = (1.0 - order) * (2.0 * u - 1.0) * 3.14159;
        let c = tilt.cos(); let sn = tilt.sin();
        let rx = dx * c - dy * sn; dy = dx * sn + dy * c; dx = rx;
        let px = cx + ring * ux; let py = cy + ring * uy;
        out.push(line(px - 8.0 * dx, py - 8.0 * dy, px + 8.0 * dx, py + 8.0 * dy).stroke("blue").width(2));
        out.push(disc(px - 8.0 * dx, py - 8.0 * dy, 3.5).fill("red").stroke("none"));
        k += 1.0;
    }
    ring += 28.0;
}
// the solute
if dip > 0.5 {
    out.push(disc(cx, cy, r0).fill("surface").stroke("text"));
    out.push(line(cx - 18.0, cy, cx + 18.0, cy).stroke("orange").width(4).arrow());
} else {
    out.push(disc(cx, cy, r0).fill("blue").stroke("none"));
    out.push(text(cx, cy, "+").fill("background").size(30));
}
out.push(line(cx, cy, hx, cy).stroke("faint").width(1).dash(4, 4));
out.push(disc(hx, cy, 11).fill("accent").stroke("none"));
out.push(text(cx, 30, "R = " + fixed(Ra, 1) + " a   (log scale)").size(21));
out.push(text(cx, 440, "drag the edge of the solvent").size(21).fill("faint"));

// panel A: fraction of the full solvation energy inside R
let pa = plot(640, 20, 520, 190).x_log(1, RA_MAX_).y_lin(0, 1).text(21);
out.push(pa.axes("R / a", "fraction inside R"));
out.push(pa.vline(Ra).stroke("faint").width(1).dash(4, 4));
out.push(pa.curve(|v| 1.0 - 1.0 / v).stroke("blue").width(3));
out.push(pa.curve(|v| 1.0 - 1.0 / (v * v * v)).stroke("orange").width(3));
let fi = 1.0 - 1.0 / Ra; let fd = 1.0 - 1.0 / (Ra * Ra * Ra);
out.push(disc(pa.x(Ra), pa.y(fi), 6).fill("blue").stroke("none"));
out.push(disc(pa.x(Ra), pa.y(fd), 6).fill("orange").stroke("none"));
out.push(text(pa.x(RA_MAX_) - 4, pa.y(0.62), "ion (Born)").fill("blue").anchor("end").size(21));
out.push(text(pa.x(RA_MAX_) - 4, pa.y(0.9) + 20, "dipole (Onsager)").fill("orange").anchor("end").size(21));

// panel B: contribution per shell, d(fraction)/d(R/a)
let pb = plot(640, 285, 520, 150).x_log(1, RA_MAX_).y_log(0.0001, 3).text(21);
out.push(pb.axes("R / a", "per shell"));
out.push(pb.vline(Ra).stroke("faint").width(1).dash(4, 4));
out.push(pb.curve(|v| 1.0 / (v * v)).stroke("blue").width(3));
out.push(pb.curve(|v| 3.0 / (v * v * v * v)).stroke("orange").width(3));
out.push(text(pb.x(3.0), pb.y(0.3), "∝ r⁻²").fill("blue").anchor("start").size(21));
out.push(text(pb.x(1.3), pb.y(0.0003), "∝ r⁻⁴").fill("orange").anchor("start").size(21));

// readouts: a = 2 Å monovalent ion and a water-like dipole (1.85 D, a = 1.4 Å), ε = 78.4
let gi = BORN_ION_; let gd = ONSAGER_;
out.push(text(20, 480, "ion: " + fixed(100.0 * fi, 1) + " % of −" + fixed(gi, 1) + " k_BT = −" + fixed(gi * fi, 1) + " k_BT")
    .fill("blue").anchor("start").size(21));
out.push(text(20, 520, "dipole: " + fixed(100.0 * fd, 1) + " % of −" + fixed(gd, 1) + " k_BT = −" + fixed(gd * fd, 1) + " k_BT")
    .fill("orange").anchor("start").size(21));
out
"""


CYCLE = r"""
// A closed loop: the transfer (top, unknown) equals discharge + move + charge.
let out = [];
out.push(rect(60, 20, 520, 470).fill("aqua").stroke("none").opacity(0.18));
out.push(rect(820, 20, 520, 470).fill("yellow").stroke("none").opacity(0.22));
out.push(text(320, 470, "solvent 1, ε₁ (e.g. water)").size(20).fill("faint"));
out.push(text(1080, 470, "solvent 2, ε₂ (e.g. oil)").size(20).fill("faint"));
for b in [[170.0, 70.0, true], [930.0, 70.0, true], [170.0, 300.0, false], [930.0, 300.0, false]] {
    out.push(rect(b[0], b[1], 300, 110).fill("surface").stroke("line").width(2));
    let cx = b[0] + 70.0; let cy = b[1] + 55.0;
    if b[2] {
        out.push(disc(cx, cy, 30).fill("blue").stroke("none"));
        out.push(text(cx, cy, "+").fill("background").size(28));
        out.push(text(cx + 140.0, cy, "ion").size(22));
    } else {
        out.push(disc(cx, cy, 30).fill("line").stroke("text").width(1));
        out.push(text(cx + 140.0, cy, "neutral sphere").size(20));
    }
}
// transfer: what we want
out.push(line(480, 125, 920, 125).stroke("text").width(3).dash(10, 6).arrow());
out.push(text(700, 100, "transfer  ΔG₁→₂ = ?").size(22));
// the detour
out.push(line(320, 185, 320, 295).stroke("blue").width(4).arrow());
out.push(text(335, 232, "discharge").anchor("start").size(20).fill("blue"));
out.push(text(335, 258, "−q²/8πε₀ε₁a").anchor("start").size(20).fill("blue"));
out.push(line(480, 355, 920, 355).stroke("blue").width(4).arrow());
out.push(text(700, 335, "move: 0 (nothing to screen)").size(20).fill("blue"));
out.push(line(1080, 295, 1080, 185).stroke("blue").width(4).arrow());
out.push(text(1065, 232, "charge").anchor("end").size(20).fill("blue"));
out.push(text(1065, 258, "+q²/8πε₀ε₂a").anchor("end").size(20).fill("blue"));
out
"""


EXPLORER = r"""
let lB0 = 560.4;
let g0 = val * val * lB0 / (2.0 * a);           // full self-energy, k_BT
let gA = -g0 * (1.0 - 1.0 / epsA);
let gB = -g0 * (1.0 - 1.0 / epsB);
let lo = -g0 * 1.08;
let out = [];

// energy levels
let pl = plot(110, 30, 360, 420).x_lin(0, 1).y_lin(lo, 0).text(19);
// own y axis: the x position carries no meaning here
let step = 10.0 ** (g0.ln() / 2.302585).floor();
if g0 / step < 3.0 { step /= 2.0; }
out.push(line(pl.x(0.0), pl.y(lo), pl.x(0.0), pl.y(0.0)).stroke("faint").width(1));
let tk = 0.0;
while tk >= lo {
    out.push(line(pl.x(0.0) - 6.0, pl.y(tk), pl.x(0.0), pl.y(tk)).stroke("faint").width(1));
    out.push(text(pl.x(0.0) - 10.0, pl.y(tk), fixed(tk, 0)).anchor("end").fill("faint").size(19));
    tk -= step;
}
out.push(text(30, pl.y(lo / 2.0), "ΔG_solv  (k_BT)").rotate(-90.0).fill("faint").size(19));
out.push(line(pl.x(0.05), pl.y(0.0), pl.x(0.95), pl.y(0.0)).stroke("faint").width(3));
out.push(text(pl.x(0.5), pl.y(0.0) + 22, "vacuum").fill("faint").size(19));
out.push(line(pl.x(0.05), pl.y(gA), pl.x(0.45), pl.y(gA)).stroke("blue").width(5));
out.push(text(pl.x(0.25), pl.y(gA) + 24, "A").fill("blue").size(20));
out.push(line(pl.x(0.55), pl.y(gB), pl.x(0.95), pl.y(gB)).stroke("orange").width(5));
out.push(text(pl.x(0.75), pl.y(gB) + 24, "B").fill("orange").size(20));
if (gB - gA).abs() > 0.5 {
    out.push(line(pl.x(0.5), pl.y(gA), pl.x(0.5), pl.y(gB)).stroke("text").width(3).arrow());
}

// one curve, two solvents on it
let pr = plot(640, 30, 700, 420).x_log(1, 100).y_lin(lo, 0).text(19);
out.push(pr.axes("dielectric constant εᵣ", "ΔG_solv  (k_BT)"));
out.push(pr.hline(-g0).stroke("faint").width(1).dash(6, 4));
out.push(text(pr.x(100.0) - 6, pr.y(-g0) + 22, "εᵣ → ∞").anchor("end").fill("faint").size(19));
out.push(pr.curve(|e| -g0 * (1.0 - 1.0 / e)).stroke("purple").width(3));
out.push(pr.line([[epsA, gA], [epsB, gA]]).stroke("faint").width(1).dash(4, 4));
if (gB - gA).abs() > 0.5 {
    out.push(line(pr.x(epsB), pr.y(gA), pr.x(epsB), pr.y(gB)).stroke("text").width(2).arrow());
}
out.push(disc(pr.x(epsA), pr.y(gA), 9).fill("blue").stroke("none"));
out.push(disc(pr.x(epsB), pr.y(gB), 9).fill("orange").stroke("none"));

let kj = 2.479;   // kJ/mol per k_BT at 298 K
let tr = gB - gA;
let sgn = if tr >= 0.0 { "+" } else { "" };
out.push(text(20, 545, "A: " + fixed(gA, 1) + " k_BT (" + fixed(gA * kj, 0) + " kJ/mol)").anchor("start").fill("blue").size(19));
out.push(text(380, 545, "B: " + fixed(gB, 1) + " k_BT (" + fixed(gB * kj, 0) + " kJ/mol)").anchor("start").fill("orange").size(19));
out.push(text(1380, 545, "transfer A → B: " + sgn + fixed(tr, 1) + " k_BT (" + sgn + fixed(tr * kj, 0) + " kJ/mol)").anchor("end").size(21));
out
"""


TEST = r"""
let p = plot(110, 30, 560, 360).x_lin(0.4, 0.75).y_lin(-560, -320).text(18);
let out = [p.axes("1 / a  (Å⁻¹)", "ΔH  (kJ/mol)")];
out.push(p.curve(|v| -696.6 * v).stroke("blue").width(3));
out.push(text(p.x(0.74), p.y(-696.6 * 0.74) + 24, "Born, Eq. 22.66").fill("blue").anchor("end").size(18));
for ion in [["Na⁺", 1.680, -414.6], ["Cl⁻", 1.937, -359.8]] {
    let x = p.x(1.0 / ion[1]); let y = p.y(ion[2]);
    out.push(disc(x, y, 8).fill("orange").stroke("none"));
    out.push(text(x + 12, y - 12, ion[0]).anchor("start").size(18));
}
out
"""


INTERFACE = r"""
let e1 = 78.4; let lB0 = 560.4;
let p0 = plot(110, 300, 1040, 220).x_lin(-20, 20).text(21);
let x0 = p0.x(-20.0); let x1 = p0.x(20.0); let xs = (x1 - x0) / 40.0;  // units per Å
let s = -20.0 + (ix - x0) / xs;            // ion centre, Å; > 0 is the upper phase
let pre = val * val * lB0;
let born2 = pre / (2.0 * a) * (1.0 / eps2 - 1.0 / e1);
let k = (e1 - eps2) / (e1 + eps2);
let gw = pre * k / (4.0 * a * e1);              // sharp model at s = −a
let gu = born2 - pre * k / (4.0 * a * eps2);     // sharp model at s = +a
// slopes there, so the blend inside one radius joins both sides smoothly
let mw = pre * k / (4.0 * e1 * a * a);
let mu = pre * k / (4.0 * eps2 * a * a);
let G = |t| {
    if smooth > 0.5 {
        // Born goes as 1/ε, so blend 1/ε: the rise is then centred on the surface
        born2 * (1.0 + (t / w).tanh()) / 2.0
    } else if t <= -a {
        pre * k / (4.0 * (-t) * e1)
    } else if t >= a {
        born2 - pre * k / (4.0 * t * eps2)
    } else {
        // cubic Hermite blend: matches value and slope at both ends
        let h = 2.0 * a; let u = (t + a) / h;
        let u2 = u * u; let u3 = u2 * u;
        (2.0 * u3 - 3.0 * u2 + 1.0) * gw + (u3 - 2.0 * u2 + u) * h * mw
            + (3.0 * u2 - 2.0 * u3) * gu + (u3 - u2) * h * mu
    }
};
let lo = 0.0; let hi = born2 * 1.1;
if zoom > 0.5 { lo = -1.0; hi = 3.0; }
let p = p0.y_lin(lo, hi);
let name = if eps2 < 1.5 { "air" } else if eps2 < 5.0 { "oil" } else { "octanol" };

let out = [];
// picture: water on the left, upper phase on the right
let top = 20.0; let bh = 220.0;
if smooth > 0.5 {
    let n = 80.0; let i = 0.0;
    while i < n {
        let t0 = -20.0 + 40.0 * i / n; let tm = t0 + 20.0 / n;
        let fw = (1.0 - (tm / w).tanh()) / 2.0;
        out.push(rect(p.x(t0), top, xs * 40.0 / n + 0.5, bh).fill("aqua").stroke("none").opacity(0.35 * fw));
        i += 1.0;
    }
} else {
    out.push(rect(x0, top, p.x(0.0) - x0, bh).fill("aqua").stroke("none").opacity(0.35));
}
out.push(line(p.x(0.0), top, p.x(0.0), top + bh).stroke("faint").width(1).dash(4, 4));
out.push(text(x0 + 10, top + 24, "water, εᵣ = 78").anchor("start").size(21));
out.push(text(x1 - 10, top + 24, name + ", εᵣ = " + fixed(eps2, 0)).anchor("end").size(21));
let cy = top + bh / 2.0;
out.push(disc(ix, cy, a * xs).fill("blue").stroke("text").opacity(0.85));
let lab = if val > 1.5 { fixed(val, 0) + "+" } else { "+" };
out.push(text(ix, cy, lab).fill("background").size(26));

// free energy
out.push(p.axes("ion position (Å)", "ΔG − ΔG_water  (k_BT)"));
out.push(p.vline(0).stroke("faint").width(1).dash(4, 4));
out.push(p.hline(0).stroke("faint").width(1));
out.push(p.curve(G, 400).stroke("orange").width(3));
let g = G.call(s);
let gy = if g > hi { hi } else if g < lo { lo } else { g };
out.push(disc(p.x(s), p.y(gy), 8).fill("orange").stroke("none"));
out.push(text(x1, 285, "ΔG = " + fixed(g, 2) + " k_BT").anchor("end").size(21));
let note = if smooth > 0.5 { "local Born, 1/ε(z) a tanh of width " + fixed(w, 1) + " Å" }
           else { "Born + image charge; a smooth blend within one radius of the interface" };
out.push(text(x0, 285, note).anchor("start").size(21).fill("faint"));
out
"""


def everyday():
    return {
        "id": "everyday",
        "elements": [
            title("everyday", "Born in the kitchen and in the cell"),
            text(
                "everyday-body",
                80,
                120,
                1440,
                640,
                "- **Vinaigrette:** salt does not dissolve in oil, so dissolve it in the vinegar first.\n"
                "- **Chili:** capsaicin is neutral and oily. Water does not help, milk fat does.\n"
                "- **Soap:** the charged head stays in water, the tail goes into the grease.\n"
                "- **Membranes** are ion-tight, so cells need channels and carriers. "
                "Valinomycin wraps K⁺ in a neutral shell: a larger $a$ lowers the Born cost (Dill 22.11).\n"
                "- **Proteins:** charged residues sit on the surface.",
                spacing={"between": 0.35},
            ),
            text(
                "everyday-q",
                80,
                790,
                1440,
                130,
                "**Question:** Why would burying one Asp⁻ in a protein core ($\\varepsilon_r \\approx 4$) "
                "unfold many proteins?",
            ),
        ],
        "builds": [{"element": "everyday-body", "delivery": "by-paragraph"}],
    }


SCREEN_MAP = r"""
let ang = 10.0;                                  // scene units per Å
let a = 2.0;
let lB = 560.4 / eps;
let kap = (8.0 * 3.14159265 * lB * salt * 0.0006022).sqrt();   // Å⁻¹
let qs = [charge(q1, x1, y1), charge(q2, x2, y2)];
let out = [];
let screened = true;
let grid = ();
try {
    grid = potential_grid(qs, width, height, 6, a * ang, kap / ang);
} catch {
    grid = potential_grid(qs, width, height, 6, a * ang);
    screened = false;
}
out.push(heatmap(grid, 0.6 * lB * ang));
for c in [[x1, y1, q1], [x2, y2, q2]] {
    out.push(disc(c[0], c[1], ang / kap).fill("none").stroke("text").width(1.5).dash(6, 6).opacity(0.6));
    out.push(disc(c[0], c[1], a * ang).fill(if c[2] > 0.0 { "blue" } else { "red" }).stroke("text").width(1));
    out.push(text(c[0], c[1], if c[2] > 0.0 { "+" } else { "−" }).fill("background").size(24));
}
out.push(text(16, 486, "drag the ions · tap one to flip its sign · dashed ring: Debye length").anchor("start").size(22).fill("faint"));
out.push(text(984, 30, "κ⁻¹ = " + fixed(1.0 / kap, 1) + " Å").anchor("end").size(22));
if !screened {
    out.push(text(500, 250, "unscreened: this Blikfang lacks potential_grid(…, kappa)").size(22).fill("red"));
}
out
"""

SCREEN_PLOT = r"""
let a = 2.0;
let lB = 560.4 / eps;
let kap = (8.0 * 3.14159265 * lB * salt * 0.0006022).sqrt();
let zz = q1 * q2;
let d = ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)).sqrt() / 10.0;
let R = if d < 2.0 * a { 2.0 * a } else { d };
let f = (1.0 + kap * a) * (1.0 + kap * a);
let p = plot(125, 20, 440, 360).x_lin(4, 60).y_lin(-6, 6).text(22);
let out = [p.axes("R  (Å)", "w / k_BT")];
out.push(p.hline(0).stroke("faint").width(1));
out.push(p.hline(1).stroke("faint").width(1).dash(6, 4));
out.push(p.hline(-1).stroke("faint").width(1).dash(6, 4));
out.push(p.curve(|r| zz * lB / r).stroke("line").width(2));
out.push(p.curve(|r| zz * lB * (-kap * (r - 2.0 * a)).exp() / (f * r)).stroke("purple").width(3));
let wR = zz * lB * (-kap * (R - 2.0 * a)).exp() / (f * R);
let xR = if R > 60.0 { 60.0 } else { R };
let yR = if wR > 6.0 { 6.0 } else if wR < -6.0 { -6.0 } else { wR };
out.push(disc(p.x(xR), p.y(yR), 8).fill("purple").stroke("none"));
out.push(text(560, 485, "w = " + fixed(wR, 2) + " k_BT at R = " + fixed(R, 1) + " Å").anchor("end").size(22));
out.push(text(p.x(58.0), p.y(zz * lB / 58.0) - 12, "no salt").anchor("end").size(22).fill("faint"));
out
"""


NOTES = {}  # media file name -> Markdown, written by main()


def box(eid, x, y, w, h, md, take=False, scale=0.8):
    """A card behind text: key concepts (line border) or take-home messages (accent border)."""
    card = {
        "id": f"{eid}-card",
        "kind": "shape",
        "frame": frame(x, y, w, h),
        "config": {"shape": "rect", "radius": 16},
        "style": {
            "fill": "surface",
            "border": {"color": "accent" if take else "line", "width": 3},
        },
    }
    return [card, text(eid, x + 30, y + 24, w - 60, h - 48, md, scale=scale)]


def notes_slide(sid, md):
    """A Markdown page for what does not fit on slides: full derivations and sources."""
    NOTES[f"{sid}.md"] = md.strip() + "\n"
    return {"id": sid, "page": {"notes": {"src": f"media/{sid}.md"}}}


def take_home(sid, heading, md):
    return {
        "id": sid,
        "elements": [
            title(sid, heading),
            *box(f"{sid}-box", 80, 160, 1440, 700, md, take=True, scale=0.9),
        ],
    }


# --- slides -------------------------------------------------------------------


def title_slide():
    return {
        "id": "title",
        "elements": [
            text(
                "t-head",
                80,
                320,
                1440,
                160,
                "# Ion solvation and the Born energy",
                align="center",
                scale=1.4,
            ),
            text(
                "t-sub",
                80,
                500,
                1440,
                120,
                "Why salt dissolves in water but not in oil, what that costs, and how salt itself "
                "weakens electric interactions",
                align="center",
            ),
            text(
                "t-ref",
                80,
                700,
                1440,
                60,
                "KEMM30 · day 4 · Dill & Bromberg ch. 22, pp. 444–451",
                align="center",
                colour="faint",
                scale=0.8,
            ),
        ],
    }


def opening():
    return {
        "id": "opening",
        "elements": [
            title("opening", "1. Salt dissolves in water, but not in oil. Why?"),
            text(
                "opening-body",
                80,
                110,
                1440,
                250,
                "On day 2 two ions in contact attracted each other by about **200 $k_BT$** in vacuum, "
                "**100 $k_BT$** in oil, but only **2.5 $k_BT$** in water. Water weakens the attraction "
                "80-fold. Today we ask what water does for a *single* ion.\n\n"
                "**Question:** What does water do for an ion that oil cannot?",
                scale=0.9,
            ),
            puzzle(
                "opening-p",
                80,
                400,
                1440,
                210,
                mode="choice",
                tries=3,
                options=[
                    {
                        "text": "Its dipoles turn towards the ion and lower the energy of the ion's field",
                        "correct": True,
                        "hint": "Yes: the solvent is polarized by the ion.",
                    },
                    {
                        "text": "Water reacts chemically with Na⁺ and Cl⁻",
                        "hint": "No bonds form or break: the ions stay intact. Think about the ion's electric field.",
                    },
                    {
                        "text": "Oil molecules are too big to fit between the ions",
                        "hint": "Size is not it: even small apolar liquids, like hexane, hardly dissolve salt.",
                    },
                    {
                        "text": "Salt is denser than oil",
                        "hint": "Density does not set solubility: sugar is denser than oil too, and dissolves in water.",
                    },
                ],
                feedback={
                    "correct": "Water's dipoles orient round the ion and partly cancel its field.",
                    "reveal": "Water polarizes round the ion and screens its field ($\\varepsilon_r \\approx 78$).",
                },
            ),
            text(
                "opening-next",
                80,
                760,
                1440,
                120,
                "Today we put a number on this, the **Born energy**, and use it for oil → water transfer, "
                "drugs, and ions near a water surface.",
                scale=0.85,
            ),
        ],
        "builds": reveal_after(("opening-next", "opening-p")),
    }


def charging():
    return {
        "id": "charging",
        "elements": [
            title(
                "charging",
                "2. Charging a sphere costs work, because like charges repel",
            ),
            text(
                "charging-body",
                80,
                100,
                1440,
                490,
                "Bring the charge $q$ onto a sphere of radius $a$ in small bits. Each new bit is pushed "
                "away by the charge already there, so every bit costs a little more than the last.\n\n"
                "- When the sphere holds $\\lambda q$ (with $\\lambda$ going from 0 to 1), its surface potential is "
                "$\\psi(\\lambda) = \\lambda q/(4\\pi\\varepsilon_0\\varepsilon_r a)$.\n"
                "- The next bit, $q\\,d\\lambda$, costs $\\psi(\\lambda)\\,q\\,d\\lambda$. Adding up all the bits:\n\n"
                "$$\\Delta G = \\int_0^1 \\psi(\\lambda)\\,q\\,d\\lambda "
                "= \\frac{q^2}{4\\pi\\varepsilon_0\\varepsilon_r a}\\int_0^1\\lambda\\,d\\lambda "
                "= \\frac{q^2}{8\\pi\\varepsilon_0\\varepsilon_r a}$$",
                scale=0.8,
                spacing={"between": 0.3},
            ),
            *box(
                "charging-key",
                80,
                610,
                1440,
                280,
                "**Key concept.** Charging a sphere costs $\\Delta G = \\dfrac{q^2}{8\\pi\\varepsilon_0\\varepsilon_r a} "
                "= \\dfrac{z^2\\ell_B}{2a}\\,k_BT$, with $\\ell_B$ the Bjerrum length (next slide). The ½ appears because each bit meets only the charge already "
                "there. Small, highly charged spheres are expensive; a medium with $\\varepsilon_r > 1$ makes them cheaper.",
            ),
            text(
                "charging-ref",
                80,
                895,
                1440,
                60,
                "Dill Ex. 22.10, Eqs. 22.53–22.55. At 25 °C, $k_BT$ = 2.48 kJ/mol = 0.593 kcal/mol. Full derivation on the next page.",
                scale=0.62,
                colour="faint",
            ),
        ],
        "builds": [{"element": "charging-body", "delivery": "by-paragraph"}],
    }


NOTES_CHARGING = r"""
# Charging a sphere, step by step

**The model.** An ion is a sphere of radius $a$ with its charge $q = ze$ spread over the
surface. It sits in a uniform medium with dielectric constant $\varepsilon_r$. We ask how much
reversible work it takes to put the charge there, starting from a neutral sphere.

**Why charge it gradually.** We cannot place the whole charge at once and multiply by the
final potential: the first bits of charge arrived when the sphere was still neutral and cost
nothing, while the last bits had to be pushed against almost the full charge. So we add the
charge in small steps and add up the cost of each step.

**The steps.** Let $\lambda$ run from 0 (neutral) to 1 (fully charged). When the sphere carries
$\lambda q$, the potential at its surface is that of a point charge at its centre,

$$\psi(\lambda) = \frac{\lambda q}{4\pi\varepsilon_0\varepsilon_r a}.$$

Bringing the next bit $dq = q\,d\lambda$ from far away to the surface costs
$dG = \psi(\lambda)\,q\,d\lambda$. Adding all the steps,

$$\Delta G = \int_0^1 \frac{\lambda q}{4\pi\varepsilon_0\varepsilon_r a}\,q\,d\lambda
= \frac{q^2}{4\pi\varepsilon_0\varepsilon_r a}\int_0^1 \lambda\,d\lambda
= \frac{q^2}{8\pi\varepsilon_0\varepsilon_r a}.$$

The integral of $\lambda$ gives the factor ½. Dill reaches the same result a second way
(Ex. 22.10): half the surface charge times the final surface potential, integrated over the
surface. Both say the same thing: on average, each bit of charge feels half the final
potential.

**In units of $k_BT$.** With the Bjerrum length $\ell_B = e^2/(4\pi\varepsilon_0\varepsilon_r k_BT)$,

$$\frac{\Delta G}{k_BT} = \frac{z^2\,\ell_B}{2a}.$$

In vacuum $\ell_B^{\rm vacuum} = 560$ Å at 25 °C, so a monovalent ion with $a = 2$ Å costs
$560/4 = 140\,k_BT$, about 350 kJ/mol. In water $\ell_B = 7.1$ Å and the same ion costs only
$1.8\,k_BT$.

**What it means.** The self-energy is large for small ions ($1/a$) and grows with the square
of the charge ($z^2$): a divalent ion costs four times as much as a monovalent one of the same
size. A polarizable medium lowers the cost by $1/\varepsilon_r$. The next slides show where that
saving comes from.

**Notation.** Dill writes the dielectric constant as $D$ and $1/(4\pi\varepsilon_0)$ as $C$; here
$\varepsilon_r$ is the dielectric constant (relative permittivity), as on days 2–3;
$\varepsilon_1$, $\varepsilon_2$, $\varepsilon_{\rm w}$ and $\varepsilon_{\rm oil}$ are its values in particular media. At 25 °C, $k_BT$ = 2.48 kJ/mol = 0.593 kcal/mol.
"""


def charging_number():
    return {
        "id": "charging-number",
        "elements": [
            title("charging-number", "In vacuum, an ion is expensive"),
            text(
                "cn-body",
                80,
                110,
                1440,
                170,
                "In units of $k_BT$ the charging cost is $z^2\\ell_B/2a$, where the Bjerrum length "
                "$\\ell_B = e^2/(4\\pi\\varepsilon_0\\varepsilon_r k_BT)$ is $\\ell_B^{\\rm vacuum} = 560$ Å in vacuum and 7.1 Å in water at 25 °C.",
                scale=0.85,
            ),
            text(
                "cn-q",
                80,
                300,
                1440,
                110,
                "**Question:** What does it cost to charge a monovalent ion with $a = 2$ Å in **vacuum**, in $k_BT$?",
                scale=0.85,
            ),
            puzzle(
                "cn-p",
                80,
                420,
                700,
                70,
                mode="numeric",
                answer=round(LB0 / 4),
                tolerance=6,
                tries=3,
                hints=[
                    "Use $z^2\\ell_B/(2a)$ with the vacuum value of $\\ell_B$.",
                    "$z = 1$, $\\ell_B = 560$ Å, $a = 2$ Å.",
                    "$560/(2 \\cdot 2)$.",
                ],
                feedback={
                    "correct": "Right: 140 $k_BT$, about 350 kJ/mol.",
                    "reveal": "$560/(2\\cdot 2) = 140\\,k_BT$, about 350 kJ/mol.",
                },
            ),
            text(
                "cn-why",
                80,
                640,
                1440,
                250,
                "That is about a hundred hydrogen bonds' worth of free energy, stored in the ion's own field. "
                "It is the energy a solvent can win back. In water almost all of it comes back; "
                "in oil only half. The next slides show how.",
                scale=0.85,
            ),
        ],
        "builds": reveal_after(("cn-why", "cn-p")),
    }


def molecular():
    return {
        "id": "molecular",
        "elements": [
            title("molecular", "3. Each solvent molecule lowers the cost a little"),
            text(
                "molecular-body",
                80,
                100,
                1440,
                520,
                "Around a cation, water molecules turn their oxygen towards the ion and their electron clouds "
                "shift. Each molecule becomes a small dipole along the ion's field, and each lowers the energy.\n\n"
                "- The ion's field at distance $r$ is $E = q/(4\\pi\\varepsilon_0 r^2)$.\n"
                "- One molecule gains $-\\tfrac12\\alpha_{\\rm eff}E^2$, with $\\alpha_{\\rm eff} = \\alpha + \\mu^2/3k_BT$ "
                "(induced plus oriented, day 3).\n"
                "- A shell from $r$ to $r + dr$ holds $\\rho\\,4\\pi r^2 dr$ molecules. Add all shells from the surface $a$ out:\n\n"
                "$$\\Delta G \\approx -\\frac{\\rho\\,\\alpha_{\\rm eff}}{2}\\int_a^\\infty "
                "\\left(\\frac{q}{4\\pi\\varepsilon_0 r^2}\\right)^2 4\\pi r^2\\,dr "
                "= -\\frac{q^2}{8\\pi\\varepsilon_0 a}\\,\\chi$$",
                scale=0.78,
                spacing={"between": 0.3},
            ),
            *box(
                "molecular-key",
                80,
                650,
                1440,
                230,
                "**Key concept.** Solvation is the sum of many small dipole energies. A shell at $r$ adds "
                "$\\propto r^{-4}\\cdot r^2\\,dr = r^{-2}\\,dr$: each far shell gives little, but there are many. "
                "In a dilute solvent the result is set by the susceptibility $\\chi = \\rho\\,\\alpha_{\\rm eff}/\\varepsilon_0 = \\varepsilon_r - 1$.",
            ),
        ],
        "builds": [{"element": "molecular-body", "delivery": "by-paragraph"}],
    }


def born():
    return {
        "id": "born",
        "elements": [
            title(
                "born",
                "4. The Born energy: moving an ion from one dielectric to another",
            ),
            text(
                "born-body",
                80,
                95,
                1440,
                485,
                "The dilute result fails for water: with $\\chi = 77$ it would win back 77 times the whole "
                "self-energy, which is impossible. In a dense liquid the molecules already there screen the "
                "field, so new solvent feels only $E/\\varepsilon_r$. Raising the permittivity from $\\varepsilon_1$ "
                "to $\\varepsilon_2$ in steps $d\\varepsilon_r$ gives\n\n"
                "$$d\\Delta G = -\\frac{q^2}{8\\pi\\varepsilon_0 a}\\,\\frac{d\\varepsilon_r}{\\varepsilon_r^2}"
                "\\qquad\\Rightarrow\\qquad"
                "\\Delta G_{\\rm Born} = \\frac{q^2}{8\\pi\\varepsilon_0 a}"
                "\\left(\\frac1{\\varepsilon_2}-\\frac1{\\varepsilon_1}\\right)$$\n\n"
                "From vacuum ($\\varepsilon_1 = 1$) into water this is the solvation free energy: $-138\\,k_BT$ "
                "(−340 kJ/mol) for $a = 2$ Å. Water wins back 99 % of the self-energy.",
                scale=0.8,
                spacing={"between": 0.3},
            ),
            *box(
                "born-key",
                80,
                565,
                1440,
                410,
                "**Key concept: the Born energy** of moving an ion from medium 1 to medium 2 (Dill Eq. 22.61):\n\n"
                "$$\\Delta G_{\\rm Born} = \\frac{z^2\\ell_B^{\\rm vacuum}}{2a}"
                "\\left(\\frac1{\\varepsilon_2}-\\frac1{\\varepsilon_1}\\right)k_BT,"
                "\\qquad \\ell_B^{\\rm vacuum} = 560\\ \\text{Å}$$\n\n"
                "From vacuum ($\\varepsilon_1 = 1$) it is the solvation free energy. It grows as $z^2$ and falls as $1/a$.",
            ),
        ],
        "builds": [{"element": "born-body", "delivery": "by-paragraph"}],
    }


NOTES_BORN = r"""
# The Born energy from the solvent's point of view

**Picture.** Put an ion into a solvent. The molecules near it turn and distort so that
their negative ends face a cation. Each molecule is now a small dipole in the ion's field, and
each lowers the free energy a little. The solvation free energy is the sum of all these small
contributions.

**One molecule.** A molecule in a field $E$ acquires a dipole $\alpha_{\rm eff}E$ and gains the
free energy $-\tfrac12\alpha_{\rm eff}E^2$ (the ½ for the same reason as in charging: the dipole
builds up as the field grows). The effective polarizability has two parts from day 3:
electronic, $\alpha$, and orientational, $\mu^2/3k_BT$, from the thermal average of a permanent
dipole's alignment.

**All molecules.** The ion's field is $E = q/(4\pi\varepsilon_0 r^2)$. A shell of radius $r$
and thickness $dr$ contains $\rho\,4\pi r^2\,dr$ molecules, with $\rho$ the number density.
Assuming the solvent is uniform outside the ion ($r > a$),

$$\Delta G \approx -\frac{\rho\,\alpha_{\rm eff}}{2}\int_a^\infty
\left(\frac{q}{4\pi\varepsilon_0 r^2}\right)^2 4\pi r^2\,dr
= -\frac{q^2}{8\pi\varepsilon_0 a}\cdot\frac{\rho\,\alpha_{\rm eff}}{\varepsilon_0}.$$

The last factor is the electric susceptibility $\chi$, and for a dilute medium
$\chi = \varepsilon_r - 1$. Each shell contributes in proportion to $r^{-2}\,dr$, so the
integral converges, but slowly: half the energy comes from beyond $r = 2a$.

**Why this fails in a liquid.** For water $\chi \approx 77$, and the formula would win back
77 times the vacuum self-energy. That cannot be: the solvent can at most cancel the field
entirely. The flaw is that each molecule was assumed to feel the bare field of the ion. In a
dense liquid the other molecules have already screened the field to $E/\varepsilon_r$.

**Building the dielectric up.** Add solvent so that the permittivity grows from $\varepsilon_r$
to $\varepsilon_r + d\varepsilon_r$. The new material has susceptibility $d\varepsilon_r$ and feels
the screened field, whose energy density is smaller by $1/\varepsilon_r^2$. Taking the medium
around the ion from $\varepsilon_1$ to $\varepsilon_2$,

$$d\Delta G = -\frac{q^2}{8\pi\varepsilon_0 a}\,\frac{d\varepsilon_r}{\varepsilon_r^2}
\quad\Rightarrow\quad
\Delta G_{\rm Born} = -\frac{q^2}{8\pi\varepsilon_0 a}\int_{\varepsilon_1}^{\varepsilon_2}\frac{d\varepsilon_r}{\varepsilon_r^2}
= \frac{q^2}{8\pi\varepsilon_0 a}\left(\frac1{\varepsilon_2}-\frac1{\varepsilon_1}\right).$$

This is the Born energy: the free energy of moving an ion from a medium with dielectric
constant $\varepsilon_1$ into one with $\varepsilon_2$ (Dill Eq. 22.61). The solvation free
energy is the special case $\varepsilon_1 = 1$, from vacuum:
$-\frac{q^2}{8\pi\varepsilon_0 a}(1 - 1/\varepsilon_r)$.

**Check against the charging picture.** Charging the sphere in vacuum costs
$q^2/(8\pi\varepsilon_0 a)$; charging it in the solvent costs $q^2/(8\pi\varepsilon_0\varepsilon_r a)$.
The difference is exactly the Born energy from vacuum into the solvent. Dill derives it this way, with a thermodynamic cycle
(Fig. 22.14, Eq. 22.61).

**Numbers.** In units of $k_BT$, $\Delta G_{\rm Born}/k_BT = (z^2\ell_B^{\rm vacuum}/2a)(1/\varepsilon_2 - 1/\varepsilon_1)$.
From vacuum this is $-(z^2\ell_B^{\rm vacuum}/2a)(1 - 1/\varepsilon_r)$.
For a monovalent ion with $a = 2$ Å in water this is $-140 \times 0.99 = -138\,k_BT$, about
−340 kJ/mol. In oil ($\varepsilon_r = 2$) it is only $-70\,k_BT$.

**Assumptions to keep in mind.** The solvent is a uniform continuum right up to the ion's
surface; it responds linearly to the field (no saturation, although the field next to a small
ion is enormous); and only electrostatics counts. The radius $a$ therefore works as an
effective, fitted cavity radius rather than the crystal radius.

## Self-test

1. Which changes the Born energy more, doubling $z$ or doubling $a$?
   *Answer: doubling $z$ (×4); doubling $a$ only halves it.*
2. What is the solvation free energy (Born from vacuum) for $\varepsilon_r \to 1$ and for $\varepsilon_r \to \infty$?
   *Answer: 0, and $-z^2\ell_B^{\rm vacuum}/2a$ (the whole self-energy).*
3. Why does the dilute formula $-(q^2/8\pi\varepsilon_0 a)\chi$ fail for water?
   *Answer: it assumes every molecule feels the bare field; in a dense liquid the field is
   already screened to $E/\varepsilon_r$.*
"""


def convergence():
    dip_mu, dip_a = 1.85 / 4.803, 1.4  # eÅ, Å: water-like
    onsager = dip_mu**2 * LB0 / dip_a**3 * (EPS_W - 1) / (2 * EPS_W + 1)
    script = (
        CONVERGENCE.replace("RA_MAX_", f"{RA_MAX:.1f}")
        .replace("CX_", f"{CX:.1f}")
        .replace("R0_", f"{R0:.1f}")
        .replace("SPAN_", f"{SPAN:.1f}")
        .replace("BORN_ION_", f"{LB0 / 4 * (1 - 1 / EPS_W):.3f}")
        .replace("ONSAGER_", f"{onsager:.3f}")
    )
    lo, hi = hx_of(9.0), hx_of(11.0)
    return {
        "id": "convergence",
        "state": {"hx": hx_of(2.0), "hy": 250.0, "dip": 0.0, "cont": 0.0},
        "elements": [
            title("convergence", "5. Ion solvation reaches far into the solvent"),
            scene(
                "convergence-scene",
                80,
                100,
                1100,
                504,
                [1200, 550],
                script,
                handles=[
                    {
                        "x": "hx",
                        "y": "hy",
                        "r": 22,
                        "within": frame(CX + R0, 249, SPAN, 2),
                    }
                ],
            ),
            {
                "id": "dip",
                "kind": "checkbox",
                "frame": frame(1280, 130, 260, 50),
                "config": {"bind": "dip", "label": "dipole at centre"},
            },
            {
                "id": "cont",
                "kind": "checkbox",
                "frame": frame(1280, 190, 260, 50),
                "config": {"bind": "cont", "label": "continuum"},
            },
            text(
                "convergence-model",
                1280,
                260,
                260,
                340,
                "Field energy per volume:\n\nion $\\propto r^{-4}$,\n\ndipole $\\propto r^{-6}$.",
                scale=0.6,
            ),
            text(
                "convergence-q",
                80,
                615,
                1440,
                110,
                "**Predict, then drag:** how far out must the solvent reach before the **ion** has 90 % of "
                "its Born energy: $2a$, $10a$ or $100a$? Drag the shell to find out.",
                scale=0.8,
            ),
            puzzle(
                "convergence-p",
                80,
                730,
                700,
                70,
                mode="condition",
                tries=2,
                check=f"hx >= {lo:.2f} && hx <= {hi:.2f}",
                hints=["The blue dot in the top panel is the ion's fraction, $1 - a/R$. Set it to 0.9."],
                feedback={
                    "correct": "Yes: $R = 10a$, about 20 Å, or seven layers of water.",
                    "reveal": "$1 - a/R = 0.9$ gives $R = 10a$.",
                },
            ),
            text(
                "convergence-why",
                820,
                730,
                700,
                250,
                "**Notice:** the dipole has 99.9 % by then. Ion solvation is long-ranged, so computer "
                "simulations of ions need large boxes of water, or a Born correction for the water left out.",
                scale=0.7,
            ),
        ],
        "builds": reveal_after(("convergence-why", "convergence-p")),
    }


def takehome_solvation():
    return take_home(
        "takehome-solvation",
        "Take-home: solvation of an ion",
        "**Take-home.**\n\n"
        "- An ion in vacuum carries a large self-energy, $z^2\\ell_B^{\\rm vacuum}/2a$: 140 $k_BT$ for $a = 2$ Å.\n"
        "- A solvent wins back the fraction $1 - 1/\\varepsilon_r$ of it, because its molecules polarize "
        "in the ion's field.\n"
        "- The Born energy, $(z^2\\ell_B^{\\rm vacuum}/2a)(1/\\varepsilon_2 - 1/\\varepsilon_1)$, is the cost of moving "
        "the ion between any two media; from vacuum it is the solvation free energy.\n"
        "- Water ($\\varepsilon_r = 78$) wins back 99 %; oil ($\\varepsilon_r = 2$) only 50 %.\n"
        "- The solvent far away still counts: 10 % of the ion's solvation comes from beyond $10a$.",
    )


def cycle():
    return {
        "id": "cycle",
        "elements": [
            title("cycle", "6. A transfer is the difference of two solvation energies"),
            scene("cycle-scene", 80, 100, 1440, 514, [1400, 500], CYCLE),
            text(
                "cycle-body",
                80,
                625,
                1440,
                100,
                "Free energy depends only on the start and end states, so the direct path (dashed) costs the "
                "same as the detour: discharge in 1, move the neutral sphere for free, charge up in 2.",
                scale=0.8,
            ),
            *box(
                "cycle-key",
                80,
                725,
                1440,
                268,
                "**Key concept** (Dill Eq. 22.61); only electrostatics, no cavity or van der Waals terms:\n\n"
                "$$\\Delta G_{\\rm transfer} = \\Delta G_{\\rm solv}(2) - \\Delta G_{\\rm solv}(1) "
                "= \\frac{z^2\\ell_B^{\\rm vacuum}}{2a}\\left(\\frac1{\\varepsilon_2}-\\frac1{\\varepsilon_1}\\right)k_BT$$",
                scale=0.75,
            ),
        ],
    }


def explorer():
    solvents = [("water", 78.4), ("octanol", 10.0), ("oil", 2.0), ("vacuum", 1.0)]

    def row(key, label, y):
        els = [
            text(
                f"ex-{key}-l",
                80,
                y - 6,
                300,
                50,
                f"{label}: $\\varepsilon_r$ = {{{{{key}:.1}}}}",
                scale=0.7,
            ),
            slider(f"ex-{key}", 380, y, 500, key, 1, 100, log=True),
        ]
        els += [
            button(
                f"ex-{key}-{name}", 920 + 152 * i, y - 4, 144, name, f"{key} = {eps}"
            )
            for i, (name, eps) in enumerate(solvents)
        ]
        return els

    return {
        "id": "explorer",
        "state": {"epsA": 78.4, "epsB": 2.0, "val": 1.0, "a": 2.0},
        "elements": [
            title("explorer", "Born explorer: two solvents on one curve"),
            scene("explorer-scene", 80, 100, 1440, 576, [1400, 560], EXPLORER),
            *row("epsA", "solvent A", 702),
            *row("epsB", "solvent B", 772),
            text("ex-z-l", 80, 836, 300, 50, "ion charge z", scale=0.7),
            *[
                button(f"ex-z{i}", 380 + 125 * i, 838, 115, lab, f"val = {v}")
                for i, (lab, v) in enumerate(
                    [("+1", 1.0), ("−1", -1.0), ("+2", 2.0), ("−2", -2.0)]
                )
            ],
            text("ex-a-l", 920, 836, 300, 50, "radius $a$ = {{a:.1}} Å", scale=0.7),
            slider("ex-a", 1220, 842, 300, "a", 1, 4),
            text(
                "ex-hint",
                80,
                900,
                1440,
                90,
                "**Predict:** water → octanol costs less than water → oil. How much less? **Notice:** the "
                "transfer is the vertical gap between two points on one curve, and above $\\varepsilon_r \\approx 20$ "
                "the curve is almost flat.",
                scale=0.65,
            ),
        ],
    }


def oil_water():
    oil = LB0 / 4 * (1 / 2 - 1 / EPS_W)
    return {
        "id": "oil-water",
        "elements": [
            title("oil-water", "7. How much does an ion dislike oil? (Dill Ex. 22.13)"),
            text(
                "ow-q",
                80,
                110,
                1440,
                110,
                "**Question:** A monovalent ion with $a = 2$ Å moves from water ($\\varepsilon_r = 78$) into "
                "oil ($\\varepsilon_r = 2$). What is $\\Delta G/k_BT$?",
                scale=0.85,
            ),
            puzzle(
                "ow-p",
                80,
                230,
                700,
                70,
                mode="numeric",
                answer=round(oil, 1),
                tolerance=4,
                tries=3,
                hints=[
                    "Use the transfer formula: the difference of two Born energies.",
                    (
                        "$\\Delta G/k_BT = \\dfrac{\\ell_B^{\\rm vacuum}}{2a}\\left(\\dfrac1{\\varepsilon_{\\rm oil}}-\\dfrac1{\\varepsilon_{\\rm w}}\\right)$, "
                        "with $\\ell_B^{\\rm vacuum} = 560$ Å."
                    ),
                    "$140 \\times (0.5 - 0.013)$.",
                ],
                feedback={
                    "correct": "Right: about 70 $k_BT$, or 170 kJ/mol.",
                    "reveal": f"$140 \\times 0.49 \\approx {oil:.0f}\\,k_BT$, about 170 kJ/mol.",
                },
            ),
            text(
                "ow-why",
                80,
                420,
                1440,
                260,
                "What does 70 $k_BT$ mean? The partition coefficient is $K = e^{-\\Delta G/k_BT} \\approx e^{-70} "
                "\\approx 10^{-30}$. Shake a litre of oil with a litre of 1 M salt water: on average, not one ion "
                "ends up in the oil.",
                scale=0.85,
            ),
            *box(
                "ow-take",
                80,
                700,
                1440,
                200,
                "**Take-home.** Bare ions do not enter oil. That is why ions stay out of lipid bilayers and "
                "protein cores, and why charged side chains sit at a protein's surface or pair up in salt bridges.",
                take=True,
            ),
        ],
        "builds": reveal_after(
            ("ow-why", "ow-p"), ("ow-take-card", "ow-p"), ("ow-take", "ow-p")
        ),
    }


def several_charges():
    # Worked example: a ±1 pair at contact 5 Å, radii 2.5 Å, water → octanol.
    a, r, e1, e2 = 2.5, 5.0, 78.4, 10.0
    vac = (
        2 * LB0 / (2 * a) - LB0 / r
    )  # self-energies minus pair attraction, vacuum, k_BT
    tr = vac * (1 / e2 - 1 / e1)
    return {
        "id": "several-charges",
        "elements": [
            title(
                "several-charges",
                "Several charges: self-energies plus pair energies, all divided by εᵣ",
            ),
            text(
                "sc-body",
                80,
                115,
                1440,
                440,
                "A molecule with several charges costs the charging energy of each charge, plus the Coulomb "
                "energy of every pair (Dill Eqs. 22.47–22.50). In units of $k_BT$, in a medium $\\varepsilon_r$:\n\n"
                "$$\\frac{\\Delta G}{k_BT} = \\frac{\\ell_B^{\\rm vacuum}}{\\varepsilon_r}\\left[\\sum_i \\frac{z_i^2}{2a_i} "
                "+ \\sum_{i<j} \\frac{z_iz_j}{r_{ij}}\\right]$$\n\n"
                "The prefactor is the Bjerrum length in the medium; the bracket depends only on the geometry. "
                "So a transfer changes only the prefactor, whatever the arrangement of charges.",
                scale=0.8,
            ),
            *box(
                "sc-example",
                80,
                570,
                1440,
                270,
                "**Worked example.** An ion pair, $+1$ and $-1$, radii 2.5 Å, in contact at 5 Å. In vacuum the "
                f"bracket is $2/(2 \\cdot 2.5) - 1/5 = 0.2$ Å⁻¹, so the energy is $560 \\times 0.2 = {vac:.0f}\\,k_BT$. "
                "From water to octanol the pair costs about "
                f"{tr:.0f} $k_BT$, from ${vac:.0f}\\,(1/10 - 1/78)$. Two separate ions would cost twice as much, "
                "about 20 $k_BT$: the partner cancels part of the field.",
                scale=0.78,
            ),
            text(
                "sc-q",
                80,
                870,
                1440,
                100,
                "**Question:** Does it help an ion to enter oil with a partner? What sets how much it helps?",
                scale=0.75,
            ),
        ],
    }


def born_test():
    return {
        "id": "born-test",
        "elements": [
            title(
                "born-test",
                "8. Born gets hydration enthalpies right, with cavity radii",
            ),
            scene("born-test-scene", 80, 110, 760, 500, [700, 460], TEST),
            text(
                "born-test-body",
                880,
                110,
                640,
                560,
                "Experiments measure hydration **enthalpies**; Born gives $\\Delta H$ from how $\\varepsilon_r$ "
                "changes with temperature (Dill Eq. 22.65).\n\n"
                "With **cavity** radii, slightly larger than crystal radii (Na⁺ 1.68 Å, Cl⁻ 1.94 Å), "
                "Born gives −774 kJ/mol for NaCl. Experiment: −769 (Dill Ex. 22.14).",
                scale=0.75,
            ),
            *box(
                "born-test-key",
                80,
                680,
                1440,
                160,
                "**Key concept.** Born predicts $\\Delta H \\propto -1/a$, and the alkali and halide ions follow "
                "that line (Dill Fig. 22.17), once $a$ is the radius of the hole the ion makes in water.",
                scale=0.75,
            ),
            text(
                "born-test-q",
                80,
                860,
                1440,
                100,
                "**Question:** Which ion is hydrated more strongly, Li⁺ or Cs⁺? Why?",
                scale=0.8,
            ),
        ],
    }


def caveats():
    return {
        "id": "caveats",
        "elements": [
            title("caveats", "What the Born model leaves out"),
            text(
                "caveats-body",
                80,
                110,
                1440,
                600,
                "- The solvent is a **uniform** continuum right up to the ion: no hydrogen bonds, no "
                "first-shell structure, and no saturation in the very strong field next to a small ion.\n"
                "- $a$ is an **effective** radius, in practice fitted. A 10 % error in $a$ gives a 10 % error in "
                "$\\Delta G$, about 40 kJ/mol.\n"
                "- Only electrostatics: the cost of opening a cavity, and dispersion, are left out.\n"
                "- Single ions cannot be measured alone, only neutral salts, so single-ion values rest on a convention.",
                scale=0.85,
                spacing={"between": 0.35},
            ),
            *box(
                "caveats-take",
                80,
                740,
                1440,
                160,
                "**Take-home.** Born is a model for *trends*: $z^2$, $1/a$ and $1/\\varepsilon_r$. "
                "Trust its ratios more than its absolute numbers.",
                take=True,
            ),
        ],
        "builds": [{"element": "caveats-body", "delivery": "by-paragraph"}],
    }


def interface():
    st = {
        "ix": 0.0,
        "iy": 130.0,
        "eps2": 1.0,
        "a": 2.0,
        "val": 1.0,
        "smooth": 0.0,
        "w": 3.0,
        "zoom": 0.0,
    }
    # Plot spans x 110..1150 for −20..20 Å; start the ion 10 Å into the water.
    x0, xs = 110.0, 1040.0 / 40
    st["ix"] = x0 + xs * 10.0
    cx, w = 1220, 300
    return {
        "id": "interface",
        "state": st,
        "elements": [
            title("interface", "9. Pulling an ion out of water costs the Born energy"),
            scene(
                "interface-scene",
                80,
                100,
                1120,
                560,
                [1200, 600],
                INTERFACE,
                handles=[
                    {"x": "ix", "y": "iy", "r": 30, "within": frame(x0, 129, 1040, 2)}
                ],
            ),
            text("if-l1", cx, 110, w, 40, "upper phase", scale=0.6, colour="faint"),
            button("if-air", cx, 150, 80, "air", "eps2 = 1.0"),
            button("if-oil", cx + 86, 150, 80, "oil", "eps2 = 2.0"),
            button("if-oct", cx + 172, 150, 128, "octanol", "eps2 = 10.0"),
            text("if-l2", cx, 215, w, 40, "ion charge z", scale=0.6, colour="faint"),
            *[
                button(f"if-z{z}", cx + 102 * i, 255, 95, f"z = {z}", f"val = {z}.0")
                for i, z in enumerate((1, 2, 3))
            ],
            text("if-l3", cx, 320, w, 40, "radius $a$ = {{a:.1}} Å", scale=0.6),
            slider("if-a", cx, 360, w, "a", 1, 4),
            {
                "id": "if-smooth",
                "kind": "checkbox",
                "frame": frame(cx, 420, w, 46),
                "config": {"bind": "smooth", "label": "smooth interface"},
            },
            text("if-l4", cx, 470, w, 40, "width = {{w:.1}} Å", scale=0.6),
            slider("if-w", cx, 510, w, "w", 1, 10),
            button("if-full", cx, 580, 145, "full scale", "zoom = 0.0"),
            button("if-zoom", cx + 155, 580, 145, "zoom in", "zoom = 1.0"),
            text(
                "if-q",
                80,
                670,
                1440,
                135,
                "**Question:** Drag the ion out. Where along the path does the cost rise most? Zoom in on the water "
                "side: why is the ion pushed *away* from the surface? With oil and $a = 2$ Å, how many "
                "times more does $z = 2$ cost than $z = 1$?",
                scale=0.75,
            ),
            *box(
                "if-ans",
                80,
                810,
                1440,
                178,
                "**Answer.** The cost rises over about one ion radius around the surface. In water the ion is "
                "repelled by its image in the air, whatever its sign: the energy goes as $z^2$. So $z = 2$ costs "
                "four times as much as $z = 1$.",
                scale=0.72,
            ),
        ],
        "builds": [
            {"element": "if-ans-card", "effect": "dissolve"},
            {"element": "if-ans", "trigger": "with-previous", "effect": "dissolve"},
        ],
    }


def real_interface():
    return {
        "id": "real-interface",
        "elements": [
            title("real-interface", "Small ions avoid the water surface"),
            text(
                "ri-body",
                80,
                110,
                1440,
                560,
                "- The water surface is not a step: the density falls over a few ångström (the smooth curve).\n"
                "- Near the surface an ion loses part of its solvation; in the image-charge picture it is "
                "repelled by its own mirror image in the air (Onsager–Samaras).\n"
                "- So the top layer of salt water holds fewer ions, and salt water has a slightly *higher* "
                "surface tension than pure water.\n"
                "- Large, polarizable anions (I⁻, SCN⁻) are the exception: they come up to the surface.",
                scale=0.85,
                spacing={"between": 0.35},
            ),
            text(
                "ri-q",
                80,
                720,
                1440,
                110,
                "**Question:** What would make a large anion less unhappy at the surface? Think of $a$ in the "
                "Born energy, and of polarizability from day 3.",
                scale=0.8,
            ),
        ],
        "builds": [{"element": "ri-body", "delivery": "by-paragraph"}],
    }


def takehome_transfer():
    return take_home(
        "takehome-transfer",
        "Take-home: moving ions between media",
        "**Take-home.**\n\n"
        "- A transfer free energy is the difference of two solvation energies (a thermodynamic cycle).\n"
        "- Water → oil costs about 70 $k_BT$ for a small ion: $K \\approx 10^{-30}$, so bare ions stay out "
        "of oil, membranes and protein cores.\n"
        "- Wet octanol ($\\varepsilon_r \\approx 10$) explains why ionizing a drug lowers $\\log P$ by 3–4 units.\n"
        "- Ions are pushed away from a water surface; the cost rises over a few ångström.",
    )


NOTES_TRANSFER = r"""
# Transfer between media, partition and drugs

**The cycle.** A single ion cannot be moved from water to oil in a calorimeter, but its
free energy change can be computed by a detour. Discharge the ion in water (gaining back
$q^2/8\pi\varepsilon_0\varepsilon_{\rm w} a$), move the neutral sphere into oil (no electrostatic cost,
since there is no field to screen), and charge it again in oil (paying
$q^2/8\pi\varepsilon_0\varepsilon_{\rm oil} a$). Free energy is a state function, so the direct path
costs the same as the detour (Dill Fig. 22.14, Eq. 22.61):

$$\Delta G_{w\to o} = \frac{z^2\ell_B^{\rm vacuum}}{2a}\left(\frac1{\varepsilon_{\rm oil}}-\frac1{\varepsilon_{\rm w}}\right)k_BT
= \Delta G_{\rm solv}(o) - \Delta G_{\rm solv}(w).$$

**Partition coefficient.** At equilibrium the concentrations in the two phases satisfy
$c_o/c_w = K = e^{-\Delta G_{w\to o}/k_BT}$. For a monovalent ion with $a = 2$ Å, from water
($\varepsilon_r = 78$) to oil ($\varepsilon_r = 2$), $\Delta G = 140\times(0.5 - 0.013) \approx 68\,k_BT$
(Dill Ex. 22.13 takes $\varepsilon_r = 80$ for water and rounds to 70), so $K \approx 10^{-30}$. A litre of 1 M salt water holds
$6\times10^{23}$ ions; next to a litre of oil, on average fewer than one of them is in the oil.

**logP.** Chemists report $\log P = \log_{10}(c_{\rm octanol}/c_{\rm water})$. Natural logarithms
turn into decimal ones by dividing by $\ln 10 = 2.303$:
$\log P = -\Delta G_{w\to o}/(2.303\,k_BT)$. Ionizing a drug adds the Born transfer cost to the
neutral molecule's $\Delta G$. With dry oil the estimate (about 30 log units) is far too large.
Octanol, however, holds a lot of water and has $\varepsilon_r \approx 10$, and a drug's charge is spread
over a group with an effective radius of about 3 Å. Then
$\Delta G \approx (560/6)(1/10 - 1/78) \approx 8\,k_BT$, a drop of $8/2.3 \approx 3.5$ in $\log P$, close to
the 3–4 units usually measured between the neutral and ionized forms of a drug.

**pH.** Only the neutral form crosses a membrane easily. An acid is neutral where the pH is
below its $\mathrm{p}K_a$, a base where the pH is above it. This is why the pH along the gut, from
about 1.5 in the stomach to 7–8 in the small intestine, matters for which drugs are absorbed where.

**Near the surface.** An ion close to the water–air surface loses part of its solvation
shell. For a sharp surface this can be described with an image charge: in water the ion feels
a repulsion from its mirror image of about $(\ell_B/4d)(\varepsilon_{\rm w} - \varepsilon_{\rm air})/(\varepsilon_{\rm w} + \varepsilon_{\rm air})\,k_BT$
at distance $d$ (about $1\,k_BT$ at contact for a monovalent ion). The surface layer is therefore
depleted of small ions, which raises the surface tension of salt solutions (Onsager and
Samaras, 1934). Large polarizable anions are an exception, as simulations and surface-sensitive
spectroscopy have shown.

**Source.** Dill & Bromberg, *Molecular Driving Forces*, 2nd ed., ch. 22, pp. 444–451.

## Self-test

1. Is the transfer of an ion from oil into water positive or negative?
   *Answer: negative; $1/\varepsilon_r$ is 0.013 in water and 0.5 in oil.*
2. Water → octanol costs $+8.1\,k_BT$ for $a = 3$ Å. What does octanol → water cost?
   *Answer: $-8.1\,k_BT$; the same two states, opposite direction.*
3. Where is a weak base with $\mathrm{p}K_a = 9$ absorbed best, stomach or small intestine?
   *Answer: the small intestine, where more of it is neutral.*
4. Why are small ions depleted at the water surface?
   *Answer: they lose part of their solvation there; their image charge repels them.*
"""


def sphere():
    return {
        "id": "sphere",
        "elements": [
            title(
                "sphere",
                "11. A charged protein shifts the pKa of groups on its surface",
            ),
            text(
                "sphere-body",
                80,
                100,
                1440,
                560,
                "A protein with net charge $ze$ acts, from outside, like a charged sphere. Its potential at "
                "distance $r$ from the centre is $e\\psi/k_BT = z\\ell_B/r$ (Dill Eq. 21.43), with "
                "$\\ell_B = 7.1$ Å in water.\n\n"
                "A proton near the surface feels that potential. Near a positive protein protons are pushed "
                "away: $[{\\rm H}^+]_{\\rm surface} = [{\\rm H}^+]_{\\rm bulk}\\,e^{-e\\psi/k_BT}$. A surface group "
                "therefore sees a different pH from the one in the bulk.",
                scale=0.8,
            ),
            *box(
                "sphere-key",
                80,
                660,
                1440,
                210,
                "**Key concept.** A surface potential $\\psi$ shifts the apparent "
                "$\\mathrm{p}K_a^{\\rm app} = \\mathrm{p}K_a - \\dfrac{e\\psi}{2.303\\,k_BT}$. "
                "**Question:** near a positive surface, is an acid more or less dissociated? (Dill 22.2, 22.4)",
            ),
        ],
        "builds": [{"element": "sphere-body", "delivery": "by-paragraph"}],
    }


def screening():
    return {
        "id": "screening",
        "elements": [
            title("screening", "12. Teaser for day 5: salt screens a charge"),
            text(
                "screening-body",
                80,
                100,
                1440,
                520,
                "Put an ion into salt water. Ions of the opposite sign gather round it, ions of the same sign "
                "keep away. This *ion atmosphere* carries the opposite charge and cancels the ion's field "
                "beyond a distance called the **Debye length**, $\\kappa^{-1}$.\n\n"
                "- The potential of an ion of radius $a$ becomes "
                "$\\dfrac{e\\psi(r)}{k_BT} = z\\,\\ell_B\\,\\dfrac{e^{-\\kappa(r-a)}}{(1+\\kappa a)\\,r}$: "
                "Coulomb's law times an exponential cut-off.\n"
                "- Two ions: $w(R)/k_BT = z_{1,\\rm eff}\\,z_{2,\\rm eff}\\,\\ell_B\\,e^{-\\kappa R}/R$ with "
                "$z_{\\rm eff} = z\\,e^{\\kappa a}/(1+\\kappa a)$ (problem 2 writes it with charges, $Q_{\\rm eff}$).\n"
                "- Blood (150 mM): $\\kappa^{-1} \\approx 8$ Å. Pure water ($10^{-7}$ M): about 1 µm. "
                "Without salt, $\\kappa \\to 0$ and Coulomb's law returns.",
                scale=0.78,
                spacing={"between": 0.3},
            ),
            *box(
                "screening-key",
                80,
                640,
                1440,
                305,
                "**Key concept: the Debye length.**\n\n"
                "$$\\kappa^2 = 8\\pi\\,\\ell_B\\,N_A I \\qquad \\kappa^{-1} = \\frac{3.04\\ \\text{Å}}{\\sqrt{I/\\text{M}}}"
                "\\quad\\text{(water, 25 °C)}$$",
            ),
        ],
        "builds": [{"element": "screening-body", "delivery": "by-paragraph"}],
    }


NOTES_SCREENING = r"""
# Salt screening, a first look

**Picture.** In salt water every ion is surrounded by a cloud of other ions. Ions of the
opposite sign are drawn in and ions of the same sign are pushed away, so the cloud carries a
net charge equal and opposite to the central ion. Far away, the ion and its cloud together look
neutral: the field has been *screened*.

**How far the cloud reaches.** The balance between electrostatic attraction (which pulls the
cloud in) and entropy (which spreads it out) sets the size of the cloud, the Debye length
$\kappa^{-1}$. For a solution of ionic strength $I$ (mol/L),

$$\kappa^2 = 8\pi\,\ell_B\,N_A I \cdot (1000\ \text{L/m}^3),$$

and in water at 25 °C this gives $\kappa^{-1} = 3.04\ \text{Å}/\sqrt{I/\text{M}}$. At 0.1 M the
Debye length is about 10 Å; at 150 mM, the salt level of blood, 8 Å. A lower dielectric
constant gives a longer Bjerrum length and hence a *shorter* Debye length at the same salt,
$\kappa^{-1} \propto \sqrt{\varepsilon_r}$.

**The screened potential.** Solving the linearized Poisson–Boltzmann (Debye–Hückel) equation
around an ion of radius $a$, from which other ions are excluded, gives

$$\frac{e\psi(r)}{k_BT} = z\,\ell_B\,\frac{e^{-\kappa(r-a)}}{(1+\kappa a)\,r}.$$

Close to the ion this is Coulomb's law; beyond a few Debye lengths it dies away exponentially.
For two ions or two charged particles this gives the screened Coulomb interaction used in
problem 2, with the effective valence $z_{\rm eff} = z\,e^{\kappa a}/(1+\kappa a)$:
$w(R)/k_BT = z_{1,\rm eff}\,z_{2,\rm eff}\,\ell_B\,e^{-\kappa R}/R$. Problem 2 writes the same with
charges, $Q_{\rm eff} = Q\,e^{\kappa a}/(1+\kappa a)$.

**Assumptions.** The linearized theory holds when $e\psi \ll k_BT$, so it works best for low
charge, high dielectric constant and moderate salt. That is why the explorable keeps
$\varepsilon_r$ between 20 and 80 (water is 78): in oil-like solvents the ion clouds are strongly nonlinear and
ions pair up instead (day 2).

**Day 5** derives the Debye length, the ion atmosphere and what it does to activity
coefficients (Dill ch. 23).

## Self-test

1. What is the Debye length in 0.01 M and in 1 M NaCl at 25 °C?
   *Answer: 30 Å and 3 Å.*
2. Adding 0.1 M salt, does the attraction between Na⁺ and Cl⁻ 10 Å apart get weaker or stronger?
   *Answer: weaker; the ion atmospheres cancel part of each field.*
3. At the same salt concentration, is the Debye length longer or shorter in ethanol than in water?
   *Answer: shorter, since $\kappa^{-1} \propto \sqrt{\varepsilon_r}$.*
"""


def screen_pair():
    st = {
        "x1": 400.0,
        "y1": 250.0,
        "q1": 1.0,
        "x2": 600.0,
        "y2": 250.0,
        "q2": -1.0,
        "salt": 0.01,
        "eps": 30.0,
    }
    area = frame(20, 20, 960, 460)
    lb = "(560.4 / eps)"
    kap = f"(8.0 * 3.14159265 * {lb} * salt * 0.0006022).sqrt()"
    w20 = f"{lb} * (-{kap} * 16.0).exp() / ((1.0 + 2.0 * {kap}) * (1.0 + 2.0 * {kap}) * 20.0)"
    return {
        "id": "screen-pair",
        "state": st,
        "elements": [
            title(
                "screen-pair", "13. Salt switches off the interaction between two ions"
            ),
            text(
                "sp-l1",
                80,
                105,
                300,
                50,
                "salt $I$ = {{salt * 1000.0:.0}} mM",
                scale=0.7,
            ),
            slider("sp-salt", 380, 110, 380, "salt", 0.001, 1.0, log=True),
            text(
                "sp-l2",
                820,
                105,
                320,
                50,
                "$\\varepsilon_r$ = {{eps:.0}}, $\\ell_B$ = {{560.4 / eps:.1}} Å",
                scale=0.7,
            ),
            slider("sp-eps", 1140, 110, 380, "eps", 20, 80),
            scene(
                "sp-map",
                80,
                170,
                900,
                450,
                [1000, 500],
                SCREEN_MAP,
                handles=[
                    {"x": "x1", "y": "y1", "r": 22, "tap": "q1 = -q1", "within": area},
                    {"x": "x2", "y": "y2", "r": 22, "tap": "q2 = -q2", "within": area},
                ],
            ),
            scene("sp-plot", 1000, 170, 520, 450, [580, 500], SCREEN_PLOT),
            text(
                "sp-q",
                80,
                626,
                1440,
                100,
                "**Predict, then slide:** keep $\\varepsilon_r = 30$ and the ions 20 Å apart. How much salt "
                "brings their interaction below $0.1\\,k_BT$? Watch the dashed rings shrink.",
                scale=0.8,
            ),
            puzzle(
                "sp-p",
                80,
                727,
                700,
                70,
                mode="condition",
                tries=2,
                check=f"(eps - 30.0).abs() <= 1.0 && {w20} < 0.1",
                hints=["Raise $I$ until $\\kappa^{-1}$ is well below 20 Å; watch the readout under the plot."],
                feedback={
                    "correct": "Yes: about 50 mM, a third of the salt in your blood.",
                    "reveal": "$I \\gtrsim 50$ mM, where $\\kappa^{-1} \\approx 8$ Å.",
                },
            ),
            text(
                "sp-why",
                820,
                750,
                700,
                220,
                "**Notice:** once the Debye length is shorter than the distance between the ions, they "
                "hardly feel each other. Salt makes charged molecules behave as if they were neutral.",
                scale=0.7,
            ),
        ],
        "builds": reveal_after(("sp-why", "sp-p")),
    }


def summary():
    return {
        "id": "summary",
        "elements": [
            title("summary", "Summary"),
            *box(
                "summary-take",
                80,
                110,
                1440,
                600,
                "**Take-home.**\n\n"
                "- Charging a sphere costs $z^2\\ell_B/2a$; a solvent wins back the fraction $1 - 1/\\varepsilon_r$, "
                "shell by shell.\n"
                "- Born: moving an ion from $\\varepsilon_1$ to $\\varepsilon_2$ costs "
                "$(z^2\\ell_B^{\\rm vacuum}/2a)(1/\\varepsilon_2 - 1/\\varepsilon_1)\\,k_BT$.\n"
                "- Ion solvation is long-ranged ($1 - a/R$); dipole solvation is local ($1 - (a/R)^3$).\n"
                "- Transfer = difference of solvation energies: about 70 $k_BT$ from water into oil, about "
                "8 $k_BT$ into wet octanol.\n"
                "- Salt screens charges beyond the Debye length $\\kappa^{-1} = 3.04\\ \\text{Å}/\\sqrt{I/\\text{M}}$.",
                take=True,
                scale=0.85,
            ),
            text(
                "summary-now",
                80,
                720,
                1440,
                180,
                "**Now:** Dill 22.1, 22.2, 22.4, 22.12, 22.13 and problems 1–3.\n\n"
                "**Next time:** the ion atmosphere and activity coefficients.",
                scale=0.9,
            ),
        ],
    }


def outcomes():
    return {
        "id": "outcomes",
        "elements": [
            title("outcomes", "After today you can…"),
            text(
                "outcomes-body",
                80,
                110,
                1440,
                700,
                "1. explain why a solvent stabilizes an ion, from the polarization of its molecules, and derive "
                "the Born energy by charging a sphere;\n"
                "2. estimate solvation and transfer free energies from $z$, $a$ and $\\varepsilon_r$, and say why "
                "ions avoid oil, membranes and protein cores;\n"
                "3. explain why ion solvation is long-ranged compared with a dipole's, and why small ions avoid "
                "a water surface;\n"
                "4. predict how a charged surface shifts the $\\mathrm{p}K_a$ of nearby groups, and estimate the "
                "Debye length to judge when salt switches off an interaction.",
                scale=0.85,
                spacing={"between": 0.4},
            ),
        ],
    }


def solvation_quiz():
    return {
        "id": "solvation-quiz",
        "elements": [
            title("solvation-quiz", "A solvation free energy starts in vacuum"),
            text(
                "sq-q1",
                80,
                110,
                1440,
                110,
                "**Question:** The solvation free energy of Na⁺ in water is the free energy change for…",
                scale=0.85,
            ),
            puzzle(
                "sq-p1",
                80,
                225,
                1440,
                140,
                mode="choice",
                tries=3,
                options=[
                    {
                        "text": "moving Na⁺ from vacuum into water",
                        "correct": True,
                        "hint": "Yes.",
                    },
                    {
                        "text": "moving Na⁺ from oil into water",
                        "hint": "That is a *transfer* free energy: the difference of two solvation free energies.",
                    },
                    {
                        "text": "dissolving solid NaCl in water",
                        "hint": "That also breaks up the crystal (day 2's lattice energy). Solvation starts from one lone ion.",
                    },
                    {
                        "text": "making Na⁺ from a Na atom",
                        "hint": "That is ionization. Solvation starts from the ion, already made, in vacuum.",
                    },
                ],
                feedback={
                    "correct": "Vacuum → solvent: one ion, no crystal, no other solvent.",
                    "reveal": "Vacuum → solvent: one ion, no crystal, no other solvent.",
                },
            ),
            *box(
                "sq-why",
                80,
                540,
                1440,
                250,
                "**Key concept.** A **solvation** free energy takes one ion from vacuum into a solvent. It is "
                "negative and large: the solvent lowers the energy of the ion's field. A **transfer** free energy "
                "(solvent 1 → solvent 2) is the *difference* of two solvation free energies.",
            ),
        ],
        "builds": reveal_after(("sq-why-card", "sq-p1"), ("sq-why", "sq-p1")),
    }


def what_if():
    oct3 = LB0 / 6 * (1 / 10 - 1 / EPS_W)
    return {
        "id": "what-if",
        "elements": [
            title("what-if", "Predict, then check with the explorer"),
            text(
                "wi-q",
                80,
                110,
                1440,
                380,
                "- **Question:** Which changes $\\Delta G_{\\rm solv}$ more: doubling $z$ or doubling $a$?\n"
                f"- **Question:** Water → octanol costs ${oct3:+.1f}\\,k_BT$ for $a = 3$ Å. What does octanol → water cost?\n"
                "- **Question:** What is $\\Delta G_{\\rm solv}$ as $\\varepsilon_r \\to 1$? As $\\varepsilon_r \\to \\infty$?",
                scale=0.85,
                spacing={"between": 0.4},
            ),
            *box(
                "wi-ans",
                80,
                520,
                1440,
                360,
                "**Answers.**\n\n"
                "- Doubling $z$ multiplies the energy by 4; doubling $a$ only halves it. Charge wins.\n"
                f"- ${-oct3:.1f}\\,k_BT$: the same two states in the opposite direction.\n"
                "- 0 in vacuum (nothing to win back); $-z^2\\ell_B^{\\rm vacuum}/2a$, the whole self-energy, for a perfect "
                "conductor. Water ($\\varepsilon_r = 78$) already gets 99 %.",
                scale=0.8,
            ),
        ],
        "builds": [
            {"element": "wi-q", "delivery": "by-paragraph"},
            {"element": "wi-ans-card", "effect": "dissolve"},
            {"element": "wi-ans", "trigger": "with-previous", "effect": "dissolve"},
        ],
    }


def logp():
    ddg = LB0 / 6 * (1 / 10 - 1 / EPS_W)
    return {
        "id": "logp",
        "elements": [
            title("logp", "10. Ionizing a drug lowers its logP by 3–4 units"),
            text(
                "logp-body",
                80,
                110,
                1440,
                340,
                "Chemists measure how well a drug enters fat and membranes by its partition between octanol and "
                "water, $\\log P = \\log_{10}([{\\rm drug}]_{\\rm octanol}/[{\\rm drug}]_{\\rm water})$. Good oral drugs "
                "have $\\log P \\approx 1$–3. Since $\\ln P = -\\Delta G_{\\rm transfer}/k_BT$, the Born transfer cost of "
                "a charge shows up directly in $\\log P$.",
                scale=0.85,
            ),
            text(
                "logp-q",
                80,
                470,
                1440,
                110,
                "**Question:** Estimate the drop in $\\log P$ when a drug is ionized. Wet octanol has "
                "$\\varepsilon_r \\approx 10$; take $a = 3\\ \\text{Å}$.",
                scale=0.85,
            ),
            *box(
                "logp-ans",
                80,
                600,
                1440,
                280,
                f"**Answer.** $\\Delta G/k_BT = \\dfrac{{560}}{{2 \\cdot 3}}\\left(\\dfrac1{{10}}-\\dfrac1{{78}}\\right) "
                f"\\approx {ddg:.1f}$, and dividing by $\\ln 10 = 2.3$ gives a drop of "
                f"${ddg / math.log(10):.1f}$ in $\\log P$, close to the 3–4 units measured. Dry oil would give "
                "about 30: octanol holds water, and the charge is spread over a group.",
                scale=0.78,
            ),
        ],
        "builds": [
            {"element": "logp-ans-card", "effect": "dissolve"},
            {"element": "logp-ans", "trigger": "with-previous", "effect": "dissolve"},
        ],
    }


def logd():
    return {
        "id": "logd",
        "elements": [
            title("logd", "Only the neutral form of a drug crosses a membrane"),
            text(
                "logd-body",
                80,
                110,
                1440,
                360,
                "The charged form pays the Born price, so pH decides where a drug is absorbed. Aspirin, an acid "
                "with $\\mathrm{p}K_a = 3.5$, is mostly neutral in the stomach (pH 1–2) and is absorbed there; in "
                "blood (pH 7.4) it is 99.99 % ionized. Drugs are often sold as **salts** (e.g. hydrochlorides) "
                "because the charged form dissolves fast in water.",
                scale=0.85,
            ),
            text(
                "logd-q",
                80,
                490,
                1440,
                110,
                "**Question:** Where is a weak **base** with $\\mathrm{p}K_a = 9$ best absorbed: stomach or small "
                "intestine?",
                scale=0.85,
            ),
            *box(
                "logd-ans",
                80,
                620,
                1440,
                220,
                "**Answer.** In the small intestine (pH 7–8). At pH 1.5 the base is fully protonated and charged; "
                "closer to its $\\mathrm{p}K_a$ a larger fraction is neutral and can cross the membrane.",
                scale=0.8,
            ),
        ],
        "builds": [
            {"element": "logd-ans-card", "effect": "dissolve"},
            {"element": "logd-ans", "trigger": "with-previous", "effect": "dissolve"},
        ],
    }


def text_height(md, w, scale=1.0, between=0.0):
    """Rough rendered height: frames do not clip Markdown, so overflow must be caught here."""
    per_line = 74 * w / 1440 / scale  # characters per line, calibrated on the editor
    lines = 0.0
    for block in re.split(r"\n\s*\n|\n(?=- )", md.strip()):
        if block.startswith("$$"):
            lines += 3.0
            continue
        visible = re.sub(
            r"\{\{[^}]*\}\}", "0000", block
        )  # interpolations show a short number
        visible = re.sub(r"\\[a-zA-Z]+|[{}$*_^]", "", visible)
        lines += math.ceil(len(visible) / per_line) + 0.8 * len(
            re.findall(r"\\d?frac", block)
        )
        lines += between
    return lines * 52 * scale


def check_fit(slides):
    for s in slides:
        for e in s.get("elements", []):
            if e["kind"] != "text":
                continue
            f, c = e["frame"], e["config"]
            st = c.get("style", {})
            h = text_height(
                c["text"],
                f["w"],
                st.get("scale", 1.0),
                st.get("spacing", {}).get("between", 0.0),
            )
            if h > f["h"] * 1.05 or f["y"] + h > 1000:
                print(
                    f"warning: {s['id']}/{e['id']}: needs ~{h:.0f}, frame {f['h']} at y {f['y']}"
                )


def main():
    bundle = Path(sys.argv[1] if len(sys.argv) > 1 else "intermolecular/day4.blikfang")
    if bundle.exists():
        shutil.rmtree(bundle)
    (bundle / "media").mkdir(parents=True)
    slides = [
        # solvation and the Born energy
        title_slide(),
        outcomes(),
        opening(),
        solvation_quiz(),
        charging(),
        notes_slide("notes-charging", NOTES_CHARGING),
        charging_number(),
        molecular(),
        born(),
        notes_slide("notes-born", NOTES_BORN),
        convergence(),
        takehome_solvation(),
        # transfer between media
        cycle(),
        explorer(),
        what_if(),
        oil_water(),
        several_charges(),
        born_test(),
        caveats(),
        interface(),
        real_interface(),
        logp(),
        logd(),
        everyday(),
        takehome_transfer(),
        notes_slide("notes-transfer", NOTES_TRANSFER),
        # charged spheres and a first look at salt
        sphere(),
        screening(),
        screen_pair(),
        notes_slide("notes-screening", NOTES_SCREENING),
        summary(),
    ]
    ids = [e["id"] for s in slides for e in s.get("elements", [])] + [
        s["id"] for s in slides
    ]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, f"duplicate ids: {dup}"
    check_fit(slides)
    for name, md in NOTES.items():
        (bundle / "media" / name).write_text(md)
    deck = {"format": "desktop", "slides": slides}
    (bundle / "deck.json").write_text(
        json.dumps(deck, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"{len(slides)} slides -> {bundle}")


main()
