# Cyberpunk profile generator

The interface is driven by a single `profile.json`. The generator creates the complete 880px-wide SVG composition:

- `header.svg` — 880×360
- `links.svg` — 880×120
- `links/*.svg` — 220×80 cards, four cards per row
- `stats.svg` — 880×560
- `stack.svg` — 880×360
- `footer.svg` — 880×80
- `README.generated.md` — inline HTML layout with no table

## Geometry guarantee

The link layout deliberately preserves the geometry of the reference interface:

`4 × 220px = 880px`

Only the first card receives the outer left rail and only the fourth card receives the outer right rail. Internal cards do not create column dividers. The generator validates these dimensions before it reports success.

## Bash

```bash
./scripts/generate-profile.sh examples/marie-curie/profile.json ./generated-profile --render
```

## PowerShell

```powershell
./scripts/generate-profile.ps1 -Profile ./examples/marie-curie/profile.json -Output ./generated-profile -Render
```

Both wrappers call the same deterministic Python generator, so the SVG geometry is identical on Linux/macOS and Windows.

## GitHub Actions

The workflow at `.github/workflows/generate-profile.yml` regenerates the Marie Curie example, runs the geometry tests, renders PNG previews with CairoSVG, and uploads the complete generated profile as a workflow artifact.

## Creating another profile

Copy `examples/marie-curie/profile.json`, change `profile`, `theme`, `links`, `stats`, `stack`, and `footer`, then run the generator. The accent can be any six-digit hexadecimal color. `accent_bright` is optional and controls the hot/glow version of the accent.
