#!/usr/bin/env python3
"""Build preview contact sheets and comparison strips for review."""
import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
if not os.path.exists(FONT):
    FONT = "/System/Library/Fonts/STHeiti Light.ttc"


def build_grid(image_paths, titles, out_path, cols=6, tile_size=(430, 430), gap=10, label_h=30):
    rows = (len(image_paths) + cols - 1) // cols
    cw, ch = tile_size
    w = cols * cw + (cols + 1) * gap
    h = rows * (ch + label_h) + (rows + 1) * gap

    can = Image.new("RGB", (w, h), (16, 16, 16))
    d = ImageDraw.Draw(can)
    fb = ImageFont.truetype(FONT, 20)
    fs = ImageFont.truetype(FONT, 16)

    for i, p in enumerate(image_paths):
        im = Image.open(p).convert("RGB")
        im.thumbnail((cw, ch), Image.LANCZOS)
        r, c = divmod(i, cols)
        x = gap + c * (cw + gap)
        y = gap + r * (ch + label_h + gap)
        # Center image within tile box
        can.paste(im, (x + (cw - im.width) // 2, y + (ch - im.height) // 2))

        title = titles[i] if i < len(titles) else os.path.basename(p)
        parts = title.split(" ", 1)
        stem = parts[0]
        desc = parts[1] if len(parts) > 1 else ""
        d.text((x + 4, y + ch + 4), stem, font=fb, fill=(240, 240, 240))
        if desc:
            d.text((x + 66, y + ch + 6), desc, font=fs, fill=(150, 150, 150))

    can.save(out_path, quality=92)
    print(f"Saved grid sheet to {out_path} ({w}x{h})")


def build_strip(items, out_path, title, subtitle="", tile_max=(640, 640)):
    """items: list of (label, image_path)"""
    ims = []
    for cap, p in items:
        im = Image.open(p).convert("RGB")
        im.thumbnail(tile_max, Image.LANCZOS)
        ims.append((cap, im))

    w = sum(im.width for _, im in ims) + 8 * (len(ims) - 1)
    h = max(im.height for _, im in ims)
    top_h = 118 if subtitle else 80
    can = Image.new("RGB", (max(w, 900), h + top_h), (16, 16, 16))
    d = ImageDraw.Draw(can)

    ft = ImageFont.truetype(FONT, 26)
    fs = ImageFont.truetype(FONT, 16)
    fb = ImageFont.truetype(FONT, 20)

    d.text((14, 14), title, font=ft, fill=(240, 240, 240))
    if subtitle:
        d.text((14, 52), subtitle, font=fs, fill=(150, 150, 150))

    x = 0
    y_img = top_h - 38
    for cap, im in ims:
        can.paste(im, (x, y_img))
        d.text((x + 6, y_img + im.height + 4), cap, font=fb, fill=(220, 220, 220))
        x += im.width + 8

    can.save(out_path, quality=93)
    print(f"Saved comparison strip to {out_path} ({can.size[0]}x{can.size[1]})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build preview sheets.")
    parser.add_argument("--mode", choices=["grid", "strip"], default="grid")
    parser.add_argument("--out", required=True, help="Output jpg path")
    parser.add_argument("--title", default="Review Sheet")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("images", nargs="+", help="Input images or label:image pairs")
    args = parser.parse_args()

    if args.mode == "grid":
        titles = [os.path.basename(p)[:8] for p in args.images]
        build_grid(args.images, titles, args.out)
    else:
        items = []
        for s in args.images:
            if ":" in s:
                lbl, p = s.split(":", 1)
            else:
                lbl, p = os.path.basename(s)[:8], s
            items.append((lbl, p))
        build_strip(items, args.out, args.title, args.subtitle)
