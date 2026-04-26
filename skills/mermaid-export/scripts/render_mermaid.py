#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdx"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract Mermaid diagrams from Markdown or render a raw .mmd file."
    )
    parser.add_argument("input", help="Path to a Markdown file or raw Mermaid file")
    parser.add_argument("output", help="Output .png or .svg path")
    parser.add_argument(
        "--diagram-index",
        type=int,
        default=1,
        help="1-based Mermaid block index when input is Markdown (default: 1)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Render all Mermaid blocks from a Markdown file into separate outputs",
    )
    parser.add_argument("--width", type=int, default=2400, help="Canvas width")
    parser.add_argument("--height", type=int, default=3200, help="Canvas height")
    parser.add_argument("--scale", type=float, default=2.0, help="PNG scale factor")
    parser.add_argument(
        "--background", default="white", help="Background color for PNG/SVG"
    )
    return parser.parse_args()


def extract_mermaid_blocks(markdown: str) -> list[str]:
    blocks = []
    in_block = False
    current = []

    for line in markdown.splitlines():
        stripped = line.strip()
        if not in_block and stripped == "```mermaid":
            in_block = True
            current = []
            continue
        if in_block and stripped == "```":
            blocks.append("\n".join(current).rstrip() + "\n")
            in_block = False
            current = []
            continue
        if in_block:
            current.append(line)

    return blocks


def extract_mermaid_block(markdown: str, diagram_index: int) -> str:
    blocks = extract_mermaid_blocks(markdown)

    if diagram_index < 1:
        raise ValueError("--diagram-index must be 1 or greater")
    if diagram_index > len(blocks):
        raise ValueError(
            f"Markdown contains {len(blocks)} mermaid block(s); "
            f"cannot select diagram {diagram_index}"
        )
    return blocks[diagram_index - 1]


def detect_browser() -> str | None:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"),
        shutil.which("chromium-browser"),
        shutil.which("chromium"),
        shutil.which("chrome"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    return None


def render_mermaid(
    source_path: Path,
    output_path: Path,
    width: int,
    height: int,
    scale: float,
    background: str,
) -> None:
    output_format = output_path.suffix.lower().lstrip(".")
    if output_format not in {"png", "svg"}:
        raise ValueError("Output path must end with .png or .svg")

    cmd = [
        "npx",
        "--yes",
        "@mermaid-js/mermaid-cli",
        "-i",
        str(source_path),
        "-o",
        str(output_path),
        "-e",
        output_format,
        "-w",
        str(width),
        "-H",
        str(height),
        "-b",
        background,
    ]
    if output_format == "png":
        cmd.extend(["-s", str(scale)])

    browser = detect_browser()
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        config_path = Path(handle.name)
        if browser:
            json.dump(
                {
                    "executablePath": browser,
                    "args": [
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--allow-file-access-from-files",
                    ],
                },
                handle,
            )
            cmd[3:3] = ["-p", str(config_path)]

    try:
        subprocess.run(cmd, check=True)
    finally:
        config_path.unlink(missing_ok=True)


def build_indexed_output_path(output_path: Path, index: int) -> Path:
    output_text = str(output_path)
    if "{index}" in output_text:
        return Path(output_text.replace("{index}", str(index)))
    return output_path.with_name(f"{output_path.stem}-{index}{output_path.suffix}")


def render_source_text(
    mermaid: str,
    output_path: Path,
    width: int,
    height: int,
    scale: float,
    background: str,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False) as handle:
        handle.write(mermaid)
        source_path = Path(handle.name)

    try:
        render_mermaid(
            source_path=source_path,
            output_path=output_path,
            width=width,
            height=height,
            scale=scale,
            background=background,
        )
    finally:
        source_path.unlink(missing_ok=True)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    try:
        if input_path.suffix.lower() in MARKDOWN_SUFFIXES:
            markdown = input_path.read_text(encoding="utf-8")
            if args.all:
                blocks = extract_mermaid_blocks(markdown)
                if not blocks:
                    raise ValueError("Markdown does not contain any mermaid blocks")
                for index, mermaid in enumerate(blocks, start=1):
                    indexed_output_path = build_indexed_output_path(output_path, index)
                    render_source_text(
                        mermaid=mermaid,
                        output_path=indexed_output_path,
                        width=args.width,
                        height=args.height,
                        scale=args.scale,
                        background=args.background,
                    )
                    print(indexed_output_path)
                return 0
            mermaid = extract_mermaid_block(markdown, args.diagram_index)
        else:
            if args.all:
                raise ValueError("--all can only be used with Markdown input")
            mermaid = input_path.read_text(encoding="utf-8")

        render_source_text(
            mermaid=mermaid,
            output_path=output_path,
            width=args.width,
            height=args.height,
            scale=args.scale,
            background=args.background,
        )
    except Exception as exc:
        print(f"render_mermaid.py: {exc}", file=sys.stderr)
        return 1

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
