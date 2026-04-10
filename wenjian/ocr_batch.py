"""批量OCR：从图片中提取文字，输出到txt文件"""

import os
import re
from paddleocr import PaddleOCR

IMAGE_DIR = "/Users/zhangshenshen/ZCodeProject/wenjian"
OUTPUT_FILE = os.path.join(IMAGE_DIR, "员工手册_提取文字.txt")


def natural_sort_key(s: str) -> list:
    """按文件名中的数字自然排序"""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", s)]


def main():
    ocr = PaddleOCR(use_textline_orientation=True, lang="ch")

    valid_exts = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")
    files = sorted(
        [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(valid_exts)],
        key=natural_sort_key,
    )

    print(f"找到 {len(files)} 张图片，开始处理...")

    all_text = []
    for i, filename in enumerate(files, 1):
        img_path = os.path.join(IMAGE_DIR, filename)
        print(f"[{i}/{len(files)}] {filename}")

        result = ocr.predict(img_path)

        lines = []
        for res in result:
            for text in res["rec_texts"]:
                lines.append(text)

        if lines:
            all_text.append("\n".join(lines))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))

    print(f"\n完成！输出文件：{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
