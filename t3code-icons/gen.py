"""generate replacement t3 code icons.

each variant is written as svg, rendered to a 1024px png with headless chrome,
then packed into a multi-size windows .ico. the preview sheets are rebuilt at the end.

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

# hand-drawn geometric "t3" as filled outlines (heavy verticals, slightly lighter horizontals).
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

# graphite: charcoal tile, soft silver t3
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

# midnight: deep navy-black, pale t3, small crescent for "nightly"
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

# accent: flat near-black, white t, violet 3
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

# coral: flat, to sit next to claude's icon (claude coral tile, ivory mark, slightly smaller glyph)
variants["coral"] = f"""
<defs>{DEFS}</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="#d97757"/>
  {glyph("#faf9f5", 'transform="translate(512 512) scale(.88) translate(-512 -512)"')}
</g>
"""

# bone: warm off-white / light ceramic, dark ink glyph (clean light-mode)
variants["bone"] = f"""
<defs>{DEFS}
  <linearGradient id="bg_bone" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f7f6f2"/>
    <stop offset="1" stop-color="#eae7de"/>
  </linearGradient>
  <linearGradient id="bone_rim" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000" stop-opacity=".08"/>
    <stop offset="1" stop-color="#000" stop-opacity=".18"/>
  </linearGradient>
  <filter id="bone_drop" x="-20%" y="-20%" width="140%" height="160%">
    <feGaussianBlur stdDeviation="12"/>
    <feOffset dy="14"/>
    <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0   0 0 0 0.15 0"/>
  </filter>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#bg_bone)"/>
  <g filter="url(#bone_drop)">{glyph("#18181b")}</g>
  {glyph("#18181b")}
  <rect x="24" y="24" width="976" height="976" rx="236" fill="none" stroke="url(#bone_rim)" stroke-width="4"/>
</g>
"""

# noir: pitch black OLED minimal, stark white mark
variants["noir"] = f"""
<defs>{DEFS}
  <linearGradient id="noir_rim" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".28"/>
    <stop offset=".4" stop-color="#fff" stop-opacity=".06"/>
    <stop offset="1" stop-color="#fff" stop-opacity=".02"/>
  </linearGradient>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="#08080a"/>
  {glyph("#ffffff")}
  <rect x="24" y="24" width="976" height="976" rx="236" fill="none" stroke="url(#noir_rim)" stroke-width="4"/>
</g>
"""

# braun: Dieter Rams industrial minimalism (warm light grey, anthracite mark, orange tactile dot)
variants["braun"] = f"""
<defs>{DEFS}
  <linearGradient id="bg_braun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#eceae4"/>
    <stop offset="1" stop-color="#dedbd2"/>
  </linearGradient>
  <linearGradient id="braun_rim" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".6"/>
    <stop offset="1" stop-color="#000" stop-opacity=".12"/>
  </linearGradient>
  <filter id="braun_drop" x="-20%" y="-20%" width="140%" height="160%">
    <feGaussianBlur stdDeviation="8"/>
    <feOffset dy="10"/>
    <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0   0 0 0 0.18 0"/>
  </filter>
  <radialGradient id="braun_dot" cx="35%" cy="30%" r="70%">
    <stop offset="0" stop-color="#ff6b2b"/>
    <stop offset="1" stop-color="#e04300"/>
  </radialGradient>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#bg_braun)"/>
  <g filter="url(#braun_drop)">{glyph("#232326")}</g>
  {glyph("#232326")}
  <circle cx="850" cy="170" r="32" fill="url(#braun_dot)"/>
  <rect x="24" y="24" width="976" height="976" rx="236" fill="none" stroke="url(#braun_rim)" stroke-width="4"/>
</g>
"""

# nord: arctic slate tile with polar white T and glacial frost cyan 3
variants["nord"] = f"""
<defs>{DEFS}
  <linearGradient id="bg_nord" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2e3440"/>
    <stop offset="1" stop-color="#21252e"/>
  </linearGradient>
  <linearGradient id="frost_cyan" x1="544" y1="282" x2="884" y2="742" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#88c0d0"/>
    <stop offset="1" stop-color="#81a1c1"/>
  </linearGradient>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#bg_nord)"/>
  <g filter="url(#drop)" opacity=".5">{glyph("#000")}</g>
  <path d="{T_PATH}" fill="#eceff4"/>
  <path d="{THREE_PATH}" fill="url(#frost_cyan)"/>
  {RIM}
