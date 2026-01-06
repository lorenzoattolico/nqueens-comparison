% N-Queens Problem - Boolean Model
% Author: Lorenzo Domenico Attolico
% Student ID: 48259726
%
% Boolean encoding with n² binary variables representing board positions.
% Each variable board[i,j] = 1 if queen at position (i,j), 0 otherwise.
%
% Constraints:
% - Exactly one queen per row
% - Exactly one queen per column
% - At most one queen per diagonal
% - At most one queen per anti-diagonal

% Problem size parameter
int: n;

% Decision variables: board[i,j] = 1 if queen at position (i,j)
array[1..n, 1..n] of var 0..1: board;

% CONSTRAINT 1: Exactly one queen per row
constraint forall(i in 1..n)(
    sum(j in 1..n)(board[i,j]) = 1
);

% CONSTRAINT 2: Exactly one queen per column
constraint forall(j in 1..n)(
    sum(i in 1..n)(board[i,j]) = 1
);

% CONSTRAINT 3: At most one queen per diagonal (i-j = constant)
% Diagonal k: all cells (i,j) where i-j = k
constraint forall(k in 2-n..n-1)(
    sum(i,j in 1..n where i-j=k)(board[i,j]) <= 1
);

% CONSTRAINT 4: At most one queen per anti-diagonal (i+j = constant)
% Anti-diagonal k: all cells (i,j) where i+j = k
constraint forall(k in 2..2*n)(
    sum(i,j in 1..n where i+j=k)(board[i,j]) <= 1
);

% Solve
solve satisfy;

% Output: Display board with Q for queens, . for empty cells
output [
    if j = 1 then "\n" else "" endif ++
    if fix(board[i,j]) = 1 then "Q " else ". " endif
    | i in 1..n, j in 1..n
] ++ ["\n"];
