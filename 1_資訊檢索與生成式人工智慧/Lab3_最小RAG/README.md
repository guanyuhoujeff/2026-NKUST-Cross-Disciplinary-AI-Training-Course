# Lab 3：最小 RAG ⭐

把**上午的檢索**和**下午的生成**縫成一個會**查資料再回答**的 RAG：
文件切塊 → 本機 embedding → FAISS 向量庫 → 檢索最相關的 k 塊 → 連同問題餵給雲端 LLM。

並親手量出 **RAG 為什麼不能用「全部貼進 prompt」取代**（token 差好幾倍），以及**護欄擋得住什麼、擋不住什麼**。

---

## 📁 檔案

| 檔案 | 用途 |
|---|---|
| `Lab3_最小RAG_教學版.ipynb` | **課堂用**。核心程式碼挖成 `____`，照 `# TODO` 提示自己填 |
| `Lab3_最小RAG_完整版.ipynb` | **回家複習用**。全部有答案 + `💡` 註解 + 小作業參考解 |
| `data/` | 三份**虛構的**宏圖飲料財報（財報摘要、法說會逐字稿、股利與風險揭露） |
| `requirements.txt` | Python 套件（與 Lab 2 同一份） |

> ⚠️ `data/` 裡的公司、數字**全是虛構教學範例**，不是真實行情，請勿引用。
> 用虛構公司是刻意的——模型訓練時沒看過它，「有 RAG / 沒 RAG」的差別才看得出來。

---

## 🔧 開始之前

**Lab 2 的環境四步（Ollama、API key、套件）如果都做過了，只剩下面這一步。**

### 拉 embedding 模型

```bash
ollama pull bge-m3
```

1.2GB，**課前就要拉好**（現場拉會等很久）。它負責把文字變成向量，**跑在你自己的電腦、不花錢、不耗雲端額度**。

> ❌ 下載中斷 → 重跑同一行，會續傳。

### 確認 key 還在

環境變數**只在當前終端機視窗有效**。中午換過視窗、重開過終端機的話要重設：

```bash
export OLLAMA_API_KEY=你的key        # Windows PowerShell：$env:OLLAMA_API_KEY="你的key"
```

**設好之後，要從那個視窗啟動 Jupyter**，notebook 才拿得到。

---

## ▶️ 開始

```bash
jupyter notebook
```

打開 `Lab3_最小RAG_教學版.ipynb`，**從上往下一格一格跑**（不能跳著執行）。
開頭有 4 格環境自我檢查，四個燈全綠再往下走。

---

## 🛟 出事了怎麼辦

| 狀況 | 怎麼辦 |
|---|---|
| `KeyError: 'OLLAMA_API_KEY'` | key 沒設，或設完沒重開 kernel |
| `model not found` | 生成模型名要帶 cloud tag（`gemma4:cloud`） |
| 連不上 `localhost:11434` | 本機 Ollama 沒起來 → 開一次 Ollama App，或下 `ollama serve`。**這個紅燈會擋住整個 Lab**（embedding 要靠它） |
| 建向量庫那格跑很久 | 正常——它要把每一塊都算成向量。這就是「建索引做一次」的那一次 |
| 檢索撈回來的塊很怪 | 先印出 `hits` 看撈到什麼。**RAG 答錯，多半錯在檢索、不是模型笨** |
| **`faiss-cpu` 裝不起來**（Windows 常見） | 改用 chromadb：`pip install langchain-chroma`，然後把 `FAISS.from_documents(chunks, emb)` 換成 `Chroma.from_documents(chunks, emb)`（`similarity_search` 用法一模一樣） |
| **雲端不通 / 額度用完** | 跑 notebook 最後的 Backup 格，改用本機 `llama3.2:3b` 生成（品質降，但流程照樣走完） |

---

## 📌 用到的模型

| 模型 | 跑在哪 | 做什麼 |
|---|---|---|
| `bge-m3` | **本機**（不花錢） | 把文字變成 1024 維向量 |
| `gemma4:cloud` | 雲端（要 key、扣額度） | 看著檢索到的資料寫出答案 |
| `llama3.2:3b` | 本機 | 只在雲端不通時當 Backup |
