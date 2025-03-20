;; Process Diagram Helper Functions for MCP Server
;; Based on guidance document for AutoCAD automation via AutoLISP

;; Function to ensure a layer exists with specified properties
(defun ensure_layer_exists (layer_name color linetype / )
  ;; If layer does not exist, create it
  (if (not (tblsearch "LAYER" layer_name))
    (command "_.LAYER" "N" layer_name "C" color layer_name "L" linetype layer_name "")
  )
  (princ (strcat "\nEnsured layer exists: " layer_name))
)

;; Function to set current layer
(defun set_current_layer (layer_name / )
  (command "_.LAYER" "S" layer_name "")
  (princ (strcat "\nSet current layer to: " layer_name))
)

;; Function to get attribute value from a block reference
(defun get_attribute_value (block_ent tag / ent_data attrib_ent attrib_data)
  ;; Get the block entity data
  (setq ent_data (entget block_ent))
  
  ;; Get the first attribute
  (setq attrib_ent (entnext block_ent))
  
  ;; Loop through all attributes to find the one with the matching tag
  (while (and attrib_ent (/= (cdr (assoc 0 (setq attrib_data (entget attrib_ent)))) "SEQEND"))
    ;; Check if this is an attribute entity and matches our tag
    (if (and (= (cdr (assoc 0 attrib_data)) "ATTRIB")
             (= (cdr (assoc 2 attrib_data)) tag))
      ;; Return the attribute value
      (progn
        (setq result (cdr (assoc 1 attrib_data)))
        (setq attrib_ent nil) ;; Exit the loop
      )
      ;; Move to the next entity in sequence
      (setq attrib_ent (entnext attrib_ent))
    )
  )
  
  (if (= result nil)
    (princ (strcat "\nAttribute '" tag "' not found"))
    (princ (strcat "\nAttribute '" tag "' value: " result))
  )
  
  result
)

;; Function to set attribute value in a block reference
(defun set_attribute_value (block_ent tag new_value / ent_data attrib_ent attrib_data new_attrib_data)
  ;; Get the block entity data
  (setq ent_data (entget block_ent))
  
  ;; Get the first attribute
  (setq attrib_ent (entnext block_ent))
  
  ;; Loop through all attributes to find the one with the matching tag
  (while (and attrib_ent (/= (cdr (assoc 0 (setq attrib_data (entget attrib_ent)))) "SEQEND"))
    ;; Check if this is an attribute entity and matches our tag
    (if (and (= (cdr (assoc 0 attrib_data)) "ATTRIB")
             (= (cdr (assoc 2 attrib_data)) tag))
      (progn
        ;; Create new attribute data with updated value
        (setq new_attrib_data (subst (cons 1 new_value) (assoc 1 attrib_data) attrib_data))
        ;; Update the attribute entity
        (entmod new_attrib_data)
        ;; Exit the loop
        (setq attrib_ent nil)
      )
      ;; Move to the next entity in sequence
      (setq attrib_ent (entnext attrib_ent))
    )
  )
  
  (princ (strcat "\nSet attribute '" tag "' to value: " new_value))
)

;; Function to set equipment layer
(defun set_equipment_layer (block_ent layer_name / ent_data new_ent_data)
  ;; Get the entity data
  (setq ent_data (entget block_ent))
  
  ;; Create new entity data with updated layer
  (setq new_ent_data (subst (cons 8 layer_name) (assoc 8 ent_data) ent_data))
  
  ;; Update the entity
  (entmod new_ent_data)
  
  (princ (strcat "\nSet entity layer to: " layer_name))
)

;; Function to insert equipment and return its entity name
(defun c:insert_equipment (equipment_type insertion_x insertion_y attributes_list / insertion_point ent_name)
  ;; Create insertion point
  (setq insertion_point (list insertion_x insertion_y 0.0))
  
  ;; Insert the block
  (command "_.INSERT" equipment_type insertion_point "1" "1" "0")
  
  ;; Get the entity name of the inserted block
  (setq ent_name (entlast))
  
  ;; Process attributes if provided
  (if attributes_list
    (progn
      (foreach att attributes_list
        (set_attribute_value ent_name (car att) (cdr att))
      )
    )
  )
  
  (princ (strcat "\nInserted equipment " equipment_type " at (" (rtos insertion_x 2 2) "," (rtos insertion_y 2 2) ")"))
  
  ;; Return the entity name
  ent_name
)

