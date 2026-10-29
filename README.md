# Crimson Wedding Grade · 绛红喜韵

[English](README.md) | [简体中文](README.zh-CN.md)

**Crimson Wedding Grade** (`crimson-wedding-grade`) is a specialized Claude Code skill and automated RAW color grading pipeline for wedding and bridal portrait photography, distilled from real-world Fuji X-T2 RAW post-production within [Lucarne](https://lucarne.app).

It achieves a refined, celebratory painterly aesthetic: deep, noble crimson wedding reds without fluorescent orange or fuchsia cast, creamy skin tones with subtle golden warmth, rich contrast without muddiness, and an objective colorimetric target driven by CIE L\*a\*b\* science.

---

## Aesthetic Vision & Color Science

Traditional digital wedding processing often struggles with two extremes: either reds become oversaturated fluorescent orange/fuchsia, or de-saturating them causes the entire image to look drab, muddy, and lifeless.

**Crimson Wedding Grade** solves this through precise colorimetric convergence and optical tonal separation:

1. **Noble Crimson Wedding Red (绛红)**:
   - **Target CIE L\*a\*b\***: $L^* \in [32, 38], a^* \in [+35, +42], b^* \in [+25, +30]$.
   - **Strict Hue Angle**: Constrained within **$36.5^\circ \sim 38.5^\circ$**.
   - Preserves traditional Chinese celebratory dignity while avoiding garish neon reds.
2. **Creamy Bridal Skin Tone**:
   - **Median Luminance**: Target facial skin median $L^* \in [0.61, 0.65]$.
   - Highlights retain delicate golden-amber warmth without blown-out flat whites.
3. **Painterly Filmic Texture**:
   - High rendering contrast (1.28) and local micro-contrast (+16 clarity) paired with fine film grain (level 5) and subtle vignette (-12).
   - Resolves sharpness and depth without relying on artificial HDR haloing.

---

## Key Features

- 🎨 **Canonical Recipe**: 90-operation baseline JSON controlling exposure, tone curves, split-toning, HSL color balance, detail, and optical corrections.
- 🔬 **Objective LAB Color Matching**: Scripted NumPy analyzer (`measure_lab.py`) comparing image regions and hue angles against target color standards instead of subjective visual guesswork.
- 🛡️ **Adaptive Lighting Calibration**:
  - **Wedding Details / Still Life**: De-yellowing and red luminance suppression for lacquer boxes, wedding vows, and gold-foil elements.
  - **Outdoor Backlit / Veil Recovery**: Highlight compression (-38) and color temp cooling (4580K) preserving delicate lace textures.
  - **Indoor Ambient / Dim Makeup Rooms**: Wide ambient lifting (+38 shadows, +0.28 EV radial mask) before subject exposure balancing to avoid artificial "spotlight cutout" looks.
- 🤝 **Interactive Retouch Checkpoint**: Facial skin smoothing (micro-pore softening) and blemish/acne healing are **never hardcoded** into presets; the assistant interactively prompts the user for preferred intensity and treatment path.
- 🚀 **macOS Native Automation**:
  - `detect_faces.swift`: High-speed bounding box extraction using Apple Vision (`VNDetectFaceRectanglesRequest`).
  - Coordinate Normalizer: Translates Vision coordinates into Lucarne's long-edge-normalized radial gradient masks.
  - `build_sheets.py`: Generates multi-column overview sheets and 100% crop skin texture inspection strips.
- 📦 **Dual-Track Delivery**:
  - **Direct Delivery (8-bit JPG)**: Quality 98, sRGB for still-life details, wide decor shots, and non-retouch portraits.
  - **High-Dynamic Retouch (16-bit TIFF)**: Uncompressed 16-bit sRGB TIFFs (~137 MB each) for portrait shots requiring manual figure liquify or AI retouching in Photoshop / 像素蛋糕.

---

## Directory Structure

```
crimson-wedding-grade/
├── SKILL.md                          # Claude Code Skill entrypoint & workflow protocol
├── README.md                         # English documentation
├── README.zh-CN.md                   # Chinese documentation
├── LICENSE                           # MIT License
├── references/
│   ├── crimson_baseline_recipe.json  # Complete 90-operation Lucarne baseline JSON
│   ├── color_science_and_lab.md      # Target LAB values, hue angles & grading science
│   └── lucarne_cli_reference.md      # Lucarne CLI RPC syntax, proto3 schemas & gotchas
└── scripts/
    ├── detect_faces.swift            # Native Apple Vision face detector (Swift)
    ├── apply_grade.py                # Batch grading & local mask injection CLI
    ├── measure_lab.py                # CIE L*a*b* & luminance objective analyzer
    └── build_sheets.py               # Review contact sheet and 100% skin strip generator
```

---

## Installation & Setup

### 1. Requirements

- macOS 13+ (Ventura, Sonoma, Sequoia)
- [Lucarne](https://lucarne.app) 1.7.0+ installed at `/Applications/Lucarne.app`
- Python 3.9+ with `Pillow` and `numpy`
- Swift command-line tools (`swiftc` bundled with Xcode Command Line Tools)

### 2. Install as a Claude Code Skill

Clone this repository into your local agents skills directory and symlink to `~/.claude/skills/`:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/tianshuo886/crimson-wedding-grade.git ~/.agents/skills/crimson-wedding-grade
ln -s ~/.agents/skills/crimson-wedding-grade ~/.claude/skills/crimson-wedding-grade
```

---

## Usage in Claude Code

Once installed, Claude Code automatically recognizes the skill when you work with wedding photos or Fuji RAW files in Lucarne.

### Natural Language Invocations

You can trigger the workflow simply by asking Claude:

- *"Apply Crimson Wedding Grade to this set of photos in Lucarne."*
- *"使用「绛红喜韵」调色管线处理这批婚礼 RAW 照片。"*
- *"/crimson-wedding-grade"*

### Interactive Workflow Execution

1. **Environment Check**: Confirms Lucarne catalog access and toolchain availability.
2. **Interactive Checkpoint**: Claude prompts for facial smoothing level (Light / Medium / None) and blemish treatment path.
3. **Virtual Copy Duplication**: Creates non-destructive virtual copies for all source photos.
4. **Baseline Ingestion**: Applies the 90-operation `crimson_baseline_recipe.json`.
5. **Adaptive Scene Tuning**: Classifies photos into Still-life, Backlit, or Dim Room and applies calibrated adjustments.
6. **Face Exposure Normalization**: Analyzes face skin luminance and balances subjects toward median $L^* = 0.61 \sim 0.65$.
7. **Contact Sheet Review**: Builds `00_总览.jpg` and `01_皮肤100%_检查.jpg` for user approval.
8. **Dual-Track Export**: Automatically exports 16-bit TIFFs for retouching and 8-bit JPEGs for final delivery.

---

## Standalone CLI Usage

The scripts can also be used independently of Claude:

```bash
# Set catalog environment
export LUCARNE_CATALOG="$HOME/Library/Application Support/Lucarne/Catalogs/Library.lucarnecatalog"

# Apply baseline and scene adaptation to document ID 105
python3 scripts/apply_grade.py 105 --scene detail

# Measure CIE L*a*b* values of a rendered image
python3 scripts/measure_lab.py rendered_preview.jpg
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
