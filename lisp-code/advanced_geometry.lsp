;; advanced_geometry.lsp
;; Provides additional geometry creation and manipulation:
;; polylines, rectangles, transformations, fillet/chamfer stubs.

;; Using absolute paths for dependencies
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/error_handling.lsp")
(load "C:/Users/hvksh/mcp-servers/autocad-mcp/lisp-code/drafting_helpers.lsp")

;; Example: create a polyline from a list of points.
(defun c:create-polyline (ptlist closedFlag / current-layer)
  (if (or (null ptlist) (< (length ptlist) 2))
    (report-error "Need at least two points for a polyline.")
  )
  ;; Save and restore current layer
  (setq current-layer (getvar "CLAYER"))
  ;; Ensure we're using the current layer
  (setvar "CLAYER" current-layer)
  
  (command "_pline")
  (foreach p ptlist
    (command p)
  )
  (if closedFlag
    (command "C")
  )
  (command "")
  (princ "\nCreated polyline.")
  (entlast)
)

;; Move an entity by delta
(defun c:move-entity (ent delta-x delta-y / start end)
  (setq start (list 0.0 0.0 0.0))
  (setq end   (list delta-x delta-y 0.0))
  (command "_MOVE" ent "" start end)
  (princ "\nEntity moved.")
)

;; Rotate an entity around a specified base point by degrees
(defun c:rotate-entity (ent base-x base-y angleDeg / base angleRad)
  (setq base (list base-x base-y 0.0))
  (setq angleRad (* pi (/ angleDeg 180.0)))
  (command "_ROTATE" ent "" base angleRad)
  (princ (strcat "\nRotated entity by " (rtos angleDeg 2 2) " degrees." ))
)

;; Rotate by ID
(defun c:rotate_entity_by_id (id_value base_x base_y angleDeg / ent)
  (setq ent (find_block_by_id id_value))
  (if ent
    (c:rotate-entity ent base_x base_y angleDeg)
    (report-error (strcat "No block found with ID: " id_value))
  )
)

;; Fillet, Chamfer, Mirror, Array stubs can go here.

(princ "\nAdvanced geometry features loaded.\n")
(princ)
