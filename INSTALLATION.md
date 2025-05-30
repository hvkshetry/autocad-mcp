# AutoCAD MCP Server - Installation Guide

This guide provides step-by-step instructions for installing and configuring the AutoCAD MCP Server.

## 📋 Prerequisites Check

Before starting, verify you have:

- [ ] **AutoCAD LT 2024 or newer** with AutoLISP support
- [ ] **Python 3.10 or higher** installed
- [ ] **Claude Desktop** or other MCP client
- [ ] **Windows 10/11** (for window automation)
- [ ] **Administrator access** (for initial setup)

### Optional: CTO P&ID Library
- [ ] CAD Tools Online P&ID Symbol Library installed at `C:\PIDv4-CTO\`

## 🚀 Quick Start Installation

### 1. Download and Setup Repository

```bash
# Clone the repository
git clone https://github.com/hvkshetry/autocad-mcp.git
cd autocad-mcp

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Choose Your Configuration

#### Option A: Full Installation (With CTO Library)
**Use this if you have the CAD Tools Online P&ID Symbol Library**

1. **Verify CTO Installation**:
   - Check that `C:\PIDv4-CTO\` exists
   - Verify subdirectories: `VALVES\`, `EQUIPMENT\`, `PUMPS-BLOWERS\`, `TANKS\`, etc.
   - Confirm .dwg files exist in subdirectories

2. **Claude Desktop Configuration**:
   Create or edit `%APPDATA%\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "autocad-mcp": {
         "command": "C:\\path\\to\\autocad-mcp\\venv\\Scripts\\python.exe",
         "args": ["C:\\path\\to\\autocad-mcp\\server_lisp_fast.py"]
       }
     }
   }
   ```

3. **Start the Server**:
   ```bash
   start_fast_server.bat
   ```

#### Option B: Basic Installation (Without CTO Library)
**Use this if you don't have the CTO library**

1. **Claude Desktop Configuration**:
   Create or edit `%APPDATA%\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "autocad-mcp": {
         "command": "C:\\path\\to\\autocad-mcp\\venv\\Scripts\\python.exe",
         "args": ["C:\\path\\to\\autocad-mcp\\server_lisp.py"]
       }
     }
   }
   ```

2. **Start the Server**:
   ```bash
   start_lisp_server.bat
   ```

### 3. AutoCAD Setup

1. **Launch AutoCAD LT 2024+**
2. **Create or open a drawing**
3. **Ensure command line is visible** (type `COMMANDLINE` if hidden)
4. **Add to Trusted Paths** (recommended):
   - Type `OPTIONS` → Files tab → Trusted Locations
   - Add your `autocad-mcp\lisp-code` directory

### 4. Test the Installation

```bash
# Run the connection test
test_connection.bat
```

If successful, you should see a line drawn in AutoCAD.

## 🔧 Detailed Configuration

### AutoCAD Security Settings

To avoid LISP loading prompts:

1. **Add Trusted Path**:
   - In AutoCAD: `OPTIONS` → Files → Trusted Locations
   - Add: `C:\path\to\autocad-mcp\lisp-code`

2. **Set Security Variables**:
   ```
   SECURELOAD = 1  (load from trusted paths only)
   ATTREQ = 0      (disable attribute prompts)
   ```

### Claude Desktop Configuration Details

Your final configuration file should look like this:

**For CTO Users (Full Features)**:
```json
{
  "mcpServers": {
    "autocad-mcp": {
      "command": "C:\\Users\\YourName\\autocad-mcp\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourName\\autocad-mcp\\server_lisp_fast.py"],
      "env": {
        "AUTOCAD_VERSION": "2024"
      }
    }
  }
}
```

**For Non-CTO Users (Basic Features)**:
```json
{
  "mcpServers": {
    "autocad-mcp": {
      "command": "C:\\Users\\YourName\\autocad-mcp\\venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourName\\autocad-mcp\\server_lisp.py"],
      "env": {
        "AUTOCAD_VERSION": "2024"
      }
    }
  }
}
```

## 🧪 Testing Your Installation

### Basic Functionality Test

1. **Start AutoCAD** and open a drawing
2. **Start Claude Desktop** 
3. **Test basic commands**:
   ```
   \"Create a line from (0,0) to (100,100)\"
   \"Add a circle at (50,50) with radius 25\"
   \"Add text 'Test' at position (75,75)\"
   ```

### P&ID Functionality Test (CTO Only)

If you have the CTO library:
```
\"Set up P&ID layers\"
\"Insert a gate valve at (100,100)\"
\"List available symbols in VALVES category\"
```

### Performance Test

Test batch operations:
```
\"Create 10 circles arranged in a grid pattern\"
```

This should be much faster than creating circles individually.

## 🔍 Troubleshooting Installation

### Common Issues

1. **"AutoCAD window not found"**
   - Ensure AutoCAD is running with a drawing open
   - Check window title contains "AutoCAD" or drawing name
   - Try running AutoCAD as Administrator

2. **"LISP files fail to load"**
   - Add LISP directory to AutoCAD trusted paths
   - Check file permissions on the lisp-code directory
   - Try manual loading: `(load "path/to/error_handling.lsp")`

3. **"P&ID tools not working"**
   - Verify CTO library installation at `C:\PIDv4-CTO\`
   - Switch to basic server if you don't have CTO library
   - Check file paths in `pid_tools.lsp`

4. **"Python/pip not found"**
   - Install Python 3.10+ from python.org
   - Ensure Python is added to system PATH
   - Try using `py` instead of `python` command

### Manual LISP Loading

If automatic loading fails, load files manually in AutoCAD:

```lisp
; Core files (required)
(load "C:/path/to/autocad-mcp/lisp-code/error_handling.lsp")
(load "C:/path/to/autocad-mcp/lisp-code/basic_shapes.lsp")
(load "C:/path/to/autocad-mcp/lisp-code/drafting_helpers.lsp")

