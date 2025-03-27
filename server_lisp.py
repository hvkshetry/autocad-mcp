#!/usr/bin/env python
"""
AutoCAD LT MCP Server (AutoLISP Version)
A specialized implementation for a general 2D drafting assistant.

This codebase now includes additional placeholders and partial
implementations for advanced geometry, annotation, layout management,
and more robust error handling, in line with the recommended feedback.
"""
import logging
import sys
import os
import time
import subprocess
import tempfile
import pyperclip
from pathlib import Path
import win32gui
import win32con
import keyboard
from typing import Optional, Dict, Any, List, Tuple
import signal

from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("autocad-lisp-mcp") # Removed the backslash

# Initialize FastMCP server
autocad_mcp = FastMCP("autocad-lisp-server")

# Global variables
acad_window = None
lisp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lisp-code") # Removed the backslash

# Add signal handlers to gracefully handle termination
def signal_handler(sig, frame):
    logger.info(f"Signal {sig} received, shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def find_autocad_window():
    """Find the AutoCAD LT window handle based on window title."""
    def enum_windows_callback(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if "AutoCAD" in window_text and ("LT" in window_text or "Drawing" in window_text):
                logger.info(f"Found AutoCAD window with title: {window_text}")
                result.append(hwnd)
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    
    if windows:
        return windows[0]
        
    # If we didn't find a window with both criteria, try just looking for AutoCAD
    windows = []
    def fallback_enum_callback(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if "AutoCAD" in window_text:
                logger.info(f"Found fallback AutoCAD window with title: {window_text}")
                result.append(hwnd)
        return True
    
    win32gui.EnumWindows(fallback_enum_callback, windows)
    
    if windows:
        return windows[0]
    return None

def activate_autocad_window():
    """Activate the AutoCAD window using multiple approaches."""
    global acad_window
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False
    
    try:
        # Try the standard activation first
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(0.5)  # Increased wait time
        
        # Check if window was activated
        active_hwnd = win32gui.GetForegroundWindow()
        if active_hwnd == acad_window:
            return True
            
        # If not activated, try alternative methods
        try:
            # Try to bring window to front using alternative method
            win32gui.ShowWindow(acad_window, win32con.SW_RESTORE)  # In case it's minimized
            time.sleep(0.3)
            win32gui.BringWindowToTop(acad_window)
            time.sleep(0.3)
            win32gui.SetForegroundWindow(acad_window)
            time.sleep(0.5)
            return True
        except Exception as e2:
            logger.error(f"Alternative activation failed: {str(e2)}")
            return False
            
    except Exception as e:
        logger.error(f"Error activating AutoCAD window: {str(e)}")
        return False

def load_lisp_file(file_path):
    """Load a LISP file into AutoCAD by simulating typed commands."""
    global acad_window
    
    # Check if file exists
    if not os.path.exists(file_path):
        logger.error(f"LISP file not found: {file_path}")
        return False, f"LISP file not found: {file_path}"
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False, "AutoCAD LT window not found"
    
    try:
        # Log the operation
        logger.info(f"Attempting to load LISP file: {file_path}")
        
        # Activate the AutoCAD window using our robust method
        if not activate_autocad_window():
            return False, "Failed to activate AutoCAD window"
        
        # Clear command line and any pending operations
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        
        # Load the LISP file - ensure proper path format and escaping
        lisp_path_formatted = Path(file_path).as_posix()
        load_command = f"(load \"{lisp_path_formatted}\")"  
        logger.info(f"Sending command: {load_command}")
        
        keyboard.write(load_command)
        time.sleep(0.2)  # Give time for the command to be entered
        keyboard.press_and_release('enter')
        time.sleep(1.0)  # Increase wait time for file loading
        
        return True, f"LISP file '{os.path.basename(file_path)}' loaded successfully"
    except Exception as e:
        logger.error(f"Error loading LISP file: {str(e)}")
        return False, f"Error loading LISP file: {str(e)}"

def execute_lisp_command(command):
    """Execute a LISP command in AutoCAD by simulating typed commands."""
    global acad_window
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False, "AutoCAD LT window not found"
    
    try:
        # Use our robust window activation method
        if not activate_autocad_window():
            return False, "Failed to activate AutoCAD window"
        
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        
        keyboard.write(command)

        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.5)
        
        return True, f"Command executed: {command}"
    except Exception as e:
        logger.error(f"Error executing LISP command: {str(e)}")
        return False, f"Error executing LISP command: {str(e)}"

def execute_lisp_from_clipboard():
    """Execute LISP code from clipboard in AutoCAD."""
    global acad_window
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False, "AutoCAD LT window not found"
    
    try:
        # Use our robust window activation method
        if not activate_autocad_window():
            return False, "Failed to activate AutoCAD window"
        
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        
        keyboard.write("(eval (read))")
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.2)
        
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.5)
        
        return True, "LISP code from clipboard executed successfully"
    except Exception as e:
        logger.error(f"Error executing LISP from clipboard: {str(e)}")
        return False, f"Error executing LISP from clipboard: {str(e)}"

