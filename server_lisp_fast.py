#!/usr/bin/env python
"""
AutoCAD LT MCP Server - Fast Version
Optimized for speed with reduced delays and batch operations
"""
import logging
import sys
import os
import time
import pyperclip
from pathlib import Path
import win32gui
import keyboard
from typing import Optional, Dict, Any, List, Tuple

from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("autocad-lisp-mcp-fast")

# Initialize FastMCP server
autocad_mcp = FastMCP("autocad-lisp-server")

# Global variables
acad_window = None
lisp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lisp-code")

# Performance configuration
FAST_MODE = True  # Enable fast mode with minimal delays
USE_ESC_KEY = False  # Disable ESC to avoid help menu issues
MINIMAL_DELAY = 0.05  # Minimal delay for fast mode
NORMAL_DELAY = 0.1  # Reduced normal delay
FOCUS_DELAY = 0.1  # Reduced window focus delay

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

def execute_lisp_command_fast(command):
    """Execute a LISP command with minimal delays."""
    global acad_window
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False, "AutoCAD LT window not found"
    
    try:
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(FOCUS_DELAY if FAST_MODE else 0.2)
        
        if USE_ESC_KEY:
            keyboard.press_and_release('esc')
            time.sleep(MINIMAL_DELAY if FAST_MODE else 0.3)
        
        keyboard.write(command)
        time.sleep(MINIMAL_DELAY if FAST_MODE else 0.1)
        keyboard.press_and_release('enter')
        time.sleep(NORMAL_DELAY if FAST_MODE else 0.2)
        return True, f"Command executed: {command}"
    except Exception as e:
        logger.error(f"Error executing LISP command: {str(e)}")
        return False, f"Error executing LISP command: {str(e)}"

def load_lisp_file_with_delay(file_path):
    """Load a LISP file with proper delay for security prompts."""
    global acad_window
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False, "AutoCAD LT window not found"
    
    try:
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(0.5)
        
        if USE_ESC_KEY:
            keyboard.press_and_release('esc')
            time.sleep(0.5)
        
        keyboard.write("(load \"{}\")".format(file_path.replace('\\', '/')))
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        
        # Keep the 3-second delay for security prompt acceptance
        time.sleep(3.0)
        
        return True, f"LISP file '{os.path.basename(file_path)}' loaded successfully"
    except Exception as e:
        logger.error(f"Error loading LISP file: {str(e)}")
        return False, f"Error loading LISP file: {str(e)}"

def execute_batch_from_clipboard(lisp_code):
    """Execute multiple LISP commands via clipboard for speed."""
    global acad_window
    
    if not acad_window:
        acad_window = find_autocad_window()
        if not acad_window:
            return False, "AutoCAD LT window not found"
    
    try:
        # Ensure LISP code is properly formatted for execution
        # Wrap in progn if not already wrapped
        if not lisp_code.strip().startswith("(progn"):
            lisp_code = f"(progn {lisp_code})"
        
        # Copy LISP code to clipboard
        pyperclip.copy(lisp_code)
        
        win32gui.SetForegroundWindow(acad_window)
        time.sleep(FOCUS_DELAY)
        
        if USE_ESC_KEY:
            keyboard.press_and_release('esc')
            time.sleep(MINIMAL_DELAY)
        
        # Type the command directly instead of using (eval (read))
        # This ensures we're in command mode, not text mode
        keyboard.write("(vl-load-com)")  # Initialize Visual LISP
        time.sleep(MINIMAL_DELAY)
        keyboard.press_and_release('enter')
        time.sleep(MINIMAL_DELAY)
        
        # Now paste and execute the LISP code
        keyboard.press_and_release('ctrl+v')
        time.sleep(MINIMAL_DELAY)
        keyboard.press_and_release('enter')
        time.sleep(NORMAL_DELAY * 2)  # Give more time for complex scripts
        
        return True, "Batch commands executed successfully"
    except Exception as e:
        logger.error(f"Error executing batch: {str(e)}")
        return False, f"Error executing batch: {str(e)}"

# Batch operation tools
@autocad_mcp.tool()
async def batch_create_lines(lines: List[List[float]]) -> str:
    """Create multiple lines in a single operation.
    lines: List of [x1, y1, x2, y2] coordinates"""
    lines_data = "("
    for line in lines:
        if len(line) == 4:
            lines_data += f"({line[0]} {line[1]} {line[2]} {line[3]}) "
    lines_data += ")"
    
    cmd = f"(c:batch-create-lines '{lines_data})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Created {len(lines)} lines"

