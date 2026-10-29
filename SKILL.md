---
name: crimson-wedding-grade
description: "Professional Fuji RAW '绛红喜韵' (Crimson Wedding) painterly color grading pipeline for wedding and bridal portrait photography in Lucarne. Delivers noble crimson reds (hue 36.5°~38.5°), creamy skin highlights, and rich filmic contrast. Features adaptive scene calibration, objective CIE L*a*b* skin balance, and 16-bit TIFF delivery handoff. Interactively prompts for skin smoothing and blemish fixing preferences."
---

# 「绛红喜韵」专业婚礼油画调色技能 (Crimson Wedding Grade Skill)

本技能沉淀自富士 X-T2 婚礼摄影 RAW 格式解码调色的完整实战。专为中式与现代典雅婚礼定制，核心目标是实现兼具**浓郁深沉的绛红喜庆感**与**油画质感、耐看沉稳**的色彩平衡，彻底解决“塑料红”、“高光惨白发飘”与“室内灯光死黄”问题。

所有操作全程遵循 **RAW-first 无损流程**：只在 Lucarne 虚拟副本上进行参数应用，原始 RAW/JPG 绝不修改。

---

## ⚠️ 强制交互检查点 (Mandatory User Checkpoint)

**铁律：面部平滑 / 毛孔微磨皮、面部斑点 / 痘痘点修不得固定写死在预设中！**

在调色流程进入人脸局部处理之前，**必须主动向用户提问确认**：

### 1. 面部平滑 / 毛孔微磨皮确认
询问用户：
> “请问本组婚礼照片是否需要开启面部平滑/毛孔微磨皮？请选择档位：
> 1. **轻度微磨皮（推荐）**：参数 `texture: -12, clarity: -2, shadows: +2, exposure: +0.02`，仅平滑微小粗糙，完整保留毛孔、细纹与骨骼轮廓。
> 2. **中度平滑**：参数 `texture: -18, clarity: -4`，适合瑕疵略多但仍需保留质感的场景。
> 3. **不做磨皮**：完全保留原始 RAW 解码纯净纹理。
> 4. **自定义数值**。”

### 2. 面部斑点 / 痘痘点修确认
询问用户：
> “请问本组照片中的面部斑点、痘痘或临时红印如何处理？
> 1. **导出 16-bit TIFF 交由专业修图软件（推荐）**：留到 Photoshop / 像素蛋糕中通过画笔或 AI 智能消除，避免局部调色算法抹平皮肤纹理。
> 2. **在 Lucarne 中添加微型局部调整**：仅针对明显固定红印做局部降饱和/提暗部（不改动几何形状）。
> 3. **保留真实自然特征**：不做点修。”

---

## 核心美学规范与 LAB 指标 (Color Science & Benchmarks)

1. **婚礼正红（绛红）规范**：
   - 目标范围：L\* 32 ~ 38, a\* +35 ~ +42, b\* +25 ~ +30
   - 色相角限制：**严格控制在 36.5° ~ 38.5°** 之间。
   - 视觉特征：深邃典雅、含蓄贵气的古典绛红，杜绝偏黄的“朱红/柿子红”和偏蓝的“洋红/紫红/荧光红”。
2. **新娘与伴娘肤色明度规范**：
   - 人脸中心中位明度：**L\* 0.61 ~ 0.65**。
   - 视觉特征：白皙透亮，面容泛出柔润的暖金光泽，高光不过曝飞白，阴影过渡平滑细腻。
3. **质感基准**：
   - 渲染对比度 1.28 + 色调对比度 +16 + 清晰度 +16 + 锐化 40。
   - 严禁通过降低对比度或模糊清晰度来“减艳”，避免画面发灰、发闷、发泥。

---

## 执行流程协议 (Step-by-Step Workflow)

### 步骤 1：环境就绪检查
1. 确认 Lucarne CLI 路径与环境变量：
   ```bash
   export LUCARNE_CATALOG="$HOME/Library/Application Support/Lucarne/Catalogs/Library.lucarnecatalog"
   LC="/Applications/Lucarne.app/Contents/Helpers/lucarne"
   ```
2. 确认辅助工具就绪：
   - Apple Vision 人脸检测：`swift <skill>/scripts/detect_faces.swift`
   - LAB 与明度测量工具：`python3 <skill>/scripts/measure_lab.py`
   - 调色应用引擎：`python3 <skill>/scripts/apply_grade.py`
   - 拼图与总览工具：`python3 <skill>/scripts/build_sheets.py`

### 步骤 2：创建虚拟副本 (Virtual Copies)
严禁修改原片！读取待调色图片的原始 doc id，为每张图片创建虚拟副本并命名：
```bash
$LC copy <orig_doc_id>
$LC rename <new_doc_id> "DSCF#### 绛红喜韵"
```

