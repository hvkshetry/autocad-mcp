# Changelog

All notable changes to the AutoCAD MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-12-XX

### 🚀 Major Features Added

#### P&ID and Process Engineering Support
- **CTO Library Integration**: Full support for CAD Tools Online P&ID Symbol Library (600+ symbols)
- **Industry Standard Symbols**: Complete ISA 5.1-2009 compliant symbol set
- **Intelligent Attribute Handling**: Proper block attributes for equipment schedules and valve lists
- **Process Equipment Tools**: Pumps, valves, tanks, instruments with proper categorization
- **Annotation System**: Equipment tags, descriptions, and line numbers

#### Performance Optimization
- **Fast Mode Server** (`server_lisp_fast.py`): 80% performance improvement
- **Batch Operations**: Create multiple objects in single operations
- **Clipboard Integration**: Efficient execution of large LISP scripts
- **Smart Loading**: Essential files only for faster startup

#### Enhanced Drawing Tools
- **Advanced Geometry**: Rectangles, arcs, ellipses with proper parameterization
- **Text Rotation**: Full rotation support for text entities
- **Attribute Management**: Complete block attribute creation and modification
- **Layer Organization**: Industry-standard P&ID layer structure

### 🔧 Technical Improvements

#### New LISP Files
- `pid_tools.lsp`: P&ID-specific drawing operations
- `attribute_tools.lsp`: Block attribute handling using entget/entmod
- `batch_operations.lsp`: Performance-optimized batch object creation

#### New Python Tools
- `insert_pid_equipment_with_attribs`: Equipment insertion with CTO attributes
- `insert_valve_with_attributes`: Valve insertion with proper attributes
- `insert_equipment_tag`: Equipment identification tags
- `insert_equipment_description`: Equipment description blocks
- `insert_line_number_tag`: Process line identification
- `setup_pid_layers`: Standard P&ID layer creation
- `batch_create_*`: High-performance batch operations

#### Attribute System Overhaul
- **Proper CTO Attributes**: EQUIPMENT-TYPE, MANUFACTURER, MODEL-NO, etc.
- **No Prompt Interference**: ATTREQ=0 during insertion, entget/entmod for updates
- **Equipment Extraction Ready**: Attributes suitable for schedules and lists
- **Category-Specific Handling**: Different attributes for equipment types

### 🛠️ Bug Fixes
- Fixed command timing issues with attribute prompts
- Resolved AutoCAD help menu opening during execution
- Corrected text creation parameter order and rotation support
- Improved error handling for missing block definitions
- Enhanced window focus detection and handling

### 📚 Documentation
- **Complete README Rewrite**: Current implementation and features
- **Installation Guide**: Step-by-step setup for both CTO and non-CTO users
- **Enhanced Troubleshooting**: CTO library issues and attribute handling
- **Performance Guide**: Optimization strategies and batch operations
- **User Guides**: Clear separation for different user scenarios

### 🔄 Breaking Changes
- **Server Selection**: Users must choose between `server_lisp.py` and `server_lisp_fast.py`
- **Attribute Parameters**: Updated function signatures for proper CTO attributes
- **File Dependencies**: New LISP files required for full functionality

### 🎯 User Experience
- **Clear Setup Paths**: Separate instructions for CTO and non-CTO users
- **Graceful Degradation**: Basic functionality available without CTO library
- **Performance Feedback**: Clear speed improvements with batch operations
- **Error Prevention**: Better validation and user guidance

## [1.0.0] - 2024-XX-XX

### Initial Release Features
- Basic AutoLISP code generation and execution
- Core drawing operations (lines, circles, text)
- Block insertion and manipulation
- Layer management
- Connection to AutoCAD LT through keyboard simulation
- MCP server integration with Claude Desktop

### Core Tools
- `create_line`: Basic line drawing
- `create_circle`: Circle creation
- `create_text`: Text placement
- `insert_block`: Block insertion
- `set_layer_properties`: Layer management
- `execute_custom_autolisp`: Direct LISP execution

### Infrastructure
- Python MCP server framework
- AutoCAD window detection and focus
- LISP file loading system
- Error handling and validation
- Basic troubleshooting documentation

---

## Migration Guide from v1.0 to v2.0

### For Existing Users

#### If You Have CTO Library
1. **Update Claude Configuration**:
   ```json
   "args": ["path\\to\\server_lisp_fast.py"]
   ```

2. **Add CTO Path to Trusted Locations**:
   - AutoCAD: OPTIONS → Files → Trusted Locations
   - Add: `C:\PIDv4-CTO\`

3. **Test P&ID Functionality**:
   ```
   "Set up P&ID layers"
   "Insert a gate valve at (100,100)"
   ```

#### If You Don't Have CTO Library
1. **Keep Current Configuration**:
   ```json
   "args": ["path\\to\\server_lisp.py"]
   ```

2. **All Existing Tools Work**: No changes to basic functionality

3. **New Performance Features**: Batch operations available in both servers

### New Features to Try

#### Batch Operations (All Users)
```
"Create 10 circles arranged in a 5x2 grid pattern"
"Draw multiple lines to create a simple floor plan"
```

#### P&ID Tools (CTO Users Only)
```
"Create a simple process with tank, pump, and valve"
"Insert equipment with proper tags and attributes"
"Set up standard wastewater treatment layers"
```

---

## Future Roadmap

### Planned for v2.1
- [ ] Advanced P&ID routing algorithms
- [ ] Equipment schedule generation
- [ ] Pipe sizing calculations
- [ ] Custom symbol library support

### Planned for v2.2
- [ ] 3D isometric P&ID views
- [ ] Integration with process simulation tools
- [ ] Automated equipment numbering
- [ ] Drawing template management

### Under Consideration
- [ ] AutoCAD full version support
- [ ] Linux/Mac compatibility
- [ ] Web-based interface
- [ ] Database integration for equipment data