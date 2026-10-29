"""Preset operations for family portrait grades."""

def sp(adj, param, val):
    val_obj = {"number": val} if isinstance(val, (int, float)) else {"enumeration": str(val)}
    return {"setParameter": {"adjustment": adj, "parameter": param, "value": val_obj}}

FAMILY_PRESETS = {
    "A": [  # A_暖家
        sp("white_balance", "temperature_k", 5150), sp("white_balance", "tint", 2),
        sp("exposure", "exposure_ev", 0.25), sp("rendering", "contrast", 1.10),
        sp("tone", "highlights", -34), sp("tone", "shadows", 30), sp("tone", "whites", 6),
        sp("tone", "blacks", -2), sp("tone", "contrast", 6),
        sp("color_adjust", "saturation", -4), sp("color_adjust", "vibrance", 8),
        sp("detail", "clarity", 5), sp("detail", "texture", -2), sp("detail", "sharpen_amount", 30),
        sp("vignette", "amount", -5),
        sp("color_grading", "midtones_hue", 38), sp("color_grading", "midtones_saturation", 8), sp("color_grading", "midtones_luminance", 3),
        sp("color_grading", "highlights_hue", 45), sp("color_grading", "highlights_saturation", 2),
        sp("color_grading", "shadows_hue", 20), sp("color_grading", "shadows_saturation", 2),
        sp("hsl", "hue_red", 4), sp("hsl", "saturation_red", -5), sp("hsl", "brightness_red", 0),
        sp("hsl", "hue_orange", -2), sp("hsl", "saturation_orange", -8), sp("hsl", "brightness_orange", 10),
        sp("hsl", "hue_yellow", 0), sp("hsl", "saturation_yellow", -6), sp("hsl", "brightness_yellow", 8)
    ],
    "B": [  # B_胶片暖金
        sp("white_balance", "temperature_k", 5600), sp("white_balance", "tint", 6),
        sp("exposure", "exposure_ev", 0.24), sp("rendering", "contrast", 1.06),
        sp("tone", "highlights", -44), sp("tone", "shadows", 40), sp("tone", "whites", 0),
        sp("tone", "blacks", -10), sp("tone", "contrast", 4),
        sp("color_adjust", "saturation", 2), sp("color_adjust", "vibrance", 12),
        sp("detail", "clarity", 2), sp("detail", "texture", -4), sp("detail", "sharpen_amount", 28),
        sp("vignette", "amount", -12),
        sp("color_grading", "midtones_hue", 32), sp("color_grading", "midtones_saturation", 14), sp("color_grading", "midtones_luminance", 4),
        sp("color_grading", "highlights_hue", 50), sp("color_grading", "highlights_saturation", 7),
        sp("color_grading", "shadows_hue", 28), sp("color_grading", "shadows_saturation", 7),
        sp("hsl", "hue_red", 6), sp("hsl", "saturation_red", 0), sp("hsl", "brightness_red", 6),
        sp("hsl", "hue_orange", -2), sp("hsl", "saturation_orange", -2), sp("hsl", "brightness_orange", 16),
        sp("hsl", "hue_yellow", 0), sp("hsl", "saturation_yellow", -2), sp("hsl", "brightness_yellow", 14)
    ],
    "C": [  # C_清透自然
        sp("white_balance", "temperature_k", 4880), sp("white_balance", "tint", -2),
        sp("exposure", "exposure_ev", 0.30), sp("rendering", "contrast", 1.16),
        sp("tone", "highlights", -30), sp("tone", "shadows", 24), sp("tone", "whites", 10),
        sp("tone", "blacks", -4), sp("tone", "contrast", 12),
        sp("color_adjust", "saturation", -8), sp("color_adjust", "vibrance", 6),
        sp("detail", "clarity", 9), sp("detail", "texture", 0), sp("detail", "sharpen_amount", 32),
        sp("vignette", "amount", -2),
        sp("color_grading", "midtones_hue", 45), sp("color_grading", "midtones_saturation", 2), sp("color_grading", "midtones_luminance", 1),
        sp("color_grading", "highlights_hue", 45), sp("color_grading", "highlights_saturation", 1),
        sp("color_grading", "shadows_hue", 20), sp("color_grading", "shadows_saturation", 1),
        sp("hsl", "hue_red", 2), sp("hsl", "saturation_red", -8), sp("hsl", "brightness_red", 0),
        sp("hsl", "hue_orange", -4), sp("hsl", "saturation_orange", -12), sp("hsl", "brightness_orange", 6),
        sp("hsl", "hue_yellow", 0), sp("hsl", "saturation_yellow", -12), sp("hsl", "brightness_yellow", 4)
    ],
    "D": [  # D_低饱和暖灰
        sp("white_balance", "temperature_k", 5300), sp("white_balance", "tint", 1),
        sp("exposure", "exposure_ev", 0.26), sp("rendering", "contrast", 1.02),
        sp("tone", "highlights", -44), sp("tone", "shadows", 36), sp("tone", "whites", 2),
        sp("tone", "blacks", -8), sp("tone", "contrast", 0),
        sp("color_adjust", "saturation", -26), sp("color_adjust", "vibrance", 2),
        sp("detail", "clarity", 3), sp("detail", "texture", -8), sp("detail", "sharpen_amount", 26),
        sp("vignette", "amount", -4),
        sp("color_grading", "midtones_hue", 35), sp("color_grading", "midtones_saturation", 4), sp("color_grading", "midtones_luminance", 2),
        sp("color_grading", "highlights_hue", 45), sp("color_grading", "highlights_saturation", 2),
        sp("color_grading", "shadows_hue", 22), sp("color_grading", "shadows_saturation", 3),
        sp("hsl", "hue_red", 4), sp("hsl", "saturation_red", -18), sp("hsl", "brightness_red", 0),
        sp("hsl", "hue_orange", -2), sp("hsl", "saturation_orange", -18), sp("hsl", "brightness_orange", 4),
        sp("hsl", "hue_yellow", 0), sp("hsl", "saturation_yellow", -14), sp("hsl", "brightness_yellow", 2)
    ]
}
