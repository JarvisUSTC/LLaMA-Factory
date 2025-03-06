## 数据处理流程

### 将 Hugging Face Datasets 转换为 ShareGPT 格式

```bash
python data/scripts/r1_onevision_system_processing.py --output_dir {path}
```

* `{path}`: 数据保存路径。此路径用于存储从 Datasets 中提取并保存的图像。
* 运行完成后，将在 `{path}` 目录下生成 `images` 文件夹（包含保存的图像）和 `R1-Onevision-with-System-sharegpt-refine.json` 文件。

### 运行 `check.py`

```bash
python data/scripts/check.py --input_file {path}/R1-Onevision-with-System-sharegpt-refine.json --output_file data/R1-Onevision-with-System-sharegpt-refine.json
```

* 此步骤将生成的 JSON 文件移动到 LLaMA-Factory 的 `data` 目录下。
* 请注意，此 JSON 文件中的图像路径为绝对路径。

**注意：**

1.  目前数据处理代码隐式区分 system 1 和 system 2。如需显式区分，请修改处理代码。
2.  数据集已在 `dataset_info.json` 中注册，名称为 `r1_onevision_w_system`。

## 训练流程

### R1-Onevision 训练超参数

```yaml
image_resolution: 512
cutoff_len: 8192
per_device_train_batch_size: 1
gradient_accumulation_steps: 16
learning_rate: 1.0e-5
num_train_epochs: 1.0
lr_scheduler_type: cosine
warmup_ratio: 0.05
bf16: true
flash_attn: fa2
```

### 训练命令

* **全参数训练：**

    ```bash
    llamafactory-cli train examples/train_full/qwen25vl_full_sft.yaml
    ```

* **LoRA 微调：**

    ```bash
    llamafactory-cli train examples/train_lora/qwen25vl_lora_sft.yaml
    ```

### Wandb 配置

请根据需要配置 Wandb：

```yaml
report_to: wandb
run_name: test_run # 可选
```
