@echo off
REM ----------------------------
REM Lösche alte Build-Ordner
REM ----------------------------
if exist "dist" (
    echo Entferne dist-Ordner...
    rmdir /s /q "dist"
)

if exist "build" (
    echo Entferne build-Ordner...
    rmdir /s /q "build"
)

REM ----------------------------
REM PyInstaller Build
REM ----------------------------
echo Starte PyInstaller...

pyinstaller --name app_desktop --clean --onefile --add-data "streamlit_app;streamlit_app" --add-data ".streamlit;.streamlit" app_desktop.py

pause
