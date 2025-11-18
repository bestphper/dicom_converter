# DICOM to Image/Video Converter

Python脚本，用于将DICOM医学影像文件转换为标准图像和视频格式（PNG/GIF/MP4）并提取元数据。

A Python script to convert DICOM medical imaging files to standard image and video formats (PNG/GIF/MP4) and extract metadata.

## 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. 运行转换 / Run Conversion

```bash
# 转换所有DICOM文件 / Convert all DICOM files
python3 dicom_converter.py

# 转换特定文件 / Convert specific file
python3 dicom_converter.py "光盘内容/DCM00000" -o my_output

# 使用8位输出（兼容性更好）/ Use 8-bit output (better compatibility)
python3 dicom_converter.py --8bit
```

### 3. 查看结果 / View Results

输出文件将保存在 `output/` 目录：
Output files will be saved in `output/` directory:

- **图像文件 / Image files**: `.png` (静态图像 / static images)
- **动画文件 / Animation files**: `.gif` (GIF动画 / GIF animations) 和 `.mp4` (MP4视频 / MP4 videos)
- **元数据文件 / Metadata files**: `.txt` (包含完整的DICOM信息 / contains complete DICOM information)

## 功能特点 / Features

- ✅ 自动识别单帧和多帧图像 / Auto-detects single and multi-frame images
- ✅ 单帧图像转换为PNG / Converts single frames to PNG
- ✅ 多帧图像同时导出GIF和MP4 / Exports multi-frame sequences as both GIF and MP4
- ✅ MP4文件比GIF小85%，更节省空间 / MP4 files are 85% smaller than GIF
- ✅ GIF优化压缩，减少文件大小 / Optimized GIF compression to reduce file size
- ✅ 支持16位高精度PNG输出 / Supports 16-bit high-precision PNG output
- ✅ 提取完整的DICOM元数据 / Extracts complete DICOM metadata
- ✅ 自动应用窗宽窗位设置 / Auto-applies window/level settings
- ✅ 支持JPEG无损压缩 / Supports JPEG Lossless compression
- ✅ 可调节视频帧率 / Adjustable video frame rate

## 输出说明 / Output Description

### 图像和视频格式 / Image and Video Formats

- **PNG**: 用于单帧图像，默认16位精度保证医学影像质量
- **PNG**: For single-frame images, 16-bit precision by default for medical quality
- **GIF**: 用于多帧序列（如血管造影动画），优化压缩
- **GIF**: For multi-frame sequences (like angiography animations), optimized compression
- **MP4**: 用于多帧序列，文件更小（比GIF小约85%），默认10fps
- **MP4**: For multi-frame sequences, much smaller files (~85% smaller than GIF), 10fps by default

### 元数据文件 / Metadata Files

每个图像都有对应的`.txt`文件，包含：
Each image has a corresponding `.txt` file containing:

- 患者信息：姓名、ID、出生日期、性别
- Patient info: Name, ID, Birth Date, Sex
- 检查信息：日期、时间、描述
- Study info: Date, Time, Description
- 设备信息：制造商、型号、医院
- Equipment info: Manufacturer, Model, Institution
- 图像参数：尺寸、位深度、窗宽窗位
- Image parameters: Dimensions, Bit Depth, Window Settings

## 项目信息 / Project Info

**DICOM文件来源 / DICOM Source**: 医疗影像光盘 / Medical imaging CD
**影像类型 / Imaging Type**: X射线血管造影 (XA) / X-Ray Angiography (XA)
**设备 / Equipment**: Philips AlluraXper
**医院 / Institution**: 北京朝阳医院 / Beijing Chaoyang Hospital

## 高级选项 / Advanced Options

### 只导出GIF，不导出MP4 / Export GIF only, no MP4

```bash
python3 dicom_converter.py --no-mp4
```

### 调整视频帧率 / Adjust video frame rate

```bash
# 更快的播放速度 / Faster playback
python3 dicom_converter.py --fps 15

# 更慢的播放速度 / Slower playback
python3 dicom_converter.py --fps 5
```

### 8位兼容模式 / 8-bit compatibility mode

```bash
python3 dicom_converter.py --8bit
```

## 常见问题 / FAQ

### 如果遇到解压错误 / If you encounter decompression errors

```bash
pip3 install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg
```

### GIF文件太大怎么办？ / GIF files too large?

推荐使用MP4格式，文件大小只有GIF的15%左右。如果不需要GIF，可以使用 `--no-mp4` 选项只生成MP4。

Recommend using MP4 format, which is about 85% smaller. If you don't need GIF, use `--no-mp4` to generate MP4 only.

### 查看所有选项 / Show all options

```bash
python3 dicom_converter.py --help
```

## 技术支持 / Technical Support

如需了解更多技术细节，请查看 `CLAUDE.md` 文件。
For more technical details, see `CLAUDE.md` file.

## 许可 / License

本项目仅用于个人医疗档案管理。
This project is for personal medical record management only.
