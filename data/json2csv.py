import json
import os
import csv

# Set the input and output directories
input_dir = 'section/json'
output_dir = 'section/csv'
os.makedirs(output_dir, exist_ok=True)

# Convert the JSON files to CSV files
for file_name in ['full.json', 'train.json', 'test.json']:
    input_file = os.path.join(input_dir, file_name)
    output_file = os.path.join(output_dir, file_name.replace('.json', '.csv'))

    with open(input_file, 'r', encoding='utf-8') as json_file, open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        data = json.load(json_file)
        writer = csv.writer(csv_file)

        # Write the header row
        writer.writerow(data[0].keys())

        # Write the data rows
        for item in data:
            writer.writerow(item.values())

    print(f"Converted {file_name} to {file_name.replace('.json', '.csv')}")