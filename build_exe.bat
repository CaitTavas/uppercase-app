@echo off
echo ============================================
echo   UPPERCASE Tool - EXE Builder
echo ============================================
echo.

@echo off
python -m PyInstaller --noconfirm --onefile --windowed --name "UPPERCASE Tool" main.py
echo Done! Find your .exe in dist/
pause