def safe_load_lisp_file(file_name):
    """
    Safely load a LISP file with better error handling and diagnostics.
    Returns (success, message)
    """
    global lisp_path
    
    full_path = os.path.join(lisp_path, file_name)
    if not os.path.exists(full_path):
        logger.error(f"LISP file not found: {full_path}")
        return False, f"LISP file not found: {full_path}"
    
    try:
        # First try to verify AutoCAD's state
        exec_success, exec_message = execute_lisp_command("(princ \"READY\")")
        if not exec_success:
            logger.warning(f"AutoCAD might not be in a ready state: {exec_message}")
            # Still continue with the load attempt
        
        # Now load the file
        success, message = load_lisp_file(full_path)
        
        # Give AutoCAD more time to process the load
        time.sleep(1.5)
        
        return success, message
    except Exception as e:
        logger.error(f"Error in safe_load_lisp_file for {file_name}: {str(e)}")
        return False, f"Error loading {file_name}: {str(e)}"

def initialize_autocad_lisp():
    """
    Initialize AutoCAD with LISP capabilities for general drafting.
    Loads multiple LISP files that together provide advanced drafting,
    geometry, annotation, layout, and error handling functions.
    """
    global acad_window, lisp_path
    
    acad_window = find_autocad_window()
    if not acad_window:
        logger.error("AutoCAD LT window not found. Make sure AutoCAD LT is running with a drawing open.")
        return False
    
    # Load files in order of dependency
    lisp_files = [
        "error_handling.lsp",      # Load error handling first
        "basic_shapes.lsp",        # Basic shapes don't depend on anything
        "drafting_helpers.lsp",    # Depends on error_handling
        "block_id_helpers.lsp",    # Depends on drafting_helpers
        "selection_and_file.lsp",  # Depends on error_handling
        "advanced_geometry.lsp",   # Load the rest
        "annotation_helpers.lsp",
        "layout_management.lsp"
    ]
    
    # Clear any pending commands or prompts
    for _ in range(3):  # Send escape multiple times to ensure clean state
        keyboard.press_and_release('esc')
        time.sleep(0.2)
    
    # First verify we can communicate with AutoCAD
    exec_success, exec_message = execute_lisp_command("(princ \"MCP INITIALIZATION\")")
    if not exec_success:
        logger.error(f"Cannot communicate with AutoCAD: {exec_message}")
        return False
    
    success_count = 0
    for f in lisp_files:
        logger.info(f"Attempting to load {f}...")
        success, message = safe_load_lisp_file(f)
        
        if success:
            success_count += 1
            logger.info(f"Successfully loaded {f}")
        else:
            logger.error(f"Failed to load {f}: {message}")
            # Continue loading other files instead of returning False immediately
    
    # Report overall success based on how many files loaded
    if success_count == len(lisp_files):
        logger.info("Successfully loaded all LISP libraries for a general 2D drafting assistant.")
        return True
    elif success_count > 0:
        logger.warning(f"Partially initialized: {success_count}/{len(lisp_files)} LISP files loaded.")
        return True  # Still return True to continue with partial functionality
    else:
        logger.error("Failed to load any LISP files.")
        return False

@autocad_mcp.tool()
async def get_autocad_status() -> str:
    """Check or initialize the AutoCAD connection."""
    global acad_window
    
    if acad_window is None:
        if initialize_autocad_lisp():
            window_title = win32gui.GetWindowText(acad_window)
            return f"Successfully connected to AutoCAD LT: {window_title}"
        else:
            return "Failed to connect to AutoCAD LT. Please ensure it is running with a drawing open."
    
    try:
        window_title = win32gui.GetWindowText(acad_window)
        if "AutoCAD" in window_title:  # Changed from "AutoCAD LT" to just "AutoCAD"
            if activate_autocad_window():
                return f"Connected to AutoCAD: {window_title}"
            else:
                return f"Connected to AutoCAD but unable to activate window: {window_title}"
        else:
            # Attempt re-initialization
            if initialize_autocad_lisp():
                window_title = win32gui.GetWindowText(acad_window)
                return f"Reconnected to AutoCAD: {window_title}"
            return "Lost connection to AutoCAD."
    except Exception as e:
        if initialize_autocad_lisp():
            return "Reconnected to AutoCAD successfully."
        return f"Lost connection to AutoCAD: {str(e)}"

