# DICOM to Image/Video Converter

[中文文档](README_CN.md) | English

A Python script to convert DICOM medical imaging files to standard image and video formats (PNG/GIF/MP4) and extract metadata.

## Features

- ✅ Auto-detects single and multi-frame images
- ✅ Converts single frames to PNG
- ✅ Exports multi-frame sequences as both GIF and MP4
- ✅ MP4 files are 85% smaller than GIF
- ✅ Optimized GIF compression to reduce file size
- ✅ Supports 16-bit high-precision PNG output
- ✅ Extracts complete DICOM metadata
- ✅ Auto-applies window/level settings
- ✅ Supports JPEG Lossless compression
- ✅ Adjustable video frame rate

## Quick Start

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Get Sample DICOM Files

**Option A: Generate Sample Files (Recommended for testing)**
```bash
python3 create_sample_dicom.py
```

**Option B: Use Your Own DICOM Files**
- Place your DICOM files in the `dicom_data/` directory
- See [SAMPLE_DATA.md](SAMPLE_DATA.md) for more options

### 3. Run Conversion

```bash
# Convert all DICOM files (default: dicom_data/ directory)
python3 dicom_converter.py

# Convert specific file
python3 dicom_converter.py dicom_data/SAMPLE_CT.dcm -o my_output

# Use 8-bit output for better compatibility
python3 dicom_converter.py --8bit
```

### 4. View Results

Output files will be saved in the `output/` directory:

- **Image files**: `.png` (static images)
- **Animation files**: `.gif` (GIF animations) and `.mp4` (MP4 videos)
- **Metadata files**: `.txt` (complete DICOM information)

## Output Format Description

### Image and Video Formats

- **PNG**: For single-frame images, 16-bit precision by default for medical quality
- **GIF**: For multi-frame sequences (like angiography animations), optimized compression
- **MP4**: For multi-frame sequences, much smaller files (~85% smaller than GIF), 10fps by default

### File Size Comparison

From testing on 34 DICOM files:
- **GIF total**: ~196 MB
- **MP4 total**: ~29 MB
- **Space saved**: ~167 MB (85%)

Example comparisons:
- DCM00001: 4.2 MB (GIF) → 380 KB (MP4) - 91% smaller
- DCM00004: 32 MB (GIF) → 5.4 MB (MP4) - 83% smaller
- DCM00007: 5.6 MB (GIF) → 492 KB (MP4) - 91% smaller

**Recommendation**: Prefer MP4 format for smaller files with same quality

### Metadata Files

Each image has a corresponding `.txt` file containing:
- Patient info: Name, ID, Birth Date, Sex
- Study info: Date, Time, Description
- Equipment info: Manufacturer, Model, Institution
- Image parameters: Dimensions, Bit Depth, Window Settings

## Advanced Options

### Export GIF only, no MP4

```bash
python3 dicom_converter.py --no-mp4
```

### Adjust video frame rate

```bash
# Faster playback
python3 dicom_converter.py --fps 15

# Slower playback
python3 dicom_converter.py --fps 5
```

### 8-bit compatibility mode

```bash
python3 dicom_converter.py --8bit
```

### Custom input/output directories

```bash
python3 dicom_converter.py /path/to/dicom/files -o /path/to/output
```

## Command Line Options

```
usage: dicom_converter.py [-h] [-o OUTPUT] [--8bit] [--no-mp4] [--fps FPS] [input_path]

positional arguments:
  input_path            DICOM file or directory (default: dicom_data)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: output)
  --8bit                Force 8-bit output (default is 16-bit for high precision)
  --no-mp4              Disable MP4 video export (only GIF for animations)
  --fps FPS             Frames per second for GIF and MP4 (default: 10)
```

## FAQ

### If you encounter decompression errors

```bash
pip3 install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg
```

### GIF files too large?

Recommend using MP4 format, which is about 85% smaller. If you don't need GIF, use `--no-mp4` to generate MP4 only.

### Show all options

```bash
python3 dicom_converter.py --help
```

## Technical Details

### DICOM Support

- **Compression**: JPEG Lossless, Non-Hierarchical, First-Order Prediction (Process 14)
- **Modality**: X-Ray Angiography (XA) and other DICOM modalities
- **Photometric**: MONOCHROME1, MONOCHROME2, RGB
- **Frames**: Single-frame and multi-frame sequences

### Conversion Process

1. Reads compressed pixel data using pylibjpeg
2. Applies window/level settings (WindowCenter, WindowWidth) if present
3. Applies RescaleSlope and RescaleIntercept for Hounsfield units
4. Handles MONOCHROME1 (inverted) and MONOCHROME2 photometric interpretation
5. Exports as PNG (16-bit by default), GIF (optimized), and MP4 (H.264 codec)
6. Extracts all DICOM tags to accompanying TXT files

## Requirements

- Python 3.8+
- pydicom >= 2.4.0
- numpy >= 1.24.0, < 2.0
- Pillow >= 10.0.0
- pylibjpeg >= 2.0
- pylibjpeg-libjpeg >= 2.0
- pylibjpeg-openjpeg >= 2.0
- opencv-python >= 4.8.0

## Project Structure

```
.
├── dicom_converter.py          # Main conversion script
├── requirements.txt            # Python dependencies
├── README.md                   # English documentation
├── README_CN.md                # Chinese documentation
├── CLAUDE.md                   # Technical documentation
├── dicom_data/                 # Input DICOM files (default)
│   ├── DCM00000
│   ├── DCM00001
│   └── ...
└── output/                     # Output directory (created by script)
    ├── DCM00000.gif
    ├── DCM00000.mp4
    ├── DCM00000.txt
    └── ...
```

## License

This project is for personal medical record management only, not for diagnosis.

## Version History

**Version 2.0** (2025-11-18)
- ✓ Added MP4 video export feature
- ✓ Optimized GIF compression to reduce file size
- ✓ Added frame rate adjustment option (--fps)
- ✓ Added option to disable MP4 export (--no-mp4)
- ✓ Updated all documentation

**Version 1.0** (2025-11-18)
- ✓ Initial version with PNG/GIF/TXT export
- ✓ Support for JPEG Lossless compressed DICOM
- ✓ Automatic metadata extraction
