import requests
import streamlit as st
import traceback
from datetime import datetime
from utils import log_to_console

class NewsService:
    def __init__(self):
        self.N8N_WEBHOOK_READ = "https://n8n.defintek.io/webhook/read_news"
        self.N8N_WEBHOOK_UPDATE = "https://n8n.defintek.io/webhook/update_news"

    def fetch_news(self, date_str):
        """獲取特定日期的新聞。"""
        try:
            # 記錄獲取嘗試與時間戳記（使用 log_to_console 讓 F12 可見）
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                log_to_console(f"🔍 [{current_time}] fetch_news called for date: {date_str}")
            except:
                pass  # 若 log_to_console 失敗則靜默處理
            
            response = requests.get(self.N8N_WEBHOOK_READ, params={"date": date_str})
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    if not data:
                        # 空列表 - 檢查日期以決定訊息
                        selected_date = datetime.strptime(date_str, "%Y/%m/%d").date()
                        today = datetime.today().date()
                        
                        if selected_date > today:
                            # 未來日期 - 無此表單
                            return {"status": "future_date", "message": "📅 無此日期資料請重選日期", "data": []}
                        else:
                            # 過去/今天 - 無新聞資料
                            return {"status": "no_news", "message": "📭 本日無新聞資料", "data": []}
                    elif len(data) == 1 and "message" in data[0]:
                        # 回應包含訊息（例如 "RAW 資料為空..."）
                        # 使用日期決定適當的回應
                        selected_date = datetime.strptime(date_str, "%Y/%m/%d").date()
                        today = datetime.today().date()
                        
                        if selected_date > today:
                            # 未來日期 - 無此表單
                            return {"status": "future_date", "message": "📅 無此日期資料請重選日期", "data": []}
                        else:
                            # 過去/今天 - 無新聞資料
                            return {"status": "no_news", "message": "📭 本日無新聞資料", "data": []}
                    else:
                        # 實際新聞資料
                        normalized_data = [item.get("json", item) for item in data]
                        return {"status": "success", "data": normalized_data}
                else:
                    return {"status": "error", "message": "n8n 回傳資料格式錯誤"}
            else:
                # 檢查錯誤回應是否表示表單未找到
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
        """發送評論至 n8n。"""
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
                # 避免顯示過長的 HTML 錯誤訊息
                error_text = response.text
                if len(error_text) > 200 or "<html" in error_text.lower():
                    error_text = f"伺服器回應錯誤 (代碼: {response.status_code})"
                return {"status": "error", "message": f"n8n 回應錯誤: {error_text}"}
        except Exception as e:
            return {"status": "error", "message": f"無法連線到 n8n 評論: {e}"}