</g>
"""


# --- stylised set (arc-style alternate icons) -------------------------------
# built lazily: some need extra assets (displacement maps, a rasterised glyph mask).

def scaled(k):
    return f'transform="translate(512 512) scale({k}) translate(-512 -512)"'

def puffy(fill, k=.86, r=44, spread=0, extra=""):
    """glyph with rounded, inflated corners (fill + same-colour round-join stroke).

    `spread` nudges the t and 3 apart so inflated letters don't fuse.
    """
    return (f'<g fill="{fill}" stroke="{fill}" stroke-width="{r}" stroke-linejoin="round" {extra}>'
            f'<g {scaled(k)}><path transform="translate({-spread} 0)" d="{T_PATH}"/>'
            f'<path transform="translate({spread} 0)" d="{THREE_PATH}"/></g></g>')

def bevel(fid, blur, height, spec, shine, light=(260, 80, 520), diffuse=True):
    """lighting filter that turns a flat shape into a lit, rounded surface."""
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
    """coverage of the glyph per cell on a cells x cells grid (0..1)."""
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


def cleartech():
    elements = []
    elements.append('''
    <pattern id="pcb_grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 0 16 H 32 M 16 0 V 32" stroke="#2a1b4e" stroke-width="1.5" fill="none"/>
      <circle cx="16" cy="16" r="1.5" fill="#3a256a"/>
    </pattern>
    <rect x="44" y="44" width="936" height="936" fill="url(#pcb_grid)" opacity=".7"/>
    ''')

    for fx in range(250, 775, 18):
        elements.append(f'''
        <rect x="{fx}" y="50" width="11" height="48" rx="2.5" fill="url(#gold_pad)" stroke="#9a6e1a" stroke-width="1.2"/>
        <line x1="{fx + 5.5}" y1="98" x2="{fx + 5.5}" y2="120" stroke="#d49a37" stroke-width="3" stroke-linecap="round"/>
        <circle cx="{fx + 5.5}" cy="120" r="5" fill="#f5c754"/>
        <circle cx="{fx + 5.5}" cy="120" r="2.2" fill="#140c26"/>
        ''')

    bus_traces = [
        ("M 260 120 V 160 L 210 210 V 310 L 160 360 V 580 L 110 630 H 70", 5),
        ("M 278 120 V 154 L 228 204 V 304 L 178 354 V 574 L 128 624 H 70", 3.5),
        ("M 296 120 V 148 L 246 198 V 298 L 196 348 V 568 L 146 618 H 70", 3.5),
        ("M 314 120 V 142 L 264 192 V 292 L 214 342 V 562 L 164 612 H 70", 3.5),
        ("M 70 240 H 130 L 180 290 H 220", 8),
        ("M 70 700 H 140 L 220 780 H 300 L 340 820 V 910", 7),
        ("M 950 260 H 890 L 840 210 H 780", 7),
        ("M 950 720 H 870 L 800 790 H 680 L 640 830 H 520 L 480 870 V 930", 7),
        ("M 760 120 V 150 L 820 210 V 320 L 880 380 V 540 L 840 580 V 670 L 890 720 H 950", 4.5),
        ("M 742 120 V 156 L 802 216 V 314 L 862 374 V 534 L 822 574 V 664 L 872 714 H 950", 3.5),
        ("M 724 120 V 162 L 784 222 V 308 L 844 368 V 528 L 804 568 V 658 L 854 708 H 950", 3.5),
        ("M 706 120 V 168 L 766 228 V 302 L 826 362 V 522 L 786 562 V 652 L 836 702 H 950", 3.5),
        ("M 470 240 V 340 L 510 380 V 540 L 470 580 V 780 L 510 820 V 920", 5),
        ("M 445 270 V 330 L 485 370 V 530 L 445 570 V 760 L 485 800 V 920", 3.5),
        ("M 535 240 V 350 L 495 390 V 550 L 535 590 V 770 L 495 810 V 920", 4),
        ("M 560 270 V 360 L 520 400 V 560 L 560 600 V 790 L 520 830 V 920", 3.5),
        ("M 100 440 H 150 L 200 490 V 550 L 150 600 H 90", 4),
        ("M 220 740 L 270 790 H 380 L 420 830 H 460", 4),
        ("M 580 840 H 680 L 730 790 H 830", 4.5),
        ("M 600 870 H 700 L 740 830 H 850 L 890 870 H 940", 4),
        ("M 80 820 L 130 870 H 220 L 260 910 H 340", 4.5),
        ("M 940 370 H 890 L 840 420 H 790", 4),
        ("M 940 470 H 880 L 830 520 H 770", 4),
    ]
    for d, w in bus_traces:
        elements.append(f'<path d="{d}" fill="none" stroke="#e5a93c" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')
        elements.append(f'<path d="{d}" fill="none" stroke="#fff0aa" stroke-width="{max(1.2, w*0.35)}" stroke-linecap="round" stroke-linejoin="round" opacity=".4"/>')

    diffs = [
        "M 80 390 H 130 L 170 430 V 510 L 130 550 H 80",
        "M 80 402 H 125 L 165 442 V 502 L 125 542 H 80",
        "M 870 410 H 820 L 780 450 V 510 L 820 550 H 870",
        "M 870 422 H 815 L 775 462 V 502 L 815 542 H 870",
    ]
    for d in diffs:
        elements.append(f'<path d="{d}" fill="none" stroke="#38bdf8" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>')

    vias = [
        (70, 240), (220, 290), (70, 700), (340, 910), (950, 260), (780, 210),
        (950, 720), (480, 930), (510, 920), (485, 920), (495, 920), (520, 920),
        (90, 600), (460, 830), (830, 790), (940, 870), (790, 420),
        (770, 520), (70, 630), (70, 624), (70, 618), (70, 612),
        (950, 714), (950, 708), (950, 702),
        (100, 160), (115, 160), (130, 160), (145, 160),
        (880, 160), (895, 160), (910, 160), (925, 160),
        (100, 860), (115, 860), (130, 860), (145, 860),
        (880, 860), (895, 860), (910, 860), (925, 860),
        (380, 860), (395, 860), (410, 860), (425, 860),
        (610, 860), (625, 860), (640, 860), (655, 860),
        (180, 120), (340, 150), (430, 190), (590, 190), (680, 150), (840, 120),
        (110, 310), (910, 310), (110, 670), (910, 670), (512, 160), (512, 860),
    ]
    for vx, vy in vias:
        elements.append(f'''
        <circle cx="{vx}" cy="{vy}" r="7" fill="url(#gold_pad)" stroke="#9a6e1a" stroke-width="1.2"/>
        <circle cx="{vx}" cy="{vy}" r="4.2" fill="#e2e8f0"/>
        <circle cx="{vx}" cy="{vy}" r="2.2" fill="#140a24"/>
        ''')

    tps = [
        (180, 85, "TP1"), (840, 85, "TP2"), (85, 470, "GND"),
        (935, 470, "VCC"), (460, 940, "CLK"), (560, 940, "RST")
    ]
    for tx, ty, lbl in tps:
        elements.append(f'''
        <circle cx="{tx}" cy="{ty}" r="12" fill="url(#gold_pad)" stroke="#a16207" stroke-width="2"/>
        <circle cx="{tx}" cy="{ty}" r="5" fill="#ffffff" opacity=".85"/>
        <text x="{tx}" y="{ty + 22}" fill="#e9d5ff" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">{lbl}</text>
        ''')

    cx, cy, cw = 720, 175, 88
    bx, by = cx - cw//2, cy - cw//2
    for p in range(7):
        off = -30 + p * 10
        elements.append(f'<rect x="{cx + off - 2.5}" y="{by - 15}" width="5" height="15" fill="#f1f5f9" stroke="#64748b" stroke-width=".8"/>')
        elements.append(f'<rect x="{cx + off - 2.5}" y="{by + cw}" width="5" height="15" fill="#f1f5f9" stroke="#64748b" stroke-width=".8"/>')
        elements.append(f'<rect x="{bx - 15}" y="{cy + off - 2.5}" width="15" height="5" fill="#f1f5f9" stroke="#64748b" stroke-width=".8"/>')
        elements.append(f'<rect x="{bx + cw}" y="{cy + off - 2.5}" width="15" height="5" fill="#f1f5f9" stroke="#64748b" stroke-width=".8"/>')
    elements.append(f'''
    <rect x="{bx}" y="{by}" width="{cw}" height="{cw}" rx="6" fill="#13111c" stroke="#2e2640" stroke-width="2.5"/>
    <circle cx="{bx + 14}" cy="{by + 14}" r="4" fill="#ffffff" opacity=".5"/>
    <text x="{cx}" y="{cy - 8}" fill="#c084fc" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="1">T3-SOC</text>
    <text x="{cx}" y="{cy + 8}" fill="#94a3b8" font-family="monospace" font-size="8.5" text-anchor="middle">9842AH</text>
    <text x="{cx}" y="{cy + 24}" fill="#f5c754" font-family="sans-serif" font-size="7.5" font-weight="bold" text-anchor="middle">REV 3.0</text>
    <rect x="{bx - 20}" y="{by - 20}" width="{cw + 40}" height="{cw + 40}" fill="none" stroke="#ffffff" stroke-width="1.2" opacity=".4" stroke-dasharray="8,6"/>
    <text x="{bx - 20}" y="{by - 24}" fill="#ffffff" font-family="monospace" font-size="11" font-weight="bold" opacity=".7">U1</text>
    ''')

    cx2, cy2, cw2, ch2 = 310, 840, 108, 52
    bx2, by2 = cx2 - cw2//2, cy2 - ch2//2
    for p in range(8):
        off = -35 + p * 10
        elements.append(f'<rect x="{cx2 + off - 2.5}" y="{by2 - 13}" width="5" height="13" fill="#f1f5f9" stroke="#64748b" stroke-width=".8"/>')
        elements.append(f'<rect x="{cx2 + off - 2.5}" y="{by2 + ch2}" width="5" height="13" fill="#f1f5f9" stroke="#64748b" stroke-width=".8"/>')
    elements.append(f'''
    <rect x="{bx2}" y="{by2}" width="{cw2}" height="{ch2}" rx="5" fill="#13111c" stroke="#2e2640" stroke-width="2.5"/>
    <path d="M {bx2} {cy2 - 8} A 8 8 0 0 1 {bx2} {cy2 + 8}" fill="none" stroke="#372c4d" stroke-width="2.5"/>
    <text x="{cx2}" y="{cy2 - 3}" fill="#c084fc" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="1">SRAM-512K</text>
    <text x="{cx2}" y="{cy2 + 13}" fill="#94a3b8" font-family="monospace" font-size="8.5" text-anchor="middle">12NS FAST</text>
    <text x="{bx2 - 18}" y="{by2 - 14}" fill="#ffffff" font-family="monospace" font-size="11" font-weight="bold" opacity=".7">U2</text>
    ''')

    elements.append('''
    <g transform="translate(200 175)">
      <rect x="-48" y="-12" width="12" height="24" rx="2" fill="url(#gold_pad)"/>
      <rect x="36" y="-12" width="12" height="24" rx="2" fill="url(#gold_pad)"/>
      <rect x="-42" y="-19" width="84" height="38" rx="19" fill="url(#metal_can)" stroke="#64748b" stroke-width="2"/>
      <rect x="-38" y="-15" width="76" height="9" rx="4.5" fill="#ffffff" opacity=".55"/>
      <text x="0" y="5" fill="#1e293b" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">16.000 MHz</text>
      <text x="-52" y="-22" fill="#ffffff" font-family="monospace" font-size="11" font-weight="bold" opacity=".7">Y1</text>
    </g>
    ''')

    elements.append('''
    <g transform="translate(780 830)">
      <circle cx="0" cy="0" r="30" fill="url(#cap_metal)" stroke="#64748b" stroke-width="2.5"/>
      <path d="M -18 -24 L 18 -24 L 18 24 L -18 24 Z" fill="#1e293b" opacity=".35"/>
      <line x1="-14" y1="-30" x2="-14" y2="30" stroke="#ffffff" stroke-width="2.5" opacity=".7"/>
      <text x="0" y="4" fill="#0f172a" font-family="sans-serif" font-size="10" font-weight="bold" text-anchor="middle">220µF</text>
      <text x="36" y="-20" fill="#ffffff" font-family="monospace" font-size="11" font-weight="bold" opacity=".7">C1</text>
    </g>
    ''')

    passives = [
        (130, 205, False, 0, "R1"), (130, 228, True, 0, "C2"),
        (285, 205, True, 90, "C3"), (610, 125, False, 0, "R2"),
        (610, 148, True, 0, "C4"), (835, 125, True, 90, "C5"),
        (835, 155, False, 90, "R3"), (80, 480, False, 90, "R4"),
        (80, 508, True, 90, "C6"), (470, 765, True, 0, "C7"),
        (470, 788, False, 0, "R5"), (460, 840, True, 90, "C8"),
        (460, 868, False, 90, "R6"), (640, 805, False, 0, "R7"),
        (640, 828, True, 0, "C9"), (640, 851, False, 0, "R8"),
        (890, 715, True, 90, "C10"), (890, 745, False, 90, "R9"),
        (380, 120, True, 0, "C11"), (540, 120, False, 0, "R10"),
    ]
    for px, py, is_cap, rot, lbl in passives:
        bcol = "#a26338" if is_cap else "#171520"
        elements.append(f'''
        <g transform="translate({px} {py}) rotate({rot})">
          <rect x="-11" y="-6" width="22" height="12" rx="2" fill="{bcol}"/>
          <rect x="-11" y="-6" width="5" height="12" rx="1.2" fill="#f1f5f9"/>
          <rect x="6" y="-6" width="5" height="12" rx="1.2" fill="#f1f5f9"/>
        </g>
        ''')

    silkscreen = [
        '<text x="512" y="108" fill="#ffffff" font-family="monospace" font-size="12" font-weight="bold" letter-spacing="4" text-anchor="middle" opacity=".45">-- ATOMIC ARCHITECTURE --</text>',
        '<text x="512" y="930" fill="#ffffff" font-family="monospace" font-size="11.5" font-weight="bold" letter-spacing="3" text-anchor="middle" opacity=".4">MADE IN KYOTO // PING 1998</text>',
        '<text x="180" y="780" fill="#ffffff" font-family="monospace" font-size="11" font-weight="bold" opacity=".45">MAIN-BUS [16-BIT]</text>',
        '<text x="800" y="770" fill="#ffffff" font-family="monospace" font-size="10.5" font-weight="bold" opacity=".5">AUDIO / STEREO</text>',
        '<g stroke="#ffffff" stroke-width="1.8" opacity=".45"><path d="M 88 88 L 112 88 M 100 76 L 100 100"/><circle cx="100" cy="88" r="6" fill="none"/></g>',
        '<g stroke="#ffffff" stroke-width="1.8" opacity=".45"><path d="M 912 88 L 936 88 M 924 76 L 924 100"/><circle cx="924" cy="88" r="6" fill="none"/></g>',
        '<g stroke="#ffffff" stroke-width="1.8" opacity=".45"><path d="M 88 924 L 112 924 M 100 912 L 100 936"/><circle cx="100" cy="924" r="6" fill="none"/></g>',
        '<g stroke="#ffffff" stroke-width="1.8" opacity=".45"><path d="M 912 924 L 936 924 M 924 912 L 924 936"/><circle cx="924" cy="924" r="6" fill="none"/></g>',
    ]
    elements.extend(silkscreen)
    pcb_content = "".join(elements)

    boss_list = []
    for bx, by in [(150, 150), (874, 150), (150, 874), (874, 874)]:
        boss_list.append(f'''
        <g transform="translate({bx} {by})">
          <circle cx="0" cy="0" r="44" fill="url(#boss_plastic)" stroke="#a855f7" stroke-width="3" stroke-opacity=".7"/>
          <circle cx="0" cy="0" r="42" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-opacity=".4"/>
          <circle cx="0" cy="0" r="28" fill="#130822"/>
          <circle cx="0" cy="0" r="26" fill="url(#brass)" stroke="#713f12" stroke-width="1.5"/>
          <circle cx="0" cy="0" r="18" fill="url(#screw_steel)" stroke="#475569" stroke-width="1.4"/>
          <path d="M -9 0 H 9 M 0 -9 V 9" stroke="#0f172a" stroke-width="3.5" stroke-linecap="round"/>
          <path d="M -8 1 H 8 M 1 -8 V 8" stroke="#ffffff" stroke-width="1.2" stroke-linecap="round" opacity=".6"/>
        </g>
        ''')
    bosses = "".join(boss_list)

    return f"""