### 步骤 3：注入「绛红喜韵」核心基准 (Baseline Ingestion)
将基准配方 `<skill>/references/crimson_baseline_recipe.json` 应用到虚拟副本：
- 色温 4950K，色调 -4，曝光 EV +0.25
- 渲染对比度 1.28，色调对比度 +16
- 高光 -28，阴影 +10，白色 +10，黑色 -8
- 鲜艳度 +12，饱和度 +4
- HSL：红色色相 +4 / 饱和 +12 / 明度 +4；橙色色相 -2 / 饱和 -3 / 明度 +6；黄色明度 +5 / 饱和 -2
- 色彩分级：中间调 (色相 25, 饱和 8, 明度 4)；高光 (色相 45, 饱和 3, 明度 2)；阴影 (色相 15, 饱和 4, 明度 0)
- 细节：清晰度 +16，纹理 +1，锐化 40
- 暗角 -12，胶片颗粒 5，胶片模拟：none

### 步骤 4：场景自适应校准 (Scene Classification & Adaptation)
针对婚礼当天的不同光照环境注入自适应校准：

#### A. 婚礼静物 / 喜字婚书 / 红漆盒 / 捧花 (Detail / Still Life)
- **目标**：保护深红纯正度，金箔璀璨闪亮，彻底去除黄染。
- **参数微调**：
  - 色温降至 4580K ~ 4640K，tint 设为 -2
  - 黄色饱和度压到 -14，黄色明度降至 0
  - 橙色饱和度压到 -6
  - 中间调暖色投射降至 4，高光暖色降至 1
  - 红色明度深压（Brightness Red: -12 ~ -23），红色饱和度微调（-8 ~ 0），红色色相 -2 ~ -3
  - **维持**渲染对比度 1.28、清晰度 16、锐化 40，绝不降对比发灰。
  - 检验指标：红区 LAB 色相角严格收敛于 **36.5° ~ 38.5°**，红区明度 L* 压至 36 ~ 40。

#### B. 户外逆光 / 白纱迎亲 (Outdoor Backlit)
- **目标**：恢复婚纱蕾丝高光细节，消除阴天泛黄。
- **参数微调**：
  - 色温降至 4580K，tint -1
  - 曝光 EV -0.18，高光 -38，对比度 +20
  - 绿色饱和度 -2，黄色饱和度 -10
  - 保护白纱纯洁质感与微金逆光轮廓。

#### C. 室内暗光 / 化妆间 (Ambient Dim Room)
- **目标**：先提环境再调人，避免孤立“手电筒抠图感”。
- **参数微调**：
  - 全局曝光 EV +0.10，阴影大提 +38，黑色 -4，高光 -64
  - 背景暗区施加大型径向遮罩（羽化 95，EV +0.28，阴影 +22）
  - 前景补光灯过曝区域（如强光打在新郎面部）施加局部负向遮罩压低高光与曝光

### 步骤 5：人脸检测与面部曝光平衡 (Face Normalization)
1. 运行 `swift <skill>/scripts/detect_faces.swift` 获取各人脸精确边界框。
2. 转换为 Lucarne 归一化长边坐标系（参见 `<skill>/references/lucarne_cli_reference.md`）。
3. 根据**交互检查点**的用户选择，注入对应强度的局部平滑遮罩。
4. **人脸明度对齐**：使用 `python3 <skill>/scripts/measure_lab.py` 测量人物面部皮肤中位明度，以基准（L ≈ 0.61 ~ 0.65）为目标微调局部曝光，避免双人合影中因布光角度产生巨大明暗反差。

### 步骤 6：生成复核拼图 (Visual Review)
使用 `<skill>/scripts/build_sheets.py` 生成：
- `00_总览_XX张.jpg`：全部入选成片 6 列网格总览。
- `01_皮肤100%_检查.jpg`：面部 100% 原尺寸裁切拼图，供用户复核毛孔质感与磨皮程度。
- 专题对比图（如静物对比组、面部曝光组）。

### 步骤 7：分流交付与全尺寸导出 (Export Handoff)
经用户确认后，分两类导出（3:2 原尺寸全分辨率 5998×3998）：
1. **JPG/ (直接成片)**：
   - 静物细节、空镜、无需液化的人像。
   - 配置：8-bit JPEG，质量 98，sRGB。
2. **TIFF_16bit/ (精修交付)**：
   - 需进行下颌线/手臂液化、面部斑点点修、衣服去死褶与构图重裁切的人物特写与双人照。
   - 配置：16-bit 无压缩 TIFF，sRGB，内嵌 ICC 配置，保留最大宽容度。
   - 无缝导入 Photoshop / 像素蛋糕完成深度修饰与二次构图裁剪。**人物照片最终以像素蛋糕导出的版本为准交付新人**。

---

## 技术避坑铁律速查

1. **`updateLocalAdjustment` 覆盖陷阱**：必须传回包含 `selection` 的完整对象，否则遮罩立即被清空！
2. **`lucarne render` 覆盖报错**：渲染前必须 `rm -f <target_file>`。
3. **导出 proto3 枚举要求**：必须写全 `EXPORT_FORMAT_TIFF`、`EXPORT_COLOR_SPACE_SRGB`、`RESIZE_MODE_ORIGINAL`；JPEG 必须显式声明 `"bitsPerChannel": 8`。
4. **拒绝全局发闷**：不要用降对比度、降清晰度的方法来解决静物偏艳，必须通过 HSL 红色明度下压和黄色饱和度压制实现。
