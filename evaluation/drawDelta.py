import json
import matplotlib.pyplot as plt
import os
import numpy as np

with open('modified_final_updatedFamilyData.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

output_dir = "delta_visualization"
os.makedirs(output_dir, exist_ok=True)

colors = plt.cm.get_cmap('tab10', len(data))

def plot_data(family, models):
    sizes = []
    deltas = []

    for size, values in sorted(models.items(), key=lambda x: float(x[0][:-1])):
        if 'delta' in values:
            sizes.append(size)
            deltas.append(values['delta'])

    if not sizes or not deltas:
        return

    fig, ax1 = plt.subplots(figsize=(14, 6))

    x = np.arange(len(sizes))

    # 绘制折线图
    ax1.plot(x, deltas, marker='o', linestyle='-', color='blue', label='delta')

    # 添加文本标签、标题和网格
    ax1.set_xlabel('Size')
    ax1.set_ylabel('Delta (tinyMMLU - mmlu)')
    ax1.set_title(f'{family}')
    ax1.set_xticks(x)
    ax1.set_xticklabels(sizes, rotation=45)
    ax1.legend()
    ax1.grid(True)

    # 保存图表
    plt.savefig(os.path.join(output_dir, f"{family}_delta_comparison.png"))
    plt.close()

# 定义一个函数，绘制总体图表
def plot_overall(data):
    fig, ax1 = plt.subplots(figsize=(16, 8))  # 增加图像宽度

    for idx, (family, models) in enumerate(data.items()):
        sizes = []
        deltas = []

        for size, values in sorted(models.items(), key=lambda x: float(x[0][:-1])):  # 按size排序
            if 'delta' in values:
                sizes.append(size)
                deltas.append(-values['delta'])  # 计算tinyMMLU - mmlu

        if not sizes or not deltas:
            continue

        x = np.arange(len(sizes))

        # 绘制折线图
        ax1.plot(x, deltas, marker='o', linestyle='-', label=family, color=colors(idx))

    # 添加文本标签、标题和网格
    ax1.set_xlabel('Size')
    ax1.set_ylabel('Delta (tinyMMLU - mmlu)')
    ax1.set_title('Overall Delta Comparison')
    ax1.set_xticks(np.arange(len(sizes)))
    ax1.set_xticklabels(sizes, rotation=45)
    ax1.legend()
    ax1.grid(True)

    # 保存图表
    plt.savefig(os.path.join(output_dir, "overall_delta_comparison.png"))
    plt.close()

# 遍历数据，为每个条目绘制图表
for family, models in data.items():
    plot_data(family, models)

# 绘制总体图表
plot_overall(data)

print(f"图表已保存到 {output_dir} 目录中")
