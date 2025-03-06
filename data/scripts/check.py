import json
import argparse

def check_and_add_image_token(filepath, output_filepath):
    """
    检查 ShareGPT JSON 文件中的 <image> token 出现次数，并在需要时添加。

    Args:
        filepath (str): ShareGPT JSON 文件的路径。
        output_filepath (str): 输出 JSON 文件的路径。
    """

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return

    modified_count = 0
    modified_data = []
    print("original length:", len(data))

    for i, item in enumerate(data):
        messages = item["messages"]
        image_token_count = 0
        video_token_count = 0

        for message in messages:
            image_token_count += message["content"].count("<image>")
            video_token_count += message["content"].count("<video>")
        
        if image_token_count > 1 or video_token_count > 0:
            print(messages)
            print("Skip")
            continue

        if image_token_count == 0:
            if messages: #确保messages列表不是空的。
                if "<image>" not in messages[0]["content"]: #确保第一个content里没有<image>
                    messages[0]["content"] = "<image>\n" + messages[0]["content"]
                    modified_count += 1
            else:
                print(f"Warning: messages list is empty in item {i}.")
        
        modified_data.append(item)

    print("modified length:", len(modified_data))

    if modified_count > 0:
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, ensure_ascii=False, indent=2)
        print(f"Added <image> token to {modified_count} items.")
    else:
        print("No items needed modification.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check and modify ShareGPT JSON file.")
    parser.add_argument("--input_file", type=str, required=True, help="Input ShareGPT JSON file path.")
    parser.add_argument("--output_file", type=str, required=True, help="Output ShareGPT JSON file path.")
    args = parser.parse_args()

    check_and_add_image_token(args.input_file, args.output_file)