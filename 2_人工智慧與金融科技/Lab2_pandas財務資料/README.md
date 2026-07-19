# Lab 2 財務資料清理：把髒表格變成模型能吃的特徵

把上一個 Lab 抓回來的髒股價資料洗乾淨，做成模型可以直接吃的特徵表。

## 怎麼開始

```bash
pip install -r requirements.txt
jupyter notebook Lab2_pandas財務資料_教學版.ipynb
```

或直接在 notebook 裡跑第一格的 `!pip install`。

## 檔案

| 檔案 | 用途 |
|---|---|
| `Lab2_pandas財務資料_教學版.ipynb` | 課堂用，引導式填空 |
| `Lab2_pandas財務資料_完整版.ipynb` | 回家複習，含全部解答與執行結果 |
| `data/prices.csv` | 證交所 2330／2026-06 真實快照（**上課用這份**） |

## 內容

- **A** 修 `prices.csv`：`dtypes` 照妖 → 故意踩 `TypeError` → 民國轉西元 → 拔千分位逗號
- **B** 寬表與缺值：`dropna` / `ffill` ✓ / `bfill` ✗（偷看未來）＋ 回證交所驗證停牌是真的
- **C** 特徵工廠（報酬率／移動平均／label）＋ 第一次 train/test 時序分割
- **D** 收尾

## 環境需求

- Python 3.9+、pandas、numpy、requests
- **B6 那一格需要網路**（連證交所 API），其餘全部離線可跑

## Backup

| 狀況 | 怎麼辦 |
|---|---|
| **B6 連不上證交所** | 跳過那一格，**不影響後面任何一步**。結論：同月台積電 22 天、鴻海 16 天，差的 6 天是減資停牌。 |
| **`data/prices.csv` 不見了** | 從 repo 重新拉一份。全班用同一份，數字才對得上教材。 |
| **數字跟教材不一樣** | 今天全部都該一樣（跟上一個 Lab 相反）。B/C 段確認 `default_rng(42)` 有含 42；A 段確認讀的是 `data/prices.csv`，不是你自己抓的那份。 |
| **`roc_to_date` 爆錯** | 多半是那格重跑了兩次（日期已轉過再轉一次）。從 `read_csv` 那格重跑一遍即可。 |
| **Excel 開 CSV 亂碼** | 存檔時加 `encoding="utf-8-sig"`。 |

## 版本

- v1.0（2026-07-19）初版。資料來源統一為證交所 TWSE。
