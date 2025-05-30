;; Test code for CAD Tools Online P&ID Symbols Library
;; This file demonstrates how to call blocks from the C:\PIDv4-CTO library

;; Method 1: Direct INSERT command with full path
(defun c:test-insert-valve ()
  (princ "\nInserting a gate valve from CTO library...")
  (command "_.-INSERT" 
           "C:\\PIDv4-CTO\\VALVES\\VA-GATE.dwg"  ; Full path to block
           pause                                  ; Let user pick insertion point
           ""                                    ; Default scale (Enter)
           ""                                    ; Default scale (Enter) 
           pause)                                ; Let user pick rotation
  (princ "\nGate valve inserted!")
  (princ)
)

;; Method 2: Using entmake after loading block definition
(defun c:test-insert-clarifier ()
  (princ "\nInserting a clarifier from CTO library...")
  ;; First, ensure the block is loaded
  (if (not (tblsearch "BLOCK" "EQUIP-CLARIFIER"))
    (command "_.-INSERT" "C:\\PIDv4-CTO\\EQUIPMENT\\EQUIP-CLARIFIER.dwg" nil)
  )
  ;; Now insert using entmake
  (setq ins-pt (getpoint "\nSpecify insertion point: "))
  (if ins-pt
    (progn
      (entmake (list
        '(0 . "INSERT")
        '(100 . "AcDbEntity")
        '(8 . "WW-PROCESS-EQUIPMENT")  ; Layer
        '(100 . "AcDbBlockReference")
        '(2 . "EQUIP-CLARIFIER")       ; Block name
        (cons 10 ins-pt)               ; Insertion point
        '(41 . 1.0)                    ; X scale
        '(42 . 1.0)                    ; Y scale
        '(43 . 1.0)                    ; Z scale
        '(50 . 0.0)                    ; Rotation
      ))
      (princ "\nClarifier inserted!")
    )
  )
  (princ)
)