<defs>{DEFS}
  <radialGradient id="case_bg" cx="50%" cy="42%" r="75%">
    <stop offset="0%" stop-color="#4c1d95"/>
    <stop offset="40%" stop-color="#3b0764"/>
    <stop offset="75%" stop-color="#240342"/>
    <stop offset="100%" stop-color="#140224"/>
  </radialGradient>
  <linearGradient id="pcb_sub" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#1e1238"/>
    <stop offset="50%" stop-color="#150c28"/>
    <stop offset="100%" stop-color="#0e071c"/>
  </linearGradient>
  <radialGradient id="frost_tint" cx="50%" cy="36%" r="80%">
    <stop offset="0%" stop-color="#9333ea" stop-opacity=".32"/>
    <stop offset="40%" stop-color="#7e22ce" stop-opacity=".52"/>
    <stop offset="75%" stop-color="#581c87" stop-opacity=".72"/>
    <stop offset="100%" stop-color="#3b0764" stop-opacity=".86"/>
  </radialGradient>
  <radialGradient id="gold_pad" cx="35%" cy="30%" r="70%">
    <stop offset="0%" stop-color="#fef08a"/>
    <stop offset="45%" stop-color="#f5c754"/>
    <stop offset="85%" stop-color="#ca8a04"/>
    <stop offset="100%" stop-color="#854d0e"/>
  </radialGradient>
  <linearGradient id="specular_sheen" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffffff" stop-opacity=".50"/>
    <stop offset="35%" stop-color="#ffffff" stop-opacity=".15"/>
    <stop offset="75%" stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="diagonal_glare" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ffffff" stop-opacity=".35"/>
    <stop offset="25%" stop-color="#e9d5ff" stop-opacity=".12"/>
    <stop offset="55%" stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="bounce_rim" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0%" stop-color="#e9d5ff" stop-opacity=".35"/>
    <stop offset="25%" stop-color="#c084fc" stop-opacity=".10"/>
    <stop offset="60%" stop-color="#c084fc" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="metal_can" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="30%" stop-color="#e2e8f0"/>
    <stop offset="70%" stop-color="#94a3b8"/>
    <stop offset="100%" stop-color="#475569"/>
  </linearGradient>
  <radialGradient id="cap_metal" cx="38%" cy="32%" r="62%">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="50%" stop-color="#cbd5e1"/>
    <stop offset="85%" stop-color="#64748b"/>
    <stop offset="100%" stop-color="#334155"/>
  </radialGradient>
  <radialGradient id="boss_plastic" cx="38%" cy="32%" r="65%">
    <stop offset="0%" stop-color="#c084fc" stop-opacity=".75"/>
    <stop offset="65%" stop-color="#7e22ce" stop-opacity=".88"/>
    <stop offset="100%" stop-color="#3b0764" stop-opacity=".96"/>
  </radialGradient>
  <radialGradient id="brass" cx="35%" cy="30%" r="65%">
    <stop offset="0%" stop-color="#fef08a"/>
    <stop offset="40%" stop-color="#eab308"/>
    <stop offset="80%" stop-color="#a16207"/>
    <stop offset="100%" stop-color="#713f12"/>
  </radialGradient>
  <linearGradient id="screw_steel" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="45%" stop-color="#94a3b8"/>
    <stop offset="75%" stop-color="#64748b"/>
    <stop offset="100%" stop-color="#334155"/>
  </linearGradient>
  <linearGradient id="glyph_face" x1="0" y1="282" x2="0" y2="742" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#ffffff"/>
    <stop offset="55%" stop-color="#ffffff"/>
    <stop offset="100%" stop-color="#e8ecf8"/>
  </linearGradient>
  <filter id="case_glyph_shadow" x="-30%" y="-30%" width="160%" height="180%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="18"/>
    <feOffset dx="0" dy="20" result="offsetblur"/>
    <feFlood flood-color="#0a0214" flood-opacity=".9"/>
    <feComposite in2="offsetblur" operator="in"/>
  </filter>
  <filter id="case_glyph_ao" x="-10%" y="-10%" width="120%" height="130%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="5"/>
    <feOffset dx="0" dy="5" result="offsetblur"/>
    <feFlood flood-color="#140624" flood-opacity=".95"/>
    <feComposite in2="offsetblur" operator="in"/>
  </filter>
  <clipPath id="pcb_clip">
    <rect x="44" y="44" width="936" height="936" rx="216"/>
  </clipPath>
