# 「绛红喜韵」· 富士婚礼油画调色技能 (Crimson Wedding Grade)

[English](README.md) | [简体中文](README.zh-CN.md)

**绛红喜韵** (`crimson-wedding-grade`) 是专为婚礼与新娘肖像摄影打造的 Claude Code 专业技能与自动化调色流水线，沉淀自富士 X-T2 RAW 格式在 [Lucarne](https://lucarne.app) 中的真实后期实战。

它旨在呈现兼具**中式传统喜庆感与古典油画耐看质感**的调色风格：纯正典雅的深沉绛红、温润通透的奶油金暖肤色、沉稳浓郁而不发泥的明暗层次，并通过严密的 CIE L\*a\*b\* 色度学指标实现客观收敛。

![商业摄影全流程架构](docs/assets/04_dual_track_pipeline_architecture.png)

---

## 视觉成果与色彩科学验证 (Visual Showcases)

> 注：为严格保护新人隐私，以下涉及人物肖像之展示已实施专业眼部马赛克/隐私遮挡条，同时完整保全皮肤影调、发丝层次、暖金高光、婚纱细节与背景绛红纯正度，供调色复核与技术研讨。

### 1. 静物细节与红漆金箔：杜绝塑料橙与死黄
中式婚礼中的红漆喜盒、龙凤婚书、喜糖茶礼极易受到室内暖光灯与数码传感器红色溢出的双重干扰，沦为刺眼的“塑料橙”或发闷的“脏黄”。「绛红喜韵」通过色温下压至 4580K、红色明度下压（-23）与黄色饱和压制（-14），将色相角严格锁定在 $36.5^\circ \sim 38.5^\circ$ 的古典绛红黄金区间，同时让金箔折射出纯正无暇的璀璨金光。

![静物色彩收敛](docs/assets/01_still_life_crimson_gold.jpg)

### 2. 人像肤色与面部曝光均衡：通透丝缎奶油肌
人像调色严守 DSCF0020 参照片标准，通过 Apple Vision 人脸识别与局部测光，将新娘与新郎面部中位明度精准收敛在 $L^* = 0.61 \sim 0.65$ 区间。高光融入中间调色相 25/高光色相 45 的微弱暖金倾向，杜绝惨白死光，保留细腻皮肤骨骼轮廓。

![人像肤色与面部曝光均衡](docs/assets/02_bridal_portrait_skin_tone.jpg)

### 3. 暗光化妆间：先提环境，再调人物
在环境昏暗、前方有化妆镜与补光灯的复杂场景下，若仅局部提亮新娘，会产生极度突兀的“闪光灯抠图感”。本调色管线采取“环境先行”策略：全局阴影大提 (+38) 配合背景超羽化大径向遮罩 (+0.28 EV)，将房间暗沉死角整体点亮；再对受环形灯直射的新郎面部负向压光 (-0.70 EV)，实现前后景深光比自然平衡。

![暗光化妆间环境与主体平衡](docs/assets/03_ambient_dim_room_balance.jpg)

---

## 工业级全流程架构：调色与精修的电影级协同

在商业摄影工业界，很多人常有一个误区：“既然下游有修图软件（如像素蛋糕、Evoto、Photoshop），是不是可以在修图软件里顺便调色？”

答案是：**调色与精修在底层科学上是完全解耦的两个世界，两者是天衣无缝的‘黄金搭档’。**

| 维度 | 上游：Claude Code + Lucarne (`crimson-wedding-grade`) | 下游：像素蛋糕 (PixCake) / Photoshop |
| :--- | :--- | :--- |
| **电影工业角色** | **DIT 数字影像工程师 / 首席调色师 (Colorist)** | **高级妆造修图师 / 商业精修师 (Retoucher)** |
| **核心职责** | 掌控 14-bit RAW 光学无损解码、定光影影调、锁定「绛红喜韵」色相角、平衡环境光比 | 骨骼形体液化、AI 仿生高低频微磨皮、祛痘祛痣、去颈纹眼袋、面部平整度 |
| **处理对象** | RAW 原始光电信号、传感器动态范围、色彩空间变换、全片静物与布景 | 人脸网格拓扑、肌肉走势、五官比例、服饰褶皱 |
| **交付产物** | **16-bit 深度无压缩 sRGB TIFF** (单张 ~137 MB) + **8-bit JPG** | 交付客户的最终商业相册 |

### 为什么像素蛋糕替代不了本技能？
1. **光学宽容度代差**：富士 RAF 包含高达 14-bit 的动态范围，阴影大提 +38、高光大压 -64、微观渲染对比度 1.28 必须在 RAW 极早期线性解码阶段进行，才能杜绝色彩断层与噪点脏色；AI 修图软件内部的 RAW 解码相对通用，无法达到专业 RAW 解码器对富士传感器色彩矩阵的深层挖掘。
2. **静物与全景是 AI 修图的盲区**：婚礼不仅有人，还有喜字婚书、红漆盒、金箔与现场空镜。AI 修图软件以人脸识别驱动，无法为静物做色相角约束；而本 Skill 保证了整场婚礼从静物到肖像的绝对风格统一。
3. **商业点数成本优化**：商业影楼按张扣点。通过本 Skill 本地无限算力批量定调，只有精选的人物特写才导出为 16-bit TIFF 喂给蛋糕修脸，大幅缩减无效点数消耗。

---

## 核心特性与技术规范

- 🎨 **经典基准配方**：90 项参数构成的 `crimson_baseline_recipe.json`，涵盖精准白平衡、胶片色调曲线、色彩分级、微观纹理与微暗角。
- 🔬 **客观色度学分析工具**：内置 `measure_lab.py` 分析脚本，自动提取全图与红区 CIE L\*a\*b\* 均值及色相角，摆脱主观肉眼调色偏差。
- 🛡️ **三大环境自适应校准**：
  - **静物 / 喜字婚书 / 红漆金箔 (`detail`)**：专属压红明度（-12 ~ -23）与强力除黄（黄饱和 -14），使金箔璀璨、红漆深红。
  - **户外逆光 / 白纱迎亲 (`backlit`)**：色温降至 4580K，高光大压 -38，完美保全蕾丝婚纱细节与纯洁冷白。
  - **室内暗光 / 化妆间 (`dim_room`)**：环境全局阴影大提（+38）与背景大型径向遮罩提亮，彻底消除突兀的“闪光灯抠图感”。
- 🤝 **强制交互检查点**：面部平滑（毛孔微磨皮）与斑点/痘痘点修**绝不写死在预设中**；执行时主动向摄影师交互询问档位（轻度/中度/不磨皮）与交付路径。
- 🚀 **macOS 原生工具链**：
  - `detect_faces.swift`：基于 Apple Vision 原生框架高精度毫秒级提取人脸 Bounding Box。
  - 坐标归一化转换器：将 Vision 图像坐标映射至 Lucarne 长边归一化径向渐变局部遮罩。
  - `build_sheets.py`：自动输出整套多列选片总览拼图与 100% 原尺寸面部质感复核图。
- 📦 **双轨分流交付 (Dual-Track)**：
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
├── docs/
│   └── assets/                       # 架构图、静物与人像成果展示图 (已遮挡脱敏)
│       ├── 01_still_life_crimson_gold.jpg
│       ├── 02_bridal_portrait_skin_tone.jpg
│       ├── 03_ambient_dim_room_balance.jpg
│       └── 04_dual_track_pipeline_architecture.png
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
