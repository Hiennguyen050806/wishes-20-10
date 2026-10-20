import streamlit as st
import random
import textwrap
import database

# Khởi tạo CSDL SQLite nếu chưa có
database.init_db()

# ============================================================
# CSS & ANIMATIONS
# ============================================================
def inject_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&family=Quicksand:wght@400;600;700&display=swap');

    /* ===== NỀN GRADIENT TỐI ĐẸP ===== */
    .stApp {
        background: linear-gradient(160deg,
            #1a0533 0%,
            #3d0b5e 20%,
            #6a1b9a 40%,
            #ad1457 65%,
            #e91e63 85%,
            #ff6090 100%
        );
        font-family: 'Quicksand', sans-serif;
        min-height: 100vh;
    }

    /* ===== TIÊU ĐỀ VÀNG ÁNH ===== */
    .main-title {
        font-family: 'Dancing Script', cursive;
        font-size: 3.6rem;
        background: linear-gradient(135deg, #fff9c4, #ffd54f, #fff, #ffd54f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        filter: drop-shadow(0 0 18px rgba(255,215,0,0.45));
        margin-bottom: 0.3rem;
        animation: fadeInDown 1s ease-out;
    }

    .subtitle {
        font-family: 'Quicksand', sans-serif;
        font-size: 1.15rem;
        color: rgba(255,255,255,0.85);
        text-align: center;
        margin-bottom: 1.5rem;
        animation: fadeInUp 1s ease-out 0.3s both;
        letter-spacing: 0.4px;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-28px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(28px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ===== HỘP MẬT KHẨU GLASSMORPHISM ===== */
    .password-box {
        background: rgba(255,255,255,0.11);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 26px;
        padding: 2.2rem 2rem;
        max-width: 480px;
        margin: 1rem auto;
        box-shadow: 0 16px 48px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.18);
        backdrop-filter: blur(22px);
        text-align: center;
    }

    .lock-icon {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        animation: bounce 2s infinite;
        display: block;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0) rotate(-5deg); }
        50%       { transform: translateY(-10px) rotate(5deg); }
    }

    /* ===== HIỆU ỨNG TRÁI TIM ĐẬP (BEATING HEART SVG + KEYFRAMES) ===== */
    .beating-heart-box {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1.2rem auto;
    }

    /* Vòng hào quang lan tỏa nhịp tim (Pulse Wave) */
    .heart-pulse-wave {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255, 23, 68, 0.45) 0%, rgba(233, 30, 99, 0.2) 50%, rgba(255, 64, 129, 0) 75%);
        animation: pulseWave 1.35s ease-out infinite;
        pointer-events: none;
    }

    .heart-pulse-wave.delay {
        animation-delay: 0.45s;
    }

    @keyframes pulseWave {
        0% {
            transform: scale(0.65);
            opacity: 0.95;
        }
        50% {
            opacity: 0.6;
        }
        100% {
            transform: scale(2.4);
            opacity: 0;
        }
    }

    /* SVG Trái tim với hiệu ứng đập sinh học (lub-dub) */
    .pulsing-heart-svg {
        animation: humanHeartBeat 1.35s ease-in-out infinite;
        filter: drop-shadow(0 0 16px rgba(255, 23, 68, 0.9)) drop-shadow(0 0 35px rgba(233, 30, 99, 0.6));
        cursor: pointer;
        transition: transform 0.25s ease;
        z-index: 2;
    }

    .pulsing-heart-svg:hover {
        animation-duration: 0.75s; /* Rê chuột vào tim đập nhanh hơn */
        transform: scale(1.1);
    }

    /* Nhịp đập chuẩn: Thình (nhanh) - Thịch (mạnh) - Nghỉ */
    @keyframes humanHeartBeat {
        0%   { transform: scale(1); }
        14%  { transform: scale(1.28) rotate(-2deg); }
        28%  { transform: scale(1.04) rotate(0deg); }
        42%  { transform: scale(1.36) rotate(2deg); }
        70%  { transform: scale(1) rotate(0deg); }
        100% { transform: scale(1) rotate(0deg); }
    }

    /* ===== CARD TRÒ CHƠI ===== */
    .game-card {
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 20px;
        padding: 1.6rem 1.4rem;
        margin: 1.2rem 0 0.4rem 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.22);
        backdrop-filter: blur(12px);
        border-left: 5px solid rgba(255,213,79,0.65);
    }

    .game-title {
        font-family: 'Dancing Script', cursive;
        font-size: 1.9rem;
        color: #ffd54f;
        margin-bottom: 0.3rem;
        text-shadow: 0 0 10px rgba(255,213,79,0.35);
    }

    .game-desc {
        color: rgba(255,255,255,0.78);
        font-size: 0.98rem;
        font-style: italic;
    }

    /* ===== PROGRESS ===== */
    .progress-text {
        text-align: center;
        font-size: 1.1rem;
        color: #ffd54f;
        font-weight: 700;
        margin: 0.6rem 0;
        text-shadow: 0 0 8px rgba(255,213,79,0.3);
    }

    /* ===== MESSAGES ===== */
    .success-msg {
        background: linear-gradient(135deg, rgba(27,94,32,0.75), rgba(46,125,50,0.75));
        border: 1px solid rgba(129,199,132,0.45);
        border-radius: 14px;
        padding: 1rem 1.4rem;
        text-align: center;
        color: #e8f5e9;
        font-weight: 700;
        font-size: 1.05rem;
        margin: 0.6rem 0;
        animation: fadeInUp 0.5s ease-out;
        backdrop-filter: blur(5px);
    }

    .fail-msg {
        background: linear-gradient(135deg, rgba(183,28,28,0.65), rgba(198,40,40,0.65));
        border: 1px solid rgba(239,154,154,0.4);
        border-radius: 14px;
        padding: 1rem 1.4rem;
        text-align: center;
        color: #ffebee;
        font-weight: 700;
        font-size: 1.05rem;
        margin: 0.6rem 0;
        backdrop-filter: blur(5px);
    }

    /* ===== TEXT TRẮNG CHO NỀN TỐI ===== */
    .stMarkdown p, .stMarkdown li,
    label, .stTextInput label,
    .stRadio label, .stNumberInput label,
    .stTextArea label, .stSelectbox label {
        color: rgba(255,255,255,0.92) !important;
    }

    .stRadio > div > label > div > p {
        color: rgba(255,255,255,0.9) !important;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        background: rgba(255,255,255,0.13) !important;
        border: 1px solid rgba(255,255,255,0.28) !important;
        border-radius: 12px !important;
        color: white !important;
        backdrop-filter: blur(5px);
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255,255,255,0.45) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #ffd54f !important;
        box-shadow: 0 0 0 2px rgba(255,213,79,0.22) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #e91e63, #9c27b0) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        padding: 0.65rem 1.4rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(233,30,99,0.38) !important;
        letter-spacing: 0.3px !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(233,30,99,0.5) !important;
        background: linear-gradient(135deg, #f06292, #ba68c8) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ffd54f, #ff6090) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.08);
        padding: 6px;
        border-radius: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        color: white !important;
        border-radius: 10px;
        padding: 8px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(233, 30, 99, 0.6) !important;
        color: #ffd54f !important;
        font-weight: bold;
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.13) !important; }

    /* Caption */
    .stCaption { color: rgba(255,255,255,0.6) !important; }

    /* ===== TRANG THƯỞNG ===== */
    .congrats-text {
        font-family: 'Dancing Script', cursive;
        font-size: 2.8rem;
        background: linear-gradient(135deg, #ffd54f, #fff9c4, #ffd54f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        filter: drop-shadow(0 0 14px rgba(255,215,0,0.5));
        animation: fadeInDown 1s ease-out;
        margin: 0.8rem 0 0.3rem 0;
    }

    .congrats-sub {
        font-family: 'Quicksand', sans-serif;
        font-size: 1.1rem;
        color: rgba(255,255,255,0.88);
        text-align: center;
        animation: fadeInUp 1s ease-out 0.5s both;
        margin-bottom: 0.4rem;
    }

    .flower-display {
        font-size: 6.5rem;
        text-align: center;
        display: block;
        animation: flowerBloom 2s ease-out, flowerSway 3s ease-in-out infinite 2s;
        filter: drop-shadow(0 0 18px rgba(233,30,99,0.45));
        margin: 0.4rem 0;
    }

    @keyframes flowerBloom {
        0%   { transform: scale(0) rotate(-180deg); opacity: 0; }
        60%  { transform: scale(1.2) rotate(10deg); opacity: 1; }
        100% { transform: scale(1) rotate(0deg); opacity: 1; }
    }

    @keyframes flowerSway {
        0%, 100% { transform: rotate(-3deg); }
        50%       { transform: rotate(3deg); }
    }

    /* Lá thư phần thưởng */
    .letter-paper {
        background: linear-gradient(160deg, #fffde7 0%, #fff8e1 55%, #fffbf0 100%);
        border-radius: 18px;
        padding: 2.5rem 2rem;
        box-shadow: 0 14px 44px rgba(0,0,0,0.28), 0 2px 0 rgba(255,213,79,0.28);
        border: 2px solid rgba(255,213,79,0.38);
        margin: 1.5rem 0;
        position: relative;
        animation: letterOpen 1.5s ease-out 0.4s both;
    }

    .letter-paper::before {
        content: '💌';
        position: absolute;
        top: -22px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 2.8rem;
    }

    @keyframes letterOpen {
        0%   { transform: rotateX(-90deg) scale(0.5); opacity: 0; }
        100% { transform: rotateX(0deg) scale(1); opacity: 1; }
    }

    .letter-header {
        font-family: 'Dancing Script', cursive;
        font-size: 1.85rem;
        color: #c2185b;
        text-align: center;
        margin-bottom: 1.3rem;
        border-bottom: 2px dashed #f48fb1;
        padding-bottom: 0.9rem;
    }

    .letter-body {
        font-family: 'Dancing Script', cursive;
        font-size: 1.35rem;
        color: #4a2040;
        line-height: 2.1;
    }

    .letter-footer {
        text-align: right;
        margin-top: 1.4rem;
        font-family: 'Dancing Script', cursive;
        font-size: 1.18rem;
        color: #e91e63;
        border-top: 1px dashed #f48fb1;
        padding-top: 0.9rem;
    }

    .floating-flowers-row {
        text-align: center;
        font-size: 2rem;
        margin: 1rem 0;
        letter-spacing: 5px;
        animation: fadeInUp 1s ease-out 1s both;
    }

    /* Petals & hearts nền */
    .petal {
        position: fixed;
        pointer-events: none;
        z-index: 999;
        animation: petalFall linear infinite;
    }

    @keyframes petalFall {
        0%   { transform: translateY(-5vh) rotate(0deg) translateX(0); opacity: 1; }
        25%  { transform: translateY(25vh) rotate(90deg) translateX(28px); }
        50%  { transform: translateY(55vh) rotate(180deg) translateX(-18px); }
        75%  { transform: translateY(80vh) rotate(270deg) translateX(22px); }
        100% { transform: translateY(110vh) rotate(360deg) translateX(-8px); opacity: 0; }
    }

    .heart-float {
        position: fixed;
        pointer-events: none;
        z-index: 998;
        animation: floatUp linear infinite;
    }

    @keyframes floatUp {
        0%   { transform: translateY(110vh); opacity: 0; }
        10%  { opacity: 0.65; }
        90%  { opacity: 0.55; }
        100% { transform: translateY(-10vh); opacity: 0; }
    }

    /* ===== ẨN UI MẶC ĐỊNH CỦA STREAMLIT ===== */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# HÀM TẠO TRÁI TIM ĐẬP (HEARTBEAT SVG COMPONENT)
# ============================================================
def render_beating_heart(size=110):
    """
    Sinh mã HTML + SVG trái tim với hiệu ứng đập sinh học và sóng lan tỏa.
    - SVG gradient đỏ thắm đến hồng cánh sen.
    - Điểm sáng 3D bóng bẩy.
    - Hiệu ứng nhịp tim 'lub-dub' chân thực.
    - Sóng pulse tỏa ra xung quanh.
    """
    return f"""
    <div class="beating-heart-box" style="width:{size+30}px;height:{size+30}px;">
        <div class="heart-pulse-wave" style="width:{size-15}px;height:{size-15}px;"></div>
        <div class="heart-pulse-wave delay" style="width:{size-15}px;height:{size-15}px;"></div>
        <svg class="pulsing-heart-svg" style="width:{size}px;height:{size}px;" viewBox="0 0 24 24" title="Trái tim đập yêu thương">
            <defs>
                <linearGradient id="heartGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#ff1744" />
                    <stop offset="40%" stop-color="#f50057" />
                    <stop offset="80%" stop-color="#c2185b" />
                    <stop offset="100%" stop-color="#880e4f" />
                </linearGradient>
                <radialGradient id="heartSpecular" cx="35%" cy="30%" r="40%">
                    <stop offset="0%" stop-color="rgba(255, 255, 255, 0.9)" />
                    <stop offset="60%" stop-color="rgba(255, 255, 255, 0.25)" />
                    <stop offset="100%" stop-color="rgba(255, 255, 255, 0)" />
                </radialGradient>
            </defs>
            <!-- Đường cong trái tim sắc nét và cân đối tuyệt đối -->
            <path fill="url(#heartGradient)" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
            <!-- Vệt sáng 3D bóng phản chiếu -->
            <ellipse cx="7.5" cy="7.5" rx="3.5" ry="2.2" fill="url(#heartSpecular)" transform="rotate(-35 7.5 7.5)"/>
        </svg>
    </div>
    """


# ============================================================
# TRANG THƯỞNG: LẤY THƯ TỪ CƠ SỞ DỮ LIỆU BACKEND
# ============================================================
def render_reward_page(letter_data):
    """Trang thưởng: hoa, trái tim đập rực rỡ, và lá thư lấy trực tiếp từ database backend (SQLite)"""

    # Petals rơi
    petals_html = ""
    petal_emojis = ["🌸", "🌺", "🌷", "🏵️", "💮", "🌼"]
    for i in range(18):
        emoji = random.choice(petal_emojis)
        left = random.randint(0, 100)
        duration = random.uniform(8, 16)
        delay = random.uniform(0, 10)
        size = random.uniform(1.2, 2.2)
        petals_html += (
            f'<span class="petal" '
            f'style="left:{left}%;animation-duration:{duration:.1f}s;'
            f'animation-delay:{delay:.1f}s;font-size:{size:.1f}rem;">'
            f'{emoji}</span>'
        )

    # Trái tim bay
    hearts_html = ""
    heart_emojis = ["❤️", "💖", "💕", "💗", "💓", "💘", "🩷"]
    for i in range(20):
        emoji = random.choice(heart_emojis)
        left = random.randint(0, 100)
        duration = random.uniform(7, 14)
        delay = random.uniform(0, 8)
        size = random.uniform(1.0, 2.4)
        hearts_html += (
            f'<span class="heart-float" '
            f'style="left:{left}%;animation-duration:{duration:.1f}s;'
            f'animation-delay:{delay:.1f}s;font-size:{size:.1f}rem;">'
            f'{emoji}</span>'
        )

    st.markdown(petals_html + hearts_html, unsafe_allow_html=True)

    # Tiêu đề chúc mừng
    st.markdown(
        '<div class="congrats-text">🎀 Chúc Mừng Ngày Phụ Nữ Việt Nam! 🎀</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="congrats-sub">✨ 20/10 – Ngày tôn vinh những người phụ nữ tuyệt vời ✨</div>',
        unsafe_allow_html=True,
    )

    # Trái tim đập rực rỡ
    st.markdown(render_beating_heart(size=125), unsafe_allow_html=True)

    recipient_name = letter_data.get("recipient_name", "Bạn")
    flower_icon = letter_data.get("flower_icon", "🌹")

    # Bông hoa tặng riêng
    st.markdown(
        f'<div class="congrats-sub" style="font-size:1.3rem;margin:0.2rem 0;">'
        f'Tặng <strong style="color:#ffd54f;">{recipient_name}</strong> bông hoa này nhé! 🌺</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<span class="flower-display">{flower_icon}</span>', unsafe_allow_html=True)

    # Hàng hoa trang trí
    st.markdown(
        '<div class="floating-flowers-row">🌸 🌺 🌹 🌷 🌻 🌼 💐 🌸 🌺 🌹</div>',
        unsafe_allow_html=True,
    )

    # Dữ liệu lá thư từ SQLite backend
    user_letter = letter_data.get("content", "").strip()
    letter_title = letter_data.get("title", "💌 Lá Thư Yêu Thương 💌")
    sender_name = letter_data.get("sender_name", "Người gửi")
    date_str = letter_data.get("date_str", "20/10/2026")

    # Escape HTML rồi chuyển \n → <br>
    safe_letter = (
        user_letter
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br>")
    )

    st.markdown(
        textwrap.dedent(f"""
        <div class="letter-paper">
            <div class="letter-header">{letter_title}</div>
            <div class="letter-body">{safe_letter}</div>
            <div class="letter-footer">
                Với tất cả yêu thương 💕<br>
                <strong>{sender_name}</strong> &bull; {date_str}
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )


# ============================================================
# TRANG QUẢN TRỊ BACKEND & SOẠN THƯ (CSDL SQLITE)
# ============================================================
def render_admin_backend_page():
    """Trang Quản trị Backend: Cho phép soạn thư, sửa thư và lưu trực tiếp vào SQLite (wishes.db)"""
    st.markdown('<div class="main-title">⚙️ Quản Trị Backend & CSDL 💌</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Soạn và tùy chỉnh các bức thư lưu trong cơ sở dữ liệu SQLite (wishes.db)</div>', unsafe_allow_html=True)

    # Nút chuyển tab
    tab_list, tab_edit, tab_preview = st.tabs(["📋 Danh Sách Thư CSDL", "✍️ Soạn / Sửa Thư", "👁️ Xem Thử (Preview)"])
    
    all_letters = database.get_all_letters()
    
    with tab_list:
        st.markdown(f"### 📦 Hiện có **{len(all_letters)}** bức thư trong CSDL `wishes.db`:")
        for idx, l in enumerate(all_letters):
            with st.expander(f"🔑 Mật khẩu: **{l['passcode']}** — Gửi đến: **{l['recipient_name']}** ({l['flower_icon']})"):
                st.markdown(f"**Tiêu đề:** {l['title']}")
                st.markdown(f"**Người gửi:** `{l['sender_name']}` | **Ngày:** `{l['date_str']}`")
                st.info(l['content'])
        
        st.caption("💡 Khi người nhận nhập mật khẩu tương ứng và vượt qua trò chơi, thư sẽ tự động hiển thị từ CSDL.")

    with tab_edit:
        st.markdown("### ✍️ Soạn nội dung thư mới hoặc chỉnh sửa thư trong CSDL:")
        
        options = ["Thêm thư mới (+)"] + [f"{l['passcode']} (cho {l['recipient_name']})" for l in all_letters]
        selected_option = st.selectbox("Chọn bức thư để chỉnh sửa hoặc tạo mới:", options)
        
        if selected_option == "Thêm thư mới (+)":
            edit_passcode = ""
            edit_recipient = ""
            edit_title = "💌 Lá Thư Yêu Thương 20/10 💌"
            edit_content = "Nhân ngày Phụ nữ Việt Nam 20/10, chúc bạn luôn vui vẻ, xinh đẹp và ngập tràn hạnh phúc! 💕"
            edit_sender = "Người thương"
            edit_date = "20/10/2026"
            edit_flower = "🌹"
        else:
            sel_passcode = selected_option.split(" (")[0]
            existing = database.get_letter_by_passcode(sel_passcode)
            edit_passcode = existing["passcode"]
            edit_recipient = existing["recipient_name"]
            edit_title = existing["title"]
            edit_content = existing["content"]
            edit_sender = existing["sender_name"]
            edit_date = existing["date_str"]
            edit_flower = existing["flower_icon"]

        with st.form("edit_letter_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                form_passcode = st.text_input("🔑 Mật khẩu mở quà (viết thường, vd: mẹ yêu, bạn gái):", value=edit_passcode)
                form_recipient = st.text_input("👤 Tên người nhận (vd: Mẹ Yêu, Bé Yêu):", value=edit_recipient)
                flower_list = ["🌹", "🌸", "🌺", "🌷", "🌻", "🌼", "💐"]
                form_flower = st.selectbox(
                    "🌺 Biểu tượng hoa tặng:",
                    flower_list,
                    index=flower_list.index(edit_flower) if edit_flower in flower_list else 0
                )
            with col_b:
                form_title = st.text_input("🎀 Tiêu đề lá thư:", value=edit_title)
                form_sender = st.text_input("✍️ Tên người gửi (vd: Con trai, Anh của em):", value=edit_sender)
                form_date = st.text_input("📅 Ngày hiển thị:", value=edit_date)
            
            form_content = st.text_area("📝 Nội dung lá thư (lưu trong CSDL):", value=edit_content, height=260)
            
            submit_save = st.form_submit_button("💾 LƯU VÀO CƠ SỞ DỮ LIỆU (SQLITE)", use_container_width=True)
            if submit_save:
                if not form_passcode.strip() or not form_recipient.strip():
                    st.error("⚠️ Vui lòng điền mật khẩu và tên người nhận!")
                else:
                    database.save_letter(
                        passcode=form_passcode,
                        recipient_name=form_recipient,
                        title=form_title,
                        content=form_content,
                        sender_name=form_sender,
                        date_str=form_date,
                        flower_icon=form_flower,
                    )
                    st.success(f"🎉 Đã lưu thành công bức thư cho [{form_recipient}] với mật khẩu [{form_passcode}] vào SQLite!")
                    st.rerun()

        if selected_option != "Thêm thư mới (+)":
            st.divider()
            if st.button(f"🗑️ Xóa bức thư mật khẩu [{edit_passcode}] khỏi CSDL", type="secondary"):
                database.delete_letter(edit_passcode)
                st.warning(f"Đã xóa bức thư có mật khẩu [{edit_passcode}]!")
                st.rerun()

    with tab_preview:
        st.markdown("### 👁️ Xem trước giao diện người nhận:")
        if all_letters:
            preview_passcode = st.selectbox("Chọn thư muốn xem trước:", [l['passcode'] for l in all_letters], key="preview_sel")
            preview_letter = database.get_letter_by_passcode(preview_passcode)
            if preview_letter:
                render_reward_page(preview_letter)
        else:
            st.info("Chưa có bức thư nào trong CSDL.")

    st.markdown("---")
    if st.button("🚪 Đăng xuất khỏi Chế độ Quản trị Backend", use_container_width=True):
        st.session_state.is_admin = False
        st.session_state.authenticated = False
        st.rerun()


# ============================================================
# TRÒ CHƠI 1: Trắc nghiệm
# ============================================================
def game_1_quiz():
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown('<div class="game-title">🌸 Trò Chơi 1: Trắc Nghiệm Vui</div>', unsafe_allow_html=True)
    st.markdown('<div class="game-desc">Trả lời đúng 3/3 câu hỏi về ngày Phụ nữ Việt Nam!</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    questions = [
        {
            "q": "Ngày Phụ nữ Việt Nam 20/10 kỷ niệm sự kiện nào?",
            "options": [
                "Ngày thành lập Hội Liên hiệp Phụ nữ Việt Nam",
                "Ngày sinh của Bà Trưng Trắc",
                "Ngày Quốc tế Phụ nữ",
                "Ngày thành lập nước",
            ],
            "answer": 0,
        },
        {
            "q": "Hội Liên hiệp Phụ nữ Việt Nam được thành lập năm nào?",
            "options": ["1925", "1930", "1945", "1950"],
            "answer": 1,
        },
        {
            "q": "Loài hoa nào thường được tặng nhất vào ngày 20/10?",
            "options": ["Hoa lan", "Hoa hướng dương", "Hoa hồng", "Hoa cúc"],
            "answer": 2,
        },
    ]

    score = 0
    answered_all = True

    for i, q in enumerate(questions):
        st.markdown(f"**Câu {i+1}:** {q['q']}")
        choice = st.radio(
            "Chọn đáp án:",
            q["options"],
            key=f"quiz_q{i}",
            index=None,
            label_visibility="collapsed",
        )
        if choice is None:
            answered_all = False
        elif q["options"].index(choice) == q["answer"]:
            score += 1
        st.divider()

    if st.button("✅ Nộp bài", key="submit_quiz", use_container_width=True):
        if not answered_all:
            st.warning("Hãy trả lời hết tất cả các câu nhé! 😊")
        elif score == 3:
            st.markdown('<div class="success-msg">🎉 Xuất sắc! Bạn trả lời đúng hết! 🌟</div>', unsafe_allow_html=True)
            st.session_state.game1_done = True
            st.rerun()
        else:
            st.markdown(f'<div class="fail-msg">😅 Bạn đúng {score}/3. Thử lại nha!</div>', unsafe_allow_html=True)


# ============================================================
# TRÒ CHƠI 2: Chọn nghĩa emoji
# ============================================================
def game_2_emoji_meaning():
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown('<div class="game-title">🎯 Trò Chơi 2: Emoji Nói Gì?</div>', unsafe_allow_html=True)
    st.markdown('<div class="game-desc">Chọn ý nghĩa đúng cho mỗi emoji! Chọn sai không sao, thử lại nhé 😊</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    puzzles = [
        {
            "emoji": "💐",
            "question": "Emoji này tượng trưng cho điều gì trong ngày 20/10?",
            "options": ["Bó hoa tặng quà 🌺", "Bữa ăn ngon 🍜", "Chuyến du lịch ✈️", "Trận bóng đá ⚽"],
            "answer": 0,
        },
        {
            "emoji": "🥰",
            "question": "Emoji này thể hiện cảm xúc gì?",
            "options": ["Tức giận 😠", "Yêu thương, hạnh phúc 💕", "Buồn bã 😢", "Ngạc nhiên 😲"],
            "answer": 1,
        },
        {
            "emoji": "🌹",
            "question": "Hoa hồng đỏ thường tượng trưng cho điều gì?",
            "options": ["Sức khỏe 💪", "Tiền bạc 💰", "Tình yêu ❤️", "Sự thành công 🏆"],
            "answer": 2,
        },
        {
            "emoji": "👸",
            "question": "Emoji này đại diện cho ai?",
            "options": ["Hoàng tử 🤴", "Công chúa / Người phụ nữ tuyệt vời 👑", "Nhà khoa học 🔬", "Ca sĩ 🎤"],
            "answer": 1,
        },
    ]

    if "game2_answers" not in st.session_state:
        st.session_state.game2_answers = [None] * len(puzzles)

    for i, p in enumerate(puzzles):
        st.markdown(f"**Câu {i+1}:** {p['emoji']}  _{p['question']}_")
        saved_idx = st.session_state.game2_answers[i]
        choice = st.radio(
            "Chọn:",
            p["options"],
            key=f"g2_q{i}",
            index=saved_idx,
            label_visibility="collapsed",
        )
        if choice is not None:
            idx = p["options"].index(choice)
            st.session_state.game2_answers[i] = idx
            if idx == p["answer"]:
                st.markdown("✅ **Đúng rồi!**")
            else:
                st.markdown("❌ Chưa đúng, thử lại!")
        st.divider()

    if st.button("✅ Kiểm tra kết quả", key="check_game2", use_container_width=True):
        correct_count = sum(
            1 for i, p in enumerate(puzzles)
            if st.session_state.game2_answers[i] == p["answer"]
        )
        if correct_count == len(puzzles):
            st.markdown('<div class="success-msg">🎊 Tuyệt vời! Bạn trả lời đúng hết! 🌟</div>', unsafe_allow_html=True)
            st.session_state.game2_done = True
            st.rerun()
        else:
            st.markdown(
                f'<div class="fail-msg">😅 Bạn đúng {correct_count}/{len(puzzles)}. '
                f'Xem lại câu chưa đúng rồi thử lại nhé!</div>',
                unsafe_allow_html=True,
            )


# ============================================================
# TRÒ CHƠI 3: Đếm hoa
# ============================================================
def game_3_catch_flowers():
    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.markdown('<div class="game-title">🌺 Trò Chơi 3: Đếm Hoa Nào!</div>', unsafe_allow_html=True)
    st.markdown('<div class="game-desc">Đếm số bông hoa 🌹 (hồng đỏ) trong hình bên dưới nhé!</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if "flower_count" not in st.session_state:
        st.session_state.flower_count = random.randint(5, 10)
        decoys = ["🌸", "🌼", "🌻", "🌷", "💐", "🏵️"]
        extra = random.randint(3, 6)
        items = ["🌹"] * st.session_state.flower_count
        for _ in range(extra):
            items.append(random.choice(decoys))
        random.shuffle(items)
        st.session_state.flower_display = items

    display = " ".join(st.session_state.flower_display)
    st.markdown(
        f'<div style="background:rgba(255,255,255,0.13);border:1px solid rgba(255,255,255,0.25);'
        f'border-radius:18px;padding:1.5rem;text-align:center;font-size:2.8rem;'
        f'line-height:2;letter-spacing:10px;margin:1rem 0;backdrop-filter:blur(5px);">'
        f'{display}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("**Có bao nhiêu bông hoa 🌹 (hồng đỏ)?**")
    guess = st.number_input(
        "Nhập số:",
        min_value=0,
        max_value=30,
        step=1,
        key="flower_guess",
    )

    if st.button("🌹 Kiểm tra", key="check_flowers", use_container_width=True):
        if int(guess) == st.session_state.flower_count:
            st.markdown('<div class="success-msg">🎉 Chính xác! Bạn thật tinh mắt! 🌟</div>', unsafe_allow_html=True)
            st.session_state.game3_done = True
            st.rerun()
        else:
            st.markdown(
                f'<div class="fail-msg">😅 Chưa đúng! Đếm kỹ lại nhé! '
                f'(Gợi ý: có từ 5 đến 10 bông 🌹)</div>',
                unsafe_allow_html=True,
            )


# ============================================================
# MAIN APPLICATION
# ============================================================
def main():
    st.set_page_config(
        page_title="🌹 Chúc Mừng 20/10 - Lời Chúc Yêu Thương 🌹",
        page_icon="💖",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    inject_global_css()

    # Khởi tạo session state
    defaults = {
        "authenticated": False,
        "is_admin": False,
        "current_letter": None,
        "game1_done": False,
        "game2_done": False,
        "game3_done": False,
        "show_reward": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ---- CHẾ ĐỘ QUẢN TRỊ BACKEND ----
    if st.session_state.is_admin:
        render_admin_backend_page()
        return

    # ---- TRANG ĐĂNG NHẬP / NHẬP MẬT KHẨU ----
    if not st.session_state.authenticated:
        st.markdown('<div class="main-title">🌹 Happy Women\'s Day 🌹</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Chào mừng ngày Phụ nữ Việt Nam 20/10 💕</div>', unsafe_allow_html=True)

        # Trái tim đập nhẹ nhàng chào đón người xem
        st.markdown(render_beating_heart(size=75), unsafe_allow_html=True)

        st.markdown('<div class="password-box">', unsafe_allow_html=True)
        st.markdown('<span class="lock-icon">🔐</span>', unsafe_allow_html=True)
        st.markdown("### Nhập mật khẩu để mở quà 🎁")

        password = st.text_input(
            "Mật khẩu:",
            type="password",
            placeholder="Nhập mật khẩu riêng của bạn...",
            key="password_input",
        )

        if st.button("🎀 Mở quà", use_container_width=True, key="login_btn"):
            pwd = password.strip().lower()
            if pwd in ["admin", "admin2010"]:
                st.session_state.is_admin = True
                st.session_state.authenticated = True
                st.rerun()
            else:
                letter = database.get_letter_by_passcode(pwd)
                if letter:
                    st.session_state.authenticated = True
                    st.session_state.current_letter = letter
                    st.session_state.is_admin = False
                    st.balloons()
                    st.rerun()
                else:
                    st.error("🔒 Mật khẩu không đúng! Hãy thử lại nhé~")

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align:center;color:rgba(255,255,255,0.6);font-size:0.85rem;margin-top:1.2rem;">'
            '💕 Mỗi người sẽ có một mật khẩu riêng để nhận quà bí mật 💕<br>'
            '<span style="font-size:0.75rem;opacity:0.6;">(Quản trị viên: nhập <code>admin</code> để soạn thư vào CSDL)</span></p>',
            unsafe_allow_html=True,
        )
        return

    letter = st.session_state.current_letter

    # ---- TRANG: PHẦN THƯỞNG (HIỂN THỊ THƯ TỪ DATABASE) ----
    if st.session_state.show_reward:
        render_reward_page(letter)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌸 Chơi lại thử thách", key="replay"):
                st.session_state.game1_done = False
                st.session_state.game2_done = False
                st.session_state.game3_done = False
                st.session_state.show_reward = False
                st.rerun()
        with col2:
            if st.button("🔄 Quay lại từ đầu", key="reset"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
        return

    # ---- TRANG: CÁC TRÒ CHƠI THỬ THÁCH ----
    st.markdown(
        f'<div class="main-title">Xin chào {letter["recipient_name"]}! 🌸</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="subtitle">Vượt qua 3 trò chơi nhỏ để nhận món quà và bức thư bí mật nhé! 🎁</div>',
        unsafe_allow_html=True,
    )

    done = sum([
        st.session_state.game1_done,
        st.session_state.game2_done,
        st.session_state.game3_done,
    ])
    st.progress(done / 3)
    st.markdown(
        f'<div class="progress-text">Tiến độ: {done}/3 trò chơi hoàn thành 🎯</div>',
        unsafe_allow_html=True,
    )

    # Khi hoàn thành hết 3 trò chơi → Mở thẳng quà và lá thư từ CSDL!
    if done == 3:
        st.markdown("---")
        st.markdown(
            f'<div style="text-align:center;font-size:1.35rem;color:#ffd54f;'
            'font-weight:700;margin:1.2rem 0;text-shadow:0 0 10px rgba(255,213,79,0.4);">'
            f'🎉🎊 Chúc mừng {letter["recipient_name"]} đã xuất sắc vượt qua tất cả! 🎊🎉<br>'
            '<span style="font-size:1.05rem;color:rgba(255,255,255,0.9);font-weight:400;">'
            'Món quà và lá thư bí mật dành riêng cho bạn đã sẵn sàng! 💌</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        if st.button("🎁 MỞ QUÀ & ĐỌC LÁ THƯ BÍ MẬT 💌", use_container_width=True, key="go_reward"):
            st.session_state.show_reward = True
            st.rerun()
        return

    # Hiển thị từng trò chơi theo thứ tự
    if not st.session_state.game1_done:
        game_1_quiz()
    else:
        st.success("✅ Trò chơi 1: Hoàn thành! 🌸")

    if st.session_state.game1_done and not st.session_state.game2_done:
        st.markdown("---")
        game_2_emoji_meaning()
    elif st.session_state.game2_done:
        st.success("✅ Trò chơi 2: Hoàn thành! 🎯")

    if st.session_state.game2_done and not st.session_state.game3_done:
        st.markdown("---")
        game_3_catch_flowers()
    elif st.session_state.game3_done:
        st.success("✅ Trò chơi 3: Hoàn thành! 🌺")


if __name__ == "__main__":
    main()