</defs>
<g clip-path="url(#sq)">
  <rect width="{S}" height="{S}" fill="url(#case_bg)"/>
  <g stroke="#ffffff" stroke-width="1.6" stroke-opacity=".07" fill="none">
    <line x1="256" y1="44" x2="256" y2="980"/>
    <line x1="512" y1="44" x2="512" y2="980"/>
    <line x1="768" y1="44" x2="768" y2="980"/>
    <line x1="44" y1="256" x2="980" y2="256"/>
    <line x1="44" y1="512" x2="980" y2="512"/>
    <line x1="44" y1="768" x2="980" y2="768"/>
    <circle cx="512" cy="512" r="95" stroke-width="1.2"/>
  </g>
  <g clip-path="url(#pcb_clip)">
    <rect x="44" y="44" width="936" height="936" fill="url(#pcb_sub)"/>
    {pcb_content}
  </g>
  {bosses}
  <rect width="{S}" height="{S}" fill="url(#frost_tint)"/>
  <text x="892" y="218" fill="#ffffff" font-family="sans-serif" font-size="9" font-weight="bold" opacity=".22" text-anchor="middle">&gt;PC&lt;</text>
  <g filter="url(#case_glyph_shadow)">{glyph("#000000")}</g>
  <g filter="url(#case_glyph_ao)">{glyph("#000000")}</g>
  {glyph("url(#glyph_face)")}
  <path d="M 50 250 C 70 120 160 60 320 48 C 500 36 680 50 820 110 C 660 85 450 80 300 115 C 160 150 90 220 50 320 Z" fill="url(#specular_sheen)"/>
  <path d="M 56 46 C 220 46 46 220 46 390 L 46 270 C 46 140 140 46 270 46 Z" fill="url(#diagonal_glare)"/>
  <rect x="44" y="800" width="936" height="180" rx="100" fill="url(#bounce_rim)"/>
  <rect x="42" y="42" width="940" height="940" rx="218" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-opacity=".22"/>
  <rect x="48" y="48" width="928" height="928" rx="212" fill="none" stroke="#000000" stroke-width="2.2" stroke-opacity=".4"/>
  {RIM}
</g>
"""


styled = {
    "neon": neon,
    "gummy": gummy,
    "fluted": fluted,
    "chrome": chrome,
    "sketch": sketch,
    "pixel": pixel,
    "cleartech": cleartech,
}

# pixel art is scaled with nearest-neighbour wherever the size is a whole multiple of its grid,
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
    """recompress the rendered png losslessly and build the .ico from it."""
    path = OUT / f"{name}.png"
    png = Image.open(path).convert("RGBA")
    png.save(path, optimize=True)
    frames = [shrink(png, name, s) for s in ICO_SIZES]
    frames[-1].save(OUT / f"{name}.ico", sizes=[f.size for f in frames], append_images=frames[:-1])


def preview(names, path, per_row=4):
    """large tile plus 48/32/16px thumbnails for each variant, on a dark background."""
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
    preview(list(styled), HERE / "preview-styled.png", per_row=4)
