# AutoCAD MCP Troubleshooting Guide

This document provides solutions for common issues with the AutoCAD MCP implementation.

## Common Issues and Solutions

### 1. LISP Files Fail to Load

**Symptoms:**
- Errors like "LOAD failed" or "Function cancelled"
- Only some functions work but others do not

**Solutions:**
- Ensure AutoCAD is running and has a drawing open
- Make sure the command line in AutoCAD is visible and not hidden
- Check that AutoCAD is not in the middle of another command
- Verify file paths are correct (using absolute paths with forward slashes)
- Try loading files manually in AutoCAD to check for syntax errors

### 2. Window Focus Issues

**Symptoms:**
- Window focus errors like "SetForegroundWindow timed out"
- Commands not being sent to AutoCAD
- AutoCAD window is not responding to commands

**Solutions:**
- Make sure AutoCAD is not minimized and is visible on screen
- Click on the AutoCAD window manually to ensure it's active before starting the server
- Try running both AutoCAD and the server as Administrator
- Close any dialog boxes or popups in AutoCAD
- Make sure no command is currently active in AutoCAD (press ESC multiple times)
- On Windows 10/11, try disabling the "Focus Assist" feature which can block window focus changes
- Try setting AutoCAD as the foreground window manually before starting the server

### 3. Function Cancelled Errors

**Symptoms:**
- "Function cancelled" errors when loading LISP files
- LISP functions load but cannot be executed

**Solutions:**
- Check if the LISP file has dependencies that were not loaded
- Ensure the dependency order is correct (error_handling.lsp should load first)
- Try pressing ESC in AutoCAD several times to clear any pending commands
- Increase the delay times in the server script to give AutoCAD more processing time

### 4. Communication Issues

**Symptoms:**
- "AutoCAD LT window not found" errors
- Commands seem to be sent but not executed

**Solutions:**
- Make sure AutoCAD window title contains "AutoCAD" or "Drawing"
- Verify the AutoCAD window is not minimized
- Check if any dialog boxes or popups in AutoCAD need to be closed
- Try running the server script as Administrator

## Testing the Implementation

To verify that the implementation is working correctly:

1. Start AutoCAD and open a drawing
2. Make sure the AutoCAD window is visible and active (click on it once)
3. Run the MCP server using `start_lisp_server.bat`
4. Use the `run_test` tool to perform a basic functionality test
5. If the test fails, check the AutoCAD command line for specific error messages
6. You can also use the `test_connection.bat` script to run a simple line creation test

## Manual Loading

If automatic loading fails, you can try loading the files manually in AutoCAD:

1. In AutoCAD, type `(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/error_handling.lsp")` and press Enter
2. Check for any errors in the command line
3. Continue with other files in the correct dependency order
4. After loading all files, test a simple function like `(c:create-line 0 0 100 100)`

## File Dependencies

The LISP files must be loaded in the following order due to dependencies:

1. error_handling.lsp
2. basic_shapes.lsp
3. drafting_helpers.lsp
4. block_id_helpers.lsp
5. selection_and_file.lsp
6. advanced_geometry.lsp
7. annotation_helpers.lsp
8. layout_management.lsp

## Advanced Troubleshooting

If problems persist:

1. Try creating a new, empty LISP file with a simple function and test loading it
2. Enable more verbose logging in the server script
3. Check AutoCAD's security settings - it may be blocking the execution of external LISP files
4. Consider running AutoCAD as Administrator to avoid permission issues
5. Try disabling any antivirus or security software that might be blocking the communication

## Debugging Window Focus Issues

Window focus issues are common with AutoCAD automation. Here are additional steps to debug:

1. **Check process isolation**: Windows may prevent one application from controlling another for security reasons
2. **Try UI Automation API**: If keyboard input fails, try alternative automation methods
3. **Test with simple commands**: Use `(princ "TEST")` in AutoCAD to check if basic communication works
4. **Verify keyboard input isn't blocked**: Some system settings or applications can block programmatic keyboard input
5. **Check if AutoCAD is in modal dialog mode**: If AutoCAD is waiting for input from a dialog, it won't accept commands

## Last Resort Options

If all else fails:

1. Try using a different version of AutoCAD
2. Create a simplified version of the MCP server that only has basic functionality
3. Check if other automation tools (like AutoHotkey) can successfully control AutoCAD
4. Consider using AutoCAD's COM interface instead of keyboard simulation
5. Restart both AutoCAD and the MCP server with all other applications closed
