;;; P&ID Tools for AutoCAD MCP
;;; Tools for creating Process Flow Diagrams and Piping & Instrumentation Diagrams
;;; Using CAD Tools Online (CTO) P&ID Symbol Library

;; Insert P&ID block from CTO library without attributes
(defun c:insert-pid-block (category symbol-name x y scale rotation / block-path block-name old-attreq)
  "Insert a P&ID symbol from the CTO library without attribute prompting"
  (setq block-path (strcat "C:/PIDv4-CTO/" category "/" symbol-name ".dwg"))
  (setq block-name symbol-name)
  
  ;; Check if block already exists in drawing
  (if (not (tblsearch "BLOCK" block-name))
    (progn
      ;; Load block definition
      (command "_.-INSERT" block-path nil)
      (princ (strcat "\nLoaded block definition: " block-name))
    )
  )
  
  ;; Insert block without attribute prompting
  (setq old-attreq (getvar "ATTREQ"))
  (setvar "ATTREQ" 0)  ; Disable attribute prompts
  
  ;; Insert block instance
  (command "_.-INSERT" block-name (list x y 0.0) scale scale rotation)
  
  ;; Restore ATTREQ
  (setvar "ATTREQ" old-attreq)
  
  (princ (strcat "\nInserted " block-name " at (" (rtos x 2 2) "," (rtos y 2 2) ")"))
)

;; Create standard P&ID layers
(defun c:setup-pid-layers ()
  "Create standard layers for P&ID drawings"
  ;; Process equipment and vessels
  (command "_.-LAYER" "_NEW" "PID-EQUIPMENT" "_COLOR" "6" "PID-EQUIPMENT" 
           "_LWEIGHT" "0.35" "PID-EQUIPMENT" "")
  
  ;; Process piping
  (command "_.-LAYER" "_NEW" "PID-PROCESS-PIPING" "_COLOR" "4" "PID-PROCESS-PIPING" 
           "_LWEIGHT" "0.50" "PID-PROCESS-PIPING" "")
  
  ;; Utility piping
  (command "_.-LAYER" "_NEW" "PID-UTILITY-PIPING" "_COLOR" "5" "PID-UTILITY-PIPING" 
           "_LTYPE" "DASHED" "PID-UTILITY-PIPING" "_LWEIGHT" "0.35" "PID-UTILITY-PIPING" "")
  
  ;; Instrumentation
  (command "_.-LAYER" "_NEW" "PID-INSTRUMENTS" "_COLOR" "1" "PID-INSTRUMENTS" 
           "_LWEIGHT" "0.25" "PID-INSTRUMENTS" "")
  
  ;; Electrical
  (command "_.-LAYER" "_NEW" "PID-ELECTRICAL" "_COLOR" "7" "PID-ELECTRICAL" 
           "_LWEIGHT" "0.25" "PID-ELECTRICAL" "")
  
  ;; Annotation
  (command "_.-LAYER" "_NEW" "PID-ANNOTATION" "_COLOR" "7" "PID-ANNOTATION" 
           "_LWEIGHT" "0.18" "PID-ANNOTATION" "")
  
  ;; Valves
  (command "_.-LAYER" "_NEW" "PID-VALVES" "_COLOR" "3" "PID-VALVES" 
           "_LWEIGHT" "0.35" "PID-VALVES" "")
  
  (princ "\nP&ID layers created successfully")
)

;; Draw process line between two points
(defun c:draw-process-line (x1 y1 x2 y2 / start-pt end-pt)
  "Draw a process line between two points"
  (setq start-pt (list x1 y1 0.0))
  (setq end-pt (list x2 y2 0.0))
  
  ;; Set current layer
  (command "_.-LAYER" "_SET" "PID-PROCESS-PIPING" "")
  
  ;; Draw polyline
  (command "_PLINE" start-pt "_WIDTH" "0" "0" end-pt "")
  
  (princ (strcat "\nProcess line drawn from (" (rtos x1 2 2) "," (rtos y1 2 2) 
                 ") to (" (rtos x2 2 2) "," (rtos y2 2 2) ")"))
)

;; Add flow arrow to a line
(defun c:add-flow-arrow (x y rotation / arrow-pt)
  "Add a flow arrow at specified location"
  (setq arrow-pt (list x y 0.0))
  
  ;; Insert flow arrow block
  (c:insert-pid-block "ANNOTATION" "ANNOT-FLOWARROW" x y 1.0 rotation)
)

;; Add equipment tag
(defun c:add-equipment-tag (x y tag-text description / tag-pt)
  "Add equipment tag and description"
  (setq tag-pt (list x y 0.0))
  
  ;; Set annotation layer
  (command "_.-LAYER" "_SET" "PID-ANNOTATION" "")
  
  ;; Insert tag block
  (c:insert-pid-block "ANNOTATION" "ANNOT-EQUIP_TAG" x y 1.0 0)
  
  ;; Add tag text
  (command "_TEXT" "J" "MC" tag-pt 2.5 0 tag-text)
  
  ;; Add description if provided
  (if (and description (> (strlen description) 0))
    (command "_TEXT" "J" "TC" (list x (- y 4.0) 0.0) 2.0 0 description)
  )
  
  (princ (strcat "\nEquipment tagged: " tag-text))
)

