# TatamibariSolver
Tatamibari Solver implements two algorithms, Exhaustive Search and SAT Solver using GUI.

# Input
Tatamibari Solver input format:
The first line consist of two inputs, _m_ and _n_  where _m,n_ > 0, followed with _m_ lines and each lines have _n_ columns where each cell is either '\+', '-', '|', or '*'

## Input
Tatamibari Solver input format:
The first line consist of two inputs, _m_ and _n_  where _m,n_ > 0, followed with _m_ lines and each lines have _n_ columns where each cell consist of 1 character (Symbol) where symbol is either '\+', '-', '|', or '\*' representing empty cell.

Input Example:

	4 4
	* * - *
	* - * |
	- * | *
	+ - * *
  
## Output
It will output the number of solutions and the solution(s). Additionaly, will output the runtime of the algorithm in command prompt.

# Requirement
+ Python 3
+ Pycosat
+ tkinter

# Additional Info
For experiment using Exhaustive Search of Tatamibari empty instance and verifier using C++: https://github.com/chrisalpha5/Tatamibari
