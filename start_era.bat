
@echo off
title ERA - Debug Mode
cd /d "%~dp0"

echo.
echo ===== ERA DEBUG MODE =====
echo Project folder: %CD%
echo.

"%~dp0env\Scripts\python.exe" -u main.py

echo.
echo ===== ERA STOPPED =====
pause
