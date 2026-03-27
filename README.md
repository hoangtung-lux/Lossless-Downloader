# 🎵 Lumina Music Downloader - Lossless Music Downloader

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![UI](https://img.shields.io/badge/UI-PySide6-purple.svg)](https://www.qt.io/qt-for-python)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Lumina Music Downloader** là một ứng dụng desktop mạnh mẽ, giúp bạn tải nhạc chất lượng cao (**Lossless FLAC**) từ nhiều nguồn khác nhau với tốc độ tối đa và giao diện hiện đại phong cách **Lumina Prism**.

---

## ✨ Tính Năng Nổi Bật

- 🚀 **Smart Routing (Điều hướng thông minh):**
  - **Hi-Fi thật:** Tự động điều hướng link **Tidal, Qobuz, Deezer** qua engine `streamrip` để lấy file FLAC gốc.
  - **ISRC Matching:** Công nghệ ISRC từ bản Android giúp tìm nhạc Spotify trên các nguồn lossless chính xác 100%.
  - **YouTube Music:** Hỗ trợ tải chất lượng cao từ YouTube qua `yt-dlp` ổn định.
- 🔍 **Search-to-Download:** Tìm kiếm trực tiếp bằng tên bài hát/ca sĩ ngay trong app, không cần dán link.
- ⚡ **Siêu tốc độ:** Tích hợp `aria2c` với cấu hình 16 luồng tải song song.
- 🎨 **Giao diện hiện đại:** Thiết kế Dark Mode phong cách Spotify, hiệu ứng Gradient và Pulse animation mượt mà.
- 📦 **Mì ăn liền:** Đã được đóng gói thành file `.exe` duy nhất, không cần cài đặt Python.
- 🖼️ **Full Metadata:** Tự động nhúng Cover Art, Album và Lời bài hát vào file nhạc.

# 🌈 Lumina Music - Premium Lossless Downloader

> **Slogan:** Khám phá âm nhạc chất lượng cao với phong cách Prism hiện đại.

Lumina Music là phiên bản nâng cấp toàn diện từ bộ mã nguồn gốc Android, được tinh giản và tối ưu hóa cho Desktop với các công nghệ tải nhạc tiên tiến nhất hiện nay.

## ✨ Tính năng nổi bật (Siêu Mix)

- **🎼 Đa dạng Định dạng**: Hỗ trợ xuất file FLAC, MP3 (320kbps), M4A, OPUS.
- **🚀 Siêu tốc độ**: Tích hợp Aria2c (16 luồng song song) giúp tải nhạc cực nhanh.
- **🛡️ SponsorBlock**: Tự động dọn dẹp các đoạn quảng cáo, intro, outro rườm rà từ YouTube.
- **🔍 ISRC Matching**: Công nghệ ánh xạ mã ISRC từ Spotify giúp tìm đúng bản nhạc Lossless trên Deezer/Tidal.
- **🌐 Metadata VN**: Tự động nhận diện và ưu tiên tên bài hát Tiếng Việt chuẩn.
- **💎 Giao diện Prism**: Phong cách Tím-Cyan hiện đại với hiệu ứng Blur nhẹ nhàng, sang trọng.

## 🚀 Cách sử dụng (A-Z)

Cực kỳ đơn giản cho người dùng không muốn cài đặt phức tạp:

1. **Tải về**: Giải nén bộ mã nguồn.
2. **Khởi chạy**: Nhấp đúp vào tệp **`Install_and_Run.bat`**.
3. **Thưởng thức**: Dán link nhạc hoặc nhập tên bài hát và nhấn **Tải xuống**.

## 🛠️ Yêu cầu hệ thống
- **Hệ điều hành**: Windows 10/11 (64-bit).
- **Phụ thuộc**: Python 3.10+ (Đã tích hợp cài đặt tự động qua .bat).
- **Công cụ**: FFmpeg (Cần có trong PATH để sử dụng SponsorBlock).

---
*Phát triển bởi Antigravity với tình yêu dành cho âm nhạc.*

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
