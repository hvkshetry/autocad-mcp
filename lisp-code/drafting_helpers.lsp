;; drafting_helpers.lsp
;; General drafting operations: block insertion, connection, labeling, arrangement.
;; Also includes a robust layer creation/setting function per the new approach.

;; (load "error_handling.lsp")

(defun ensure_layer_exists (layer_name color linetype / )
  ;; Minimal approach for create/update. We'll rely on a separate function
  ;; if we want to incorporate lineweight, plot style, etc.
  (if (not (tblsearch "LAYER" layer_name))
    (command "_LAYER"
             "N" layer_name
             "C" color layer_name
             "L" linetype layer_name
             "" "") ;; ensure we fully exit LAYER
  )
  (princ (strcat "\nEnsured layer exists: " layer_name))
)

;; A new robust function to create or update a layer
;; and set it current with setvar "CLAYER"
(defun c:create_or_set_layer (layer_name color linetype lineweight plot_style transparency / )
  ;; We do a "no frills" approach for color, linetype, etc.:
  (command "_LAYER"
           "N" layer_name
           "C" color layer_name
           "L" linetype layer_name
           "" "")
  ;; Potentially set lineweight:
  ;; AutoCAD LT may have limitations. We'll try anyway:
  ;; (command "_LAYER"
  ;;         "Lineweight" lineweight layer_name
  ;;         "" "")
  ;; Possibly set plot style:
  ;; (command "_LAYER" "Plot" plot_style layer_name "" "")
  ;; We skip advanced for now or do a check if it’s supported in LT

  ;; Now set current layer:
  (setvar "CLAYER" layer_name)

  ;; Optionally handle transparency if desired. 
  ;; In LT, might not be fully supported. 
  (princ (strcat "\nLayer " layer_name " created/updated, set current."))
)

(defun set_current_layer (layer_name / )
  ;; Direct approach is safer than messing with _LAYER "S"...
  (setvar "CLAYER" layer_name)
  (princ (strcat "\nSet current layer to: " layer_name))
)

;; --------------------------------------------------------------------------
;; Insert block with optional ID attribute
(defun c:insert_block (block_name x y id_value scale rotation / insertion_pt ent_name)
  (if (not (tblsearch "BLOCK" block_name))
    (progn
      (princ (strcat "\nBlock definition '" block_name "' not found."))
      (exit)
    )
  )
  (setq insertion_pt (list x y 0.0))
  (command "_.INSERT" block_name insertion_pt scale scale rotation)
  (setq ent_name (entlast))
  (if (/= id_value "")
    (set_attribute_value ent_name "ID" id_value)
  )
  (princ (strcat "\nInserted block '" block_name "' at (" (rtos x 2 2) "," (rtos y 2 2)
                 ") with ID='" id_value "'"))
  ent_name
)

;; --------------------------------------------------------------------------
;; Connection point retrieval
(defun get_attribute_value (block_ent tag / ent_data attrib_ent attrib_data result)
  (setq ent_data (entget block_ent))
  (setq attrib_ent (entnext block_ent))
  (while (and attrib_ent (/= (cdr (assoc 0 (setq attrib_data (entget attrib_ent)))) "SEQEND"))
    (if (and (= (cdr (assoc 0 attrib_data)) "ATTRIB")
             (= (strcase (cdr (assoc 2 attrib_data))) (strcase tag)))
      (progn
        (setq result (cdr (assoc 1 attrib_data)))
        (setq attrib_ent nil)
      )
      (setq attrib_ent (entnext attrib_ent))
    )
  )
  result
)

(defun set_attribute_value (block_ent tag new_value / ent_data attrib_ent attrib_data new_attrib_data)
  (setq ent_data (entget block_ent))
  (setq attrib_ent (entnext block_ent))
  (while (and attrib_ent (/= (cdr (assoc 0 (setq attrib_data (entget attrib_ent)))) "SEQEND"))
    (if (and (= (cdr (assoc 0 attrib_data)) "ATTRIB")
             (= (strcase (cdr (assoc 2 attrib_data))) (strcase tag)))
      (progn
        (setq new_attrib_data (subst (cons 1 new_value) (assoc 1 attrib_data) attrib_data))
        (entmod new_attrib_data)
        (setq attrib_ent nil)
      )
      (setq attrib_ent (entnext attrib_ent))
    )
  )
)

