@echo off
rem Routine misa-bh-sync goi file nay moi luot (Buoc 1c): thu lai BH thieu ma/khach khi ERP da bo sung. Dung 03/10/2026.
rem KHONG kem tham so - de khop dung quyen da cho phep san.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set OUT=%~dp0log\thu-lai-thieu-ma-lan-cuoi.txt
echo ===== %DATE% %TIME% thu-lai-thieu-ma > "%OUT%"
"%~dp0.venv\Scripts\python.exe" "%~dp0thu-lai-thieu-ma.py" >> "%OUT%" 2>&1
set RC=%ERRORLEVEL%
type "%OUT%"
type "%OUT%" >> "%~dp0log\nhat-ky.txt"
exit /b %RC%
