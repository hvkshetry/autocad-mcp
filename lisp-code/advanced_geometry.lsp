;; advanced_geometry.lsp
;; Additional geometry creation and manipulation.

;; (load "drafting_helpers.lsp")
;; (load "error_handling.lsp")

(defun c:create-polyline (ptlist closedFlag / )
  (if (or (null ptlist) (< (length ptlist) 2))
    (report-error "Need at least two points for a polyline.")
  )
  (command "_pline")
  (foreach p ptlist
    (command p)
  )
  (if closedFlag
    (command "C")
  )
  (command "")
  (princ "\nCreated polyline.")
)

(defun c:move-entity (ent delta-x delta-y / start end)
  (setq start (list 0.0 0.0 0.0))
  (setq end   (list delta-x delta-y 0.0))
  (command "_MOVE" ent "" start end)
  (princ "\nEntity moved.")
)

(defun c:rotate-entity (ent base-x base-y angleDeg / base angleRad)
  (setq base (list base-x base-y 0.0))
  (setq angleRad (* pi (/ angleDeg 180.0)))
  (command "_ROTATE" ent "" base angleRad)
  (princ (strcat "\nRotated entity by " (rtos angleDeg 2 2) " degrees." ))
)

(defun c:rotate_entity_by_id (id_value base_x base_y angleDeg / ent)
  (setq ent (find_block_by_id id_value))
  (if ent
    (c:rotate-entity ent base_x base_y angleDeg)
    (report-error (strcat "No block found with ID: " id_value))
  )
)

(princ "\nAdvanced geometry features loaded.\n")
(princ)
