segment(point2d(5, 4), point2d(5, 5)).
segment(point2d(4, 12), point2d(6, 10)).
rectangle(point2d(9, 16), point2d(16, 14)). % Upper Left and Lower Right corners
rectangle(point2d(3, 6), point2d(10, 3)). % Upper Left and Lower Right corners
square(point2d(3, 13), 4). % Upper Left corner and length of side
square(point2d(11, 6), 2). % Upper Left corner and length of side 
circle(point2d(12, 4), 3). % Center, radius
point2d(12,2).
point2d(4, 13).
point2d(20 ,1).


%   --------------------------------- Parallel ------------------------------------------    %
%   Check to see if they are two vertical lines (div by zero error)
parallel(segment(point2d(X1_1,Y1_1), point2d(X1_2,Y1_2)),
         segment(point2d(X2_1,Y2_1), point2d(X2_2,Y2_2))) :-
    (X1_2 - X1_1) =:= 0,
    (X2_2 - X2_1) =:= 0.

%    Find slope and compare
parallel(segment(point2d(X1_1,Y1_1), point2d(X1_2,Y1_2)),
         segment(point2d(X2_1,Y2_1), point2d(X2_2,Y2_2))) :-
    not(vertical(segment(point2d(X1_1,Y1_1), point2d(X1_2,Y1_2)))),
    not(vertical(segment(point2d(X2_1,Y2_1), point2d(X2_2,Y2_2)))),
    ((Y1_2 - Y1_1) / (X1_2 - X1_1)) =:= ((Y2_2 - Y2_1) / (X2_2 - X2_1)).
%   -------------------------------------------------------------------------------------    %


%   ------------------------- Perpendicular to other line -------------------------------    %
%   Check to see if two lines are perpendicular
%   Case of horizontal line with vertical line
perpendicular(segment(point2d(X1_1,Y1_1), point2d(X1_2,Y1_2)),
              segment(point2d(X2_1,Y2_1), point2d(X2_2,Y2_2))) :-
    (X1_2 - X1_1) =:= 0,
    (Y2_2 - Y2_1) =:= 0.
%   Case of horizontal line with vertical line (other way around)
perpendicular(segment(point2d(X1_1,Y1_1), point2d(X1_2,Y1_2)),
              segment(point2d(X2_1,Y2_1), point2d(X2_2,Y2_2))) :-
    (X2_2 - X2_1) =:= 0,
    (Y1_2 - Y1_1) =:= 0.
%   Check slope and compare
perpendicular(segment(point2d(X1_1,Y1_1), point2d(X1_2,Y1_2)),
              segment(point2d(X2_1,Y2_1), point2d(X2_2,Y2_2))) :-
    not(vertical(segment(point2d(X1_1,Y1_1), point2d(X1_2,Y1_2)))),
    not(vertical(segment(point2d(X2_1,Y2_1), point2d(X2_2,Y2_2)))),
    ((Y1_2 - Y1_1) / (X1_2 - X1_1)) =:= -1 / ((Y2_2 - Y2_1) / (X2_2 - X2_1)).
%   -------------------------------------------------------------------------------------    %


%   =====================================================================================    %
%   ================================= CONTAINED =========================================    %
%   -------------------------- Line Contained in Circle ---------------------------------    %
%   Check distance of both points and circle's midpoint to see if its less than radius
contained(segment(point2d(X1,Y1), point2d(X2,Y2)), circle(point2d(X,Y),R)) :-
    sqrt(((X-X1)*(X-X1)) + ((Y-Y1)*(Y-Y1))) =< R,
    sqrt(((X-X2)*(X-X2)) + ((Y-Y2)*(Y-Y2))) =< R.
%   -------------------------------------------------------------------------------------    %


%   ------------------------- Square contained in Circle --------------------------------    %
%   Check distance of all the points in the square with midpoint. Must be =< radius.
%   Could also do with 2 contained(segment) calls that criss-cross
contained(square(point2d(X1,Y1), L), circle(point2d(X,Y),R)) :-
    sqrt(((X-X1)*(X-X1))         + ((Y-Y1)*(Y-Y1)))         =< R, % Upper left
    sqrt(((X-(X1+L))*(X-(X1+L))) + ((Y-Y1)*(Y-Y1)))         =< R, % Upper Right
    sqrt(((X-(X1+L))*(X-(X1+L))) + ((Y-(Y1-L))*(Y-(Y1-L)))) =< R, % Lower Right
    sqrt(((X-X1)*(X-X1))         + ((Y-(Y1-L))*(Y-(Y1-L)))) =< R. % Lower Left
