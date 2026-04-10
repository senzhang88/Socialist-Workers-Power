"""清理OCR输出：去除水印、乱码，保留真实内容"""

import re

INPUT_FILE = "/Users/zhangshenshen/ZCodeProject/wenjian/员工手册_提取文字.txt"
OUTPUT_FILE = "/Users/zhangshenshen/ZCodeProject/wenjian/员工手册_清理版.txt"

# 水印行匹配：各种变体词根 + 可选数字后缀
WATERMARK_ROOTS = [
    "sensen", "senan", "sAn5en", "San5en", "SAn5an", "SAnen",
    "senson", "sonson", "sohson", "sonsor", "sonaon", "sonsen",
    "senoe", "seneen", "sengen", "sen5en", "sen49n",
    "nsen", "n5en", "on5en", "nnen", "nnon", "nn5n", "nen",
    "conson", "conaon", "gonson", "ponson", "3onson",
    "sonsn", "senser", "Bnnson", "Bnnen", "Bnnban", "Bonen",
    "annsor", "Sn5an", "sonaon", "senser",
    "5onson", "on5n", "n5on", "nson", "non",
    "sen", "senn", "ensen", "onaon", "neon", "senoen", "nn5en",
]

_watermark_pats = [re.escape(r) for r in WATERMARK_ROOTS]
watermark_line_re = re.compile(
    r"^((" + "|".join(_watermark_pats) + r")\s*\d{0,4})$",
    re.IGNORECASE,
)

# 独立水印数字（3726, 3720, 3728, 726, 372 等）
standalone_watermark_num_re = re.compile(r"^(3726|3720|3728|372|726|720|72|26)$")

# 行尾水印清除：去掉末尾的 "3726", "3720", "726", "：3726" 等
trailing_watermark_re = re.compile(
    r"[·：:\s]*(3726|3720|3728|372|726|720|72|26)\s*$"
)


def is_watermark_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True  # 空行保留由后续逻辑决定
    # 匹配 "sensen 3726", "sonson3720", "conson 3720" 等
    if watermark_line_re.match(stripped):
        return True
    # 匹配独立水印数字
    if standalone_watermark_num_re.match(stripped):
        return True
    # 极短纯字母/数字水印残留（如 "nn", "1n", "F", "E", "T"）
    if len(stripped) <= 3 and re.match(r"^[a-zA-Z\d]+$", stripped):
        # 排除可能是正文的短文本（如 "V2.2" 格式、序号等）
        if not re.match(r"^[IVX]+$", stripped):  # 保留罗马数字
            return True
    return False


def clean_line(line: str) -> str:
    """清理行内水印，保留正文"""
    # 去掉行尾水印数字
    cleaned = trailing_watermark_re.sub("", line)
    return cleaned.strip()


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    cleaned_lines = []
    for line in raw_lines:
        stripped = line.strip()
        # 跳过纯水印行
        if is_watermark_line(stripped):
            continue
        # 清理行内水印
        cleaned = clean_line(stripped)
        # 清理后再次检查（防止去掉数字后暴露出水印词根）
        if is_watermark_line(cleaned):
            continue
        if cleaned:
            cleaned_lines.append(cleaned)

    # 去除连续空行（最多保留1个空行分隔）
    result = []
    prev_empty = False
    for line in cleaned_lines:
        if not line:
            if not prev_empty:
                result.append("")
            prev_empty = True
        else:
            prev_empty = False
            result.append(line)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(result))

    print(f"原始行数: {len(raw_lines)}")
    print(f"清理后行数: {len(result)}")
    print(f"输出文件: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
