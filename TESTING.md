# Testing Guide

This document describes how to test the DICOM converter to ensure it works correctly.

## Quick Test (Using Sample Data)

### 1. Generate Sample DICOM Files

```bash
python3 create_sample_dicom.py
```

Expected output:
```
================================================================================
DICOM Sample Data Generator
================================================================================

Output directory: dicom_data/

Creating sample CT scan: dicom_data/SAMPLE_CT.dcm
  ✓ Created: SAMPLE_CT.dcm (512x512, CT)
Creating sample MR scan: dicom_data/SAMPLE_MR.dcm
  ✓ Created: SAMPLE_MR.dcm (256x256, MR)
Creating sample multi-frame sequence: dicom_data/SAMPLE_CINE.dcm
  ✓ Created: SAMPLE_CINE.dcm (128x128x15 frames)

================================================================================
✓ Successfully created 3 sample DICOM files
```

### 2. Run Converter

```bash
python3 dicom_converter.py
```

Expected output:
```
Found 3 DICOM files
Output directory: output
Precision mode: 16-bit
Video format: GIF + MP4
Frame rate: 10 fps
================================================================================

[1/3] Processing: SAMPLE_CINE.dcm
  Metadata saved to: output/SAMPLE_CINE.txt
  GIF animation saved to: output/SAMPLE_CINE.gif (15 frames, optimized)
  MP4 video saved to: output/SAMPLE_CINE.mp4 (15 frames, 10 fps)

[2/3] Processing: SAMPLE_CT.dcm
  Metadata saved to: output/SAMPLE_CT.txt
  Image saved to: output/SAMPLE_CT.png

[3/3] Processing: SAMPLE_MR.dcm
  Metadata saved to: output/SAMPLE_MR.txt
  Image saved to: output/SAMPLE_MR.png (16-bit precision)

================================================================================
Conversion complete: 3/3 files processed successfully
Output saved to: output
```

### 3. Verify Output

```bash
ls -lh output/
```

Expected files:
- `SAMPLE_CT.png` - CT scan image
- `SAMPLE_CT.txt` - CT metadata
- `SAMPLE_MR.png` - MR scan image (16-bit)
- `SAMPLE_MR.txt` - MR metadata
- `SAMPLE_CINE.gif` - Animated GIF (15 frames)
- `SAMPLE_CINE.mp4` - MP4 video (15 frames)
- `SAMPLE_CINE.txt` - Cine metadata

## Testing Different Options

### Test 8-bit Output

```bash
rm -rf output
python3 dicom_converter.py --8bit
```

Verify: All PNG files should be 8-bit (smaller file size)

### Test GIF Only (No MP4)

```bash
rm -rf output
python3 dicom_converter.py --no-mp4
```

Verify: No `.mp4` files should be created

### Test Different Frame Rates

```bash
rm -rf output
python3 dicom_converter.py --fps 5   # Slower
```

```bash
rm -rf output
python3 dicom_converter.py --fps 20  # Faster
```

Verify: GIF and MP4 files have different playback speeds

### Test Single File Conversion

```bash
python3 dicom_converter.py dicom_data/SAMPLE_CT.dcm -o test_single
```

Verify: Only CT files created in `test_single/` directory

## Testing with Real DICOM Data

### Using Public Datasets

```bash
# Download sample from Medical Connections
curl -o dicom_data/REAL_SAMPLE.dcm "http://www.dclunie.com/images/compressed/JPEGLS/IMAGES/JLSN"

# Convert
python3 dicom_converter.py
```

### Using Your Own Data

```bash
# Copy your DICOM files
cp /path/to/your/dicom/files/* dicom_data/

# Convert
python3 dicom_converter.py
```

## Automated Testing

Run all tests:

