import json
import os

# Directory containing the JSON files
directory = 'JSONOutput'  # Adjust the path as needed

# Initialize the merged data structure
merged_data = []

# Iterate over all JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):  # Ensure only JSON files are processed
        file_path = os.path.join(directory, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
                data = json.load(file)
                merged_data.append(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {filename}: {e}")
        except UnicodeDecodeError as e:
            print(f"Encoding error in {filename}: {e}")

# Save the aggregated data to a single JSON file
output_file = 'merged_data.json'
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile, indent=4, ensure_ascii=False)  # Ensure proper encoding

print(f"Merged JSON saved to '{output_file}'")
