import json
import os

# 读取处理后的JSON文件
with open('final_updatedFamilyData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 定义一个函数，进行数据修改
def modify_data(d):
    modified_data = {}
    for family, models in d.items():
        new_models = {}
        for model, values in models.items():
            size = model.split('-')[-1]
            new_values = {}
            if 'mmlu' in values and 'tinyMMLU' in values:
                mmlu_acc = values['mmlu'].get('acc,none', 'N/A')
                tinyMMLU_acc = values['tinyMMLU'].get('acc,none', 'N/A')
                if mmlu_acc != 'N/A' and tinyMMLU_acc != 'N/A':
                    delta =  tinyMMLU_acc - mmlu_acc
                else:
                    delta = 'N/A'
                new_values['mmlu'] = {'acc': mmlu_acc}
                new_values['tinyMMLU'] = {'acc': tinyMMLU_acc}
                new_values['delta'] = delta
            new_models[size] = new_values
        modified_data[family] = new_models
    return modified_data

# 修改数据
modified_data = modify_data(data)

# 将处理后的数据写入新的JSON文件
with open('modified_final_updatedFamilyData.json', 'w', encoding='utf-8') as file:
    json.dump(modified_data, file, ensure_ascii=False, indent=4)

print("处理完成，文件已保存为 modified_final_updatedFamilyData.json")
