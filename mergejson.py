import json
from pathlib import Path

def merge_json_folder_with_context(input_folder, output_file):
    # Initialize an empty dictionary for the merged content
    merged_data = {}

    # Get all JSON files in the input folder
    json_files = list(Path(input_folder).glob("*.json"))

    for idx, file_path in enumerate(json_files):
        # Load each JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {file_path}")
                continue

            for key, value in data.items():
                # Add context by recording the source file
                source_key = f"from_file_{file_path.name}"

                if key in merged_data:
                    # Handle existing key
                    if isinstance(merged_data[key], dict) and isinstance(value, dict):
                        # Merge nested dictionaries with context
                        for sub_key, sub_value in value.items():
                            if sub_key in merged_data[key]:
                                # Add source metadata for conflicts
                                merged_data[key][sub_key] = {
                                    source_key: sub_value,
                                    **merged_data[key][sub_key],
                                }
                            else:
                                merged_data[key][sub_key] = {source_key: sub_value}
                    else:
                        # Convert existing value to a dict with context if it's not already
                        if not isinstance(merged_data[key], dict):
                            merged_data[key] = {
                                f"from_file_{json_files.index(file_path) + 1}": merged_data[key]
                            }
                        # Add new conflicting value
                        merged_data[key][source_key] = value
                else:
                    # New key, add with source context
                    merged_data[key] = {source_key: value}

    # Write the merged data to the output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(merged_data, out_file, indent=4, ensure_ascii=False)

    print(f"Context-aware merged JSON saved to {output_file}")

# Specify the folder containing JSON files and the output file name
input_folder = "JSONOutput"  # Replace with the folder path containing JSON files
output_file = "merged_with_context.json"  # Specify the output file

# Run the merge function
merge_json_folder_with_context(input_folder, output_file)
