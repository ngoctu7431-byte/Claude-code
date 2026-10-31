@echo off
rem Tu tu chay: dan ma bot Telegram (khong hien chu), roi bam START voi bot. Dung 29/09/2026.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
"%~dp0.venv\Scripts\python.exe" "%~dp0tele.py" --cai
