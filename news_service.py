import requests
import streamlit as st
import traceback
from datetime import datetime

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
                
                if isinstance(data, list):
                    if not data:
                        # Empty list - check date to determine message
                        selected_date = datetime.strptime(date_str, "%Y/%m/%d").date()
                        today = datetime.today().date()
                        
                        if selected_date > today:
                            # Future date - no such sheet
                            return {"status": "future_date", "message": "📅 無此日期資料請重選日期", "data": []}
                        else:
                            # Past/Today date - no news data
                            return {"status": "no_news", "message": "📭 本日無新聞資料", "data": []}
                    elif len(data) == 1 and "message" in data[0]:
                        # Response contains a message (e.g., "RAW 資料為空...")
                        # Use date to determine the appropriate response
                        selected_date = datetime.strptime(date_str, "%Y/%m/%d").date()
                        today = datetime.today().date()
                        
                        if selected_date > today:
                            # Future date - no such sheet
                            return {"status": "future_date", "message": "📅 無此日期資料請重選日期", "data": []}
                        else:
                            # Past/Today date - no news data
                            return {"status": "no_news", "message": "📭 本日無新聞資料", "data": []}
                    else:
                        # Actual news data
                        normalized_data = [item.get("json", item) for item in data]
                        return {"status": "success", "data": normalized_data}
                else:
                    return {"status": "error", "message": "n8n 回傳資料格式錯誤"}
            else:
                # Check if error response indicates sheet not found
                error_text = response.text.lower()
                if "not found" in error_text or "404" in error_text or "找不到" in response.text or "不存在" in response.text:
                    return {"status": "error", "message": "📅 無此日期資料請重選日期"}
                return {"status": "error", "message": f"n8n 回應錯誤: {response.text}"}
        except Exception as e:
            error_msg = str(e).lower()
            if "not found" in error_msg or "404" in error_msg:
                return {"status": "error", "message": "📅 無此日期資料請重選日期"}
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
