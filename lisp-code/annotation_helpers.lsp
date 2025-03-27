;; annotation_helpers.lsp
;; Dimensions, Leaders, Multileaders, Hatching, Tables, etc.
;; Many features are partial or stubs, as they can be complex or restricted in LT.

;; Using absolute path for dependencies
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/error_handling.lsp")
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/block_id_helpers.lsp") ;; Needed for find_block_by_id

(defun c:create-linear-dim (x1 y1 x2 y2 dimX dimY / pt1 pt2 dimLinePt current-layer)
  ;; Enhanced linear dimension with improved precision
  ;; Convert to exact floats to avoid rounding issues
  (setq pt1 (list (float x1) (float y1) 0.0))
  (setq pt2 (list (float x2) (float y2) 0.0))
  (setq dimLinePt (list (float dimX) (float dimY) 0.0))
  
  ;; Save current layer
  (setq current-layer (getvar "CLAYER"))
  ;; Ensure we're using the current layer
  (setvar "CLAYER" current-layer)
  
  ;; Use command sequence with exact coordinates
  (command "_dimlinear")
  (command pt1)
  (command pt2)
  (command dimLinePt)
  (princ "\nLinear dimension created.")
  (entlast)
)

(defun c:hatch_closed_poly_by_id (id_value hatch_pattern / ent)
  (setq ent (find_block_by_id id_value))
  (if ent
    (progn
      ;; In real usage, we'd check if ent is a polyline, or
      ;; let the user select. This is just a placeholder.
      (command "_HATCH" hatch_pattern "" "P" ent "")
      (princ "\nHatch applied to entity by ID.")
    )
    (report-error (strcat "No entity found with ID: " id_value))
  )
)

(princ "\nAnnotation helpers loaded.\n")
(princ)
