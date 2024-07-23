#!/bin/bash

# 定义pretrained模型数组
pretrained_models=(
"openai-community/gpt2"
    "openai-community/gpt2-large"
    "openai-community/gpt2-medium"
    "openai-community/gpt2-xl"
    "EleutherAI/pythia-70m"
    "EleutherAI/pythia-160m"
    "EleutherAI/pythia-410m"
    "EleutherAI/pythia-1b"
    "EleutherAI/pythia-1.4b"
    "EleutherAI/pythia-2.8b"
    "EleutherAI/pythia-6.9b"
    "EleutherAI/pythia-12b"
    "Qwen/Qwen1.5-0.5B"
    "Qwen/Qwen1.5-1.8B"
    "Qwen/Qwen1.5-4B"
    "Qwen/Qwen1.5-7B"
    "Qwen/Qwen1.5-14B"
    "Qwen/Qwen1.5-32B"
    "01-ai/Yi-1.5-6B"
    "01-ai/Yi-1.5-9B"
    "bigscience/bloom-560m"
    "bigscience/bloom-1b1"
    "bigscience/bloom-1b7"
    "bigscience/bloom-3b"
    "bigscience/bloom-7b1"
)

# 定义任务数组
tasks_array=(
    "tinyMMLU"
    "mmlu"
)

# 定义其他参数
device="cuda:1"
batch_size=1

# 遍历pretrained模型和任务数组并执行命令
for model in "${pretrained_models[@]}"; do
    for task in "${tasks_array[@]}"; do
        output_path="${model//\//_}_${task}/"
        results_file="${output_path}results.json"
        
        # 检查results.json文件是否存在
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
        fi
    done
done
