@echo off
echo ===================================
echo AutoCAD LT MCP Server - FAST MODE
echo ===================================
echo This version prioritizes speed over reliability
echo - Minimal delays between commands
echo - Batch operations support
echo - Fast initialization (essential files only)
echo ===================================
echo.
echo 1. Ensure AutoCAD LT is running with a drawing open
echo 2. Add lisp-code folder to AutoCAD trusted paths for best performance
echo 3. Close unnecessary applications
echo ===================================

cd /d "%~dp0"

if exist venv\Scripts\activate (
    call venv\Scripts\activate
    echo Virtual environment activated
) else (
    echo Virtual environment not found. Please run: python -m venv venv
    exit /b 1
)

echo Starting the Fast AutoLISP MCP Server...
python "%~dp0server_lisp_fast.py"

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo ERROR: Server exited with code %ERRORLEVEL%
  pause
)