;; Function to get port coordinates on a block (predefined offset positions)
(defun get_port_coordinates (block_ent port_name / ent_data insertion_point block_angle offset_coords global_coords)
  ;; Get the entity data
  (setq ent_data (entget block_ent))
  
  ;; Get the insertion point
  (setq insertion_point (cdr (assoc 10 ent_data)))
  
  ;; Get the rotation angle
  (setq block_angle (cdr (assoc 50 ent_data)))
  (if (= block_angle nil) (setq block_angle 0.0))
  
  ;; Define standard port offsets based on equipment type
  ;; This is a simplified approach - in a real implementation, you might have a lookup table
  ;; or store this information in the block definition itself
  
  ;; Get the block name
  (setq block_name (cdr (assoc 2 ent_data)))
  
  ;; Set default offset coordinates based on port name and block name
  (cond
    ;; For PUMP-CENTRIF1 and PUMP-CENTRIF2
    ((or (= block_name "PUMP-CENTRIF1") (= block_name "PUMP-CENTRIF2"))
      (cond
        ((= port_name "in") (setq offset_coords (list -5.0 0.0 0.0)))
        ((= port_name "out") (setq offset_coords (list 5.0 0.0 0.0)))
        (T (setq offset_coords (list 0.0 0.0 0.0))) ;; Default for unknown port
      )
    )
    ;; For BLOWER-ROTARY
    ((= block_name "BLOWER-ROTARY")
      (cond
        ((= port_name "in") (setq offset_coords (list 0.0 -5.0 0.0)))
        ((= port_name "out") (setq offset_coords (list 0.0 5.0 0.0)))
        (T (setq offset_coords (list 0.0 0.0 0.0))) ;; Default for unknown port
      )
    )
    ;; Default for other blocks
    (T
      (cond
        ((= port_name "in") (setq offset_coords (list -3.0 0.0 0.0)))
        ((= port_name "out") (setq offset_coords (list 3.0 0.0 0.0)))
        (T (setq offset_coords (list 0.0 0.0 0.0))) ;; Default for unknown port
      )
    )
  )
  
  ;; Apply rotation to the offset coordinates if block is rotated
  ;; Note: This is a simplified approach. For complex rotations, use transformation matrices.
  (if (/= block_angle 0.0)
    (progn
      (setq cos_angle (cos block_angle))
      (setq sin_angle (sin block_angle))
      (setq x (car offset_coords))
      (setq y (cadr offset_coords))
      (setq rotated_x (- (* x cos_angle) (* y sin_angle)))
      (setq rotated_y (+ (* x sin_angle) (* y cos_angle)))
      (setq offset_coords (list rotated_x rotated_y 0.0))
    )
  )
  
  ;; Add offset to insertion point to get global coordinates
  (setq global_coords (list 
    (+ (car insertion_point) (car offset_coords))
    (+ (cadr insertion_point) (cadr offset_coords))
    (+ (caddr insertion_point) (caddr offset_coords))
  ))
  
  (princ (strcat "\nPort '" port_name "' coordinates: (" 
                 (rtos (car global_coords) 2 2) "," 
                 (rtos (cadr global_coords) 2 2) ")"))
  
  global_coords
)

;; Function to connect equipment with a line (pipe)
(defun c:connect_equipment (block_ent1 block_ent2 pipe_type from_port to_port / start_point end_point)
  ;; Get the port coordinates
  (setq start_point (get_port_coordinates block_ent1 from_port))
  (setq end_point (get_port_coordinates block_ent2 to_port))
  
  ;; Determine the appropriate layer based on pipe_type
  (setq pipe_layer (strcat "Pipes_" pipe_type))
  
  ;; Ensure the layer exists
  (ensure_layer_exists pipe_layer "white" "CONTINUOUS")
  
  ;; Set current layer
  (set_current_layer pipe_layer)
  
  ;; Draw the line
  (command "_line" start_point end_point "")
  
  (princ (strcat "\nConnected equipment with pipe type: " pipe_type))
  
  ;; Return the entity name of the line
  (entlast)
)

