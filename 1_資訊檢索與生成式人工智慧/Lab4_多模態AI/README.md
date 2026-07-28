# Lab 4：多模態 AI —— 讓模型「看圖」讀財報 ⭐

前面 Lab 2、Lab 3 的模型都只讀**文字**。這一段讓它**看圖**：直接讀 K 線圖、損益表截圖，
並拿**開源模型 `minimax-m3:cloud`** 和**商用旗艦 `gemini-3.5-flash`** 讀同一張圖，
親手比出**誰讀得準、誰比較貴、什麼時候會讀歪**。

---

## 📁 檔案

| 檔案 | 用途 |
|---|---|
| `Lab4_多模態AI_教學版.ipynb` | **課堂用**。核心程式碼挖成 `____`，照 `# TODO` 提示自己填 |
| `Lab4_多模態AI_完整版.ipynb` | **回家複習用**。全部有答案 + `💡` 註解 + 小作業參考解 |
| `data/fig1.png` | 先進光(3362) K 線＋資券進出圖（**較難的圖**，藏了一個讀圖陷阱）|
| `data/fig2.png` | 台積電(2330) 綜合損益表季表（**密集表格**，考精準讀數字）|
| `requirements.txt` | Python 套件 |

> ⚠️ **關於這兩張圖：** 本 Lab 的重點是「讓模型**讀**一張現成的公開圖表」，
> 所以刻意用**真實的公開財報圖／看盤圖**（才有真實的密集表格與陷阱可讀）。
> 這是本課「金融情境一律用虛構『宏圖飲料』」鐵則的**唯一例外**，且僅用於「讀圖示範」、
> **不主張、不引用任何真實行情做投資判斷**。圖上數字請勿當作投資依據。

---

## 🔧 開始之前

### 準備好**兩把** key（這一段兩把都要用）

Lab 4 會**同時**呼叫開源 minimax（要 OLLAMA key）和商用 Gemini（要 Gemini key），
所以**兩把 key 都是必備**。notebook 最上面的「檢查 1」那格，把兩把 key 直接貼進引號中間：

```python
os.environ["OLLAMA_API_KEY"] = "在這裡貼上你的 OLLAMA key"   # ← 換成你的 OLLAMA key
os.environ["GOOGLE_API_KEY"] = "在這裡貼上你的 Gemini key"   # ← 換成你的 Gemini key
```

- **OLLAMA key**：沿用 Lab 2／Lab 3 那把。
- **Gemini key**：到 **https://aistudio.google.com/apikey** 用 Google 帳號登入免費建一把
  （Lab 2 已經辦過就用同一把）。辦 key 時選 **Flash 免費層**、不確定先別綁卡。

> ⚠️ 貼了 key 的 notebook 別上傳 GitHub、別傳給別人、別截圖。key 等於你帳號的鑰匙。

### 不用拉 embedding 模型、不用畫圖

Lab 4 沒有 embedding、沒有向量庫，圖也已經幫你放在 `data/`，
所以**不用 `ollama pull`、不用裝 matplotlib**——只要兩把 key ＋ `requirements.txt` 的套件即可。

---

## ▶️ 開始

```bash
jupyter notebook
```

打開 `Lab4_多模態AI_教學版.ipynb`，**從上往下一格一格跑**（不能跳著執行）。
開頭有 3 格環境自我檢查，燈全綠再往下走。

> ⚠️ **notebook 要留在這個資料夾裡跑，不要單獨搬到桌面或別的地方。**
> 它用相對路徑 `data/fig1.png`、`data/fig2.png` 去讀隔壁的圖——搬走就讀不到圖，
> 會在讀圖那格噴 `FileNotFoundError`。要搬就**整個資料夾一起搬**（`data/` 跟著走）。

---

## 🛟 出事了怎麼辦

| 狀況 | 怎麼辦 |
|---|---|
| `KeyError: 'OLLAMA_API_KEY'` | 沒跑到貼 key 的那格 → 回「檢查 1」貼好兩把 key，再從頭一格格跑 |
| Gemini 那格報金鑰錯誤 / 403 | Gemini key 沒貼對，或還沒到 https://aistudio.google.com/apikey 辦 → 辦好貼上再跑 |
| `model not found` | 開源模型名要帶 cloud tag（`minimax-m3:cloud`），漏了會去找本機同名模型 |
| `FileNotFoundError: data/fig1.png` | notebook 被搬離資料夾了 → 整個資料夾搬回去，或把 notebook 放回 `data/` 隔壁 |
| 模型把數字讀歪了 | **這正是 Lab 4 要你看到的事**——多模態不保證 100% 正確，關鍵數字一定要自己回頭核對圖 |
| **雲端不通 / 額度用完** | 跑 notebook 最後的 Backup 格說明；minimax 掛了可換本機有 vision 的模型，gemini 掛了就先看 minimax 一顆 |

---

## 📌 用到的模型

| 模型 | 跑在哪 | 做什麼 |
|---|---|---|
| `minimax-m3:cloud` | Ollama 雲端（要 OLLAMA key） | 開源多模態模型，讀圖 |
| `gemini-3.5-flash` | Google 雲端（要 Gemini key） | 商用旗艦多模態模型，讀同一張圖對照 |

---

## 版本歷史

| 版本 | 日期 | 內容 |
|---|---|---|
| v1.0 | 2026-07-28 | 初版。完整版以**真實 API key 實跑**過，輸出為真實結果。主線：fig2 台積電損益表兩顆都讀對 → fig1 先進光 K 線 minimax 把「2 月報價 106」誤當現在（讀歪）、gemini 較穩 → 多模態能讀非純文字財報素材，但關鍵數字要人工核對；接區塊 5 多模態 RAG。 |