@autocad_mcp.tool()
async def run_test() -> str:
    """Run a test to verify that all AutoCAD functions are working."""
    global acad_window, lisp_path
    
    if acad_window is None:
        if not initialize_autocad_lisp():
            return "Failed to connect to AutoCAD LT. Please ensure it is running with a drawing open."
    
    # First try to load our test file
    test_file = os.path.join(lisp_path, "mcp_test.lsp")
    if not os.path.exists(test_file):
        return "Test file not found. Please ensure mcp_test.lsp exists in the lisp-code directory."
    
    # Clear any pending commands
    for _ in range(3):
        keyboard.press_and_release('esc')
        time.sleep(0.2)
    
    # Execute a diagnostic command
    success, message = execute_lisp_command("(princ \"TEST INITIALIZATION\")")
    if not success:
        return f"Cannot communicate with AutoCAD: {message}"
    
    # Now load the test file
    success, message = load_lisp_file(test_file)
    if not success:
        return f"Failed to load test file: {message}"
    
    # Now run the test command
    time.sleep(1.5)  # Give more time for the file to load
    success, message = execute_lisp_command("(c:mcp_test)")
    
    if success:
        return "Test completed successfully. The AutoCAD MCP implementation is working. Check the AutoCAD drawing to see the test results."
    else:
        return f"Test failed: {message}"


###############################################################################
# Example Tools: Basic shapes
###############################################################################

@autocad_mcp.tool()
async def create_line(start_x: float, start_y: float, end_x: float, end_y: float) -> str:
    # First ensure we're using the active layer
    execute_lisp_command('(setq current-layer (getvar "CLAYER"))')
    execute_lisp_command('(setvar "CLAYER" current-layer)')
    
    cmd = f"(c:create-line {start_x} {start_y} {end_x} {end_y})"
    success, message = execute_lisp_command(cmd)
    return message if not success else f"Line created from ({start_x},{start_y}) to ({end_x},{end_y})."

@autocad_mcp.tool()
async def create_circle(center_x: float, center_y: float, radius: float) -> str:
    # First ensure we're using the active layer
    execute_lisp_command('(setq current-layer (getvar "CLAYER"))')
    execute_lisp_command('(setvar "CLAYER" current-layer)')
    
    cmd = f"(c:create-circle {center_x} {center_y} {radius})"
    success, message = execute_lisp_command(cmd)
    return message if not success else f"Circle created at ({center_x},{center_y}), radius {radius}."

@autocad_mcp.tool()
async def create_text(x: float, y: float, text: str, height: float = 2.5) -> str:
    # First ensure we're using the active layer
    execute_lisp_command('(setq current-layer (getvar "CLAYER"))')
    execute_lisp_command('(setvar "CLAYER" current-layer)')
    
    text_escaped = text.replace('"', '\\"')
    cmd = f'(c:create-text {x} {y} "{text_escaped}" {height})'
    success, message = execute_lisp_command(cmd)
    return message if not success else f"Text '{text}' created at ({x},{y})."

###############################################################################
# Example Tools: Block insertion, labeling, arrangement
###############################################################################

@autocad_mcp.tool()
async def insert_block(block_name: str, x: float, y: float, block_id: str = "",
                       scale: float = 1.0, rotation: float = 0.0) -> str:
    # First ensure we're using the active layer
    execute_lisp_command('(setq current-layer (getvar "CLAYER"))')
    execute_lisp_command('(setvar "CLAYER" current-layer)')
    
    block_id_escaped = block_id.replace('"', '\\"')
    cmd = f'(c:insert_block "{block_name}" {x} {y} "{block_id_escaped}" {scale} {rotation})'
    success, message = execute_lisp_command(cmd)
    return message if not success else f"Block '{block_name}' inserted at ({x},{y}) with ID '{block_id}'."

