;; Basic Shapes AutoLISP Library for MCP Server
;; Functions for creating process engineering components

;; Create a line with specified coordinates
(defun c:create-line (start-x start-y end-x end-y / start end)
  (setq start (list start-x start-y 0.0))
  (setq end (list end-x end-y 0.0))
  (command "_line" start end "")
  (princ "\nLine created.")
)

;; Create a circle with specified center and radius
(defun c:create-circle (center-x center-y radius / center)
  (setq center (list center-x center-y 0.0))
  (command "_circle" center radius)
  (princ (strcat "\nCircle created with radius " (rtos radius 2 2)))
)

;; Create text at specified location
(defun c:create-text (x y text height / point)
  (setq point (list x y 0.0))
  (command "_text" "j" "m" point height "0" text)
  (princ (strcat "\nText created: " text))
)

;; Create standard pump symbol
(defun c:create-pump (x y size tag / center)
  (setq center (list x y 0.0))
  ;; Create the pump circle
  (command "_circle" center (* size 1.0))
  ;; Create the triangle
  (command "_line" 
    (list (- x size) (- y size) 0.0) 
    (list (+ x size) y 0.0) 
    "")
  (command "_line" 
    (list (+ x size) y 0.0) 
    (list (- x size) (+ y size) 0.0) 
    "")
  (command "_line" 
    (list (- x size) (+ y size) 0.0) 
    (list (- x size) (- y size) 0.0) 
    "")
  ;; Add tag if provided
  (if (/= tag "")
    (progn
      (command "_text" "j" "m" (list x (+ y (* size 2.0)) 0.0) (* size 0.5) "0" tag)
    )
  )
  (princ (strcat "\nPump created at (" (rtos x 2 2) "," (rtos y 2 2) ")"))
)

;; Create standard vessel symbol (vertical)
(defun c:create-vessel (x y width height tag / center top-center bottom-center)
  (setq center (list x y 0.0))
  (setq top-center (list x (+ y (/ height 2.0)) 0.0))
  (setq bottom-center (list x (- y (/ height 2.0)) 0.0))
  ;; Create the vessel body - ellipse for the top and bottom, lines for the sides
  (command "_ellipse" "_c" top-center (list (+ x (/ width 2.0)) (+ y (/ height 2.0)) 0.0) (/ width height))
  (command "_ellipse" "_c" bottom-center (list (+ x (/ width 2.0)) (- y (/ height 2.0)) 0.0) (/ width height))
  (command "_line" 
    (list (- x (/ width 2.0)) (+ y (/ height 2.0)) 0.0) 
    (list (- x (/ width 2.0)) (- y (/ height 2.0)) 0.0) 
    "")
  (command "_line" 
    (list (+ x (/ width 2.0)) (+ y (/ height 2.0)) 0.0) 
    (list (+ x (/ width 2.0)) (- y (/ height 2.0)) 0.0) 
    "")
  ;; Add tag if provided
  (if (/= tag "")
    (progn
      (command "_text" "j" "m" (list x (+ y (/ height 2.0) (* width 0.3)) 0.0) (* width 0.2) "0" tag)
    )
  )
  (princ (strcat "\nVessel created at (" (rtos x 2 2) "," (rtos y 2 2) ")"))
)

;; Create standard heat exchanger symbol
(defun c:create-heat-exchanger (x y size tag / center)
  (setq center (list x y 0.0))
  ;; Create the outer circle
  (command "_circle" center (* size 1.2))
  ;; Create the inner circle
  (command "_circle" center (* size 0.8))
  ;; Create the cross lines
  (command "_line" 
    (list (- x (* size 1.2)) y 0.0) 
    (list (+ x (* size 1.2)) y 0.0) 
    "")
  (command "_line" 
    (list x (- y (* size 1.2)) 0.0) 
    (list x (+ y (* size 1.2)) 0.0) 
    "")
  ;; Add tag if provided
  (if (/= tag "")
    (progn
      (command "_text" "j" "m" (list x (+ y (* size 1.5)) 0.0) (* size 0.3) "0" tag)
    )
  )
  (princ (strcat "\nHeat exchanger created at (" (rtos x 2 2) "," (rtos y 2 2) ")"))
)

;; Create a pipe connection between two points
(defun c:create-pipe (start-x start-y end-x end-y / start end)
  (setq start (list start-x start-y 0.0))
  (setq end (list end-x end-y 0.0))
  (command "_line" start end "")
  (princ "\nPipe created.")
)

;; Create a simple PFD with pump feeding vessel through heat exchanger
(defun c:create-simple-pfd (x y scale / pump-x exchanger-x vessel-x y-bottom)
  (setq pump-x (+ x (* scale 10.0)))
  (setq exchanger-x (+ pump-x (* scale 30.0)))
  (setq vessel-x (+ exchanger-x (* scale 30.0)))
  (setq y-bottom (- y (* scale 5.0)))
  
  ;; Create equipment
  (c:create-pump pump-x y (* scale 5.0) "P-101")
  (c:create-heat-exchanger exchanger-x y (* scale 6.0) "E-101")
  (c:create-vessel vessel-x y (* scale 8.0) (* scale 25.0) "V-101")
  
  ;; Create connecting pipes
  (c:create-pipe (+ pump-x (* scale 5.0)) y (- exchanger-x (* scale 6.0)) y)
  (c:create-pipe (+ exchanger-x (* scale 6.0)) y (- vessel-x (* scale 4.0)) y)
  
  (princ "\nSimple PFD created.")
)

;; Initialize when loaded
(princ "\nBasic shapes AutoLISP library loaded successfully.")
(princ)
