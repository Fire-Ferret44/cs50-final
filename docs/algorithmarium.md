#### Constraint-Satisfaction Theory and Building up Algorithm

Summary pasted here under "Basic Solver for Submission", but the remaining algorithmarium.md file goes into the different details I looked at and how I built up the different solver models in the tests/algorithmarium folder (basic_model_1.py, basic_model_2.py, int_model_1.py)

### Basic Solver for Submission

*Variable*: Each shift will be its own node
*Domain*:   Each shift will have a domain of possible doctors to assign
*Constraints*:
-Unary:
--Leave
--Shifts that have no overlap can only be filled by independent doctors
-Binary:
--Some doctors must work with specific other doctors
--Some doctors cannot work with specific other doctors
*Consistency Checks*:
--A solution has a satisfying assignment (doctor) for each variable (shift)
--A doctor may not work more than one shift in a day
--A doctor may not work shifts on consecutive days
--Hours should be balanced accross all doctors
--Weekend hours should be balanced accross all doctors

Counts were initialised for doctors to keep track of hours and weekend hours worked.

1) Pruning: Unary Constraints were used to prune domain size for each variable

2) MRV: The Variables were ordered from smallest to largest domain
-All those with the same smallest remaining domain were randomised to see which one will be tried first (this ensured different iterations of rosters and no bias of which date assigned first)

3) "LCV": The doctors were ordered from lowest highest assigned hours
-The least constraining doctor will be the one with the most hours left to assign
-If the shift that needed to be filled was a weekend, weekend hours were looked at specifically from the candidate doctors with the lowest hours
-These were then also randomised to prevent bias of assigning alphabetically
-By starting to try assignments from least hours there is a build-in feature to distribute hours amongst all doctors

4) Consistency Checks
-The possible candidate that was tried for a shift was then checked with the consistency checks
-If all checks passed that doctor was assigned and then hours were added to the counts of the doctor
-If a check failed, that candidate was backtracked and removed from the assignment, then the next candidate in line would be tried

5) Solution
-If all variables had an assignment a solution was found!

### Theory, Definition and Concepts

References
-CS 161: Course notes (Design and Analysis of Algorithms, Stanford University, Summer 2025 by Matthew Sotoudeh)
	5.6 More Classic Algorithms
	5.8 Other Famous Algorithms
-Artificial Intelligence: A Modern Approach (Russel and Norvig)
	Chapter 5 Constraint Satisfaction Problems pg164
-OR-Tools by Google
-YouTube Tutorials 

ref: https://www.youtube.com/watch?v=qK46ET1xk2A
ref: https://www.geeksforgeeks.org/artificial-intelligence/constraint-satisfaction-problems-csp-in-artificial-intelligence/

(Bulk in word doc -- to be copied here when more comfortable with md formatting. Currently easier to read on word doc and make notes.)

### Rostering Algorithm

Computational Complexity
P Class
P Problem: “Polynomial time problem” polynomial function of its size. N to other powers but not exponential (to the power of N). 
Problems in the P complexity class are decision problems that can be efficiently solved by a deterministic Turing machine in polynomial time.
The correctness of a solution can be verified in polynomial time, ensuring that the proposed solution is correct without significant computational effort.
E.g. Sorting
NP Class
NP Problem: “Non-deterministic Polynomial time”
Nondeterministic polynomial-time problems, commonly known as NP problems. These problems have the special property that, once a potential solution is provided, its correctness can be verified quickly. However, finding the solution itself may be computationally difficult.
Nondeterministic Polynomial time problems are computational problems for which solutions can be verified efficiently in polynomial time.
While verification is efficient, finding a solution may be computationally challenging, with no known polynomial time algorithm for general instances.
Can be verified by a deterministic machine in polynomial time.
Co-NP Class
Co-NP stands for the complement of NP Class. It means if the answer to a problem in Co-NP is No, then there is proof that can be checked in polynomial time.
In a deterministic algorithm, for a given particular input, the computer will always produce the same output going through the same states but in the case of the non-deterministic algorithm, for the same input, the compiler may produce different output in different runs.
NP Hard Class
An NP-hard problem is at least as hard as the hardest problem in NP and it is a class of problems such that every problem in NP reduces to NP-hard.

NP Complete Class


Scott Aaronson (complexity research at MIT):
“If P=NP, then the world would be a profoundly different place than we usually assume it to be. There would be no special value in “creative leaps,” no fundamental gap between solving a problem and recognizing the solution once it's found. Everyone who could appreciate a symphony would be Mozart; everyone who could follow a step-by-step argument would be Gauss; everyone who could recognize a good investment strategy would be Warren Buffett.”


