"""Generate replacement T3 Code icons.

Each variant is written as SVG, rendered to a 1024px PNG with headless Chrome,
then packed into a multi-size Windows .ico. The preview sheets are rebuilt at the end.

    python gen.py              # everything
    python gen.py neon         # just one
"""
import base64, io, os, pathlib, subprocess, sys

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


# --- Stylised set (Arc-style alternate icons) -------------------------------
# Built lazily: some need extra assets (displacement maps, a rasterised glyph mask).

def scaled(k):
    return f'transform="translate(512 512) scale({k}) translate(-512 -512)"'

def puffy(fill, k=.86, r=44, spread=0, extra=""):
    """Glyph with rounded, inflated corners (fill + same-colour round-join stroke).

    `spread` nudges the T and 3 apart so inflated letters don't fuse.
    """
    return (f'<g fill="{fill}" stroke="{fill}" stroke-width="{r}" stroke-linejoin="round" {extra}>'
            f'<g {scaled(k)}><path transform="translate({-spread} 0)" d="{T_PATH}"/>'
            f'<path transform="translate({spread} 0)" d="{THREE_PATH}"/></g></g>')

def bevel(fid, blur, height, spec, shine, light=(260, 80, 520), diffuse=True):
    """Lighting filter that turns a flat shape into a lit, rounded surface."""
    lx, ly, lz = light
    shade = (f'<feDiffuseLighting in="b" surfaceScale="{height}" diffuseConstant="1.05" lighting-color="#fff" result="d">'
             f'<fePointLight x="{lx}" y="{ly}" z="{lz * 2}"/></feDiffuseLighting>'
             '<feComposite in="SourceGraphic" in2="d" operator="arithmetic" k1="1" result="base"/>'
             if diffuse else '<feMerge result="base"><feMergeNode in="SourceGraphic"/></feMerge>')
    return f"""<filter id="{fid}" filterUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <feGaussianBlur in="SourceAlpha" stdDeviation="{blur}" result="b"/>
    {shade}
    <feSpecularLighting in="b" surfaceScale="{height}" specularConstant="{spec}" specularExponent="{shine}" lighting-color="#fff" result="s">
      <fePointLight x="{lx}" y="{ly}" z="{lz}"/></feSpecularLighting>
    <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
    <feComposite in="base" in2="s2" operator="arithmetic" k2="1" k3="1"/>
  </filter>"""

def data_png(im):
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def sparkle(x, y, r, fill="#fff", op=1):
    q = r * .18
    return (f'<path d="M{x} {y-r} Q{x+q} {y-q} {x+r} {y} Q{x+q} {y+q} {x} {y+r} Q{x-q} {y+q} {x-r} {y} Q{x-q} {y-q} {x} {y-r}Z" '
            f'fill="{fill}" opacity="{op}"/>')


def neon():
    tube = lambda c: f"""
      <g fill="none" stroke="{c}" stroke-linejoin="round" {scaled(.8)}>
        <g filter="url(#haze)" stroke-width="40" opacity=".9"><path d="{T_PATH}"/><path d="{THREE_PATH}"/></g>
        <g filter="url(#halo)" stroke-width="30"><path d="{T_PATH}"/><path d="{THREE_PATH}"/></g>
        <g stroke-width="26"><path d="{T_PATH}"/><path d="{THREE_PATH}"/></g>
      </g>"""
    core = f'<g fill="none" stroke="#fff" stroke-opacity=".85" stroke-width="9" stroke-linejoin="round" {scaled(.8)}>'
    return f"""
<defs>{DEFS}
  <pattern id="brick" width="160" height="80" patternUnits="userSpaceOnUse">
    <rect width="160" height="80" fill="#140f1c"/>
    <path d="M0 0.5H160M0 40.5H160M0.5 0V40M80.5 40V80" stroke="#07050b" stroke-width="7"/>
  </pattern>
  <radialGradient id="vig" cx="50%" cy="50%" r="70%">
    <stop offset=".35" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/>
  </radialGradient>
  <filter id="haze" filterUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}"><feGaussianBlur stdDeviation="46"/></filter>
  <filter id="halo" filterUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}"><feGaussianBlur stdDeviation="12"/></filter>
  <clipPath id="left"><rect width="522" height="{S}"/></clipPath>
  <clipPath id="right"><rect x="522" width="{S}" height="{S}"/></clipPath>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#brick)"/>
  <ellipse cx="330" cy="512" rx="360" ry="300" fill="#ff2fb4" opacity=".16" filter="url(#haze)"/>
  <ellipse cx="720" cy="512" rx="340" ry="300" fill="#22e6ff" opacity=".14" filter="url(#haze)"/>
  <g clip-path="url(#left)">{tube("#ff2fb4")}</g>
  <g clip-path="url(#right)">{tube("#22e6ff")}</g>
  {core}<path d="{T_PATH}"/><path d="{THREE_PATH}"/></g>
  <rect width="{S}" height="{S}" fill="url(#vig)"/>
  {RIM}
</g>
"""


