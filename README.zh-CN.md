# fuji-06a-grade · 富士 06A「喜庆油画」调色技能

[English](README.md) | [简体中文](README.zh-CN.md)

`fuji-06a-grade` 是一个专为婚礼与人像摄影打造的 Claude Code 智能调色技能（Skill）与色彩流水线，沉淀自富士 X-T2 RAW 格式照片在 [Lucarne](https://lucarne.app) 解码环境下的全套调色实践。

---

## 核心特性

- 🎨 **经典「06A 喜庆油画」风格**：浓郁喜庆但沉稳贵气，告别“塑料红”与高光惨白，呈现扎实的油画胶片感。
- 🔬 **客观 LAB 数值基准**：基于严苛的 LAB 测光基准（婚礼红色相角收敛至 36.5°~38.5°，明度 L* 36~40；新娘皮肤中位明度 L* 0.61~0.65），彻底避免靠肉眼主观瞎猜。
- 🛡️ **自适应场景校准**：
  - **红漆盒/金箔细节**：深红保护与去黄，避免橙红发飘或金箔泛白。
  - **户外大逆光/迎亲**：透亮白纱高光恢复，消除阴天泛黄。
  - **室内暗光/化妆间**：先大范围提亮环境光，再微调主体，避免“手电筒照人”般的抠图假光。
  - **家庭温馨系列**：提供 4 款不套用浓重婚礼红的独立温润预设。
- 🤝 **交互式修饰检查点**：面部平滑（毛孔微磨皮）与面部斑点点修**不写死在预设中**，每次调色时主动询问用户档位与处理路径。
- 🚀 **自动化工具链**：内置 macOS Native Apple Vision 人脸检测与长边归一化坐标转换、LAB 色彩测光仪、批量审核拼图工具。
- 📦 **双轨高质量交付**：细节直接出 8-bit 高质量 JPG；人物主体出 16-bit 无压缩 sRGB TIFF，无损交付 Photoshop / 像素蛋糕完成液化与精修。

---

## 仓库结构

```
fuji-06a-grade/
├── SKILL.md                          # Claude Code Skill 入口定义
├── README.md                         # 英文说明
├── README.zh-CN.md                   # 中文说明
├── LICENSE                           # MIT 许可证
├── references/
│   ├── 06a_baseline_recipe.json      # 90 项 Lucarne 06A 核心调色配方
│   ├── color_science_and_lab.md      # 目标 LAB 数值、调色经验与避坑
│   ├── lucarne_cli_reference.md      # Lucarne CLI 自动化命令与致命陷阱
│   └── family_grades.md              # 家庭温馨系列四套独立参数预设
└── scripts/
    ├── detect_faces.swift            # 基于 Apple Vision 的人脸检测工具
    ├── apply_grade.py                # 批量调色、场景自适应与遮罩注入引擎
    ├── family_presets.py             # 家庭预设定义
    ├── measure_lab.py                # LAB 色彩与明度客观测光仪
    └── build_sheets.py               # 6列总览与 100% 原尺寸面部拼图工具
```

---

## 安装与使用

### 1. 安装至 Claude Code

将本仓库克隆至 `~/.agents/skills/`，并在 `~/.claude/skills/` 中建立软链接：

```bash
# 克隆仓库
git clone https://github.com/tianshuo886/fuji-06a-grade.git ~/.agents/skills/fuji-06a-grade

# 建立软链接
ln -s ~/.agents/skills/fuji-06a-grade ~/.claude/skills/fuji-06a-grade
```

### 2. 在 Claude Code 中调用

在任何相片编辑会话中，只需对 Claude 说：
- *"帮我把这组照片用 06A 调色"*
- *"套用 06A 喜庆油画风格"*
- *"执行 /fuji-06a-grade"*

Claude 将自动载入本技能流程：首先检查工具与照片，询问你的磨皮/点修偏好，然后自动建立虚拟副本、注入配方、校准场景、测量人脸对齐亮度，并生成拼图供你审核！

---

## 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。
