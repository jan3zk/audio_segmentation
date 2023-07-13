# Concatenate Audio Segments

This is a Python script that reads information about audio segments from a text file, downloads corresponding audio files, and then concatenates them into one mp3 file. The resulting mp3 files are saved in a specified output folder.

## Features

- Parses and processes audio segments
- Downloads audio files from given links
- Concatenates multiple audio files into one
- Stores concatenated audio in a specified output folder

## Requirements

This script requires the following Python libraries installed:

- os
- requests
- pydub
- BeautifulSoup4
- argparse

To install these requirements, use pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the script, use the following command:

```bash
python concatenate_segments.py segment_file output_folder
```

Where:
- `segment_file` is a text file that contains information about the audio segments to be concatenated.
- `output_folder` is the directory where the concatenated mp3 files will be saved. If the directory doesn't exist, the script will create it.

## Example

```bash
python concatenate_segments.py IRISS_new-segments-with-original-segments.txt ./concatenated_audio
```

## How it works

The script works in the following steps:
- Reads the `segment_file` to get information about the audio segments.
- Finds the corresponding mp3 file links using BeautifulSoup.
- Downloads the mp3 files using the requests library.
- Concatenates the audio files using pydub.
- Saves the concatenated audio files in the specified `output_folder`.