%   -------------------------------------------------------------------------------------    %


%   --------------------------- Square contained in Rect --------------------------------    %
%   Check top left and bottom right corners for square. Must be within rectangle bounds
%   Could also do with 2 contained(segment) calls that criss-cross
contained(square(point2d(X,Y), L), rectangle(point2d(X1,Y1), point2d(X2,Y2))):-
    X     >= X1,
    Y     =< Y1,
    X + L =< X2,
    Y - L >= Y2.
%   -------------------------------------------------------------------------------------    %


%   --------------------------- Rect contained in Circle --------------------------------    %
%   Check distance of all the points in the rect with midpoint. Must be =< radius.
%   Could also do with 2 contained(segment) calls that criss-cross
contained(rectangle(point2d(X1,Y1), point2d(X2,Y2)), circle(point2d(X,Y),R)) :-
    sqrt(((X-X1)*(X-X1)) + ((Y-Y1)*(Y-Y1))) =< R, % Upper left
    sqrt(((X-X2)*(X-X2)) + ((Y-Y1)*(Y-Y1))) =< R, % Upper Right
    sqrt(((X-X2)*(X-X2)) + ((Y-Y2)*(Y-Y2))) =< R, % Lower Right
    sqrt(((X-X1)*(X-X1)) + ((Y-Y2)*(Y-Y2))) =< R. % Lower Left
%   -------------------------------------------------------------------------------------    %


%   --------------------------- Rect contained in Square --------------------------------    %
%   Check top left and bottom right corners for square. Must be within rectangle bounds
%   Could also do with 2 contained(segment) calls that criss-cross
contained(rectangle(point2d(X1,Y1), point2d(X2,Y2)),square(point2d(X,Y), L)):-
    X1 >= X,
    Y1 =< Y,
    X2 =< X + L,
    Y2 >= Y - L.
%   -------------------------------------------------------------------------------------    %


%   --------------------------- Circle contained in Rect --------------------------------    %
%   Check the direct top, left, right, bottom points and see if they are all within rect
contained(circle(point2d(X,Y), R),rectangle(point2d(X1,Y1), point2d(X2,Y2))):-
    X - R >= X1,
    X + R =< X2,
    Y + R =< Y1,
    Y - R >= Y2.
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Circle contained in Square -------------------------------    %
%   Check the direct top, left, right, bottom points and see if they are all within square
contained(circle(point2d(X,Y), R), square(point2d(X1,Y1), L)):-
    X - R >= X1,
    X + R =< X1 + L,
    Y + R =< Y1,
    Y - R >= Y1 - L.
%   -------------------------------------------------------------------------------------    %
%   =============================== END CONTAINED =======================================    %
%   =====================================================================================    %


