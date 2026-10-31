@echo off
rem Routine misa-bh-sync goi file nay moi luot (GHI THAT). Dung 29/09/2026.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set OUT=%~dp0log\chay-routine-lan-cuoi.txt
echo ===== %DATE% %TIME% chay-routine %* > "%OUT%"
"%~dp0.venv\Scripts\python.exe" "%~dp0quet-bh-misa-len-erp.py" --tu-dong --that --bo-qua "C:\Claude Code\routines\misa-bh-sync-bo-qua.md" %* >> "%OUT%" 2>&1
set RC=%ERRORLEVEL%
type "%OUT%"
type "%OUT%" >> "%~dp0log\nhat-ky.txt"
rem Bao Telegram cho Tu (chi khi co chuyen dang bao; tin trung thi khong gui lai). Them 29/09/2026.
"%~dp0.venv\Scripts\python.exe" "%~dp0tele.py" --tu-log "%OUT%"
exit /b %RC%
