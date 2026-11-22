@echo off
rem Windows: double-click this file to install the skill from a menu.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
echo.
pause