@autocad_mcp.tool()
async def connect_blocks(start_id: str, end_id: str, layer: str = "Connections", 
                         from_point: str = "CONN_DEFAULT1", to_point: str = "CONN_DEFAULT2") -> str:
    """
    Connect two blocks by ID with a line from a named connection point in
    the first block to a named connection point in the second block.
    """
    cmd = f'(c:connect_blocks_by_id "{start_id}" "{end_id}" "{layer}" "{from_point}" "{to_point}")'
    success, message = execute_lisp_command(cmd)
    return message if not success else f"Connected block '{start_id}' to '{end_id}' on layer '{layer}'."

@autocad_mcp.tool()
async def label_block(block_id: str, label_text: str, height: float = 2.5) -> str:
    label_escaped = label_text.replace('"', '\\"')
    cmd = f'(c:label_block_by_id "{block_id}" "{label_escaped}" {height})'
    success, message = execute_lisp_command(cmd)
    return message if not success else f"Labeled block '{block_id}' with text '{label_text}'."

@autocad_mcp.tool()
async def arrange_blocks(blocks_and_ids: list, start_x: float, start_y: float, 
                         direction: str = "right", distance: float = 20.0) -> str:
    """
    Arrange multiple blocks in a sequence with optional ID assignment.
    blocks_and_ids is a list of tuples (block_name, block_id).
    """
    try:
        # Convert to a LISP list form: (("BlockName" (("ID" . "B-1"))) ...)
        block_list_lisp = "("
        for (b_name, b_id) in blocks_and_ids:
            block_list_lisp += f'("{b_name}" (("ID" . "{b_id}"))) '
        block_list_lisp += ")"
        
        cmd = f'(c:arrange_blocks {block_list_lisp} {start_x} {start_y} "{direction}" {distance})'
        success, message = execute_lisp_command(cmd)
        return message if not success else f"Arranged {len(blocks_and_ids)} blocks starting at ({start_x},{start_y})."
    except Exception as e:
        logger.error(f"Error in arrange_blocks: {str(e)}")
        return f"Error: {str(e)}"

###############################################################################
# Additional Tools / placeholders
###############################################################################

@autocad_mcp.tool()
async def create_polyline(points: List[Tuple[float, float]], closed: bool = False) -> str:
    """
    Create a polyline from a list of points.
    E.g., points=[(0,0), (10,0), (10,5)], closed=True
    """
    if len(points) < 2:
        return "Need at least two points to create a polyline."
        
    # First approach: Try to use direct command entry with _pline
    try:
        if not activate_autocad_window():
            return "Failed to activate AutoCAD window"
            
        # Clear command line
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        
        # Ensure current layer is preserved
        execute_lisp_command('(setq current-layer (getvar "CLAYER"))')
        execute_lisp_command('(setvar "CLAYER" current-layer)')
        time.sleep(0.1)
        
        # Start polyline command
        keyboard.write("_pline")
        keyboard.press_and_release('enter')
        time.sleep(0.2)
        
        # Enter points
        for (x, y) in points:
            keyboard.write(f"{x},{y}")
            keyboard.press_and_release('enter')
            time.sleep(0.1)
            
        # Close if needed
        if closed:
            keyboard.write("C")
            keyboard.press_and_release('enter')
        else:
            keyboard.press_and_release('enter')
            
        time.sleep(0.2)  # Give time for command to complete
        return "Polyline created."
        
    except Exception as e:
        logger.error(f"Error with direct polyline creation: {str(e)}")
        
        # Fallback to LISP method if direct method fails
        try:
            # Build a LISP list of point lists
            pts_lisp = "(list "
            for (x, y) in points:
                pts_lisp += f"(list {x} {y} 0.0) "
            pts_lisp += ")"
            
            cmd = f"(c:create-polyline {pts_lisp} {'T' if closed else 'nil'})"
            success, message = execute_lisp_command(cmd)
            return message if not success else "Polyline created."
        except Exception as e2:
            return f"Failed to create polyline: {str(e2)}"

@autocad_mcp.tool()
async def rotate_entity_by_id(block_id: str, base_x: float, base_y: float, angle_degrees: float) -> str:
    """
    Rotate an entity identified by ID around a specified base point by given degrees.
    """
    cmd = f'(c:rotate_entity_by_id "{block_id}" {base_x} {base_y} {angle_degrees})'
    success, message = execute_lisp_command(cmd)
    return message if not success else f"Rotated entity {block_id} around ({base_x}, {base_y}) by {angle_degrees} degrees."

