# 🎵 SpotiFLAC Clone - Lossless Music Downloader

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![UI](https://img.shields.io/badge/UI-PySide6-green.svg)](https://www.qt.io/qt-for-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SpotiFLAC Clone** là một ứng dụng desktop mạnh mẽ, giúp bạn tải nhạc chất lượng cao (**Lossless FLAC**) từ nhiều nguồn khác nhau với tốc độ tối đa và giao diện hiện đại.

---

## ✨ Tính Năng Nổi Bật

- 🚀 **Smart Routing (Điều hướng thông minh):**
  - **Hi-Fi thật:** Tự động điều hướng link **Tidal, Qobuz, Deezer** qua engine `streamrip` để lấy file FLAC gốc.
  - **Chất lượng cao:** Hỗ trợ **YouTube Music, SoundCloud, Spotify** qua `yt-dlp`.
- 🔍 **Search-to-Download:** Tìm kiếm trực tiếp bằng tên bài hát/ca sĩ ngay trong app, không cần dán link.
- ⚡ **Siêu tốc độ:** Tích hợp `aria2c` với cấu hình 16 luồng tải song song.
- 🎨 **Giao diện hiện đại:** Thiết kế Dark Mode phong cách Spotify, hiệu ứng Gradient và Pulse animation mượt mà.
- 📦 **Mì ăn liền:** Đã được đóng gói thành file `.exe` duy nhất, không cần cài đặt Python.
- 🖼️ **Full Metadata:** Tự động nhúng Cover Art, Album và Lời bài hát vào file nhạc.

---

## 🛠️ Yêu Cầu Hệ Thống

Nếu bạn chạy từ mã nguồn:
- Python 3.14+
- Các công cụ trong thư mục `bin/` (FFmpeg, Aria2c, Deno).

Nếu bạn dùng bản đóng gói:
- Windows 10/11 64-bit.

---

## 🚀 Hướng Dẫn Sử Dụng

### Cho Người Dùng (Chỉ cần chạy .exe)
1. Truy cập mục **Releases** trên GitHub.
2. Tải bản **`SpotiFLAC-Clone.exe`** mới nhất về máy và chạy.

### Cho Nhà Phát Triển (Chạy từ mã nguồn)
Nếu bạn muốn chỉnh sửa code hoặc đóng góp cho dự án:
1. **Clone repository:**
   ```bash
   git clone https://github.com/hoangtung-lux/Lossless-Downloader.git
   cd Lossless-Downloader
   ```
2. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Chuẩn bị công cụ (bin/):** 
   Tải và giải nén các công cụ sau vào thư mục `bin/` (hoặc thêm vào PATH):
   - FFmpeg (Windows build)
   - Aria2c
   - Deno (Dành cho bản YouTube)
   - `streamrip` (Có thể cài qua pip)
4. **Chạy ứng dụng:**
   ```bash
   python main.py
   ```

---

## 💻 Cấu Trúc Dự Án

```text
├── bin/            # Các công cụ bổ trợ (FFmpeg, Aria2c, Deno, Rip)
├── core/           # Logic xử lý tải nhạc và routing
├── ui/             # Giao diện người dùng PySide6
├── main.py         # Điểm khởi chạy ứng dụng
└── build.bat       # Script tự động đóng gói .exe
```

---

## 📜 Miễn Trừ Trách Nhiệm

Dự án này được tạo ra cho mục đích học tập và nghiên cứu cá nhân. Vui lòng tôn trọng quyền tác giả và quy định của các nền tảng phát nhạc trực tuyến. Chúng tôi không chịu trách nhiệm về bất kỳ hành vi sử dụng sai mục đích nào.

---

**Made with ❤️ by [hoangtung-lux]**