Return to this definitions section at a later time. It is not necessary understanding the definitions in so much details to go forward.
References:
P vs. NP and the Computational Complexity Zoo by hackerdashery (https://www.youtube.com/watch?v=YX40hbAHx3s) 
https://www.geeksforgeeks.org/dsa/p-vs-np-problems/

 
Dynamic Programming
Rod Cutting Problem
Rod Cutting Problem: 
Given a rod of length n units, and the price of all pieces smaller than n, find the most profitable way of cutting the rod.
memoisation: an optimization technique used primarily to speed up computer programmes by storing the results of expensive calls to pure functions and returning the cached result when the same inputs occur again.
Without dynamic programming, the problem has a complexity of O(2^n) but with memoisation the problem is reduced to O(n^2)
Bottom-up solution

References:
https://www.youtube.com/watch?v=ElFrskby_7M

Fibonacci Sequence
Recursion in python:
def fibonacci(n):
    if n <= 2:
        return 1 
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(1))
print(fibonacci(2))
print(fibonacci(3))
print(fibonacci(4))

but the above would be very slow if E.g. n = 50 or higher. Time complexity 2^n. 2 and 1 would be “base cases”. 
Height = Distance from root node is the base case 
Level = nodes same number of nodes away from the root node
Nodes in a tree  time complexity
Looking at the fib(7) in a tree there are a lot of duplicate subtrees. And the same subtrees try to answer the same questions and get the same answer. You might want to store the subtree answers to use later. If there are overlapping sub-problems this is known as dynamic programming.
Now if we want to capture duplicate subproblems and store the answers it would look like this:

“”””memoisation””””
“”””python dic with keys = arg, values = return values””””

def fibonacci(n, memo={}):
    if (n in memo):
        return memo[n];
    elif n <= 2:
        return 1; 
    else:
        memo[n] = fibonacci(n-1, memo) + fibonacci(n-2,memo);
        return memo[n];

To do this we implement memoisation. (Same as the rod-cutting one). “Memo” is like a reminder. Good thing to use would be a fast-access data structure. Like a “hashmap” equivalent.
In python it would be like making a dictionary of key-value pairs that are encountered as the function runs. Then when it is encountered again the key can be looked up in the dictionary and the value can be given immediately.
Time complexity would be the number of nodes.
Memoisation changes the fibonacci recursion from an O(2^n) time complexity to a (O(2n) ) O(n) time complexity.

Ref:
https://www.youtube.com/watch?v=oBt53YbR9Kk&t=290s

Knapsack 0/1 problem
This is similar to the rod cutting problem, but unlike the rods where you can have multiple of the same length, the items of the knapsack can only be packed or not packed (not packed multiple times). 

Ref:
https://www.youtube.com/watch?v=hagBB17_hvg

 
Return to CSP: Theory
The dynamic programming and optimisation has been an interesting detour, but my not be directly practical in helping with my problem.
I will now go specifically into the theory of constraint-satisfaction problems and be more focused with my time. 
https://www.youtube.com/watch?v=qK46ET1xk2A
Terminology
Ref: https://www.geeksforgeeks.org/artificial-intelligence/constraint-satisfaction-problems-csp-in-artificial-intelligence/
https://www.youtube.com/watch?v=qK46ET1xk2A

Variable(or node): things we need to find values for (E.g. shift slot)
Domain: set of possible values that a variable can have (E.g. doctors for shifts)
Constraints: rules that restrict how variables can be assigned values. 
	Unary constraints: apply to a single variable (E.g. This shift cannot be filled be ‘E’)
	Binary constraints: involves two variables (E.g. back-to-back shifts cannot be filled by the same person)
	High-order constraints: involves three or more variables (E.g. each doctor must have similar hours/shift number)
Node consistency: when all the values in a variable’s domain satisfy the variable’s unary constraints.
Arc consistency: when all the values in a variable’s domain satisfy the variable’s binary constraints. (I.e. to make X arc-consistent with respect to Y, remove elements form t X’s domain until every choice for X has a possible choice for Y)
AC-3(csp): a function that checks arc consistency throughout a whole problem.

Examples from lecture of what this would look like:
Arc Consistency
Function AC-3(csp):
	queue = all arcs in csp
	while queue non-empty:
		(X,Y) = DEQUEUE(queue)
		if REVISE(csp,X,Y):
			if size of X.domain == 0:
				return false
			for each Z in X.neighbours – {Y}:
				ENQUEUE(queue,(Z,X))
			return true

Backtracking Search:

function BACKTRACK(assignment, csp):
	if assignment complete: return assignment
	var=SELECT-UNASSIGNED-VAR(assignment,csp)
	for value in DOMAIN-VALUES(var,assignment,csp):
		if value consistent with assignement:
			add {var=value} to assignment
			result = BACKTRACK(assignment, csp)
			if result =/= failure: return result
		remove {var=value} from assignment

