import json
import matplotlib.pyplot as plt
import os
import numpy as np

# 创建保存图片的目录
output_dir = "visualizations"
os.makedirs(output_dir, exist_ok=True)

# 读取处理后的JSON文件
with open('final_updatedFamilyData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 定义一个函数，绘制图表
def plot_data(family, models):
    sizes = []
    mmlu_accs = []
    tinyMMLU_accs = []

    for model, values in models.items():
        size = model.split('-')[-1]
        sizes.append(size)
        mmlu_accs.append(values.get('mmlu', {}).get('acc,none', None))
        tinyMMLU_accs.append(values.get('tinyMMLU', {}).get('acc,none', None))

    x = np.arange(len(sizes))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 定义颜色
    bar_color1 = 'darkblue'
    line_color1 = 'blue'
    bar_color2 = 'darkorange'
    line_color2 = 'orange'

    # 绘制条形图
    bars1 = ax1.bar(x - width/2, mmlu_accs, width, label='mmlu', color=bar_color1)
    bars2 = ax1.bar(x + width/2, tinyMMLU_accs, width, label='tinyMMLU', color=bar_color2)

    # 绘制线型图
    ax1.plot(x, mmlu_accs, marker='o', linestyle='-', color=line_color1)
    ax1.plot(x, tinyMMLU_accs, marker='o', linestyle='-', color=line_color2)

    # 添加文本标签、标题和网格
    ax1.set_xlabel('Size')
    ax1.set_ylabel('Accuracy')
    ax1.set_title(f'{family}')
    ax1.set_xticks(x)
    ax1.set_xticklabels(sizes)
    ax1.legend(handles=[bars1, bars2])
    ax1.grid(True)

    # 保存图表
    plt.savefig(os.path.join(output_dir, f"{family}.png"))
    plt.close()

# 遍历数据，为每个条目绘制图表
for family, models in data.items():
    plot_data(family, models)

print(f"图表已保存到 {output_dir} 目录中")
