import requests
import streamlit as st
import traceback

class NewsService:
    def __init__(self):
        self.N8N_WEBHOOK_READ = "https://n8n.defintek.io/webhook/read_news"
        self.N8N_WEBHOOK_UPDATE = "https://n8n.defintek.io/webhook/update_news"

    def fetch_news(self, date_str):
        """Fetch news for a specific date."""
        try:
            response = requests.get(self.N8N_WEBHOOK_READ, params={"date": date_str})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and data:
                    if len(data) == 1 and "message" in data[0]:
                        return {"status": "success", "message": data[0]["message"], "data": []}
                    else:
                        # Normalize data structure
                        normalized_data = [item.get("json", item) for item in data]
                        return {"status": "success", "data": normalized_data}
                else:
                    return {"status": "warning", "message": "n8n 回傳資料為空"}
            else:
                return {"status": "error", "message": f"n8n 回應錯誤: {response.text}"}
        except Exception as e:
            return {"status": "error", "message": f"無法連線到 n8n 更新 : {e}", "traceback": traceback.format_exc()}

    def post_comment(self, sheet_name, row_index, comment):
        """Post a comment to n8n."""
        try:
            payload = {
                "sheetName": sheet_name,
                "rowIndex": row_index,
                "comment": comment
            }
            response = requests.post(self.N8N_WEBHOOK_UPDATE, json=payload)
            if response.status_code == 200:
                return {"status": "success", "message": "評論已送出！"}
            else:
                return {"status": "error", "message": f"n8n 回應錯誤: {response.text}"}
        except Exception as e:
            return {"status": "error", "message": f"無法連線到 n8n 評論: {e}"}
