import json
import re

# 定义函数，提取大小用于排序
def extract_size(size_str):
    match = re.match(r"(\d+(\.\d+)?)(B)", size_str)
    if match:
        size, _, _ = match.groups()
        return float(size)
    return float(size_str)

# 读取处理后的JSON文件
with open('final_familyData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 初始化一个字典，用于存储排序后的数据
sorted_family_data = {}

# 对每个family的数据按大小排序
for family, models in data.items():
    sorted_models = dict(sorted(models.items(), key=lambda x: extract_size(x[0].split('-')[-1])))
    sorted_family_data[family] = sorted_models

# 将处理后的数据写入新的JSON文件
with open('final_sortedFamilyData.json', 'w', encoding='utf-8') as file:
    json.dump(sorted_family_data, file, ensure_ascii=False, indent=4)

print("处理完成，文件已保存为 final_sortedFamilyData.json")
