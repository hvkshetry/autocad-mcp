#!/usr/bin/env python
"""
AutoCAD LT MCP Server (AutoLISP Version)
A specialized implementation for a general 2D drafting assistant.

Revisions:
- Added a robust layer management approach that calls a new AutoLISP function 
  c:create_or_set_layer to handle creation + set current reliably.
- For lineweight, color, linetype, etc., pass them as strings. Added a slight 
  time.sleep(0.2) after sending commands to help with typed-command concurrency.
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

from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("autocad-lisp-mcp")

# Initialize FastMCP server
autocad_mcp = FastMCP("autocad-lisp-server")

# Global variables
acad_window = None
lisp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lisp-code")

# Configuration flag to disable ESC key presses if they cause issues
# Set to False if AutoCAD help menu keeps opening
USE_ESC_KEY = True

def find_autocad_window():
    """Find the AutoCAD LT window handle by checking window titles."""
    def enum_windows_callback(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            win_text = window_text.lower()
            if "autocad" in win_text and ("drawing" in win_text or ".dwg" in win_text):
                result.append(hwnd)
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    
    if windows:
        return windows[0]
    return None

def load_lisp_file(file_path):
    """Load a LISP file into AutoCAD by simulating typed commands."""
    global acad_window
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False, "AutoCAD LT window not found"
    
    try:
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(0.5)
        
        # Single ESC with proper delay
        keyboard.press_and_release('esc')
        time.sleep(0.5)
        keyboard.write("(load \"{}\")".format(file_path.replace('\\', '/')))
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        
        # Extended delay for security prompt acceptance
        # Adjust this value if you need more time to accept the prompt
        time.sleep(3.0)  # Increased from 0.5 to 3.0 seconds
        
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
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(0.2)
        
        if USE_ESC_KEY:
            # Single ESC with longer delay to avoid accidental key combinations
            keyboard.press_and_release('esc')
            time.sleep(0.3)  # Increased delay to ensure clean key release
        
        keyboard.write(command)
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.2)  # Small wait to ensure command is fully processed
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
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(0.2)
        
        if USE_ESC_KEY:
            # Single ESC with longer delay to avoid accidental key combinations
            keyboard.press_and_release('esc')
            time.sleep(0.3)  # Increased delay to ensure clean key release
        
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

def initialize_autocad_lisp():
    """
    Initialize AutoCAD with LISP capabilities for general drafting.
    Loads multiple LISP files for advanced drafting, geometry, annotation, etc.
    """
    global acad_window, lisp_path
    
    acad_window = find_autocad_window()
    if not acad_window:
        logger.error("AutoCAD LT window not found. Make sure AutoCAD LT is running with a drawing open.")
        return False
    
    lisp_files = [
        "error_handling.lsp",
        "basic_shapes.lsp",
        "drafting_helpers.lsp",
        "block_id_helpers.lsp",
        "selection_and_file.lsp",
        "advanced_geometry.lsp",
        "advanced_entities.lsp",
        "entity_modification.lsp",
        "annotation_helpers.lsp",
        "layout_management.lsp"
    ]
    
    for f in lisp_files:
        full_path = os.path.join(lisp_path, f)
        if os.path.exists(full_path):
            success, message = load_lisp_file(full_path)
            if not success:
                logger.error(f"Failed to load {f}: {message}")
                return False
        else:
            logger.error(f"LISP file not found: {full_path}")
            return False
    
    logger.info("Successfully loaded all LISP libraries for a general 2D drafting assistant.")
    return True

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
        if "AutoCAD LT" in window_title:
            return f"Connected to AutoCAD: {window_title}"
        else:
            if initialize_autocad_lisp():
                window_title = win32gui.GetWindowText(acad_window)
                return f"Reconnected to AutoCAD: {window_title}"
            return "Lost connection to AutoCAD LT."
    except Exception as e:
        if initialize_autocad_lisp():
            return "Reconnected to AutoCAD LT successfully."
        return f"Lost connection to AutoCAD LT: {str(e)}"

###############################################################################
# Example Tools
###############################################################################

@autocad_mcp.tool()
async def create_line(start_x: float, start_y: float, end_x: float, end_y: float) -> str:
    cmd = f"(c:create-line {start_x} {start_y} {end_x} {end_y})"
    success, message = execute_lisp_command(cmd)
    if success:
        return f"Line created from ({start_x},{start_y}) to ({end_x},{end_y})."
    return message

@autocad_mcp.tool()
async def create_circle(center_x: float, center_y: float, radius: float) -> str:
    cmd = f"(c:create-circle {center_x} {center_y} {radius})"
    success, message = execute_lisp_command(cmd)
    if success:
        return f"Circle created at ({center_x},{center_y}), radius {radius}."
    return message

@autocad_mcp.tool()
async def create_text(x: float, y: float, text: str, height: float = 2.5) -> str:
    text_escaped = text.replace('"', '\\"')
    cmd = f'(c:create-text {x} {y} "{text_escaped}" {height})'
    success, message = execute_lisp_command(cmd)
    if success:
        return f"Text '{text}' created at ({x},{y})."
    return message

@autocad_mcp.tool()
async def insert_block(block_name: str, x: float, y: float, block_id: str = "",
                       scale: float = 1.0, rotation: float = 0.0) -> str:
    block_id_escaped = block_id.replace('"', '\\"')
    cmd = f'(c:insert_block "{block_name}" {x} {y} "{block_id_escaped}" {scale} {rotation})'
    success, message = execute_lisp_command(cmd)
    if success:
        return f"Block '{block_name}' inserted at ({x},{y}) with ID '{block_id}'."
    return message

@autocad_mcp.tool()
async def connect_blocks(start_id: str, end_id: str, layer: str = "Connections", 
                         from_point: str = "CONN_DEFAULT1", to_point: str = "CONN_DEFAULT2") -> str:
    cmd = f'(c:connect_blocks_by_id "{start_id}" "{end_id}" "{layer}" "{from_point}" "{to_point}")'
    success, message = execute_lisp_command(cmd)
    if success:
        return f"Connected block '{start_id}' to '{end_id}' on layer '{layer}'."
    return message

@autocad_mcp.tool()
async def label_block(block_id: str, label_text: str, height: float = 2.5) -> str:
    label_escaped = label_text.replace('"', '\\"')
    cmd = f'(c:label_block_by_id "{block_id}" "{label_escaped}" {height})'
    success, message = execute_lisp_command(cmd)
    if success:
        return f"Labeled block '{block_id}' with text '{label_text}'."
    return message

@autocad_mcp.tool()
async def arrange_blocks(blocks_and_ids: list, start_x: float, start_y: float, 
                         direction: str = "right", distance: float = 20.0) -> str:
    try:
        block_list_lisp = "("
        for (b_name, b_id) in blocks_and_ids:
            block_list_lisp += f'("{b_name}" (("ID" . "{b_id}"))) '
        block_list_lisp += ")"
        
        cmd = f'(c:arrange_blocks {block_list_lisp} {start_x} {start_y} "{direction}" {distance})'
        success, message = execute_lisp_command(cmd)
        if success:
            return f"Arranged {len(blocks_and_ids)} blocks starting at ({start_x},{start_y})."
        else:
            return message
    except Exception as e:
        logger.error(f"Error in arrange_blocks: {str(e)}")
        return f"Error: {str(e)}"

@autocad_mcp.tool()
async def create_polyline(points: List[Tuple[float, float]], closed: bool = False) -> str:
    if len(points) < 2:
        return "Need at least two points to create a polyline."
    pts_str = ""
    for (x, y) in points:
        pts_str += f" (list {x} {y} 0.0)"
    cmd = f"(c:create-polyline (list {pts_str}) {'T' if closed else 'nil'})"
    success, message = execute_lisp_command(cmd)
    return message if not success else "Polyline created."

@autocad_mcp.tool()
async def create_rectangle(x1: float, y1: float, x2: float, y2: float,
                           layer: Optional[str] = None) -> str:
    layer_part = f' "{layer}"' if layer else " nil"
    cmd = f"(c:create-rectangle {x1} {y1} {x2} {y2}{layer_part})"
    success, message = execute_lisp_command(cmd)
    return message if not success else "Rectangle created."

@autocad_mcp.tool()
async def create_arc(center_x: float, center_y: float, radius: float,
                     start_angle: float, end_angle: float,
                     layer: Optional[str] = None) -> str:
    layer_part = f' "{layer}"' if layer else " nil"
    cmd = (f"(c:create-arc {center_x} {center_y} {radius} {start_angle}"
           f" {end_angle}{layer_part})")
    success, message = execute_lisp_command(cmd)
    return message if not success else "Arc created."

@autocad_mcp.tool()
async def create_ellipse(center_x: float, center_y: float,
                         major_axis_end_x: float, major_axis_end_y: float,
                         minor_axis_ratio: float,
                         layer: Optional[str] = None) -> str:
    layer_part = f' "{layer}"' if layer else " nil"
    cmd = (f"(c:create-ellipse {center_x} {center_y} {major_axis_end_x}"
           f" {major_axis_end_y} {minor_axis_ratio}{layer_part})")
    success, message = execute_lisp_command(cmd)
    return message if not success else "Ellipse created."

@autocad_mcp.tool()
async def create_mtext(x: float, y: float, width: float, text_string: str,
                       height: float, layer: Optional[str] = None,
                       style: Optional[str] = None,
                       rotation: Optional[float] = 0.0) -> str:
    text_escaped = text_string.replace('"', '\\"')
    style_part = f' "{style}"' if style else " nil"
    layer_part = f' "{layer}"' if layer else " nil"
    cmd = (f'(c:create-mtext {x} {y} {width} "{text_escaped}" {height}'
           f'{layer_part}{style_part} {rotation})')
    success, message = execute_lisp_command(cmd)
    return message if not success else "MText created."

@autocad_mcp.tool()
async def create_wipeout_from_points(points: List[Tuple[float, float]],
                                     frame_visible: bool = False) -> str:
    pts_str = ""
    for (x, y) in points:
        pts_str += f" (list {x} {y} 0.0)"
    frame_flag = 'T' if frame_visible else 'nil'
    cmd = f"(c:create-wipeout-from-points (list {pts_str}) {frame_flag})"
    success, message = execute_lisp_command(cmd)
    return message if not success else "Wipeout created."

@autocad_mcp.tool()
async def move_last_entity(delta_x: float, delta_y: float) -> str:
    cmd = f"(c:move-last-entity {delta_x} {delta_y})"
    success, message = execute_lisp_command(cmd)
    return message if not success else "Entity moved."

@autocad_mcp.tool()
async def rotate_entity_by_id(block_id: str, base_x: float, base_y: float, angle_degrees: float) -> str:
    cmd = f'(c:rotate_entity_by_id "{block_id}" {base_x} {base_y} {angle_degrees})'
    success, message = execute_lisp_command(cmd)
    return message if not success else f"Rotated entity {block_id} around ({base_x}, {base_y}) by {angle_degrees} degrees."

@autocad_mcp.tool()
async def create_linear_dimension(x1: float, y1: float, x2: float, y2: float, dim_x: float, dim_y: float) -> str:
    cmd = f"(c:create-linear-dim {x1} {y1} {x2} {y2} {dim_x} {dim_y})"
    success, message = execute_lisp_command(cmd)
    return message if not success else "Linear dimension created."

@autocad_mcp.tool()
async def create_hatch(polyline_id: str, hatch_pattern: str = "ANSI31") -> str:
    cmd = f'(c:hatch_closed_poly_by_id "{polyline_id}" "{hatch_pattern}")'
    success, message = execute_lisp_command(cmd)
    return message if not success else "Hatch created."

###############################################################################
# FIXED LAYER FUNCTION
###############################################################################

@autocad_mcp.tool()
async def set_layer_properties(layer_name: str, color: str, linetype: str = "CONTINUOUS",
                               lineweight: str = "Default", plot_style: str = "ByLayer",
                               transparency: int = 0) -> str:
    """
    Create or modify a layer, then set it current. All parameters are strings (except transparency).
    We rely on a new AutoLISP function c:create_or_set_layer for reliability.
    """
    # Convert everything to strings as needed
    color_str = color
    linetype_str = linetype
    lineweight_str = lineweight
    plot_style_str = plot_style
    transp_str = str(transparency)

    # We'll pass them as a single command
    # (c:create_or_set_layer layer_name color linetype lineweight plot_style transparency)
    cmd = f'(c:create_or_set_layer "{layer_name}" "{color_str}" "{linetype_str}" "{lineweight_str}" "{plot_style_str}" {transp_str})'
    
    success, message = execute_lisp_command(cmd)
    if success:
        return (f"Layer '{layer_name}' created/updated and set current. "
                f"Properties: color={color_str}, linetype={linetype_str}, "
                f"lineweight={lineweight_str}, plot_style={plot_style_str}, transparency={transp_str}")
    else:
        return message

@autocad_mcp.tool()
async def execute_custom_autolisp(code: str) -> str:
    """Execute custom AutoLISP code directly from a string."""
    try:
        pyperclip.copy(code)
        success, message = execute_lisp_from_clipboard()
        return message if not success else "Custom AutoLISP code executed successfully."
    except Exception as e:
        logger.error(f"Error executing custom AutoLISP: {str(e)}")
        return f"Error executing custom AutoLISP: {str(e)}"

if __name__ == "__main__":
    if initialize_autocad_lisp():
        logger.info("Successfully initialized AutoCAD LT with advanced LISP libraries.")
    else:
        logger.warning("Failed to initialize AutoCAD LT with LISP. Will retry on tool calls.")
    autocad_mcp.run(transport='stdio')
