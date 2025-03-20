# AutoCAD LT AutoLISP MCP Server

This MCP server enables natural language control of AutoCAD LT 2024/2025 through AutoLISP code generation and execution. It bridges Claude or other LLM clients with AutoCAD LT for creating engineering drawings through conversational prompts.

## Features

- Generates and executes AutoLISP code in AutoCAD LT
- Creates process engineering symbols (pumps, vessels, heat exchangers)
- Draws piping connections and complete process diagrams
- Provides direct access to AutoLISP for custom drawing operations
- Supports text-to-CAD functionality through natural language

## Prerequisites

- AutoCAD LT 2024 or newer (with AutoLISP support)
- Python 3.10 or higher
- Claude Desktop or other MCP client application

## Setup Instructions

1. **Install Dependencies**:
   ```
   cd pathto\mcp-servers\autocad-mcp
   python -m venv venv
   venv\Scripts\activate
   pip install mcp[cli] keyboard pyperclip pywin32
   ```

2. **Configure Claude Desktop**:
   - Open Claude Desktop settings
   - Edit the configuration file to include:
   ```json
   {
     "mcpServers": {
       "autocad-lisp": {
         "command": "pathto\\mcp-servers\\autocad-mcp\\venv\\Scripts\\python.exe",
         "args": ["pathto\\mcp-servers\\autocad-mcp\\server_lisp.py"]
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
- `create_equipment_symbol`: Draw process equipment symbols (vessel, pump, exchanger)
- `create_pipe`: Connect equipment with pipe lines
- `create_simple_pfd`: Create a complete process flow diagram
- `execute_custom_autolisp`: Run custom AutoLISP code directly

## Usage Examples

1. **Basic Drawing Operations**:
   - "Draw a line from coordinates (100,100) to (200,150)"
   - "Create a circle at (150,150) with radius 25"
   - "Add text 'Cooling System' at position (100,200)"

2. **Process Equipment**:
   - "Draw a pump at (100,100) with tag P-101"
   - "Create a vessel at (200,150) labeled TK-101"
   - "Place a heat exchanger at (150,120)"

3. **Process Flow Diagrams**:
   - "Create a simple process flow diagram starting at (50,100)"
   - "Draw a pump feeding into a heat exchanger and then to a storage vessel"
   - "Create a PFD for a water treatment system with feed pump, filter, and storage tank"

4. **Custom AutoLISP**:
   - "Execute this AutoLISP code to create a custom piping configuration: (defun c:create-pipe-bend ...)"

## Limitations

- Requires AutoCAD LT 2024 or newer with AutoLISP support
- Relies on window focus and keyboard simulation for command execution
- User should not interact with AutoCAD while commands are being sent
- Limited to 2D drawing operations

## Troubleshooting

- If connection fails, ensure AutoCAD LT is running with a drawing open
- Verify window title contains "AutoCAD LT" and "Drawing"
- Run the server as Administrator
- Check that your AutoCAD LT version supports AutoLISP (2024 or newer)
- Look at server console for detailed error messages
