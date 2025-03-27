@echo off
echo ===================================
echo AutoCAD LT AutoLISP MCP Server
echo ===================================
echo 1. Ensure AutoCAD LT is running with a drawing open
echo 2. Make sure the AutoCAD window is visible and not minimized
echo 3. Click on the AutoCAD window once to ensure it's active
echo 4. Make sure the command line in AutoCAD is visible
echo 5. Press ESC a few times in AutoCAD to clear any active commands
echo 6. Run this script as Administrator
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
    echo Then run: venv\Scripts\pip install keyboard pywin32 pyperclip
    exit /b 1
)

echo ===================================
echo Starting the AutoLISP MCP Server for AutoCAD LT...
echo Loading LISP files in order: error_handling, basic_shapes, drafting_helpers, block_id_helpers, etc.
echo Make sure AutoCAD has the command line visible and is not busy with any other operations.
echo ===================================

python "%~dp0server_lisp.py"

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo ERROR: Server exited with code %ERRORLEVEL%
  echo.
  pause
)
