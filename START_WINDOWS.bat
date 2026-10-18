@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -m venv .venv
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto fail
.venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto fail
.venv\Scripts\python.exe manage.py seed_demo
if errorlevel 1 goto fail
echo.
echo Save the generated admin password printed above.
echo Site: http://127.0.0.1:8000/
echo Admin: http://127.0.0.1:8000/admin/
echo Press Ctrl+C to stop the server.
.venv\Scripts\python.exe manage.py runserver
pause
exit /b
:fail
echo Setup failed. Check the message above. Python 3.12+ and internet are required.
pause
exit /b 1
