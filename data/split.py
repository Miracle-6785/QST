import json
import random
import os

# Set the input and output directories
input_dir = 'class'
output_dir = 'section/json'
os.makedirs(output_dir, exist_ok=True)

# Merge the three JSON files
data = []
for file_name in ['negative.json', 'positive.json', 'neutral.json']:
    with open(os.path.join(input_dir, file_name), 'r', encoding='utf-8') as file:
        data.extend(json.load(file))

# Add the 'label_id' field
for item in data:
    if item['label'] == 'positive':
        item['label_id'] = 0
    elif item['label'] == 'negative':
        item['label_id'] = 1
    else:
        item['label_id'] = 2

# Sort the data by label_id
data.sort(key=lambda x: x['label_id'])

# Save the merged data to full.json
with open(os.path.join(output_dir, 'full.json'), 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=3)

print("The merged data has been saved to full.json.")

# Split the data into train and test sets, ensuring equal class distribution in the train set
positive_samples = [item for item in data if item['label_id'] == 0]
negative_samples = [item for item in data if item['label_id'] == 1]
neutral_samples = [item for item in data if item['label_id'] == 2]

train_data = (positive_samples[:int(len(positive_samples) * 0.6)] + negative_samples[:int(len(negative_samples) * 0.6)] + neutral_samples[:int(len(neutral_samples) * 0.6)])
test_data = (positive_samples[int(len(positive_samples) * 0.6):] + negative_samples[int(len(negative_samples) * 0.6):] + neutral_samples[int(len(neutral_samples) * 0.6):])

# Save the train and test sets to JSON files
with open(os.path.join(output_dir, 'train.json'), 'w', encoding='utf-8') as file:
    json.dump(train_data, file, ensure_ascii=False, indent=3)

with open(os.path.join(output_dir, 'test.json'), 'w', encoding='utf-8') as file:
    json.dump(test_data, file, ensure_ascii=False, indent=3)

print("The data has been split into train.json and test.json files with equal class distribution in the train set.")

# Print the number of samples for each label in the train set
train_positive = len([item for item in train_data if item['label_id'] == 0])
train_negative = len([item for item in train_data if item['label_id'] == 1])
train_neutral = len([item for item in train_data if item['label_id'] == 2])

print(f"Train set: Positive samples: {train_positive}, Negative samples: {train_negative}, Neutral samples: {train_neutral}")

# Print the number of samples for each label in the test set
test_positive = len([item for item in test_data if item['label_id'] == 0])
test_negative = len([item for item in test_data if item['label_id'] == 1])
test_neutral = len([item for item in test_data if item['label_id'] == 2])

print(f"Test set: Positive samples: {test_positive}, Negative samples: {test_negative}, Neutral samples: {test_neutral}")