@echo off
rem CHI DOC. Doi chieu don ERP voi BH tren MISA 10 ngay gan nhat. Dung 29/09/2026.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set OUT=%~dp0log\doi-chieu-lan-cuoi.txt
echo ===== %DATE% %TIME% doi-chieu %* > "%OUT%"
"%~dp0.venv\Scripts\python.exe" "%~dp0doi-chieu-erp-misa.py" %* >> "%OUT%" 2>&1
set RC=%ERRORLEVEL%
type "%OUT%"
type "%OUT%" >> "%~dp0log\nhat-ky.txt"
exit /b %RC%
