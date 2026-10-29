#!/usr/bin/env python3
"""Measure objective LAB color and luminance metrics for 06A grading verification."""
import argparse
import sys
import numpy as np
from PIL import Image


def rgb_to_lab(a):
    """Convert RGB float [0, 1] to CIE L*a*b*."""
    with np.errstate(all="ignore"):
        a = np.clip(a, 0.0, 1.0)
        # sRGB companding to linear
        lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
        M = np.array([
            [0.4124, 0.3576, 0.1805],
            [0.2126, 0.7152, 0.0722],
            [0.0193, 0.1192, 0.9505]
        ], dtype=np.float32)
        xyz = lin @ M.T
        # Reference D65 white point
        wp = np.array([0.95047, 1.0, 1.08883], dtype=np.float32)
        xyz = np.clip(xyz / wp, 1e-6, 10.0)
        # f(t)
        f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16.0 / 116.0)
        L = 116.0 * f[..., 1] - 16.0
        A = 500.0 * (f[..., 0] - f[..., 1])
        B = 200.0 * (f[..., 1] - f[..., 2])
    return L, A, B


def measure_image(path, face_coords=None):
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im, dtype=np.float32) / 255.0
    H, W = arr.shape[:2]
    m = arr.reshape(-1, 3)

    # Whole frame Luminance
    lum = 0.2126 * m[:, 0] + 0.7152 * m[:, 1] + 0.0722 * m[:, 2]
    clip_pct = float((lum > 0.97).mean() * 100)
    black_pct = float((lum < 0.02).mean() * 100)

    # Whole frame LAB
    L, A, B = rgb_to_lab(m)
    whole_L = float(L.mean())
    whole_A = float(A.mean())
    whole_B = float(B.mean())
    whole_C = float(np.hypot(A, B).mean())

    # Red cluster
    mx = m.max(1)
    mn = m.min(1)
    sat = (mx - mn) / np.maximum(mx, 1e-4)
    red_sel = (m[:, 0] == mx) & (m[:, 0] > 0.15) & (sat > 0.45)
    red_count = int(red_sel.sum())

    red_metrics = {}
    if red_count > 100:
        Lr, Ar, Br = L[red_sel], A[red_sel], B[red_sel]
        Cr = np.hypot(Ar, Br)
        hue_rad = np.arctan2(np.median(Br), np.median(Ar))
        hue_deg = float(np.degrees(hue_rad)) % 360
        red_metrics = {
            "L": float(np.median(Lr)),
            "C": float(np.median(Cr)),
            "hue": hue_deg,
            "count": red_count
        }

    # Skin tone measurements if face coordinates provided
    skin_metrics = []
    if face_coords:
        for (cx, cy) in face_coords:
            px, py = int(cx * W), int(cy * H)
            r = max(8, int(min(W, H) * 0.033))
            patch = arr[max(0, py - r):min(H, py + r), max(0, px - r):min(W, px + r)].reshape(-1, 3)
            if len(patch) == 0:
                continue
            p_mx = patch.max(1)
            p_mn = patch.min(1)
            p_sat = (p_mx - p_mn) / np.maximum(p_mx, 1e-4)
            skin_sel = (p_mx > 0.30) & (patch[:, 0] >= patch[:, 1] - 0.02) & (p_sat > 0.08)
            skin_px = patch[skin_sel] if skin_sel.sum() > 40 else patch
            s_lum = 0.2126 * skin_px[:, 0] + 0.7152 * skin_px[:, 1] + 0.0722 * skin_px[:, 2]
            skin_metrics.append({
                "median_L": float(np.median(s_lum)),
                "p90_L": float(np.percentile(s_lum, 90)),
                "mean_RGB": [round(float(v), 2) for v in skin_px.mean(0)]
            })

    return {
        "file": path,
        "size": [W, H],
        "whole_L": round(whole_L, 1),
        "whole_A": round(whole_A, 1),
        "whole_B": round(whole_B, 1),
        "whole_C": round(whole_C, 1),
        "clip_pct": round(clip_pct, 2),
        "black_pct": round(black_pct, 2),
        "red": red_metrics,
        "faces": skin_metrics
    }


def main():
    parser = argparse.ArgumentParser(description="Measure color & tone metrics.")
    parser.add_argument("images", nargs="+", help="Image paths")
    parser.add_argument("--faces", help="Comma-separated cx,cy pairs, e.g. '0.42,0.54;0.82,0.26'")
    args = parser.parse_args()

    face_coords = None
    if args.faces:
        face_coords = [[float(v) for v in pair.split(",")] for pair in args.faces.split(";")]

    print(f"{'File':20} {'Whole L*':>9} {'a*':>6} {'b*':>6} {'Red L*':>7} {'Red C*':>7} {'Red Hue':>8} {'Face L':>7} {'Clip%':>6}")
    print("-" * 84)

    for p in args.images:
        res = measure_image(p, face_coords)
        red_str_l = f"{res['red'].get('L', 0):.1f}" if res['red'] else "N/A"
        red_str_c = f"{res['red'].get('C', 0):.1f}" if res['red'] else "N/A"
        red_str_h = f"{res['red'].get('hue', 0):.1f}°" if res['red'] else "N/A"
        face_l = f"{res['faces'][0]['median_L']:.2f}" if res['faces'] else "N/A"
        print(f"{p.split('/')[-1]:20} {res['whole_L']:9.1f} {res['whole_A']:6.1f} {res['whole_B']:6.1f} "
              f"{red_str_l:>7} {red_str_c:>7} {red_str_h:>8} {face_l:>7} {res['clip_pct']:5.2f}%")


if __name__ == "__main__":
    main()
