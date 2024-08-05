import os
import json
import re

def extract_and_convert_size(key):
    size_pattern = re.compile(r'(\d+(\.\d+)?)([bm])', re.IGNORECASE)
    match = size_pattern.search(key)
    if match:
        value, _, unit = match.groups()
        value = float(value)
        if unit.lower() == 'm':
            value /= 1000
        return f"{value}B"
    return None

def process_keys(results):
    new_results = {}
    for key, value in results.items():
        parts = key.split('_')
        if len(parts) == 3:
            model = parts[1]
            task = parts[2]
            new_key = f"{model}_{task}"
            new_results[new_key] = value

            # Extract and convert size
            converted_size = extract_and_convert_size(key)
            if converted_size:
                new_results[new_key]['size'] = converted_size
            else:
                new_results[new_key]['size'] = "NA"
        else:
            new_results[key] = value
            new_results[key]['size'] = "NA"
    return new_results

def add_size_labels(final_data):
    for folder, content in final_data.items():
        results = content.get('results', {})
        new_results = process_keys(results)
        final_data[folder]['results'] = new_results

def main():
    base_path = os.getcwd()
    final_json_path = os.path.join(base_path, 'final.json')

    # Load final.json
    with open(final_json_path, 'r', encoding='utf-8') as final_file:
        final_data = json.load(final_file)

    # Add size labels
    add_size_labels(final_data)

    # Save the updated final.json
    with open(final_json_path, 'w', encoding='utf-8') as final_file:
        json.dump(final_data, final_file, ensure_ascii=False, indent=4)

    print(f'Updated final JSON file created at: {final_json_path}')

if __name__ == '__main__':
    main()
