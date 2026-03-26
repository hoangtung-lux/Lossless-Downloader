@echo off
title SpotiFLAC Builder (Fix Extraction Error)
echo ==========================================
echo    DANG DONG GOI SPOTIFLAC CLONE...
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
    --add-data "icon.ico;." ^
    --icon icon.ico ^
    --name "SpotiFLAC-Clone" ^
    main.py

echo.
echo ==========================================
echo    THANH CONG! Neu van loi, hay thu run as Admin
echo    hoac tam tat Antivirus khi mo App lan dau.
echo ==========================================
pause