%   =====================================================================================    %
%   ================================= INTERSECTS ========================================    %
%   Intersects if not contained and at least one point is in the figure.
%   -------------------------- Segmnt intersects Circle ---------------------------------    %
intersects(segment(point2d(X1,Y1), point2d(X2,Y2)), circle(point2d(X,Y),R)) :-
    S1 is sqrt((X-X1)*(X-X1) + (Y-Y1)*(Y-Y1)),
    S2 is sqrt((X2-X1)*(X2-X1) + (Y2-Y1)*(Y2-Y1)),
    S3 is sqrt((X-X2)*(X-X2) + (Y-Y2)*(Y-Y2)),
    sqrt(S1*S1 +
     S2*0.5*S2*0.5 - 
     (S1*S2)*((S2*S2+S1*S1-S3*S3)/(2*S1*S2))) =< R.
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Segmnt intersects Segmnt ---------------------------------    %
intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
            segment(point2d(Cx,Cy), point2d(Dx,Dy))) :-
    ((Bx-Ax)*(Cy-Ay) - (By-Ay)*(Cx-Ax)) * ((Bx-Ax)*(Dy-Ay) - (By-Ay)*(Dx-Ax)) < 0,
    ((Dx-Cx)*(Ay-Cy) - (Dy-Cy)*(Ax-Cx)) * ((Dx-Cx)*(By-Cy) - (Dy-Cy)*(Bx-Cx)) < 0.
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Segmnt intersects Square ---------------------------------    %
intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), square(point2d(X,Y),L)) :-
    (intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
                segment(point2d(X,Y), point2d(X+L,Y))) ;
     intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
                segment(point2d(X,Y), point2d(X,Y-L))) ;
     intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
                segment(point2d(X+L,Y), point2d(X+L,Y-L))) ;
     intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
                segment(point2d(X,Y-L), point2d(X+L,Y-L)))).
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Segmnt intersects Rectan ---------------------------------    %
intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
           rectangle(point2d(X,Y), point2d(X2,Y2))) :-
    (intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
                segment(point2d(X,Y), point2d(X2,Y))) ;
     intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
                segment(point2d(X,Y), point2d(X,Y2))) ;
     intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
                segment(point2d(X2,Y), point2d(X2,Y2))) ;
     intersects(segment(point2d(Ax,Ay), point2d(Bx,By)), 
                segment(point2d(X,Y2), point2d(X2,Y2)))).
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Square intersects Segmnt ---------------------------------    %
intersects(square(point2d(X,Y),L), segment(point2d(X1,Y1), point2d(X2,Y2))) :-
    intersects(segment(point2d(X1,Y1), point2d(X2,Y2)), square(point2d(X,Y),L)).
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Square intersects Circle ---------------------------------    %
intersects(square(point2d(X1,Y1), L), circle(point2d(X,Y),R)) :-
    (intersects(segment(point2d(X1,Y1), point2d(X1+L,Y1)), circle(point2d(X,Y),R)) ;
     intersects(segment(point2d(X1,Y1), point2d(X1,Y1-L)), circle(point2d(X,Y),R)) ;
     intersects(segment(point2d(X1,Y1-L), point2d(X1+L,Y1-L)), circle(point2d(X,Y),R)) ;
     intersects(segment(point2d(X1+L,Y1-L), point2d(X1+L,Y1)), circle(point2d(X,Y),R))
    ).
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Square intersects Rectan ---------------------------------    %
intersects(square(point2d(X,Y), L), rectangle(point2d(X1,Y1), point2d(X2,Y2))) :-
    X   =< X2,
    X+L >= X1,
    Y   >= Y2,
    Y-L =< Y1.
    %not(contained(square(point2d(X,Y), L), rectangle(point2d(X1,Y1), point2d(X2,Y2)))),
    %not(contained(rectangle(point2d(X1,Y1), point2d(X2,Y2)), square(point2d(X,Y), L))),
    %(in(point2d(X,Y),         rectangle(point2d(X1,Y1), point2d(X2,Y2))) ;
    % in(point2d(X + L,Y),     rectangle(point2d(X1,Y1), point2d(X2,Y2))) ;
    % in(point2d(X,Y - L),     rectangle(point2d(X1,Y1), point2d(X2,Y2))) ;
    % in(point2d(X + L,Y - L), rectangle(point2d(X1,Y1), point2d(X2,Y2)))).
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Rectan intersects Segmnt ---------------------------------    %
intersects(rectangle(point2d(X3,Y3), point2d(X4,Y4)),
            segment(point2d(X1,Y1), point2d(X2,Y2))) :-
    intersects(segment(point2d(X1,Y1), point2d(X2,Y2)), 
               rectangle(point2d(X3,Y3), point2d(X4,Y4))).


%   -------------------------------------------------------------------------------------    %


%   -------------------------- Rectan intersects Square ---------------------------------    %
intersects(rectangle(point2d(X1,Y1), point2d(X2,Y2)), square(point2d(X,Y), L)) :-
    intersects(square(point2d(X,Y), L), rectangle(point2d(X1,Y1), point2d(X2,Y2))).
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Rectan intersects Circle ---------------------------------    %
intersects(rectangle(point2d(X1,Y1), point2d(X2,Y2)), circle(point2d(X,Y),R)) :-
    (intersects(segment(point2d(X1,Y1), point2d(X2,Y1)), circle(point2d(X,Y),R)) ;
     intersects(segment(point2d(X1,Y1), point2d(X1,Y2)), circle(point2d(X,Y),R)) ;
     intersects(segment(point2d(X1,Y2), point2d(X2,Y2)), circle(point2d(X,Y),R)) ;
     intersects(segment(point2d(X2,Y2), point2d(X2,Y1)), circle(point2d(X,Y),R))
    ).
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Circle intersects Rectan ---------------------------------    %
intersects(circle(point2d(X,Y),R), rectangle(point2d(X1,Y1), point2d(X2,Y2))) :-
    intersects(rectangle(point2d(X1,Y1), point2d(X2,Y2)), circle(point2d(X,Y),R)).
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Circle intersects Square ---------------------------------    %
intersects(circle(point2d(X,Y),R), square(point2d(X1,Y1), L)) :-
    intersects(square(point2d(X1,Y1), L), circle(point2d(X,Y),R)).
