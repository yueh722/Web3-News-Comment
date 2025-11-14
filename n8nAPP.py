import streamlit as st
import requests
from datetime import datetime
import traceback

# 兼容舊版本 Streamlit 的 rerun 方法
def rerun():
    """兼容不同版本的 Streamlit rerun 方法"""
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()
    # 如果都没有，按钮点击会自动触发重新运行

# ====== n8n Webhook URL ======

N8N_WEBHOOK_read = "https://n8n.defintek.io/webhook/read_news"
N8N_WEBHOOK_update = "https://n8n.defintek.io/webhook/update_news"

# ====== Streamlit 標題 ======
# 使用自定義樣式調整標題大小，避免手機上換行
st.markdown(
    """
    <style>
    .custom-title {
        font-size: 1.5rem !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    

    @media (max-width: 768px) {
        /* 手機上強制按鈕保持同一行 - 更強力的規則 */
        [data-testid="column"],
        div[data-testid="column"],
        .stColumns [data-testid="column"],
        .element-container [data-testid="column"],
        .stColumns > div > div {
            flex: 1 1 0% !important;
            min-width: 0 !important;
            max-width: 33.33% !important;
            flex-shrink: 1 !important;
            flex-basis: 0 !important;
        }
       
    }
    </style>
    <h1 class="custom-title">✨ Web3 精選新聞 ✨</h1>
    """,
    unsafe_allow_html=True
)

# ====== 初始化 Session State ======
if "today_rows" not in st.session_state:
    st.session_state.today_rows = []
if "comment_values" not in st.session_state:
    st.session_state.comment_values = {}
if "star_container" not in st.session_state:
    st.session_state.star_container = st.empty()
if "status_container" not in st.session_state:
    st.session_state.status_container = st.empty()
if "controls_container" not in st.session_state:
    st.session_state.controls_container = st.empty()
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "selected_date" not in st.session_state:
    st.session_state.selected_date = datetime.today().date()
if "current_date" not in st.session_state:
    st.session_state.current_date = datetime.today().date()

# ====== 顯示狀態 ======
def update_status(current_index):
    # 獲取目前設定的日期字串
    selected_date_str = st.session_state.selected_date.strftime("%Y/%m/%d")
    
    if st.session_state.today_rows:
        # 從 today_rows 中獲取當前行的數據
        if 0 <= current_index < len(st.session_state.today_rows):
            row = st.session_state.today_rows[current_index]
            st.session_state.status_container.info(
                f"已取得 {selected_date_str} 新聞共 {len(st.session_state.today_rows)} 則 | NO.{row['sno']}  idx:{current_index}"
            )
        else:
            st.session_state.status_container.info(
                f"已取得 {selected_date_str} 新聞共 {len(st.session_state.today_rows)} 則 |  idx:{current_index}"
            )
    else:
        st.session_state.status_container.warning(f"請先按 🔄 更新，取得新聞內容")

# ====== 顯示新聞 ======
def show_current_star(data, index):
    with st.session_state.star_container.container():
        # 日期選擇器（無論是否有數據都顯示，位置一致，取代原本的日期顯示）
        st.session_state.selected_date = st.date_input(
            "選擇日期：",
            value=st.session_state.selected_date,
            key="date_picker"
        )
        
        # 如果沒有數據，只顯示日期選擇器後返回
        if not data:
            return

        row = data[index]    
        
        current_date_str = st.session_state.current_date
        st.write(f"{current_date_str}")


        # 分開顯示 NO.5 和標題，並為 NO.5 添加顏色
        st.markdown(
            f"""
            <div style="margin-bottom: 0.5rem;">
                <span style="color: #FF6B6B; font-weight: bold; font-size: 1.1em;">NO.{row['sno']}</span>
            </div>
            <h3 style="margin-top: 0.2rem;">{row['標題']}</h3>
            """,
            unsafe_allow_html=True
        )
        st.write(f"{row['url']}")
        st.write(f"{row['ai評選原因']}")
        st.write(f"分數: {row['分數']}")
        st.write(f"主題: {row['主題']}")
        #st.write(f"備註: {row['備註']}")
        #st.write(f"評論: {row['評論']}")

        # ====== 按鈕（顯示在主題和留下評論之間）======
        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            if st.button("⬅ 上一則", key=f"prev_{row.get('sno')}_{row.get('日期')}"):
                if(st.session_state.current_index > 0):
                    st.session_state.current_index -= 1
                    rerun()

        with col2:
            if st.button("🔄 更新", key=f"update_{row.get('sno')}_{row.get('日期')}"):
                button_update_content()
        with col3:
            if st.button("➡ 下一則", key=f"next_{row.get('sno')}_{row.get('日期')}"):
                if(st.session_state.current_index < (len(st.session_state.today_rows)-1)):    
                    st.session_state.current_index += 1
                    rerun()

        comment_key = f"comment_{row.get('sno')}_{row.get('日期')}"

        # 初始化 session_state 
        if comment_key not in st.session_state:
            st.session_state[comment_key] = str(row.get("評論", ""))


        comment = st.text_area(
            "留下評論：",
            value=st.session_state[comment_key],
            key=comment_key
        )
        

        button_key = f"send_comment_{row.get('列號')}_{row.get('日期')}"
        if st.button("送出評論", key=button_key):
            try:
                # 使用選擇的日期作為 sheetName
                sheet_name = st.session_state.selected_date.strftime("%Y/%m/%d")
                payload = {
                    "sheetName": sheet_name, 
                    "rowIndex": row["列號"],   
                    "comment": comment
                }

                #st.json(payload)
                #st.write("即將送出的 payload：", payload)


                response = requests.post(N8N_WEBHOOK_update, json=payload)
                if response.status_code == 200:
                    st.success("評論已送出！")

                    for r in st.session_state.today_rows:
                        if r["列號"] == row["列號"]:
                            r["評論"] = comment
                            break

                else:
                    st.error(f"n8n 回應錯誤: {response.text}")
            except Exception as e:
                st.error(f"無法連線到 n8n 評論: {e}")


def button_update_content():
                selected_date_str = st.session_state.selected_date.strftime("%Y/%m/%d")
                try:
                    response = requests.get(N8N_WEBHOOK_read, params={"date": selected_date_str})
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list) and data:
                            if len(data) == 1 and "message" in data[0]:
                                st.success(data[0]["message"])  
                            else:    
                                st.session_state.today_rows = [item.get("json", item) for item in data]
                                st.session_state.current_index = 0
                                st.session_state.current_date = selected_date_str
                                rerun()
                        else:
                            st.warning("n8n 回傳資料為空")
                    else:
                        st.error(f"n8n 回應錯誤: {response.text}")
                except Exception as e:
                    st.error(f"無法連線到 n8n 更新 : {e}")
                    st.text(traceback.format_exc())



# ====== 按鈕（只在還沒有更新時顯示在底部）======
if not st.session_state.today_rows:
    with st.session_state.controls_container.container():
        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            st.empty()  # 左側空白

        with col2:
            if st.button("🔄 更新", key="update_initial"):
                button_update_content()
        with col3:
            st.empty()  # 右側空白
            
# ====== 顯示目前新聞和狀態 ======
update_status(st.session_state.current_index)
show_current_star(st.session_state.today_rows, st.session_state.current_index)
