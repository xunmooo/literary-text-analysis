# -*- coding: utf-8 -*-
import jieba
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 設定中文字體
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

with open("text.txt", "r", encoding="utf-8-sig") as f:
    text = f.read()

stopwords = set("的 了 是 在 我 你 他 她 們 也 就 都 而 及 與 著 或 一個 沒有 這個 那個 這 那 就 都 而 很 又 把 被 讓 向 從 對".split())
words = []
for w in jieba.cut(text):
    w = w.strip()
    if len(w) > 1 and w not in stopwords:
        words.append(w)

word_counts = Counter(words)
top20 = word_counts.most_common(20)
with open("top_words.txt", "w", encoding="utf-8") as f:
    f.write("=== 最高頻 20 個詞彙 ===\n")
    for i, (word, count) in enumerate(top20, 1):
        f.write(f"{i}. {word} : {count} 次\n")

positive_words = set("好 美 快樂 喜歡 開心 溫暖 感謝 幸福 漂亮 可愛 感動 希望 光明 燦爛 笑 愛 讚 棒 優雅 美好 溫柔 想念 喜歡 溫暖 美麗 動人".split())
negative_words = set("悲傷 難過 痛苦 討厭 害怕 恐懼 氣憤 絕望 孤單 寂寞 恨 醜 悲 哭 怒 愁 苦 慘 淒涼 冷漠 沉重 壓力".split())

pos_count = sum(1 for w in words if w in positive_words)
neg_count = sum(1 for w in words if w in negative_words)
total = len(words)

with open("emotion_summary.txt", "w", encoding="utf-8") as f:
    f.write("=== 情感分析結果 ===\n")
    f.write(f"總詞數: {total}\n")
    f.write(f"積極詞出現次數: {pos_count}\n")
    f.write(f"消極詞出現次數: {neg_count}\n")
    if total > 0:
        f.write(f"積極詞佔比: {pos_count/total*100:.1f}%\n")
        f.write(f"消極詞佔比: {neg_count/total*100:.1f}%\n")

# === 畫長條圖 ===
words_list = [w for w, c in top20]
counts_list = [c for w, c in top20]
plt.figure(figsize=(10, 6))
plt.barh(words_list[::-1], counts_list[::-1], color="#3498db")
plt.xlabel("出現次數")
plt.title("最高頻 20 個詞彙")
plt.tight_layout()
plt.savefig("top_words_chart.png", dpi=100)
plt.close()

# === 畫圓餅圖 ===
plt.figure(figsize=(6, 6))
plt.pie([pos_count, neg_count, total - pos_count - neg_count],
        labels=[f"積極詞 ({pos_count})", f"消極詞 ({neg_count})", f"其他 ({total - pos_count - neg_count})"],
        colors=["#2ecc71", "#e74c3c", "#bdc3c7"],
        autopct="%1.1f%%",
        startangle=90)
plt.title("情感分佈")
plt.savefig("emotion_pie.png", dpi=100)
plt.close()

# === 表格列 ===
table_rows = ""
for i, (word, count) in enumerate(top20, 1):
    table_rows += f"<tr><td>{i}</td><td>{word}</td><td>{count}</td></tr>\n"

pos_pct = f"{pos_count/total*100:.1f}" if total > 0 else "0"
neg_pct = f"{neg_count/total*100:.1f}" if total > 0 else "0"

html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>文學文本分析報告</title>
<style>
body {{ font-family: "Microsoft YaHei", sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #fafafa; color: #333; }}
h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
h2 {{ color: #2c3e50; margin-top: 40px; }}
table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
th, td {{ border: 1px solid #ddd; padding: 10px 14px; text-align: left; }}
th {{ background: #3498db; color: white; }}
tr:nth-child(even) {{ background: #f2f2f2; }}
img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 8px; margin: 15px 0; }}
.emotion {{ display: flex; gap: 30px; margin-top: 20px; }}
.card {{ flex: 1; padding: 20px; border-radius: 8px; text-align: center; }}
.pos {{ background: #e8f8f5; border: 2px solid #2ecc71; }}
.neg {{ background: #fdedec; border: 2px solid #e74c3c; }}
.big-number {{ font-size: 36px; font-weight: bold; }}
.pos .big-number {{ color: #27ae60; }}
.neg .big-number {{ color: #c0392b; }}
</style>
</head>
<body>
<h1>📊 文學文本分析報告</h1>

<h2>一、最高頻 20 個詞彙</h2>
<img src="top_words_chart.png" alt="最高頻詞彙長條圖">
<table>
  <tr><th>排名</th><th>詞彙</th><th>出現次數</th></tr>
  {table_rows}
</table>

<h2>二、情感分析結果</h2>
<img src="emotion_pie.png" alt="情感分佈圓餅圖">
<div class="emotion">
  <div class="card pos"><h3>😊 積極詞</h3><div class="big-number">{pos_count}</div><div>佔比 {pos_pct}%</div></div>
  <div class="card neg"><h3>😢 消極詞</h3><div class="big-number">{neg_count}</div><div>佔比 {neg_pct}%</div></div>
</div>

<p style="margin-top:40px;color:#999;font-size:13px;">分析工具：Python + jieba + matplotlib</p>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 完成！已產生長條圖、圓餅圖和更新版 index.html")