%   -------------------------------------------------------------------------------------    %


%   -------------------------- Circle intersects Segmnt ---------------------------------    %
intersects(circle(point2d(X,Y),R), segment(point2d(X1,Y1), point2d(X2,Y2))) :-
    intersects(segment(point2d(X1,Y1), point2d(X2,Y2)), circle(point2d(X,Y),R)).
%   -------------------------------------------------------------------------------------    %
%   =============================== END INTERSECT =======================================    %
%   =====================================================================================    %


%   --------------------------------- Vertical line -------------------------------------    %
%   Vertical if the X values are the same
vertical(segment(point2d(X1,_), point2d(X2,_))) :-
    X1 =:= X2.
%   -------------------------------------------------------------------------------------    %


%   ------------------------------- Horizontal line -------------------------------------    %
%   Horizontal if the Y values are the same
horizontal(segment(point2d(_,Y1), point2d(_,Y2))) :-
    Y1 =:= Y2.
%   -------------------------------------------------------------------------------------    %


%   ------------------------------- Point on Figure -------------------------------------    %
% Segment ----
on(point2d(X,Y), segment(point2d(X1,Y1), point2d(X2,Y2))) :-
    sqrt(((X-X1)*(X-X1)) + ((Y-Y1)* (Y-Y1))) +
    sqrt(((X2-X)*(X2-X)) + ((Y2-Y)* (Y2-Y))) =:=
    sqrt(((X2-X1)*(X2-X1)) + ((Y2-Y1)* (Y2-Y1))). 
% Rect ----
on(point2d(X,Y), rectangle(point2d(X1,Y1),point2d(X2,Y2))) :-
    (X =:= X1 ; X =:= X2),
    Y =< Y1,
    Y >= Y2.
on(point2d(X,Y), rectangle(point2d(X1,Y1),point2d(X2,Y2))) :-
    (Y =:= Y1 ; Y =:= Y2),
    X >= X1,
    X =< X2.
% Square ----
on(point2d(X,Y), square(point2d(X1,Y1),L)) :-
    (X =:= X1 ; X =:= X1 + L),
    Y =< Y1,
    Y >= Y1 - L.
on(point2d(X,Y), square(point2d(X1,Y1),L)) :-
    (Y =:= Y1 ; Y =:= Y1 - L),
    X >= X1,
    X =< X1 + L.
% Circ ----
on(point2d(X,Y), circle(point2d(X1,Y1),R)) :-
    sqrt(((X1-X)*(X1-X)) + ((Y1-Y)*(Y1-Y))) =:= R.
%   -------------------------------------------------------------------------------------    %


%   ------------------------------- Point in Figure -------------------------------------    %
%   Same thing with distance formula-- Check to see the distance between point and midpoint
%        of circle. Must be less than or eq to radius. 
in(point2d(X0,Y0), circle(point2d(X,Y),R)) :-
    % Distance between the center of circle and proposed point should be less than Radius
    sqrt(((X-X0)*(X-X0)) + ((Y-Y0)* (Y-Y0))) < R.

in(point2d(X0,Y0), square(point2d(X,Y),L)) :-
    % X0 and Y0 should be between X+L and Y-L
    X0 > X,
    X0 < X + L,
    Y0 < Y,
    Y0 > Y - L.

in(point2d(X0,Y0), rectangle(point2d(X1,Y1),point2d(X2,Y2))) :-
    X0 > X1,
    Y0 < Y1,
    X0 < X2,
    Y0 > Y2.

%   -------------------------------------------------------------------------------------    %

test :-
    write('--- Testing these following lines ---'), nl,
    open('test.txt',read,S),

    repeat,
    read(S,X),

    write('Testing: '), write(X), nl,
    
    X == end_of_file,
    close(S).