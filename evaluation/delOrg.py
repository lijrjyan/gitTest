import json

# 读取原始JSON文件
with open('final.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 处理JSON数据，删除下划线前的部分
processed_data = {}
for key in data.keys():
    new_key = "_".join(key.split("_")[1:])
    processed_data[new_key] = data[key]

# 将处理后的数据写入新的JSON文件
with open('final_deletedOrg.json', 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, ensure_ascii=False, indent=4)