;; Function to label equipment
(defun c:label_equipment (block_ent label_text height / ent_data insertion_point label_point)
  ;; Get the entity data
  (setq ent_data (entget block_ent))
  
  ;; Get the insertion point
  (setq insertion_point (cdr (assoc 10 ent_data)))
  
  ;; Create label point (above the equipment)
  (setq label_point (list 
    (car insertion_point)
    (+ (cadr insertion_point) 6.0)
    (caddr insertion_point)
  ))
  
  ;; Ensure the label layer exists
  (ensure_layer_exists "Labels" "green" "CONTINUOUS")
  
  ;; Set current layer
  (set_current_layer "Labels")
  
  ;; Create the text
  (command "_text" "j" "m" label_point height "0" label_text)
  
  (princ (strcat "\nLabeled equipment with text: " label_text))
  
  ;; Return the entity name of the text
  (entlast)
)

;; Function to arrange equipment in a sequence
(defun c:arrange_equipment (equipment_list start_x start_y direction distance / current_x current_y prev_ent current_ent)
  ;; Set initial position
  (setq current_x start_x)
  (setq current_y start_y)
  
  ;; Initialize previous entity
  (setq prev_ent nil)
  
  ;; Ensure equipment layer exists
  (ensure_layer_exists "Equipment" "yellow" "CONTINUOUS")
  
  ;; Set equipment layer
  (set_current_layer "Equipment")
  
  ;; Process each equipment type in the list
  (foreach equip equipment_list
    ;; Extract equipment type and attributes
    (setq equipment_type (car equip))
    (setq attributes (cadr equip))
    
    ;; Insert the equipment
    (setq current_ent (c:insert_equipment equipment_type current_x current_y attributes))
    
    ;; Connect to the previous equipment if it exists
    (if prev_ent
      (c:connect_equipment prev_ent current_ent "Main" "out" "in")
    )
    
    ;; Update previous entity
    (setq prev_ent current_ent)
    
    ;; Update current position based on direction
    (cond
      ((= direction "right") (setq current_x (+ current_x distance)))
      ((= direction "left") (setq current_x (- current_x distance)))
      ((= direction "up") (setq current_y (+ current_y distance)))
      ((= direction "down") (setq current_y (- current_y distance)))
      (T (setq current_x (+ current_x distance))) ;; Default is right
    )
  )
  
  (princ "\nEquipment arrangement complete.")
)

;; Function to create a predefined block
(defun c:create_block_with_ports (block_name port_definitions / )
  ;; This is a simplified implementation
  ;; In a real application, you would create a block definition with these ports
  (princ "\nBlock creation requires custom implementation based on your environment.")
)

;; Function to insert one of our predefined equipment blocks
(defun c:insert_standard_equipment (equipment_type x y tag scale / )
  ;; Map the equipment type to the appropriate block name
  (cond
    ((= equipment_type "pump-centrifugal-1") (setq block_name "PUMP-CENTRIF1"))
    ((= equipment_type "pump-centrifugal-2") (setq block_name "PUMP-CENTRIF2"))
    ((= equipment_type "blower-rotary") (setq block_name "BLOWER-ROTARY"))
    (T (setq block_name equipment_type)) ;; Use directly if unknown
  )
  
  ;; Create a list of tag attributes
  (setq attributes_list (list (cons "TAG" tag)))
  
  ;; Insert the equipment and get the entity name
  (setq ent_name (c:insert_equipment block_name x y attributes_list))
  
  ;; Scale the block if needed (simplified approach)
  (if (/= scale 1.0)
    (command "_.SCALE" ent_name "" (list x y 0.0) scale)
  )
  
  (princ (strcat "\nInserted standard equipment " block_name " with tag " tag))
  
  ;; Return the entity name
  ent_name
)

;; Initialize when loaded
(princ "\nProcess diagram helper functions loaded successfully.")
(princ)
