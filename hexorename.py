import os
import re
import yaml
import sys
def rename_hexo_post(filepath):
    """
    Renames a Hexo post from YYYY-MM-DD-old.md to YYYY-MM-DD-title.md
    while preserving Chinese, Japanese, and Korean characters.
    """
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return

    filename = os.path.basename(filepath)
    directory = os.path.dirname(filepath)

    # 1. Extract the YYYY-MM-DD date prefix
    date_match = re.match(r'^(\d{4}-\d{2}-\d{2})', filename)
    if not date_match:
        print(f"Skipping {filename}: No YYYY-MM-DD prefix found.")
        return
    date_prefix = date_match.group(1)

    try:
        # 2. Read file with UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 3. Extract Front-matter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not fm_match:
            print(f"Skipping {filename}: No front matter found.")
            return

        front_matter = yaml.safe_load(fm_match.group(1))
        title = front_matter.get('title')

        if not title:
            print(f"Skipping {filename}: Title field is empty.")
            return

        # 4. Universal Sanitization
        # Remove only illegal filename characters: \ / : * ? " < > |
        clean_title = re.sub(r'[\\/:*?"<>|]', '', str(title))
        # Replace spaces and multiple hyphens with a single hyphen
        clean_title = re.sub(r'\s+', '-', clean_title).strip('-')

        # 5. Execute Rename
        new_filename = f"{date_prefix}-{clean_title}.md"
        new_filepath = os.path.join(directory, new_filename)

        if filepath == new_filepath:
            print(f"No change needed for: {filename}")
            return
        if os.path.exists(new_filepath) and filepath != new_filepath:
            print(f"Error: Target filename already exists: {new_filename}")
            return
        os.rename(filepath, new_filepath)
        print(f"Renamed: {filename} -> {new_filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # sys.argv[1:] captures all arguments after the script name
    files = sys.argv[1:]

    if not files:
        print("Usage: hexorename <file1.md> <file2.md> ...")
    else:
        for filepath in files:
            rename_hexo_post(filepath)
