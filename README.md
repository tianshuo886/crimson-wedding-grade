# fuji-06a-grade · Fuji 06A Painterly Wedding Grade Skill

[English](README.md) | [简体中文](README.zh-CN.md)

`fuji-06a-grade` is a professional Claude Code skill and automated color grading pipeline for wedding and portrait photography, distilled from real-world Fuji X-T2 RAW post-production within [Lucarne](https://lucarne.app).

---

## Key Features

- 🎨 **Canonical "06A Festive Painterly" Look**: Rich celebratory tones with deep, noble crimson reds, creamy skin highlights, and filmic golden warmth.
- 🔬 **Objective LAB Science**: Strict colorimetric convergence standards (wedding red constrained to hue angle 36.5°~38.5° and L* 36~40; bride skin median L* 0.61~0.65) avoiding subjective guesswork.
- 🛡️ **Adaptive Scene Rules**:
  - **Red Lacquer / Gold Foil Details**: Deep crimson protection and anti-yellowing to prevent fluorescent orange casts.
  - **Outdoor Backlit / Veil Recovery**: Clean daylight highlights preserving lace textures.
  - **Indoor Ambient / Dim Makeup Rooms**: Wide ambient environment lift before local adjustments to prevent artificial "cut-out spotlight" effects.
  - **Family Series**: 4 dedicated warm, natural presets avoiding heavy festive red vignettes.
- 🤝 **Interactive Retouch Checkpoint**: Facial skin smoothing (micro-pore softening) and blemish/acne healing are **never hardcoded**; the assistant interactively prompts the user for preferred intensity and treatment path.
- 🚀 **Automation Toolchain**: Native macOS Apple Vision face detector, coordinate transformer, LAB color analyzer, and contact sheet generator.
- 📦 **Dual-Track Delivery**: 8-bit high-quality JPEGs for ready shots; 16-bit uncompressed sRGB TIFFs for manual liquify and retouching in Photoshop / 像素蛋糕.

---

## Directory Structure

```
fuji-06a-grade/
├── SKILL.md                          # Claude Code Skill entrypoint
├── README.md                         # English README
├── README.zh-CN.md                   # Chinese README
├── LICENSE                           # MIT License
├── references/
│   ├── 06a_baseline_recipe.json      # Complete 90-operation Lucarne 06A recipe
│   ├── color_science_and_lab.md      # Target LAB values & grading principles
│   ├── lucarne_cli_reference.md      # CLI syntax, coordinate mapping & gotchas
│   └── family_grades.md              # 4 family portrait preset recipes
└── scripts/
    ├── detect_faces.swift            # Apple Vision face detection tool
    ├── apply_grade.py                # Batch grading & mask injection engine
    ├── family_presets.py             # Family preset definitions
    ├── measure_lab.py                # LAB & luminance objective analyzer
    └── build_sheets.py               # Review contact sheet builder
```

---

## Installation & Usage

### 1. Install into Claude Code

Clone into `~/.agents/skills/` and symlink into `~/.claude/skills/`:

```bash
git clone https://github.com/tianshuo886/fuji-06a-grade.git ~/.agents/skills/fuji-06a-grade
ln -s ~/.agents/skills/fuji-06a-grade ~/.claude/skills/fuji-06a-grade
```

### 2. Invoke in Claude Code

In any Claude Code conversation managing photos, prompt:
- *"Apply 06A color grading to these photos"*
- *"Use fuji-06a-grade on this set"*
- *"/fuji-06a-grade"*

Claude will initiate the pipeline: verify tools, query your smoothing/healing preference, create virtual copies, adapt to scene lights, balance skin exposures, and build contact sheets for review.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
