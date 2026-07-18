# Lab 1 金融爬蟲：把公開資料變成表格

課程 2「人工智慧與金融科技」Day 2 第一站。寫程式把**公開的金融資料**抓回來、整理成表格，是全課「從爬資料 → 用 AI 輔助投資決策」的**共同源頭**。

## 這個 Lab 會產出

| 檔案 | 來源 | 之後給誰用 |
|---|---|---|
| `prices.csv` | 證交所 TWSE API（股價） | 數據路：pandas → KNN → 決策樹 → GA |
| `news_raw.csv` | 鉅亨網 API（財經新聞 date/title/text） | 文字路：情緒打分 |

## 環境需求

- Python 3.9+
- 套件：`requests`、`beautifulsoup4`、`pandas`（notebook 第一格 `!pip install` 會自動裝；或 `pip install -r requirements.txt`）
- **不需要 API key**（純 requests / pandas；Day 3 的 Lab 才需要）

## 怎麼開始

1. 開 `Lab1_金融爬蟲_教學版.ipynb`，從上到下一格一格跑，照 `# TODO` 提示把 `____` 填起來。
2. 卡住或想對答案 → 看 `Lab1_金融爬蟲_完整版.ipynb`（每格都有解答與 `💡` 註解）。
3. **一定要從第一格開始、由上往下跑**——後面的格子會用到前面的變數。

## ⚠️ 抓到的跟教材不一樣是正常的

這個 Lab 爬的是**活的真實網站**——新聞每分鐘在變、行情每天在變。你印出來的新聞標題、行情數字**跟講義、跟同學都會不一樣**。**看結構**：三欄（date / title / text）都有值、字數合理，就是成功。

## 🛟 Backup（斷網 / 被網站擋 / 套件裝不起來）

> notebook 本身**不含**離線退路格（精簡版收在 C2）；斷網時**由老師現場處理**。

- **斷網 / 網站掛了：** 老師會在**上課當天**發一份 `cache/` 資料夾（當天早上抓的快照：中央社 RSS、鉅亨 API 回應、證交所回應、中央社內頁）。**這份快照不放在 repo 裡**——因為它必須是「當天的新鮮資料」，而且裡面是別人網站的內容，我們不轉貼。現場斷網時，老師帶大家把抓取那行改成讀本地檔（例如 `open("cache/cnyes.json")` 再 `json.loads`）。
- **被擋（403 / 429）：** C2 抓內頁記得帶 `headers=UA`（notebook 已示範有/無 UA 的差別）；抓太快就把 `sleep(1)` 改 `sleep(3)`。
- **套件裝不起來：** 改用 Colab（已內建），或老師預建的 venv。

## 🧑‍🏫 講師開課前時效檢查（Day 2 前 2–3 天）

爬的是活網站，開課前務必各跑一次確認還活著、並重建 `cache/`：
1. 鉅亨 API `api.cnyes.com/media/api/v1/newslist/category/tw_stock` 回 JSON（`items.data` 有 `title`+`content`）— C1 正式貨源、最優先
2. 證交所 STOCK_DAY 回 `stat=OK`（`date` 參數換當月）
3. 中央社 RSS 有 `<item>`、內頁三個 selector（`h1` / `div.paragraph p` / `div.updatetime`）撈得到
4. 四家 robots.txt 沒變（鉅亨 api 主機仍 404、www 的 `*` 段未禁 `/news/`；中央社 `/news/` 未禁；經濟日報禁 AI 那段）

## 版本歷史

- **v1.1（2026-07-18）** — 走完草稿交棒法：使用者標挖空 + 重構（UA 教學從 A 段挪到 C2 用「有/無 headers」對照實驗帶、加「.json 對 XML 會失敗」對照、多個 peek 格、刪 D 段與 Backup）。主 Claude 產教學版＋完整版（逐格對應、真實輸出 0 錯誤）、機械驗收全過。對應教具 v1.3。
- **v1.0（2026-07-18）** — 首版完整版＋草稿（主 Claude 端到端跑過）。
