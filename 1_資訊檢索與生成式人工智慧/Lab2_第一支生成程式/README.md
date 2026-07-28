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

### 第 3 步：拿一把 Ollama Cloud API key（呼叫雲端的「門票」）

到 **https://ollama.com/settings/keys** 建一把 key、整串複製起來，**先放著**——
今天**不用設環境變數**（那步容易出錯）。等一下在 notebook 最上面的「檢查 2」那格，把 key 直接貼進引號中間就好：

```python
os.environ["OLLAMA_API_KEY"] = "在這裡貼上你的 OLLAMA key"   # ← 把引號中間換成你的 key，再跑這一格
```

> ⚠️ **整串貼進引號中間，前後不要多留空格**。
> ⚠️ **貼了 key 的 notebook 別上傳 GitHub、別傳給別人、別截圖**——key 等於你帳號的鑰匙。
> ❌ 註冊不了 / key 貼壞了 → 找講師拿共用 key。

### 第 3.5 步：辦第二把 Gemini key（**課前必辦**，這門課會用到）

除了上面的 Ollama key，**每個人還要辦一把自己的 Gemini key**——到 **https://aistudio.google.com/apikey**，用 **Google 帳號登入**即可**免費**建一把，同樣**先放記事本存著**。等一下在 notebook 最上面的「檢查 2」那格，跟 Ollama key 一起貼進去：

```python
os.environ["GOOGLE_API_KEY"] = "在這裡貼上你的 Gemini key"   # ← 把引號中間換成你的 key，再跑這一格
```

> ⚠️ **一人一把自己的 key**，同樣別上傳 GitHub、別截圖。
> ⚠️ **課前先確認**：極少數帳號辦 Gemini key 時會被要求綁信用卡——**課前先點一次確認拿得到 key**，別留到上課才發現卡關。
> ❌ 辦不了 → 找講師拿共用 key。

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

啟動 Jupyter：

```bash
jupyter notebook
```

打開 `Lab2_第一支生成程式_教學版.ipynb`，**從上往下一格一格跑**（不能跳著執行）。第一次跑到「檢查 2」那格時，記得先把你的 OLLAMA key 貼進去（見第 3 步）。

---

## 🛟 出事了怎麼辦

| 狀況 | 怎麼辦 |
|---|---|
| `KeyError: 'OLLAMA_API_KEY'` | 沒跑到貼 key 的那格 → 回 notebook 最上面「檢查 2」那格貼好 key，再從頭一格格跑 |
| `model not found` | 模型名漏了 cloud tag（要 `gemma4:cloud`） |
| `401` / 認證失敗 | key 貼錯（前後別留空格）→ 檢查「檢查 2」那格引號中間的 key |
| 跑很久沒反應 | 雲端要幾秒到十幾秒才回，**不是當掉**；真的太久就重跑那格 |
| **雲端不通 / 額度用完** | **降本地生成**：先 `ollama pull llama3.2:3b`，再跑 notebook 最後的 Backup 格（品質降，但整個 Lab 照樣做得完） |

---

## 📌 用到的模型

| 模型 | 跑在哪 | 這個 Lab 用它做什麼 |
|---|---|---|
| `gemma4:cloud` | 雲端（Ollama Cloud） | **生成回答**（今天的主角） |
| `bge-m3` | 本機 | 今天不用——**Lab 3** 做 embedding 用 |
| `llama3.2:3b` | 本機 | 只在雲端不通時當 Backup |

---

## 版本歷史

| 版本 | 日期 | 內容 |
|---|---|---|
| v1.0 | 2026-07-14 | 初版。32 cells × 2 版，6 處挖空（挖空點由講師親自標定）。完整版以**真實 API key 實跑**過，輸出為真實結果。**教具已同步至 v2.0。** |
| v1.1 | 2026-07-14 | **embedding 模型改為 `bge-m3`**（第 2 步、檢查 4、模型表）。Lab 3 實跑證實 `nomic-embed-text` 經 LangChain 呼叫時對中文財報的檢索是壞的（六個不同問題 top-1 全撈回同一塊）。**Lab 2 本身的教學內容一字未動**，只換學員課前要拉的模型。 |
| v1.2 | 2026-07-16 | **API key 改為 notebook 內直接貼**（教學版＋完整版的「檢查 2」那格 `os.environ["OLLAMA_API_KEY"] = "..."`、Gemini 同款）——學員不必設環境變數。README 第 3 步、啟動說明、排錯表同步。**公開版一律放佔位字串，真 key 絕不進版控。** |

**v1.0 相對於 Lab 2 教具 v1.1 的訂正**——實跑後發現教具有誤，notebook 以實測為準；**教具已於 2026-07-14 同步為 v2.0**（見教具設計筆記）：

1. **拿掉 `temperature` 示範**。實測 `gemma4:cloud` **完全忽略 temperature**（0.0～2.0 輸出都在變、給 `seed` 也一樣），教具 §5-2「溫度差異較細微」的說法不成立。換 `gpt-oss:20b-cloud` 也不行（temp=0 仍不穩，且會吐簡體字）。**溫度概念改由投影片講述，不做上機示範。**
2. **`num_predict` 從 30 改 20**，並把提問改成「詳細解釋…並舉例」——30 有時剛好收在句號，看不出被截斷。
3. **幻覺那格問法拿掉年份**（改問「最近一季」）。原本問「2026 Q1」，模型會用「時間還沒到」當理由拒答，失焦；改問法後它穩定回「知識庫中沒有這家公司」，並主動說「可以提供相關文件給我」——正好接到下一格。
4. **新增「看 token 用量」一格**（`usage_metadata`），並修正教具「token ≈ 可見字數」的說法：實測回答 39 個字只算 28 個 token。
5. **新增「把資料跟問題一起送」一格**——手工做一次 RAG 的最後一刀，作為 Lab 3 的橋樑。
