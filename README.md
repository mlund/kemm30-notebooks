# KEMM30 lecture slides

Lectures are Jupyter notebooks, shown as slides with [Quarto](https://quarto.org) (reveal.js).

## First time on a new machine

1. Install [uv](https://docs.astral.sh/uv/) and Quarto ≥ 1.10 (`brew install --cask quarto`).
   If `quarto` isn't found, open a new terminal; it lives in `/Applications/quarto/bin`.
2. `uv sync` — installs the pinned Python packages into `.venv`.

## Day to day

Prefix commands with `uv run` so Quarto executes notebooks with the project's Python.

```bash
uv run jupyter lab                                          # edit notebooks
uv run quarto preview intermolecular/day1_lecture.ipynb --to revealjs    # live slides; re-render on save
uv run quarto render intermolecular/day1_lecture.ipynb --to revealjs --execute   # build intermolecular/day1_lecture.html
uv run python tools/check_overflow.py intermolecular/day1_lecture.html          # list slides whose content is cut off
uv run ruff check --fix tools && uv run ruff format tools                     # lint the tools
```

Run the cells and save before previewing: `preview` shows the outputs stored in
the notebook, `render --execute` re-runs everything.

## Slide syntax (in markdown cells)

| Want | Write |
|---|---|
| New slide | cell starting with `## Title`, or a line `---` |
| Reveal on click | `::: {.fragment}` … `:::` |
| Hide a code cell | first line `#| include: false` |
| Smaller text on one slide | `## Title {.smaller}` |
| Let one slide scroll | `## Title {.scrollable}` |

Interactive diagrams are D3 scripts in `intermolecular/explorables/<name>.js`, shown by a
code cell `explorable("<name>")` (helper in the day 2 and 3 setup cells). They run in JupyterLab
after the cell is executed and in the rendered slides; D3 is loaded from a CDN, so both
need internet.

Deck options (title, chalkboard, code hidden, …) are in the YAML raw cell at
the top of the notebook. The slide-type dropdown in JupyterLab is ignored.

Slides are 1050×700 px; if `check_overflow.py` reports a slide, split it. Set plot sizes
with `figsize=` in the code: Quarto ignores per-cell `fig-height` for Jupyter, and a
slide with a single plot is stretched to fill the space unless its heading has
`{.nostretch}`.

## Files

- `intermolecular/dayN_lecture.ipynb` — lecture slides (edit these)
- `intermolecular/dayN_solutions.ipynb` — exercise solutions
- `intermolecular/explorables/` — JavaScript for interactive diagrams
- `tools/check_overflow.py` — slide-fit checker (Playwright + installed Chrome or Edge)
- `pyproject.toml`, `uv.lock`, `.python-version` — pinned environment;
  `uv lock --upgrade` to update

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/): reuse and adapt
freely with attribution; share adaptations under the same license. See `LICENSE`.
