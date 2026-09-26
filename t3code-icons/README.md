# t3code-icons

Replacement icons for [T3 Code](https://github.com/pingdotgg/t3code), made because the nightly build's icon was a bit much.

![preview](preview.png)

| | Variant | Vibe |
|---|---|---|
| <img src="icons/graphite.png" width="48"> | `graphite` | Charcoal tile, silver T3. The clean one. |
| <img src="icons/midnight.png" width="48"> | `midnight` | Navy-black with a small crescent, a quiet nod to "nightly". |
| <img src="icons/accent.png" width="48"> | `accent` | Near-black, white T, violet 3. |
| <img src="icons/coral.png" width="48"> | `coral` | Flat Claude coral and ivory, made to sit next to the Claude app in the taskbar. |

Each variant in [`icons/`](icons) comes as `.svg` (source), `.png` (1024px) and `.ico` (16–256px, for Windows).

## Using one on Windows

Right-click the T3 Code shortcut → **Properties** → **Change Icon…** → pick the `.ico`. For a pinned taskbar icon, change the shortcut in
`%APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar`.

Or from PowerShell:

```powershell
$lnk = (New-Object -ComObject WScript.Shell).CreateShortcut("$env:USERPROFILE\Desktop\T3 Code.lnk")
$lnk.IconLocation = "C:\path\to\midnight.ico,0"
$lnk.Save()
```

This only changes shortcuts. The running app's window and unpinned taskbar button still use the icon built into the executable.

## Regenerating

The glyph is hand-drawn as SVG paths in [`gen.py`](gen.py); each variant is just a background and fill on top of it. Edit colours there and run:

```sh
pip install pillow
python gen.py            # all variants (or: python gen.py midnight)
```

It renders through headless Chrome, so set `CHROME=/path/to/chrome` if it isn't at the default Windows location.
