# Lab 2：第一支生成程式

寫出第一支**會呼叫 LLM、印出它生成文字**的程式：`ChatOllama` 指向雲端 → `invoke` 送問題 → `.content` 取回答。
順便看見 **token 成本**、玩 **`num_predict`**，最後親眼看到 **LLM 的幻覺**，並手工治好它一次（＝下午 Lab 3 RAG 的雛形）。

> **這個 Lab 也負責把 Lab 3 的環境一次設好**——第 2、4 步拉的模型與套件今天用不到，是給 Lab 3 用的。

---

## 📁 檔案

| 檔案 | 用途 |
|---|---|
| `Lab2_第一支生成程式_教學版.ipynb` | **課堂用**。核心程式碼挖成 `____`，照 `# TODO` 提示自己填（共 5 處） |
| `Lab2_第一支生成程式_完整版.ipynb` | **回家複習用**。全部有答案 + `💡` 註解 + 小作業參考解 |
| `requirements.txt` | Python 套件 |

---

## 🔧 開始之前：環境五步

notebook 開頭有 4 格**環境自我檢查**，跑一格看一個燈。下面是紅燈時要回頭補的步驟。

### 第 1 步：裝 Ollama 並確認服務在跑

到 **https://ollama.com/download**（會自動偵測你的系統）：

- **Windows**：下載 `OllamaSetup.exe`，雙擊安裝（裝完**重開終端機**讓 PATH 生效）
- **macOS**：下載 `Ollama.dmg`，拖進 Applications
- **Linux**：`curl -fsSL https://ollama.com/install.sh | sh`

確認：

```bash
ollama --version     # 看到版本號 = 已裝
ollama list          # 能列出來（就算是空清單）= 背景服務通
```

> ❌ `command not found` → 沒裝好（Windows 記得重開終端機）
> ❌ `could not connect` → 服務沒起：開一次 Ollama App，或下 `ollama serve`

### 第 2 步：拉 embedding 模型（**這步是為 Lab 3 鋪路**）

```bash
ollama pull bge-m3
```

1.2GB。**今天的生成用不到它**——Lab 3 要用它把文件變成向量（本地跑、不花錢）。**檔案不小，趁現在拉好**，下午就不用等下載。

> ❌ 下載中斷 → 重跑同一行，會續傳。

### 第 3 步：設定 Ollama Cloud API key（呼叫雲端的「門票」）

先到 **https://ollama.com/settings/keys** 建一把 key，整串複製，然後：

```bash
# Mac / Linux
export OLLAMA_API_KEY=你的key

# Windows PowerShell
$env:OLLAMA_API_KEY="你的key"
```

確認有設進去（會印出你那串 key，不是空白）：

```bash
echo $OLLAMA_API_KEY            # Windows PowerShell：echo $env:OLLAMA_API_KEY
```

> ⚠️ **`=` 後面直接貼，前後不要留空格、不要加引號**——多一個空格就會 `KeyError`。
> ⚠️ **環境變數只在「當前終端機視窗」有效**。換視窗、重開終端機就要重設。
> ⚠️ **設好之後，要從那個視窗啟動 Jupyter**（或重開 kernel），notebook 才拿得到。
> ❌ 註冊不了 / key 貼壞了 → 找講師拿共用 key。

### 第 4 步：裝套件（**一次裝齊 Lab 2 + Lab 3 要用的**）

```bash
pip install -r requirements.txt
```

Lab 2 只會用到 `langchain-ollama`；其餘三個是 Lab 3 的 RAG 要用的（切塊、向量庫），一起裝好省得下午再等。

> ❌ Windows 上 `faiss-cpu` 偶爾裝不起來 → **今天不影響**，Lab 3 前再處理。

### 第 5 步：不寫 Python，先確認雲端這條路通不通

```bash
ollama run gemma4:cloud "用一句繁體中文說明什麼是毛利率"
```

幾秒內會串流出一句中文。**這一步繞過所有 Python**，先確認「帳號 + key + 雲端」是通的——這裡通了，notebook 裡出問題才不會把「帳號問題」跟「程式問題」混在一起。

> ❌ `model not found` → 模型名要帶 cloud tag（`gemma4:cloud`）
> ❌ `401` / 認證失敗 → key 沒設對，回第 3 步

---

## ▶️ 開始

從**設好 key 的那個終端機視窗**啟動：

```bash
jupyter notebook
```

打開 `Lab2_第一支生成程式_教學版.ipynb`，**從上往下一格一格跑**（不能跳著執行）。

---

## 🛟 出事了怎麼辦

| 狀況 | 怎麼辦 |
|---|---|
| `KeyError: 'OLLAMA_API_KEY'` | key 沒設，或設完沒重開 kernel → 回第 3 步 |
| `model not found` | 模型名漏了 cloud tag（要 `gemma4:cloud`） |
| `401` / 認證失敗 | key 貼錯（前後別留空格、別加引號）→ 回第 3 步 |
| 跑很久沒反應 | 雲端要幾秒到十幾秒才回，**不是當掉**；真的太久就重跑那格 |
| **雲端不通 / 額度用完** | **降本地生成**：先 `ollama pull llama3.2:3b`，再跑 notebook 最後的 Backup 格（品質降，但整個 Lab 照樣做得完） |

---

## 📌 用到的模型

| 模型 | 跑在哪 | 這個 Lab 用它做什麼 |
|---|---|---|
| `gemma4:cloud` | 雲端（Ollama Cloud） | **生成回答**（今天的主角） |
| `bge-m3` | 本機 | 今天不用——**Lab 3** 做 embedding 用 |
| `llama3.2:3b` | 本機 | 只在雲端不通時當 Backup |
