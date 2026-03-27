@echo off
title Lumina Music - Installer & Launcher
echo ======================================================
echo          Lumina Music - Lossless Downloader
echo ======================================================
echo.
echo [1] Dang kiem tra moi truong Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Loi: Chua tim thay Python. Vui long cai dat Python 3.10+ truoc.
    pause
    exit /b
)

echo [2] Dang cai dat cac thu vien can thiet...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [!] Loi khi cai dat requirements. Vui long kiem tra ket noi mang.
    pause
    exit /b
)

echo [3] Dang khoi chay Lumina Music...
start /b python main.py
echo.
echo ======================================================
echo     Chuc ban co nhung giay phut nghe nhac tuyet voi!
echo ======================================================
timeout /t 5 >nul
exit
