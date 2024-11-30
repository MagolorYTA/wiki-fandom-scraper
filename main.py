import requests
import mwparserfromhell
import json
from urllib.parse import quote
import re
import os
import logging

# Configure logging
logging.basicConfig(
    filename="error_log.txt",  # Log file name
    level=logging.ERROR,       # Log only errors and critical issues
    format="%(asctime)s - %(levelname)s - %(message)s"  # Log format
)

# Function to sanitize file names
def sanitize_filename(filename):
    """Replaces invalid characters in file names with an underscore."""
    return re.sub(r'[\/:*?"<>|]', '_', filename)

# Helper function to recursively parse and resolve nested templates
def resolve_nested_templates(value, wikicode):
    if "{{" in value and "}}" in value:
        nested_code = mwparserfromhell.parse(value)
        resolved_data = {}
        template_count = {}

        for template in nested_code.filter_templates():
            template_name = str(template.name).strip()
            # Handle multiple occurrences of the same template
            if template_name not in template_count:
                template_count[template_name] = 1
            else:
                template_count[template_name] += 1

            template_key = f"{template_name}_{template_count[template_name]}"  # Unique key
            template_data = {}
            for param in template.params:
                key = str(param.name).strip()
                value = str(param.value).strip()
                template_data[key] = resolve_nested_templates(value, wikicode)  # Recursive parsing
            resolved_data[template_key] = template_data
        return resolved_data

    # Handle [[Links]] and [[Zoan#Artificial Zoan|Artificial Zoan]]
    if "[[" in value and "]]" in value:
        parsed_code = mwparserfromhell.parse(value)
        return parsed_code.strip_code()  # Extract readable text

    return value  # Return original value if no nested template or link

# Load page names from a file
with open("page_names.txt", "r", encoding="utf-8") as file:
    page_names = [line.strip() for line in file if line.strip()]

# Ensure output directory exists
output_dir = "output_json"
os.makedirs(output_dir, exist_ok=True)

# Base API URL
base_url = "https://onepiece.fandom.com/api.php"

for page_name in page_names:
    # Replace spaces with underscores and encode special characters for the MediaWiki API
    formatted_name = quote(page_name.replace(" ", "_"))

    # Build the API URL for the current page
    api_url = f"{base_url}?action=query&prop=revisions&titles={formatted_name}&rvprop=content&format=json"

    print(f"Fetching data for page: {page_name}")
    print(f"API URL: {api_url}")

    try:
        # Get JSON Response
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()

        # Check if the page has valid data
        if "query" not in data or "pages" not in data["query"]:
            logging.error(f"No data found for page: {page_name}")
            continue

        pages = data['query']['pages']
        for page_id, page_content in pages.items():
            if 'revisions' not in page_content:
                logging.error(f"No revisions found for page: {page_name}")
                continue

            # Extract the `*` field from the first revision
            content = page_content['revisions'][0].get('*', '')

            # Parse the MediaWiki content
            wikicode = mwparserfromhell.parse(content)

            # Extract templates into JSON-friendly format
            templates_data = {}
            for template in wikicode.filter_templates():
                template_name = str(template.name).strip()
                template_data = {}
                for param in template.params:
                    key = str(param.name).strip()
                    value = str(param.value).strip()
                    # Resolve nested templates
                    template_data[key] = resolve_nested_templates(value, wikicode)
                templates_data[template_name] = template_data

            # Extract plain text sections
            sections_data = {}
            for heading in wikicode.get_sections(include_lead=True, flat=True):
                section_title = heading.filter_headings()[0].title.strip() if heading.filter_headings() else "Lead"
                sections_data[section_title] = heading.strip_code()

            # Combine everything into a single JSON structure
            parsed_output = {
                "metadata": {
                    "page_id": page_id,
                    "title": page_content.get("title", "Unknown"),
                    "url": f"https://onepiece.fandom.com/wiki/{formatted_name}"
                },
                "templates": templates_data,
                "sections": sections_data,
            }

            # Convert to JSON
            json_output = json.dumps(parsed_output, indent=4, ensure_ascii=False)

            # Sanitize the file name and save the JSON output
            output_filename = os.path.join(output_dir, f"{sanitize_filename(formatted_name)}.json")
            with open(output_filename, "w", encoding="utf-8") as json_file:
                json_file.write(json_output)

            print(f"Data saved to: {output_filename}")

    except requests.exceptions.RequestException as req_err:
        logging.error(f"HTTP request error for page: {page_name} - {req_err}")
    except Exception as e:
        logging.error(f"Error while processing page: {page_name} - {e}")
