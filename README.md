# AutoCAD LT AutoLISP MCP Server

This MCP server enables natural language control of AutoCAD LT 2024/2025 through AutoLISP code generation and execution. It bridges Claude or other LLM clients with AutoCAD LT for creating engineering drawings through conversational prompts.

## Features

- Generates and executes AutoLISP code in AutoCAD LT
- Creates basic shapes (lines, circles, polylines, text)
- Handles block insertion with attribute management
- Supports connecting blocks with lines between named connection points
- Arranges multiple blocks in sequence with custom spacing
- Provides robust layer creation and management
- Creates hatches and dimensions for technical drawings
- Allows entity rotation and manipulation
- Supports direct custom AutoLISP code execution
- Enables text-to-CAD functionality through natural language

## Prerequisites

- AutoCAD LT 2024 or newer (with AutoLISP support)
- Python 3.10 or higher
- Claude Desktop or other MCP client application

## Setup Instructions

1. **Install Dependencies**:
   ```
   git clone https://github.com/hvkshetry/autocad-mcp.git
   cd autocad-mcp
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Claude Desktop**:
   - Open Claude Desktop settings
   - Edit the configuration file to include:
   ```json
   {
     "mcpServers": {
       "autocad-lisp": {
         "command": "path\\to\\autocad-mcp\\venv\\Scripts\\python.exe",
         "args": ["path\\to\\autocad-mcp\\server_lisp.py"]
       }
     }
   }
   ```

   - Alternatively, you can use the included `claude_desktop_config_lisp.json` as a template

3. **Start AutoCAD LT**:
   - Launch AutoCAD LT
   - Create or open a drawing
   - Make sure the window title contains "AutoCAD LT" and "Drawing"

4. **Start the Server**:
   - Run `start_lisp_server.bat` as Administrator
   - Alternatively, use `restart_fixed_server.bat` if you encounter issues with LISP loading

5. **Test the Connection**:
   - Run `test_connection.bat` to verify proper functionality

## Available Tools

- `get_autocad_status`: Check connection to AutoCAD
- `create_line`: Draw a line between two points
- `create_circle`: Create a circle with defined center and radius
- `create_text`: Add text labels at specified coordinates
- `insert_block`: Insert a block with optional ID attribute, scale, and rotation
- `connect_blocks`: Connect two blocks with a line between named connection points
- `label_block`: Add a text label to a block
- `arrange_blocks`: Arrange multiple blocks in a sequence with custom spacing
- `create_polyline`: Create a polyline from a series of points
- `rotate_entity_by_id`: Rotate an entity around a base point
- `create_linear_dimension`: Add a linear dimension between two points
- `create_hatch`: Add hatching to a closed polyline area
- `set_layer_properties`: Create or modify layers with color, linetype, lineweight, etc.
- `execute_custom_autolisp`: Run custom AutoLISP code directly

## LISP Library Structure

The server loads multiple LISP files for functionality:

1. **error_handling.lsp**: Base error handling and validation functions
2. **basic_shapes.lsp**: Core functions for creating lines, circles, and text
3. **drafting_helpers.lsp**: Functions for block manipulation, layer management, and connecting elements
4. **block_id_helpers.lsp**: Functions for finding and manipulating blocks by ID attribute
5. **selection_and_file.lsp**: Selection set management and file operations
6. **advanced_geometry.lsp**: Extended geometry creation and manipulation
7. **annotation_helpers.lsp**: Text and dimension creation tools
8. **layout_management.lsp**: Functions for managing layouts and viewports

## Usage Examples

1. **Basic Drawing Operations**:
   - "Draw a line from coordinates (100,100) to (200,150)"
   - "Create a circle at (150,150) with radius 25"
   - "Add text 'System Title' at position (100,200)"
   - "Create a polyline with points at (10,10), (50,50), (100,10) and close it"

2. **Block Operations**:
   - "Insert a block named 'PUMP' at position (100,100) with ID 'P-101'"
   - "Label the block with ID 'P-101' as 'Feed Pump'"
   - "Connect block 'P-101' to 'V-201' on the 'Piping' layer"
   - "Rotate the block 'P-101' by 45 degrees around its insertion point"

3. **Multi-Block Operations**:
   - "Arrange blocks 'PUMP', 'VALVE', and 'TANK' starting at (50,100) going right with 30 units spacing"
   - "Create a layer named 'Equipment' with color 'yellow'"
   - "Add a dimension between the two blocks showing the distance"

4. **Advanced Operations**:
   - "Create a closed polyline and add ANSI31 hatching inside it"
   - "Create a dimension showing the diameter of the circle"
   - "Set the current layer to 'Dimensions' with color 'cyan' and lineweight '0.30mm'"

5. **Custom AutoLISP**:
   - "Execute this AutoLISP code to create a custom function: (defun c:my-function ...)"

## Limitations

- Requires AutoCAD LT 2024 or newer with AutoLISP support
- Relies on window focus and keyboard simulation for command execution
- User should not interact with AutoCAD while commands are being sent
- Limited to 2D drawing operations
- Connection points for blocks use predefined connection point names (CONN_DEFAULT1, CONN_DEFAULT2)
- Layer colors must be specified as strings (e.g., "red", "yellow", "120")

## Troubleshooting

See the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) file for common issues and solutions. Common issues include:

- LISP files failing to load
- Window focus issues with AutoCAD
- Function cancelled errors
- Communication problems between the server and AutoCAD

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