def gummy():
    return f"""
<defs>{DEFS}
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ffe0f0"/><stop offset="1" stop-color="#c9b8ff"/>
  </linearGradient>
  <linearGradient id="jelly" x1="0" y1="250" x2="0" y2="780" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#ff6fa8"/><stop offset="1" stop-color="#e0106a"/>
  </linearGradient>
  {bevel("gel", 26, 11, .95, 22, light=(250, 60, 460))}
  <filter id="shadow" filterUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <feGaussianBlur stdDeviation="26"/><feOffset dy="34"/>
  </filter>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#bg)"/>
  {puffy("#b0104f", r=24, spread=14, extra='filter="url(#shadow)" opacity=".45"')}
  {puffy("url(#jelly)", r=24, spread=14, extra='filter="url(#gel)"')}
</g>
"""


def fluted():
    rib = 56
    dmap = Image.new("RGB", (S, S))
    row = bytes(b for x in range(S) for b in (round(255 * (x % rib) / (rib - 1)), 128, 128))
    dmap.frombytes(row * S)
    return f"""
<defs>{DEFS}
  <filter id="blobs" filterUnits="userSpaceOnUse" x="-300" y="-300" width="1624" height="1624"><feGaussianBlur stdDeviation="95"/></filter>
  <filter id="flute" filterUnits="userSpaceOnUse" x="-300" y="-300" width="1624" height="1624">
    <feImage href="{data_png(dmap)}" x="0" y="0" width="{S}" height="{S}" preserveAspectRatio="none" result="map"/>
    <feDisplacementMap in="SourceGraphic" in2="map" scale="150" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <linearGradient id="ribshade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".25" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".8" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".18"/>
  </linearGradient>
  <pattern id="ribs" width="{rib}" height="{S}" patternUnits="userSpaceOnUse">
    <rect width="{rib}" height="{S}" fill="url(#ribshade)"/>
  </pattern>
  <filter id="lift" filterUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <feGaussianBlur in="SourceAlpha" stdDeviation="20"/><feOffset dy="16"/>
    <feColorMatrix values="0 0 0 0 .1  0 0 0 0 0  0 0 0 0 .2  0 0 0 .45 0"/>
    <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<g clip-path="url(#sq)">
  <g filter="url(#flute)">
    <rect x="-300" y="-300" width="1624" height="1624" fill="#1b0b3a"/>
    <g filter="url(#blobs)">
      <circle cx="220" cy="230" r="320" fill="#ff7a18"/>
      <circle cx="820" cy="260" r="300" fill="#ff2d95"/>
      <circle cx="330" cy="860" r="340" fill="#7b2ff7"/>
      <circle cx="860" cy="860" r="280" fill="#00c2ff"/>
      <circle cx="560" cy="540" r="160" fill="#ffd24a" opacity=".8"/>
    </g>
  </g>
  <rect width="{S}" height="{S}" fill="url(#ribs)"/>
  <g filter="url(#lift)">{glyph("#fff", scaled(.86))}</g>
  {RIM}
</g>
"""


