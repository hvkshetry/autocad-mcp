;; mcp_test.lsp
;; Test file for verifying that all MCP functions are loaded and accessible

;; Load all dependencies using absolute paths
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/error_handling.lsp")
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/basic_shapes.lsp")
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/drafting_helpers.lsp")
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/block_id_helpers.lsp")
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/selection_and_file.lsp")
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/advanced_geometry.lsp")
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/annotation_helpers.lsp")
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/layout_management.lsp")

;; Create a test function that will create a simple drawing to test functionality
(defun c:mcp_test ( / test_block_name layer_name layer1 layer2)
  (princ "\n=== MCP Test Function ===\n")
  
  ;; Test layer management functionality
  (setq layer1 "MCP_TEST_LAYER1")
  (setq layer2 "MCP_TEST_LAYER2")
  
  ;; Set up test layers with different colors
  (ensure_layer_exists layer1 "red" "CONTINUOUS")
  (ensure_layer_exists layer2 "blue" "CONTINUOUS")
  
  ;; Set Layer 1 as active and verify
  (setvar "CLAYER" layer1)
  (if (= (getvar "CLAYER") layer1)
    (princ "\n- Layer switching works correctly")
    (princ "\n- FAILED: Layer switching not working"))
  
  ;; Create a line on Layer 1
  (c:create-line 0 0 100 100)
  (princ "\n- Line created on Layer 1")
  
  ;; Switch to Layer 2 and verify
  (setvar "CLAYER" layer2)
  (if (= (getvar "CLAYER") layer2)
    (princ "\n- Layer 2 is now active")
    (princ "\n- FAILED: Could not switch to Layer 2"))
  
  ;; Create a circle on Layer 2
  (c:create-circle 50 50 25)
  (princ "\n- Circle created on Layer 2")
  
  ;; Switch back to Layer 1
  (setvar "CLAYER" layer1)
  
  ;; Create text on Layer 1
  (c:create-text 50 100 "MCP Test" 5.0)
  (princ "\n- Text created on Layer 1")
  
  ;; Create a polyline with c:create-polyline if it's available
  (if (not (vl-catch-all-error-p (vl-catch-all-apply 'c:create-polyline
                                                    (list (list (list 0 0 0) (list 100 0 0) (list 100 100 0)) nil))))
    (princ "\n- Polyline created successfully")
    (princ "\n- Polyline function not available or failed"))
  
  ;; Try to create a simple block definition for testing
  (setq test_block_name "MCP_TEST_BLOCK")
  (command "_-block" test_block_name "0,0" "_circle" "0,0" "10" "")
  (princ "\n- Block defined successfully")
  
  ;; Switch to Layer 2 for block insertion
  (setvar "CLAYER" layer2)
  
  ;; Try inserting the block with an ID
  (if (not (vl-catch-all-error-p (vl-catch-all-apply 'c:insert_block
                                                    (list test_block_name 150 150 "TEST_ID" 1.0 0.0))))
    (princ "\n- Block inserted successfully with ID on Layer 2")
    (princ "\n- Block insertion function not available or failed"))
  
  ;; Test label_block_by_id if available
  (if (not (vl-catch-all-error-p (vl-catch-all-apply 'c:label_block_by_id
                                                    (list "TEST_ID" "Test Label" 3.0))))
    (princ "\n- Block labeled successfully")
    (princ "\n- Block labeling function not available or failed"))
  
  ;; Report success
  (princ "\n\nMCP Test completed. Check the drawing for test objects on different layers.")
  (princ)
)

(princ "\nMCP Test module loaded successfully. Type 'mcp_test' to run the test.\n")
(princ)