@autocad_mcp.tool()
async def batch_create_circles(circles: List[List[float]]) -> str:
    """Create multiple circles in a single operation.
    circles: List of [center_x, center_y, radius]"""
    circles_data = "("
    for circle in circles:
        if len(circle) == 3:
            circles_data += f"({circle[0]} {circle[1]} {circle[2]}) "
    circles_data += ")"
    
    cmd = f"(c:batch-create-circles '{circles_data})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Created {len(circles)} circles"

@autocad_mcp.tool()
async def batch_create_texts(texts: List[Dict[str, Any]]) -> str:
    """Create multiple text entities in a single operation.
    texts: List of dicts with keys: x, y, height, string, rotation (optional)"""
    texts_data = "("
    for text in texts:
        # Escape quotes in the string
        escaped_string = text["string"].replace('"', '\\"')
        texts_data += f'({text["x"]} {text["y"]} {text["height"]} "{escaped_string}") '
    texts_data += ")"
    
    cmd = f"(c:batch-create-texts '{texts_data})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Created {len(texts)} text entities"

# Note: execute_lisp_script removed - use batch operations or execute_custom_autolisp instead

@autocad_mcp.tool()
async def set_performance_mode(fast_mode: bool, minimal_delay: float = 0.05, 
                              normal_delay: float = 0.1) -> str:
    """Configure performance settings."""
    global FAST_MODE, MINIMAL_DELAY, NORMAL_DELAY
    FAST_MODE = fast_mode
    MINIMAL_DELAY = minimal_delay
    NORMAL_DELAY = normal_delay
    mode = "fast" if fast_mode else "normal"
    return f"Performance mode set to {mode} with delays: minimal={minimal_delay}s, normal={normal_delay}s"

# Include all original tools with fast execution
@autocad_mcp.tool()
async def create_line(x1: float, y1: float, x2: float, y2: float) -> str:
    cmd = f"(c:create-line {x1} {y1} {x2} {y2})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Line created successfully."

@autocad_mcp.tool()
async def create_circle(center_x: float, center_y: float, radius: float) -> str:
    cmd = f"(c:create-circle {center_x} {center_y} {radius})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Circle created successfully."

@autocad_mcp.tool()
async def create_text(x: float, y: float, height: float, text_string: str, 
                      rotation: float = 0.0) -> str:
    text_escaped = text_string.replace('"', '\\"')
    if rotation != 0.0:
        # Use the rotated text function when rotation is specified
        cmd = f'(c:create-text-rotated {x} {y} "{text_escaped}" {height} {rotation})'
    else:
        # Use the basic function for non-rotated text
        cmd = f'(c:create-text {x} {y} "{text_escaped}" {height})'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Text created successfully."

# Note: execute_custom_autolisp removed - use specific tools or batch operations instead
# This avoids issues with arbitrary code being pasted as text in AutoCAD

# Additional essential tools from the original server with fast execution

@autocad_mcp.tool()
async def create_polyline(points: List[Tuple[float, float]], closed: bool = False) -> str:
    """Create a polyline from a series of points."""
    pts_str = ""
    for (x, y) in points:
        pts_str += f" (list {x} {y} 0.0)"
    cmd = f"(c:create-polyline (list {pts_str}) {'T' if closed else 'nil'})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Polyline created."

@autocad_mcp.tool()
async def create_rectangle(x1: float, y1: float, x2: float, y2: float,
                          layer: Optional[str] = None) -> str:
    """Create a rectangle using two opposite corners."""
    layer_part = f' "{layer}"' if layer else " nil"
    cmd = f"(c:create-rectangle {x1} {y1} {x2} {y2}{layer_part})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Rectangle created."

@autocad_mcp.tool()
async def insert_block(block_name: str, x: float, y: float,
                      scale: float = 1.0, rotation: float = 0.0,
                      block_id: Optional[str] = None) -> str:
    """Insert a block at specified location with optional ID attribute."""
    id_part = f' "{block_id}"' if block_id else ""
    cmd = f'(c:insert-block "{block_name}" {x} {y} {scale} {rotation}{id_part})'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Block '{block_name}' inserted."

