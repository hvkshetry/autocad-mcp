# AutoCAD LT AutoLISP MCP Server

This MCP server enables natural language control of AutoCAD LT 2024/2025 through AutoLISP code generation and execution. It bridges Claude or other LLM clients with AutoCAD LT for creating engineering drawings through conversational prompts.

## Features

- Generates and executes AutoLISP code in AutoCAD LT
- Creates basic shapes (lines, circles, text)
- Handles block insertion with attribute management
- Supports connecting blocks with lines between named connection points
- Arranges multiple blocks in sequence with custom spacing
- Provides layer creation and management
- Allows direct custom AutoLISP code execution
- Supports text-to-CAD functionality through natural language

## Prerequisites

- AutoCAD LT 2024 or newer (with AutoLISP support)
- Python 3.10 or higher
- Claude Desktop or other MCP client application

## Setup Instructions

1. **Install Dependencies**:
   ```
   git clone https://github.com/your-username/autocad-mcp.git
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

3. **Start AutoCAD LT**:
   - Launch AutoCAD LT
   - Create or open a drawing
   - Make sure the window title contains "AutoCAD LT" and "Drawing"

4. **Start the Server**:
   - Run `start_lisp_server.bat` as Administrator

## Available Tools

- `get_autocad_status`: Check connection to AutoCAD
- `create_line`: Draw a line between two points
- `create_circle`: Create a circle with defined center and radius
- `create_text`: Add text labels at specified coordinates
- `insert_block`: Insert a block with optional ID attribute, scale, and rotation
- `connect_blocks`: Connect two blocks with a line between named connection points
- `label_block`: Add a text label to a block
- `arrange_blocks`: Arrange multiple blocks in a sequence with custom spacing
- `set_layer_properties`: Create or modify layers with color and linetype
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

2. **Block Operations**:
   - "Insert a block named 'PUMP' at position (100,100) with ID 'P-101'"
   - "Label the block with ID 'P-101' as 'Feed Pump'"
   - "Connect block 'P-101' to 'V-201' on the 'Piping' layer"

3. **Multi-Block Operations**:
   - "Arrange blocks 'PUMP', 'VALVE', and 'TANK' starting at (50,100) going right with 30 units spacing"
   - "Create a layer named 'Equipment' with color 'yellow'"

4. **Custom AutoLISP**:
   - "Execute this AutoLISP code to create a custom function: (defun c:my-function ...)"

## Limitations

- Requires AutoCAD LT 2024 or newer with AutoLISP support
- Relies on window focus and keyboard simulation for command execution
- User should not interact with AutoCAD while commands are being sent
- Limited to 2D drawing operations
- Connection points for blocks are currently hard-coded (pointA, pointB)

## Troubleshooting

See the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) file for common issues and solutions.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.