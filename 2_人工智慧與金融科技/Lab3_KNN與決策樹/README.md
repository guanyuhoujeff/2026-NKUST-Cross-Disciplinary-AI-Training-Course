# Lab 3 KNN 與決策樹：兩台分類器，同一把誠實的尺

先用手編的財務指標親手做出**兩台**「猜漲跌」的分類器，再換到**真股票資料**上，在同一份資料、同一個切法上比一比——並且看它們**用同一種方式壞掉**。

## 怎麼開始

```bash
pip install -r requirements.txt
jupyter notebook Lab3_KNN與決策樹_教學版.ipynb
```

或直接在 notebook 裡跑第一格的 `!pip install`。

## 檔案

| 檔案 | 用途 |
|---|---|
| `Lab3_KNN與決策樹_教學版.ipynb` | 課堂用，引導式填空 |
| `Lab3_KNN與決策樹_完整版.ipynb` | 回家複習，含全部解答與執行結果 |
| `data/prices_cache.csv` | 8 檔台灣大型股的技術指標特徵表（**上課用這份**，全班一致、離線可跑） |

## 內容

- **A** 兩種判法各手刻一次：純 Python 算距離投票（KNN）／巢狀 `if/else`（決策樹）——用 6 家手編虛構公司練手感
- **B** ⭐ 換上**真股票**：用 Yahoo Finance 抓 8 檔台灣大型股三年價量 → 算 5 個技術指標 → label＝隔日漲跌；先故意「拿念過的考卷考自己」
- **C** ⭐ 課程重點：**用日期切** train/test（真股票是時間序列，不能隨機切）→ 掃 k → 掃 `max_depth`，兩張表並排看「樣本內 100% 是陷阱」，並挑出該用的設定
- **D** 收尾

## 環境需求

- Python 3.9+、scikit-learn、pandas、numpy、yfinance
- **第一次跑 B 段需要網路**（連 Yahoo Finance 抓資料，抓完自動存成 `data/prices_cache.csv`）；**之後與沒網路時，程式會自動改讀快取，全程離線可跑**。
- repo 已附一份 `data/prices_cache.csv`，所以就算第一次也不必連網。

## 數字說明

**今天全班的數字應該一模一樣**——因為大家讀的是同一份 `data/prices_cache.csv`。跟教材不一樣時，多半是那個快取被刪、程式重新上網抓了（Yahoo 會隨新股利微調過去價格）。用 repo 附的那份快取就會對得上。

已在 **scikit-learn 1.6.1 / 1.7.2 / 1.8.0** 三個版本上驗證，輸出一致；pandas 2.x / 3.x 皆可。

## Backup

| 狀況 | 怎麼辦 |
|---|---|
| `No module named 'sklearn'` 或 `'yfinance'` | 跑第一格的 `!pip install`。**套件名是 `scikit-learn`，import 名是 `sklearn`**。裝不動改用 Colab（sklearn 已內建，yfinance 用第一格裝）。 |
| **B 段連不上 Yahoo Finance** | 只要 `data/prices_cache.csv` 在，就**完全不需要網路**——第一格會自動讀它。這個檔 repo 裡已經附了。 |
| **數字跟教材不一樣** | 多半是快取被刪、重新上網抓了新資料。用 repo 附的 `data/prices_cache.csv` 就會一致；決策樹的數字還要記得帶 `random_state=42`。 |
| `max_depth=None` 寫成 `"None"` | `None` 是 Python 的「沒有值」，清單裡直接放 `None`，不要加引號。 |
| `export_text` 印出 `feature_0` | 忘了傳 `feature_names=feature_names`。 |
| 特徵重要性某個是 `0.0` | 不是壞掉——代表那個指標沒被拿來分岔。 |
| 想拿它去真的預測股票 | **別。** 樣本外才 5 成，跟擲銅板差不多。今天學的是「怎麼誠實驗證模型」，不是「這台能拿去下單」。 |
| 整本想快速確認環境 | 跑最後一格「最小可跑核心」，兩行都印 `[0 1]` 就沒問題。 |

## 版本

- v1.1（2026-07-22）B/C 段資料源由 `make_classification` 改為 **Yahoo Finance 真股票**（8 檔台灣大型股、5 技術指標、隔日漲跌）；train/test 由隨機切改為**時序切分**；新增 `data/prices_cache.csv` 快取與離線 backup。Part A 手刻 6 家不變。
- v1.0（2026-07-20）初版。由原「模組 3 KNN」＋「模組 4 決策樹」兩份教具合併而成。
