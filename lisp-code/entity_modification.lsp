;; entity_modification.lsp
;; Simple entity modification helpers

(defun c:move-last-entity (dx dy / ent)
  (setq ent (entlast))
  (if ent
    (c:move-entity ent dx dy)
    (report-error "No entity found to move.")
  )
)

(princ "\nEntity modification helpers loaded.\n")
(princ)
