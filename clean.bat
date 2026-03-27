@echo off
title Lumina Music Cleaner
echo ==========================================
echo    DANG DON DEP DU AN Lumina Music...
echo ==========================================

if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
if exist core\__pycache__ rmdir /s /q core\__pycache__
if exist ui\__pycache__ rmdir /s /q ui\__pycache__

echo.
echo ==========================================
echo    DA DON DEP SACH SE!
echo ==========================================
pause
