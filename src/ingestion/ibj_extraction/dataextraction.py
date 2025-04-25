from src.ingestion import ibj_extraction
import json

# Open the JSON file and load it into a dictionary
with open('data.json', 'r') as file:
    d = json.load(file)

# Convert each item in the dictionary to a JSON string with key-value pairs
json_strings = []
for key, value in d.items():
    json_string = f'"{key}" : {json.dumps(value)}'
    json_strings.append(json_string)

print()