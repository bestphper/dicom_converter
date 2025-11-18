# DICOM医学影像转视频转换器

中文 | [English](README.md)

Python脚本，用于将DICOM医学影像文件转换为标准图像和视频格式（PNG/GIF/MP4）并提取元数据。

## 功能特点

- ✅ 自动识别单帧和多帧图像
- ✅ 单帧图像转换为PNG
- ✅ 多帧图像同时导出GIF和MP4
- ✅ MP4文件比GIF小85%，更节省空间
- ✅ GIF优化压缩，减少文件大小
- ✅ 支持16位高精度PNG输出
- ✅ 提取完整的DICOM元数据
- ✅ 自动应用窗宽窗位设置
- ✅ 支持JPEG无损压缩
- ✅ 可调节视频帧率

## 快速开始

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 2. 运行转换

```bash
# 转换所有DICOM文件（默认：dicom_data/ 目录）
python3 dicom_converter.py

# 转换特定文件
python3 dicom_converter.py dicom_data/DCM00000 -o my_output

# 使用8位输出（兼容性更好）
python3 dicom_converter.py --8bit
```

### 3. 查看结果

输出文件将保存在 `output/` 目录：

- **图像文件**: `.png` (静态图像)
- **动画文件**: `.gif` (GIF动画) 和 `.mp4` (MP4视频)
- **元数据文件**: `.txt` (包含完整的DICOM信息)

## 输出格式说明

### 图像和视频格式

- **PNG**: 用于单帧图像，默认16位精度保证医学影像质量
- **GIF**: 用于多帧序列（如血管造影动画），优化压缩
- **MP4**: 用于多帧序列，文件更小（比GIF小约85%），默认10fps

### 文件大小对比

基于34个DICOM文件的测试结果：
- **GIF总大小**: ~196 MB
- **MP4总大小**: ~29 MB
- **节省空间**: ~167 MB (85%)

示例对比：
- DCM00001: 4.2 MB (GIF) → 380 KB (MP4) - 节省91%
- DCM00004: 32 MB (GIF) → 5.4 MB (MP4) - 节省83%
- DCM00007: 5.6 MB (GIF) → 492 KB (MP4) - 节省91%

**推荐**: 优先使用MP4格式，文件更小、质量相同

### 元数据文件

每个图像都有对应的`.txt`文件，包含：
- 患者信息：姓名、ID、出生日期、性别
- 检查信息：日期、时间、描述
- 设备信息：制造商、型号、医院
- 图像参数：尺寸、位深度、窗宽窗位

## 高级选项

### 只导出GIF，不导出MP4

```bash
python3 dicom_converter.py --no-mp4
```

### 调整视频帧率

```bash
# 更快的播放速度
python3 dicom_converter.py --fps 15

# 更慢的播放速度
python3 dicom_converter.py --fps 5
```

### 8位兼容模式

```bash
python3 dicom_converter.py --8bit
```

### 自定义输入/输出目录

```bash
python3 dicom_converter.py /path/to/dicom/files -o /path/to/output
```

## 命令行选项

```
用法: dicom_converter.py [-h] [-o OUTPUT] [--8bit] [--no-mp4] [--fps FPS] [input_path]

位置参数:
  input_path            DICOM文件或目录 (默认: dicom_data)

可选参数:
  -h, --help            显示帮助信息
  -o OUTPUT, --output OUTPUT
                        输出目录 (默认: output)
  --8bit                强制8位输出 (默认为16位高精度)
  --no-mp4              禁用MP4视频导出 (只导出GIF)
  --fps FPS             GIF和MP4的帧率 (默认: 10)
```

## 常见问题

### 如果遇到解压错误

```bash
pip3 install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg
```

### GIF文件太大怎么办？

推荐使用MP4格式，文件大小只有GIF的15%左右。如果不需要GIF，可以使用 `--no-mp4` 选项只生成MP4。

### 查看所有选项

```bash
python3 dicom_converter.py --help
```

## 技术细节

### DICOM支持

- **压缩格式**: JPEG无损、非分层、一阶预测 (Process 14)
- **影像模式**: X射线血管造影 (XA) 及其他DICOM模式
- **光度解释**: MONOCHROME1, MONOCHROME2, RGB
- **帧数**: 单帧和多帧序列

### 转换流程

1. 使用pylibjpeg读取压缩像素数据
2. 应用窗宽窗位设置（如果存在）
3. 应用RescaleSlope和RescaleIntercept（Hounsfield单位）
4. 处理MONOCHROME1（反转）和MONOCHROME2光度解释
5. 导出为PNG（默认16位）、GIF（优化）和MP4（H.264编码）
6. 提取所有DICOM标签到对应的TXT文件

## 系统要求

- Python 3.8+
- pydicom >= 2.4.0
- numpy >= 1.24.0, < 2.0
- Pillow >= 10.0.0
- pylibjpeg >= 2.0
- pylibjpeg-libjpeg >= 2.0
- pylibjpeg-openjpeg >= 2.0
- opencv-python >= 4.8.0

## 项目结构

```
.
├── dicom_converter.py          # 主转换脚本
├── requirements.txt            # Python依赖
├── README.md                   # 英文文档
├── README_CN.md                # 中文文档
├── CLAUDE.md                   # 技术文档
├── dicom_data/                 # DICOM输入文件（默认）
│   ├── DCM00000
│   ├── DCM00001
│   └── ...
└── output/                     # 输出目录（由脚本创建）
    ├── DCM00000.gif
    ├── DCM00000.mp4
    ├── DCM00000.txt
    └── ...
```

## 许可证

本项目仅用于个人医疗档案管理，不可用于诊断。

## 版本历史

**版本 2.0** (2025-11-18)
- ✓ 新增MP4视频导出功能
- ✓ 优化GIF压缩，减少文件大小
- ✓ 新增帧率调节选项 (--fps)
- ✓ 新增禁用MP4选项 (--no-mp4)
- ✓ 更新所有文档

**版本 1.0** (2025-11-18)
- ✓ 初始版本，支持PNG/GIF/TXT导出
- ✓ 支持JPEG无损压缩DICOM
- ✓ 自动元数据提取
