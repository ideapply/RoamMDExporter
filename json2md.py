#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


def load_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load JSON file: {file_path}. Error: {str(e)}")
        sys.exit(1)


def write_markdown_file(file_path, content):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Failed to write Markdown file: {file_path}. Error: {str(e)}")
        sys.exit(1)


def replace_links_with_paths(roam_json, firebase_local_records):
    for page in roam_json:
        children = page.get("children", [])
        replace_links_in_blocks(children, firebase_local_records)


def replace_links_in_blocks(blocks, firebase_local_records):
    for block in blocks:
        content = block.get("string", "")
        for link, path in firebase_local_records.items():
            content = content.replace(link, path)
        block["string"] = content

        children = block.get("children", [])
        replace_links_in_blocks(children, firebase_local_records)

def has_text_content(page):
    blocks = page.get("children", [])

    for block in blocks:
        content = block.get("string", "").strip()
        if content:
            return True

    return False

def roam_page_to_markdown(page):
    blocks = page.get("children", [])
    markdown = ""
    
    for block in blocks:
        markdown += roam_block_to_markdown(block)
    
    return markdown.strip()

def roam_block_to_markdown(block, indent=0):
    content = block.get("string", "").replace("\n", " ")

    content = content.replace("^^", "==")  # Highlight
    content = content.replace("__", "_")  # Italicize

    children = block.get("children", [])

    heading = block.get("heading", None)
    if heading == 1:
        prefix = "# "
    elif heading == 2:
        prefix = "## "
    elif heading == 3:
        prefix = "### "
    else:
        prefix = "  " * indent + "- "

    markdown = f"{prefix}{content}\n"
    
    for child in children:
        markdown += roam_block_to_markdown(child, indent + 1)

    if indent == 0:
        markdown = markdown.lstrip("- ").rstrip("\n") + "\n"
    
    # Check if content starts with '> ', if so, add an extra newline character
    if content.startswith("> "):
        markdown += "\n"

# If content starts with '**' or '![', replace '- ' at the start of markdown with '  '
    if content.startswith("**") or content.startswith("!["):
#        markdown = markdown.replace("- ", "", 1)
        markdown = markdown.lstrip("- ").rstrip("\n") + "\n"        
        
    return markdown


def main(input_file, output_dir):
    temp_dir = str(output_dir).replace("roam_file", "roam_image")
    firebase_local_records_file = os.path.join(temp_dir, "firebase_local_records.json")

    roam_json = load_json_file(input_file)
    firebase_local_records = load_json_file(firebase_local_records_file)
    
    # URL to Path
    replace_links_with_paths(roam_json, firebase_local_records)

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for page in roam_json:
        if not has_text_content(page):
            continue

        markdown = roam_page_to_markdown(page)

        title = page.get("title").replace("/", "／")
        output_file = os.path.join(output_dir, f"{title}.md")

        write_markdown_file(output_file, markdown)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Roam Research JSON data to Markdown format")
    parser.add_argument("input_file", help="Path to Roam Research JSON file")
    parser.add_argument("output_dir", help="Directory to store the converted Markdown files")
    args = parser.parse_args()

    main(args.input_file, args.output_dir)