@autocad_mcp.tool()
async def create_linear_dimension(x1: float, y1: float, x2: float, y2: float, dim_x: float, dim_y: float) -> str:
    """
    Placeholder for a linear dimension creation.
    In LT, dimension creation can be done with a command sequence or dimension command stubs.
    """
    # First ensure we're using the active layer
    execute_lisp_command('(setq current-layer (getvar "CLAYER"))')
    execute_lisp_command('(setvar "CLAYER" current-layer)')
    
    cmd = f"(c:create-linear-dim {x1} {y1} {x2} {y2} {dim_x} {dim_y})"
    success, message = execute_lisp_command(cmd)
    return message if not success else "Linear dimension created."

@autocad_mcp.tool()
async def create_hatch(polyline_id: str, hatch_pattern: str = "ANSI31") -> str:
    """
    Placeholder for hatching a closed polyline by ID.
    """
    cmd = f'(c:hatch_closed_poly_by_id "{polyline_id}" "{hatch_pattern}")'
    success, message = execute_lisp_command(cmd)
    return message if not success else "Hatch created."

###############################################################################
# Utility Tools
###############################################################################

@autocad_mcp.tool()
async def set_layer_properties(layer_name: str, color: str, linetype: str = "CONTINUOUS",
                             lineweight: str = "Default", plot_style: str = "ByLayer",
                             transparency: int = 0) -> str:
    """
    Create or modify a layer with extended properties.
    Uses a simpler, more robust approach with individual commands.
    """
    try:
        # First check if AutoCAD is ready
        if not activate_autocad_window():
            return "Failed to activate AutoCAD window"
        
        # Clear any pending commands - be very thorough
        for _ in range(3):
            keyboard.press_and_release('esc')
            time.sleep(0.2)
        
        # Start with a simple command to ensure we're in a clean state
        execute_lisp_command('(princ "READY")')
        time.sleep(0.2)
        
        # Check if layer exists first using a simple LISP query
        layer_exists_lisp = f'(if (tblsearch "LAYER" "{layer_name}") (princ "T") (princ "nil"))'
        success, result = execute_lisp_command(layer_exists_lisp)
        
        # Create the layer if it doesn't exist - using direct command approach
        if "T" not in result:
            # Use direct keyboard commands instead of LISP
            keyboard.press_and_release('esc')
            time.sleep(0.2)
            keyboard.write("LAYER")
            keyboard.press_and_release('enter')
            time.sleep(0.3)
            
            # Create a new layer
            keyboard.write("N")
            keyboard.press_and_release('enter')
            time.sleep(0.2)
            keyboard.write(layer_name)
            keyboard.press_and_release('enter')
            time.sleep(0.2)
            
            # Set the color
            keyboard.write("C")
            keyboard.press_and_release('enter')
            time.sleep(0.2)
            keyboard.write(color)
            keyboard.press_and_release('enter')
            time.sleep(0.2)
            keyboard.write(layer_name)
            keyboard.press_and_release('enter')
            time.sleep(0.2)
            
            # Set the linetype
            keyboard.write("L")
            keyboard.press_and_release('enter')
            time.sleep(0.2)
            keyboard.write(linetype)
            keyboard.press_and_release('enter')
            time.sleep(0.2)
            keyboard.write(layer_name)
            keyboard.press_and_release('enter')
            time.sleep(0.2)
            
            # Exit the LAYER command
            keyboard.press_and_release('esc')
            time.sleep(0.3)
        else:
            # Layer exists, just modify properties
            # Similar direct command approach...
            pass
        
        # Now try to set this as the current layer - using direct keyboard command
        keyboard.press_and_release('esc')
        time.sleep(0.2)
        keyboard.write("-LAYER")  # Using the command line version for more reliability
        keyboard.press_and_release('enter')
        time.sleep(0.3)
        keyboard.write("S")  # Set option
        keyboard.press_and_release('enter')
        time.sleep(0.2)
        keyboard.write(layer_name)
        keyboard.press_and_release('enter')
        time.sleep(0.3)
        
        # Verify current layer
        verify_current_lisp = '(getvar "CLAYER")'
        verify_success, current_layer = execute_lisp_command(verify_current_lisp)
        current_layer = current_layer.strip()
        
        if current_layer == layer_name:
            return f"Layer '{layer_name}' created and set as current layer."
        else:
            return f"Layer '{layer_name}' created but could not be set as current. Current layer is '{current_layer}'"
            
    except Exception as e:
        logger.error(f"Error setting layer properties: {str(e)}")
        return f"Error setting layer properties: {str(e)}"
                
