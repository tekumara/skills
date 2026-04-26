---
name: mermaid-export
description: Extract Mermaid diagrams from Markdown documents or raw Mermaid files and render them to PNG or SVG. Use when a task involves fenced ```mermaid blocks, Mermaid architecture diagrams in docs, or reliable image export where browser and Mermaid CLI configuration can be fragile.
---

# Mermaid Export

Render Mermaid diagrams from Markdown or `.mmd` files to PNG or SVG.

Use the bundled script instead of rebuilding the workflow manually. It handles Mermaid block extraction, picks a real browser binary, writes a temporary Puppeteer config, and calls Mermaid CLI with stable defaults.

## Quick Start

Render the first Mermaid block from a Markdown file to PNG:

```bash
scripts/render_mermaid.py path/to/doc.md path/to/output.png
```

Render the second Mermaid block:

```bash
scripts/render_mermaid.py path/to/doc.md path/to/output.png --diagram-index 2
```

Render all Mermaid blocks from a Markdown file into separate numbered PNGs:

```bash
scripts/render_mermaid.py path/to/doc.md path/to/output.png --all
```

This writes `output-1.png`, `output-2.png`, and so on.

If you want a custom naming pattern, include `{index}` in the output path:

```bash
scripts/render_mermaid.py path/to/doc.md path/to/output-{index}.png --all
```

Render a raw Mermaid file to SVG:

```bash
scripts/render_mermaid.py path/to/diagram.mmd path/to/output.svg
```

## Workflow

1. Prefer `scripts/render_mermaid.py` for export work.
2. Pass a Markdown file when the diagram lives inside a fenced `mermaid` block.
3. When invoking the script from Codex, request escalated permissions up front for the render command. On this machine, sandboxed Mermaid CLI and Chrome runs can hang even when the diagram is valid.
4. Use `--diagram-index` when you want one specific Mermaid block.
5. Use `--all` when you want separate output files for every Mermaid block in the Markdown source.
6. Pass a `.mmd` file when the Mermaid source already exists on disk.
7. Use PNG for slide decks and screenshots. Use SVG when the user wants scalable output.
8. Increase `--width`, `--height`, or `--scale` if the exported PNG is too small.

## Notes

- The script treats `.md`, `.markdown`, and `.mdx` as Markdown sources.
- `--diagram-index` is 1-based.
- `--all` only works with Markdown input.
- Without `{index}` in the output path, `--all` writes numbered files next to the requested output path using the pattern `name-1.png`, `name-2.png`, and so on.
- In Codex, prefer running the render command with escalated permissions immediately instead of first attempting a sandboxed run. This avoids local hangs in Mermaid CLI and browser startup.
- The script prefers a real Google Chrome or Chromium executable over broken wrapper scripts.
- The script shells out to `npx --yes @mermaid-js/mermaid-cli`, so network access or package approval may still be required the first time Mermaid CLI is used on a machine.
