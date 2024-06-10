import json
import os

input_files = ["plain/positive.txt",
               "plain/negative.txt",
               "plain/neutral.txt"]

output_files = ["class/positive.json",
                "class/negative.json",
                "class/neutral.json"]

label_map = {"positive.txt": 'positive', "negative.txt": 'negative', "neutral.txt": 'neutral'}
for i, input_file in enumerate(input_files):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    for line in lines:
        line = line.strip()
        if line:
            data.append({'text': line, 'label': label_map[os.path.basename(input_file)]})

    with open(output_files[i], 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