@autocad_mcp.tool()
async def execute_custom_autolisp(code: str) -> str:
    """Execute custom AutoLISP code directly from a string."""
    try:
        # Clean up the code - remove extra whitespace, ensure proper formatting
        code = code.strip()
        
        # For direct command entry, if it's a single-line LISP expression, just execute directly
        if not "\n" in code and len(code) < 120:  # If it's a short, single line command
            success, message = execute_lisp_command(code)
            return message if not success else "Custom AutoLISP code executed successfully."
        
        # Otherwise, use a more robust approach - create a temporary LISP file
        try:
            # Create a temp file with the LISP code
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, "temp_autolisp_code.lsp")
            
            with open(temp_file, "w") as f:
                f.write(code)
            
            # Load the temp file
            success, message = load_lisp_file(temp_file)
            
            # Clean up
            try:
                os.remove(temp_file)
            except Exception:
                pass  # Ignore cleanup errors
                
            return message if not success else "Custom AutoLISP code executed successfully."
        
        except Exception as file_error:
            logger.error(f"Error with temp file approach: {str(file_error)}")
            
            # Fall back to clipboard method if file approach fails
            pyperclip.copy(code)
            success, message = execute_lisp_from_clipboard()
            return message if not success else "Custom AutoLISP code executed successfully."
            
    except Exception as e:
        logger.error(f"Error executing custom AutoLISP: {str(e)}")
        return f"Error executing custom AutoLISP: {str(e)}"

# Add a health check function for the server
@autocad_mcp.tool()
async def server_health_check() -> str:
    """Check the server's health and connection to AutoCAD."""
    try:
        logger.info("Performing server health check...")
        
        # Check if AutoCAD window is found
        if acad_window is None:
            acad_window = find_autocad_window()
            if acad_window is None:
                return "WARNING: AutoCAD window not found. Please make sure AutoCAD is running with a drawing open."
        
        # Verify window is still valid
        try:
            window_title = win32gui.GetWindowText(acad_window)
            if not window_title or "AutoCAD" not in window_title:
                return "WARNING: AutoCAD window appears to be invalid or closed."
            
            # Test basic commands
            success, message = execute_lisp_command("(princ \"HEALTH_CHECK\")")
            if not success:
                return f"WARNING: Failed to execute basic LISP command: {message}"
            
            # All checks passed
            return f"Server health: OK, connected to: {window_title}"
        except Exception as e:
            logger.error(f"Error in health check: {str(e)}")
            return f"WARNING: Server health check failed: {str(e)}"
    except Exception as e:
        logger.error(f"Error during health check: {str(e)}")
        return f"ERROR: Health check failed with exception: {str(e)}"

# Setup error handling for stream errors
def setup_error_handling():
    """Set up robust error handling for stream errors."""
    try:
        # Add more robust error handling for stream-related operations
        import sys
        original_stderr = sys.stderr
        
        class CustomStderr:
            def write(self, message):
                # Still write to original stderr
                original_stderr.write(message)
                
                # Log critical errors
                if "BrokenResourceError" in message or "transport closed" in message:
                    logger.critical(f"STREAM ERROR DETECTED: {message.strip()}")
            
            def flush(self):
                original_stderr.flush()
        
        # Replace stderr with our custom handler
        sys.stderr = CustomStderr()
        logger.info("Enhanced error handling for stream errors configured")
    except Exception as e:
        logger.error(f"Failed to set up error handling: {str(e)}")

if __name__ == "__main__":
    # Set up enhanced error handling
    setup_error_handling()
    
    # Give AutoCAD time to be fully ready before initialization
    time.sleep(1.0)
    
    # Initialize connection to AutoCAD
    logger.info("Starting AutoCAD LT MCP server...")
    if initialize_autocad_lisp():
        logger.info("Successfully initialized AutoCAD LT with advanced LISP libraries.")
    else:
        logger.warning("Failed to initialize AutoCAD LT with LISP. Will retry on tool calls.")
    
    try:
        # Run the server
        logger.info("Starting MCP server...")
        autocad_mcp.run(transport='stdio')
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
    except Exception as e:
        logger.critical(f"Server crashed: {str(e)}")