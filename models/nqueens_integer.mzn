% N-Queens Problem - Integer Model with Global Constraints
% Author: Lorenzo Domenico Attolico
% Student ID: 48259726
%
% Compact encoding using n integer variables with alldifferent constraints.
% Variable q[i] represents the column position of the queen in row i.
%
% Constraints:
% - All queens in different columns: alldifferent(q)
% - All queens on different diagonals: alldifferent(q[i] + i)
% - All queens on different anti-diagonals: alldifferent(q[i] - i)
%
% Mathematical insight:
% Two queens at (i₁, q[i₁]) and (i₂, q[i₂]) attack each other diagonally if:
%   |i₁ - i₂| = |q[i₁] - q[i₂]|
% This is equivalent to:
%   q[i₁] + i₁ = q[i₂] + i₂  (same diagonal)
%   or
%   q[i₁] - i₁ = q[i₂] - i₂  (same anti-diagonal)

include "alldifferent.mzn";

% Problem size parameter
int: n;

% Decision variables: q[i] = column position of queen in row i
array[1..n] of var 1..n: q;

% CONSTRAINT 1: All queens in different columns
constraint alldifferent(q);

% CONSTRAINT 2: All queens on different diagonals
% q[i] + i must be different for all i
constraint alldifferent([q[i] + i | i in 1..n]);

% CONSTRAINT 3: All queens on different anti-diagonals
% q[i] - i must be different for all i
constraint alldifferent([q[i] - i | i in 1..n]);

% Search strategy: first-fail with median value selection
solve :: int_search(q, first_fail, indomain_median, complete) satisfy;

% Output: Display solution array and board
output [
    "q = [" ++ show(q) ++ "]\n"
] ++ [
    if j = 1 then "\n" else "" endif ++
    if fix(q[i]) = j then "Q " else ". " endif
    | i in 1..n, j in 1..n
] ++ ["\n"];
