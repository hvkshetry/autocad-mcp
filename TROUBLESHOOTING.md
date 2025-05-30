# AutoCAD MCP Troubleshooting Guide

This document provides solutions for common issues with the AutoCAD MCP implementation, including P&ID and CTO library specific problems.

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

### 2. Security Prompt Issues During LISP Loading

**Symptoms:**
- Security warning dialogs appear when loading LISP files
- Not enough time to click "Allow" or "Load" on security prompts
- LISP files fail to load due to cancelled security prompts

**Solutions:**

**Option 1: Add to Trusted Paths (Recommended)**
1. In AutoCAD, type `OPTIONS` and press Enter
2. Go to the **Files** tab
3. Expand **Trusted Locations**
4. Click **Add...** and browse to your `autocad-mcp\lisp-code` directory
5. Click **OK** to save
6. Restart AutoCAD

**Option 2: Use TRUSTEDPATHS Command**
1. In AutoCAD command line, type: `TRUSTEDPATHS`
2. Click **Add...**
3. Browse to and select your `autocad-mcp\lisp-code` directory
4. Click **OK**

**Option 3: Adjust Security Settings**
1. Set SECURELOAD system variable:
   - Type `SECURELOAD` in AutoCAD
   - Enter `0` to disable security prompts (not recommended for production)
   - Enter `1` to only load from trusted locations
   - Enter `2` to prompt for all locations (default)

**Option 4: Use Extended Delays**
- The server has been modified to wait 3 seconds after each LISP load
- You can increase this delay in `server_lisp.py` line 80 if needed

**Option 5: Manual Loading**
- Use `manual_load_lisp.bat` to load files one by one with unlimited time for prompts

### 3. AutoCAD Help Menu Opens During Execution

**Symptoms:**
- AutoCAD help window (F1) opens repeatedly during tool execution
- Help menu appears but doesn't stop the commands from working

**Cause:**
- The keyboard library might be sending key combinations that AutoCAD interprets as F1
- Rapid ESC key presses or timing issues with keyboard simulation