maintaining arc-consistency: algorithm for enforcing arc-consistency every time we make a new assignment. i.e. whenever we make a new assignment to X, calls AC-3, starting with a queue of all arcs (Y,X) where Y is a neighbour of X.
Revised version of backtracking function where there is an inference line inside the backtracking algorithm:
function BACKTRACK(assignment, csp):
	if assignment complete: return assignment
	var=SELECT-UNASSIGNED-VAR(assignment,csp)
	for value in DOMAIN-VALUES(var,assignment,csp):
		if value consistent with assignement:
			add {var=value} to assignment
			inferences = INFERENCE(assignment,csp)
			if inferences=/= failure: add inferences to assignment
			result = BACKTRACK(assignment, csp)
			if result =/= failure: return result
		remove {var=value} and inferences from assignment

The above adds the idea that if we add a value to a variable it will also shrink the domain of neighbours. Trying to solve the problem more efficiently
More heuristics:
SELECT-UNASSIGNED-VAR
Minimum remaining values (MRV) heuristic: select the variable that has the smallest domain
Degree heuristic: select the variable that has the highest degree (the number of nodes attached by the node – constrained by that node)
Least-constraining values heuristic: return variables in order by number of choices that are ruled out for neighbouring variables (try least-constraining values first)

Problem Formulation:
Local Search
Linear Programming
Constraint Satisfaction

Linear Programming: minimise a cost function, that has a number of variables involved with co-efficients. Often comes up when trying to optimise for something. 
-Simplex
-Interior-Point Algorithm
Libraries scipy
##
Ref: https://www.youtube.com/watch?v=2dYsfrNbV48
These kind of efficiency/optimisation problems also form part of operations research
##
Ref: https://www.youtube.com/watch?v=E72DWgKP_1Y
The art of linear programming

Ref:
https://www.youtube.com/watch?v=D1LVbE8nyXs

https://www.youtube.com/watch?v=81z2ANjQcH4



Generator
-First take care of unary constraints: this would be things like leave days and (and perhaps weekends/weekday off?)
-For continued arc consistency, one would have to dynamically take away options (delete doctors in domain of specific shift slots) as doctors are placed for example: the day-off after post-call.
So far with the basic example of variables, values and constraints of no back-to-back calls, the list of values goes on alphabetically and only A and B are assigned calls on alternative days. That would be rather unfair on A and B. If there is a time where another assignment should be called, would it be better if it is done randomly?

Basic model 1 
5 doctors, 10 shifts, 10 days
Initially I had this problem as above:
So far with the basic example of variables, values and constraints of no back-to-back calls, the list of values goes on alphabetically and only A and B are assigned calls on alternative days. That would be rather unfair on A and B. If there is a time where another assignment should be called, would it be better if it is done randomly?
First proposed solution was that I make a maximum number of shifts per person (no shifts/ no doctors). But then this would happen:
(A,B,A,B,C,D,C,E,D,E)  immediately biasing the those alphabetically or beginning of list
So a better way to assign would be to sort the doctors by how many shifts they have already been assigned. So the next assignment would be one of the doctors that has least current assignments.
This would take into account the number of shifts per person and spread evenly as you went forward in this basic example.
(A,B,C,D,E,A,B,C,D,E)

Basic model 2 
-I am working on slightly bigger example:
 7 doctors, 2 shifts per day (same shift), 20 shifts. The number of unordered pairs is =
 C(n,r)=n!/r!(n-r!) (where n = 7, r = 2) = 21
