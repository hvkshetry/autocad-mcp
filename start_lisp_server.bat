@echo off
echo ===================================
echo AutoCAD LT MCP Server - BASIC MODE
echo ===================================
echo This version provides standard functionality without CTO library
echo - All basic drawing operations
echo - Block insertion and management
echo - Layer control and dimensions
echo - NO P&ID specific tools
echo ===================================
echo.
echo 1. Ensure AutoCAD LT 2024+ is running with a drawing open
echo 2. Window title should include "AutoCAD" or drawing name (.dwg)
echo 3. Use start_fast_server.bat if you have CTO library installed
echo ===================================

cd /d "%~dp0"
echo Current directory: %CD%

if not exist venv\Lib\site-packages\mcp (
    echo Installing required packages...
    call venv\Scripts\pip install -r requirements.txt
)

if exist venv\Scripts\activate (
    call venv\Scripts\activate
    echo Virtual environment activated
) else (
    echo Virtual environment not found. Please run: python -m venv venv
    exit /b 1
)

echo Starting the Basic AutoCAD MCP Server (no P&ID tools)...
python "%~dp0server_lisp.py"

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo ERROR: Server exited with code %ERRORLEVEL%
  pause
)