;; Method 3: Wrapper function for common wastewater equipment
(defun c:insert-ww-equipment (/ equip-type path block-name)
  (princ "\nWastewater Equipment Types:")
  (princ "\n1 - Clarifier")
  (princ "\n2 - Filter")
  (princ "\n3 - Gas Scrubber")
  (princ "\n4 - Centrifuge")
  (princ "\n5 - Belt Skimmer")
  (setq equip-type (getint "\nSelect equipment type (1-5): "))
  
  (setq block-info 
    (cond
      ((= equip-type 1) '("EQUIPMENT" . "EQUIP-CLARIFIER"))
      ((= equip-type 2) '("EQUIPMENT" . "EQUIP-FILTER"))
      ((= equip-type 3) '("EQUIPMENT" . "EQUIP-GAS_SCRUBBER"))
      ((= equip-type 4) '("EQUIPMENT" . "EQUIP-CENTRIFUGE"))
      ((= equip-type 5) '("EQUIPMENT" . "EQUIP-BELT_SKIMMER"))
      (t nil)
    ))
  
  (if block-info
    (progn
      (setq path (strcat "C:\\PIDv4-CTO\\" 
                        (car block-info) "\\" 
                        (cdr block-info) ".dwg"))
      (command "_.-INSERT" path pause "" "" pause)
      (princ (strcat "\n" (cdr block-info) " inserted!"))
    )
    (princ "\nInvalid selection.")
  )
  (princ)
)

;; Method 4: Batch setup - Add CTO paths to support file search path
(defun c:setup-cto-library ()
  ;; This adds the CTO directories to AutoCAD's search path
  ;; allowing you to insert blocks by name only
  (setq support-path (getenv "ACAD"))
  (setq new-paths "C:\\PIDv4-CTO\\VALVES;C:\\PIDv4-CTO\\EQUIPMENT;C:\\PIDv4-CTO\\PUMPS-BLOWERS;C:\\PIDv4-CTO\\TANKS;C:\\PIDv4-CTO\\INSTRUMENTS;C:\\PIDv4-CTO\\PIPING")
  
  (if (not (vl-string-search "PIDv4-CTO" support-path))
    (progn
      (setenv "ACAD" (strcat support-path ";" new-paths))
      (princ "\nCTO library paths added to AutoCAD search path.")
      (princ "\nYou can now insert blocks by name: INSERT VA-GATE")
    )
    (princ "\nCTO library paths already configured.")
  )
  (princ)
)

;; Method 5: Create a wastewater-specific block inserter
(defun c:ww-valve (/ valve-type path)
  (princ "\nWastewater Valve Types:")
  (princ "\n1 - Gate Valve")
  (princ "\n2 - Butterfly Valve")
  (princ "\n3 - Check Valve")
  (princ "\n4 - Ball Valve")
  (princ "\n5 - Plug Valve")
  (princ "\n6 - Knife Gate Valve")
  (setq valve-type (getint "\nSelect valve type (1-6): "))
  
  (setq valve-name
    (nth (1- valve-type)
         '("VA-GATE" "VA-BUTTERFLY" "VA-CHECK" "VA-BALL" "VA-PLUG" "VA-KNIFEGATE")))
  
  (if valve-name
    (progn
      (setq path (strcat "C:\\PIDv4-CTO\\VALVES\\" valve-name ".dwg"))
      (command "_.-INSERT" path pause "" "" pause)
      (princ (strcat "\n" valve-name " inserted!"))
    )
    (princ "\nInvalid selection.")
  )
  (princ)
)

;; Test function to list available wastewater-relevant blocks
(defun c:list-ww-blocks ()
  (princ "\n=== WASTEWATER-RELEVANT CTO BLOCKS ===")
  (princ "\n\nEQUIPMENT:")
  (princ "\n  EQUIP-CLARIFIER")
  (princ "\n  EQUIP-FILTER")
  (princ "\n  EQUIP-GAS_SCRUBBER")
  (princ "\n  EQUIP-CENTRIFUGE")
  (princ "\n  EQUIP-BELT_SKIMMER")
  (princ "\n  EQUIP-AIR_DRYER")
  (princ "\n  EQUIP-SCREENBAR")
  (princ "\n  EQUIP-ROTARY_SCREEN")
  
  (princ "\n\nPUMPS:")
  (princ "\n  PUMP-CENTRIF1, PUMP-CENTRIF2")
  (princ "\n  PUMP-SUBMERSIBLE")
  (princ "\n  PUMP-PROGRESSIVE_CAVITY")
  (princ "\n  PUMP-DIAPHRAGM")
  (princ "\n  PUMP-METERING")
  
  (princ "\n\nBLOWERS:")
  (princ "\n  BLOWER-CENTRIFUGAL")
  (princ "\n  BLOWER-ROTARY")
  
  (princ "\n\nVALVES:")
  (princ "\n  VA-GATE, VA-BUTTERFLY, VA-CHECK")
  (princ "\n  VA-BALL, VA-PLUG, VA-KNIFEGATE")
  (princ "\n  VA-BACKFLOWPREVENTER")
  
  (princ "\n\nTANKS:")
  (princ "\n  TANK-CONE_BOTTOM_OPEN")
  (princ "\n  TANK-VERTICAL_OPEN")
  (princ "\n  TANK-PROP_AGITATOR")
  (princ "\n  TANK-SPARGE_AERATOR")
  
  (princ "\n\nUse commands like TEST-INSERT-CLARIFIER to insert blocks.")
  (princ)
)

(princ "\n=== CTO BLOCK TEST LOADED ===")
(princ "\nAvailable commands:")
(princ "\n  TEST-INSERT-VALVE     - Insert a gate valve")
(princ "\n  TEST-INSERT-CLARIFIER - Insert a clarifier") 
(princ "\n  INSERT-WW-EQUIPMENT   - Insert wastewater equipment")
(princ "\n  WW-VALVE             - Insert wastewater valves")
(princ "\n  SETUP-CTO-LIBRARY    - Add CTO to search paths")
(princ "\n  LIST-WW-BLOCKS       - List available blocks")
(princ)