def chrome():
    stars = "".join(sparkle(x, y, r, op=o) for x, y, r, o in
                    ((820, 190, 58, 1), (190, 820, 34, .8), (880, 700, 22, .6), (150, 200, 18, .5)))
    return f"""
<defs>{DEFS}
  <radialGradient id="bg" cx="50%" cy="40%" r="75%">
    <stop offset="0" stop-color="#1c2b5a"/><stop offset=".6" stop-color="#070a18"/><stop offset="1" stop-color="#020308"/>
  </radialGradient>
  <linearGradient id="metal" x1="0" y1="250" x2="0" y2="780" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="#b9d4ff"/><stop offset=".47" stop-color="#46618f"/>
    <stop offset=".5" stop-color="#0d1426"/><stop offset=".53" stop-color="#4a3a2a"/><stop offset=".72" stop-color="#e9cfa6"/>
    <stop offset="1" stop-color="#ffffff"/>
  </linearGradient>
  {bevel("shine", 16, 10, 1.6, 40, light=(700, 120, 380), diffuse=False)}
  <filter id="glow" filterUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}"><feGaussianBlur stdDeviation="30"/></filter>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#bg)"/>
  {puffy("#6f8cff", r=60, extra='filter="url(#glow)" opacity=".7"')}
  {puffy("#0a0f22", r=58)}
  {puffy("url(#metal)", r=22, extra='filter="url(#shine)"')}
  {stars}
  {RIM}
</g>
"""


def sketch():
    return f"""
<defs>{DEFS}
  <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
    <path d="M0 .5H48M.5 0V48" stroke="#9ec3ea" stroke-width="2" fill="none"/>
  </pattern>
  <pattern id="hatch" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(-38)">
    <path d="M0 13H26" stroke="#2448c9" stroke-width="7"/>
  </pattern>
  <filter id="wobble" filterUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <feTurbulence type="fractalNoise" baseFrequency=".018" numOctaves="2" seed="7"/>
    <feDisplacementMap in="SourceGraphic" scale="16" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="wobble2" filterUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">
    <feTurbulence type="fractalNoise" baseFrequency=".022" numOctaves="2" seed="21"/>
    <feDisplacementMap in="SourceGraphic" scale="20" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="#fbf8ef"/>
  <rect width="{S}" height="{S}" fill="url(#grid)"/>
  <path d="M170 0V{S}" stroke="#ef7d7d" stroke-width="5"/>
  <g filter="url(#wobble)">{glyph("url(#hatch)", scaled(.84))}</g>
  <g filter="url(#wobble)" fill="none" stroke="#1a2fa0" stroke-width="13" stroke-linejoin="round" {scaled(.84)}>
    <path d="{T_PATH}"/><path d="{THREE_PATH}"/></g>
  <g filter="url(#wobble2)" fill="none" stroke="#1a2fa0" stroke-width="6" opacity=".65" stroke-linejoin="round"
     transform="translate(10 -8) translate(512 512) scale(.84) translate(-512 -512)">
    <path d="{T_PATH}"/><path d="{THREE_PATH}"/></g>
  <path filter="url(#wobble2)" d="M200 845 C330 815 470 870 600 840 S790 815 850 838" fill="none" stroke="#e5484d" stroke-width="16" stroke-linecap="round"/>
  {sparkle(862, 190, 60, fill="none")}
  <path filter="url(#wobble2)" d="M862 128 V252 M800 190 H924 M818 146 L906 234 M906 146 L818 234" stroke="#e5484d" stroke-width="12" stroke-linecap="round"/>
</g>
"""


def glyph_mask(cells, k):
    """Coverage of the glyph per cell on a cells x cells grid (0..1)."""
    tmp = OUT / "_mask.png"
    shoot(f'<rect width="{S}" height="{S}" fill="#000"/>{glyph("#fff", scaled(k))}', tmp)
    m = Image.open(tmp).convert("L").resize((cells, cells), Image.BOX)
    tmp.unlink()
    return [[m.getpixel((x, y)) / 255 for x in range(cells)] for y in range(cells)]


