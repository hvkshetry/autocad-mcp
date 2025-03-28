;; layout_management.lsp
;; Placeholder for layout, viewport, and page setup management.

;; (load "error_handling.lsp")

(defun c:create_new_layout (layout_name / )
  (command "_layout" "create" layout_name)
  (princ (strcat "\nCreated layout: " layout_name))
)

(defun c:create_viewport (layout_name center_x center_y width height / )
  (princ (strcat "\nCreated viewport on layout '" layout_name "' at center("
                 (rtos center_x 2 2) "," (rtos center_y 2 2) ") with size("
                 (rtos width 2 2) "x" (rtos height 2 2) ")"))
)

(defun c:set_current_layout (layout_name / )
  (command "_layout" "set" layout_name)
  (princ (strcat "\nSet current layout to: " layout_name))
)

(princ "\nLayout management loaded.\n")
(princ)
