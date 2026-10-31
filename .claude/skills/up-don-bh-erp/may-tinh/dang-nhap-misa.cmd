@echo off
rem Mo cua so Chrome rieng de Tu dang nhap MISA. Chay tach rieng, khong bat routine phai cho. Dung 29/09/2026.
rem Tu dang nhap xong thi DONG cua so do. Script khong giu mat khau, chi giu phien.
tasklist /v /fi "imagename eq python.exe" | findstr /i /c:"Dang nhap MISA" >nul && exit /b 0
start "Dang nhap MISA" /min "%~dp0.venv\Scripts\python.exe" "%~dp0quet-bh-misa-len-erp.py" --dang-nhap
echo Da mo cua so dang nhap MISA.
exit /b 0