@autocad_mcp.tool()
async def set_layer_properties(layer_name: str, color: str, linetype: str = "CONTINUOUS",
                              lineweight: str = "Default", plot_style: str = "ByLayer",
                              transparency: int = 0) -> str:
    """Create or modify a layer with specified properties."""
    cmd = f'(c:create_or_set_layer "{layer_name}" "{color}" "{linetype}" "{lineweight}" "{plot_style}" {transparency})'
    success, message = execute_lisp_command_fast(cmd)
    if success:
        return (f"Layer '{layer_name}' created/updated. "
                f"Properties: color={color}, linetype={linetype}")
    else:
        return message

@autocad_mcp.tool()
async def move_last_entity(delta_x: float, delta_y: float) -> str:
    """Move the most recently created entity."""
    cmd = f"(c:move-last-entity {delta_x} {delta_y})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Entity moved."

# P&ID specific tools

@autocad_mcp.tool()
async def setup_pid_layers() -> str:
    """Create standard layers for P&ID drawings."""
    cmd = "(c:setup-pid-layers)"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "P&ID layers created successfully."

@autocad_mcp.tool()
async def insert_pid_symbol(category: str, symbol_name: str, x: float, y: float,
                           scale: float = 1.0, rotation: float = 0.0) -> str:
    """Insert a P&ID symbol from the CTO library.
    
    Categories: ACTUATORS, ANNOTATION, ELECTRICAL, EQUIPMENT, FUNCTION, 
                INSTRUMENTS, PIPING, PRIMARY_ELEMENTS, PUMPS-BLOWERS, 
                REGULATORS, TANKS, VALVES"""
    cmd = f'(c:insert-pid-block "{category}" "{symbol_name}" {x} {y} {scale} {rotation})'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Inserted {symbol_name} from {category}"

@autocad_mcp.tool()
async def draw_process_line(x1: float, y1: float, x2: float, y2: float) -> str:
    """Draw a process line between two points."""
    cmd = f"(c:draw-process-line {x1} {y1} {x2} {y2})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Process line drawn."

@autocad_mcp.tool()
async def connect_equipment(x1: float, y1: float, x2: float, y2: float) -> str:
    """Connect two equipment with orthogonal process line routing."""
    cmd = f"(c:connect-equipment {x1} {y1} {x2} {y2})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Equipment connected."

@autocad_mcp.tool()
async def add_flow_arrow(x: float, y: float, rotation: float = 0.0) -> str:
    """Add a flow arrow at specified location."""
    cmd = f"(c:add-flow-arrow {x} {y} {rotation})"
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Flow arrow added."

@autocad_mcp.tool()
async def add_equipment_tag(x: float, y: float, tag: str, description: str = "") -> str:
    """Add equipment tag and description."""
    desc_escaped = description.replace('"', '\\"')
    cmd = f'(c:add-equipment-tag {x} {y} "{tag}" "{desc_escaped}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Equipment tagged: {tag}"

@autocad_mcp.tool()
async def add_line_number(x: float, y: float, line_num: str, spec: str) -> str:
    """Add line number with specification."""
    cmd = f'(c:add-line-number {x} {y} "{line_num}" "{spec}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Line number added: {line_num}-{spec}"

@autocad_mcp.tool()
async def insert_valve(x: float, y: float, valve_type: str = "GATE", 
                      rotation: float = 0.0) -> str:
    """Insert a valve. Types: GATE, GLOBE, CHECK, BALL, BUTTERFLY"""
    cmd = f'(c:insert-valve-on-line {x} {y} "{valve_type}" {rotation})'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"{valve_type} valve inserted."

@autocad_mcp.tool()
async def insert_instrument(x: float, y: float, instrument_type: str,
                           rotation: float = 0.0) -> str:
    """Insert an instrument. Types: FLOW, PRESSURE, TEMPERATURE, LEVEL"""
    cmd = f'(c:insert-instrument {x} {y} "{instrument_type}" {rotation})'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"{instrument_type} instrument inserted."

@autocad_mcp.tool()
async def insert_pump(x: float, y: float, pump_type: str = "CENTRIFUGAL",
                     rotation: float = 0.0) -> str:
    """Insert a pump. Types: CENTRIFUGAL, DIAPHRAGM, GEAR"""
    cmd = f'(c:insert-pump {x} {y} "{pump_type}" {rotation})'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"{pump_type} pump inserted."