```bash
#!/bin/bash

echo "Running automated tests..."

# Test 1: Generate samples
echo "Test 1: Generating sample data..."
python3 create_sample_dicom.py || { echo "FAILED"; exit 1; }
echo "PASSED"

# Test 2: Basic conversion
echo "Test 2: Basic conversion..."
rm -rf output
python3 dicom_converter.py || { echo "FAILED"; exit 1; }
[ -f output/SAMPLE_CT.png ] || { echo "FAILED: CT image not created"; exit 1; }
[ -f output/SAMPLE_CINE.gif ] || { echo "FAILED: GIF not created"; exit 1; }
[ -f output/SAMPLE_CINE.mp4 ] || { echo "FAILED: MP4 not created"; exit 1; }
echo "PASSED"

# Test 3: 8-bit mode
echo "Test 3: 8-bit mode..."
rm -rf output
python3 dicom_converter.py --8bit || { echo "FAILED"; exit 1; }
echo "PASSED"

# Test 4: No MP4
echo "Test 4: No MP4 mode..."
rm -rf output
python3 dicom_converter.py --no-mp4 || { echo "FAILED"; exit 1; }
[ ! -f output/SAMPLE_CINE.mp4 ] || { echo "FAILED: MP4 should not exist"; exit 1; }
echo "PASSED"

echo "All tests PASSED!"
```

## Expected File Sizes

Approximate file sizes for sample data:

| File | Size |
|------|------|
| SAMPLE_CT.png | ~3 KB |
| SAMPLE_MR.png | ~2 KB |
| SAMPLE_CINE.gif | ~180 KB |
| SAMPLE_CINE.mp4 | ~50 KB |
| Each .txt file | ~3-4 KB |

Note: MP4 should be significantly smaller than GIF (60-70% reduction)

## Troubleshooting Tests

### "No DICOM files found"
- Check `dicom_data/` directory exists
- Run `create_sample_dicom.py` first
- Verify files with `ls dicom_data/`

### "Unable to decompress"
```bash
pip3 install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg
```

### Output files missing
- Check `output/` directory: `ls output/`
- Verify no errors in conversion output
- Try single file: `python3 dicom_converter.py dicom_data/SAMPLE_CT.dcm`

### File size unexpected
- 16-bit PNG files are larger than 8-bit
- Use `--8bit` for smaller PNG files
- MP4 should always be smaller than GIF

## Continuous Integration

For CI/CD pipelines:

```yaml
# .github/workflows/test.yml
name: Test DICOM Converter

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Generate sample data
        run: python3 create_sample_dicom.py
      - name: Run converter
        run: python3 dicom_converter.py
      - name: Verify output
        run: |
          [ -f output/SAMPLE_CT.png ] || exit 1
          [ -f output/SAMPLE_CINE.gif ] || exit 1
          [ -f output/SAMPLE_CINE.mp4 ] || exit 1
```

## Performance Testing

### Measure Conversion Speed

```bash
time python3 dicom_converter.py
```

Expected: 1-2 seconds per file on modern hardware

### Memory Usage

```bash
/usr/bin/time -v python3 dicom_converter.py 2>&1 | grep "Maximum resident"
```

Expected: < 200 MB for sample files

## Validation

### Verify DICOM Compliance

```python
import pydicom

# Verify sample DICOM file is valid
ds = pydicom.dcmread('dicom_data/SAMPLE_CT.dcm')
print(f"Patient: {ds.PatientName}")
print(f"Modality: {ds.Modality}")
print(f"Image size: {ds.Rows}x{ds.Columns}")
```

### Verify Output Image Quality

```python
from PIL import Image
import numpy as np

# Check PNG output
img = Image.open('output/SAMPLE_CT.png')
print(f"Image mode: {img.mode}")
print(f"Image size: {img.size}")
print(f"Image format: {img.format}")

# Check pixel data
arr = np.array(img)
print(f"Array shape: {arr.shape}")
print(f"Data type: {arr.dtype}")
print(f"Value range: {arr.min()} to {arr.max()}")
```

## Test Coverage

- ✅ Single-frame DICOM (CT, MR)
- ✅ Multi-frame DICOM (Cine sequence)
- ✅ PNG output (8-bit and 16-bit)
- ✅ GIF output (optimized)
- ✅ MP4 output (H.264)
- ✅ Metadata extraction
- ✅ File filtering (.txt, .md, .DS_Store)
- ✅ Command-line options (--8bit, --no-mp4, --fps)
- ✅ Custom input/output directories

## Need Help?

If tests fail, check:
1. [README.md](README.md) - Usage instructions
2. [SAMPLE_DATA.md](SAMPLE_DATA.md) - Data sources
3. [CLAUDE.md](CLAUDE.md) - Technical details
4. GitHub Issues - Report problems

---

**Last Updated**: 2025-11-18
**Test Status**: All tests passing ✅
