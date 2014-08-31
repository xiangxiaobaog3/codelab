(defun ask-number() 

  (format t "Please enter a number.")

  (let ((var (read)))
    (if (numberp var)
      var
     (ask-number)))
)
