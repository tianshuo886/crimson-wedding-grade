# 「绛红喜韵」· 富士婚礼油画调色技能

[English](README.md) | [简体中文](README.zh-CN.md)

**绛红喜韵** (`crimson-wedding-grade`) 是专为婚礼与新娘肖像摄影打造的 Claude Code 专业技能与自动化调色流水线，沉淀自富士 X-T2 RAW 格式在 [Lucarne](https://lucarne.app) 中的真实后期实战。

它旨在呈现兼具**中式传统喜庆感与古典油画耐看质感**的调色风格：纯正典雅的深沉绛红、温润通透的奶油金暖肤色、沉稳浓郁而不发泥的明暗层次，并通过严密的 CIE L\*a\*b\* 色度学指标实现客观收敛。

---

## 美学理念与色度学指标

数码婚礼调色在处理红色主色调时往往面临两个极端：要么红色过饱和沦为刺眼的“塑料红/荧光红/发紫洋红”，要么粗暴降低饱和度导致整体画面寡淡发灰、油腻发泥。

「绛红喜韵」通过精密的光学影调分层与色彩收敛解决了这一难题：

1. **贵气中式正红（绛红）**：
   - **目标 CIE L\*a\*b\***：$L^* \in [32, 38], a^* \in [+35, +42], b^* \in [+25, +30]$。
   - **色相角硬约束**：严格收敛于 **$36.5^\circ \sim 38.5^\circ$**。
   - 视觉效果：既有喜庆氛围的浓烈，又具深宫红漆与朱砂般的沉稳庄重，彻底杜绝偏黄的柿子红与发青蓝的紫红。
2. **通透白皙的奶油新娘肤色**：
   - **面部中位明度**：对齐至 $L^* \in [0.61, 0.65]$。
   - 高光区融入微弱的暖金调（中间调色相 25/饱和 8，高光色相 45/饱和 3），呈现柔美润泽的丝缎光感，不飞白、不惨白。
3. **沉稳耐看的油画影调**：
   - 维持 1.28 高渲染对比度与 +16 色调对比度，结合 +16 清晰度与 40 锐化。
   - 绝不通过全局降对比、降清晰度来“软化”画面；所有色彩浓淡调整均在 HSL 分通道精确完成，确保质感锐利且沉静。

---

## 核心特性

- 🎨 **经典基准配方**：90 项参数构成的 `crimson_baseline_recipe.json`，涵盖精准白平衡、胶片色调曲线、色彩分级、微观纹理与微暗角。
- 🔬 **客观色度学分析工具**：内置 `measure_lab.py` 分析脚本，自动提取全图与红区 CIE L\*a\*b\* 均值及色相角，摆脱主观肉眼调色偏差。
- 🛡️ **三大环境自适应校准**：
  - **静物 / 喜字婚书 / 红漆金箔**：专属压红明度（-12 ~ -23）与强力除黄（黄饱和 -14），使金箔璀璨、红漆深红。
  - **户外逆光 / 白纱迎亲**：色温降至 4580K，高光大压 -38，完美保全蕾丝婚纱细节与纯洁冷白。
  - **室内暗光 / 化妆间**：环境全局阴影大提（+38）与背景大型径向遮罩提亮，彻底消除突兀的“闪光灯抠图感”。
- 🤝 **强制交互检查点**：面部平滑（毛孔微磨皮）与斑点/痘痘点修**绝不写死在预设中**；执行时主动向摄影师交互询问档位（轻度/中度/不磨皮）与交付路径。
- 🚀 **macOS 原生工具链**：
  - `detect_faces.swift`：基于 Apple Vision 原生框架高精度毫秒级提取人脸 Bounding Box。
  - 坐标归一化转换器：将 Vision 图像坐标映射至 Lucarne 长边归一化径向渐变局部遮罩。
  - `build_sheets.py`：自动输出整套多列选片总览拼图与 100% 原尺寸面部质感复核图。
- 📦 **双轨分流交付**：
  - **直接出片 (8-bit JPG)**：质量 98、sRGB 色域，适用于静物特写、大景现场与免液化肖像。
  - **高宽容度精修 (16-bit TIFF)**：全尺寸无压缩 16 位 sRGB TIFF（约 137 MB/张），专供导入 Photoshop / 像素蛋糕进行高精度形体液化与手工点修。

---

## 目录结构

```
crimson-wedding-grade/
├── SKILL.md                          # Claude Code Skill 入口定义与交互协议
├── README.md                         # 英文文档
├── README.zh-CN.md                   # 中文文档
├── LICENSE                           # MIT 许可证
├── references/
│   ├── crimson_baseline_recipe.json  # 完整的 90 项 Lucarne 核心基准 JSON
│   ├── color_science_and_lab.md      # CIE L*a*b* 色度学标准与色相角规范
│   └── lucarne_cli_reference.md      # Lucarne CLI 协议、坐标体系与避坑要点
└── scripts/
    ├── detect_faces.swift            # 苹果原生 Apple Vision 人脸识别 (Swift)
    ├── apply_grade.py                # 批量调色应用与局部遮罩注入脚本
    ├── measure_lab.py                # CIE L*a*b* 色度与中位明度测量工具
    └── build_sheets.py               # 拼图总览与 100% 皮肤复核图生成工具
```

---

## 安装与配置

### 1. 运行依赖

- macOS 13+ (Ventura, Sonoma, Sequoia)
- [Lucarne](https://lucarne.app) 1.7.0+（位于 `/Applications/Lucarne.app`）
- Python 3.9+ 并安装 `Pillow` 与 `numpy`
- Xcode 命令行工具（包含 `swiftc`）

### 2. 作为 Claude Code 技能安装

将本仓库克隆至本地 agents skills 目录，并软链接至 Claude Code 技能目录：

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/tianshuo886/crimson-wedding-grade.git ~/.agents/skills/crimson-wedding-grade
ln -s ~/.agents/skills/crimson-wedding-grade ~/.claude/skills/crimson-wedding-grade
```

---

## 在 Claude Code 中使用

安装完成后，在涉及婚礼照片调色或富士 RAW 格式处理的对话中，Claude Code 将自动识别并推荐此技能。

### 自然语言唤起示例

- *“对这批婚礼照片应用「绛红喜韵」调色管线。”*
- *“帮我把选出的这几张富士婚礼 RAW 调成 绛红喜韵 风格。”*
- *“/crimson-wedding-grade”*

### 标准执行流程

1. **环境检查**：验证 Lucarne 编目环境及相关脚本可用性。
2. **交互检查点**：主动向您确认面部微磨皮强度（轻度/中度/不磨皮）及瑕疵点修方案。
3. **创建虚拟副本**：无损复制原始文件版本，绝不触碰原片。
4. **注入基准配方**：一键应用 `crimson_baseline_recipe.json`。
5. **场景光线自适应**：自动识别静物、逆光或暗光环境并注入校准参数。
6. **面部曝光均衡**：测量面部肤色明度，平衡至 $L^* = 0.61 \sim 0.65$ 黄金区间。
7. **拼图复核交付**：生成全景总览图与 100% 皮肤裁切拼图供您确认。
8. **双轨规格导出**：根据照片用途自动分别导出 16-bit 精修 TIFF 或高质量 8-bit JPG。

---

## 独立命令行运行

该脚本亦可独立于 Claude 在终端中直接运行：

```bash
# 设置 Lucarne 编目路径
export LUCARNE_CATALOG="$HOME/Library/Application Support/Lucarne/Catalogs/Library.lucarnecatalog"

# 对指定照片文档 (ID: 105) 应用静物场景调色
python3 scripts/apply_grade.py 105 --scene detail

# 测量已渲染图像的 CIE L*a*b* 色度数值
python3 scripts/measure_lab.py rendered_preview.jpg
```

---

## 开源协议

本项目采用 MIT 许可证，详情请参阅 [LICENSE](LICENSE)。
