@echo off
rem Chay thu CHI XEM, khong ghi gi len ERP. Dung 29/09/2026.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set OUT=%~dp0log\xem-thu-lan-cuoi.txt
echo ===== %DATE% %TIME% xem-thu %* > "%OUT%"
"%~dp0.venv\Scripts\python.exe" "%~dp0quet-bh-misa-len-erp.py" --tu-dong --bo-qua "C:\Claude Code\routines\misa-bh-sync-bo-qua.md" %* >> "%OUT%" 2>&1
set RC=%ERRORLEVEL%
type "%OUT%"
type "%OUT%" >> "%~dp0log\nhat-ky.txt"
exit /b %RC%
