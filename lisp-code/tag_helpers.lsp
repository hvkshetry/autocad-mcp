;; Tag-based Helpers for Equipment Management
;; Functions for finding and manipulating equipment by tag

;; Function to find an entity by tag attribute
(defun find_entity_by_tag (tag_value / ss ent_name ent_data attrib_ent attrib_data)
  ;; Select all block references
  (setq ss (ssget "X" '((0 . "INSERT"))))
  
  ;; If no blocks found, return nil
  (if (= ss nil)
    (progn
      (princ (strcat "\nNo blocks found in drawing when searching for tag: " tag_value))
      nil
    )
    ;; Otherwise, search through blocks for the one with matching tag
    (progn
      (setq found_entity nil)
      (setq i 0)
      
      ;; Loop through all block references
      (while (and (< i (sslength ss)) (= found_entity nil))
        (setq ent_name (ssname ss i))
        (setq ent_data (entget ent_name))
        
        ;; Get the first attribute entity
        (setq attrib_ent (entnext ent_name))
        
        ;; Flag to indicate if we've found our entity
        (setq found_match nil)
        
        ;; Loop through all attributes to find the one with the tag "TAG"
        (while (and attrib_ent (not found_match) 
                   (/= (cdr (assoc 0 (setq attrib_data (entget attrib_ent)))) "SEQEND"))
          ;; Check if this is an attribute entity with tag "TAG" and matching value
          (if (and (= (cdr (assoc 0 attrib_data)) "ATTRIB")
                   (or (= (cdr (assoc 2 attrib_data)) "TAG") 
                       (= (cdr (assoc 2 attrib_data)) "tag"))
                   (= (cdr (assoc 1 attrib_data)) tag_value))
            (progn
              (setq found_entity ent_name)
              (setq found_match T)
            )
            ;; Move to the next entity in sequence
            (setq attrib_ent (entnext attrib_ent))
          )
        )
        
        ;; Move to the next entity
        (setq i (1+ i))
      )
      
      ;; Return the found entity or nil
      (if found_entity
        (progn
          (princ (strcat "\nFound entity with tag: " tag_value))
          found_entity
        )
        (progn
          (princ (strcat "\nNo entity found with tag: " tag_value))
          nil
        )
      )
    )
  )
)

;; Function to connect equipment by tag values
(defun c:connect_equipment_by_tag (source_tag target_tag pipe_type from_port to_port / source_ent target_ent)
  ;; Find the source and target entities
  (setq source_ent (find_entity_by_tag source_tag))
  (setq target_ent (find_entity_by_tag target_tag))
  
  ;; If both entities are found, connect them
  (if (and source_ent target_ent)
    (progn
      (c:connect_equipment source_ent target_ent pipe_type from_port to_port)
      (princ (strcat "\nConnected equipment with tags " source_tag " and " target_tag))
      T
    )
    (progn
      (princ (strcat "\nFailed to connect equipment - could not find one or both entities with tags " 
                     source_tag " and " target_tag))
      nil
    )
  )
)

;; Function to label equipment by tag value
(defun c:label_equipment_by_tag (tag_value label_text height / ent_name)
  ;; Find the entity
  (setq ent_name (find_entity_by_tag tag_value))
  
  ;; If entity is found, label it
  (if ent_name
    (progn
      (c:label_equipment ent_name label_text height)
      (princ (strcat "\nLabeled equipment with tag " tag_value))
      T
    )
    (progn
      (princ (strcat "\nFailed to label equipment - could not find entity with tag " tag_value))
      nil
    )
  )
)

;; Function to set equipment layer by tag value
(defun c:set_equipment_layer_by_tag (tag_value layer_name / ent_name)
  ;; Find the entity
  (setq ent_name (find_entity_by_tag tag_value))
  
  ;; If entity is found, set its layer
  (if ent_name
    (progn
      (set_equipment_layer ent_name layer_name)
      (princ (strcat "\nSet layer for equipment with tag " tag_value " to " layer_name))
      T
    )
    (progn
      (princ (strcat "\nFailed to set layer - could not find entity with tag " tag_value))
      nil
    )
  )
)

;; Initialize when loaded
(princ "\nTag helpers loaded successfully.")
(princ)
