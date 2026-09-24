# -*- coding: utf-8 -*-
import jieba
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

positive_words = set("好 美 快樂 喜歡 開心 溫暖 感謝 幸福 漂亮 可愛 感動 希望 光明 燦爛 笑 愛 讚 棒 優雅 美好 溫柔 想念 美麗 動人".split())
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

# 長條圖
words_list = [w for w, c in top20]
counts_list = [c for w, c in top20]
bar_colors = ["#7f9ca4", "#8ea8a0", "#9aaea4", "#afb9a4", "#b8c4ad",
              "#a7b7b0", "#93a8a2", "#8aa09d", "#a6b8b5", "#a8a7a0",
              "#bcc7b1", "#9eab9b", "#a8bcb4", "#b0b8aa", "#8ca29a",
              "#c0b8a5", "#9fb4ab", "#b3a89f", "#9ea9a0", "#aab8b1"]
plt.figure(figsize=(10, 6))
plt.barh(words_list[::-1], counts_list[::-1], color=bar_colors[:len(words_list[::-1])], edgecolor="#e8e0d8", linewidth=0.8)
plt.xlabel("出現次數")
plt.title("最高頻 20 個詞彙")
plt.tight_layout()
plt.savefig("top_words_chart.png", dpi=100)
plt.close()

# 圓餅圖
plt.figure(figsize=(6, 6))
plt.pie([pos_count, neg_count, total - pos_count - neg_count],
        labels=[f"積極 ({pos_count})", f"消極 ({neg_count})", f"中性 ({total - pos_count - neg_count})"],
        colors=["#8aa7a1", "#c8a899", "#d9d2c7"],
        autopct="%1.1f%%", startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.2})
plt.title("情感分佈")
plt.savefig("emotion_pie.png", dpi=100)
plt.close()

# 表格列
table_rows = ""
for i, (word, count) in enumerate(top20, 1):
    table_rows += f"<tr><td>{i}</td><td>{word}</td><td>{count}</td></tr>\n"

pos_pct = f"{pos_count/total*100:.1f}" if total > 0 else "0"
neg_pct = f"{neg_count/total*100:.1f}" if total > 0 else "0"

html = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《落花雨》文本賞析與分析報告</title>
<style>
  :root {{
    --bg: #f2efe9;
    --panel: rgba(255, 255, 255, 0.82);
    --panel-strong: #fbf8f4;
    --ink: #2d2d2d;
    --muted: #6d6a64;
    --line: #e4ddd2;
    --mist: #dfe7e5;
    --mist-deep: #abc0c5;
    --lake: #7f9ca4;
    --lake-deep: #536f7d;
    --reed: #879b8d;
    --reed-soft: #edf3ee;
    --saffron: #c6a77d;
    --saffron-soft: #f7f0e6;
    --rose: #b98a7d;
    --rose-soft: #f5eeeb;
    --shadow: 0 18px 42px rgba(52, 58, 60, 0.08);
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    font-family: "Noto Serif TC", "Microsoft YaHei", serif;
    background:
      radial-gradient(circle at top left, rgba(127, 156, 164, 0.14), transparent 32%),
      radial-gradient(circle at bottom right, rgba(198, 167, 125, 0.12), transparent 36%),
      var(--bg);
    color: var(--ink);
    line-height: 1.9;
  }}

  .hero {{
    position: relative;
    overflow: hidden;
    padding: 86px 22px 64px;
    text-align: center;
    background: linear-gradient(135deg, #6d8b97 0%, #a7b8b2 35%, #d9d2c7 100%);
    color: #fff;
    box-shadow: inset 0 -1px 0 rgba(255,255,255,0.18);
  }}

  .hero::before {{
    content: "";
    position: absolute;
    inset: 0;
    background:
      radial-gradient(circle at 12% 18%, rgba(255,255,255,0.25), transparent 12%),
      radial-gradient(circle at 68% 20%, rgba(255,255,255,0.22), transparent 16%),
      radial-gradient(circle at 52% 70%, rgba(255,255,255,0.15), transparent 18%);
    pointer-events: none;
  }}

  .hero-inner {{
    position: relative;
    z-index: 1;
    max-width: 980px;
    margin: 0 auto;
  }}

  .hero-tag {{
    display: inline-block;
    letter-spacing: 0.22em;
    font-size: 0.78rem;
    text-transform: uppercase;
    padding: 8px 16px;
    border: 1px solid rgba(255,255,255,0.32);
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    margin-bottom: 18px;
  }}

  .hero h1 {{ font-size: clamp(2.1rem, 3vw, 3.2rem); letter-spacing: 0.08em; margin-bottom: 12px; }}
  .hero .subtitle {{
    font-size: 1.08rem;
    opacity: 0.9;
    letter-spacing: 0.08em;
  }}

  .container {{
    max-width: 1080px;
    margin: -28px auto 42px;
    padding: 0 20px;
    position: relative;
    z-index: 2;
  }}

  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(180px, 1fr));
    gap: 18px;
    margin: 0 0 26px;
  }}

  .stat-card {{
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(80, 80, 80, 0.08);
    border-radius: 18px;
    padding: 22px 18px;
    box-shadow: var(--shadow);
    text-align: center;
  }}

  .stat-card .label {{
    color: var(--muted);
    font-size: 0.8rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 10px;
  }}

  .stat-card .value {{
    font-size: clamp(1.2rem, 2vw, 1.75rem);
    font-weight: 700;
    color: var(--lake-deep);
  }}

  .card {{
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(120, 120, 120, 0.06);
    border-radius: 20px;
    padding: 30px 28px 26px;
    margin-bottom: 24px;
    box-shadow: var(--shadow);
  }}

  .card h2 {{
    color: #3d4e54;
    font-size: clamp(1.45rem, 2vw, 1.85rem);
    margin-bottom: 18px;
    padding-left: 16px;
    border-left: 5px solid var(--lake);
    line-height: 1.5;
  }}

  .card h3 {{
    color: #3b4d5d;
    font-size: 1.18rem;
    margin: 18px 0 10px;
  }}

  .lead {{
    font-size: 1.06rem;
    color: #3e3b38;
    text-indent: 2em;
  }}

  .analysis-text {{
    background: linear-gradient(90deg, rgba(198,167,125,0.12), rgba(255,255,255,0.35));
    border-left: 4px solid var(--saffron);
    border-radius: 10px;
    padding: 18px 20px;
    margin-top: 16px;
  }}

  .analysis-text p {{ margin-bottom: 12px; text-indent: 2em; }}

  .insight-list {{
    list-style: none;
    display: grid;
    grid-template-columns: repeat(2, minmax(240px, 1fr));
    gap: 14px 24px;
    margin-top: 18px;
  }}

  .insight-list li {{
    background: #f8f5f2;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 14px 16px;
    position: relative;
    padding-left: 18px;
  }}

  .insight-list li::before {{
    content: "•";
    position: absolute;
    left: 10px;
    top: 12px;
    color: var(--lake);
    font-size: 1.4rem;
    line-height: 1;
  }}

  .quote-panel {{
    background: linear-gradient(135deg, #f2efe8, #f8f6f2);
    border: 1px solid rgba(135,155,149,0.32);
    border-radius: 14px;
    padding: 18px 22px;
    margin: 18px 0;
    font-size: 1.08rem;
    color: #5e5b57;
    font-style: italic;
    text-align: center;
  }}

  .chart-wrap {{
    margin-top: 16px;
    padding: 14px;
    background: #fcfbfa;
    border: 1px solid var(--line);
    border-radius: 14px;
  }}

  img {{
    display: block;
    width: 100%;
    max-width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(90,90,90,0.08);
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    margin: 10px 0 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 16px;
    overflow: hidden;
    border-radius: 14px;
    border: 1px solid rgba(120, 135, 132, 0.32);
    background: #fffefc;
  }}

  th, td {{
    padding: 12px 14px;
    border-bottom: 1px solid rgba(130, 142, 139, 0.25);
    text-align: left;
  }}

  th {{
    background: linear-gradient(135deg, #a3b7b0, #7d8f8a);
    color: #f9fbfa;
    font-weight: 600;
    letter-spacing: 0.04em;
  }}

  tr:nth-child(even) {{ background: #f5f1ec; }}
  tr:nth-child(odd) {{ background: #fffdfb; }}

  td {{ color: #3b3b3b; }}

  .emotion-row {{
    display: flex;
    gap: 18px;
    margin-top: 20px;
    flex-wrap: wrap;
  }}

  .emotion-box {{
    flex: 1 1 240px;
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    box-shadow: inset 0 0 0 1px rgba(0,0,0,0.03);
  }}

  .emotion-box.positive {{ background: var(--reed-soft); border: 2px solid rgba(135,155,141,0.45); }}
  .emotion-box.negative {{ background: var(--rose-soft); border: 2px solid rgba(185,138,125,0.42); }}

  .emotion-box h3 {{ margin-top: 0; margin-bottom: 6px; }}
  .emotion-num {{
    font-size: clamp(2.2rem, 3vw, 3rem);
    font-weight: 700;
    line-height: 1.2;
  }}

  .positive .emotion-num {{ color: var(--reed); }}
  .negative .emotion-num {{ color: var(--rose); }}

  .footer {{
    text-align: center;
    color: #7a756f;
    padding: 18px 20px 42px;
    font-size: 0.92rem;
  }}

  @media (max-width: 820px) {{
    .stats-grid, .insight-list {{ grid-template-columns: 1fr 1fr; }}
  }}

  @media (max-width: 620px) {{
    .stats-grid, .insight-list {{ grid-template-columns: 1fr; }}
    .card {{ padding: 22px 18px; }}
    .hero {{ padding-top: 72px; }}
  }}
</style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <div class="hero-tag">文學文本研究</div>
      <h1>《落花雨》</h1>
      <div class="subtitle">文本賞析與情感分析報告</div>
    </div>
  </header>

  <main class="container">
    <section class="stats-grid">
      <div class="stat-card">
        <div class="label">核心意象</div>
        <div class="value">雨 · 花 · 故鄉</div>
      </div>
      <div class="stat-card">
        <div class="label">敘事空間</div>
        <div class="value">九江 · 浙江 · 香港</div>
      </div>
      <div class="stat-card">
        <div class="label">情感基調</div>
        <div class="value">柔和 · 懷舊 · 沈靜</div>
      </div>
      <div class="stat-card">
        <div class="label">文學特色</div>
        <div class="value">細節 · 意象 · 反覆</div>
      </div>
    </section>

    <section class="card">
      <h2>一、文本總覽：一篇在雨中漂泊的故鄉書</h2>
      <p class="lead">這篇散文沒有以劇烈的情緒宣洩開篇，而是從“雨”出發，將自己的流動人生與故土記憶一層一層地展開。它的敘事方式具有典型散文特徵：重在感受、重在意象、重在細節。作者在三個地點之間移動，從江西九江到浙江，再到香港，像一盞暗處的燈，被雨水與花香一路照亮。文本的力量不在於“我很悲傷”，而在於“我如何把一個地方的氣味、光線與季節，寫成自己内心最深處的回聲”。</p>
      <div class="analysis-text">
        <p>在文學上，故鄉常常不是單一地理意義上的地方，而是一種“不可替代的情感模版”。作者寫九江的“薄雨”、浙江的“春雨”、香港的“驟雨”，實際上不是三種自然現象的羅列，而是三段生活的時間標記。當“雨”逐層變化，內心也逐步發生變化：先是對故鄉的眷戀，後是對新生活的調適，再到在異鄉中對回憶的深深依賴。整篇文本的情感軸線，恰恰是從“離開故鄉”到“理解故鄉”。</p>
      </div>
    </section>

    <section class="card">
      <h2>二、核心意象：雨、花、白色與家族記憶</h2>
      <ul class="insight-list">
        <li>雨成為文章的主導意象，連接時間與城市，讓景物與情感彼此交疊。</li>
        <li>白蘭花與白玉蘭不只是植物，而是故鄉氣味與童年感知的具體化媒介。</li>
        <li>母親、婆婆、門前庭院的景物，把私人記憶提升為家族共同的情感場域。</li>
        <li>文本中的“白”帶有清潔、純淨、柔和與遠離繁華的氣質，是情感的底色。</li>
      </ul>

      <h3>1. 雨：一個穿越城市的心靈軌跡</h3>
      <p class="lead">“家鄉的秋雨很薄”“浙江的雨最多情”“香港的雨很凶，又纏綿”，這三種描述讓雨不再是單純的天氣，而是三個時期、三種人生狀態的記憶符號。九江的雨是柔、是微、是淡；浙江的雨是疏、是濕、是浪漫；香港的雨則是濁、是重、是壓迫。這種變化讓文章獲得了極強的動態感：雨是作者旅途中的照明器，也是自我心境的映照鏡。</p>

      <h3>2. 白蘭花與白玉蘭：故鄉的香氣與視線</h3>
      <p class="lead">作者特別寫白蘭花的香氣：比栀子清爽，比茉莉悠長，甚至“聞起來連眼睛都是凉的”。這樣的描寫極具感官細膩度，說明作者並不只是“記得花”，而是記得花帶來的整個生活方式——陽台、帷幕、略帶秋涼的空氣、婆婆插在衣襟上的襟花。到了浙江，玉蘭花又以“未開、盛開、凋落”的不同阶段呈現，形成一個完整的生命循環。這種細節使植物不再是靜物，而是時間流動的見證者。</p>

      <div class="quote-panel">“雨下著，帘外还能透进清光来，细密地织成一副朦胧的画。”</div>

      <h3>3. 家庭與母親：從自然意象轉向情感依附</h3>
      <p class="lead">文本中的婆婆與母親都不是旁觀者，而是使“故鄉”成為一個可被感知和理解的場域的存在。婆婆插花、母親養花，這些生活中的小動作，通過“自然與人”相互映照，使故鄉之感不只是抽象的離愁，而是一種被生活實踐過的情感記憶。這也使散文的情感比純抒情更具“生活根基”。</p>
    </section>

    <section class="card">
      <h2>三、結構層次：從北到南，從記憶到現實</h2>
      <p class="lead">文章的空間移動非常明顯：九江——浙江——香港，仿佛一條由北到南、由内到外的抒情軌道。這條軌道不僅是一個地理路線，也是一個情感的遷徙：最初在九江的“白蘭花”中感到故鄉之甘，後來在浙江的“白玉蘭”中學習新的生活節奏，最後在香港的“驟雨”中感到被外界壓迫、被記憶包圍。這種結構有很強的“回環感”，因為文章最後再次回到故鄉的花與雨，形成一個完整的情感閉環。</p>
      <div class="analysis-text">
        <p>此外，文本中也有明顯的“時代與季節感”：秋雨、春雨、夏雨，彼此相連，構成一個充滿流動的時間節奏。作者不是以“我如何離開故鄉”來總結，而是通過花與雨的季節變換，看見生活的經過與情緒的開展。這種寫法使散文更接近詩歌：情感不靠宣告，而靠一個季節、一朵花、一場雨慢慢發酵。</p>
      </div>
    </section>

    <section class="card">
      <h2>四、語言風格：細節密度、氣質修辭與抒情張力</h2>
      <p class="lead">本文的語言特點是“輕而有力”。它不靠浮泛的情緒詞，而是靠細節的感官描寫讓情感顯現：雨聲、花香、露珠、雾氣、窗景、枝頭、枕邊的花瓣。這種寫法使文章極其“有觸感”，這也是散文最重要的美感來源之一。</p>
      <ul class="insight-list">
        <li>大量使用“有質感”的形容詞，如“薄”“濃”“多情”“凶”“纏綿”，使景色有生命。</li>
        <li>對颜色、濕度、氣味的細節描寫，使文本帶有強烈的場景感。</li>
        <li>反覆出現“白”“雨”“花”“江南”等語詞，形成強烈的主題回環。</li>
        <li>句子長短交替，既有散文式緩慢抒情，也有記憶中的快速回憶。</li>
      </ul>
      <div class="quote-panel">“四方人间，没有人能走出故乡。眼睛看着香港的雨，心就跟着淋漓，下起江南的雨。”</div>
      <p class="lead">這一段可視為全文的情感高潮：作者不再將“故鄉”當作一個地名，而是將它轉化為一種“內在的雨”。這一句的美感，在於它將外部景物與內心感受完全合一——香港的雨，照見了江南的雨，眼裡的香港，心中卻仍然在下故鄉的雨。這是思鄉的最高境界：不是離開，而是永遠帶著。</p>
    </section>

    <section class="card">
      <h2>五、詞頻與情感分析</h2>
      <div class="chart-wrap">
        <img src="top_words_chart.png" alt="詞頻長條圖">
      </div>
      <table>
        <tr><th>排名</th><th>詞彙</th><th>出現次數</th></tr>
        {table_rows}
      </table>

      <div class="analysis-text">
        <p><strong>詞頻解讀：</strong>“江南”“浙江”“香港”三個地名的反覆出現，直接說明文章的空間設計是其主軸；“白蘭花”“白玉蘭”則象徵最深的情感核心。這種“地名 + 花名”的搭配，恰如文學中常見的“景物搭載情感”的寫法：它不說“我想家”，而是讓一个地方、一个物象替你承接思念。</p>
      </div>

      <div class="emotion-row">
        <div class="emotion-box positive">
          <h3>積極詞</h3>
          <div class="emotion-num">{pos_count}</div>
          <div>佔比 {pos_pct}%</div>
        </div>
        <div class="emotion-box negative">
          <h3>消極詞</h3>
          <div class="emotion-num">{neg_count}</div>
          <div>佔比 {neg_pct}%</div>
        </div>
      </div>

      <div class="chart-wrap">
        <img src="emotion_pie.png" alt="情感分佈圓餅圖">
      </div>
      <div class="analysis-text">
        <p><strong>情感總結：</strong>全文的情感並非極端悲痛，而是“溫柔的惆悵”。這種情緒極像江南雨的氣質——不是猛烈，不是宣洩，而是持續地落、持續地濕、持續地入心。作者因為思鄉而感到“難忍”，但又以花、雨、景色來平衡這份情感，讓文字有余韻，讓讀者能在心緒中慢慢回味。</p>
      </div>
    </section>

    <section class="card">
      <h2>六、總結：思鄉不在於回到原地，而在於帶著原地的氣味</h2>
      <p class="lead">《落花雨》最打動人的地方，不是它寫了多少風景，而是它讓“故鄉”在不同城市中以不同形式活著。在九江的白蘭花中，在浙江的白玉蘭中，在香港的雨中，故鄉始終存在，像一棵無法被拔起的樹，扎根在作者的視線和記憶裡。這種思鄉不是逃避現實，而是更清醒地理解：生活可以流動，城市可以變化，但真正留在人內心的，是曾經呼吸過的、落過雨的地方。這也正是散文最深的力量——它讓時間與情感相遇，讓一片雨、一朵花，變成一生的回憶。</p>
    </section>
  </main>

  <footer class="footer">
    分析工具：Python + jieba 分詞 + matplotlib 視覺化 + 文學文本賞析<br>
    生成日期：2026 年 9 月
  </footer>
</body>
</html>
'''

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 完成！已升級為完整文學分析報告")