;; block_id_helpers.lsp
;; Provides functions for referencing/manipulating blocks by an "ID" attribute.

;; (load "drafting_helpers.lsp")

(defun find_block_by_id (id_value / ss i block_ent attrib_ent attrib_data found_ent)
  (setq ss (ssget "X" '((0 . "INSERT"))))
  (if (not ss)
    (progn
      (princ (strcat "\nNo blocks found while searching for ID: " id_value))
      nil
    )
    (progn
      (setq found_ent nil)
      (setq i 0)
      (while (and (< i (sslength ss)) (not found_ent))
        (setq block_ent (ssname ss i))
        (setq attrib_ent (entnext block_ent))
        (while (and attrib_ent (not found_ent)
                    (/= (cdr (assoc 0 (setq attrib_data (entget attrib_ent)))) "SEQEND"))
          (if (and (= (cdr (assoc 0 attrib_data)) "ATTRIB")
                   (equal (strcase (cdr (assoc 2 attrib_data))) "ID")
                   (equal (cdr (assoc 1 attrib_data)) id_value))
            (setq found_ent block_ent)
            (setq attrib_ent (entnext attrib_ent))
          )
        )
        (setq i (1+ i))
      )
      (if found_ent
        (progn
          (princ (strcat "\nFound block with ID: " id_value))
          found_ent
        )
        (progn
          (princ (strcat "\nNo block found with ID: " id_value))
          nil
        )
      )
    )
  )
)

(defun c:connect_blocks_by_id (start_id end_id layer_name from_pt to_pt / ent1 ent2)
  (setq ent1 (find_block_by_id start_id))
  (setq ent2 (find_block_by_id end_id))
  (if (and ent1 ent2)
    (c:connect_blocks ent1 ent2 layer_name from_pt to_pt)
    (princ (strcat "\nCould not find one or both IDs: " start_id ", " end_id))
  )
)

(defun c:label_block_by_id (id_value label_text height / block_ent)
  (setq block_ent (find_block_by_id id_value))
  (if block_ent
    (c:label_block block_ent label_text height)
    (princ (strcat "\nCould not label. No block with ID: " id_value))
  )
)

(defun c:set_block_layer_by_id (id_value layer_name / block_ent)
  (setq block_ent (find_block_by_id id_value))
  (if block_ent
    (progn
      (setvar "CLAYER" layer_name)
      (princ (strcat "\nSet layer for block with ID: " id_value " to " layer_name)))
    (princ (strcat "\nNo block found with ID: " id_value))
  )
)

(princ "\nBlock ID helpers loaded successfully.\n")
(princ)

