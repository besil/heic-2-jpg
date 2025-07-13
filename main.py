import sys
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import pillow_heif
from tqdm.asyncio import tqdm

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

def convert_heic_to_jpg(heic_path, jpg_path):
    """Synchronous conversion function to be run in thread pool"""
    try:
        # Open the HEIC file with Pillow (now supports HEIF after registration)
        image = Image.open(heic_path)
        
        # Convert to RGB if necessary (HEIC might be in different color space)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save as JPEG with high quality, preserving EXIF data
        image.save(jpg_path, "JPEG", quality=100, exif=image.getexif())
        
        # Remove the original HEIC file
        os.remove(heic_path)
        
        return f"Converted and removed: {heic_path} -> {jpg_path}"
    except Exception as e:
        return f"Error converting {heic_path}: {str(e)}"

async def convert_heic_async(heic_path, jpg_path, executor, pbar):
    """Async wrapper for the conversion function"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, convert_heic_to_jpg, heic_path, jpg_path)
    pbar.update(1)  # Update progress bar
    pbar.set_postfix_str(f"Last: {os.path.basename(heic_path)}")
    return result

async def main():
    if len(sys.argv) < 2:
        print("Usage: python heic_to_jpg.py <folder>")
        sys.exit(1)
    folder = sys.argv[1]
    
    # Collect all HEIC files first
    heic_files = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.lower().endswith('.heic'):
                heic_path = os.path.join(root, filename)
                jpg_path = os.path.join(root, os.path.splitext(filename)[0] + '.jpg')
                heic_files.append((heic_path, jpg_path))
    
    if not heic_files:
        print("No HEIC files found in the specified folder.")
        return
    
    print(f"Found {len(heic_files)} HEIC files to convert...")
    
    # Use ThreadPoolExecutor to run conversions concurrently
    # Limit concurrent threads to avoid overwhelming the system
    max_workers = min(8, len(heic_files))
    
    # Create progress bar
    with tqdm(total=len(heic_files), desc="Converting HEIC files", unit="file") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            tasks = [
                convert_heic_async(heic_path, jpg_path, executor, pbar)
                for heic_path, jpg_path in heic_files
            ]
            
            # Run all conversions concurrently
            results = await asyncio.gather(*tasks)
    
    # Print summary of results
    successful = sum(1 for result in results if "Converted and removed:" in result)
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