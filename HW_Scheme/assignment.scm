;;; Questions:
;;;    What about like base 12? aka invalid bases
;;;    Is this method legal for this class
;;;    Return? or just display? for all of these things

(define (convert number base)
    (cond 
        ((= base 2)  (number->string number base)) 
        ((= base 8)  (number->string number base))
        ((= base 16) (number->string number base))
        (else (display "False"))
    )
)

(define (roll-till-you-win)
    (let (
            (die-roll (1+ (random 6)))
            (result   (1+ (random 6)))
        )
        (display "Bet: ") (display die-roll)
        (display "   Result: " ) (display result)
        (newline)
        (cond ((= die-roll result) (display "You Won!"))
            (else (roll-till-you-win)))
   )
)

;;; list-primes prints out all the primes up to n
(define (list-primes n)
    (let (
            (primeVec (make-vector n #t)) ;Vector to keep track of primes
        )
        (do ((i 2 (1+ i))) ; Loop and find multiples of primes and set them to be false
            ((>= (* i i) n))
            (if (equal? #t (vector-ref primeVec i))
                (do ((j (* i 2) (+ j i)))
                ((>= j n))
                    (vector-set! primeVec j #f)
                )
            )
        )
        (do ((i 2 (1+ i))) ; Loop through the vector and print out all true values
            ((>= i n))
            (cond ((equal? #t (vector-ref primeVec i)) (display i) (newline)))
        )
    )
)