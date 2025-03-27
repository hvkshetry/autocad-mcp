;; error_handling.lsp
;; Central place for error reporting, parameter checks, and robust returns.

(defun report-error (msg)
  (princ (strcat "\nERROR: " msg))
  (princ)
)

(princ "\nError handling loaded.\n")
(princ)
