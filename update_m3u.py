import requests
import re

# 源地址
SOURCE = "https://woshinibaba.tzh911.qzz.io/playlist.m3u"

# 只保留这些频道
ALLOW = [
    "香港",
    "台湾",
    "印度",
    "泰国",
    "越南",
    "体育"
]

# 翻译字典（国家 + 频道名）
TRANSLATE = {
    "香港": "HongKong",
    "台湾": "Taiwan",
    "印度": "India",
    "泰国": "Thailand",
    "越南": "Vietnam",
    "体育": "Sports",
    "高清": "HD",
    "备用": "Backup",
    "频道": "Channel",
    "综合": "General",
    "新闻": "News",
    "电影": "Movies",
    "综艺": "Entertainment",
    "卫视": "TV"
}

# 抓取
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(SOURCE, headers=headers, timeout=10)
lines = r.text.splitlines()

keep = []
seen = set()

for line in lines:
    s = line.strip()
    if s.startswith("#EXTM3U"):
        keep.append(line)
    
    # 只保留允许的频道
    if s.startswith("#EXTINF"):
        keep_line = False
        for keyword in ALLOW:
            if keyword in line:
                keep_line = True
                break
        if not keep_line:
            continue

    # 去重
    if s in seen:
        continue
    seen.add(s)

    # 翻译
    for cn, en in TRANSLATE.items():
        line = line.replace(cn, en)

    keep.append(line)

# 保存
final = "\n".join(keep)
with open("live.m3u", "w", encoding="utf-8") as f:
    f.write(final)

print("✅ 完成：仅保留 HK/TW/IN/TH/VN/SPORTS 并翻译英文")
