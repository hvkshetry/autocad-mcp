@echo off
echo ===================================
echo Direct AutoCAD LISP Function Test
echo ===================================
echo This script tests if LISP functions are loaded correctly
echo by sending commands directly to AutoCAD.
echo.
echo REQUIREMENTS:
echo - AutoCAD LT 2024+ must be running with a drawing open
echo - Run one of the server scripts first (start_lisp_server.bat or start_fast_server.bat)
echo - Wait for "initialization complete" message before running this test
echo ===================================
echo.

cd /d "%~dp0"

if not exist venv\Scripts\python.exe (
    echo ERROR: Virtual environment not found.
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo Creating test script...
call venv\Scripts\python -c "import pyperclip; pyperclip.copy('(progn (c:create-line 0 0 100 100) (c:create-circle 50 50 25) (c:create-text 25 75 \"TEST-SUCCESS\" 5) (princ \"\\nTest completed - check for line, circle, and text\"))')"

echo.
echo Test command copied to clipboard!
echo.
echo INSTRUCTIONS:
echo 1. Click on the AutoCAD window to make it active
echo 2. Click in the command line area
echo 3. Press Ctrl+V to paste the test command
echo 4. Press Enter to run the test
echo.
echo You should see:
echo - A line from (0,0) to (100,100)
echo - A circle at (50,50) with radius 25
echo - Text saying "TEST-SUCCESS" at (25,75)
echo.
echo If these appear, the basic LISP functions are working correctly!
echo.
pause