@autocad_mcp.tool()
async def insert_tank(x: float, y: float, tank_type: str = "VERTICAL",
                     scale: float = 1.0) -> str:
    """Insert a tank. Types: VERTICAL, HORIZONTAL, CONE"""
    cmd = f'(c:insert-tank {x} {y} "{tank_type}" {scale})'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"{tank_type} tank inserted."

@autocad_mcp.tool()
async def list_pid_symbols(category: str) -> str:
    """List available P&ID symbols in a category."""
    import glob
    path = f"C:/PIDv4-CTO/{category}/*.dwg"
    files = glob.glob(path)
    symbols = [os.path.splitext(os.path.basename(f))[0] for f in files]
    if symbols:
        return f"Available symbols in {category}: " + ", ".join(sorted(symbols)[:20])
    else:
        return f"No symbols found in category: {category}"

@autocad_mcp.tool()
async def create_simple_pid_example() -> str:
    """Create a simple P&ID example with tank, pump, and valve."""
    # This demonstrates how the AI can chain tools to create complex drawings
    results = []
    
    # Set up layers
    cmd = "(c:setup-pid-layers)"
    success, msg = execute_lisp_command_fast(cmd)
    results.append("Layers created" if success else msg)
    
    # Insert tank at (0, 0)
    cmd = '(c:insert-tank 0 0 "VERTICAL" 2.0)'
    success, msg = execute_lisp_command_fast(cmd)
    results.append("Tank inserted" if success else msg)
    
    # Add tank tag
    cmd = '(c:add-equipment-tag 0 15 "TK-101" "Feed Tank")'
    success, msg = execute_lisp_command_fast(cmd)
    results.append("Tank tagged" if success else msg)
    
    # Insert pump at (30, -5)
    cmd = '(c:insert-pump 30 -5 "CENTRIFUGAL" 0)'
    success, msg = execute_lisp_command_fast(cmd)
    results.append("Pump inserted" if success else msg)
    
    # Connect tank to pump
    cmd = "(c:connect-equipment 10 0 30 -5)"
    success, msg = execute_lisp_command_fast(cmd)
    results.append("Connected" if success else msg)
    
    # Add valve on line
    cmd = '(c:insert-valve-on-line 20 -2.5 "GATE" 0)'
    success, msg = execute_lisp_command_fast(cmd)
    results.append("Valve added" if success else msg)
    
    # Add flow arrow
    cmd = "(c:add-flow-arrow 25 -3.5 0)"
    success, msg = execute_lisp_command_fast(cmd)
    results.append("Flow arrow added" if success else msg)
    
    return "Simple P&ID created: " + ", ".join(results)

# Block attribute handling tools

@autocad_mcp.tool()
async def insert_block_with_attributes(block_path: str, x: float, y: float,
                                      scale: float = 1.0, rotation: float = 0.0,
                                      attributes: List[str] = None) -> str:
    """Insert a block with attribute values.
    
    Args:
        block_path: Full path to the .dwg file
        x, y: Insertion point
        scale: Block scale factor
        rotation: Rotation in degrees
        attributes: List of attribute values in order they appear in block
    """
    if attributes is None:
        attributes = []
    
    # Format attributes for LISP
    attrib_list = " ".join([f'"{attr}"' for attr in attributes])
    cmd = f'(c:insert-block-with-attribs "{block_path}" {x} {y} {scale} {rotation} (list {attrib_list}))'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else "Block inserted with attributes."

@autocad_mcp.tool()
async def update_block_attribute(x: float, y: float, tag_name: str, new_value: str) -> str:
    """Update a specific attribute on the nearest block to the given point.
    
    Args:
        x, y: Point near the block to update
        tag_name: The attribute tag name (e.g., "TAG", "DESCRIPTION")
        new_value: New value for the attribute
    """
    value_escaped = new_value.replace('"', '\\"')
    cmd = f'(c:update-block-attribs {x} {y} "{tag_name}" "{value_escaped}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Updated {tag_name} to: {new_value}"

