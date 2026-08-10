# 模組 5 情緒打分機：用 LLM 把財經新聞打成情緒分數

把一則財經新聞丟給 LLM → 判斷利多／利空／中性、給一個 0~1 分數 → 批次跑一批新聞、每檔每天平均成一欄 `news_sent`，存成 CSV 餵回選股模型。這一欄之後可以當作模型的一個特徵——今天是它的「出生地」。

## 怎麼開始

```bash
pip install -r requirements.txt
jupyter notebook Lab5_情緒打分機_教學版.ipynb
```

或直接在 notebook 裡跑第一格的 `!pip install`。

## 需要什麼

- **Ollama Cloud key**：這個 Lab 會呼叫雲端 `gemma4:cloud` 生成，需要 `OLLAMA_API_KEY`。在 notebook 第二格把引號中間換成老師給你的 key（沿用課程 1 的設定）。
- **會中文的生成模型**：跟課程 1 一路用的 `gemma4:cloud` 相同，不重裝。
- 解析分數、聚合 `news_sent` 的部分**全是純本地 Python／pandas**，不依賴 LLM、每次跑都一樣。

## 檔案

| 檔案 | 用途 |
|---|---|
| `Lab5_情緒打分機_教學版.ipynb` | 課堂用，引導式填空 |
| `Lab5_情緒打分機_完整版.ipynb` | 回家複習，含全部解答與執行結果 |

**沒有 `data/` 資料夾**——今天的新聞全部是程式裡自己編的虛構示意新聞，不需要任何外部檔案。`news_sent.csv` 由 C 段當場產生。

## 內容

- **A** 為什麼把新聞變分數 → zero-shot 直接問（看 LLM 回的自由文字、很亂、抽不出乾淨分數）
- **B** few-shot ＋ 要求回 JSON ＋ 穩健 parser → 拿到能存表格的 `{label, score}` → 包成 `score_news()`
- **C** `to_signed` 方向分 → 批次跑一批新聞 → `groupby` 每檔每天平均 → 一欄 `news_sent` → 存 CSV（＋FinBERT 對比，只講不動手）
- **D** 收尾：文字路第一塊完成、金融三鐵則免責

## 關於分數「每次不一樣」

LLM 是**非決定性**的——沒有 `random_state` 可固定，每次回傳都可能略不同。所以：

- `label`（利多／利空／中性）對明顯的新聞應該大致一致；`score` 的數值會浮動，**這是正常的**。
- 純 Python 的部分（`parse_sentiment` 四案例、`to_signed`、`groupby`）每次跑都一樣。
- 這也是為什麼要 few-shot＋JSON 框住格式、用 parser 接住、最後 `groupby` 平均看趨勢，而不是死摳單一數字。

## Backup（跟不上時）

- **`401`／key 沒設**：把第二格引號中間換成你的 key，重跑那一格。
- **`model not found`**：漏了 `:cloud` tag，要寫完整 `gemma4:cloud`。
- **雲端斷線／額度用完**：讀老師預先算好的 `news_sent.csv` 離線檔，照樣練 `to_signed`／`groupby`。
- **LLM 沒回 JSON**：正常——`parse_sentiment` 會退回關鍵字、再不行給中性 0.5，永遠回得出 `{label, score}`。
- 卡在某一格時，跑最後的「最小可跑核心」（純 Python、不需 Ollama），能跑就代表核心觀念沒問題。

## 版本歷史

- **v1.0**（2026-07-22）：初版雙版本。走草稿交棒法：完整版用真 Ollama key 端到端跑過補真實輸出（LLM 輸出每次不同、屬示意；純 Python 骨幹決定性）。
