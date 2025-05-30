;;; Batch Operations for Performance Optimization
;;; Execute multiple drawing commands in a single call

(defun c:batch-create-lines (lines-data / line-spec)
  "Create multiple lines in one operation.
   Input: list of line specifications ((x1 y1 x2 y2) (x1 y1 x2 y2) ...)"
  (foreach line-spec lines-data
    (if (= (length line-spec) 4)
      (command "_LINE" 
               (list (nth 0 line-spec) (nth 1 line-spec) 0.0)
               (list (nth 2 line-spec) (nth 3 line-spec) 0.0)
               "")
      (princ (strcat "\nInvalid line specification: " (vl-princ-to-string line-spec)))))
  (princ (strcat "\nCreated " (itoa (length lines-data)) " lines"))
  (princ))

(defun c:batch-create-circles (circles-data / circle-spec)
  "Create multiple circles in one operation.
   Input: list of circle specifications ((cx cy radius) (cx cy radius) ...)"
  (foreach circle-spec circles-data
    (if (= (length circle-spec) 3)
      (command "_CIRCLE" 
               (list (nth 0 circle-spec) (nth 1 circle-spec) 0.0)
               (nth 2 circle-spec))
      (princ (strcat "\nInvalid circle specification: " (vl-princ-to-string circle-spec)))))
  (princ (strcat "\nCreated " (itoa (length circles-data)) " circles"))
  (princ))

(defun c:batch-create-texts (texts-data / text-spec)
  "Create multiple text entities in one operation.
   Input: list of text specifications ((x y height string) (x y height string) ...)"
  (foreach text-spec texts-data
    (if (>= (length text-spec) 4)
      (command "_TEXT" 
               (list (nth 0 text-spec) (nth 1 text-spec) 0.0)
               (nth 2 text-spec)
               0
               (nth 3 text-spec))
      (princ (strcat "\nInvalid text specification: " (vl-princ-to-string text-spec)))))
  (princ (strcat "\nCreated " (itoa (length texts-data)) " text entities"))
  (princ))

(defun c:batch-mixed-operations (operations / op)
  "Execute multiple different operations in sequence.
   Input: list of operations (('line x1 y1 x2 y2) ('circle cx cy r) ('text x y h str) ...)"
  (foreach op operations
    (cond
      ((eq (car op) 'line)
       (if (= (length op) 5)
         (command "_LINE" 
                  (list (nth 1 op) (nth 2 op) 0.0)
                  (list (nth 3 op) (nth 4 op) 0.0)
                  "")))
      ((eq (car op) 'circle)
       (if (= (length op) 4)
         (command "_CIRCLE" 
                  (list (nth 1 op) (nth 2 op) 0.0)
                  (nth 3 op))))
      ((eq (car op) 'text)
       (if (>= (length op) 5)
         (command "_TEXT" 
                  (list (nth 1 op) (nth 2 op) 0.0)
                  (nth 3 op)
                  0
                  (nth 4 op))))
      (t (princ (strcat "\nUnknown operation: " (vl-princ-to-string op))))))
  (princ "\nBatch operations completed")
  (princ))

(princ "\nBatch operations loaded successfully\n")