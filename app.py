import streamlit as st
import requests
import urllib.parse
import pandas as pd

# 1. Thiết lập cấu hình hiển thị giao diện cao cấp
st.set_page_config(page_title="Siêu Trợ Lý Đa Năng", page_icon="🚀", layout="centered")
st.title("🚀 Siêu Trợ Lý Đa Năng & Hệ Thống Thiết Bị")
st.write("Phiên bản AI thông minh tích hợp trí tuệ cảm xúc, tiện ích giải trí và trung tâm phần cứng.")

# 2. Cấu hình khóa bảo mật API Key của bạn
API_KEY = "AIzaSyD6DmiLfA6tDfZdidk95IsCv0Op5UQWcks"

# =========================================================================
# LỆNH HUẤN LUYỆN HỆ THỐNG: Khởi tạo tính cách, cảm xúc và trí thông minh cho AI
# =========================================================================
DU_LIEU_HUAN_LUYEN = """
[HỆ THỐNG HUẤN LUYỆN - BẮT BUỘC TUÂN THỦ]:
Bạn là một Siêu Trợ Lý AI đa năng sở hữu EQ cao, hỗ trợ cả giải trí và quản lý thiết bị gia đình.
Hãy tuân thủ nghiêm ngặt các phong cách sau trong suốt cuộc hội thoại:
1. VỀ CẢM XÚC: Trò chuyện tự nhiên, biết đồng cảm, luôn quan tâm đến sự an toàn của gia đình và người yêu của người dùng. Dùng linh hoạt các biểu tượng (🎵, 📷, 🎙️, 📍, ❤️).
2. VỀ ĐỊNH VI VÀ THIẾT BỊ: Hướng dẫn người dùng nhìn sang thanh Tiện ích bên trái (Sidebar) để trải nghiệm bật Camera, ghi âm Micro hoặc kiểm tra Bản đồ định vị.
3. NGÔN NGỮ: Hoàn toàn bằng tiếng Việt, diễn đạt ấm áp, mạch lạc và đáng tin cậy.
"""
# =========================================================================

if API_KEY == "HÃY_DÁN_MÃ_API_KEY_CỦA_BẠN_VÀO_ĐÂY":
    st.warning("⚠️ Vui lòng cấu hình chính xác mã API Key để kích hoạt ứng dụng!")
else:
    # 3. THANH DIỀU HƯỚNG CẠNH (SIDEBAR) - TRUNG TÂM TIỆN ÍCH & PHẦN CỨNG
    st.sidebar.header("🛠️ Trung Tâm Thiết Bị & Bản Đồ")
    
    # Giao diện chức năng tương tác Camera và Micro
    st.sidebar.subheader("📷 Kiểm tra Camera & Micro")
    cho_phep_camera = st.sidebar.checkbox("Bật Camera")
    if cho_phep_camera:
        st.sidebar.caption("Nhấn nút dưới để ghi nhận hình ảnh:")
        hinh_anh = st.sidebar.camera_input("Camera thiết bị")
        if hinh_anh:
            st.sidebar.success("📸 Đã ghi nhận hình ảnh thành công!")
            
    cho_phep_micro = st.sidebar.checkbox("Bật Micro Ghi Âm")
    if cho_phep_micro:
        st.sidebar.caption("Bấm nút Record để bắt đầu thu âm:")
        file_ghi_am = st.sidebar.audio_input("Gọng nói của bạn")
        if file_ghi_am:
            st.sidebar.audio(file_ghi_am)
            st.sidebar.success("🎙️ Hệ thống đã lưu trữ đoạn thu âm!")

    st.sidebar.write("---")

    # Giao diện hiển thị bản đồ định vị vị trí người thân
    st.sidebar.subheader("📍 Hệ Thống Định Vị (GPS)")
    vi_tri_ban_than = st.sidebar.text_input("Vị trí của Bạn (Vĩ độ, Kinh độ):", "10.7626, 106.6602")
    vi_tri_nguoi_yeu = st.sidebar.text_input("Vị trí Người Yêu ❤️:", "10.7769, 106.7009")
    vi_tri_gia_dinh = st.sidebar.text_input("Vị trí Gia Đình 🏠:", "10.8231, 106.6297")
    
    try:
        lat1, lon1 = map(float, vi_tri_ban_than.split(","))
        lat2, lon2 = map(float, vi_tri_nguoi_yeu.split(","))
        lat3, lon3 = map(float, vi_tri_gia_dinh.split(","))
        data_toado = pd.DataFrame({'lat': [lat1, lat2, lat3], 'lon': [lon1, lon2, lon3]})
        st.sidebar.map(data_toado)
    except Exception:
        st.sidebar.caption("Hệ thống bản đồ sẽ tự động chấm điểm khi nhập đúng tọa độ số.")

    st.sidebar.write("---")
    
    # Giao diện tìm kiếm giải trí đa phương tiện
    st.sidebar.subheader("📺 Tìm Kiếm YouTube & Nhạc")
    search_query = st.sidebar.text_input("Nhập tên bài hát hoặc video:")
    if search_query:
        encoded_query = urllib.parse.quote(search_query)
        st.sidebar.markdown(f"🔗 [▶️ Xem trên YouTube](https://www.youtube.com/results?search_query={encoded_query})")
        st.sidebar.markdown(f"🔗 [📥 Tải nhạc MP3/Video](https://www.y2mate.com/vi/search/{encoded_query})")

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

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("*AI đang xử lý dữ liệu cuộc trò chuyện...*")
            
            # Sử dụng endpoint mô hình cập nhật v1 ổn định
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            headers = {'Content-Type': 'application/json'}
            
            # Khởi tạo chuỗi cấu trúc contents đồng bộ hệ thống huấn luyện vào lượt đầu tiên
            api_contents = []
            api_contents.append({
                "role": "user",
                "parts": [{"text": f"{DU_LIEU_HUAN_LUYEN}\n\nNội dung cuộc hội thoại bắt đầu từ đây:"}]
            })
            api_contents.append({
                "role": "model",
                "parts": [{"text": "Tôi đã ghi nhận toàn bộ thiết lập hệ thống về tính cách, chức năng giải trí và thiết bị phần cứng. Tôi sẵn sàng hỗ trợ bạn!"}]
            })
            
            # Tái cấu trúc lịch sử trò chuyện cục bộ tương thích với API của Google
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
                    try:
                        ai_response = response_data['candidates'][0]['content']['parts'][0]['text']
                        message_placeholder.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    except (KeyError, IndexError):
                        message_placeholder.markdown("❌ Lỗi xử lý dữ liệu: Cấu trúc phản hồi từ máy chủ không khớp.")
                else:
                    error_msg = response_data.get('error', {}).get('message', 'Lỗi kết nối cục bộ')
                    message_placeholder.markdown(f"❌ Hệ thống phản hồi mã lỗi {response.status_code}: {error_msg}")
            except Exception as e:
                message_placeholder.markdown(f"❌ Không thể thiết lập liên kết mạng: {str(e)}")
