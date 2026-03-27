#!/bin/bash

# Lumina Music - Installer & Launcher for Linux/macOS
echo "======================================================"
echo "         Lumina Music - Lossless Downloader"
echo "======================================================"
echo ""

# 1. Kiem tra moi truong Python
if ! command -v python3 &> /dev/null
then
    echo "[!] Loi: Chua tim thay Python 3. Vui long cai dat Python 3.10+ truoc."
    exit 1
fi

# 2. Tao venv (Khuyen khich tren Linux/macOS)
if [ ! -d "venv" ]; then
    echo "[2] Dang tao moi truong ao (venv)..."
    python3 -m venv venv
fi

source venv/bin/activate

# 3. Cai dat cac thu vien
echo "[3] Dang cai dat cac thu vien can thiet..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "[!] Loi khi cai dat requirements. Vui long kiem tra ket noi mang."
    exit 1
fi

# 4. Khoi chay
echo "[4] Dang khoi chay Lumina Music..."
python3 main.py

echo ""
echo "======================================================"
echo "    Chuc ban co nhung giay phut nghe nhac tuyet voi!"
echo "======================================================"
