# Hướng dẫn Upload Source Code lên GitHub 🚀

Để chia sẻ dự án **Lumina Music-Downloader** của bác lên GitHub một cách chuyên nghiệp nhất, bác hãy làm theo các bước sau nhé:

## Bước 1: Chuẩn bị Repository
1. Truy cập [github.com](https://github.com/) và tạo một Repository mới (ví dụ tên là `Lumina Music-Downloader`).
2. Đừng tích chọn "Initialize this repository with a README" (vì mình đã có code sẵn rồi).

## Bước 2: Chạy lệnh Git tại thư mục dự án
Bác mở Terminal ngay tại thư mục `LosslessDownloader` và gõ lần lượt các lệnh này:

```bash
# 1. Khởi tạo Git
git init

# 2. Thêm toàn bộ file (Git sẽ tự bỏ qua các file rác nhờ .gitignore em đã tạo)
git add .

# 3. Tạo bản lưu đầu tiên
git commit -m "Initial commit - Lumina Music Downloader"

# 4. Đổi tên nhánh chính thành main
git branch -M main

# 5. Kết nối tới link GitHub của bác (Thay [LINK_CUA_BAC] bằng link bác vừa tạo)
git remote add origin [LINK_CUA_BAC]

# 6. Đẩy code lên!
git push -u origin main
```

## Lưu ý quan trọng ⚠️
- **Thư mục `bin/`**: Em đã để mặc định là **KHÔNG** ignore trong `.gitignore`. Điều này giúp người khác tải về là dùng được luôn (Mì ăn liền). Tuy nhiên nếu bác muốn repo nhẹ hơn, hãy sửa `.gitignore` để bỏ qua `bin/`.
- **Thư mục `venv/`**: Tuyệt đối không upload cái này (em đã ignore sẵn rồi), vì mỗi máy sẽ tự cài thư viện riêng.

Chúc bác có một Profile GitHub thật xịn nhé! 🌟✨
