;; advanced_entities.lsp
;; Advanced shape creation: rectangle, arc, ellipse, mtext, wipeout

(defun c:create-rectangle (x1 y1 x2 y2 layer / p1 p2)
  (setq p1 (list x1 y1 0.0))
  (setq p2 (list x2 y2 0.0))
  (if layer
    (progn
      (ensure_layer_exists layer "white" "CONTINUOUS")
      (set_current_layer layer)
    )
  )
  (command "_RECTANG" p1 p2)
  (princ (strcat "\nRectangle created from (" (rtos x1 2 2) "," (rtos y1 2 2)
                 ") to (" (rtos x2 2 2) "," (rtos y2 2 2) ")"))
)

(defun c:create-arc (cx cy radius startAng endAng layer / center sp ep)
  (setq center (list cx cy 0.0))
  (setq sp (list (+ cx (* radius (cos (* pi (/ startAng 180.0)))))
                 (+ cy (* radius (sin (* pi (/ startAng 180.0)))))
                 0.0))
  (setq ep (list (+ cx (* radius (cos (* pi (/ endAng 180.0)))))
                 (+ cy (* radius (sin (* pi (/ endAng 180.0)))))
                 0.0))
  (if layer
    (progn
      (ensure_layer_exists layer "white" "CONTINUOUS")
      (set_current_layer layer)
    )
  )
  (command "_ARC" "C" center sp ep)
  (princ (strcat "\nArc created at (" (rtos cx 2 2) "," (rtos cy 2 2)
                 ") radius " (rtos radius 2 2)))
)

(defun c:create-ellipse (cx cy major_dx major_dy minor_ratio layer / center major_end)
  (setq center (list cx cy 0.0))
  (setq major_end (list (+ cx major_dx) (+ cy major_dy) 0.0))
  (if layer
    (progn
      (ensure_layer_exists layer "white" "CONTINUOUS")
      (set_current_layer layer)
    )
  )
  (command "_ELLIPSE" center major_end minor_ratio)
  (princ (strcat "\nEllipse created at (" (rtos cx 2 2) "," (rtos cy 2 2) ")"))
)

(defun c:create-mtext (x y width txt height layer style rotation / inspt)
  (setq inspt (list x y 0.0))
  (if layer
    (progn
      (ensure_layer_exists layer "white" "CONTINUOUS")
      (set_current_layer layer)
    )
  )
  (command "_.-MTEXT" inspt "H" height "R" rotation
           (if style (list "S" style) "")
           "W" width "" txt "")
  (princ "\nMText created.")
)

(defun c:create-wipeout-from-points (ptlist frameVisible / )
  (setvar "WIPEOUTFRAME" (if frameVisible 1 0))
  (command "_WIPEOUT" "P")
  (foreach p ptlist (command p))
  (command "")
  (princ "\nWipeout created.")
)

(princ "\nAdvanced entity creation loaded.\n")
(princ)
