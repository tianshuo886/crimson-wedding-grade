# Lucarne CLI 自动化与操作手册 (Lucarne CLI Reference & Gotchas)

Lucarne (当前适配版本 1.7.x) 提供了完备的命令行辅助工具与 RPC 接口。本手册记录了在无头/自动化环境下操作 Lucarne 的权威规范与重大避坑点。

---

## 1. 基础环境与调用方式

- **可执行文件路径**：`/Applications/Lucarne.app/Contents/Helpers/lucarne`
- **默认图库路径**：`~/Library/Application Support/Lucarne/Catalogs/Library.lucarnecatalog`
- **环境变量**：所有命令依赖 `LUCARNE_CATALOG` 环境变量或 `--catalog <path>` 参数。
  ```bash
  export LUCARNE_CATALOG="$HOME/Library/Application Support/Lucarne/Catalogs/Library.lucarnecatalog"
  LC="/Applications/Lucarne.app/Contents/Helpers/lucarne"
  ```

---

## 2. 核心命令清单

### 2.1 虚拟副本管理 (Virtual Copies)
严禁直接在母本上修改！所有调色必须在虚拟副本上进行。
```bash
# 复制指定版本（原图 doc id 如 106）
$LC copy 106
# 重命名虚拟副本
$LC rename <new_doc_id> "DSCF0020 06A"
```

### 2.2 文档参数读取与应用 (Doc Get / Apply)
```bash
# 读取当前文档参数（输出包含 "revision N" 头信息及 JSON 主体）
$LC doc get <doc_id>

# 批量应用参数 JSON
$LC doc apply <doc_id> @/path/to/operations.json
```

### 2.3 快速渲染与全尺寸导出
```bash
# 快速预览渲染 (render)
$LC render <doc_id> --out /path/to/preview.jpg --long-edge 1600 --format JPEG --quality 95

# 导出带遮罩可视化的预览
$LC render <doc_id> --out /path/to/mask_view.jpg --long-edge 1200 --mask skin0

# 全尺寸高质量导出 (export)
$LC export <doc_id1> <doc_id2> --settings @/path/to/export_settings.json
```

---

## 3. 重大技术避坑指南 (Critical Gotchas)

### 3.1 `updateLocalAdjustment` 会彻底抹除未传的 `selection`！
- **严重 Bug**：在 Lucarne 中调用 `updateLocalAdjustment` 时，如果 payload 中仅包含 `{"id": "skin0", "settings": {...}}`，Lucarne 会将整个局部调整对象覆盖，导致 `selection` 变为空对象 `{}`，**从而彻底摧毁遮罩径向梯度！**
- **铁律**：更新局部调整时，必须先通过 `doc get` 取出当前的完整 `localAdjustment` 对象（包含 `id`, `name`, `enabled`, `amount`, `selection`），在其 `settings` 字段上修改后，将整个对象完整传回。

### 3.2 坐标系映射 (Vision BoundingBox -> Lucarne Radial Mask)
Lucarne 的局部调整径向渐变使用归一化坐标，但其坐标系有严苛的定义：
1. **坐标系原点**：左上角为 `(0, 0)`，X 向右，Y 向下。
2. **长边归一化半径 (Long-edge Normalized)**：
   - 半径 `radiusX` 和 `radiusY` 的度量基准是照片的**长边 (Long Edge)**。
   - 竖构图照片（EXIF 旋转后，宽 4000 × 高 6000）：
     - X 轴缩放因子 `wx = 4000 / 6000 ≈ 0.6667`
     - Y 轴缩放因子 `hy = 1.0`
     - 因此若人脸框相对宽度为 `w`，则 `radiusX = 0.72 * w * wx`，`radiusY = 0.88 * h * hy`。
3. **Vision 检测框转换**：
   - Apple Vision (`VNDetectFaceRectanglesRequest`) 输出原点为**左下角** `(0, 0)`。
   - 映射到 Lucarne 中心点：
     $$\text{centre.x} = x + \frac{w}{2}$$
     $$\text{centre.y} = 1.0 - \left(y + \frac{h}{2}\right)$$

### 3.3 `lucarne render` 拒绝覆盖已有文件
- 执行 `lucarne render` 时，若目标文件已存在，命令会直接报错：`FILE_WRITE_FAILED: cannot write file ... a file exists at the path`，且退出码不为 0。
- **规范**：在渲染前必须先检查并删除旧目标文件（`rm -f <target_file>`）。

### 3.4 全尺寸导出 (ExportSettings) 规范
`export` 命令使用 proto3 JSON 规范，字段名与枚举值大小写敏感：
- **TIFF 16-bit 无压缩导出配置**：
  ```json
  {
    "format": "EXPORT_FORMAT_TIFF",
    "bitsPerChannel": 16,
    "colorSpace": "EXPORT_COLOR_SPACE_SRGB",
    "size": { "mode": "RESIZE_MODE_ORIGINAL" },
    "destination": "/path/to/output_folder",
    "fileNameTemplate": "{file_name}",
    "collisionPolicy": "COLLISION_POLICY_OVERWRITE",
    "includeMetadata": true
  }
  ```
- **JPEG 8-bit 高质量导出配置**：
  ```json
  {
    "format": "EXPORT_FORMAT_JPEG",
    "quality": 98,
    "bitsPerChannel": 8,
    "colorSpace": "EXPORT_COLOR_SPACE_SRGB",
    "size": { "mode": "RESIZE_MODE_ORIGINAL" },
    "destination": "/path/to/output_folder",
    "fileNameTemplate": "{file_name}",
    "collisionPolicy": "COLLISION_POLICY_OVERWRITE",
    "includeMetadata": true
  }
  ```
  *注：JPEG 格式不能省略 `bitsPerChannel: 8`，否则会被拒绝。*
