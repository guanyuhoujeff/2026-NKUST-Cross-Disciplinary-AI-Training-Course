# Lab 3 KNN 與決策樹：兩台分類器，同一把誠實的尺

用虛構的財務指標親手做出**兩台**「猜漲跌」的分類器，然後在同一份資料、同一個切法上比一比——並且看它們**用同一種方式壞掉**。

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

**沒有 `data/` 資料夾**——今天的資料全部由程式當場生成（6 家手寫虛構公司 ＋ `make_classification` 生的 200 家），不需要任何外部檔案。

## 內容

- **A** 兩種判法各手刻一次：純 Python 算距離投票（KNN）／巢狀 `if/else`（決策樹）
- **B** sklearn 同一個介面跑兩台：`fit` / `predict` / `score` ＋ 決策樹的 `export_text`、`feature_importances_`
- **C** ⭐ 課程重點：切一次 train/test → **掃 k → 掃 `max_depth`**，兩張表並排看「樣本內 100% 是陷阱」
- **D** 收尾

## 環境需求

- Python 3.9+、scikit-learn、pandas、numpy
- **全程離線可跑**：不需要網路、不需要 API key、不需要 Ollama

## 數字說明

**今天全班的數字應該一模一樣**（資料是程式生的、亂數種子固定）——這跟 Lab 1 抓活網站相反。跟教材不一樣就是有地方跑掉了。

已在 **scikit-learn 1.6.1 / 1.7.2 / 1.8.0** 三個版本上驗證，輸出完全相同；pandas 2.x / 3.x 皆可。

## Backup

| 狀況 | 怎麼辦 |
|---|---|
| `No module named 'sklearn'` | 跑第一格的 `!pip install`。**套件名是 `scikit-learn`，import 名是 `sklearn`**。裝不動改用 Colab（已內建）。 |
| **數字跟教材不一樣** | 幾乎都是漏了 `random_state=42`。今天有**三處**要帶：`make_classification`、`train_test_split`、`DecisionTreeClassifier`（KNN 不用，它沒有隨機性）。 |
| `make_classification` 的數字是負的 | 正常，它生的是標準化過的虛構數。 |
| `max_depth=None` 寫成 `"None"` | `None` 是 Python 的「沒有值」，清單裡直接放 `None`，不要加引號。 |
| `export_text` 印出 `feature_0` | 忘了傳 `feature_names=feature_names`。 |
| 特徵重要性某個是 `0.0` | 不是壞掉——代表那個指標沒被拿來分岔。 |
| 整本想快速確認環境 | 跑最後一格「最小可跑核心」，兩行都印 `[0 1]` 就沒問題。 |

## 版本

- v1.0（2026-07-20）初版。由原「模組 3 KNN」＋「模組 4 決策樹」兩份教具合併而成。
