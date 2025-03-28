@echo off
echo ===================================
echo AutoCAD LT AutoLISP MCP Server
echo ===================================
echo 1. Ensure AutoCAD LT is running with a drawing open
echo 2. Window title should include "AutoCAD LT" and "Drawing"
echo 3. Run as Administrator if needed
echo ===================================

cd /d "%~dp0"
echo Current directory: %CD%

if not exist venv\Lib\site-packages\keyboard (
    echo Installing required packages...
    call venv\Scripts\pip install keyboard pyperclip pywin32
)

if exist venv\Scripts\activate (
    call venv\Scripts\activate
    echo Virtual environment activated
) else (
    echo Virtual environment not found. Please run: python -m venv venv
    exit /b 1
)

echo Starting the AutoLISP MCP Server for AutoCAD LT...
python "%~dp0server_lisp.py"

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo ERROR: Server exited with code %ERRORLEVEL%
  pause
)
