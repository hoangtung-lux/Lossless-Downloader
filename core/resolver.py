import requests
import json
import subprocess
import os
import time
import hmac
import hashlib
import base64
import struct
import re
from typing import Optional, Dict, List

# Hệ thống Resolver cho Lumina Music
class SpotifyResolver:
    """Handles Spotify metadata extraction and cross-platform mapping using ISRC/Songlink."""
    
    # Secret identified from source code to bypass guest token restrictions
    TOTP_SECRET = "GM3TMMJTGYZTQNZVGM4DINJZHA4TGOBYGMZTCMRTGEYDSMJRHE4TEOBUG4YTCMRUGQ4DQOJUGQYTAMRRGA2TCMJSHE3TCMBY"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        })
        self.access_token = None
        self.token_expiry = 0.0
        self.market = "VN" # Mặc định thị trường Việt Nam

    def _get_totp(self) -> str:
        """Generates a TOTP code using the embedded secret."""
        key = base64.b32decode(self.TOTP_SECRET, True)
        msg = struct.pack(">Q", int(time.time() / 30))
        digest = hmac.new(key, msg, hashlib.sha1).digest()
        ob = digest[19] & 15
        token = (struct.unpack(">I", digest[ob:ob+4])[0] & 0x7fffffff) % 1000000
        return "{:06d}".format(token)

    def refresh_token(self) -> bool:
        """Retrieves a fresh Spotify access token using the TOTP bypass."""
        totp = self._get_totp()
        url = "https://open.spotify.com/api/token"
        params = {
            "reason": "init",
            "productType": "web-player",
            "totp": totp,
            "totpVer": "61",
            "totpServer": totp
        }
        try:
            resp = self.session.get(url, params=params, timeout=10, verify=False)
            if resp.status_code == 200:
                data = resp.json()
                self.access_token = data.get("accessToken")
                # Tokens usually last 1 hour, let's refresh every 50 mins
                self.token_expiry = time.time() + 3000 
                return True
        except Exception:
            pass
        return False

    def get_token(self) -> Optional[str]:
        if not self.access_token or time.time() > self.token_expiry:
            self.refresh_token()
        return self.access_token

    def get_track_isrc(self, spotify_id: str) -> Optional[str]:
        """Tries to fetch ISRC using both V1 API and GraphQL fallback."""
        token = self.get_token()
        if not token:
            return None
            
        # 1. Try V1 API (Faster if works)
        url = f"https://api.spotify.com/v1/tracks/{spotify_id}"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            resp = self.session.get(url, headers=headers, timeout=10, verify=False)
            if resp.status_code == 200:
                data = resp.json()
                isrc = data.get("external_ids", {}).get("isrc")
                if isrc: return isrc
        except Exception as e:
            print(f"[Resolver] V1 Error: {e}")

        # 2. Try GraphQL (More robust bypass)
        return self.get_track_isrc_graphql(spotify_id)

    def get_track_isrc_graphql(self, track_id: str) -> Optional[str]:
        """Sử dụng Deno Core (TypeScript) để phân giải ISRC (Tính năng Language Combination) hoặc fallback về Python."""
        try:
            # Ưu tiên sử dụng Deno để đạt hiệu năng cao hơn
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            deno_exe = os.path.join(base_dir, "bin", "deno.exe")
            ts_script = os.path.join(base_dir, "core", "resolver.ts")

            if os.path.exists(deno_exe) and os.path.exists(ts_script):
                cmd = [deno_exe, "run", "--allow-net", ts_script, track_id]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                data = json.loads(result.stdout)
                if "isrc" in data:
                    print(f"[*] Deno Core Resolved: {data['isrc']}")
                    return data["isrc"]
        except Exception as e:
            print(f"[!] Deno Core Error, falling back to Python: {str(e)}")

        # Fallback về Python thuần túy
        token = self.get_token() # Assuming get_web_token is get_token
        if not token:
            return None

        url = "https://api-partner.spotify.com/pathfinder/v1/query"
        params = {
            "operationName": "getTrack",
            "variables": json.dumps({"uri": f"spotify:track:{track_id}"}),
            "extensions": json.dumps({
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "612585ae06ba435ad26369870deaae23b5c8800a256cd8a57e08eddc25a37294"
                }
            })
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            # Dùng params tự động encode cho GET request
            resp = self.session.get(url, params=params, headers=headers, timeout=10, verify=False)
            if resp.status_code == 200:
                data = resp.json()
                # Thường ISRC nằm sâu trong trackUnion -> externalIds
                track = data.get("data", {}).get("trackUnion", {})
                return track.get("externalIds", {}).get("isrc", {}).get("isrc")
        except Exception as e:
            print(f"[Resolver] GraphQL Error: {e}")
        return None

    def resolve_via_songlink(self, spotify_url: str) -> Dict[str, str]:
        """Uses Odesli (Songlink) to find platform equivalent URLs."""
        # Clean URL to avoid param issues
        clean_url = spotify_url.split('?')[0]
        url = f"https://api.song.link/v1-alpha.1/links?url={clean_url}"
        results = {}
        try:
            resp = self.session.get(url, timeout=10, verify=False)
            if resp.status_code == 200:
                data = resp.json()
                links_by_platform = data.get("linksByPlatform", {})
                
                # Mapping Songlink platform keys to our internal keys
                map_keys = {
                    "deezer": "deezer",
                    "tidal": "tidal",
                    "amazonMusic": "amazon",
                    "qobuz": "qobuz",
                    "youtubeMusic": "youtube_music",
                    "youtube": "youtube"
                }
                
                for sl_key, our_key in map_keys.items():
                    if sl_key in links_by_platform:
                        results[our_key] = links_by_platform[sl_key]["url"]
        except Exception:
            pass
        return results

    @staticmethod
    def normalize_title(title: str) -> str:
        """Removes common suffixes that interfere with search matching."""
        # Ported logic from title_match_utils.go
        patterns = [
            r"\(Remastered.*?\)", r"\[Remastered.*?\]",
            r"\(Live.*?\)", r"\[Live.*?\]",
            r"\(Deluxe.*?\)", r"\[Deluxe.*?\]",
            r"\(Explicit.*?\)", r"\[Explicit.*?\]",
            r"- Remastered.*$", r"- Live.*$"
        ]
        lowered = title.lower()
        for p in patterns:
            lowered = re.sub(p, "", lowered, flags=re.IGNORECASE)
        return lowered.strip()

    def find_on_deezer_by_isrc(self, isrc: str) -> Optional[str]:
        """Calls Deezer API to find a track by its ISRC."""
        url = f"https://api.deezer.com/2.0/search?q=isrc:{isrc}"
        try:
            resp = self.session.get(url, timeout=10, verify=False)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("data", [])
                if items:
                    # Return the Deezer direct link
                    return items[0].get("link")
        except Exception:
            pass
        return None

# Global instance
resolver = SpotifyResolver()