(defun get_connection_offset (block_ent point_name / attrib_val offset_x offset_y splitted)
  (setq attrib_val (get_attribute_value block_ent point_name))
  (if attrib_val
    (progn
      (setq offset_x 0.0
            offset_y 0.0)
      (setq splitted (vl-string-search "," attrib_val))
      (if splitted
        (progn
          ;; splitted is the index of comma in the string. We'll parse
          ;; or we can do a more robust parse if needed.
          (setq cpos splitted)
          (setq dx (substr attrib_val 1 cpos))
          (setq dy (substr attrib_val (+ cpos 2)))
          (setq offset_x (atof dx))
          (setq offset_y (atof dy))
        )
      )
      (list offset_x offset_y)
    )
    (list 0.0 0.0)
  )
)

(defun get_connection_point (block_ent point_name / block_data insertion_pt scale_x scale_y rotation offset offset_x offset_y)
  (setq block_data (entget block_ent))
  (setq insertion_pt (cdr (assoc 10 block_data)))
  (setq rotation (cdr (assoc 50 block_data)))
  (if (not rotation) (setq rotation 0.0))

  (setq scale_x (cdr (assoc 41 block_data)))
  (setq scale_y (cdr (assoc 42 block_data)))
  (if (not scale_x) (setq scale_x 1.0))
  (if (not scale_y) (setq scale_y 1.0))

  (setq offset (get_connection_offset block_ent point_name)) 
  (setq offset_x (* (car offset) scale_x))
  (setq offset_y (* (cadr offset) scale_y))

  (if (/= rotation 0.0)
    (progn
      (setq new_x (- (* offset_x (cos rotation)) (* offset_y (sin rotation))))
      (setq new_y (+ (* offset_x (sin rotation)) (* offset_y (cos rotation))))
      (setq offset_x new_x)
      (setq offset_y new_y)
    )
  )

  (list (+ (car insertion_pt) offset_x)
        (+ (cadr insertion_pt) offset_y)
        (caddr insertion_pt))
)

(defun c:connect_blocks (block_ent1 block_ent2 layer_name from_point to_point / start_pt end_pt)
  (setq start_pt (get_connection_point block_ent1 from_point))
  (setq end_pt   (get_connection_point block_ent2 to_point))

  (ensure_layer_exists layer_name "white" "CONTINUOUS")
  (set_current_layer layer_name)
  (command "_line" start_pt end_pt "")
  (princ (strcat "\nConnected blocks on layer '" layer_name "' from '" from_point "' to '" to_point "'." ))
  (entlast)
)

(defun c:label_block (block_ent label_text height / block_data insertion_pt label_pt)
  (setq block_data (entget block_ent))
  (setq insertion_pt (cdr (assoc 10 block_data)))
  (ensure_layer_exists "Labels" "green" "CONTINUOUS")
  (set_current_layer "Labels")
  (setq label_pt (list (car insertion_pt) (+ (cadr insertion_pt) 5.0) (caddr insertion_pt)))
  (command "_text" "j" "m" label_pt height "0" label_text)
  (princ (strcat "\nLabeled block: " label_text))
  (entlast)
)

(defun c:arrange_blocks (block_list start_x start_y direction distance / current_x current_y)
  (setq current_x start_x)
  (setq current_y start_y)
  (ensure_layer_exists "Blocks" "yellow" "CONTINUOUS")
  (set_current_layer "Blocks")

  (foreach blk block_list
    (setq block_name (car blk))
    (setq attributes (cadr blk))

    (setq ent_name (c:insert_block block_name current_x current_y "" 1.0 0.0))

    (foreach pair attributes
      (set_attribute_value ent_name (car pair) (cdr pair))
    )

    (cond
      ((= (strcase direction) "RIGHT") (setq current_x (+ current_x distance)))
      ((= (strcase direction) "LEFT")  (setq current_x (- current_x distance)))
      ((= (strcase direction) "UP")    (setq current_y (+ current_y distance)))
      ((= (strcase direction) "DOWN")  (setq current_y (- current_y distance)))
      (T (setq current_x (+ current_x distance)))
    )
  )
  (princ (strcat "\nBlocks arranged in direction " direction " with spacing " (rtos distance 2 2)))
)

(princ "\nDrafting helpers loaded successfully.\n")
(princ)