@autocad_mcp.tool()
async def insert_pid_equipment_with_attribs(category: str, symbol_name: str,
                                           x: float, y: float, scale: float = 1.0,
                                           rotation: float = 0.0, equipment_no: str = "",
                                           equipment_type: str = "", manufacturer: str = "",
                                           model_no: str = "", line_no: str = "",
                                           capacity: str = "") -> str:
    """Insert P&ID equipment with proper CTO block attributes.
    
    Args:
        category: CTO category (e.g., "EQUIPMENT", "TANKS", "PUMPS-BLOWERS")
        symbol_name: Symbol name (e.g., "TANK-VERTICAL_OPEN", "PUMP-CENTRIF1")
        x, y: Insertion point
        scale: Scale factor (default 1.0)
        rotation: Rotation in degrees (default 0.0)
        equipment_no: Equipment number/tag (e.g., "P-101", "TK-201")
        equipment_type: Type of equipment (e.g., "Centrifugal Pump", "Storage Tank")
        manufacturer: Equipment manufacturer
        model_no: Model number
        line_no: Associated line number
        capacity: Equipment capacity (tanks only)
    """
    # Escape quotes in string parameters - handle empty strings properly
    equipment_no = equipment_no.replace('"', '\\"') if equipment_no else ""
    equipment_type = equipment_type.replace('"', '\\"') if equipment_type else ""
    manufacturer = manufacturer.replace('"', '\\"') if manufacturer else ""
    model_no = model_no.replace('"', '\\"') if model_no else ""
    line_no = line_no.replace('"', '\\"') if line_no else ""
    capacity = capacity.replace('"', '\\"') if capacity else ""
    
    cmd = f'(c:insert-pid-equipment "{category}" "{symbol_name}" {x} {y} {scale} {rotation} "{equipment_no}" "{equipment_type}" "{manufacturer}" "{model_no}" "{line_no}" "{capacity}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Inserted {symbol_name} with equipment number {equipment_no}"

@autocad_mcp.tool()
async def insert_valve_with_attributes(x: float, y: float, valve_type: str,
                                      equipment_type: str = "", manufacturer: str = "",
                                      model_no: str = "", va_size: str = "",
                                      va_no: str = "", line_no: str = "") -> str:
    """Insert a valve with proper CTO block attributes.
    
    Args:
        x, y: Insertion point
        valve_type: GATE, GLOBE, CHECK, BALL, or BUTTERFLY
        equipment_type: Type of valve (e.g., "Gate Valve")
        manufacturer: Valve manufacturer
        model_no: Model number
        va_size: Valve size (e.g., "6\"")
        va_no: Valve number/tag (e.g., "V-101")
        line_no: Associated line number
    """
    # Escape quotes in string parameters
    equipment_type = equipment_type.replace('"', '\\"') if equipment_type else '""'
    manufacturer = manufacturer.replace('"', '\\"') if manufacturer else '""'
    model_no = model_no.replace('"', '\\"') if model_no else '""'
    va_size = va_size.replace('"', '\\"') if va_size else '""'
    va_no = va_no.replace('"', '\\"') if va_no else '""'
    line_no = line_no.replace('"', '\\"') if line_no else '""'
    
    cmd = f'(c:insert-valve-with-attributes {x} {y} "{valve_type}" "{equipment_type}" "{manufacturer}" "{model_no}" "{va_size}" "{va_no}" "{line_no}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Inserted {valve_type} valve {va_no}"

@autocad_mcp.tool()
async def insert_instrument_with_attributes(x: float, y: float, instrument_type: str,
                                          tag_id: str, range_value: str = "") -> str:
    """Insert an instrument with TAG and RANGE attributes.
    
    Args:
        x, y: Insertion point
        instrument_type: PRESSURE, TEMPERATURE, FLOW, or LEVEL
        tag_id: Instrument tag (e.g., "PT-101", "FT-201")
        range_value: Instrument range (e.g., "0-100 PSI", "0-500 GPM")
    """
    range_escaped = range_value.replace('"', '\\"')
    cmd = f'(c:insert-instrument-with-tag {x} {y} "{instrument_type}" "{tag_id}" "{range_escaped}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Inserted {instrument_type} instrument {tag_id}"

