#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["cairosvg"]
# ///
"""Build images/logo.svg from the CC0 secateurs source + a git graph.

Composes a badge (circle) + a git commit graph + the public-domain secateurs
illustration (Openclipart, CC0), flattens the result via cairosvg so it uses
only portable primitives (no <pattern>/<image>/nested <svg>) and renders on
GitHub, then writes images/logo.svg. Regenerate images/logo.png separately.
"""

import math
import pathlib
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
SHEARS_FLAT = HERE / "shears_flat.svg"  # cairosvg-flattened CC0 source
OUT_SVG = HERE / "logo.svg"

# --- geometry knobs -------------------------------------------------------
VB_W, VB_H = 33.081445, 116.510838  # source shears viewBox
SHEARS_TARGET_H = 176.0
ROT = 135  # handles top-left, blade bottom-right
BLADE_ANCHOR = (19.0, 14.0)  # near the blade tip (cutting point), source coords
MAIN_Y = 60
TRUNK_XS = [-66, -22, 22, 66]  # 4 equidistant trunk commit dots
BRANCH_FROM_INDEX = 2  # branch off the 3rd dot
BRANCH_DELTA = 50  # 45deg branch length (dx == dy)


def main() -> None:
    inner_svg = SHEARS_FLAT.read_text(encoding="utf-8")
    inner = inner_svg[inner_svg.index(">", inner_svg.index("<svg")) + 1 : inner_svg.rindex("</svg>")]

    s = SHEARS_TARGET_H / VB_H
    theta = math.radians(ROT)
    ax_f = VB_W - BLADE_ANCHOR[0]  # mirrored x (long-axis flip)
    lx, ly = ax_f * s, BLADE_ANCHOR[1] * s
    rx = lx * math.cos(theta) - ly * math.sin(theta)
    ry = lx * math.sin(theta) + ly * math.cos(theta)

    third = TRUNK_XS[BRANCH_FROM_INDEX]
    end_x, end_y = third + BRANCH_DELTA, MAIN_Y - BRANCH_DELTA
    # Blade cuts at the MIDPOINT of the 45deg branch (not the tip).
    cut_x, cut_y = third + BRANCH_DELTA / 2, MAIN_Y - BRANCH_DELTA / 2
    tx, ty = cut_x - rx, cut_y - ry

    # Redraw the branch from the cut midpoint out to the end dot IN FRONT, so the
    # clipped-off portion appears gripped in the jaws (in front of the lower blade).
    bx, by = cut_x, cut_y

    shears_open = (
        f'<g transform="translate({tx:.3f} {ty:.3f}) rotate({ROT}) scale({s:.5f}) '
        f'scale(-1,1) translate({-VB_W},0)">'
        f'<svg width="{VB_W}" height="{VB_H}" viewBox="0 0 {VB_W} {VB_H}" overflow="visible">'
    )
    dots = "\n    ".join(f'<circle cx="{x}" cy="{MAIN_Y}" r="10" class="sec"/>' for x in TRUNK_XS)

    logo = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 266" width="1200" height="266" role="img" aria-label="git-secateurs">
  <title>git-secateurs</title>
  <desc>Secateurs clipping off a git branch — logo for the git-secateurs CLI.</desc>
  <style>
    .wordmark {{ font-family:"DejaVu Sans","Bitstream Vera Sans","Verdana",sans-serif; font-weight:700; }}
    .git {{ fill:#3F3F46; }} .sec {{ fill:#F05133; }}
    .tagline {{ font-family:"DejaVu Sans","Verdana",sans-serif; fill:#8A8A8A; letter-spacing:1px; }}
  </style>
  <g transform="translate(133 133)">
    <circle r="112" fill="#FBEDEA"/>
    <circle r="112" fill="none" stroke="#F05133" stroke-width="6"/>
    <g fill="none" stroke="#F05133" stroke-linecap="round" stroke-linejoin="round">
      <path d="M{TRUNK_XS[0]} {MAIN_Y} H{TRUNK_XS[-1]}" stroke-width="9"/>
      <path d="M{third} {MAIN_Y} L {end_x} {end_y}" stroke-width="9"/>
    </g>
    {dots}
    {shears_open}{inner}</svg></g>
    <path d="M{bx:.1f} {by:.1f} L {end_x} {end_y}" fill="none" stroke="#F05133" stroke-width="9" stroke-linecap="round"/>
    <circle cx="{end_x}" cy="{end_y}" r="9" class="sec"/>
  </g>
  <text x="288" y="150" class="wordmark" font-size="112"><tspan class="git">git-</tspan><tspan class="sec">secateurs</tspan></text>
  <text x="290" y="200" class="tagline" font-size="29">prune merged &amp; stray branches</text>
</svg>
"""

    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as tf:
        tf.write(logo)
        composed = tf.name
    # Flatten to portable primitives so it renders on GitHub.
    subprocess.run(["cairosvg", composed, "-f", "svg", "-o", str(OUT_SVG)], check=True)
    print(f"wrote {OUT_SVG}")


if __name__ == "__main__":
    main()
