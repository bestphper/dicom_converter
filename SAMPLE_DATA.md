# Sample DICOM Data

This document explains how to obtain sample DICOM files for testing the converter.

## Option 1: Use Public DICOM Sample Data (Recommended)

### Free DICOM Sample Datasets

1. **Medical Connections** (Recommended)
   - URL: https://www.mcguffin.com/dicom/sample-dicom-files
   - Various modalities including CT, MR, US, XA
   - Free download, no registration required

2. **OsiriX DICOM Sample Image Sets**
   - URL: https://www.osirix-viewer.com/resources/dicom-image-library/
   - High-quality medical imaging samples
   - Multiple modalities and anatomies

3. **TCIA (The Cancer Imaging Archive)**
   - URL: https://www.cancerimagingarchive.net/
   - Large collection of medical imaging data
   - Requires registration (free)

4. **Pydicom Sample Data**
   - Included with pydicom installation
   - Location: `pydicom.data.get_testdata_file()`
   - Small but useful for testing

### Quick Start with Sample Data

```python
# Download sample DICOM files using pydicom
import pydicom
from pydicom.data import get_testdata_files

# Get list of sample DICOM files
sample_files = get_testdata_files()
print(f"Found {len(sample_files)} sample files")

# Copy to dicom_data directory
import shutil
from pathlib import Path

dicom_data_dir = Path("dicom_data")
dicom_data_dir.mkdir(exist_ok=True)

for i, file_path in enumerate(sample_files[:10]):  # Copy first 10 files
    dest = dicom_data_dir / f"SAMPLE_{i:03d}.dcm"
    shutil.copy(file_path, dest)
    print(f"Copied: {dest.name}")
```

## Option 2: Generate Synthetic DICOM Files

Use the provided script to create sample DICOM files for testing:

```bash
python3 create_sample_dicom.py
```

This will create:
- `dicom_data/SAMPLE_001.dcm` - Single-frame CT image (512x512)
- `dicom_data/SAMPLE_002.dcm` - Single-frame MR image (256x256)
- `dicom_data/SAMPLE_003.dcm` - Multi-frame sequence (10 frames, 128x128)

## Option 3: Download from Medical Connections

Quick download command (requires curl):

```bash
# Create dicom_data directory
mkdir -p dicom_data

# Download sample CT scan
curl -o dicom_data/SAMPLE_CT.dcm "http://www.dclunie.com/images/compressed/JPEGLS/IMAGES/JLSN"

# Download sample MR scan
curl -o dicom_data/SAMPLE_MR.dcm "http://www.dclunie.com/images/compressed/JPEGLS/IMAGES/JLSI"
```

## Testing the Converter

Once you have sample data in `dicom_data/`:

```bash
# View available files
ls dicom_data/

# Run converter
python3 dicom_converter.py

# Check output
ls output/
```

## Important Notes

### Privacy & Ethics
- ⚠️ **Never use real patient data without proper authorization**
- ✅ Use anonymized sample data for testing
- ✅ Public datasets have appropriate consents

### Data Formats
- This converter supports most DICOM formats
- Best tested with: CT, MR, XA, US modalities
- Handles both compressed (JPEG Lossless) and uncompressed DICOM

### File Naming
- Sample files can have any name
- Common extensions: `.dcm`, `.dicom`, or no extension
- The converter auto-detects DICOM format

## Troubleshooting

### "No DICOM files found"
- Ensure files are in `dicom_data/` directory
- Check file permissions (must be readable)
- Verify files are actually DICOM format

### "Unable to decompress"
- Install compression libraries:
  ```bash
  pip3 install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg
  ```

### "No pixel data found"
- Some DICOM files contain only metadata (e.g., DICOMDIR)
- Try different sample files

## Example Workflow

```bash
# 1. Create directory
mkdir -p dicom_data

# 2. Get sample data (choose one method)
python3 create_sample_dicom.py

# 3. Run converter
python3 dicom_converter.py

# 4. View results
ls -lh output/
open output/SAMPLE_001.png
```

## Resources

- **DICOM Standard**: https://www.dicomstandard.org/
- **Pydicom Documentation**: https://pydicom.github.io/
- **Sample Datasets**: https://github.com/pydicom/pydicom/tree/main/pydicom/data/test_files

---

**Need Help?**
- Check [README.md](README.md) for general usage
- See [CLAUDE.md](CLAUDE.md) for technical details
- Open an issue on GitHub
