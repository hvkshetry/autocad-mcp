@echo off
echo ===================================
echo AutoCAD LT AutoLISP MCP Server
echo ===================================
echo IMPORTANT STEPS:
echo 1. Make sure AutoCAD LT is running with a drawing open
echo 2. The drawing window title should include "AutoCAD LT" and "Drawing"
echo 3. Run this script as Administrator
echo 4. The server will send AutoLISP commands to AutoCAD
echo ===================================
echo.
echo NOTE: This server requires AutoCAD LT 2024 or later with AutoLISP support.
echo.
echo ===================================

:: Change to the directory where this batch file is located
cd /d "%~dp0"
echo Current directory: %CD%

:: Check for necessary packages
if not exist venv\Lib\site-packages\keyboard (
    echo Installing required packages...
    echo This may take a minute...
    call venv\Scripts\pip install keyboard pyperclip pywin32
)

:: Activate virtual environment
if exist venv\Scripts\activate (
    call venv\Scripts\activate
    echo Virtual environment activated
) else (
    echo Virtual environment not found. Please run: python -m venv venv
    echo Then run: venv\Scripts\pip install keyboard pyperclip pywin32
    exit /b 1
)

echo Starting AutoLISP MCP Server for AutoCAD LT...
echo.
echo NOTE: This server will send AutoLISP commands to AutoCAD.
echo You can press CTRL+C to stop the server at any time.
echo.
python "%~dp0server_lisp.py"

:: Keep window open on error
if %ERRORLEVEL% NEQ 0 (
  echo.
  echo ERROR: Server exited with code %ERRORLEVEL%
  echo.
  echo Troubleshooting tips:
  echo - Make sure AutoCAD LT is running with an active drawing
  echo - The window title should contain "AutoCAD LT" and "Drawing"
  echo - Make sure you're using AutoCAD LT 2024 or later with AutoLISP support
  echo - Run this script as Administrator
  echo.
  pause
)
