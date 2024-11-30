# wiki-fandom-scraper

Here’s a README file for your script:

---

# MediaWiki to JSON Scraper

This script fetches content from a MediaWiki-based site (e.g., One Piece Fandom Wiki) using its API. It extracts and processes page data, including templates and sections, and saves the results as structured JSON files.

---

## Features

- Fetches the latest revision of pages specified in a text file.
- Handles special characters and spaces in page titles.
- Extracts templates and sections from MediaWiki content.
- Saves the parsed data into individual JSON files with sanitized filenames.

---

## Prerequisites

### Python Modules:
Ensure you have the following Python modules installed:
- `requests`: For making API requests.
- `mwparserfromhell`: For parsing MediaWiki content.
- `re`: For sanitizing filenames (part of Python's standard library).

Install the required modules using `pip`:
```bash
pip install requests mwparserfromhell
```

---

## Input File

The script reads page titles from a text file (`test.txt`). Each line in the file should contain one page title. Example:

### `test.txt`
```plaintext
Battaman
Monkey D. Luffy
"Gang" Bege's Oh My Family
4Kids Entertainment/Episode List and DVD Releases
```

---

## Usage

1. **Clone or Copy the Script**:
   Save the script as `mediawiki_scraper.py`.

2. **Prepare the Input File**:
   Create a text file named `test.txt` with the page titles you want to scrape.

3. **Run the Script**:
   Execute the script in a terminal or command prompt:
   ```bash
   python mediawiki_scraper.py
   ```

4. **Output**:
   The JSON files will be saved in the same directory with filenames based on the page titles. Invalid characters in filenames (e.g., `/`, `?`, `:`) are replaced with underscores.

---

## Output Structure

Each JSON file contains:
- **Metadata**:
  - `page_id`: The page's unique ID.
  - `title`: The page's title.
  - `url`: The URL of the original page.
- **Templates**: Extracted data from templates (e.g., infoboxes).
- **Sections**: Plain text content organized by section headings.

### Example Output:
```json
{
    "metadata": {
        "page_id": "123456",
        "title": "Monkey D. Luffy",
        "url": "https://onepiece.fandom.com/wiki/Monkey_D._Luffy"
    },
    "templates": {
        "Infobox": {
            "name": "Monkey D. Luffy",
            "alias": "Straw Hat Luffy"
        }
    },
    "sections": {
        "Lead": "Monkey D. Luffy is a pirate...",
        "Appearance": "Luffy is a young man with..."
    }
}
```

---

## Error Handling

- If a page cannot be retrieved or has no content, the script logs a message and skips to the next page.
- Filenames with invalid characters are sanitized.

---

## Notes

- Ensure your input file (`test.txt`) contains valid page titles from the target MediaWiki site.
- The script fetches content from the **latest revision** of each page.
- Modify the `base_url` variable to point to a different MediaWiki API if needed.

---

## Customization

### Change Input File:
Modify the filename in this section to use a different input file:
```python
with open("test.txt", "r", encoding="utf-8") as file:
```

### Save Output to a Directory:
To save JSON files to a specific directory:
```python
output_dir = "output_json"
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.join(output_dir, f"parsed_output_{sanitize_filename(formatted_name)}.json")
```

---

## License

This script is open-source and can be modified or redistributed under the MIT License.

---

Let me know if you’d like additional customization or if anything is unclear! 🚀
