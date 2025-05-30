@echo off
echo ===================================
echo Manual LISP Loader for AutoCAD
echo ===================================
echo.
echo This script will help you manually load all LISP files
echo with enough time to accept each security prompt.
echo.
echo 1. Make sure AutoCAD is running with a drawing open
echo 2. After each file loads, you'll have time to accept the security prompt
echo 3. Press any key to continue to the next file
echo.
pause

echo Loading error_handling.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/error_handling.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo Loading basic_shapes.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/basic_shapes.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo Loading drafting_helpers.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/drafting_helpers.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo Loading block_id_helpers.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/block_id_helpers.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo Loading selection_and_file.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/selection_and_file.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo Loading advanced_geometry.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/advanced_geometry.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo Loading advanced_entities.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/advanced_entities.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo Loading entity_modification.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/entity_modification.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo Loading annotation_helpers.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/annotation_helpers.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo Loading layout_management.lsp...
echo Copy and paste this command in AutoCAD:
echo (load "lisp-code/layout_management.lsp")
echo.
echo Press any key after accepting the security prompt...
pause > nul

echo.
echo ===================================
echo All LISP files loaded successfully!
echo You can now start the MCP server.
echo ===================================
pause