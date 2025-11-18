#!/usr/bin/env python3
"""
Create Sample DICOM Files for Testing
Generates synthetic DICOM files with various characteristics for testing the converter.
"""

import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
from datetime import datetime
from pathlib import Path


def create_sample_ct(output_path):
    """Create a sample CT scan DICOM file"""
    print(f"Creating sample CT scan: {output_path}")

    # Create a 512x512 synthetic CT image
    rows, cols = 512, 512
    pixel_array = np.zeros((rows, cols), dtype=np.int16)

    # Add some structures (simple geometric shapes to simulate anatomy)
    # Circle (like a skull)
    y, x = np.ogrid[-rows//2:rows//2, -cols//2:cols//2]
    mask = x**2 + y**2 <= 200**2
    pixel_array[mask] = 1000  # Bone-like density

    # Inner circle (like brain)
    mask_inner = x**2 + y**2 <= 180**2
    pixel_array[mask_inner] = 50  # Soft tissue

    # Some details (simulated ventricles)
    mask_detail1 = (x-50)**2 + (y-30)**2 <= 20**2
    mask_detail2 = (x+50)**2 + (y-30)**2 <= 20**2
    pixel_array[mask_detail1] = 0
    pixel_array[mask_detail2] = 0

    # Create DICOM dataset
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT Image Storage
    file_meta.MediaStorageSOPInstanceUID = '1.2.3.4.5.6.7.8.9.1'
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'  # Implicit VR Little Endian
    file_meta.ImplementationClassUID = '1.2.3.4.5.6.7.8.9.0'

    ds = FileDataset(output_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Patient Information (anonymized)
    ds.PatientName = "Sample^Patient"
    ds.PatientID = "SAMPLE001"
    ds.PatientBirthDate = "19800101"
    ds.PatientSex = "O"  # Other (anonymized)

    # Study Information
    ds.StudyDate = datetime.now().strftime('%Y%m%d')
    ds.StudyTime = datetime.now().strftime('%H%M%S')
    ds.StudyDescription = "Sample CT Study"
    ds.StudyInstanceUID = '1.2.3.4.5.6.7.8.9.10.11'

    # Series Information
    ds.SeriesDescription = "Sample CT Series"
    ds.SeriesInstanceUID = '1.2.3.4.5.6.7.8.9.10.11.12'
    ds.SeriesNumber = 1
    ds.Modality = "CT"

    # Image Information
    ds.InstanceNumber = 1
    ds.ImageType = ["ORIGINAL", "PRIMARY", "AXIAL"]
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID

    # Technical parameters
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.Rows = rows
    ds.Columns = cols
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 1  # Signed

    # CT-specific parameters
    ds.RescaleIntercept = -1024
    ds.RescaleSlope = 1
    ds.WindowCenter = 40
    ds.WindowWidth = 400

    # Equipment
    ds.Manufacturer = "Sample DICOM Generator"
    ds.ManufacturerModelName = "Synthetic CT v1.0"
    ds.InstitutionName = "Sample Medical Center"

    # Pixel Data
    ds.PixelData = pixel_array.tobytes()

    # Save
    ds.save_as(output_path, write_like_original=False)
    print(f"  ✓ Created: {output_path.name} ({rows}x{cols}, CT)")


def create_sample_mr(output_path):
    """Create a sample MR scan DICOM file"""
    print(f"Creating sample MR scan: {output_path}")

    # Create a 256x256 synthetic MR image
    rows, cols = 256, 256
    pixel_array = np.zeros((rows, cols), dtype=np.uint16)

    # Add some structures (T2-weighted appearance)
    y, x = np.ogrid[-rows//2:rows//2, -cols//2:cols//2]

    # Brain outline
    mask = x**2 + y**2 <= 100**2
    pixel_array[mask] = 3000

    # Gray matter (brighter in T2)
    mask_gray = (x**2 + y**2 <= 90**2) & (x**2 + y**2 > 50**2)
    pixel_array[mask_gray] = 4000

    # White matter (darker in T2)
    mask_white = x**2 + y**2 <= 50**2
    pixel_array[mask_white] = 2000

    # CSF (very bright in T2)
    mask_csf = (x-30)**2 + (y-20)**2 <= 15**2
    pixel_array[mask_csf] = 5000

    # Create DICOM dataset
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'  # MR Image Storage
    file_meta.MediaStorageSOPInstanceUID = '1.2.3.4.5.6.7.8.9.2'
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
    file_meta.ImplementationClassUID = '1.2.3.4.5.6.7.8.9.0'

    ds = FileDataset(output_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Patient Information
    ds.PatientName = "Sample^Patient"
    ds.PatientID = "SAMPLE002"
    ds.PatientBirthDate = "19850101"
    ds.PatientSex = "O"

    # Study Information
    ds.StudyDate = datetime.now().strftime('%Y%m%d')
    ds.StudyTime = datetime.now().strftime('%H%M%S')
    ds.StudyDescription = "Sample MR Study"
    ds.StudyInstanceUID = '1.2.3.4.5.6.7.8.9.10.21'

    # Series Information
    ds.SeriesDescription = "Sample T2 Brain"
    ds.SeriesInstanceUID = '1.2.3.4.5.6.7.8.9.10.21.22'
    ds.SeriesNumber = 2
    ds.Modality = "MR"

    # Image Information
    ds.InstanceNumber = 1
    ds.ImageType = ["ORIGINAL", "PRIMARY", "T2", "NONE"]
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID

    # Technical parameters
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.Rows = rows
    ds.Columns = cols
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0  # Unsigned

    # MR-specific parameters
    ds.WindowCenter = 2500
    ds.WindowWidth = 5000

    # Equipment
    ds.Manufacturer = "Sample DICOM Generator"
    ds.ManufacturerModelName = "Synthetic MR v1.0"
    ds.InstitutionName = "Sample Medical Center"

    # Pixel Data
    ds.PixelData = pixel_array.tobytes()

    # Save
    ds.save_as(output_path, write_like_original=False)
    print(f"  ✓ Created: {output_path.name} ({rows}x{cols}, MR)")


def create_sample_multiframe(output_path, num_frames=10):
    """Create a sample multi-frame DICOM file (for animation)"""
    print(f"Creating sample multi-frame sequence: {output_path}")

    # Create animated sequence (like a beating heart or pulsing vessel)
    rows, cols = 128, 128
    frames = []

    for frame_idx in range(num_frames):
        pixel_array = np.zeros((rows, cols), dtype=np.uint8)

        # Pulsating circle (simulates heart or vessel)
        radius = 30 + 10 * np.sin(2 * np.pi * frame_idx / num_frames)
        y, x = np.ogrid[-rows//2:rows//2, -cols//2:cols//2]
        mask = x**2 + y**2 <= radius**2
        pixel_array[mask] = 200

        # Add some background texture
        noise = np.random.randint(0, 20, (rows, cols), dtype=np.uint8)
        pixel_array = np.clip(pixel_array + noise, 0, 255).astype(np.uint8)

        frames.append(pixel_array)

    # Stack frames
    pixel_array_multi = np.array(frames, dtype=np.uint8)

    # Create DICOM dataset
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.7'  # Secondary Capture
    file_meta.MediaStorageSOPInstanceUID = '1.2.3.4.5.6.7.8.9.3'
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
    file_meta.ImplementationClassUID = '1.2.3.4.5.6.7.8.9.0'

    ds = FileDataset(output_path, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Patient Information
    ds.PatientName = "Sample^Patient"
    ds.PatientID = "SAMPLE003"
    ds.PatientBirthDate = "19900101"
    ds.PatientSex = "O"

    # Study Information
    ds.StudyDate = datetime.now().strftime('%Y%m%d')
    ds.StudyTime = datetime.now().strftime('%H%M%S')
    ds.StudyDescription = "Sample Multi-frame Study"
    ds.StudyInstanceUID = '1.2.3.4.5.6.7.8.9.10.31'

    # Series Information
    ds.SeriesDescription = "Sample Cine Sequence"
    ds.SeriesInstanceUID = '1.2.3.4.5.6.7.8.9.10.31.32'
    ds.SeriesNumber = 3
    ds.Modality = "OT"  # Other

    # Image Information
    ds.InstanceNumber = 1
    ds.ImageType = ["ORIGINAL", "PRIMARY"]
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID

    # Multi-frame specific
    ds.NumberOfFrames = num_frames

    # Technical parameters
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.Rows = rows
    ds.Columns = cols
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0  # Unsigned

    # Window/Level
    ds.WindowCenter = 128
    ds.WindowWidth = 256

    # Equipment
    ds.Manufacturer = "Sample DICOM Generator"
    ds.ManufacturerModelName = "Synthetic Multi-frame v1.0"
    ds.InstitutionName = "Sample Medical Center"

    # Pixel Data (all frames)
    ds.PixelData = pixel_array_multi.tobytes()

    # Save
    ds.save_as(output_path, write_like_original=False)
    print(f"  ✓ Created: {output_path.name} ({rows}x{cols}x{num_frames} frames)")


def main():
    """Generate all sample DICOM files"""
    print("=" * 80)
    print("DICOM Sample Data Generator")
    print("=" * 80)
    print()

    # Create dicom_data directory
    dicom_data_dir = Path("dicom_data")
    dicom_data_dir.mkdir(exist_ok=True)
    print(f"Output directory: {dicom_data_dir}/")
    print()

    # Create sample files
    try:
        create_sample_ct(dicom_data_dir / "SAMPLE_CT.dcm")
        create_sample_mr(dicom_data_dir / "SAMPLE_MR.dcm")
        create_sample_multiframe(dicom_data_dir / "SAMPLE_CINE.dcm", num_frames=15)

        print()
        print("=" * 80)
        print("✓ Successfully created 3 sample DICOM files")
        print()
        print("Next steps:")
        print("  1. Run: python3 dicom_converter.py")
        print("  2. Check output/ directory for results")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ Error creating sample files: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
