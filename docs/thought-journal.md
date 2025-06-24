# Thoughts, Reasoning and Ideas

Place to keep all thoughts, ideas and reasoning about the project as they come. Later to be used to inform other documents and order into neat continuously edited sections regarding different aspects E.g. algorithm-development, module-details. 

### Start

I was thinking about what project I wanted to do for the final CS50 throughout the course and have a notebook of ideas. This idea came a bit later, when I was thinking about problems I identified while doing internship rotations at hospitals and also talking to other people E.g. teachers and creating timetables for subjects at school. Not a problem so much as a space that could really lean code and automisation.

I came up with a long list of things I would have liked to include if I was someone using this app as an admin and things that I would have liked to be considered if I was a participant effected by how the roster was made. This initial outline was everything from the user interface, data input, scalability to different rooms for groups, shift swop requests, aliases so names are not available, what metadata to look at, printable output versions etc. This quickly became a very big project. It is an exciting project for me because I think it could really give some personal satisfaction to make a tangible problem more efficient. But the same thing said it would be unmanageable to do this alone at my level for a cs50 project. 

It is unfortunate that I won't be able to hand something in that I can be show works or has a nice UI, but the thing that I would really like to work on, is the crux of the problem --  the algorithm. This would be the most exciting part for me and I think would be where I can really grow in my logical thinking and transfer some skills learnt into other areas. I don't really want to get stuck on the outer UI design (I will), when what I really want to work on and understand is the machinery.

I made a strict rule for myself not to see what is out there for this problem, before I think through my solution first and have a good idea of how I want my algorithm to run.

### Focus on Algorithm for CS50

For the CS50 final project I think it would be reasonable to hand-in something that is in CLI where the user **inputs** files:
1. global constraints of the roster
(month working on, shift lengths, weekday and week-end specifications, shifts that need to be filled, some constraints like post-call cool off, leave days, max and min hours)
2. list of participants with constraints
(alias, leave days, weekday and weekend preferences, inter-person preferences - or requirements (in case jnr or snr)) 

