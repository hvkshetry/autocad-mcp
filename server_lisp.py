#!/usr/bin/env python
"""
AutoCAD LT MCP Server (AutoLISP Version)
A specialized implementation that uses AutoLISP code generation and execution.
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

def find_autocad_window():
    """Find the AutoCAD LT window handle."""
    def enum_windows_callback(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if "AutoCAD LT" in window_text and "Drawing" in window_text:
                result.append(hwnd)
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    
    if windows:
        return windows[0]
    return None

def load_lisp_file(file_path):
    """Load a LISP file into AutoCAD."""
    global acad_window
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False, "AutoCAD LT window not found"
    
    try:
        # Activate the AutoCAD window
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(0.2)  # Give it time to focus
        
        # Command to load LISP file
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        keyboard.write("(load \"{}\")".format(file_path.replace('\\', '/')))
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.5)  # Wait for loading
        
        return True, "LISP file loaded successfully"
    except Exception as e:
        logger.error(f"Error loading LISP file: {str(e)}")
        return False, f"Error loading LISP file: {str(e)}"

def execute_lisp_command(command):
    """Execute a LISP command in AutoCAD."""
    global acad_window
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False, "AutoCAD LT window not found"
    
    try:
        # Activate the AutoCAD window
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(0.2)  # Give it time to focus
        
        # Clear any previous command
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        
        # Execute command
        keyboard.write(command)
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.5)  # Wait for command execution
        
        return True, "Command executed successfully"
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
        # Activate the AutoCAD window
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(0.2)  # Give it time to focus
        
        # Command to execute LISP code from clipboard
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        keyboard.press_and_release('esc')
        time.sleep(0.1)
        
        # Execute using LISP's (eval (read)) pattern
        keyboard.write("(eval (read))")
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.2)
        
        # AutoCAD now expects LISP code input
        # Use Ctrl+V to paste from clipboard
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.1)
        keyboard.press_and_release('enter')
        time.sleep(0.5)  # Wait for execution
        
        return True, "LISP code from clipboard executed successfully"
    except Exception as e:
        logger.error(f"Error executing LISP from clipboard: {str(e)}")
        return False, f"Error executing LISP from clipboard: {str(e)}"

def initialize_autocad_lisp():
    """Initialize AutoCAD with LISP capabilities."""
    global acad_window, lisp_path
    
    # Find AutoCAD window
    acad_window = find_autocad_window()
    if not acad_window:
        logger.error("AutoCAD LT window not found. Make sure AutoCAD LT is running with a drawing open.")
        return False
    
    # Load our main LISP library
    basic_shapes_lisp = os.path.join(lisp_path, "basic_shapes.lsp")
    process_helpers_lisp = os.path.join(lisp_path, "process_diagram_helpers.lsp")
    tag_helpers_lisp = os.path.join(lisp_path, "tag_helpers.lsp")
    
    # Load basic shapes library
    if os.path.exists(basic_shapes_lisp):
        success, message = load_lisp_file(basic_shapes_lisp)
        if not success:
            logger.error(f"Failed to load basic shapes library: {message}")
            return False
    else:
        logger.error(f"LISP file not found: {basic_shapes_lisp}")
        return False
    
    # Load process diagram helpers library
    if os.path.exists(process_helpers_lisp):
        success, message = load_lisp_file(process_helpers_lisp)
        if not success:
            logger.error(f"Failed to load process diagram helpers library: {message}")
            return False
    else:
        logger.error(f"LISP file not found: {process_helpers_lisp}")
        return False
        
    # Load tag helpers library
    if os.path.exists(tag_helpers_lisp):
        success, message = load_lisp_file(tag_helpers_lisp)
        if success:
            logger.info("Successfully loaded all LISP libraries")
            return True
        else:
            logger.error(f"Failed to load tag helpers library: {message}")
            return False
    else:
        logger.error(f"LISP file not found: {tag_helpers_lisp}")
        return False

@autocad_mcp.tool()
async def get_autocad_status() -> str:
    """Get the current status of the AutoCAD connection.
    
    Returns:
        Status message indicating if AutoCAD is connected.
    """
    global acad_window
    
    if acad_window is None:
        if initialize_autocad_lisp():
            window_title = win32gui.GetWindowText(acad_window)
            return f"Successfully connected to AutoCAD LT with AutoLISP support: {window_title}"
        else:
            return "Failed to connect to AutoCAD LT. Please ensure AutoCAD LT is running with a drawing open."
    
    try:
        window_title = win32gui.GetWindowText(acad_window)
        if "AutoCAD LT" in window_title:
            return f"Connected to AutoCAD LT with AutoLISP support: {window_title}"
        else:
            # Try to reconnect
            if initialize_autocad_lisp():
                window_title = win32gui.GetWindowText(acad_window)
                return f"Reconnected to AutoCAD LT with AutoLISP support: {window_title}"
            return "Lost connection to AutoCAD LT."
    except Exception as e:
        # Try to reconnect
        if initialize_autocad_lisp():
            return "Reconnected to AutoCAD LT successfully."
        return f"Lost connection to AutoCAD LT: {str(e)}"

@autocad_mcp.tool()
async def create_line(start_x: float, start_y: float, end_x: float, end_y: float) -> str:
    """Create a line in AutoCAD using AutoLISP.
    
    Args:
        start_x: X coordinate of start point
        start_y: Y coordinate of start point
        end_x: X coordinate of end point
        end_y: Y coordinate of end point
        
    Returns:
        Confirmation message or error
    """
    try:
        command = f"(c:create-line {start_x} {start_y} {end_x} {end_y})"
        success, message = execute_lisp_command(command)
        if success:
            return f"Line created from ({start_x},{start_y}) to ({end_x},{end_y})"
        else:
            return message
    except Exception as e:
        logger.error(f"Error creating line: {str(e)}")
        return f"Error creating line: {str(e)}"

@autocad_mcp.tool()
async def create_circle(center_x: float, center_y: float, radius: float) -> str:
    """Create a circle in AutoCAD using AutoLISP.
    
    Args:
        center_x: X coordinate of center point
        center_y: Y coordinate of center point
        radius: Radius of the circle
        
    Returns:
        Confirmation message or error
    """
    try:
        command = f"(c:create-circle {center_x} {center_y} {radius})"
        success, message = execute_lisp_command(command)
        if success:
            return f"Circle created at ({center_x},{center_y}) with radius {radius}"
        else:
            return message
    except Exception as e:
        logger.error(f"Error creating circle: {str(e)}")
        return f"Error creating circle: {str(e)}"

@autocad_mcp.tool()
async def create_text(x: float, y: float, text: str, height: float = 2.5) -> str:
    """Create text in AutoCAD using AutoLISP.
    
    Args:
        x: X coordinate of insertion point
        y: Y coordinate of insertion point
        text: Text content
        height: Text height (default: 2.5)
        
    Returns:
        Confirmation message or error
    """
    try:
        # Need to handle the text string for LISP
        text_escaped = text.replace('"', '\\"')
        command = f'(c:create-text {x} {y} "{text_escaped}" {height})'
        success, message = execute_lisp_command(command)
        if success:
            return f"Text '{text}' created at ({x},{y})"
        else:
            return message
    except Exception as e:
        logger.error(f"Error creating text: {str(e)}")
        return f"Error creating text: {str(e)}"

@autocad_mcp.tool()
async def create_equipment_symbol(equipment_type: str, x: float, y: float, tag: str = "",
                                 scale: float = 1.0) -> str:
    """Create a process equipment symbol using AutoLISP.
    
    Args:
        equipment_type: Type of equipment ('vessel', 'pump', 'exchanger')
        x: X coordinate for insertion point
        y: Y coordinate for insertion point
        tag: Equipment tag (default: empty)
        scale: Symbol scale (default: 1.0)
        
    Returns:
        Confirmation message or error
    """
    try:
        # Handle the tag string for LISP
        tag_escaped = tag.replace('"', '\\"')
        
        # Use the standard equipment insertion function for predefined block types
        if equipment_type.lower() in ['pump-centrif1', 'pump-centrifugal-1']:
            command = f'(c:insert_standard_equipment "pump-centrifugal-1" {x} {y} "{tag_escaped}" {scale})'
        elif equipment_type.lower() in ['pump-centrif2', 'pump-centrifugal-2']:
            command = f'(c:insert_standard_equipment "pump-centrifugal-2" {x} {y} "{tag_escaped}" {scale})'
        elif equipment_type.lower() in ['blower-rotary', 'blower']:
            command = f'(c:insert_standard_equipment "blower-rotary" {x} {y} "{tag_escaped}" {scale})'
        # Fall back to original equipment types for backward compatibility
        elif equipment_type.lower() == 'pump':
            command = f'(c:create-pump {x} {y} {scale} "{tag_escaped}")'
        elif equipment_type.lower() == 'vessel':
            width = 8.0 * scale
            height = 20.0 * scale
            command = f'(c:create-vessel {x} {y} {width} {height} "{tag_escaped}")'
        elif equipment_type.lower() in ['exchanger', 'heat exchanger']:
            command = f'(c:create-heat-exchanger {x} {y} {scale} "{tag_escaped}")'
        else:
            return f"Unknown equipment type: {equipment_type}"
        
        success, message = execute_lisp_command(command)
        if success:
            return f"{equipment_type.capitalize()} symbol created at ({x},{y}) with tag '{tag}'"
        else:
            return message
    except Exception as e:
        logger.error(f"Error creating equipment symbol: {str(e)}")
        return f"Error creating equipment symbol: {str(e)}"

@autocad_mcp.tool()
async def create_pipe(start_x: float, start_y: float, end_x: float, end_y: float) -> str:
    """Create a pipe line between two points using AutoLISP.
    
    Args:
        start_x: X coordinate of start point
        start_y: Y coordinate of start point
        end_x: X coordinate of end point
        end_y: Y coordinate of end point
        
    Returns:
        Confirmation message or error
    """
    try:
        command = f"(c:create-pipe {start_x} {start_y} {end_x} {end_y})"
        success, message = execute_lisp_command(command)
        if success:
            return f"Pipe created from ({start_x},{start_y}) to ({end_x},{end_y})"
        else:
            return message
    except Exception as e:
        logger.error(f"Error creating pipe: {str(e)}")
        return f"Error creating pipe: {str(e)}"

@autocad_mcp.tool()
async def create_simple_pfd(x: float, y: float, scale: float = 1.0) -> str:
    """Create a simple process flow diagram using AutoLISP.
    
    Args:
        x: X coordinate for starting point
        y: Y coordinate for center line
        scale: Overall scaling factor (default: 1.0)
        
    Returns:
        Confirmation message or error
    """
    try:
        command = f"(c:create-simple-pfd {x} {y} {scale})"
        success, message = execute_lisp_command(command)
        if success:
            return f"Simple process flow diagram created at ({x},{y}) with scale {scale}"
        else:
            return message
    except Exception as e:
        logger.error(f"Error creating process flow diagram: {str(e)}")
        return f"Error creating process flow diagram: {str(e)}"

@autocad_mcp.tool()
async def connect_equipment(start_equipment_id: str, end_equipment_id: str, 
                           pipe_type: str = "Main", from_port: str = "out", 
                           to_port: str = "in") -> str:
    """Connect two equipment blocks with a pipe.
    
    Args:
        start_equipment_id: Tag or ID of the starting equipment
        end_equipment_id: Tag or ID of the ending equipment
        pipe_type: Type of pipe (Main, Secondary, etc.)
        from_port: Port name on the starting equipment (default: out)
        to_port: Port name on the ending equipment (default: in)
        
    Returns:
        Confirmation message or error
    """
    try:
        # Create a LISP command that finds the equipment by tag and connects them
        # This requires implementing a helper function in AutoLISP to find entities by tag
        command = f'(c:connect_equipment_by_tag "{start_equipment_id}" "{end_equipment_id}" "{pipe_type}" "{from_port}" "{to_port}")'
        
        # For now, we'll use a simpler approach and just indicate this needs to be implemented
        # In a real implementation, we would need to track entity names of inserted equipment
        success, message = execute_lisp_command(command)
        if success:
            return f"Connected {start_equipment_id} to {end_equipment_id} with {pipe_type} pipe"
        else:
            return f"Error connecting equipment: {message}. This function requires implementation of equipment tracking by tag."
    except Exception as e:
        logger.error(f"Error connecting equipment: {str(e)}")
        return f"Error connecting equipment: {str(e)}"

@autocad_mcp.tool()
async def label_equipment(equipment_id: str, label_text: str, height: float = 2.5) -> str:
    """Label an equipment block with text.
    
    Args:
        equipment_id: Tag or ID of the equipment to label
        label_text: Text content for the label
        height: Text height (default: 2.5)
        
    Returns:
        Confirmation message or error
    """
    try:
        # Create a LISP command that finds the equipment by tag and labels it
        label_escaped = label_text.replace('"', '\\"')
        command = f'(c:label_equipment_by_tag "{equipment_id}" "{label_escaped}" {height})'
        
        # For now, we'll use a simpler approach and just indicate this needs to be implemented
        success, message = execute_lisp_command(command)
        if success:
            return f"Labeled equipment {equipment_id} with text: {label_text}"
        else:
            return f"Error labeling equipment: {message}. This function requires implementation of equipment tracking by tag."
    except Exception as e:
        logger.error(f"Error labeling equipment: {str(e)}")
        return f"Error labeling equipment: {str(e)}"

@autocad_mcp.tool()
async def arrange_equipment(equipment_types: list, start_x: float, start_y: float, 
                          direction: str = "right", distance: float = 20.0) -> str:
    """Arrange multiple equipment blocks in a sequence with connections.
    
    Args:
        equipment_types: List of tuples containing (equipment_type, tag)
        start_x: X coordinate for starting position
        start_y: Y coordinate for starting position
        direction: Direction for arrangement (right, left, up, down)
        distance: Distance between equipment blocks
        
    Returns:
        Confirmation message or error
    """
    try:
        # Convert the equipment list to a LISP format
        equipment_list_lisp = "("
        for eq in equipment_types:
            eq_type, eq_tag = eq
            equipment_list_lisp += f'("{eq_type}" (("TAG" . "{eq_tag}"))) '
        equipment_list_lisp += ")"
        
        command = f'(c:arrange_equipment {equipment_list_lisp} {start_x} {start_y} "{direction}" {distance})'
        
        # Execute the command
        success, message = execute_lisp_command(command)
        if success:
            return f"Arranged {len(equipment_types)} equipment blocks starting at ({start_x},{start_y})"
        else:
            return message
    except Exception as e:
        logger.error(f"Error arranging equipment: {str(e)}")
        return f"Error arranging equipment: {str(e)}"

@autocad_mcp.tool()
async def set_layer_properties(layer_name: str, color: str, linetype: str = "CONTINUOUS") -> str:
    """Create or modify a layer with specified properties.
    
    Args:
        layer_name: Name of the layer
        color: Color name or number
        linetype: Line type name (default: CONTINUOUS)
        
    Returns:
        Confirmation message or error
    """
    try:
        command = f'(ensure_layer_exists "{layer_name}" "{color}" "{linetype}")'
        
        success, message = execute_lisp_command(command)
        if success:
            return f"Layer {layer_name} created/updated with color {color} and linetype {linetype}"
        else:
            return message
    except Exception as e:
        logger.error(f"Error setting layer properties: {str(e)}")
        return f"Error setting layer properties: {str(e)}"

@autocad_mcp.tool()
async def execute_custom_autolisp(code: str) -> str:
    """Execute custom AutoLISP code directly.
    
    Args:
        code: AutoLISP code to execute
        
    Returns:
        Execution result message
    """
    try:
        # Use clipboard for more complex/longer code
        pyperclip.copy(code)
        success, message = execute_lisp_from_clipboard()
        if success:
            return "Custom AutoLISP code executed successfully"
        else:
            return message
    except Exception as e:
        logger.error(f"Error executing custom AutoLISP: {str(e)}")
        return f"Error executing custom AutoLISP: {str(e)}"

@autocad_mcp.prompt("create_process_diagram")
async def create_process_diagram_prompt(process_description: str, equipment_list: str) -> dict:
    """
    A prompt template to create a process diagram based on text description.
    
    Args:
        process_description: Description of the process
        equipment_list: Comma-separated list of major equipment items
    """
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"""I need to create a process diagram for the following process:
                
