# Web3 精選新聞 App

這是一個使用 Streamlit 建立的 Web3 新聞閱讀應用程式，透過 n8n webhook 取得和更新新聞資料。

## 功能

- 📰 顯示每日精選 Web3 新聞
- ⭐ 查看 AI 評選原因和分數
- 💬 對新聞留下評論
- 🔄 即時更新新聞列表

## 本地運行

1. 安裝依賴：
```bash
pip install -r requirements.txt
```

2. 運行應用：
```bash
streamlit run n8nAPP.py
```

## 部署到 Streamlit Cloud

### 步驟 1: 將代碼推送到 GitHub

1. 在 GitHub 上創建一個新的倉庫（如果還沒有）
2. 初始化 git 並推送代碼：
```bash
git init
git add .
git commit -m "Initial commit: Web3 news app"
git branch -M main
git remote add origin https://github.com/yueh722/你的倉庫名稱.git
git push -u origin main
```

### 步驟 2: 在 Streamlit Cloud 部署

1. 前往 [Streamlit Cloud](https://streamlit.io/cloud) 並登入
2. 點擊 "New app" 按鈕
3. 連接你的 GitHub 帳號（如果還沒連接）
4. 選擇你的倉庫 (`yueh722/你的倉庫名稱`)
5. 設置主文件路徑為：`n8nAPP.py`
6. 點擊 "Deploy!"

### 步驟 3: 配置 Secrets（可選）

如果你想使用不同的 webhook URLs，可以在 Streamlit Cloud 設置 secrets：

1. 在 Streamlit Cloud 的應用頁面，點擊右上角的 "⋮" 選單
2. 選擇 "Settings" → "Secrets"
3. 添加以下格式的 secrets：
```toml
[n8n]
webhook_read = "https://n8n.defintek.io/webhook/read_news"
webhook_update = "https://n8n.defintek.io/webhook/update_news"
```

**注意**：如果不設置 secrets，應用會使用代碼中的預設 webhook URLs。

## 配置說明

應用會優先從 Streamlit secrets 讀取 n8n webhook URLs，如果沒有設置則使用代碼中的預設值：
- `N8N_WEBHOOK_read`: 讀取新聞的 webhook
- `N8N_WEBHOOK_update`: 更新評論的 webhook

