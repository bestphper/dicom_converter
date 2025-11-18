#!/usr/bin/env python3
"""
DICOM to Image Converter
Converts DICOM medical imaging files to PNG/GIF/MP4 and extracts metadata to text files.
"""

import os
import sys
from pathlib import Path
import pydicom
from pydicom.errors import InvalidDicomError
import numpy as np
from PIL import Image
import argparse
import cv2


def normalize_pixel_array(pixel_array, window_center=None, window_width=None):
    """
    Normalize pixel array to 0-255 range for image display.
    Applies windowing if window center and width are provided.
    """
    if window_center is not None and window_width is not None:
        # Apply window/level adjustment
        lower = window_center - window_width / 2
        upper = window_center + window_width / 2
        pixel_array = np.clip(pixel_array, lower, upper)
        pixel_array = ((pixel_array - lower) / (upper - lower) * 255.0).astype(np.uint8)
    else:
        # Auto-scale to full range
        pixel_array = pixel_array.astype(np.float64)
        pixel_min = pixel_array.min()
        pixel_max = pixel_array.max()

        if pixel_max > pixel_min:
            pixel_array = ((pixel_array - pixel_min) / (pixel_max - pixel_min) * 255.0)

        pixel_array = pixel_array.astype(np.uint8)

    return pixel_array


