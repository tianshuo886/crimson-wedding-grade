#!/usr/bin/env python3
"""Batch apply 'Crimson Wedding Grade' (绛红喜韵) color grading to Lucarne catalog versions."""
import argparse
import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REF_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "references")
BASELINE_JSON = os.path.join(REF_DIR, "crimson_baseline_recipe.json")
DETECT_SWIFT = os.path.join(SCRIPT_DIR, "detect_faces.swift")

LC = os.environ.get("LUCARNE_CLI", "/Applications/Lucarne.app/Contents/Helpers/lucarne")
CAT = os.environ.get(
    "LUCARNE_CATALOG",
    os.path.expanduser("~/Library/Application Support/Lucarne/Catalogs/Library.lucarnecatalog")
)
ENV = dict(os.environ, LUCARNE_CATALOG=CAT)


def run_lc(args, check=True):
    r = subprocess.run([LC] + args, capture_output=True, text=True, env=ENV)
    if check and r.returncode != 0:
        raise RuntimeError(f"Lucarne command failed: {args}\n{r.stderr.strip()}")
    return r.stdout.strip()


def get_doc(doc_id):
    out = run_lc(["doc", "get", str(doc_id)])
    lines = out.split("\n", 1)
    if len(lines) > 1:
        return json.loads(lines[1])
    return json.loads(out)


def apply_ops(doc_id, ops):
    tmp_path = f"/tmp/_lc_ops_{doc_id}.json"
    with open(tmp_path, "w") as f:
        json.dump(ops, f)
    run_lc(["doc", "apply", str(doc_id), f"@{tmp_path}"])
    if os.path.exists(tmp_path):
        os.remove(tmp_path)


def sp(adj, param, val):
    val_obj = {"number": val} if isinstance(val, (int, float)) else {"enumeration": str(val)}
    return {"setParameter": {"adjustment": adj, "parameter": param, "value": val_obj}}


def get_scene_ops(scene):
    ops = []
    if scene == "detail":
        # Crimson protection & de-yellowing for red lacquer / gold foil
        ops.extend([
            sp("white_balance", "temperature_k", 4580),
            sp("white_balance", "tint", -2),
            sp("hsl", "hue_red", -3),
            sp("hsl", "saturation_red", -8),
            sp("hsl", "brightness_red", -23),
            sp("hsl", "hue_orange", -2),
            sp("hsl", "saturation_orange", -6),
            sp("hsl", "saturation_yellow", -14),
            sp("hsl", "brightness_yellow", 0),
            sp("color_grading", "midtones_saturation", 4),
            sp("color_grading", "highlights_saturation", 1),
        ])
    elif scene == "backlit":
        # Outdoor daylight / veil highlight recovery
        ops.extend([
            sp("white_balance", "temperature_k", 4580),
            sp("white_balance", "tint", -1),
            sp("exposure", "exposure_ev", -0.18),
            sp("tone", "highlights", -38),
            sp("tone", "contrast", 20),
            sp("hsl", "saturation_green", -2),
            sp("hsl", "saturation_yellow", -10),
            sp("color_grading", "midtones_saturation", 5),
        ])
    elif scene == "dim_room":
        # Ambient lift for indoor dark room
        ops.extend([
            sp("exposure", "exposure_ev", 0.10),
            sp("tone", "shadows", 38),
            sp("tone", "blacks", -4),
            sp("tone", "highlights", -64),
        ])
    return ops


def build_face_masks(faces_tsv_line, is_portrait, smooth_level):
    """
    smooth_level: 'none', 'light', 'medium'
    """
    if smooth_level == "none":
        return []

    settings = {"texture": -12, "clarity": -2, "shadows": 2, "exposure": 0.02}
    if smooth_level == "medium":
        settings = {"texture": -18, "clarity": -4, "shadows": 2, "exposure": 0.02}

    wx = 4000.0 / 6000.0 if is_portrait else 1.0
    hy = 1.0 if is_portrait else 4000.0 / 6000.0

    la_ops = []
    boxes = [b.strip() for b in faces_tsv_line.split(";") if b.strip()]
    for i, b_str in enumerate(boxes):
        parts = [float(v) for v in b_str.split(",")]
        if len(parts) != 4:
            continue
        x, y, w, h = parts
        cx = x + w / 2.0
        cy = 1.0 - (y + h / 2.0)
        rx = round(0.72 * w * wx, 4)
        ry = round(0.88 * h * hy, 4)

        la_ops.append({
            "insertLocalAdjustment": {
                "index": i,
                "localAdjustment": {
                    "id": f"skin{i}",
                    "name": f"Skin {i+1}",
                    "enabled": True,
                    "amount": 100,
                    "selection": {
                        "parts": [{
                            "mode": "SELECTION_MODE_ADD",
                            "radialGradient": {
                                "centre": {"x": round(cx, 4), "y": round(cy, 4)},
                                "radiusX": rx,
                                "radiusY": ry,
                                "rotation": 0,
                                "feather": 70
                            }
                        }]
                    },
                    "settings": dict(settings)
                }
            }
        })
    return la_ops


def main():
    parser = argparse.ArgumentParser(description="Apply Crimson Wedding Grade pipeline.")
    parser.add_argument("doc_id", help="Lucarne document version ID")
    parser.add_argument("--scene", choices=["portrait", "detail", "backlit", "dim_room"],
                        default="portrait", help="Scene type adaptation")
    parser.add_argument("--smooth", choices=["none", "light", "medium"], default="none",
                        help="Face smoothing level (defaults to none; interactive confirm needed)")
    parser.add_argument("--faces", help="Vision bbox string 'x,y,w,h;...'")
    parser.add_argument("--portrait-orient", action="store_true", help="Set if photo is portrait orientation")
    args = parser.parse_args()

    # 1. Apply Baseline Recipe
    with open(BASELINE_JSON, "r") as f:
        base_ops = json.load(f)
    print(f"Applying Crimson Wedding baseline ({len(base_ops)} ops) to doc {args.doc_id}...")
    apply_ops(args.doc_id, base_ops)

    # 2. Apply Scene Overrides
    scene_ops = get_scene_ops(args.scene)
    if scene_ops:
        print(f"Applying scene '{args.scene}' adaptation ({len(scene_ops)} ops)...")
        apply_ops(args.doc_id, scene_ops)

    # 3. Apply Face Smoothing Masks if requested
    if args.smooth != "none" and args.faces:
        face_ops = build_face_masks(args.faces, args.portrait_orient, args.smooth)
        if face_ops:
            print(f"Injecting {len(face_ops)} facial mask(s) at level '{args.smooth}'...")
            apply_ops(args.doc_id, face_ops)

    print(f"Done grading doc {args.doc_id}.")


if __name__ == "__main__":
    main()
