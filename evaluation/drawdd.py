import json
import matplotlib.pyplot as plt
import os
import numpy as np

# 读取JSON文件
with open('modified_final_updatedFamilyData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 创建保存图片的目录
output_dir = "line_plots"
os.makedirs(output_dir, exist_ok=True)

# 定义颜色列表
colors = plt.cm.get_cmap('tab10', len(data))

# 定义一个函数，绘制总体图表
def plot_overall(data):
    fig, ax1 = plt.subplots(figsize=(16, 8))  # 增加图像宽度
    color_map = plt.cm.get_cmap('tab10', len(data))

    all_sizes = set()
    size_to_idx = {}

    # 收集所有的size并排序
    for family, models in data.items():
        for size in models.keys():
            all_sizes.add(size)
    
    sorted_sizes = sorted(all_sizes, key=lambda x: float(x[:-1]))

    for idx, size in enumerate(sorted_sizes):
        size_to_idx[size] = idx

    for idx, (family, models) in enumerate(data.items()):
        sizes = []
        deltas = []

        for size, values in sorted(models.items(), key=lambda x: float(x[0][:-1])):  # 按size排序
            if 'delta' in values:
                sizes.append(size)
                deltas.append(values['delta'])  # 计算tinyMMLU - mmlu

        if not sizes or not deltas:
            continue

        x = [size_to_idx[size] for size in sizes]

        # 绘制折线图
        ax1.plot(x, deltas, marker='o', linestyle='-', label=family, color=color_map(idx))


    # 添加文本标签、标题和网格
    ax1.set_xlabel('Size')
    ax1.set_ylabel('Delta (tinyMMLU - mmlu)')
    ax1.set_title('Overall')
    ax1.set_xticks(range(len(sorted_sizes)))
    ax1.set_xticklabels(sorted_sizes, rotation=45)
    ax1.legend()
    ax1.grid(True)

    # 保存图表
    plt.savefig(os.path.join(output_dir, "model_delta_comparison.png"))
    plt.close()

# 绘制总体图表
plot_overall(data)

print(f"图表已保存到 {output_dir} 目录中")
