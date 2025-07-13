# HEIC to JPG Converter

A fast, async Python script that converts HEIC (High Efficiency Image Container) files to JPG format while preserving EXIF metadata and automatically cleaning up the original files.

## Features

- 🚀 **Async Processing**: Converts multiple files concurrently for maximum speed
- 📁 **Recursive Directory Scanning**: Automatically finds HEIC/HEIF files in all subdirectories
- 📊 **Progress Bar**: Real-time progress tracking with file count and current file name
- 🔍 **EXIF Preservation**: Maintains original photo metadata in converted JPG files
- 🗑️ **Auto Cleanup**: Removes original HEIC files after successful conversion (optional)
- ⚡ **Configurable Quality**: Adjustable JPEG quality from 1-100%
- 🔧 **Flexible Options**: Command-line arguments for workers, quality, and file extensions
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

### Command Line Options

```bash
uv run main.py [-h] [--workers WORKERS] [--quality QUALITY] [--keep-originals] 
               [--extensions EXTENSIONS [EXTENSIONS ...]] folder
```

**Arguments:**
- `folder`: Path to folder containing HEIC files (searches recursively)

**Options:**
- `-h, --help`: Show help message and exit
- `-w, --workers WORKERS`: Maximum number of concurrent workers (default: 8)
- `-q, --quality [1-100]`: JPEG quality 1-100 (default: 100)
- `-k, --keep-originals`: Keep original HEIC files after conversion
- `--extensions`: File extensions to convert (default: .heic .heif)

### Basic Usage

Convert all HEIC files in a directory (removes originals):

```bash
uv run main.py /path/to/your/photos
```

### Advanced Examples

Convert with custom quality and keep originals:
```bash
uv run main.py /path/to/photos --quality 95 --keep-originals
```

Convert with 4 workers for slower systems:
```bash
uv run main.py /path/to/photos --workers 4
```

Convert both HEIC and HEIF files:
```bash
uv run main.py /path/to/photos --extensions .heic .heif
```

Convert files in current directory:
```bash
uv run main.py .
```

Convert with spaces in folder name:
```bash
uv run main.py "/Users/username/Pictures/My iPhone Photos"
```

Get help:
```bash
uv run main.py --help
```

## How It Works

1. **Scanning**: The script recursively scans the specified directory and all subdirectories for files with specified extensions (default: `.heic`, `.heif`)
2. **Processing**: Found files are processed concurrently using async programming with a configurable thread pool
3. **Converting**: Each HEIC/HEIF file is:
   - Opened and converted to RGB format if necessary
   - Saved as a JPEG with specified quality and preserved EXIF metadata
   - Original file is optionally deleted after successful conversion (default behavior)
4. **Progress**: A real-time progress bar shows conversion status and current file
5. **Summary**: Final report shows successful conversions and any errors encountered

## Performance

- **Configurable Concurrency**: Adjustable number of concurrent workers (default: 8)
- **Optimized for Speed**: Uses thread pools for CPU-intensive operations
- **Memory Efficient**: Processes files individually to avoid memory issues
- **Scalable**: Automatically adjusts worker count based on available files and user preference

## Output Format

- **Format**: JPEG
- **Quality**: Configurable (1-100%, default: 100%)
- **Color Space**: RGB
- **Metadata**: Original EXIF data preserved
- **Naming**: Same filename as original, with `.jpg` extension
- **Original Files**: Removed by default (use `--keep-originals` to preserve)

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

```bash
$ uv run main.py /path/to/photos --quality 95 --workers 4

Found 15 files to convert...
Quality: 95%, Workers: 4, Keep originals: False
Converting files: 100%|████████████| 15/15 [00:23<00:00,  1.52file/s, Last: IMG_1234.heic]

Completed processing 15 files.
Successfully converted: 15
```

```bash
$ uv run main.py --help

usage: main.py [-h] [--workers WORKERS] [--quality [1-100]] [--keep-originals] 
               [--extensions EXTENSIONS [EXTENSIONS ...]] folder

Convert HEIC files to JPG format with EXIF metadata preservation

positional arguments:
  folder                Path to folder containing HEIC files (searches recursively)

options:
  -h, --help            show this help message and exit
  -w, --workers WORKERS
                        Maximum number of concurrent workers (default: 8)
  -q, --quality [1-100]
                        JPEG quality (1-100, default: 100)
  -k, --keep-originals  Keep original HEIC files after conversion
  --extensions EXTENSIONS [EXTENSIONS ...]
                        File extensions to convert (default: .heic .heif)

Examples:
  main.py /path/to/photos                    Convert all HEIC files in directory
  main.py . --workers 4                     Convert with 4 concurrent workers
  main.py /photos --quality 95               Convert with 95% quality
  main.py /photos --keep-originals           Keep original HEIC files
```

## Troubleshooting

### Common Issues

**"No files with extensions [.heic, .heif] found"**
- Check that the directory path is correct
- Ensure files have supported extensions (case-insensitive)
- Verify you have read permissions for the directory
- Try specifying custom extensions with `--extensions`

**"Permission denied"**
- Ensure you have read/write permissions for the target directory
- Try running with appropriate permissions or choose a different directory

**"Import errors" or "libheif not found"**
- Make sure all dependencies are installed: `uv sync`
- On macOS, install libheif: `brew install libheif`
- Verify you're using Python 3.12 or higher

### Performance Tips

- For best performance, run on directories stored on fast storage (SSD)
- Adjust `--workers` based on your system capabilities (default: 8)
- Use lower `--quality` settings for faster processing and smaller file sizes
- Close other resource-intensive applications during batch conversions
- Use `--keep-originals` if you want to preserve source files for safety

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute as needed.

## Changelog

### v0.2.0
- Added argparse for professional command-line interface
- Configurable JPEG quality (1-100%)
- Optional preservation of original files with `--keep-originals`
- Configurable number of worker threads
- Support for custom file extensions
- Enhanced help system with examples
- Improved error messages and validation

### v0.1.0
- Initial release with async processing
- Progress bar implementation
- EXIF metadata preservation
- Recursive directory scanning
- Automatic cleanup of original files