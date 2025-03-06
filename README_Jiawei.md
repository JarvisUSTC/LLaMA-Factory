## 数据处理流程

将Huggingface上Datasets转换成ShareGPT格式:
```bash
python data/scripts/r1_onevision_system_processing.py --output_dir {path}
```
这里{path}表示数据保存路径，主要是用于将Datasets里的图片编码保存成图片放在一个比较大容量的路径下，运行完之后会得到path/images和path/R1-Onevision-with-System-sharegpt-refine.json

运行一下check.py
```bash
python data/scripts/check.py --input_file {path}/R1-Onevision-with-System-sharegpt-refine.json --output_file data/R1-Onevision-with-System-sharegpt-refine.json
```
运行完之后，json文件会被放到LLaMA-Factory的data目录下，这个json里的图片路径是绝对路径。

Note: 1. 目前数据处理代码里采用的格式是隐式区分system 1和system 2。如果要显式区分，要简单修改下处理代码。2. dataset_info.json里已经注册这个数据集，名字是r1_onevision_w_system

## 训练流程

R1-Onevision的训练超参数:
```bash
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

全参数训练: llamafactory-cli train examples/train_full/qwen25vl_full_sft.yaml
LoRA微调: llamafactory-cli train examples/train_lora/qwen25vl_lora_sft.yaml

wandb的话自己配置一下：
report_to: wandb
run_name: test_run # 可选