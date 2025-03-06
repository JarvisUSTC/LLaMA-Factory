import base64
import io
import os
from PIL import Image
from datasets import DatasetDict, Dataset, load_dataset
import json
from tqdm import tqdm
import argparse

def convert_to_sharegpt(dataset_dict, output_dir):
    """
    将 DatasetDict 转换为 ShareGPT 格式，并处理图像和对话。

    Args:
        dataset_dict (DatasetDict): 包含训练数据的 DatasetDict。
        output_dir (str): 保存 ShareGPT 数据的目录。
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    image_dir = os.path.join(output_dir, "images")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    train_dataset = dataset_dict["train"]
    sharegpt_data = []

    for i, example in tqdm(enumerate(train_dataset)):
        messages = []
        images = []

        # 处理图像
        image_base64 = example["image"]
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            if image.mode == "RGBA" or image.mode == "P":
                image = image.convert("RGB")  # 将RGBA和P转换为RGB

            image_filename = f"image_{i}.jpg"
            image_path = os.path.join(image_dir, image_filename)
            image.save(image_path, "JPEG") #明确指定保存格式为JPEG。
            images.append(image_path)
        except Exception as e:
            print(f"Error processing image {i}: {e}")
            continue  # 跳过错误图像

        # 处理对话
        conversations = example["conversations"]

        for conversation in conversations:
            messages.append({"role": conversation["from"], "content": conversation["value"]})

        # 处理 system_choose 和 system_1_reasoning/system_1_answer
        if example["system_choose"] == "1":
            reasoning = example["system_1_reasoning"]
            answer = example["system_1_answer"]
            if len(messages) > 0 and messages[-1]["role"] == "assistant":
                messages[-1]["content"] = f"<think>\n{reasoning}\n</think>\n<answer>\n{answer}\n</answer>"

        image_token_count = 0
        video_token_count = 0

        for message in messages:
            image_token_count += message["content"].count("<image>")
            video_token_count += message["content"].count("<video>")

        if image_token_count > 1 or video_token_count > 0:
            print(f"Warning: More than one <image> token found in conversations {i}.")
            continue #跳过该数据

        if image_token_count == 0:
            messages[0]["content"] = "<image>\n" + messages[0]["content"]

        sharegpt_data.append({"messages": messages, "images": images})

    # 保存 ShareGPT 数据
    output_file = os.path.join(output_dir, "R1-Onevision-with-System-sharegpt-refine.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sharegpt_data, f, ensure_ascii=False, indent=2)

    print(f"ShareGPT data saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert dataset to ShareGPT format.")
    parser.add_argument("--output_dir", type=str, default="/opt/dlami/nvme/data/R1-Onevision-with-System-sharegpt_data/", help="Output directory for ShareGPT data.")
    args = parser.parse_args()

    ds = load_dataset("Jarvis1111/R1-Onevision-with-System")
    convert_to_sharegpt(ds, args.output_dir)