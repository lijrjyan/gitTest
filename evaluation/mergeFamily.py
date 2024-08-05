import json
from collections import defaultdict
import re

# 定义函数，将模型大小调整成统一的格式
def format_model_size(size_str):
    # 匹配包含数字和可选的小数点后部分的字符串，后面可以跟m或b
    match = re.match(r"(\d+(\.\d+)?)([mbMB]?)", size_str)
    if not match:
        return size_str  # 如果不匹配，返回原始字符串
    
    size, _, unit = match.groups()
    size = float(size)
    
    if unit.lower() == 'm':
        size /= 1000  # 将m转换为B
    elif unit.lower() == 'b':
        size = size  # 保持B单位不变
    # 处理没有单位的情况，假设为B
    formatted_size = f"{size}B"
    
    return formatted_size

# 读取处理后的JSON文件
with open('final_mergedData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 初始化一个字典，用于存储合并后的数据
family_data = defaultdict(dict)

# 遍历数据，将同一个模型family的内容合并
for key, value in data.items():
    parts = key.split('-')
    model_family = "-".join(parts[:-1])  # 获取family名称，不包括最后一个元素
    formatted_size = format_model_size(parts[-1])  # 格式化模型大小
    formatted_key = f"{model_family}-{formatted_size}"
    if model_family not in family_data:
        family_data[model_family] = {}
    family_data[model_family][formatted_key] = value

# 将处理后的数据写入新的JSON文件
with open('final_familyData.json', 'w', encoding='utf-8') as file:
    json.dump(family_data, file, ensure_ascii=False, indent=4)

print("处理完成，文件已保存为 final_familyData.json")
