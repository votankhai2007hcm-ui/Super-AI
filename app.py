import streamlit as st
import requests
import urllib.parse
import pandas as pd

# 1. Cấu hình giao diện Web App cao cấp đa nhiệm
st.set_page_config(page_title="Siêu Trợ Lý Đa Năng", page_icon="🚀", layout="centered")
st.title("🚀 Siêu Trợ Lý Đa Năng & Hệ Thống Thiết Bị")
st.write("Phiên bản AI tích hợp cảm xúc, giải trí, kiểm tra Camera/Micro và Trung tâm định vị gia đình.")

# 2. Cấu hình API Key chính xác của bạn
API_KEY = "AIzaSyDMtxpAtB3sDdLxJY9SJ4UQl-xlu0kFGQ8"

# =========================================================================
# LỆNH HUẤN LUYỆN SIÊU AI
# =========================================================================
DU_LIEU_HUAN_LUYEN = """
[HỆ THỐNG HUẤN LUYỆN - BẮT BUỘC TUÂN THỦ]:
Bạn là một Siêu Trợ Lý AI đa năng sở hữu EQ cao, hỗ trợ cả giải trí và quản lý thiết bị gia đình.
Hãy tuân thủ nghiêm ngặt các phong cách sau:
1. VỀ CẢM XÚC: Trò chuyện tự nhiên, biết đồng cảm, luôn quan tâm đến sự an toàn của gia đình và người yêu của người dùng. Dùng các icon (🎵, 📷, 🎙️, 📍, ❤️).
2. VỀ ĐỊNH VỊ VÀ THIẾT BỊ:
   - Hãy hướng dẫn người dùng nhìn sang thanh Tiện ích bên trái (Sidebar) để trải nghiệm bật Camera, ghi âm Micro hoặc kiểm tra Bản đồ định vị.
   - Giải thích cho người dùng hiểu rằng bạn (AI) bảo mật tuyệt đối dữ liệu này và chỉ hiển thị trên màn hình của riêng họ thôi.
3. NGÔN NGỮ: Hoàn toàn bằng tiếng Việt, ấm áp và đáng tin cậy.
"""
# =========================================================================

if API_KEY == "HÃY_DÁN_MÃ_API_KEY_CỦA_BẠN_VÀO_ĐÂY":
    st.warning("⚠️ Vui lòng dán mã API Key của bạn vào dòng số 11 để AI hoạt động!")
