;; basic_shapes.lsp
;; Simple shape creation for lines, circles, single-line text.

(defun c:create-line (start-x start-y end-x end-y / start end)
  (setq start (list start-x start-y 0.0))
  (setq end   (list end-x end-y 0.0))
  (command "_line" start end "")
  (princ (strcat "\nLine created from (" (rtos start-x 2 2) "," (rtos start-y 2 2)
                 ") to (" (rtos end-x 2 2) "," (rtos end-y 2 2) ")"))
)

(defun c:create-circle (center-x center-y radius / center)
  (setq center (list center-x center-y 0.0))
  (command "_circle" center radius)
  (princ (strcat "\nCircle created at center (" (rtos center-x 2 2) "," (rtos center-y 2 2)
                 ") radius " (rtos radius 2 2)))
)

(defun c:create-text (x y text height / insertion_pt)
  (setq insertion_pt (list x y 0.0))
  (command "_text" "j" "m" insertion_pt height "0" text)
  (princ (strcat "\nText created at (" (rtos x 2 2) "," (rtos y 2 2) "): " text))
)

;; New function that supports rotation
(defun c:create-text-rotated (x y text height rotation / insertion_pt)
  (setq insertion_pt (list x y 0.0))
  (command "_text" "j" "m" insertion_pt height rotation text)
  (princ (strcat "\nText created at (" (rtos x 2 2) "," (rtos y 2 2) 
                 ") with rotation " (rtos rotation 2 2) ": " text))
)

(princ "\nBasic shapes AutoLISP library loaded successfully.\n")
(princ)
