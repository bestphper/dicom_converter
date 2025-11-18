# DICOM Converter Project Index

## 📚 Documentation Files

### English Documentation
- **[README.md](README.md)** - Main English documentation (Quick Start, Features, Usage)
- **[CONVERSION_REPORT.txt](CONVERSION_REPORT.txt)** - English conversion report and detailed information
- **[CLAUDE.md](CLAUDE.md)** - Technical documentation for developers

### Chinese Documentation (中文文档)
- **[README_CN.md](README_CN.md)** - 中文主文档（快速开始、功能、使用方法）
- **[转换说明_CN.txt](转换说明_CN.txt)** - 中文转换报告和详细信息

## 🔧 Core Files

- **[dicom_converter.py](dicom_converter.py)** - Main conversion script
- **[requirements.txt](requirements.txt)** - Python dependencies

## 📁 Directories

- **dicom_data/** - Input DICOM files (source medical imaging data)
- **output/** - Output directory (PNG, GIF, MP4, and TXT files)

## 🚀 Quick Start

For English users:
```bash
# Install dependencies
pip3 install -r requirements.txt

# Convert all DICOM files
python3 dicom_converter.py

# View help
python3 dicom_converter.py --help
```

对于中文用户：
```bash
# 安装依赖
pip3 install -r requirements.txt

# 转换所有DICOM文件
python3 dicom_converter.py

# 查看帮助
python3 dicom_converter.py --help
```

## 📖 Which Documentation Should I Read?

**I want to quickly start using the converter:**
- English: Read [README.md](README.md)
- 中文: 阅读 [README_CN.md](README_CN.md)

**I want detailed conversion results and examples:**
- English: Read [CONVERSION_REPORT.txt](CONVERSION_REPORT.txt)
- 中文: 阅读 [转换说明_CN.txt](转换说明_CN.txt)

**I want technical details for development:**
- Read [CLAUDE.md](CLAUDE.md)

## ✨ Key Features

- ✅ PNG output for single-frame images (16-bit precision)
- ✅ GIF + MP4 output for multi-frame sequences
- ✅ MP4 files are 85% smaller than GIF
- ✅ Complete DICOM metadata extraction to TXT files
- ✅ Support for JPEG Lossless compressed DICOM files

## 📊 Project Statistics

- **Total DICOM Files**: 34
- **Output Formats**: PNG, GIF, MP4, TXT
- **Total Output Files**: 90 (12 PNG + 22 GIF + 22 MP4 + 34 TXT)
- **Space Savings**: MP4 is ~85% smaller than GIF (196MB → 29MB)

## 🔗 Quick Links

| Task | English | 中文 |
|------|---------|------|
| Quick Start Guide | [README.md](README.md) | [README_CN.md](README_CN.md) |
| Detailed Report | [CONVERSION_REPORT.txt](CONVERSION_REPORT.txt) | [转换说明_CN.txt](转换说明_CN.txt) |
| Technical Docs | [CLAUDE.md](CLAUDE.md) | [CLAUDE.md](CLAUDE.md) |

---

**Version**: 2.0
**Last Updated**: 2025-11-18
**License**: For personal medical record management only
