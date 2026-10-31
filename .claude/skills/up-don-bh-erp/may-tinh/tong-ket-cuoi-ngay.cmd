@echo off
rem Routine misa-bh-sync goi file nay (Buoc 5, tu 17:00): tu dem, gui Telegram tong ket, ghi moc. Dung 06/10/2026.
rem KHONG kem tham so - de khop dung quyen da cho phep san.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
"%~dp0.venv\Scripts\python.exe" "%~dp0tong-ket-cuoi-ngay.py"
