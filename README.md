# 🎵 SpotiFLAC Clone - Lossless Music Downloader

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![UI](https://img.shields.io/badge/UI-PySide6-green.svg)](https://www.qt.io/qt-for-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SpotiFLAC Clone** là một ứng dụng desktop mạnh mẽ, giúp bạn tải nhạc chất lượng cao (**Lossless FLAC**) từ nhiều nguồn khác nhau với tốc độ tối đa và giao diện hiện đại.

---

## ✨ Tính Năng Nổi Bật

- 🚀 **Smart Routing (Điều hướng thông minh):**
  - **Hi-Fi thật:** Tự động điều hướng link **Tidal, Qobuz, Deezer** qua engine \`streamrip\` để lấy file FLAC gốc.
  - **Chất lượng cao:** Hỗ trợ **YouTube Music, SoundCloud, Spotify** qua \`yt-dlp\`.
- 🔍 **Search-to-Download:** Tìm kiếm trực tiếp bằng tên bài hát/ca sĩ ngay trong app, không cần dán link.
- ⚡ **Siêu tốc độ:** Tích hợp \`aria2c\` với cấu hình 16 luồng tải song song.
- 🎨 **Giao diện hiện đại:** Thiết kế Dark Mode phong cách Spotify, hiệu ứng Gradient và Pulse animation mượt mà.
- 📦 **Mì ăn liền:** Đã được đóng gói thành file \`.exe\` duy nhất, không cần cài đặt Python.
- 🖼️ **Full Metadata:** Tự động nhúng Cover Art, Album và Lời bài hát vào file nhạc.

---

## 🛠️ Yêu Cầu Hệ Thống

Nếu bạn chạy từ mã nguồn:
- Python 3.14+
- Các công cụ trong thư mục \`bin/\` (FFmpeg, Aria2c, Deno).

Nếu bạn dùng bản đóng gói:
- Windows 10/11 64-bit.

---

## 🚀 Hướng Dẫn Sử Dụng

1. **Tải về:** Clone repository hoặc tải bản \`.exe\` trong mục \`dist\`.
2. **Nhập liệu:** Dán URL bài hát hoặc gõ từ khóa tìm kiếm vào ô nhập liệu.
3. **Cấu hình (Tùy chọn):** 
   - Nhấn nút **Cookie** để nạp tệp cookie (nếu bạn có tài khoản Premium Tidal/Deezer).
   - Chọn thư mục lưu nhạc qua nút **Thay đường dẫn**.
4. **Thưởng thức:** Nhấn **Tải xuống** và đợi giây lá để có bản nhạc Lossless xịn nhất.

---

## 💻 Cấu Trúc Dự Án

\`\`\`text
├── bin/            # Các công cụ bổ trợ (FFmpeg, Aria2c, Deno, Rip)
├── core/           # Logic xử lý tải nhạc và routing
├── ui/             # Giao diện người dùng PySide6
├── main.py         # Điểm khởi chạy ứng dụng
└── build.bat       # Script tự động đóng gói .exe
\`\`\`

---

## 📜 Miễn Trừ Trách Nhiệm

Dự án này được tạo ra cho mục đích học tập và nghiên cứu cá nhân. Vui lòng tôn trọng quyền tác giả và quy định của các nền tảng phát nhạc trực tuyến. Chúng tôi không chịu trách nhiệm về bất kỳ hành vi sử dụng sai mục đích nào.

---

**Made with ❤️ by [hoangtung-lux]**
