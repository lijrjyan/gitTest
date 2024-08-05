import json

# 读取处理后的JSON文件
with open('final_deletedOrg.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 处理JSON数据，删除非results键，并将results的内容提升到最上级
processed_data = {}
for key, value in data.items():
    if "results" in value:
        processed_data[key] = value["results"]

# 将处理后的数据写入新的JSON文件
with open('final_directData.json', 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, ensure_ascii=False, indent=4)

print("处理完成，文件已保存为 final_directData.json")
