#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""git external diff driver for images.

Args: path old-file old-hex old-mode new-file new-hex new-mode
Images are drawn on /dev/tty to bypass the pager.
"""
import filecmp
import html
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from string import Template

TEMPLATE = Path(__file__).resolve().with_suffix(".html")
OUT_ROOT = Path(tempfile.gettempdir()) / "git-image-dir"


def show(path):
    with open("/dev/tty", "wb") as tty:
        subprocess.run(["chafa", "-f", "kitty", str(path)], stdout=tty)


def render(path, old=None, new=None):
    """Render image-diff.html into a fresh dir and return a clickable terminal link."""
    OUT_ROOT.mkdir(exist_ok=True)
    out_dir = Path(tempfile.mkdtemp(dir=OUT_ROOT))
    figures = []
    names = {}
    # both sides present: render only the fade slider
    fade = old is not None and new is not None
    # git's temp files vanish after the diff, so copy images next to the html
    for label, src in (("Old", old), ("New", new)):
        if src is None:
            continue
        name = f"{label.lower()}{Path(src).suffix or Path(path).suffix}"
        shutil.copyfile(src, out_dir / name)
        names[label] = name
        figures.append(f"<figure><figcaption>{label}</figcaption><img src=\"{name}\"></figure>")
    if fade:
        figures = [
            '<section id="fade">'
            '<input type="range" min="0" max="100" value="50" aria-label="Fade between old and new">'
            f'<div class="stack"><img src="{names["Old"]}"><img src="{names["New"]}"></div>'
            '</section>'
        ]
    page = out_dir / "index.html"
    page.write_text(Template(TEMPLATE.read_text()).substitute(
        path=html.escape(path), figures="\n".join(figures)))
    # OSC 8 hyperlink: the file:// URL stays hidden behind the label
    return f"\033]8;;{page.as_uri()}\033\\open in browser\033]8;;\033\\"


def main():
    path, old, new = sys.argv[1], sys.argv[2], sys.argv[5]

    if old == "/dev/null":
        print(f"{path}: image added ({render(path, new=new)})")
        show(new)
    elif new == "/dev/null":
        print(f"{path}: image removed ({render(path, old=old)})")
        show(old)
    elif filecmp.cmp(old, new, shallow=False):
        print(f"{path}: images are identical")
    else:
        print(f"{path}: image changed ({render(path, old=old, new=new)})")
        show(new)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"image-diff: {e}", file=sys.stderr)
    sys.exit(0)
