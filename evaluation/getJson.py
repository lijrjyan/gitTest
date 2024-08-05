import os
import json

def read_results_json(folder_path):
    results_file = os.path.join(folder_path, 'results.json')
    if os.path.exists(results_file):
        with open(results_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

def main():
    base_path = os.getcwd()
    final_data = {}

    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            results_content = read_results_json(folder_path)
            if results_content is not None:
                final_data[folder_name] = results_content

    final_json_path = os.path.join(base_path, 'final.json')
    with open(final_json_path, 'w', encoding='utf-8') as final_file:
        json.dump(final_data, final_file, ensure_ascii=False, indent=4)

    print(f'Final JSON file created at: {final_json_path}')

if __name__ == '__main__':
    main()
