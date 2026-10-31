@echo off
rem Ghi ngay hom nay (yyyy-mm-dd) vao log\bao-cuoi-ngay.txt sau khi gui tong ket cuoi ngay. Dung 03/10/2026.
rem Ly do: phien nen dung tool Write/Edit sua file nay bi hoi quyen, dung cho ca toi (01/10 va 02/10/2026).
"%~dp0.venv\Scripts\python.exe" -c "import datetime,pathlib; p=pathlib.Path(r'%~dp0log\bao-cuoi-ngay.txt'); p.write_text(datetime.date.today().isoformat()+'\n', encoding='utf-8'); print('Da ghi', p.read_text().strip())"