**Solutions:**
1. **Disable ESC key presses** (if they're not needed):
   - Edit `server_lisp.py` and change `USE_ESC_KEY = True` to `USE_ESC_KEY = False` on line 44
   
2. **Ensure clean AutoCAD state**:
   - Make sure no commands are active before running the server
   - Close any dialog boxes or tool palettes
   
3. **Check for keyboard shortcuts**:
   - Verify no custom keyboard shortcuts conflict with ESC key
   - Check if any AutoCAD plugins are intercepting keyboard input

### 4. LISP Script Execution Creates Text Instead of Running

**Symptoms:**
- Using `execute_lisp_script` pastes the script as text in the drawing
- Multi-line LISP code appears as text object instead of executing

**Cause:**
- AutoCAD might be in text input mode when clipboard paste occurs
- Multi-line clipboard content is interpreted as text input

**Solutions:**
1. **Use single-line scripts** when possible:
   - The tool automatically converts multi-line scripts to single line
   - Comments are removed and lines are joined
   
2. **Ensure clean command state**:
   - Make sure no text command is active
   - Press ESC before running scripts
   
3. **Use batch operation tools** instead:
   - `batch_create_lines()`, `batch_create_circles()`, etc.
   - These are optimized for multiple operations

### 5. Window Focus Issues

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

### 6. Attribute Handling Issues (New in v2.0)

**Symptoms:**
- Block attributes not updating properly
- "ATTRIB entity not found" errors
- Attribute values appear as defaults instead of specified values

**Solutions:**
1. **Check ATTREQ Setting**:
   - In AutoCAD, type `ATTREQ` and ensure it's set to 0 or 1
   - The server temporarily sets this to 0 during insertion

2. **Verify Block Definitions**:
   - Ensure the block has defined attributes with correct tag names
   - CTO blocks use specific attribute tags (EQUIPMENT-TYPE, MANUFACTURER, etc.)

3. **Manual Attribute Edit**:
   - If automatic update fails, use `edit_last_block_attribute` tool
   - Or manually use AutoCAD's ATTEDIT command

4. **Block Insertion Order**:
   - Always insert the block first, then update attributes
   - Don't try to modify attributes on non-existent blocks

### 7. Function Cancelled Errors

**Symptoms:**
- "Function cancelled" errors when loading LISP files
- LISP functions load but cannot be executed

**Solutions:**
- Check if the LISP file has dependencies that were not loaded
- Ensure the dependency order is correct (error_handling.lsp should load first)
- Try pressing ESC in AutoCAD several times to clear any pending commands
- Increase the delay times in the server script to give AutoCAD more processing time

### 4. CTO Library Issues (P&ID Functionality)

**Symptoms:**
- "File not found" errors when using P&ID tools
- "Block definition not found" errors
- P&ID symbols don't insert properly

**Solutions:**

**For Users WITH CTO Library:**
1. **Verify Installation Path**:
   - Ensure CTO library is installed at `C:\PIDv4-CTO\`
   - Check that subdirectories exist: VALVES, EQUIPMENT, PUMPS-BLOWERS, TANKS, etc.
   - Verify .dwg files exist in each subdirectory

2. **Check File Permissions**:
   - Ensure the CTO directory has read permissions
   - Try running AutoCAD as Administrator
   - Add `C:\PIDv4-CTO\` to AutoCAD trusted paths

3. **Path Configuration**:
   - If CTO is installed elsewhere, modify the paths in `pid_tools.lsp`
   - Update line 8: `(setq block-path (strcat "YOUR-PATH/" category "/" symbol-name ".dwg"))`

**For Users WITHOUT CTO Library:**
1. **Use Alternative Server**:
   - Switch to `server_lisp.py` instead of `server_lisp_fast.py`
   - Update Claude Desktop configuration to use the standard server

2. **Disable P&ID Tools**:
   - P&ID specific tools will return errors - this is expected
   - Use basic drawing tools instead: `create_circle`, `create_rectangle`, `create_text`

3. **Alternative Workflow**:
   ```
   Instead of: "Insert centrifugal pump P-101"
   Use: "Draw a circle at (100,100) and add text 'P-101 Pump' nearby"
   ```

### 5. Communication Issues

**Symptoms:**
- "AutoCAD LT window not found" errors
- Commands seem to be sent but not executed

**Solutions:**
- Make sure AutoCAD window title contains "AutoCAD" or "Drawing"
- Verify the AutoCAD window is not minimized
- Check if any dialog boxes or popups in AutoCAD need to be closed
- Try running the server script as Administrator

## Testing the Implementation

### Basic Functionality Test
1. Start AutoCAD and open a drawing
2. Make sure the AutoCAD window is visible and active (click on it once)
3. Run the appropriate server:
   - **With CTO Library**: `start_fast_server.bat`
   - **Without CTO Library**: `start_lisp_server.bat`
4. Test basic functionality:
   ```
   "Create a line from (0,0) to (100,100)"
   "Add a circle at (50,50) with radius 25"
   ```
5. Use `test_connection.bat` to run automated tests

### P&ID Functionality Test (CTO Library Only)
If you have the CTO library, test P&ID tools:
1. Run: `"Set up P&ID layers"`
2. Try: `"Insert a gate valve at (100,100)"`
3. Test: `"List available symbols in VALVES category"`

If these fail, you likely have CTO library path issues.

### Performance Test
For speed comparison:
1. Test individual operations: `"Create 5 circles at different locations"`
2. Test batch operations: Use `batch_create_circles` tool
3. Batch operations should be significantly faster (80%+ improvement)

## Manual Loading

If automatic loading fails, you can try loading the files manually in AutoCAD:

### Basic Files (Required for all functionality)
1. `(load "path/to/autocad-mcp/lisp-code/error_handling.lsp")`
2. `(load "path/to/autocad-mcp/lisp-code/basic_shapes.lsp")`
3. `(load "path/to/autocad-mcp/lisp-code/drafting_helpers.lsp")`

### P&ID Files (Only if you have CTO library)
4. `(load "path/to/autocad-mcp/lisp-code/pid_tools.lsp")`
5. `(load "path/to/autocad-mcp/lisp-code/attribute_tools.lsp")`

### Performance Files (Optional)
6. `(load "path/to/autocad-mcp/lisp-code/batch_operations.lsp")`

After loading, test:
- Basic: `(c:create-line 0 0 100 100)`
- P&ID: `(c:setup-pid-layers)` (if CTO library available)

## File Dependencies

The LISP files must be loaded in the following order due to dependencies:

### Core Files (Always Required)
1. error_handling.lsp
2. basic_shapes.lsp  
3. drafting_helpers.lsp

### Enhanced Functionality (Optional)
4. batch_operations.lsp (for performance)
5. advanced_geometry.lsp (for complex shapes)
6. advanced_entities.lsp (for rectangles, arcs)
7. annotation_helpers.lsp (for text and dimensions)
8. entity_modification.lsp (for entity manipulation)

### P&ID Functionality (CTO Library Required)
9. pid_tools.lsp (P&ID operations)
10. attribute_tools.lsp (block attribute handling)

### Legacy Files (Loaded by server_lisp.py only)
- block_id_helpers.lsp
- selection_and_file.lsp  
- layout_management.lsp

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

## Server Selection Guide

### Choose the Right Server for Your Setup

**Use `server_lisp_fast.py` if:**
- ✅ You have the CTO P&ID library installed
- ✅ You want maximum performance (80% faster)
- ✅ You plan to create P&ID drawings
- ✅ You need batch operations for complex drawings

**Use `server_lisp.py` if:**
- ❌ You don't have the CTO library
- ✅ You only need basic AutoCAD functionality
- ✅ You want maximum compatibility
- ✅ You're having issues with the fast server

### Configuration Examples

**Claude Desktop config for CTO users:**
```json
{
  "mcpServers": {
    "autocad-mcp": {
      "command": "path\\to\\venv\\Scripts\\python.exe",
      "args": ["path\\to\\server_lisp_fast.py"]
    }
  }
}
```

**Claude Desktop config for non-CTO users:**
```json
{
  "mcpServers": {
    "autocad-mcp": {
      "command": "path\\to\\venv\\Scripts\\python.exe",
      "args": ["path\\to\\server_lisp.py"]
    }
  }
}
```

## Last Resort Options

If all else fails:

1. Try using a different version of AutoCAD LT (2024 minimum required)
2. Use the basic server (`server_lisp.py`) without P&ID functionality
3. Check if other automation tools (like AutoHotkey) can successfully control AutoCAD
4. Create simple geometric shapes instead of using complex blocks
5. Restart both AutoCAD and the MCP server with all other applications closed
6. Disable antivirus temporarily to check for interference
7. Run both AutoCAD and MCP server as Administrator