@autocad_mcp.tool()
async def insert_equipment_tag(x: float, y: float, equipment_tag: str) -> str:
    """Insert ANNOT-EQUIP_TAG block with equipment number.
    
    Args:
        x, y: Insertion point
        equipment_tag: Equipment tag/number (e.g., "P-101", "TK-201")
    """
    tag_escaped = equipment_tag.replace('"', '\\"')
    cmd = f'(c:insert-equipment-tag {x} {y} "{tag_escaped}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Inserted equipment tag: {equipment_tag}"

@autocad_mcp.tool()
async def insert_equipment_description(x: float, y: float, equipment_name: str,
                                      description1: str = "", description2: str = "",
                                      description3: str = "", description4: str = "",
                                      description5: str = "", description6: str = "") -> str:
    """Insert ANNOT-EQUIP_DESCR block with equipment description.
    
    Args:
        x, y: Insertion point
        equipment_name: Equipment name (will be underlined)
        description1-6: Additional description lines
    """
    # Escape quotes in string parameters
    equipment_name = equipment_name.replace('"', '\\"') if equipment_name else '""'
    description1 = description1.replace('"', '\\"') if description1 else '""'
    description2 = description2.replace('"', '\\"') if description2 else '""'
    description3 = description3.replace('"', '\\"') if description3 else '""'
    description4 = description4.replace('"', '\\"') if description4 else '""'
    description5 = description5.replace('"', '\\"') if description5 else '""'
    description6 = description6.replace('"', '\\"') if description6 else '""'
    
    cmd = f'(c:insert-equipment-description {x} {y} "{equipment_name}" "{description1}" "{description2}" "{description3}" "{description4}" "{description5}" "{description6}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Inserted equipment description: {equipment_name}"

@autocad_mcp.tool()
async def insert_line_number_tag(x: float, y: float, line_number: str) -> str:
    """Insert ANNOT-LINE_NUMBER block with line number.
    
    Args:
        x, y: Insertion point
        line_number: Line number (e.g., "2\"-WW-001")
    """
    line_escaped = line_number.replace('"', '\\"')
    cmd = f'(c:insert-line-number {x} {y} "{line_escaped}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Inserted line number: {line_number}"

@autocad_mcp.tool()
async def edit_last_block_attribute(tag_name: str, new_value: str) -> str:
    """Edit an attribute on the last inserted block.
    
    Useful for updating attributes after insertion.
    """
    value_escaped = new_value.replace('"', '\\"')
    cmd = f'(c:edit-last-block-attrib "{tag_name}" "{value_escaped}")'
    success, message = execute_lisp_command_fast(cmd)
    return message if not success else f"Updated {tag_name} on last block"

def initialize_autocad_lisp_fast():
    """Fast initialization - load only essential LISP files.
    Note: LISP file loading still uses 3s delay for security prompts,
    but all other operations use fast delays."""
    global acad_window, lisp_path
    
    logger.info("Fast initialization starting...")
    logger.info("LISP files will load with 3s delay for security prompts")
    logger.info("All other operations will use fast mode delays")
    
    acad_window = find_autocad_window()
    if not acad_window:
        logger.error("AutoCAD LT window not found")
        return False
    
    # Load essential files including those for added tools
    essential_files = [
        "error_handling.lsp",
        "basic_shapes.lsp",
        "batch_operations.lsp",  # New batch operations file
        "advanced_geometry.lsp",  # For polylines
        "advanced_entities.lsp",  # For rectangles
        "drafting_helpers.lsp",   # For blocks and layers
        "entity_modification.lsp", # For move operations
        "pid_tools.lsp",         # P&ID specific tools
        "attribute_tools.lsp"    # Block attribute handling
    ]
    
    for f in essential_files:
        full_path = os.path.join(lisp_path, f)
        if os.path.exists(full_path):
            # Use traditional loading with 3s delay for security prompts
            success, message = load_lisp_file_with_delay(full_path)
            if success:
                logger.info(f"Loaded {f}")
            else:
                logger.error(f"Failed to load {f}: {message}")
    
    logger.info("Fast initialization complete")
    return True

if __name__ == "__main__":
    logger.info("AutoCAD LT MCP Server (Fast Version) starting...")
    if initialize_autocad_lisp_fast():
        logger.info("Successfully initialized AutoCAD LT with fast LISP libraries.")
    else:
        logger.warning("Failed to initialize AutoCAD LT with LISP. Will retry on tool calls.")
    autocad_mcp.run(transport='stdio')