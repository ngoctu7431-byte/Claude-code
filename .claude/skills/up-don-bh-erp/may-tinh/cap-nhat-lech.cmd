@echo off
rem Routine misa-bh-sync goi file nay moi luot (SUA THAT). Ra BH ke toan sua sau khi up, sua SO cho khop. Dung 29/09/2026.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set OUT=%~dp0log\cap-nhat-lech-lan-cuoi.txt
echo ===== %DATE% %TIME% cap-nhat-lech %* > "%OUT%"
"%~dp0.venv\Scripts\python.exe" "%~dp0cap-nhat-lech-bh.py" --that %* >> "%OUT%" 2>&1
set RC=%ERRORLEVEL%
type "%OUT%"
type "%OUT%" >> "%~dp0log\nhat-ky.txt"
rem Bao Telegram cho Tu (tin trung thi khong gui lai). Them 29/09/2026.
"%~dp0.venv\Scripts\python.exe" "%~dp0tele.py" --tu-log "%OUT%"
exit /b %RC%
