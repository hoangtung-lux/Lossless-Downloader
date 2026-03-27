"""
Smart routing downloader:
- Tidal / Qobuz / Deezer / Amazon → streamrip (FLAC thật)
- YouTube / SoundCloud / Spotify / các trang khác → yt-dlp + cookie file (nếu có)
"""
import os
import sys
import re
import subprocess
import urllib.request
import yt_dlp
import streamrip # Đảm bảo PyInstaller bundle thư viện này
from PySide6.QtCore import QThread, Signal

# Map domain → streamrip source ID
STREAMRIP_SOURCES = {
    'tidal.com': 'tidal',
    'qobuz.com': 'qobuz',
    'deezer.com': 'deezer',
    'music.amazon': 'amazon',
}


def detect_source(url: str) -> str:
    """Trả về tên nguồn (streamrip source hoặc 'ytdlp')."""
    for domain, source in STREAMRIP_SOURCES.items():
        if domain in url:
            return source
    return 'ytdlp'


class DownloaderThread(QThread):
    progress_signal = Signal(dict)
    finished_signal = Signal(str, str)
    error_signal = Signal(str)

    def __init__(self, url: str, output_dir: str, cookie_file: str = ""):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.cookie_file = cookie_file  # Netscape cookie file hoặc config.toml
        self.is_cancelled = False

    def run(self):
        # Xác định bin_dir cho cả dev và đóng gói .exe
        if getattr(sys, 'frozen', False):
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.bin_dir = os.path.join(base_dir, 'bin')
        
        source = detect_source(self.url)
        if source == 'ytdlp':
            self._run_ytdlp()
        else:
            self._run_streamrip(source)

    # ─── yt-dlp branch ─────────────────────────────────────────────────────

    def _run_ytdlp(self):
        ffmpeg_exe = os.path.join(self.bin_dir, 'ffmpeg.exe')
        aria_exe = os.path.join(self.bin_dir, 'aria2c.exe')
        outtmpl = os.path.join(self.output_dir, '%(title)s.%(ext)s')

        # Khi chạy file .exe (frozen), việc gọi aria2c qua subprocess
        # có thể block UI thread hoặc gây freeze. Dùng downloader nội bộ của yt-dlp.
        is_frozen = getattr(sys, 'frozen', False)
        use_aria2c = (not is_frozen) and os.path.exists(aria_exe)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'progress_hooks': [self.my_hook],
            'ffmpeg_location': ffmpeg_exe if os.path.exists(ffmpeg_exe) else None,
            # Chỉ dùng aria2c khi chạy từ source, không phải .exe
            **({
                'external_downloader': aria_exe,
                'external_downloader_args': {
                    'aria2c': ['-c', '-j', '16', '-x', '16', '-s', '16', '-k', '1M'],
                },
            } if use_aria2c else {}),
            'concurrent_fragment_downloads': 8,  # Thay thế aria2c khi chạy .exe
            'writethumbnail': True,
            'write_description': False,
            'write_annotations': False,
            'writesubtitles': False, # Tắt để tránh file .vtt rác
            'skip_download_live_chat': True, # Tắt tải live chat JSON
            'noprogress': True,
            'quiet': True,
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'flac'},
                {'key': 'FFmpegMetadata', 'add_metadata': True},
                {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},
            ],
        }

        if self.cookie_file and os.path.exists(self.cookie_file):
            ydl_opts['cookiefile'] = self.cookie_file

        try:
            self._emit_status('fetching_metadata', 'Đang kết nối...')

            url = self.url
            if 'spotify.com' in url:
                url = self._resolve_spotify(url)
                if url is None:
                    return

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if 'entries' in info:
                    info = info['entries'][0]
                title = info.get('title', 'Unknown Title')
                filepath = ydl.prepare_filename(info)
                base, _ = os.path.splitext(filepath)
                final_path = f"{base}.flac"
                if not os.path.exists(final_path):
                    final_path = filepath
                self.finished_signal.emit(title, final_path)
        except Exception as e:
            if not self.is_cancelled:
                self.error_signal.emit(str(e))

    def _resolve_spotify(self, url: str):
        self._emit_status('fetching_metadata', 'Parsing Spotify...')
        try:
            req = urllib.request.Request(
                url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
            og_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', html)
            artist_match = re.search(r'<meta\s+property="og:description"\s+content="([^"]+)"', html)
            if og_match:
                song = og_match.group(1).strip()
                artist = artist_match.group(1).split('·')[0].strip() if artist_match else ''
                search_term = f"{song} {artist}".strip()
            else:
                title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
                if title_match:
                    full_title = title_match.group(1)
                    search_term = full_title.split('|')[0].replace('- song and lyrics by', '').strip()
                else:
                    raise ValueError("Không lấy được tên bài từ Spotify")
            return f"ytsearch1:{search_term}"
        except Exception as e:
            self.error_signal.emit(f"Lỗi Spotify: {str(e)}")
            return None

    # ─── streamrip branch ──────────────────────────────────────────────────

    def _run_streamrip(self, source: str):
        self._emit_status('fetching_metadata', f'Đang kết nối {source.capitalize()}...')
        try:
            rip_exe = os.path.join(self.bin_dir, 'rip.exe')
            if not os.path.exists(rip_exe):
                # Thử tìm trong venv nếu đang dev
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                rip_exe = os.path.join(base_dir, 'venv', 'Scripts', 'rip.exe')
                if not os.path.exists(rip_exe):
                    rip_exe = 'rip'

            cmd = [
                rip_exe, 'url', self.url,
                '--directory', self.output_dir,
            ]
            if self.cookie_file and os.path.exists(self.cookie_file):
                cmd += ['--config-path', self.cookie_file]

            self._emit_status('downloading', f'[{source.upper()}] Đang tải FLAC lossless thật...')

            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            assert proc.stdout is not None
            title = str(self.url)
            for line in proc.stdout:
                line = line.strip()
                if self.is_cancelled:
                    proc.terminate()
                    return
                if 'Downloading' in line:
                    self._emit_status('downloading', line[:60])
                elif line.startswith('Title:') or 'Album:' in line:
                    title = line.split(':', 1)[-1].strip()

            proc.wait()
            if proc.returncode != 0:
                raise RuntimeError(f"streamrip thoát với mã lỗi {proc.returncode}")

            self.finished_signal.emit(title, self.output_dir)

        except FileNotFoundError:
            self.error_signal.emit(
                "Không tìm thấy streamrip! Hãy chạy: pip install streamrip"
            )
        except Exception as e:
            if not self.is_cancelled:
                self.error_signal.emit(str(e))

    # ─── Hooks ─────────────────────────────────────────────────────────────

    def _emit_status(self, status: str, title: str):
        self.progress_signal.emit({
            'status': status,
            'percentage': 0,
            'speed': '...',
            'eta': '...',
            'filename': '',
            'title': title,
        })

    def my_hook(self, d):
        if self.is_cancelled:
            raise Exception("Download cancelled by user")

        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            percentage = (downloaded / total * 100) if total > 0 else 0.0
            speed = d.get('speed', 0)
            speed_str = f"{speed / 1024 / 1024:.2f} MiB/s" if speed else "Đang tính..."
            eta = d.get('eta', 0)
            self.progress_signal.emit({
                'status': 'downloading',
                'percentage': percentage,
                'speed': speed_str,
                'eta': f"{eta}s" if eta else "...",
                'filename': os.path.basename(d.get('filename', '')),
                'title': d.get('info_dict', {}).get('title', 'Đang tải...'),
            })
        elif d['status'] == 'finished':
            self.progress_signal.emit({
                'status': 'processing',
                'percentage': 100.0,
                'speed': 'Đang nén...',
                'eta': '...',
                'filename': os.path.basename(d.get('filename', '')),
                'title': d.get('info_dict', {}).get('title', 'FFmpeg...'),
            })

    def cancel(self):
        self.is_cancelled = True
