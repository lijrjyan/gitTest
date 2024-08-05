import json

# 定义一个递归函数，遍历并修改第三级条目中的键名
def rename_keys(d):
    if isinstance(d, dict):
        for key, value in d.items():
            if isinstance(value, dict):
                if key == "tinyMMLU":
                    if "acc_norm" in value:
                        value["acc"] = value.pop("acc_norm")
                    if "acc_norm_stderr" in value:
                        value["acc_stderr"] = value.pop("acc_norm_stderr")
                else:
                    rename_keys(value)

# 读取处理后的JSON文件
with open('final_sortedFamilyData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 调用递归函数修改键名
rename_keys(data)

# 将处理后的数据写入新的JSON文件
with open('final_updatedFamilyData.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("处理完成，文件已保存为 final_updatedFamilyData.json")
