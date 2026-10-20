"""
Module Quản lý Cơ sở dữ liệu SQLite cho Thiệp & Lời chúc 20/10
Lưu trữ toàn bộ nội dung thư ở backend trong file SQLite: wishes.db
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "wishes.db")


def get_db_connection():
    """Tạo kết nối tới SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Khởi tạo cấu trúc bảng và nạp dữ liệu mẫu ban đầu nếu chưa có."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS letters (
            passcode TEXT PRIMARY KEY,
            recipient_name TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            sender_name TEXT NOT NULL,
            date_str TEXT DEFAULT '20/10/2026',
            flower_icon TEXT DEFAULT '🌹'
        )
    """)

    # Kiểm tra xem đã có dữ liệu chưa, nếu chưa có thì nạp sẵn các bức thư backend mẫu
    cursor.execute("SELECT COUNT(*) FROM letters")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_letters = [
            (
                "mẹ yêu",
                "Mẹ Yêu",
                "💌 Kính Gửi Mẹ Yêu Dấu Của Con 💌",
                (
                    "Mẹ yêu kính mến của con,\n\n"
                    "Nhân ngày Phụ nữ Việt Nam 20/10, con muốn gửi đến Mẹ tất cả lòng biết ơn và sự kính yêu sâu sắc nhất từ tận đáy lòng.\n\n"
                    "Cảm ơn Mẹ đã luôn là điểm tựa bình yên nhất trong cuộc đời con, đã hy sinh, lo lắng và dành cho con những điều tốt đẹp nhất vô điều kiện. Từng bữa cơm ấm, từng lời dặn dò của Mẹ đều là hành trang quý giá nhất theo con lớn khôn.\n\n"
                    "Con chúc Mẹ luôn dồi dào sức khỏe, luôn nở nụ cười thật tươi và an yên trong cuộc sống. Con yêu Mẹ rất nhiều! 💕"
                ),
                "Con yêu của Mẹ",
                "20/10/2026",
                "🌹"
            ),
            (
                "em yêu",
                "Em Yêu",
                "💖 Gửi Công Chúa Bé Nhỏ Của Anh 💖",
                (
                    "Em yêu à,\n\n"
                    "Chúc mừng em nhân ngày 20/10! Chúc cô gái tuyệt vời nhất của anh luôn xinh đẹp, rạng rỡ và ngập tràn niềm vui mỗi ngày.\n\n"
                    "Cảm ơn em đã bước vào cuộc sống của anh, mang theo nụ cười ngọt ngào và những khoảnh khắc ấm áp vô giá. Có em ở bên, mỗi ngày trôi qua với anh đều trở nên thật ý nghĩa và trọn vẹn.\n\n"
                    "Dù sau này có thế nào, anh vẫn luôn ở đây chở che và yêu thương em. Yêu em nhiều hơn mỗi ngày! 🌸💕"
                ),
                "Anh của em",
                "20/10/2026",
                "🌺"
            ),
            (
                "chị gái",
                "Chị Gái",
                "🌷 Gửi Người Chị Tuyệt Vời Của Em 🌷",
                (
                    "Chị gái yêu quý,\n\n"
                    "Nhân ngày 20/10, chúc chị luôn xinh đẹp, trẻ trung, thành công trong công việc và gặp thật nhiều may mắn trong cuộc sống!\n\n"
                    "Cảm ơn chị vì lúc nào cũng che chở, chia sẻ và luôn ủng hộ em trong mọi chuyện. Chúc chị sớm đạt được những mục tiêu lớn và luôn giữ nụ cười hạnh phúc trên môi nhé! 💕"
                ),
                "Em của Chị",
                "20/10/2026",
                "🌷"
            ),
            (
                "bạn thân",
                "Bạn Thân",
                "🌻 Gửi Người Bạn Tri Kỷ 🌻",
                (
                    "Ê bạn thân ơi,\n\n"
                    "Chúc mừng ngày Phụ nữ Việt Nam 20/10 nhé! Chúc bạn ngày càng xinh gái, kiếm thật nhiều tiền, ăn hoài không béo và luôn tràn đầy năng lượng tích cực!\n\n"
                    "Cảm ơn mày đã luôn đồng hành, cùng tao trải qua bao nhiêu kỷ niệm dở khóc dở cười. Mãi là bạn tốt của nhau nhé! 🥳✨"
                ),
                "Đứa bạn chí cốt",
                "20/10/2026",
                "🌻"
            ),
        ]

        cursor.executemany("""
            INSERT INTO letters (passcode, recipient_name, title, content, sender_name, date_str, flower_icon)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_letters)
        conn.commit()

    conn.close()


def get_letter_by_passcode(passcode: str):
    """Tìm thư theo mật khẩu (passcode không phân biệt hoa thường)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM letters WHERE LOWER(TRIM(passcode)) = LOWER(TRIM(?))
    """, (passcode,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_all_letters():
    """Lấy danh sách tất cả các bức thư trong CSDL."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM letters ORDER BY recipient_name ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_letter(passcode, recipient_name, title, content, sender_name, date_str="20/10/2026", flower_icon="🌹"):
    """Lưu hoặc cập nhật bức thư vào database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO letters (passcode, recipient_name, title, content, sender_name, date_str, flower_icon)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(passcode) DO UPDATE SET
            recipient_name = excluded.recipient_name,
            title = excluded.title,
            content = excluded.content,
            sender_name = excluded.sender_name,
            date_str = excluded.date_str,
            flower_icon = excluded.flower_icon
    """, (passcode.strip().lower(), recipient_name.strip(), title.strip(), content.strip(), sender_name.strip(), date_str.strip(), flower_icon.strip()))
    conn.commit()
    conn.close()


def delete_letter(passcode: str):
    """Xóa một bức thư khỏi database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM letters WHERE LOWER(TRIM(passcode)) = LOWER(TRIM(?))", (passcode,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    init_db()
    print("[OK] Đã khởi tạo cơ sở dữ liệu SQLite thành công tại:", DB_PATH)
    all_letters = get_all_letters()
    print(f"[INFO] Hiện có {len(all_letters)} bức thư trong database:")
    for l in all_letters:
        print(f"  - Mật khẩu: [{l['passcode']}] -> Người nhận: {l['recipient_name']}")
