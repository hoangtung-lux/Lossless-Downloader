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
import ssl
import yt_dlp
from PySide6.QtCore import QThread, Signal
from core.resolver import resolver

# Bỏ qua kiểm tra SSL cho urllib (Khắc phục lỗi trên một số máy Windows)
ssl._create_default_https_context = ssl._create_unverified_context

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

    def __init__(self, url: str, output_dir: str, cookie_file: str = "", codec: str = "flac"):
        super().__init__()
        self.url = url
        self.output_dir = output_dir
        self.cookie_file = cookie_file  # Netscape cookie file hoặc config.toml
        self.codec = codec.lower()
        self.is_cancelled = False

    def run(self):
        # Xác định bin_dir cho cả dev và đóng gói .exe
        if getattr(sys, 'frozen', False):
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.bin_dir = os.path.join(base_dir, 'bin')
        
        current_url = self.url
        # Nếu là Spotify, thử tìm link lossless trước
        if 'spotify.com' in current_url:
            resolved = self._resolve_spotify(current_url)
            if resolved:
                if resolved.startswith('http'):
                    current_url = resolved
                    print(f"[Resolver] Chuyển hướng sang: {current_url}")
                else:
                    # Là ytsearch1:... thì vẫn dùng ytdlp
                    self.url = resolved
        
        source = detect_source(current_url)
        if source == 'ytdlp':
            # Nếu đã resolve ra ytsearch thì _run_ytdlp sẽ dùng self.url
            self._run_ytdlp()
        else:
            # Nếu resolve ra link Deezer/Tidal/v.v. thì dùng streamrip
            self.url = current_url
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
                    'aria2c': ['-c', '-j', '16', '-x', '16', '-s', '16', '-k', '1M', '--file-allocation=none', '--summary-interval=0'],
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
                # 1. Tách Audio
                {'key': 'FFmpegExtractAudio', 'preferredcodec': self.codec, 'preferredquality': '320' if self.codec == 'mp3' else None},
                # 2. SponsorBlock (Tính năng từ YTDLnis): Tự động xóa sponsor, intro, outro
                {'key': 'SponsorBlock'},
                # 3. Metadata nâng cao
                {'key': 'FFmpegMetadata', 'add_metadata': True},
                {'key': 'EmbedThumbnail', 'already_have_thumbnail': False},
            ],
            # Cấu hình SponsorBlock chi tiết: xóa hết các đoạn không phải âm nhạc
            'sponsorblock_remove': ['sponsor', 'intro', 'outro', 'selfpromo', 'preview', 'filler'],
        }

        if self.cookie_file and os.path.exists(self.cookie_file):
            ydl_opts['cookiefile'] = self.cookie_file

        try:
            self._emit_status('fetching_metadata', 'Đang kết nối...')

            url = self.url
            # (Spotify đã được xử lý ở run() nếu là link Spotify)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if 'entries' in info:
                    info = info['entries'][0]
                title = info.get('title', 'Unknown Title')
                filepath = ydl.prepare_filename(info)
                base, _ = os.path.splitext(filepath)
                # Đảm bảo signal trả về đúng extension đã chọn
                final_path = f"{base}.{self.codec}"
                if not os.path.exists(final_path):
                    final_path = filepath
                self.finished_signal.emit(title, final_path)
        except Exception as e:
            if not self.is_cancelled:
                self.error_signal.emit(str(e))

    def _resolve_spotify(self, url: str):
        self._emit_status('fetching_metadata', 'Lumina Resolver đang xử lý...')
        try:
            # 1. Trích xuất Spotify ID
            track_id_match = re.search(r'track/([a-zA-Z0-9]+)', url)
            if not track_id_match:
                return f"ytsearch1:{url}"
            
            track_id = track_id_match.group(1)
            
            # 2. Thử Songlink để lấy link Deezer/Tidal (Nhanh nhất)
            mapping = resolver.resolve_via_songlink(url)
            for plat in ['deezer', 'tidal', 'qobuz']:
                if plat in mapping:
                    print(f"[Resolver] Tìm thấy link {plat} qua Songlink")
                    return mapping[plat]

            # 3. Lấy ISRC và tìm trên Deezer (Chính xác nhất nếu Songlink tịt)
            isrc = resolver.get_track_isrc(track_id)
            if isrc:
                deezer_url = resolver.find_on_deezer_by_isrc(isrc)
                if deezer_url:
                    print(f"[Resolver] Tìm thấy qua ISRC ({isrc}) trên Deezer")
                    return deezer_url

            # 4. Fallback: Lấy metadata để search YouTube (Nếu các cách trên thất bại)
            # Dùng lại logic scraping cũ hoặc gọi Spotify API lấy Title/Artist
            req = urllib.request.Request(
                url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            html_data = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
            og_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', html_data)
            artist_match = re.search(r'<meta\s+property="og:description"\s+content="([^"]+)"', html_data)
            
            if og_match:
                song = og_match.group(1).strip()
                artist = artist_match.group(1).split('·')[0].strip() if artist_match else ''
                search_term = f"{song} {artist}".strip()
            else:
                search_term = url # Cùng lắm thì để yt-dlp tự xử lý
            
            normalized = resolver.normalize_title(search_term)
            return f"ytsearch1:{normalized}"
            
        except Exception as e:
            print(f"[Resolver] Error: {e}")
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

            # Ánh xạ codec cho streamrip
            rip_codec_map = {
                'flac': 'flac',
                'mp3': 'mp3',
                'm4a': 'aac',
                'opus': 'ogg'
            }
            rip_codec = rip_codec_map.get(self.codec, 'flac')

            cmd = [
                rip_exe, 'url', self.url,
                '--directory', self.output_dir,
                '--codec', rip_codec,
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
