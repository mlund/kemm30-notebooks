"""Flag reveal.js slides whose content is taller than the slide.

Opens rendered slides (Quarto or nbconvert HTML) in an installed Chrome or
Edge via Playwright, visits every slide and compares its content height to
the configured slide height.

Usage: python tools/check_overflow.py slides.html [--all]
Exit status is 1 if any slide overflows.
"""

import argparse
import re
import sys
from pathlib import Path

from playwright.sync_api import Error, sync_playwright

MEASURE = """
async (revealUrl) => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  // nbconvert loads reveal via require.js; Quarto exposes a global.
  const Reveal = await new Promise((r) =>
    window.require && revealUrl ? require([revealUrl], r) : r(window.Reveal));
  if (!Reveal.isReady()) await new Promise((r) => Reveal.on("ready", r));
  // Rendered math changes heights: MathJax 2 has a queue, MathJax 3 a promise.
  const mathDone = () => new Promise((r) => {
    const M = window.MathJax;
    if (M && M.Hub) M.Hub.Queue(r);
    else if (M && M.startup) M.startup.promise.then(r);
    else r();
  });
  await document.fonts.ready;
  await sleep(1000);
  const slides = [...document.querySelectorAll(".reveal .slides section")]
    .filter((s) => !s.querySelector("section"));  // skip stack wrappers
  const out = [];
  for (const s of slides) {
    const i = Reveal.getIndices(s);
    Reveal.slide(i.h, i.v);
    await mathDone();
    await sleep(300);
    const title = (s.querySelector("h1,h2,h3") || s).innerText || "";
    // Hidden fragments still take layout space: this is the fully revealed slide.
    out.push({ h: i.h + 1, v: i.v || 0, height: s.scrollHeight, title });
  }
  return { limit: Reveal.getConfig().height, slides: out };
}
"""


def measure(path: Path) -> dict:
    page_html = path.read_text()
    m = re.search(r'"(https://[^"]+/reveal\.js)"', page_html)
    with sync_playwright() as p:
        browser = None
        for channel in ("chrome", "msedge"):
            try:
                browser = p.chromium.launch(channel=channel)
                break
            except Error:
                continue
        if browser is None:
            sys.exit("needs Google Chrome or Microsoft Edge installed")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(path.as_uri(), wait_until="load")
        result = page.evaluate(MEASURE, m.group(1) if m else None)
        browser.close()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("html", type=Path, help="rendered slides")
    parser.add_argument("--all", action="store_true", help="list every slide")
    args = parser.parse_args()

    result = measure(args.html.resolve())
    limit, cut = result["limit"], 0
    for s in result["slides"]:
        over = s["height"] > limit
        cut += over
        if over or args.all:
            num = f"{s['h']}.{s['v'] + 1}" if s["v"] else str(s["h"])
            title = " ".join(s["title"].replace("¶", "").split())[:60]
            mark = "CUT " if over else "    "
            print(f"{mark}{num:>5}  {s['height']}/{limit}px  {title}")
    if not cut:
        print(f"all {len(result['slides'])} slides fit")
    sys.exit(1 if cut else 0)


if __name__ == "__main__":
    main()