def pixel():
    n, c = 32, S // 32  # one art pixel per screen pixel at 32px
    cov = glyph_mask(n, .84)
    on = lambda x, y: 0 <= x < n and 0 <= y < n and cov[y][x] > .45
    corner = {(1, 1), (2, 1), (3, 1), (1, 2), (1, 3), (2, 2)}
    def in_tile(x, y):
        cx, cy = min(x, n - 1 - x), min(y, n - 1 - y)
        return cx >= 1 and cy >= 1 and (cx, cy) not in corner
    sky = ["#1b0f3b", "#241356", "#2f1870", "#3d1d86", "#51239a", "#6c2aa8", "#8a33ae", "#a83fad"]
    rects = []
    px = lambda x, y, col: rects.append(f'<rect x="{x * c}" y="{y * c}" width="{c}" height="{c}" fill="{col}"/>')
    stars = {(5, 4), (25, 5), (28, 12), (6, 25), (22, 27), (13, 3), (3, 16)}
    rows = n - 2
    for y in range(n):
        for x in range(n):
            if not in_tile(x, y):
                continue
            t = (y - 1) * len(sky) / rows
            band = int(t)
            # checkerboard dither on the last row of each band for that 16-colour feel
            if t - band > 1 - len(sky) / rows and (x + y) % 2 and band + 1 < len(sky):
                band += 1
            px(x, y, "#fff" if (x, y) in stars else sky[band])
    for y in range(n):
        for x in range(n):
            if on(x, y):
                continue
            if on(x - 2, y - 2) or on(x - 1, y - 2) or on(x - 2, y - 1):
                px(x, y, "#12072a")  # hard drop shadow
            if any(on(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px(x, y, "#12072a")  # outline
    for y in range(n):
        for x in range(n):
            if not on(x, y):
                continue
            col = "#ffcf3a"
            if not on(x, y - 1) or not on(x - 1, y):
                col = "#fff2a8"
            elif not on(x, y + 1) or not on(x + 1, y):
                col = "#f08a1c"
            px(x, y, col)
    return f'<defs>{DEFS}</defs><g shape-rendering="crispEdges">{"".join(rects)}</g>'


styled = {"neon": neon, "gummy": gummy, "fluted": fluted, "chrome": chrome, "sketch": sketch, "pixel": pixel}

# Pixel art is scaled with nearest-neighbour wherever the size is a whole multiple of its grid,
# so the 32/64/128/256px frames stay sharp instead of being smoothed.
CRISP = {"pixel": 32}


def shrink(im, name, size):
    grid = CRISP.get(name)
    if grid and size % grid == 0:
        return im.resize((grid, grid), Image.BOX).resize((size, size), Image.NEAREST)
    return im.resize((size, size), Image.LANCZOS)


def shoot(body, png_path):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">{body}</svg>'
    html = png_path.with_name(f"_{png_path.stem}.html")
    html.write_text(f'<html><body style="margin:0;background:transparent">{svg}</body></html>', encoding="utf-8")
    try:
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--default-background-color=00000000", f"--window-size={S},{S}",
             f"--screenshot={png_path}", html.as_uri()],
            check=True, capture_output=True,
        )
    finally:
        html.unlink()
    return svg


def render(name, body):
    svg = shoot(body, OUT / f"{name}.png")
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
    pack(name)


def pack(name):
    """Recompress the rendered PNG losslessly and build the .ico from it."""
    path = OUT / f"{name}.png"
    png = Image.open(path).convert("RGBA")
    png.save(path, optimize=True)
    frames = [shrink(png, name, s) for s in ICO_SIZES]
    frames[-1].save(OUT / f"{name}.ico", sizes=[f.size for f in frames], append_images=frames[:-1])


def preview(names, path, per_row=4):
    """Large tile plus 48/32/16px thumbnails for each variant, on a dark background."""
    rows = -(-len(names) // per_row)
    cols = min(len(names), per_row)
    sheet = Image.new("RGBA", (cols * 272 + 16, rows * 352 + 16), (32, 32, 32, 255))
    for i, n in enumerate(names):
        im = Image.open(OUT / f"{n}.png").convert("RGBA")
        x, y = 16 + i % per_row * 272, 16 + i // per_row * 352
        sheet.alpha_composite(shrink(im, n, 256), (x, y))
        for dx, s in ((0, 48), (60, 32), (104, 16)):
            sheet.alpha_composite(shrink(im, n, s), (x + dx, y + 272))
    sheet.save(path, optimize=True)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    names = sys.argv[1:] or [*variants, *styled]
    unknown = [n for n in names if n not in variants and n not in styled]
    if unknown:
        sys.exit(f"unknown variant(s): {', '.join(unknown)}\navailable: {', '.join([*variants, *styled])}")
    for n in names:
        render(n, variants[n] if n in variants else styled[n]())
        print("rendered", n)
    preview(list(variants), HERE / "preview.png")
    preview(list(styled), HERE / "preview-styled.png", per_row=3)
