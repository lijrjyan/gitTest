#!/bin/bash

# 读取 modelNames.json 文件中的模型名称
modelNamesFile="model_names.json"
if [ ! -f "$modelNamesFile" ]; then
    echo "Error: $modelNamesFile not found!"
    exit 1
fi

pretrained_models=($(jq -r '.[]' $modelNamesFile))

# 定义任务数组
tasks_array=(
    "tinyMMLU"
    "mmlu"
)

# 定义其他参数
device="cuda:1"
batch_size=1

# 遍历 pretrained 模型和任务数组并执行命令
for model in "${pretrained_models[@]}"; do
    all_tasks_success=true

    for task in "${tasks_array[@]}"; do
        output_path="${model//\//_}_${task}/"
        results_file="${output_path}results.json"

        # 检查 results.json 文件是否存在
        if [ -f "$results_file" ]; then
            echo "Results already exist for model ${model} and task ${task}. Skipping execution."
            continue
        fi

        # 定义重试次数
        max_retries=2
        retries=0
        success=false

        # 尝试执行命令，最多重试两次
        while [ $retries -lt $max_retries ]; do
            python eval.py --model hf --model_args pretrained=${model} --tasks ${task} --device ${device} --batch_size ${batch_size} --output_path ${output_path}
            if [ $? -eq 0 ]; then
                success=true
                break
            else
                retries=$((retries+1))
                echo "Command failed for model ${model} and task ${task}. Retry $retries/$max_retries."
            fi
        done

        if [ "$success" = false ]; then
            echo "Command failed for model ${model} and task ${task} after $max_retries attempts. Skipping to next."
            all_tasks_success=false
        fi
    done

    if [ "$all_tasks_success" = true ]; then
        # 删除缓存中的模型文件
        echo "Deleting cache for model ${model}..."
        model_cache_path="${model//\//--}"
        rm -rf ~/.cache/huggingface/hub/models--${model_cache_path}
        echo "Cache for model ${model} deleted."
    fi
done