And combined with number of naïve possibilities for this roster is 21^10 (^20 for number of shifts or ^10 for number of shift pairs per day? I think 10, but either way it is a lot) and the there was no output after running the file for several minutes.
So I have decided to add some unary constraints (leave, max shifts) and binary constraints (one pair cannot work together, one person has to work with a senior)
In this way I can cut down on the number of unordered pairs per shift from the get go. (limiting the domain for each shift). (Now instead of 21 options each time, it is more like 17, 17, 17, 11, 11, 11, 13, 13, 13, 13) 
Initial 21^10 (1.7 x 10^13) compared to ~1.87 x 10^11. (Slightly less.)
I have chosen to consider the shift with least number of available pairs first (this one will have the most clashes if handled later  MRV) and then like the previous example we choose the doctors that have the least assignments so far (this will balance the shifts as they are being assigned.)
As I implemented this and let the max shifts be round(shifts/doctors) + 1 the solution that it came up with was None. So that is strange. The average number of shifts would be between 2 and 3 and I had set max to 4 and it did not work. Although when I set it to 5 it did work! I am not sure why as the solution it found gave all doctors between 2 and 3 shifts.
This was just a test to see if it would work and it worked fairly quickly giving the same answer each time. I thought it would take way too long and I would have to further prune the domains of adjacent shifts as we assign pairs (forward tracking) to make the run feasible. But it seems this was not necessary. Although this is a good simple example to try it and still understand the concepts. (Finally I have come to forward tracking!)
Interestingly it prints out the shift and assignments as they were assigned and not in order. Which is interesting, but not too important now. For formatting later. 
Another thing I want to implement is a “randomiser” between shifts that all have the same number of possible pairs and test variable pairs that have the same sum shifts between them.
It seems to work well without but later I would also want to incorporate a way to look at the MRV of the doctors themselves. I.e. a list of available dates and the MRV would have the least available dates and combine this with the least shifts assigned list to find the next. Or I suppose it is a kind of LCV as assigning someone with the least possible shifts first knocks out less possibilities for other shifts where it was not an option. 
Suggestions:
-Review pruning and copying info existing shifts safely to work on (instead of original)
-Make a global list of available pairs and then have different steps to whittle down the list for 1. Unary and 2. Binary constraints. This will be easier to create a modular approach for more complex problems.
E.g.
all_pairs = list (combinations(doctors, 2))
def filter_unary_constraints(shift, pairs)
“””Filters pairs based on availability and leave”””
…
def filter_binary_constraints(shift, pairs)
“””Filters pairs based on compatibility”””
…
def get_valid_pairs(shift):
“””Apply unary then binary constraints in order.”””
unary_filtered = filter_unary_constraints(shift, all_pairs)
binary_filtered = filter_binary_constraints(after_unary)
…
 
#Get valid pairs for each shift:
valid_pairs = {}
for shift in shift:
	valid_pairs[shift] = get_valied_pairs(shift)
##
Thinking for intermediate model:
-Haven’t done preferences/”soft constraints” yet
-Haven’t worked with hours yet (and varying hours of shift)
	 pairs for different hour shifts can no longer be unordered for Mon-Thur
-Haven’t worked with different days of the week yet
-Need more doctors and shifts? Probably
I think I will start with doing hours, days of week first in intermediate model 1 and then on soft constraints in intermediate model 2. I suspect model 2 will need another algorithm to measure how well preferences are granted. 
Gonna start folding in the classes and utilities like fluffy egg whites in batter.
More difficult than anticipated: 1. Paths to get to folder in the parent folder if run form inside the tests/algorithmarium folder.
2. the shift structure class does not have unique id or even dates in the structure. Perhaps something that needs to be changed for the whole project, but definitely something that needs to be addressed now otherwise it cannot be connected to algorithm and shift domain pairs.
Shift_id = DDMMYY_<dow>_<shift_type>_<slot>
Add a date attribute to Shift class, with None passed in in def
Actual dates added in a loop in build_calendar function. 
Add shift_id to shift class also with None passed in in def. 
Actual shift_id made inside build_calendar function with schema above.

Intermediate Model 1 – 2xvariables/day
(*Intermediate Model 2 should look at soft constraints on the simpler basic_2 model and then after that we try combine)
The next step I thought of doing would be to change shifts to the structure I want to solve. So this would be:
MON-THU: 1x long (16h00-10h00+), 1x short (16h00-20h00)
FRI: 2x long (16h00-08h00+)
SAT: 2x long (08h00-08h00+)
SUN: 2x long (08h00-10h00+)

Firstly, I think it would be good to import the shift_structure class I have already created along with the csv input file for shift requirements (kind of shift per day and how many of that shift, how many hours and how many staff required per shift type for that day).
 Where the hesitation comes in is moving from 1x variable with 1x domain (i.e. doctor pair assignments per day) to a system where each variable is its own domain. The concern is now reworking all the binary constraints that trimmed the domain initially to checking constraints. The options were:
1) Keep is pairs but Mon-Thu are now ordered pairs
2) Make each shift a domain
3) Make each shift a domain for Mon-Thu but used unordered pairs for Fri-Sun
 I think I will try making each shift a domain and then making checking constraints so I understand how it works.
(There is a roadblock trying to import models from different directories, but there was a “fix” I used for this so it would just run here, but this should not be a problem for the main.py or app.py that will run from root.)
Already have a shift_id system that is inside ShiftCalendar.
Small problem with the shift_id system:
1) printing shift_id as ddmmyy, but actually want it as yymmdd
2) for counting the slots the helper function is counting the number of occurrences of a specific shift_type on a given day, but it actually needs to see how many staff are required, because for identical shifts I didn’t write the shift type twice, I just increased the number of staff required

Now within the ShiftCalendar I think we need a key to say what the day behaves like

Wave form collapse
