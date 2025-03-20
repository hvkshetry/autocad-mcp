;; PID Symbols Library Integration for MCP Server
;; Functions for inserting process engineering components from AutoCAD's built-in library

;; List of symbol categories and their paths (based on menu structure)
(defun c:list-pid-categories ()
  (princ "\nAvailable PID Symbol Categories:")
  (princ "\n- Equipment")
  (princ "\n  - Pumps")
  (princ "\n  - Blowers")
  (princ "\n  - Compressors")
  (princ "\n  - Tanks and Components")
  (princ "\n  - Inline piping components")
  (princ "\n  - Process equipment")
  (princ "\n- Valves / Actuators")
  (princ "\n- Line types / Drawing connectors")
  (princ "\n- Instrumentation")
  (princ)
)

;; Generic function to insert a symbol from the PID library
(defun c:insert-pid-symbol (category symbol-name x y scale rotation tag / insertion-point)
  (setq insertion-point (list x y 0.0))
  
  ;; Activate the ribbon tab/panel for PID Symbols
  (command "_ribbonclose")  ;; Close current ribbon to avoid conflicts
  (command "-ribbon")       ;; Open ribbon command
  (command "_toolpalettes")  ;; Open tool palettes 
  
  ;; Give user feedback
  (princ (strcat "\nInserting " category " - " symbol-name " at position (" (rtos x 2 2) "," (rtos y 2 2) ")"))
  (princ "\nPlease wait while the tool palette is accessed...")
  
  ;; Insert using coordinate input to position at the exact location
  (command "_insert")
  (command insertion-point scale scale rotation)
  
  ;; If tag is provided, add text label
  (if (/= tag "")
    (progn
      (command "_text" "j" "m" (list x (+ y 10.0) 0.0) 2.5 "0" tag)
      (princ (strcat "\nAdded tag: " tag))
    )
  )
  
  (princ (strcat "\nInserted " category " - " symbol-name))
)

;; Function to insert pump symbol from library
(defun c:insert-pump (pump-type x y scale rotation tag / )
  (c:insert-pid-symbol "Pump" pump-type x y scale rotation tag)
)

;; Function to insert tank symbol from library
(defun c:insert-tank (tank-type x y scale rotation tag / )
  (c:insert-pid-symbol "Tank" tank-type x y scale rotation tag)
)

;; Function to insert valve symbol from library
(defun c:insert-valve (valve-type x y scale rotation tag / )
  (c:insert-pid-symbol "Valve" valve-type x y scale rotation tag)
)

;; Function to insert heat exchanger from library
(defun c:insert-heat-exchanger (exchanger-type x y scale rotation tag / )
  (c:insert-pid-symbol "Heat Exchanger" exchanger-type x y scale rotation tag)
)

;; Helper function to browse available symbols
(defun c:browse-pid-symbols ()
  (command "_toolpalettes")
  (princ "\nPID Symbol palettes opened. Browse to select desired symbols.")
)

;; Function to create a complete PID from selected components
(defun c:create-pid-from-components (component-list / component i x y)
  (setq i 1)
  (foreach component component-list
    (setq x (nth 1 component))
    (setq y (nth 2 component))
    (setq type (nth 0 component))
    (setq name (nth 3 component))
    (setq tag (nth 4 component))
    (setq scale (nth 5 component))
    (setq rotation (nth 6 component))
    
    ;; Insert based on component type
    (cond
      ((= type "pump") (c:insert-pump name x y scale rotation tag))
      ((= type "tank") (c:insert-tank name x y scale rotation tag))
      ((= type "valve") (c:insert-valve name x y scale rotation tag))
      ((= type "heat-exchanger") (c:insert-heat-exchanger name x y scale rotation tag))
      (T (princ (strcat "\nUnknown component type: " type)))
    )
    
    ;; If not the last component and next component exists, create connecting pipe
    (if (< i (length component-list))
      (progn
        (setq next-component (nth i component-list))
        (setq next-x (nth 1 next-component))
        (setq next-y (nth 2 next-component))
        (command "_line" (list x y 0.0) (list next-x next-y 0.0) "")
        (princ (strcat "\nCreated connection from " tag " to " (nth 4 next-component)))
      )
    )
    (setq i (+ i 1))
  )
  (princ "\nPID created successfully.")
)

;; Initialize when loaded
(princ "\nPID Symbols integration loaded successfully.")
(princ)
