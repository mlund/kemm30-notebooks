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

Deck options (title, chalkboard, code hidden, …) are in the YAML raw cell at
the top of the notebook. The slide-type dropdown in JupyterLab is ignored.

Slides are 1050×700 px; if content is cut off, split the slide.

## Files

- `intermolecular/day1_lecture.ipynb` — the lecture (edit this)
- `pyproject.toml`, `uv.lock`, `.python-version` — pinned environment;
  `uv lock --upgrade` to update

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/): reuse and adapt
freely with attribution; share adaptations under the same license. See `LICENSE`.
