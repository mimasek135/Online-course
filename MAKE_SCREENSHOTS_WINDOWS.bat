@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe goto missing
.venv\Scripts\python.exe -m pip install -r requirements-screenshots.txt
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m playwright install chromium
if errorlevel 1 goto fail
.venv\Scripts\python.exe scripts\capture_screenshots.py
if errorlevel 1 goto fail
echo Screenshots are ready in the screenshots folder.
explorer screenshots
pause
exit /b
:missing
echo Run START_WINDOWS.bat first and leave the server running.
pause
exit /b 1
:fail
echo Capture failed. Leave START_WINDOWS.bat running and check the error above.
pause
exit /b 1
