import re
import json
import os
import time
import random

# ================= 配置区域 =================
INPUT_FILE = 'data.txt'
OUTPUT_JSON = 'game_data.json'
# ===========================================

def clean_title(raw_title):
    title = raw_title.strip()
    title = re.sub(r'\.(apk|rar|zip|7z|txt|docx|mp4)$', '', title, flags=re.IGNORECASE)
    title = re.sub(r'^分享文件：', '', title)
    title = re.sub(r'（.*?）', '', title) 
    title = re.sub(r'\(.*?\)', '', title)
    title = re.sub(r'【.*?】', '', title) 
    return title.strip()

def get_tag_from_url(url):
    """自动识别网盘类型"""
    if "xunlei" in url: return "迅雷"
    if "quark" in url: return "夸克"
    if "baidu" in url: return "百度"
    return "网盘"

def get_random_image(index):
    """生成一个随机封面图 (Picsum 源)"""
    return f"https://picsum.photos/seed/{index}/300/200"

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ 找不到文件: {INPUT_FILE}")
        return

    print("✅ 正在智能分析数据...")
    with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    matches = re.findall(r'分享文件：(.*?)\n.*?链接：(https?://[^\s]+)', content, re.DOTALL)

    data_list = []
    current_date = time.strftime("%Y-%m-%d")

    for i, (raw_name, url) in enumerate(matches):
        clean_name = clean_title(raw_name)
        if not clean_name: clean_name = raw_name.strip()
        
        item = {
            "title": clean_name,
            "url": url,
            "date": current_date,
            "tag": get_tag_from_url(url),
            "image": get_random_image(i)
        }
        data_list.append(item)

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, indent=2, ensure_ascii=False)

    print("-" * 30)
    print(f"🎉 升级完成！已生成 {OUTPUT_JSON}")
    print(f"包含字段：标题、链接、日期、标签({len(data_list)}个)、封面图")
    print("-" * 30)

if __name__ == '__main__':
    main()