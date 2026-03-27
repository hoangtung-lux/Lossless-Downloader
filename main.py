import sys
import os
import multiprocessing

# QUAN TRỌNG: Phải gọi trước khi làm bất kỳ việc gì khác.
# Ngăn PyInstaller trên Windows spawn vô hạn khi chạy file .exe.
if __name__ == "__main__":
    multiprocessing.freeze_support()

# Cấu hình lại biến môi trường PATH đầu tiên để yt-dlp nhận được Deno/FFmpeg.
if getattr(sys, 'frozen', False):
    # Đang chạy từ executable (PyInstaller)
    base_dir = sys._MEIPASS
else:
    # Đang chạy từ file .py bình thường
    base_dir = os.path.dirname(os.path.abspath(__file__))

bin_dir = os.path.join(base_dir, 'bin')
os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Font chữ đẹp hơn
    font = app.font()
    font.setFamily("Segoe UI")
    app.setFont(font)
    
    window = MainWindow()
    
    # Tạo folder mặc định tải nhạc
    default_path = os.path.join(os.path.expanduser('~'), 'Music', 'Downloads')
    os.makedirs(default_path, exist_ok=True)
    window.status_label.setText(f"Thư mục lưu: {default_path}")
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
