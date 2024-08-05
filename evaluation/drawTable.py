import json
import os

# 读取处理后的JSON文件
with open('final_updatedFamilyData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 创建保存LaTeX表格的目录
output_dir = "latex_tables"
os.makedirs(output_dir, exist_ok=True)

# 定义一个函数，生成LaTeX表格
def generate_latex_table(family, models):
    table_content = "\\begin{table}[h!]\n\\centering\n\\begin{tabular}{|c|c|c|}\n\\hline\n"
    table_content += "Model Size & mmlu Acc & tinyMMLU Acc \\\\ \n\\hline\n"
    
    for model, values in models.items():
        size = model.split('-')[-1]
        mmlu_acc = values.get('mmlu', {}).get('acc,none', 'N/A')
        tinyMMLU_acc = values.get('tinyMMLU', {}).get('acc,none', 'N/A')
        table_content += f"{size} & {mmlu_acc} & {tinyMMLU_acc} \\\\ \n\\hline\n"
    
    table_content += "\\end{tabular}\n\\caption{Accuracy Comparison for " + family + "}\n\\end{table}\n"
    
    return table_content

# 遍历数据，为每个条目生成LaTeX表格
for family, models in data.items():
    latex_table = generate_latex_table(family, models)
    
    with open(os.path.join(output_dir, f"{family}_table.tex"), 'w', encoding='utf-8') as file:
        file.write(latex_table)

print(f"LaTeX表格已保存到 {output_dir} 目录中")