;; Add line number
(defun c:add-line-number (x y line-num spec / num-pt)
  "Add line number with specification"
  (setq num-pt (list x y 0.0))
  
  ;; Insert line number block
  (c:insert-pid-block "ANNOTATION" "ANNOT-LINE_NUMBER" x y 1.0 0)
  
  ;; Add line number text
  (command "_.-LAYER" "_SET" "PID-ANNOTATION" "")
  (command "_TEXT" "J" "MC" num-pt 2.0 0 (strcat line-num "-" spec))
  
  (princ (strcat "\nLine number added: " line-num "-" spec))
)

;; Connect two equipment with orthogonal routing
(defun c:connect-equipment (x1 y1 x2 y2 / start-pt mid-pt end-pt)
  "Connect two equipment with orthogonal process line"
  (setq start-pt (list x1 y1 0.0))
  (setq end-pt (list x2 y2 0.0))
  
  ;; Calculate midpoint for orthogonal routing
  (if (> (abs (- x2 x1)) (abs (- y2 y1)))
    ;; Horizontal first, then vertical
    (setq mid-pt (list x2 y1 0.0))
    ;; Vertical first, then horizontal
    (setq mid-pt (list x1 y2 0.0))
  )
  
  ;; Set process piping layer
  (command "_.-LAYER" "_SET" "PID-PROCESS-PIPING" "")
  
  ;; Draw polyline with orthogonal routing
  (command "_PLINE" start-pt "_WIDTH" "0" "0" mid-pt end-pt "")
  
  (princ "\nEquipment connected with process line")
)

;; Insert valve on a line
(defun c:insert-valve-on-line (x y valve-type rotation / valve-name)
  "Insert a valve at specified location on a line"
  ;; Map valve type to CTO symbol name
  (cond
    ((= (strcase valve-type) "GATE") (setq valve-name "VA-GATE"))
    ((= (strcase valve-type) "GLOBE") (setq valve-name "VA-GLOBE"))
    ((= (strcase valve-type) "CHECK") (setq valve-name "VA-CHECK"))
    ((= (strcase valve-type) "BALL") (setq valve-name "VA-BALL"))
    ((= (strcase valve-type) "BUTTERFLY") (setq valve-name "VA-BUTTERFLY"))
    (t (setq valve-name "VA-GATE")) ; Default to gate valve
  )
  
  ;; Set valve layer
  (command "_.-LAYER" "_SET" "PID-VALVES" "")
  
  ;; Insert valve
  (c:insert-pid-block "VALVES" valve-name x y 1.0 rotation)
  
  (princ (strcat "\n" valve-type " valve inserted"))
)

;; Insert instrument on a line
(defun c:insert-instrument (x y instrument-type rotation / inst-category inst-name)
  "Insert an instrument at specified location"
  ;; Map instrument type to CTO symbol
  (cond
    ((= (strcase instrument-type) "FLOW") 
     (setq inst-category "PRIMARY_ELEMENTS")
     (setq inst-name "PRIMELEM-ORIFICE_PLATE"))
    ((= (strcase instrument-type) "PRESSURE") 
     (setq inst-category "ELECTRICAL")
     (setq inst-name "ELEC-PRESS_SW_ACT"))
    ((= (strcase instrument-type) "TEMPERATURE") 
     (setq inst-category "ELECTRICAL")
     (setq inst-name "ELEC-TEMP_SW_ACT"))
    ((= (strcase instrument-type) "LEVEL") 
     (setq inst-category "ELECTRICAL")
     (setq inst-name "ELEC-LIQ_LEV_SW_ACT"))
    (t 
     (setq inst-category "INSTRUMENTS")
     (setq inst-name "INST-DISC-FLDACCESS"))
  )
  
  ;; Set instrument layer
  (command "_.-LAYER" "_SET" "PID-INSTRUMENTS" "")
  
  ;; Insert instrument
  (c:insert-pid-block inst-category inst-name x y 0.75 rotation)
  
  (princ (strcat "\n" instrument-type " instrument inserted"))
)

;; Quick insert functions for common equipment
(defun c:insert-pump (x y pump-type rotation)
  "Insert a pump"
  (cond
    ((= (strcase pump-type) "CENTRIFUGAL") 
     (c:insert-pid-block "PUMPS-BLOWERS" "PUMP-CENTRIF1" x y 1.0 rotation))
    ((= (strcase pump-type) "DIAPHRAGM") 
     (c:insert-pid-block "PUMPS-BLOWERS" "PUMP-DIAPHRAGM" x y 1.0 rotation))
    ((= (strcase pump-type) "GEAR") 
     (c:insert-pid-block "PUMPS-BLOWERS" "PUMP-GEAR" x y 1.0 rotation))
    (t 
     (c:insert-pid-block "PUMPS-BLOWERS" "PUMP-CENTRIF1" x y 1.0 rotation))
  )
  (princ (strcat "\n" pump-type " pump inserted"))
)

(defun c:insert-tank (x y tank-type scale)
  "Insert a tank or vessel"
  (cond
    ((= (strcase tank-type) "VERTICAL") 
     (c:insert-pid-block "TANKS" "TANK-VERTICAL_OPEN" x y scale 0))
    ((= (strcase tank-type) "HORIZONTAL") 
     (c:insert-pid-block "TANKS" "TANK-HORIZONTAL" x y scale 0))
    ((= (strcase tank-type) "CONE") 
     (c:insert-pid-block "TANKS" "TANK-CONE_BOTTOM_OPEN" x y scale 0))
    (t 
     (c:insert-pid-block "TANKS" "TANK-VERTICAL_OPEN" x y scale 0))
  )
  (princ (strcat "\n" tank-type " tank inserted"))
)

(princ "\nP&ID tools loaded successfully\n")