import streamlit as st
import requests
import urllib.parse
import pandas as pd

# 1. Thiết lập cấu hình hiển thị giao diện
st.set_page_config(page_title="Siêu Trợ Lý Đa Năng", page_icon="🚀", layout="centered")
st.title("🚀 Siêu Trợ Lý Đa Năng & Hệ Thống Thiết Bị")
st.write("Phiên bản Bất Tử - Đã tối ưu băng thông chống nghẽn mã lỗi 429.")

# 2. Cấu hình khóa bảo mật API Key mới của bạn
API_KEY = "AIzaSyDMtxpAtB3sDdLxJY9SJ4UQl-xlu0kFGQ8"

# =========================================================================
# LỆNH HUẤN LUYỆN HỆ THỐNG: Khởi tạo tính cách ngắn gọn để tiết kiệm dung lượng
# =========================================================================
DU_LIEU_HUAN_LUYEN = "Bạn là Siêu Trợ Lý AI EQ cao, hỗ trợ giải trí (YouTube, nhạc) và thiết bị (camera, vị trí người yêu, gia đình). Nói tiếng Việt thân thiện, dùng nhiều icon."
# =========================================================================

if API_KEY == "HÃY_DÁN_MÃ_API_KEY_CỦA_BẠN_VÀO_ĐÂY":
    st.warning("⚠️ Vui lòng cấu hình chính xác mã API Key để kích hoạt ứng dụng!")
else:
    # 3. THANH DIỀU HƯỚNG CẠNH (SIDEBAR)
    st.sidebar.header("🛠️ Trung Tâm Thiết Bị & Bản Đồ")
    
    st.sidebar.subheader("📷 Kiểm tra Camera & Micro")
    cho_phep_camera = st.sidebar.checkbox("Bật Camera")
    if cho_phep_camera:
        hinh_anh = st.sidebar.camera_input("Camera thiết bị")
        if hinh_anh: st.sidebar.success("📸 Thành công!")
            
    cho_phep_micro = st.sidebar.checkbox("Bật Micro Ghi Âm")
    if cho_phep_micro:
        file_ghi_am = st.sidebar.audio_input("Giọng nói")
        if file_ghi_am: st.sidebar.success("🎙️ Đã lưu!")

    st.sidebar.write("---")

    st.sidebar.subheader("📍 Hệ Thống Định Vị (GPS)")
    vi_tri_ban_than = st.sidebar.text_input("Vị trí của Bạn:", "10.7626, 106.6602")
    vi_tri_nguoi_yeu = st.sidebar.text_input("Vị trí Người Yêu ❤️:", "10.7769, 106.7009")
    vi_tri_gia_dinh = st.sidebar.text_input("Vị trí Gia Đình 🏠:", "10.8231, 106.6297")
    
    try:
        lat1, lon1 = map(float, vi_tri_ban_than.split(","))
        lat2, lon2 = map(float, vi_tri_nguoi_yeu.split(","))
        lat3, lon3 = map(float, vi_tri_gia_dinh.split(","))
        data_toado = pd.DataFrame({'lat': [lat1, lat2, lat3], 'lon': [lon1, lon2, lon3]})
        st.sidebar.map(data_toado)
    except:
        pass

    st.sidebar.write("---")
    st.sidebar.subheader("📺 Tìm Kiếm YouTube & Nhạc")
    search_query = st.sidebar.text_input("Nhập tên bài hát:")
    if search_query:
        encoded_query = urllib.parse.quote(search_query)
        st.sidebar.markdown(f"🔗 [▶️ YouTube](https://www.youtube.com/results?search_query={encoded_query}) | [📥 Tải MP3](https://www.y2mate.com/vi/search/{encoded_query})")

    if st.sidebar.button("🗑️ Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

    # 4. Kiểm soát và hiển thị tiến trình hội thoại
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Xử lý logic khi gửi yêu cầu hội thoại
    if user_query := st.chat_input("Nhập nội dung cuộc trò chuyện tại đây..."):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        # CRITICAL TRICK: Nếu lịch sử dài quá 6 câu, tự động cắt bỏ những câu quá cũ để bảo vệ quota dữ liệu
        if len(st.session_state.messages) > 6:
            st.session_state.messages = st.session_state.messages[-6:]

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            headers = {'Content-Type': 'application/json'}
            
            # Cấu trúc nội dung siêu gọn nhẹ
            api_contents = []
            api_contents.append({
                "role": "user",
                "parts": [{"text": f"Yêu cầu hệ thống: {DU_LIEU_HUAN_LUYEN}\nLịch sử chat:"}]
            })
            api_contents.append({
                "role": "model",
                "parts": [{"text": "Đã hiểu rõ nhiệm vụ."}]
            })
            
            for msg in st.session_state.messages:
                role_name = "model" if msg["role"] == "assistant" else "user"
                api_contents.append({
                    "role": role_name,
                    "parts": [{"text": msg["content"]}]
                })

            payload = {"contents": api_contents}

            try:
                response = requests.post(url, headers=headers, json=payload)
                response_data = response.json()
                
                if response.status_code == 200:
                    ai_response = response_data['candidates'][0]['content']['parts'][0]['text']
                    message_placeholder.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                elif response.status_code == 429:
                    message_placeholder.markdown("⚠️ Bạn chat nhanh quá, đợi khoảng 10 giây rồi gõ tiếp nhé!")
                else:
                    error_msg = response_data.get('error', {}).get('message', 'Lỗi kết nối')
                    message_placeholder.markdown(f"❌ Lỗi {response.status_code}: {error_msg}")
            except Exception as e:
                message_placeholder.markdown(f"❌ Lỗi mạng: {str(e)}")
