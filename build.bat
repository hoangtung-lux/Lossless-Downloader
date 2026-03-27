@echo off
title Lumina Music Builder (Fix Extraction Error)
echo ==========================================
echo    DANG DONG GOI Lumina Music Downloader...
echo    (Su dung cac co fix loi giai nen)
echo ==========================================

:: Xoa cac thu muc build cu
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: Chay PyInstaller với các cờ bổ sung để fix lỗi Cryptodome
.\venv\Scripts\pyinstaller --noconsole ^
    --onefile ^
    --noupx ^
    --collect-all Cryptodome ^
    --add-data "bin;bin" ^
    --add-data "assets\app_icon.ico;." ^
    --icon "assets\app_icon.ico" ^
    --name "Lumina Music-Downloader" ^
    main.py

echo.
echo ==========================================
echo    THANH CONG! Neu van loi, hay thu run as Admin
echo    hoac tam tat Antivirus khi mo App lan dau.
echo ==========================================
