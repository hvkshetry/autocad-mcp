@echo off
echo ===================================
echo AutoCAD MCP Test Script
echo ===================================
echo This script sends a simple command to test if the MCP server
echo is correctly connected to AutoCAD.
echo.
echo IMPORTANT: Make sure the server is already running!
echo ===================================
echo.

set /p confirm=Press ENTER to run the test or CTRL+C to cancel...

echo.
echo Sending test command to create a line from (0,0) to (100,100)...
echo.

REM Simple JSON payload for the create_line tool
echo {"tool":"create_line","parameters":{"start_x":0,"start_y":0,"end_x":100,"end_y":100}} | curl -X POST http://localhost:8000 -H "Content-Type: application/json" -d @-

echo.
echo Test complete. Check AutoCAD to see if a line was created.
echo If you see a line, the MCP server is working correctly!
echo.
pause
