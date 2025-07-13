import sys
import os
import asyncio
import argparse
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import pillow_heif
from tqdm.asyncio import tqdm

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

def convert_heic_to_jpg(heic_path, jpg_path, quality=100, keep_originals=False):
    """Synchronous conversion function to be run in thread pool"""
    try:
        # Open the HEIC file with Pillow (now supports HEIF after registration)
        image = Image.open(heic_path)
        
        # Convert to RGB if necessary (HEIC might be in different color space)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save as JPEG with specified quality, preserving EXIF data
        image.save(jpg_path, "JPEG", quality=quality, exif=image.getexif())
        
        # Remove the original HEIC file unless keeping originals
        action = "Converted"
        if not keep_originals:
            os.remove(heic_path)
            action = "Converted and removed"
        
        return f"{action}: {heic_path} -> {jpg_path}"
    except Exception as e:
        return f"Error converting {heic_path}: {str(e)}"

async def convert_heic_async(heic_path, jpg_path, executor, pbar, quality=100, keep_originals=False):
    """Async wrapper for the conversion function"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor, 
        convert_heic_to_jpg, 
        heic_path, 
        jpg_path, 
        quality, 
        keep_originals
    )
    pbar.update(1)  # Update progress bar
    pbar.set_postfix_str(f"Last: {os.path.basename(heic_path)}")
    return result

async def main():
    parser = argparse.ArgumentParser(
        description='Convert HEIC files to JPG format with EXIF metadata preservation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s /path/to/photos                    Convert all HEIC files in directory
  %(prog)s . --workers 4                     Convert with 4 concurrent workers
  %(prog)s /photos --quality 95               Convert with 95%% quality
  %(prog)s /photos --keep-originals           Keep original HEIC files

The script recursively scans the specified folder and all subfolders for HEIC files.
Original HEIC files are removed after successful conversion unless --keep-originals is used.
        '''
    )
    
    parser.add_argument(
        'folder',
        help='Path to folder containing HEIC files (searches recursively)'
    )
    
    parser.add_argument(
        '--workers', '-w',
        type=int,
        default=8,
        help='Maximum number of concurrent workers (default: 8)'
    )
    
    parser.add_argument(
        '--quality', '-q',
        type=int,
        default=100,
        choices=range(1, 101),
        metavar='[1-100]',
        help='JPEG quality (1-100, default: 100)'
    )
    
    parser.add_argument(
        '--keep-originals', '-k',
        action='store_true',
        help='Keep original HEIC files after conversion'
    )
    
    parser.add_argument(
        '--extensions',
        nargs='+',
        default=['.heic', '.heif'],
        help='File extensions to convert (default: .heic .heif)'
    )
    
    args = parser.parse_args()
    
    # Validate folder path
    if not os.path.exists(args.folder):
        print(f"Error: Folder '{args.folder}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(args.folder):
        print(f"Error: '{args.folder}' is not a directory.")
        sys.exit(1)
    
    # Collect all HEIC files first
    heic_files = []
    extensions = [ext.lower() for ext in args.extensions]
    
    for root, dirs, files in os.walk(args.folder):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in extensions):
                heic_path = os.path.join(root, filename)
                jpg_path = os.path.join(root, os.path.splitext(filename)[0] + '.jpg')
                heic_files.append((heic_path, jpg_path))
    
    if not heic_files:
        ext_list = ', '.join(args.extensions)
        print(f"No files with extensions [{ext_list}] found in '{args.folder}'.")
        return
    
    print(f"Found {len(heic_files)} files to convert...")
    print(f"Quality: {args.quality}%, Workers: {args.workers}, Keep originals: {args.keep_originals}")
    
    # Use ThreadPoolExecutor to run conversions concurrently
    # Limit concurrent threads to avoid overwhelming the system
    max_workers = min(args.workers, len(heic_files))
    
    # Create progress bar
    with tqdm(total=len(heic_files), desc="Converting files", unit="file") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            tasks = [
                convert_heic_async(heic_path, jpg_path, executor, pbar, args.quality, args.keep_originals)
                for heic_path, jpg_path in heic_files
            ]
            
            # Run all conversions concurrently
            results = await asyncio.gather(*tasks)
    
    # Print summary of results
    successful = sum(1 for result in results if "Converted" in result and "Error" not in result)
    errors = len(results) - successful
    
    print(f"\nCompleted processing {len(heic_files)} files.")
    print(f"Successfully converted: {successful}")
    if errors > 0:
        print(f"Errors encountered: {errors}")
        # Print error details
        for result in results:
            if "Error converting" in result:
                print(f"  {result}")

if __name__ == "__main__":
    asyncio.run(main())