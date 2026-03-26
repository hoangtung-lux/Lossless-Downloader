import os
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QProgressBar,
    QGraphicsDropShadowEffect, QFrame, QSizePolicy, QFileDialog
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer
from PySide6.QtGui import QFont, QColor, QPalette, QLinearGradient, QPainter, QBrush, QPen, QIcon


class GradientHeader(QWidget):
    """Widget header nền gradient từ xanh đậm sang tím."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(160)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#0d6e3b"))
        gradient.setColorAt(0.5, QColor("#1DB954"))
        gradient.setColorAt(1.0, QColor("#1a1040"))
        painter.fillRect(self.rect(), QBrush(gradient))


class PulseButton(QPushButton):
    """Nút bấm với glow effect khi hover."""
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1DB954, stop:1 #17a349);
                color: white;
                border-radius: 22px;
                padding: 11px 28px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1ed760, stop:1 #1DB954);
            }
            QPushButton:pressed {
                background: #158a3e;
            }
        """)
        # Drop shadow glow xanh nhẹ
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor("#1DB954"))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)


class StatCard(QFrame):
    """Card nhỏ hiển thị số liệu thống kê."""
    def __init__(self, label: str, value: str = "0"):
        super().__init__()
        self.setFixedSize(120, 70)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 10px;
                border: 1px solid #2a2a2a;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(2)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet("color: #1DB954; font-size: 22px; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel(label)
        self.text_label.setStyleSheet("color: #888; font-size: 11px;")
        self.text_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.value_label)
        layout.addWidget(self.text_label)

    def set_value(self, v: str):
        self.value_label.setText(v)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpotiFLAC — Lossless Downloader")
        self.setMinimumSize(960, 620)
        self.resize(1040, 680)
        self._stats = {"total": 0, "done": 0, "error": 0}
        self.threads: list = []
        self.cookie_file: str = ""  # Path tới Netscape cookie file

        # Load Icon
        if getattr(sys, 'frozen', False):
            icon_path = os.path.join(sys._MEIPASS, "icon.ico")
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(base_dir, "icon.ico")
        
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet("""
            QMainWindow, QWidget#root {
                background-color: #121212;
            }
            QScrollBar:vertical {
                background: #1e1e1e;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #3e3e3e;
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ─── Header Gradient ───────────────────────────────────────────
        header = GradientHeader()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(36, 22, 36, 18)
        header_layout.setSpacing(6)

        top_row = QHBoxLayout()
        icon_label = QLabel("♫")
        icon_label.setStyleSheet("color: white; font-size: 28px;")
        app_name = QLabel("SpotiFLAC")
        app_name.setStyleSheet("color: white; font-size: 26px; font-weight: bold; letter-spacing: 1px;")
        tagline = QLabel("Lossless Downloader")
        tagline.setStyleSheet("color: rgba(255,255,255,0.65); font-size: 12px; margin-top: 6px;")

        top_row.addWidget(icon_label)
        top_row.addSpacing(8)
        top_row.addWidget(app_name)
        top_row.addSpacing(10)
        top_row.addWidget(tagline)
        top_row.addStretch()

        # Mini badges
        for badge_text in ["FLAC", "Aria2c ×16", "FFmpeg"]:
            badge = QLabel(badge_text)
            badge.setStyleSheet("""
                color: #1DB954;
                border: 1px solid #1DB954;
                border-radius: 8px;
                padding: 2px 8px;
                font-size: 11px;
                font-weight: bold;
            """)
            top_row.addSpacing(6)
            top_row.addWidget(badge)

        header_layout.addLayout(top_row)

        # ─── Input bar (nằm trong header) ───────────────────────────────
        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("🔍  Dán URL hoặc nhập tên bài hát, ca sĩ để tải nhanh...")
        self.url_input.setFixedHeight(44)
        self.url_input.returnPressed.connect(self.start_download)
        self.url_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255,255,255,0.12);
                border: 1.5px solid rgba(255,255,255,0.2);
                color: white;
                border-radius: 22px;
                padding: 0 18px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1.5px solid #1DB954;
                background-color: rgba(255,255,255,0.18);
            }
        """)

        self.download_btn = PulseButton("⬇  Tải xuống")
        self.download_btn.setFixedHeight(44)
        self.download_btn.clicked.connect(self.start_download)

        input_row.addWidget(self.url_input)
        input_row.addWidget(self.download_btn)
        header_layout.addLayout(input_row)

        root_layout.addWidget(header)

        # ─── Stats row ─────────────────────────────────────────────────
        stats_row_widget = QWidget()
        stats_row_widget.setStyleSheet("background-color: #181818;")
        stats_row = QHBoxLayout(stats_row_widget)
        stats_row.setContentsMargins(36, 12, 36, 12)
        stats_row.setSpacing(16)

        self.card_total = StatCard("Tổng cộng", "0")
        self.card_done  = StatCard("Hoàn tất", "0")
        self.card_error = StatCard("Lỗi", "0")

        stats_row.addWidget(self.card_total)
        stats_row.addWidget(self.card_done)
        stats_row.addWidget(self.card_error)
        stats_row.addStretch()

        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        stats_row.addWidget(self.status_label)

        folder_btn = QPushButton("📂  Thay đường dẫn")
        folder_btn.setFixedHeight(34)
        folder_btn.setCursor(Qt.PointingHandCursor)
        folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: #ccc;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 0 14px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border-color: #1DB954;
                color: #1DB954;
            }
        """)
        folder_btn.clicked.connect(self._pick_folder)
        stats_row.addWidget(folder_btn)

        self.cookie_btn = QPushButton("🍪  Cookie")
        self.cookie_btn.setFixedHeight(34)
        self.cookie_btn.setCursor(Qt.PointingHandCursor)
        self.cookie_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: #ccc;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 0 14px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border-color: #f0a500;
                color: #f0a500;
            }
        """)
        self.cookie_btn.setToolTip("Chọn file cookie (.txt) để tải Deezer, Qobuz, Tidal...")
        self.cookie_btn.clicked.connect(self._pick_cookie)
        stats_row.addWidget(self.cookie_btn)

        root_layout.addWidget(stats_row_widget)

        # ─── Separator ─────────────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("border: none; border-top: 1px solid #222;")
        sep.setFixedHeight(1)
        root_layout.addWidget(sep)

        # ─── Table ─────────────────────────────────────────────────────
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["  Bài hát", "Trạng thái", "Tiến độ", "Tốc độ", "ETA"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #121212;
                color: #ccc;
                gridline-color: transparent;
                border: none;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px 10px;
                border-bottom: 1px solid #1e1e1e;
            }
            QTableWidget::item:selected {
                background-color: #1a2e1a;
                color: white;
            }
            QHeaderView::section {
                background-color: #181818;
                color: #666;
                padding: 8px 10px;
                border: none;
                border-bottom: 1px solid #282828;
                font-size: 11px;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #2a2a2a;
                height: 8px;
                text-align: center;
                color: transparent;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1DB954, stop:1 #17a349);
                border-radius: 4px;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(2, 160)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setDefaultSectionSize(52)
        root_layout.addWidget(self.table)

        # ─── Footer ────────────────────────────────────────────────────
        footer = QWidget()
        footer.setFixedHeight(32)
        footer.setStyleSheet("background-color: #0d0d0d;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)
        footer_lbl = QLabel("SpotiFLAC Clone  •  yt-dlp + FFmpeg + Aria2c (16 threads)  •  FLAC Lossless")
        footer_lbl.setStyleSheet("color: #444; font-size: 11px;")
        footer_layout.addWidget(footer_lbl)
        footer_layout.addStretch()
        root_layout.addWidget(footer)

        # Set output dir
        self.output_dir = os.path.join(os.path.expanduser('~'), 'Music', 'Downloads')
        os.makedirs(self.output_dir, exist_ok=True)
        self.status_label.setText(f"💾  {self.output_dir}")

    # ─── Business logic ────────────────────────────────────────────────

    def _pick_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Chọn thư mục lưu nhạc",
            self.output_dir,
            QFileDialog.ShowDirsOnly
        )
        if folder:
            self.output_dir = folder
            self.status_label.setText(f"💾  {folder}")
            self.status_label.setStyleSheet("color: #1DB954; font-size: 12px;")

    def _pick_cookie(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn Cookie File (Netscape .txt)",
            os.path.expanduser('~'),
            "Cookie files (*.txt);;Tất cả (*.*)"
        )
        if path:
            self.cookie_file = path
            name = os.path.basename(path)
            self.cookie_btn.setText(f"🍪  {name}")
            self.cookie_btn.setStyleSheet(self.cookie_btn.styleSheet().replace("#ccc", "#f0a500"))

    def start_download(self):
        raw_input = self.url_input.text().strip()
        if not raw_input:
            return

        # Smart Detect: Nếu không phải URL thì coi là từ khóa tìm kiếm
        if not raw_input.startswith("http"):
            url = f"ytsearch1:{raw_input}"
            search_display = f"🔍 {raw_input}"
        else:
            url = raw_input
            search_display = "⏳ Đang lấy thông tin..."

        from core.downloader import DownloaderThread

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setRowHeight(row, 52)

        self.table.setItem(row, 0, QTableWidgetItem(search_display))
        status_item = QTableWidgetItem("Khởi tạo")
        status_item.setForeground(QColor("#888"))
        self.table.setItem(row, 1, status_item)

        progress_bar = QProgressBar()
        progress_bar.setValue(0)
        progress_bar.setTextVisible(False)
        self.table.setCellWidget(row, 2, progress_bar)
        self.table.setItem(row, 3, QTableWidgetItem("—"))
        self.table.setItem(row, 4, QTableWidgetItem("—"))

        output_dir = self.output_dir
        os.makedirs(output_dir, exist_ok=True)

        thread = DownloaderThread(url, output_dir, cookie_file=self.cookie_file)
        thread.row_index = row
        thread.progress_signal.connect(self.update_progress)
        thread.finished_signal.connect(self.download_finished)
        thread.error_signal.connect(self.download_error)
        thread.finished.connect(lambda: self._cleanup_thread(thread))

        self.threads.append(thread)
        thread.start()
        self.url_input.clear()

        self._stats["total"] += 1
        self.card_total.set_value(str(self._stats["total"]))

    def _cleanup_thread(self, thread):
        try:
            self.threads.remove(thread)
        except ValueError:
            pass

    def update_progress(self, data):
        sender_thread = self.sender()
        if not sender_thread:
            return
        row = sender_thread.row_index
        status = data.get('status', '')

        title_item = self.table.item(row, 0)
        if title_item:
            title = data.get('title', '')
            if title and title != 'Đang kết nối...':
                title_item.setText(f"🎵  {title}")

        status_map = {
            'fetching_metadata': ('Đang lấy info', '#888'),
            'downloading': ('Đang tải', '#1DB954'),
            'processing': ('FFmpeg...', '#f0a500'),
        }
        text, color = status_map.get(status, (status, '#888'))
        status_item = self.table.item(row, 1)
        if status_item:
            status_item.setText(text)
            status_item.setForeground(QColor(color))

        progress_bar = self.table.cellWidget(row, 2)
        if progress_bar:
            progress_bar.setValue(int(data.get('percentage', 0)))

        speed_item = self.table.item(row, 3)
        if speed_item:
            speed_item.setText(data.get('speed', '—'))

        eta_item = self.table.item(row, 4)
        if eta_item:
            eta_item.setText(data.get('eta', '—'))

    def download_finished(self, title, filepath):
        sender_thread = self.sender()
        if not sender_thread:
            return
        row = sender_thread.row_index

        title_item = self.table.item(row, 0)
        if title_item:
            title_item.setText(f"✅  {title}")
            title_item.setForeground(QColor("#ffffff"))

        status_item = self.table.item(row, 1)
        if status_item:
            status_item.setText("Hoàn tất")
            status_item.setForeground(QColor("#1DB954"))

        progress_bar = self.table.cellWidget(row, 2)
        if progress_bar:
            progress_bar.setValue(100)

        for col, text in [(3, "Done"), (4, "0s")]:
            item = self.table.item(row, col)
            if item:
                item.setText(text)

        self._stats["done"] += 1
        self.card_done.set_value(str(self._stats["done"]))

    def download_error(self, error_msg):
        sender_thread = self.sender()
        if not sender_thread:
            return
        row = sender_thread.row_index

        title_item = self.table.item(row, 0)
        if title_item:
            title_item.setForeground(QColor("#ff5555"))

        status_item = self.table.item(row, 1)
        if status_item:
            status_item.setText("❌ Lỗi")
            status_item.setForeground(QColor("#ff5555"))

        speed_item = self.table.item(row, 3)
        if speed_item:
            speed_item.setText(str(error_msg)[:50])
            speed_item.setForeground(QColor("#ff5555"))

        self._stats["error"] += 1
        self.card_error.set_value(str(self._stats["error"]))

    def closeEvent(self, event):
        for thread in list(self.threads):
            thread.cancel()
            thread.wait(5000)
        self.threads.clear()
        event.accept()
