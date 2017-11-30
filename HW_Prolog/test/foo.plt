:- begin_tests(foo).
test(x) :- not(x(5)).

test(x) :- x(6).
:- end_tests(foo).