def extract_metadata(ds, output_txt_path):
    """
    Extract DICOM metadata and save to text file.
    """
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("DICOM Metadata\n")
        f.write("=" * 80 + "\n\n")

        # Extract key patient and study information
        important_tags = [
            'PatientName', 'PatientID', 'PatientBirthDate', 'PatientSex',
            'StudyDate', 'StudyTime', 'StudyDescription', 'SeriesDescription',
            'Modality', 'InstitutionName', 'Manufacturer', 'ManufacturerModelName',
            'ImageComments', 'StudyComments', 'SeriesNumber', 'InstanceNumber',
            'ImageType', 'PhotometricInterpretation', 'SamplesPerPixel',
            'Rows', 'Columns', 'BitsAllocated', 'BitsStored',
            'WindowCenter', 'WindowWidth', 'RescaleIntercept', 'RescaleSlope'
        ]

        f.write("Key Information:\n")
        f.write("-" * 80 + "\n")
        for tag in important_tags:
            if hasattr(ds, tag):
                value = getattr(ds, tag)
                f.write(f"{tag}: {value}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("Complete DICOM Header:\n")
        f.write("=" * 80 + "\n\n")
        f.write(str(ds))


def convert_dicom_to_image(dicom_path, output_dir, preserve_precision=True, export_mp4=True, fps=10):
    """
    Convert a DICOM file to PNG image(s), GIF animation, and/or MP4 video.

    Args:
        dicom_path: Path to DICOM file
        output_dir: Directory to save output files
        preserve_precision: If True, use 16-bit PNG for high precision data
        export_mp4: If True, export multi-frame sequences as MP4 video
        fps: Frames per second for video output

    Returns:
        True if successful, False otherwise
    """
    try:
        # Read DICOM file
        ds = pydicom.dcmread(dicom_path)

        # Get base filename without extension
        base_name = Path(dicom_path).stem
        output_base = Path(output_dir) / base_name

        # Extract metadata
        output_txt = f"{output_base}.txt"
        extract_metadata(ds, output_txt)
        print(f"  Metadata saved to: {output_txt}")

        # Check if DICOM has pixel data
        if not hasattr(ds, 'pixel_array'):
            print(f"  Warning: No pixel data found in {dicom_path}")
            return False

        # Get pixel array
        pixel_array = ds.pixel_array

        # Get window center and width if available
        window_center = getattr(ds, 'WindowCenter', None)
        window_width = getattr(ds, 'WindowWidth', None)

        # Handle multiple window values (take first)
        if isinstance(window_center, (list, pydicom.multival.MultiValue)):
            window_center = float(window_center[0])
        elif window_center is not None:
            window_center = float(window_center)

        if isinstance(window_width, (list, pydicom.multival.MultiValue)):
            window_width = float(window_width[0])
        elif window_width is not None:
            window_width = float(window_width)

        # Apply rescale slope and intercept if present
        if hasattr(ds, 'RescaleSlope') and hasattr(ds, 'RescaleIntercept'):
            pixel_array = pixel_array * float(ds.RescaleSlope) + float(ds.RescaleIntercept)

        # Check if multi-frame (animation)
        if len(pixel_array.shape) > 2 and pixel_array.shape[0] > 1:
            # Multi-frame image - save as GIF and MP4
            frames_pil = []
            frames_np = []

            for i in range(pixel_array.shape[0]):
                frame = pixel_array[i]
                normalized_frame = normalize_pixel_array(frame, window_center, window_width)

                # Handle photometric interpretation
                if hasattr(ds, 'PhotometricInterpretation'):
                    if ds.PhotometricInterpretation == "MONOCHROME1":
                        # Invert for MONOCHROME1
                        normalized_frame = 255 - normalized_frame

                frames_pil.append(Image.fromarray(normalized_frame, mode='L'))
                frames_np.append(normalized_frame)

            # Save as animated GIF with optimization
            output_gif = f"{output_base}.gif"
            frames_pil[0].save(
                output_gif,
                save_all=True,
                append_images=frames_pil[1:],
                duration=int(1000 / fps),  # Convert fps to duration in ms
                loop=0,
                optimize=True,  # Enable optimization to reduce file size
                disposal=2  # Clear frame before next frame (reduces size for medical images)
            )
            print(f"  GIF animation saved to: {output_gif} ({len(frames_pil)} frames, optimized)")

            # Save as MP4 video
            if export_mp4:
                output_mp4 = f"{output_base}.mp4"
                height, width = frames_np[0].shape

                # Define codec and create VideoWriter object
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_mp4, fourcc, fps, (width, height), isColor=False)

                for frame in frames_np:
                    out.write(frame)

                out.release()
                print(f"  MP4 video saved to: {output_mp4} ({len(frames_np)} frames, {fps} fps)")

        else:
            # Single frame image
            if len(pixel_array.shape) > 2:
                pixel_array = pixel_array[0]

            # Normalize pixel array
            normalized_array = normalize_pixel_array(pixel_array, window_center, window_width)

            # Handle photometric interpretation
            if hasattr(ds, 'PhotometricInterpretation'):
                if ds.PhotometricInterpretation == "MONOCHROME1":
                    # Invert for MONOCHROME1
                    normalized_array = 255 - normalized_array

            # Create PIL Image
            if hasattr(ds, 'SamplesPerPixel') and ds.SamplesPerPixel == 3:
                # Color image
                if len(normalized_array.shape) == 2:
                    img = Image.fromarray(normalized_array, mode='L')
                else:
                    img = Image.fromarray(normalized_array, mode='RGB')
            else:
                # Grayscale image
                img = Image.fromarray(normalized_array, mode='L')

            # Save as PNG (supports high bit depth if needed)
            output_png = f"{output_base}.png"

            # For high precision data, optionally save as 16-bit PNG
            if preserve_precision and pixel_array.dtype in [np.int16, np.uint16, np.int32, np.uint32]:
                # Save original pixel range as 16-bit
                pixel_16bit = pixel_array.astype(np.float64)
                pixel_min = pixel_16bit.min()
                pixel_max = pixel_16bit.max()

                if pixel_max > pixel_min:
                    pixel_16bit = ((pixel_16bit - pixel_min) / (pixel_max - pixel_min) * 65535.0)

                pixel_16bit = pixel_16bit.astype(np.uint16)

                if hasattr(ds, 'PhotometricInterpretation') and ds.PhotometricInterpretation == "MONOCHROME1":
                    pixel_16bit = 65535 - pixel_16bit

                img_16bit = Image.fromarray(pixel_16bit, mode='I;16')
                img_16bit.save(output_png)
                print(f"  Image saved to: {output_png} (16-bit precision)")
            else:
                img.save(output_png)
                print(f"  Image saved to: {output_png}")

        return True

    except InvalidDicomError:
        print(f"  Error: {dicom_path} is not a valid DICOM file")
        return False
    except Exception as e:
        print(f"  Error processing {dicom_path}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert DICOM files to PNG/GIF/MP4 and extract metadata'
    )
    parser.add_argument(
        'input_path',
        nargs='?',
        default='dicom_data',
        help='DICOM file or directory containing DICOM files (default: dicom_data)'
    )
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='Output directory (default: output)'
    )
    parser.add_argument(
        '--8bit',
        action='store_true',
        help='Force 8-bit output (default is 16-bit for high precision data)'
    )
    parser.add_argument(
        '--no-mp4',
        action='store_true',
        help='Disable MP4 video export (only GIF for animations)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=10,
        help='Frames per second for GIF and MP4 output (default: 10)'
    )

    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_dir = Path(args.output)
    preserve_precision = not args.__dict__['8bit']
    export_mp4 = not args.no_mp4
    fps = args.fps

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Collect DICOM files
    dicom_files = []
    if input_path.is_file():
        dicom_files = [input_path]
    elif input_path.is_dir():
        # Find all DICOM files (skip DICOMDIR and non-DICOM files)
        skip_extensions = {'.exe', '.dll', '.inf', '.txt', '.md', '.py', '.DS_Store', '.db'}
        for file_path in sorted(input_path.iterdir()):
            if file_path.is_file() and file_path.name != 'DICOMDIR':
                # Skip known non-DICOM files
                if any(file_path.name.endswith(ext) for ext in skip_extensions) or file_path.name.startswith('.'):
                    continue
                dicom_files.append(file_path)
    else:
        print(f"Error: {input_path} does not exist")
        sys.exit(1)

    if not dicom_files:
        print("No DICOM files found")
        sys.exit(1)

    print(f"Found {len(dicom_files)} DICOM files")
    print(f"Output directory: {output_dir}")
    print(f"Precision mode: {'16-bit' if preserve_precision else '8-bit'}")
    print(f"Video format: {'GIF + MP4' if export_mp4 else 'GIF only'}")
    print(f"Frame rate: {fps} fps")
    print("=" * 80)

    # Process each file
    success_count = 0
    for i, dicom_file in enumerate(dicom_files, 1):
        print(f"\n[{i}/{len(dicom_files)}] Processing: {dicom_file.name}")
        if convert_dicom_to_image(dicom_file, output_dir, preserve_precision, export_mp4, fps):
            success_count += 1

    print("\n" + "=" * 80)
    print(f"Conversion complete: {success_count}/{len(dicom_files)} files processed successfully")
    print(f"Output saved to: {output_dir}")


if __name__ == '__main__':
    main()
