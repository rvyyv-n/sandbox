# t3code-icons

replacement icons for [t3 code](https://github.com/pingdotgg/t3code), made because the nightly build's icon was a bit much.

![preview](preview.png)

| | variant | vibe |
|---|---|---|
| <img src="icons/graphite.png" width="40"> | `graphite` | charcoal tile, silver t3. the clean one. |
| <img src="icons/midnight.png" width="40"> | `midnight` | navy-black with a small crescent, a quiet nod to "nightly". |
| <img src="icons/accent.png" width="40"> | `accent` | near-black, white t, violet 3. |
| <img src="icons/coral.png" width="40"> | `coral` | flat claude coral and ivory, made to sit next to the claude app. |

## stylised set

louder alternates in the spirit of arc's app icons. each one is a different material.

![stylised preview](preview-styled.png)

| | variant | vibe |
|---|---|---|
| <img src="icons/neon.png" width="40"> | `neon` | pink and cyan neon tubing on a dark brick wall. |
| <img src="icons/gummy.png" width="40"> | `gummy` | glossy raspberry jelly on a pastel tile. |
| <img src="icons/fluted.png" width="40"> | `fluted` | sunset gradient behind ribbed fluted glass. |
| <img src="icons/chrome.png" width="40"> | `chrome` | y2k liquid chrome with sparkles. |
| <img src="icons/sketch.png" width="40"> | `sketch` | ballpoint doodle on graph paper. |
| <img src="icons/pixel.png" width="40"> | `pixel` | 32×32 pixel art, so it's pixel-perfect at 32px. |

each variant in [`icons/`](icons) comes as `.svg` (source), `.png` (1024px) and `.ico` (16–256px, for windows).

## using one on windows

right-click the t3 code shortcut, open **properties**, click **change icon…** and pick the `.ico`. for a pinned taskbar icon, change the shortcut in `%APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar`.

or from powershell:

```powershell
$lnk = (New-Object -ComObject WScript.Shell).CreateShortcut("$env:USERPROFILE\Desktop\T3 Code.lnk")
$lnk.IconLocation = "C:\path\to\midnight.ico,0"
$lnk.Save()
```

this only changes shortcuts. the running app's window and unpinned taskbar button still use the icon built into the executable.

## regenerating

the glyph is hand-drawn as svg paths in [`gen.py`](gen.py). the core variants are just a background and fill on top of it. the stylised set gets its materials from svg filters (lighting, displacement and noise); the pixel icon is rasterised from the same glyph. edit them there and run:

```sh
pip install pillow
python gen.py            # all variants (or: python gen.py midnight)
```

it renders through headless chrome, so set `CHROME=/path/to/chrome` if it isn't at the default windows location.
