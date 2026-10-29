# Crimson Wedding Grade · 绛红喜韵

[English](README.md) | [简体中文](README.zh-CN.md)

**Crimson Wedding Grade** (`crimson-wedding-grade`) is a specialized Claude Code skill and automated RAW color grading pipeline for wedding and portrait photography, distilled from real-world Fuji X-T2 RAW post-production within [Lucarne](https://lucarne.app).

It achieves a refined, celebratory painterly aesthetic: deep, noble crimson wedding reds without fluorescent orange or fuchsia cast, creamy skin tones with subtle golden warmth, rich contrast without muddiness, and an objective colorimetric target driven by CIE L\*a\*b\* science.

![Pipeline Architecture](docs/assets/01_pipeline_architecture_line_art.png)

---

## Real Photo Validation: Before vs After Comparisons

Moving away from subjective guesswork, this pipeline validates color through **real photo Before vs After comparisons** (100% focused on still life and scene decor, with zero exposed portraits):

### 1. Still-Life Details: Banishing Warm Tungsten Yellow and Fluorescent Orange
Still-life items such as red lacquer boxes, wedding vows, tea ceremonies, and floral bouquets often suffer from warm tungsten ambient light and digital red clipping, turning garish orange or dull mustard yellow. **Crimson Wedding Grade** cools the color temperature (4580K), suppresses red luminance (-23), and reduces yellow saturation (-14) to lock the red hue angle strictly at **$38.8^\circ$**, while gold foil shines with authentic, brilliant gold luster.

![Still-Life Before vs After](docs/assets/02_still_life_before_after.jpg)

### 2. Scene Backdrop Folds: Rich 06A Oil-Painting Depth
A direct crop from the top background of the master reference photo (DSCF0020), showing the three-dimensional gold double-happiness character (囍) and layered red velvet drapery. The camera standard file is flat and washed out; after 06A grading, velvet shadow luminance $L^*$ drops to 28~32, revealing dramatic three-dimensional folds, fine film grain, and rich 1.28 painterly contrast.

![Backdrop Details Before vs After](docs/assets/03_background_curtain_before_after.jpg)

### 3. Core Color Palette & Hue Angle Hard Constraint
Color grading is converted into verifiable colorimetric benchmarks:

![Color Science Swatches](docs/assets/04_color_science_swatches.jpg)

* **Noble Crimson (大漆绛红)**: $L^* 36.0, a^* +38.5, b^* +28.0$ · Hue angle $37.4^\circ$, deep, dignified ceremonial red.
* **Imperial Gold (龙凤纯金)**: $L^* 80.5, a^* +10.2, b^* +56.0$ · Pure gold foil reflection, neither green nor artificial orange.
* **Satin Cream (丝缎奶油)**: $L^* 63.5, a^* +15.5, b^* +18.0$ · Smooth golden highlights bridging skin and satin gown.
* **Deep Brocade (深宫锦缎)**: $L^* 28.0, a^* +32.0, b^* +20.0$ · Shadow curtain red holding depth without turning muddy.
* **Strict Hue Angle Hard Constraint**: Constrained strictly within **$36.5^\circ \sim 38.5^\circ$** (Noble Crimson), avoiding fuchsia ($< 32^\circ$) and neon orange ($> 43^\circ$).

---

## Industrial Dual-Engine Architecture: Color Science Meets AI Retouching

Color grading and facial retouching are fundamentally decoupled in imaging science, serving as complementary partners:

| Dimension | Upstream: Claude Code + Lucarne (`crimson-wedding-grade`) | Downstream: 像素蛋糕 (PixCake) / Photoshop |
| :--- | :--- | :--- |
| **Film Industry Role** | **DIT / Digital Image Technician & Chief Colorist** | **Senior Beauty Retoucher & High-End Finisher** |
| **Core Mission** | 14-bit RAW optical decoding, tonal grading, locking crimson hue angle, balancing ambient lighting ratios | Skeletal liquify, biometric high/low frequency smoothing, acne/blemish healing, wrinkle removal, **final cropping** |
| **Data Domain** | Raw sensor voltages, linear dynamic range, color matrices, still-life decor | Facial mesh topology, muscle flow, feature proportions, clothing fabric creases |
| **Output Deliverable**| **16-bit Uncompressed sRGB TIFF** (~137 MB each) + **8-bit JPG** | **Final Master Client Album** |

### Master Deliverables Policy
1. **Track A: Direct Delivery (8-bit JPG)**:
   * For: Still life details, wedding vows, lacquer boxes, wide venue shots.
   * Batch exported locally at quality 98; zero retouch credits required.
2. **Track B: High-Dynamic Retouch (16-bit TIFF) $\rightarrow$ 像素蛋糕 (PixCake)**:
   * For: Bride portraits, groom portraits, couple portraits.
   * **Master Version Policy**: Portraits undergo facial retouching, micro-smoothing, body contouring, and final re-cropping in 像素蛋糕 (PixCake); **the final client deliverables are the versions exported from PixCake**.

---

## Key Features

- 🎨 **Canonical Recipe**: 90-operation baseline JSON controlling exposure, tone curves, split-toning, HSL color balance, detail, and optical corrections.
- 🔬 **Objective LAB Color Matching**: Scripted NumPy analyzer (`measure_lab.py`) comparing image regions and hue angles against target color standards instead of subjective visual guesswork.
- 🛡️ **Adaptive Lighting Calibration**:
  - **Wedding Details / Still Life (`detail`)**: De-yellowing and red luminance suppression for lacquer boxes, wedding vows, and gold-foil elements.
  - **Outdoor Backlit / Veil Recovery (`backlit`)**: Highlight compression (-38) and color temp cooling (4580K) preserving delicate lace textures.
  - **Indoor Ambient / Dim Makeup Rooms (`dim_room`)**: Wide ambient lifting (+38 shadows, +0.28 EV radial mask) before subject exposure balancing to avoid artificial "spotlight cutout" looks.
- 🤝 **Interactive Retouch Checkpoint**: Facial skin smoothing (micro-pore softening) and blemish/acne healing are **never hardcoded** into presets; the assistant interactively prompts the user for preferred intensity and treatment path.
- 🚀 **macOS Native Automation**:
  - `detect_faces.swift`: High-speed bounding box extraction using Apple Vision (`VNDetectFaceRectanglesRequest`).
  - Coordinate Normalizer: Translates Vision coordinates into Lucarne's long-edge-normalized radial gradient masks.
  - `build_sheets.py`: Generates multi-column overview sheets and 100% crop skin texture inspection strips.

---

## Directory Structure

```
crimson-wedding-grade/
├── SKILL.md                          # Claude Code Skill entrypoint & workflow protocol
├── README.md                         # English documentation
├── README.zh-CN.md                   # Chinese documentation
├── LICENSE                           # MIT License
├── docs/
│   └── assets/                       # White line-art architecture diagram and Before/After comparisons
│       ├── 01_pipeline_architecture_line_art.png
│       ├── 02_still_life_before_after.jpg
│       ├── 03_background_curtain_before_after.jpg
│       └── 04_color_science_swatches.jpg
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
9. **Downstream PixCake Finalization**: Portraits are retouched and re-cropped in 像素蛋糕 (PixCake); **the PixCake export version serves as the final client delivery**.

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
