;; annotation_helpers.lsp
;; Dimensions, Leaders, Multileaders, Hatching, Tables, etc. (partial stubs).

;; (load "error_handling.lsp")

(defun c:create-linear-dim (x1 y1 x2 y2 dimX dimY / pt1 pt2 dimLinePt)
  (setq pt1 (list x1 y1 0.0))
  (setq pt2 (list x2 y2 0.0))
  (setq dimLinePt (list dimX dimY 0.0))
  (command "_dimlinear" pt1 pt2 dimLinePt "")
  (princ "\nLinear dimension created.")
)

(defun c:hatch_closed_poly_by_id (id_value hatch_pattern / ent)
  (setq ent (find_block_by_id id_value))
  (if ent
    (progn
      (command "_HATCH" "P" hatch_pattern "" "S" "L" "")
      (princ "\nHatch applied (pattern: ")(princ hatch_pattern)(princ ")"))
    (report-error (strcat "No entity found with ID: " id_value))
  )
)

(princ "\nAnnotation helpers loaded.\n")
(princ)
