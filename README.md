# script-utils

This project contains two utility shell scripts for processing files in a directory.

## Files

- **[list-extensions.sh](list-extensions.sh)**  
  Scans a given directory and lists all file extensions found, along with the number of occurrences and percentage of the total.
  
- **[compress-files.sh](compress-files.sh)**  
  Processes video and image files within a directory:
  - Compresses video files (e.g., mp4, mov, mkv) using `ffmpeg`.
  - Compresses image files (e.g., jpg, png, heic) using ImageMagick's `convert`.
  - Logs processing details in `compression.log` and errors in `error.log`.

## Requirements

- **ffmpeg:** Required for video processing.
- **ImageMagick (convert):** Required for image processing.
- Compatible with macOS (uses BSD utilities and options).

## Usage

### list-extensions.sh
```sh
./list-extensions.sh <directory>