And the **output**:
1. Actual roster
(or perhaps 3 variants)
2. General Metadata on the roster
(can be in each roster file so that it's clear, should include basic things like min/max hours worked, no weekend/ weekday hours or number of shifts, avg hours worked, if hard constraints were violated, % preferences met)
3. Person-specific metadata about placement

## 17/18 June 2025

Constraints that were considered.

### Hard Constraints
 - No person may work more than one shift per day.
 - No person may work back-to-back long shifts without a minimum 2-day cool-off period before and after.
 - No shifts assigned on a person's approved leave days. (This should include the adjacent weekends if leave starts Monday or ends Friday)
 - Roster must meet minimum required shift coverage per day (e.g., 2 people per weekday shift, 2 per weekend).
 - No shifts may violate hour limits set by department policy.
 - Weekend shifts must be distributed so that everyone does at least one.
 - Interperson specifications E.g. new jnr doc must be placed with a more snr doc
 - Sick cover can also not violate hard constraints as person can be called out to work

### Soft Constraints/Personal Preferences
 - Distribution preference: even throughout month, more in beg. (Day 1 - 15), mid (Day 8 - 23), end (Day 16 - end)
 - Weekend distribution preference: Fri & Sun call (means less weekends worked), Sat call (more time for rest in weekend but likely work more weekends)
 - One weekday preference to be off
 - One weekend preference to be off
 - Interperson preference E.g. not be paired with spouse overnight for household responsibilities
 - Religious observations
 - Is working on end-of-month or pay-day weekend going to influence workload in this department?
 - A day or weekend preference to be "on"
 - Person on leave has priority to get a long call the day before their leave so they can leave at an earlier time the next day (post-call) to start leave earlier - if they so wish


## 18 June 2025

Realisation that it can't all fit into one model

### Outline of project ideas and shifts

Started off thinking this problem would be simpler to model than it is — it seemed logical: shifts, constraints, fairness. But the more I dug in, the more the complexity grew. Realised very quickly that every department seems to operate on slightly different shift models (and different definitions of what’s reasonable or fair). Some have fixed daytime hours with after-hours calls, others work purely in shift blocks. 

→ Realisation: One universal model probably won’t work. Better to design something modular where departments can choose a model type and then we run constraints on that.

### Constraint Overload

I initially tried to account for **all** possible hard and soft constraints, across all departments and human preferences — but it felt like I was overfitting a model that couldn’t breathe. So it would be good to have general lay-outs available for the admin to choose from and then edit.

### Modular system

*Model 1*: Fixed-day time hours with long (and short) shifts and weekend cover and sick cover. (E.g. medical rotation)
*Model 2*: Fully shift-based schedule (E.g. EC)

## 18 June 2025

Idea ping-ponging and understanding logic of how this problem can be solved. 

### What problem is this?

Initial understanding of this field with ai and describing what my problem is

**Constraint Satisfaction Problem**
--> assigning values (shifts) to
--> to variables (people)
--> with constraints 

With secondary characteristics:
*Combinatorial Optimisation*
--> solutions must not just be valid. They must also be the best solutions

*Multi-objective*
--> balancing sometimes conflicting goals
--> non-linear and potentially NP-hard (NP-hard type problem rabbit hole and return)

### Initial Thoughts on How?

Initial thought-experiments... 

#### Brute Force
Look at every roster combination and take it from there. 
Initial: This is dumb. 
Even for a fairly small set of shifts that need to be filled by people, the number of different combinations possible will be enormous. I don't think this is a good way to solve this problem efficiently. 
Aside: what would the Big O of solving this problem be? That would be a interesting comparison between the algorithms I consider for a specific mock problem.

#### How would a human solve this?
How would I try to solve this? I would probably starts with someone that has many constraints e.g. someone who has 2 weeks of leave in a month. They are likely to work on the other weekends and can be distributed better on the limited available weekdays as well before those slots are taken up by other people that have more options. But then who is next? It will automatically cause biase as the last people will get the "left-over" shifts that might not distribute well. Perhaps after the leave person we can look at contested days (usually weekends, two days before a public holiday). As a person you can swap people around and change things dynamically, but this could take a lot of time. There will probably still be biase with who you start with and who gets certain shifts. 

#### Concepts

Concepts brought up by chat to learn about and consider. 

*Weight Constraint Satisfaction Problem*
- translating human sense of "fairness" to numbers to describe particular shift assignment
- now the allocations can be quantifiable and numbers can easily be compared. 
- you can compare two different people's assignment to one shift, but you can also scale:
    - compare fairness throughout entire roster between people
- good but this is almost like "so this is how to do the brute force manually, but in numbers" if we do every possible combination and look at numbers

*Heuristic Approach*
- Finding a good enough solution quickly, rather than the absolute best solution
- This sounds practical because everything else in this context would be brute force

*Pareto Optimal*
- How nice to have a term for this
- Sounds relevant in this problem of allocation. Perhaps more reading around if interested.

List of other terms to look into:
Integer Programming (IP) / Mixed-Integer Programming (MIP)
Constraint Programming (CP)
Satisfiability Modulo Theories (SMT)

*Examples of Heuristic Approaches:*
- Greedy algorithms
- Backtracking with pruning
- Local search
- Simulated annealing
- Genetic algorithms (I looked at this a little and it sounds like a fun experiment!)

## 19 June 2025

Today some more theory around this problem and making a plan for a solution I want to try. Likely involving combination of approaches. Initial and thern for optimisation. 

### Heuristic Assignment
- Most Constrained Variable First
- Minimum Remaining Values for variables

Constraint Graphs
Arc Consistency
Force pruning

### Constraint Propagation
-Reducing Domain size before search...
**Node Consistency**
Arc Consistency
--> AC-3, AC-4, AC-2001
Path Consistency
Forward Checking
Constraint Propagation with GAC

### Backtracking Search

### Heuristics

### Local Search and Metaheuristics

### Optimisation-based

Initial thoughts: Combination of different models. E.g. start with Node Consistency and shrink domains to only value that don't violated hard constraints that can be easily mapped (e.g. leave)
Then start with most constrained, then minimum remaingin values
Then could start with random assignment of the rest and do min-conflicts or do genetic algorithms
The integer programmnig solution would have been interesting to learnin about, but not feasible right now.

## 20 June 2025 

Algorithm think-throughs continue

-Another big CSP timetabling problem is airline crews! I did not think about that. (Not something to think about doing, but I think they will have very refined algorithms looking for almost perfect solutions)

### Complexity Classes
Summary from geeksforgeeks:
*P*	Easily solvable in polynomial time.
*NP*	Yes, answers can be checked in polynomial time.
*Co-NP*	No, answers can be checked in polynomial time.
*NP-hard*	All NP-hard problems are not in NP and it takes a long time to check them.
*NP-complete*	A problem that is NP and NP-hard is NP-complete.

My problem is NP-hard. Lekker

### Practise

Running some practise scenarios in new dir "algorithmarium" to understand how pulp works.

Was pretty easy to write some stuff out manually and get results for small set. Might be difficult to scale, but could be done if the preferences are save well in easily accessible dictionaries or in classes and loops run through?

## 21 July 2025

Ramp up the speed a bit. Make some bigger practise data for a month in a data input folder and then write the framework to parse the csv files and saving the output. Even if the algorithm details are a bit later and that can be polished up. Will have the biggest return on investment for time. Guess we leaving the sql database idea for now possibly.

## 22 July 2025

Break

## 23 July 2025

Reviewing parsing csv into python files and then setting up how I will handle the data. 

Finished the input files. Decided would be nice to go with classes for the doctors, a class for the shifts (lenghths, how many on duty etc). Made a test folder to test various files manually for debugging. Doctor class work for the manual input. Now can be looped in the load_inputs file from the csv.

## 24 July 2025

doctor csv, shift class
