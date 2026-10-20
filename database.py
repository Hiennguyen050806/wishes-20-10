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
    """Khởi tạo cấu trúc bảng và nạp/cập nhật dữ liệu mẫu."""
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
    conn.commit()
    conn.close() # Đóng kết nối tạm thời để dùng hàm save_letter bên dưới

    # KHÔNG DÙNG "if count == 0" NỮA, MÀ LUÔN QUÉT QUA DANH SÁCH ĐỂ CẬP NHẬT
    sample_letters = [
        (
            "tranngocuyenthy",
            "Uyên Thy",
            "💌 Kính Gửi",
            (
                "Happy women's day ,\n\n"
                "Nhân ngày Phụ nữ Việt Nam 20/10, Chúc em ngày càng xinh gái, học giỏi, hạnh phúc và luôn tràn đầy năng lượng tích cực! .\n\n"
                "Chúc cho Uyên Thy học đâu pass đó thi môn nào A+ môn đó nhé đặc biệt là sau này giàu đừng có quên thằng anh này:)).\n\n"
            ),
            "UTE",
            "20/10/2026",
            "🌹"
        ),
        (
            "phamthanhnhan",
            "Thanh Nhàn",
            "💖 Gửi baby 💖",
            (
                "Happy women's day,\n\n"
                "Nhân ngày 20/10! Chúc em ngày càng xinh gái, học giỏi, hạnh phúc và luôn tràn đầy năng lượng tích cực!\n\n"
                "Cảm ơn em đã bước vào cuộc sống của anh, mang theo nụ cười ngọt ngào và những khoảnh khắc ấm áp vô giá. Có em ở bên, mỗi ngày trôi qua với anh đều trở nên thật ý nghĩa và trọn vẹn.\n\n"
            ),
            "Love uuu",
            "20/10/2026",
            "🌺"
        ),
        # ... (thêm bao nhiêu người tùy ý vào đây) ...
    ]

    # Vòng lặp này sẽ tự động THÊM MỚI (nếu chưa có) hoặc CẬP NHẬT (nếu đã có passcode)
    for data in sample_letters:
        save_letter(data[0], data[1], data[2], data[3], data[4], data[5], data[6])


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
