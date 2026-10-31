@echo off
rem Gui mot tin Telegram cho Tu: gui-tele.cmd "noi dung". Dung 29/09/2026.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
"%~dp0.venv\Scripts\python.exe" "%~dp0tele.py" %*
