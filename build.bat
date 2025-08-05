@echo off
REM Clean previous build and dist folders, if they exist
rmdir /s /q dist
rmdir /s /q build

pyinstaller --clean --name=VencordLauncher --icon=icon.ico main.py

REM Copy config.json next to the executable
copy config.json dist\VencordLauncher\config.json

echo.
echo Done! The EXE and config.json are now in dist\VencordLauncher\
pause
