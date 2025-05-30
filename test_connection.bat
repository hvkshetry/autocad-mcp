@echo off
echo ===================================
echo AutoCAD MCP Connection Test
echo ===================================
echo This script tests the MCP server connection by:
echo 1. Creating a simple line
echo 2. Adding a circle
echo 3. Inserting text
echo.
echo IMPORTANT: 
echo - AutoCAD LT must be running with a drawing open
echo - The MCP server must be running in Claude Desktop
echo - You must use Claude Desktop to run this test
echo ===================================
echo.

echo To test the connection, copy and paste these commands in Claude:
echo.
echo Test 1: "Create a line from (0,0) to (100,100)"
echo Test 2: "Add a circle at (50,50) with radius 25"
echo Test 3: "Add text 'MCP Test Success' at position (25,75)"
echo.
echo If you have CTO library installed, also try:
echo Test 4: "Set up P&ID layers"
echo Test 5: "List available symbols in VALVES category"
echo.
echo ===================================
echo Alternative: Manual LISP Test
echo ===================================
echo You can also test directly in AutoCAD command line:
echo.
echo Type: (c:create-line 0 0 100 100)
echo.
echo If this creates a line, the LISP files are loaded correctly.
echo If you get "Unknown command", the server needs to be restarted.
echo.
pause