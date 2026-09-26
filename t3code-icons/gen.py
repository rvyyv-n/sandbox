"""Generate dark-mode T3 Code icons.

Each variant is written as SVG, rendered to a 1024px PNG with headless Chrome,
then packed into a multi-size Windows .ico. A preview sheet is rebuilt at the end.

    python gen.py              # all variants
    python gen.py midnight     # just one
"""
import os, pathlib, subprocess, sys

from PIL import Image

HERE = pathlib.Path(__file__).parent
OUT = HERE / "icons"
CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
S = 1024
ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)

# Hand-drawn geometric "T3" as filled outlines (heavy verticals, slightly lighter horizontals).
T_PATH = "M140 282 H500 V386 H384 V742 H256 V386 H140 Z"
THREE_PATH = ("M544 282 H872 V376 L782 462 C846 470 884 522 884 602 C884 692 830 742 700 742 H544 V638 H700 "
              "C740 638 756 622 756 602 C756 582 740 566 700 566 H624 V478 L724 386 H544 Z")

def glyph(fill, extra=""):
    return f'<g fill="{fill}" {extra}><path d="{T_PATH}"/><path d="{THREE_PATH}"/></g>'

SHAPE = '<rect x="24" y="24" width="976" height="976" rx="236"/>'
DEFS = f"""<clipPath id="sq">{SHAPE}</clipPath>
  <linearGradient id="rim" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".4" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <filter id="drop" x="-20%" y="-20%" width="140%" height="160%">
    <feGaussianBlur stdDeviation="18"/><feOffset dy="18"/>
  </filter>
"""
RIM = '<rect x="24" y="24" width="976" height="976" rx="236" fill="none" stroke="url(#rim)" stroke-width="6"/>'

variants = {}

# Graphite: charcoal tile, soft silver T3
variants["graphite"] = f"""
<defs>{DEFS}
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#26262a"/><stop offset="1" stop-color="#111113"/>
  </linearGradient>
  <linearGradient id="ink" x1="0" y1="282" x2="0" y2="742" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#f5f5f6"/><stop offset="1" stop-color="#bdbdc4"/>
  </linearGradient>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#bg)"/>
  <g filter="url(#drop)" opacity=".6">{glyph("#000")}</g>
  {glyph("url(#ink)")}
  {RIM}
</g>
"""

# Midnight: deep navy-black, pale T3, small crescent for "nightly"
variants["midnight"] = f"""
<defs>{DEFS}
  <radialGradient id="bg" cx="70%" cy="10%" r="100%">
    <stop offset="0" stop-color="#1b2340"/><stop offset=".6" stop-color="#0c0f1c"/><stop offset="1" stop-color="#06070d"/>
  </radialGradient>
  <mask id="moon"><rect width="{S}" height="{S}" fill="#fff"/><circle cx="878" cy="138" r="58" fill="#000"/></mask>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#bg)"/>
  <circle cx="842" cy="168" r="62" fill="#9fb2ff" mask="url(#moon)"/>
  <g filter="url(#drop)" opacity=".5">{glyph("#000")}</g>
  {glyph("#e9edf8")}
  {RIM}
</g>
"""

# Accent: flat near-black, white T, violet 3
variants["accent"] = f"""
<defs>{DEFS}
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#18181b"/><stop offset="1" stop-color="#0c0c0e"/>
  </linearGradient>
  <linearGradient id="vio" x1="544" y1="282" x2="884" y2="742" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#b9a3ff"/><stop offset="1" stop-color="#7c5cff"/>
  </linearGradient>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#bg)"/>
  <path d="{T_PATH}" fill="#f4f4f5"/>
  <path d="{THREE_PATH}" fill="url(#vio)"/>
  {RIM}
</g>
"""

# Coral: flat, to sit next to Claude's icon (Claude coral tile, ivory mark, slightly smaller glyph)
variants["coral"] = f"""
<defs>{DEFS}</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="#d97757"/>
  {glyph("#faf9f5", 'transform="translate(512 512) scale(.88) translate(-512 -512)"')}
</g>
"""


def render(name, body):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">{body}</svg>'
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    html = OUT / f"_{name}.html"
    html.write_text(f'<html><body style="margin:0;background:transparent">{svg}</body></html>', encoding="utf-8")
    try:
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--default-background-color=00000000", f"--window-size={S},{S}",
             f"--screenshot={OUT / (name + '.png')}", html.as_uri()],
            check=True, capture_output=True,
        )
    finally:
        html.unlink()
    png = Image.open(OUT / f"{name}.png").convert("RGBA")
    png.resize((256, 256), Image.LANCZOS).save(OUT / f"{name}.ico", sizes=[(s, s) for s in ICO_SIZES])


def preview():
    """Large tile plus 48/32/16px thumbnails for each variant, on a dark background."""
    names = list(variants)
    sheet = Image.new("RGBA", (len(names) * 272 + 16, 368), (32, 32, 32, 255))
    for i, n in enumerate(names):
        im = Image.open(OUT / f"{n}.png").convert("RGBA")
        x = 16 + i * 272
        sheet.alpha_composite(im.resize((256, 256), Image.LANCZOS), (x, 16))
        for dx, s in ((0, 48), (60, 32), (104, 16)):
            sheet.alpha_composite(im.resize((s, s), Image.LANCZOS), (x + dx, 288))
    sheet.save(HERE / "preview.png")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for n in sys.argv[1:] or variants:
        render(n, variants[n])
        print("rendered", n)
    preview()