{process_description}

The main equipment includes: {equipment_list}

Please analyze this description and help me create the diagram by generating appropriate AutoLISP code and using the AutoCAD LT MCP server tools.

You have these main tools available:
- create_equipment_symbol (equipment_type, x, y, tag, scale)
  - Available equipment types: 'pump-centrif1', 'pump-centrif2', 'blower-rotary'
- create_pipe (start_x, start_y, end_x, end_y)
- create_text (x, y, text, height)
- connect_equipment (start_equipment_id, end_equipment_id, pipe_type, from_port, to_port)
- label_equipment (equipment_id, label_text, height)
- arrange_equipment (equipment_types, start_x, start_y, direction, distance)
- set_layer_properties (layer_name, color, linetype)
- create_simple_pfd (x, y, scale)
- execute_custom_autolisp (code)

For more complex diagrams, you can generate custom AutoLISP code and execute it directly.

Start by identifying the major equipment items, their connections, and suggesting a logical layout.
"""
            }
        }
    ]
    return {"messages": messages}

if __name__ == "__main__":
    # Initialize AutoCAD connection
    if initialize_autocad_lisp():
        logger.info("Successfully initialized AutoCAD LT with AutoLISP support")
    else:
        logger.warning("Failed to initialize AutoCAD LT with AutoLISP, will try again when tools are called")
    
    # Run the MCP server
    autocad_mcp.run(transport='stdio')
