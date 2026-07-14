# Lab 1 古典 IR：親手做出一個最小搜尋引擎

課程 1「資訊檢索與生成式人工智慧」上午實作段（練 A～D）的 Jupyter Notebook 教材。
親手做出一個會「打分數、排名次」的最小搜尋引擎——它就是下午 Lab 3 RAG「檢索」那一半的原型。

> 語料聲明：`data/news/` 全部為**虛構、教學用**財經新聞（非真實行情，不含任何真實公司數字）。

## 兩本 notebook 怎麼用

| 檔案 | 用途 | 用法 |
|---|---|---|
| `Lab1_古典IR_教學版.ipynb` | **課堂用** | 核心 1–3 行挖成 `____` 並標 `# TODO：`，照每格上方 📖 引導自己填。每群結尾有 📝 小作業。 |
| `Lab1_古典IR_完整版.ipynb` | **回家複習** | cell 與教學版一一對應（44 cells）。所有 TODO 已填正確答案、關鍵行附 `# 💡 為什麼這樣寫`、小作業附參考解（參考解不只一種）。可 Restart & Run All 一路全綠跑通。 |

**課堂節奏（講練交織）：** 每段講述完馬上回 notebook 動手做對應的練 A～D。BM25 附錄為選做（需 `rank_bm25`），卡在前面的直接跳過。

**⚠️ 開啟位置：** 請在本資料夾（`Lab1_古典IR/`）底下啟動 Jupyter 再開 notebook——練 D 用相對路徑讀 `data/news/*.txt`，第一格環境檢查會幫你確認。

## 環境需求

- Python 3.9+，Jupyter（`pip install notebook` 或 JupyterLab / VS Code 皆可）
- 套件：`pip install -r requirements.txt`
  - `scikit-learn`、`numpy`：練 A–C 就要（全程本機、**不需網路/API**）
  - `jieba`：練 D 中文斷詞才用到（notebook 把檢查放在練 D 開頭，不會在第一格擋人）
  - `rank_bm25`：**選做**，只有 BM25 附錄用
- **開課前務必在教室機驗證**：sklearn 已裝、且完整版能 Restart & Run All 全綠。

## 🛟 出事了怎麼辦（按最常先爆排序）

| 故障情境 | 現場 Plan B |
|---|---|
| `No module named 'sklearn'` | `pip install scikit-learn`（套件名 `scikit-learn`、import 名 `sklearn`）。教室機裝不動 → 改開 Google Colab，上傳 notebook + `data/`。 |
| 練 B `shape` 變 `(5, 0)`（一個詞都沒抓到） | 一定是漏改 `token_pattern`。確認 `TfidfVectorizer(token_pattern=r"(?u)\S+")`。 |
| 查詢誤用 `fit_transform` → 分數全 0 / 維度錯 | 規則：**文件 fit、查詢 transform**。查詢一律 `vectorizer.transform([query])`。 |
| 練 D `FileNotFoundError` | 確認在 `Lab1_古典IR/` 底下開 notebook；真的讀不到就退回練 B 的 5 句 `docs`，照樣完成全部學習目標。 |
| 編碼亂碼 | `open(p, encoding="utf-8")` 一定要帶（Windows 預設不是 utf-8）。 |
| `jieba` 裝不起來 | 走小作業 D 的 ⭐：`TfidfVectorizer(analyzer="char_wb", ngram_range=(2,3))` 字 n-gram，**免斷詞、零安裝**，中文也搜得動（比 jieba 粗一點）。 |
| `rank_bm25` 裝不起來 | BM25 是選做附錄，直接跳過，不影響核心。 |

環境快速自測：notebook 開頭「最小可跑核心」5 行能印出 `[0.7xx 0.]`，整個 Lab 的核心就沒問題。

## 資料夾結構

```
Lab1_古典IR/
├── Lab1_古典IR_教學版.ipynb   ← 課堂發放（引導式填空）
├── Lab1_古典IR_完整版.ipynb   ← 回家複習（含全部解答與小作業參考解）
├── data/news/                 ← 15 篇虛構財經新聞 .txt（練 D 語料）
├── README.md
└── requirements.txt
```