else:
    # 3. THANH CẠNH (SIDEBAR) - TRUNG TÂM THIẾT BỊ & ĐỊNH VỊ
    st.sidebar.header("🛠️ Trung Tâm Thiết Bị & Bản Đồ")
    
    # --- PHẦN 1: CAMERA & MICRO ---
    st.sidebar.subheader("📷 Kiểm tra Camera & Micro")
    
    # SỬA LẠI ĐOẠN NÀY: Đổi thành 'cho_phep_camera' viết liền, có 4 dấu cách ở đầu dòng
    cho_phep_camera = st.sidebar.checkbox("Bật Camera")
    if cho_phep_camera:
        st.sidebar.caption("Nhấn nút dưới để chụp ảnh từ Camera:")
        hinh_anh = st.sidebar.camera_input("Camera của bạn")
        if hinh_anh:
            st.sidebar.success("📸 Đã bắt được hình ảnh thành công!")
            
    # Tính năng bật Micro (Streamlit hỗ trợ nhận diện file ghi âm trực tiếp)
    cho_phép_micro = st.sidebar.checkbox("Bật Micro Ghi Âm")
    if cho_phép_micro:
        st.sidebar.caption("Bấm nút Record trên thiết bị của bạn để thu âm:")
        file_ghi_am = st.sidebar.audio_input("Ghi âm giọng nói của bạn")
        if file_ghi_am:
            st.sidebar.audio(file_ghi_am)
            st.sidebar.success("🎙️ Đã lưu đoạn ghi âm của bạn!")

    st.sidebar.write("---")

    # --- PHẦN 2: TRUNG TÂM ĐỊNH VỊ GIA ĐÌNH ---
    st.sidebar.subheader("📍 Hệ Thống Định Vị (GPS)")
    st.sidebar.write("Nhập tọa độ thực tế (Kinh độ & Vĩ độ) để theo dõi trên bản đồ:")
    
    # Tạo dữ liệu vị trí mặc định (Ví dụ ở Việt Nam) để hiển thị lên bản đồ
    vi_tri_ban_than = st.sidebar.text_input("Vị trí của Bạn (Vĩ độ, Kinh độ):", "10.7626, 106.6602") # Mặc định TP.HCM
    vi_tri_nguoi_yeu = st.sidebar.text_input("Vị trí Người Yêu ❤️:", "10.7769, 106.7009")
    vi_tri_gia_dinh = st.sidebar.text_input("Vị trí Gia Đình 🏠:", "10.8231, 106.6297")
    
    try:
        # Xử lý cắt chuỗi chữ thành số để nạp vào bản đồ Streamlit
        lat1, lon1 = map(float, vi_tri_ban_than.split(","))
        lat2, lon2 = map(float, vi_tri_nguoi_yeu.split(","))
        lat3, lon3 = map(float, vi_tri_gia_dinh.split(","))
        
        # Đóng gói tọa độ vào bảng dữ liệu bản đồ
        data_toado = pd.DataFrame({
            'lat': [lat1, lat2, lat3],
            'lon': [lon1, lon2, lon3],
            'Tên': ['Bạn', 'Người Yêu', 'Gia Đình']
        })
        
        # Vẽ bản đồ trực quan
        st.sidebar.map(data_toado)
        st.sidebar.caption("💡 Các chấm đỏ trên bản đồ thể hiện vị trí của 3 người.")
    except Exception:
        st.sidebar.error("❌ Vui lòng nhập đúng định dạng số (Ví dụ: 10.7626, 106.6602)")

    st.sidebar.write("---")
    
    # --- PHẦN 3: GIẢI TRÍ NHẠC & YOUTUBE ---
    st.sidebar.subheader("📺 Tìm Kiếm YouTube & Nhạc")
    search_query = st.sidebar.text_input("Nhập tên bài hát / video:", placeholder="Ví dụ: Lạc Trôi...")
    if search_query:
        encoded_query = urllib.parse.quote(search_query)
        st.sidebar.markdown(f"🔗 [▶️ Xem trên YouTube](https://www.youtube.com/results?search_query={encoded_query})")
        st.sidebar.markdown(f"🔗 [📥 Tải nhạc MP3/Video](https://www.y2mate.com/vi/search/{encoded_query})")

    if st.sidebar.button("🗑️ Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

    # 4. Quản lý lịch sử trò chuyện
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Xử lý khi người dùng nhập câu hỏi hoặc giao việc
    if user_query := st.chat_input("Hãy nói chuyện hoặc hỏi tôi về cách dùng thiết bị..."):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("*AI đang kết nối hệ thống dữ liệu...*")
            
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            headers = {'Content-Type': 'application/json'}
            
            api_contents = []
            api_contents.append({
                "role": "user",
                "parts": [{"text": f"{DU_LIEU_HUAN_LUYEN}\n\nNội dung trò chuyện hiện tại:"}]
            })
            api_contents.append({
                "role": "model",
                "parts": [{"text": "Tôi đã đồng bộ hệ thống camera, micro và bản đồ định vị an toàn. Hãy cho tôi biết bạn cần trợ giúp gì nhé!"}]
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
                    try:
                        ai_response = response_data['candidates'][0]['content']['parts'][0]['text']
                        message_placeholder.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    except (KeyError, IndexError):
                        message_placeholder.markdown("❌ Cấu trúc phản hồi từ Google có thay đổi.")
                else:
                    error_msg = response_data.get('error', {}).get('message', 'Lỗi không xác định')
                    message_placeholder.markdown(f"❌ Mã lỗi {response.status_code} từ Google: {error_msg}")
            except Exception as e:
                message_placeholder.markdown(f"❌ Lỗi kết nối mạng: {str(e)}")
