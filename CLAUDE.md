# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains DICOM (Digital Imaging and Communications in Medicine) medical imaging data and a Python script to convert these files into standard image and video formats (PNG, GIF, MP4).

## Directory Structure

- `dicom_data/` - Contains the original DICOM files from the medical imaging CD
  - `DCM00000` through `DCM00037` - DICOM medical imaging files (X-ray angiography)
  - `DICOMDIR` - DICOM directory file
  - `DicomViewer.exe`, `DcmRead.dll` - Original Windows viewer software (not used)

- `dicom_converter.py` - Main conversion script
- `requirements.txt` - Python dependencies
- `README.md` - English documentation
- `README_CN.md` - Chinese documentation
- `output/` - Default output directory (created by script)

## Setup and Installation

### Install Dependencies

```bash
pip3 install -r requirements.txt
```

**Important**: The script requires `pylibjpeg` libraries to decode JPEG Lossless compressed DICOM files. If you encounter decompression errors, ensure all dependencies are installed.

## Usage

### Convert All DICOM Files

By default, converts all DICOM files in the `dicom_data` directory:

```bash
python3 dicom_converter.py
```

This creates an `output/` directory with:
- PNG images (for single-frame DICOMs)
- GIF animations and MP4 videos (for multi-frame DICOMs)
- TXT files containing metadata (same base name as images)

### Convert Specific Files

```bash
python3 dicom_converter.py dicom_data/DCM00000 -o custom_output
```

### Options

- `-o, --output` - Specify output directory (default: `output`)
- `--8bit` - Force 8-bit output instead of 16-bit for high-precision data
- `--no-mp4` - Disable MP4 video export (only GIF for animations)
- `--fps` - Frames per second for GIF and MP4 output (default: 10)

### Examples

```bash
# Convert all files with 8-bit output
python3 dicom_converter.py --8bit

# Convert single file to specific directory
python3 dicom_converter.py dicom_data/DCM00001 -o my_images

# Only export GIF, no MP4
python3 dicom_converter.py --no-mp4

# Adjust frame rate to 15 fps
python3 dicom_converter.py --fps 15

# Show help
python3 dicom_converter.py --help
```

## Technical Details

### DICOM File Format

The DICOM files in this project are:
- **Modality**: X-Ray Angiography (XA)
- **Compression**: JPEG Lossless, Non-Hierarchical, First-Order Prediction (Process 14)
- **Type**: Mix of single-frame images and multi-frame animations
- **Patient**: Medical records for patient HU LIANG
- **Institution**: Beijing Chaoyang Hospital
- **Equipment**: Philips AlluraXper

### Conversion Process

1. **Pixel Array Extraction**: Reads compressed pixel data using pylibjpeg
2. **Normalization**: Applies window/level settings (WindowCenter, WindowWidth) if present
3. **Rescaling**: Applies RescaleSlope and RescaleIntercept for Hounsfield units
4. **Photometric Interpretation**: Handles MONOCHROME1 (inverted) and MONOCHROME2
5. **Output Format**:
   - Single-frame → PNG (16-bit by default, 8-bit with `--8bit`)
   - Multi-frame → GIF animation (optimized, default 10 fps) + MP4 video (H.264, default 10 fps)
6. **Metadata**: Extracts all DICOM tags to accompanying TXT files

### Image and Video Quality

- **PNG**: By default uses 16-bit for high-precision medical data, preserves original pixel value ranges
- **GIF**: 8-bit with optimized compression to reduce file size
- **MP4**: H.264 codec, grayscale, produces files ~85% smaller than GIF
- Use `--8bit` flag for 8-bit PNG output if needed for compatibility
- Use `--fps` to adjust video playback speed (default: 10 fps)

## Metadata Extraction

Each image has a corresponding `.txt` file containing:
- **Key Information**: Patient details, study info, image parameters
- **Complete DICOM Header**: All DICOM tags and values

Example metadata fields:
- Patient Name, ID, Birth Date, Sex
- Study Date/Time, Description
- Modality, Institution, Equipment
- Image dimensions, bit depth, window settings
- Transfer syntax, compression info

## Common Tasks

### View Conversion Results

```bash
# List output files
ls -lh output/

# Count output files
ls output/*.png 2>/dev/null | wc -l  # Static images
ls output/*.gif 2>/dev/null | wc -l  # GIF animations
ls output/*.mp4 2>/dev/null | wc -l  # MP4 videos

# Compare file sizes
du -h output/DCM00001.gif output/DCM00001.mp4

# View metadata for specific file
cat output/DCM00000.txt | head -30
```

### Troubleshooting

**Error: "Unable to decompress... missing dependencies"**
- Install JPEG decompression libraries: `pip3 install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg`

**Error: "No pixel data found"**
- Some DICOM files (like DICOMDIR) don't contain images, only metadata

**Numpy version conflicts**
- Use `numpy>=1.24.0,<2.0` to avoid compatibility issues with pylibjpeg

**GIF files too large**
- MP4 files are ~85% smaller than GIF (e.g., 4.2MB GIF → 380KB MP4)
- Use `--no-mp4` if you only need one format
- Adjust `--fps` to reduce file size (lower fps = smaller files)

## File Naming Convention

Output files follow this pattern:
- `DCM00000.png` - Static image
- `DCM00000.gif` - GIF animation (multi-frame)
- `DCM00000.mp4` - MP4 video (multi-frame)
- `DCM00000.txt` - Metadata

Names match the original DICOM file names for easy correlation.

## Performance Notes

From testing on 34 DICOM files:
- **Total output**: 12 PNG images, 22 GIF animations, 22 MP4 videos, 34 metadata files (90 files total)
- **File size comparison**:
  - GIF total: ~196 MB
  - MP4 total: ~29 MB
  - MP4 saves ~85% disk space compared to GIF
- **Processing time**: ~1-2 seconds per file on modern hardware
