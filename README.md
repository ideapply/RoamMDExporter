# Roam JSON to Markdown Converter

## Overview
This Python script converts Roam Research JSON files into Markdown format. It supports text formatting, link conversion, and is capable of organizing exported content into structured Markdown files based on Roam's hierarchy. The script can handle custom tags, highlights, tasks, and can restructure content to fit standard Markdown conventions.

## Features
- **Custom Markdown Formatting:** Converts Roam's custom syntax to Markdown, including tasks, highlights, and tags.
- **Link Management:** Can replace online image links with local paths if provided with a mapping file.
- **Content Structuring:** Maintains Roam's hierarchical structure in the Markdown format.
- **Directory Management:** Automatically creates directories and manages files for organized storage.

## Prerequisites
To run this script, you will need:
- Python 3.x
- `json` library (usually included in standard Python installation)
- `os`, `shutil`, `argparse`, `re` libraries (all included in standard Python installation)

## Installation
Clone this repository to your local machine:
```bash
git clone https://github.com/ideapply/roam-json-to-markdown.git
```

## Usage
To convert a Roam Research JSON file into Markdown, run the following command in the terminal:
```bash
python3 roam_json_to_md.py path_to_your_roam_json_file path_to_output_directory
```
Replace path_to_your_roam_json_file with the path to your Roam JSON file, and path_to_output_directory with the path where you want the Markdown files to be saved.