; P&ID files (if you have CTO library)
(load "C:/path/to/autocad-mcp/lisp-code/pid_tools.lsp")
(load "C:/path/to/autocad-mcp/lisp-code/attribute_tools.lsp")

; Test basic functionality
(c:create-line 0 0 100 100)
```

## 📁 Directory Structure

After installation, your directory should look like:

```
autocad-mcp/
├── venv/                          # Python virtual environment
├── lisp-code/                     # AutoLISP files
│   ├── error_handling.lsp         # Core error handling
│   ├── basic_shapes.lsp           # Basic drawing functions
│   ├── pid_tools.lsp              # P&ID operations
│   ├── attribute_tools.lsp        # Block attribute handling
│   └── ...                        # Other LISP files
├── server_lisp.py                 # Basic MCP server
├── server_lisp_fast.py            # Fast MCP server with P&ID
├── start_lisp_server.bat          # Start basic server
├── start_fast_server.bat          # Start fast server
├── test_connection.bat            # Test installation
├── requirements.txt               # Python dependencies
├── README.md                      # Main documentation
├── TROUBLESHOOTING.md             # Problem solving guide
└── INSTALLATION.md                # This file
```

## ✅ Installation Checklist

- [ ] Python 3.10+ installed and accessible
- [ ] Repository cloned and virtual environment created
- [ ] Dependencies installed with pip
- [ ] AutoCAD LT 2024+ running with drawing open
- [ ] Claude Desktop configured with correct server path
- [ ] LISP directory added to AutoCAD trusted paths
- [ ] Connection test successful
- [ ] Basic drawing commands working
- [ ] P&ID commands working (if CTO library installed)

## 🚀 Next Steps

After successful installation:

1. **Read the main documentation**: [README.md](README.md)
2. **Try example workflows**: Create your first P&ID drawing
3. **Review performance tips**: [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md)
4. **Bookmark troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 🆘 Getting Help

If you encounter issues:

1. **Check the troubleshooting guide**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Review common issues**: Most problems are related to paths or AutoCAD setup
3. **File a GitHub issue**: Provide error messages and system details
4. **Include your configuration**: Share (redacted) Claude Desktop config

---

*Installation complete! You're ready to start creating AutoCAD drawings with natural language.*