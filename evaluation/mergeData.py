import json
from collections import defaultdict

# 读取处理后的JSON文件
with open('final_directData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 初始化一个字典，用于存储合并后的数据
merged_data = defaultdict(dict)

# 遍历数据，将相同模型的不同任务合并
for key, value in data.items():
    model_name = key.split('_')[0]
    for sub_key, sub_value in value.items():
        merged_data[model_name][sub_key] = sub_value

# 将处理后的数据写入新的JSON文件
with open('final_mergedData.json', 'w', encoding='utf-8') as file:
    json.dump(merged_data, file, ensure_ascii=False, indent=4)

print("处理完成，文件已保存为 final_mergedData.json")
