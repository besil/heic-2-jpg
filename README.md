# HEIC to JPG Converter

A fast, async Python script that converts HEIC (High Efficiency Image Container) files to JPG format while preserving EXIF metadata and automatically cleaning up the original files.

## Features

- 🚀 **Async Processing**: Converts multiple files concurrently for maximum speed
- 📁 **Recursive Directory Scanning**: Automatically finds HEIC files in all subdirectories
- 📊 **Progress Bar**: Real-time progress tracking with file count and current file name
- 🔍 **EXIF Preservation**: Maintains original photo metadata in converted JPG files
- 🗑️ **Auto Cleanup**: Removes original HEIC files after successful conversion
- ⚡ **High Quality**: Saves JPG files at 100% quality
- 🛡️ **Error Handling**: Continues processing even if individual files fail
- 📈 **Summary Report**: Shows conversion statistics and any errors encountered

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- On macOS, install libheif: `brew install libheif` 

### Setup

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:

```bash
uv sync
```

## Usage

### Basic Usage

Convert all HEIC files in a directory:

```bash
uv run main.py /path/to/your/photos
```

### Examples

Convert HEIC files in the current directory:
```bash
uv run main.py .
```

Convert HEIC files in a specific folder:
```bash
uv run main.py /Users/username/Pictures/iPhone-Photos
```

Convert HEIC files in a folder with spaces in the name:
```bash
uv run main.py "/Users/username/Pictures/My iPhone Photos"
```

## How It Works

1. **Scanning**: The script recursively scans the specified directory and all subdirectories for `.heic` files
2. **Processing**: Found files are processed concurrently using async programming with a thread pool
3. **Converting**: Each HEIC file is:
   - Opened and converted to RGB format if necessary
   - Saved as a high-quality JPG with preserved EXIF metadata
   - Original HEIC file is deleted after successful conversion
4. **Progress**: A real-time progress bar shows conversion status
5. **Summary**: Final report shows successful conversions and any errors

## Performance

- **Concurrent Processing**: Up to 8 files are processed simultaneously
- **Optimized for Speed**: Uses thread pools for CPU-intensive operations
- **Memory Efficient**: Processes files individually to avoid memory issues
- **Scalable**: Automatically adjusts worker count based on available files

## Output Format

- **Format**: JPEG
- **Quality**: 100% (maximum quality)
- **Color Space**: RGB
- **Metadata**: Original EXIF data preserved
- **Naming**: Same filename as original, with `.jpg` extension

## Error Handling

The script handles various error scenarios gracefully:

- **Permission Issues**: Continues with other files if one can't be accessed
- **Corrupted Files**: Skips damaged HEIC files and reports errors
- **Disk Space**: Continues processing if individual conversions fail
- **File Conflicts**: Overwrites existing JPG files with the same name

## Dependencies

- **pillow**: Image processing library
- **pillow-heif**: HEIF/HEIC format support for Pillow
- **tqdm**: Progress bar functionality

## Project Structure

```
heic-2-jpg/
├── main.py          # Main conversion script
├── pyproject.toml   # Project configuration and dependencies
├── README.md        # This file
└── uv.lock         # Dependency lock file
```

## Example Output

```
Found 15 HEIC files to convert...
Converting HEIC files: 100%|████████████| 15/15 [00:23<00:00,  1.52file/s, Last: IMG_1234.heic]

Completed processing 15 files.
Successfully converted: 15
```

## Troubleshooting

### Common Issues

**"No HEIC files found"**
- Check that the directory path is correct
- Ensure HEIC files have `.heic` extension (case-insensitive)
- Verify you have read permissions for the directory

**"Permission denied"**
- Ensure you have read/write permissions for the target directory
- Try running with appropriate permissions or choose a different directory

**"Import errors"**
- Make sure all dependencies are installed: `uv sync`
- Verify you're using Python 3.12 or higher

### Performance Tips

- For best performance, run on directories stored on fast storage (SSD)
- Close other resource-intensive applications during batch conversions
- The script automatically limits concurrent workers to prevent system overload

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute as needed.

## Changelog

### v0.1.0
- Initial release with async processing
- Progress bar implementation
- EXIF metadata preservation
- Recursive directory scanning
- Automatic cleanup of original files