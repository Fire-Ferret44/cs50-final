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

Today some more theory around this problem and making a plan for a solution I want to try. Likely involving combination of approaches. Initial and then for optimisation. 

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

## 21 June 2025

Ramp up the speed a bit. Make some bigger practise data for a month in a data input folder and then write the framework to parse the csv files and saving the output. Even if the algorithm details are a bit later and that can be polished up. Will have the biggest return on investment for time. Guess we leaving the sql database idea for now possibly.

## 22 June 2025

Break

## 23 June 2025

Reviewing parsing csv into python files and then setting up how I will handle the data. 

Finished the input files. Decided would be nice to go with classes for the doctors, a class for the shifts (lenghths, how many on duty etc). Made a test folder to test various files manually for debugging. Doctor class work for the manual input. Now can be looped in the load_inputs file from the csv.

Update on the shift structure: Might need to be more generalised. E.g. Mon to Thur are exactly the same and can work as "weekday" blueprint. Fri, Sat and Sun will each be their own blue print potentially. And public holiday will either act as a Sun or Sat. Depending what day it is followed by. (Mon-Friday or Sat respectively). And the day preceding the public holiday will move from weekday --> friday or Sun --> Sat. 

## 24 June 2025

doctor upload function, shift class, seperate file and classes for how different days behave. Will need to map the string preferences to workable data types for the algorithm.

## 25 June 2025

So far have the following classes under utility:
-DayType, Doctor, ShiftCalendar, ShiftStructure, Shift

Following csv files under input:
-doctors, leave, pairing_constraints, preferences, public_holidays_2025, schedule_period, shift_structure

Following functions under load_inputs file:
-parse_date, generate_date_range, load_doctors, load_shift_structure, load_public_holidays, load_schedule_period, build_schedule_calendar

## 26 June 2025

Rearrange folders for better grouping. 
Focus on Input --> CSV --> Output to work on bigger structure flask and metadata. Then return to algorithm and work on the inner workings work.
Random scheduler to assign someone to every day. Bug fixed where only Fri, Sat, Sun were assigned. (Other days got confounded with day type and didn't get assigned.)

## 27 June 2025

...

## 28 June 2025

Continue working on basic data flow, flask and metadata for something to showcase in the demo video. 

## 29 June - 23 July 2025

Break

## 24 July 2025

Return to project!

View issues raised by SE-KLING:
1. add requirements.txt for dependency management
2. consider adding setup.py (package manager for python so others can setup and use easier)
3. update project structure to more standard organisation

1. yes! To be added when complete with project
2. watch tutorial how best to do this - possibly better to do when I have full pipeline to work on
3. yes! Work on changing this and then carry on working from there 

Dive back in and get to grips with concepts again after break. Let's get things done!

Notes re: re-organisation:
-models folder: class definitions etc? (-> this name will be confusing when there are different schedule models)
-type folder: type definitions? 
are the two folders above overlapping?
-I like load_inputs and load_metadata as names tbc...

## 25 July 2025

Completed restructuring. 
Append: Short shift can also not follow long shift as the person would be off in that time. 
Can short shift prepend long shift? Maybe, depends on facility

## 26 July 2025

Created utils for checking existing test files and then creating the following filename number. The test_x_schedule and test_x_metadata (where x is the file number) should have the same number value so they can be compared. Initially there will not be a metadata for each schedule test. 

Also created utils for formatting the schedule into txt that can be saved into a txt file under tests. Each file should have a time stamp in the beginning when the file was generated to refer back to. This same formatting can then also be printed.

Having the metadata which describes the DoctorMetadata class under types did not really make sense to me. I have moved it to where the other classes are described. load_metadata I will then name to metadata_generator and do the logic for calculating metadata here. With the formatter_utils I will then access this metadata_generator info to create the metadata txt output.

### Metadata

To create metadata I can loop through the roster the number of times there are doctors. This will be easier to do and easier to debug. A more efficient way of doing this would be to loop through the roster once and increment the different values for each doctor as you go. This will take less computing time, but I think at this stage that is negligible unless I look at a huge dataset with thousands of doctors and shifts. Even then. It would probably not take too long computationally. Big O order n*m

Once the basic things are done then can have a closer look at more nuanced metadata such as if preferences are granted and what satisfaction weight a preference has. 

Basic pipeline works with random schedule generator! For plan ahead:
1) continue with basic flask framework (csv input and txt output)
2) output with nicely formatted calendar
3) start on the actual scheduler with current data sets
4) input options on flask
5) SQL database, input interface for fixed shift settings
6) Different shift models and scheduler for different instances

## 27-28 July 2025

Simple html framework. So far for layout, index and create html files. Icon added for title. Basic navigation bar set up and styled with css. Entered form for csv files (required) in the create.html file.

## 29 July 2025

Goal for today is simple print to screen after intputting csv files. That will open up the space to move onto the scheduler logic. Also: think about renaming to a descriptive name.

Creating function in main that the flask app can call. 
Noticed: don't use shift_period value anywhere. Which is strange. Did I hard-code it somewhere? It's all under load_shift_calendar. Might have to consider changing so more modular? but currently working. Might be a problem the different helper functions for main call specific paths and not user input paths. 

Created a new file for parsing csv files. Apparently files uploaded via web form are "file-like" objects and are read as bytes if passed into another function. They need to be encoded and wrapped to be read as text. Can use io.StringIO or io.TextIOWrapper. Using read moves the pointer along the file and stream seek 0 needs to be used to take back to beginning. 

Reviewed a lot of basic things in python with debugging. E.g. syntax with loops, lists, dictionaries. Flash messages need a secret key (should not hardcode in real deployment).Will add to gitignore list

## 30 July 2025

Made session and updated functions to read uplaoded files in new directory and new filename taht includes session number.
schedule_period value found. Used within the load_shift_calendar function. Updated together for new filename.

A lot of debugging the different pages. Now there is a basic pipeline! Upload files, validate files, save files, run random scheduler, print schedule and metadata to screen.

HTML Short-term:
1. Print schedule in a calendar format
2. Print metadata in table so it can be easily scanned. Or even in a csv layout. 

(i.e. Change formatting in the utils so the printing is easier to read for both html and the testing main.py. Can aslo be saved as a csv file for accessing.)

After the results can be read easily, the real scheduler theory and work can begin.
(Don't forget to update the structure tree and the requirements.txt)

Instead of appending the metadata list with "\n". Changed to ", ". More or less well-algined for now to work on the scheduler tomorrow! Noticed inconsistency with the sum of weekdays worked in metadata. Fix bug.

A lot of other bugs creeped up now that I wanted to return back to working on main() after adding some arguments to functions etc. Now running well again. Formatted metadata also let's data be visualised easier. Both main() abd the functionf for flask run now. 

Now dedicated proper roster work can begin.

## 31 July - 3 August 2025

Break and travel back to place of work

## 4 - 6 August 2025

Gather resources for learning algorithms and methods. Textbooks prove difficult to understand with examples put in maths/logic notation. Stuck at beginning with computational complexity and getting caught up in terminology and distinctions that will not make a difference in my understanding the project. Combination of above lead to roadblock.

## 7 - 24 August 2025

Break and focus on work/other activities

## 25 - 29 August 2025

Restarted looking at notes started when looking at studying theory. Got caught in a rabbit hole of dynamic programming and memoisation. Specifically looked at the rod cutting problem, bottom-up solutions, fibonacci sequence with recursion vs memoisation, representation in nodes (trees, heights, levels) and grouping problem into subsets, time complexity, grid traveller, knapsack 1/0. Difficulty understanding how these fundamentals will directly help with solving problem of constraint-satisfaction. 

## 30 - 31 August 2025

Break

## 1 September 2025

Happy Spring Day! 

Today's focus is restarting and reframing. I have a focused list of concepts I want to go through in the next few days that include: terminology of CSPs and theory of different ways of solving this problem. I have found a video by the CS50 team ("Optimization - Lecture 3 - CS50's Introduction to Artificial Intelligence with Python 2020") that explains some of the topics. I think looking at these concepts and then breaking my problem in to small steps to grow on will be most beneficial. Not too much at once.

To keep this thought journal and what I learned more clear I will make a seperate file for what I learned for scheduling problems called "algorithmarium". The actual tests can be in a different directory, but the csp theory I will keep in this doc. Initionally I will work on a word doc externally and then paste things into the doc as I get more comfortable formatting with markdown - currently a distraction.

Make a small problem to try solve (10 days, 5 doctors). Initial 1 shift per day and then 2 shifts per day for 6 doctors. Too complicated with other csvs. Just create lists within the basic_model_1.py file.

## 2 September 2025

Looked at other lectures as well. Including some youtube videos (see CSP doc). Completed basic model 1 and made plan for what to include in basic model 2.

## 3 - 7 September 2025

Break

## 8 September 2025

Complete basic model 2. A lot of concepts reviewed and applied. (Outlined in CSP doc). Making connections between theory and practice. 

## 9 - 14 September 2025

Break

## 15 September 2025

Reviewed and refined made basic model 2. Smoothed out some features. Reviewed the whole file on chat and prompted for suggestions. Suggestions noted for intermediate model 1. Now time to bring in classes and utilites already worked on in general project to include days of the week in the intermediate model.

## 16 September 2025

Started with changing the variables and unary and binary constraints. It looks very nice. 

Started trying to fold in the classes and utilities like fluffy egg whites in batter.
More difficult than anticipated:
1. Paths to get to folder in the parent folder if run form inside the tests/algorithmarium folder.
2. the shift structure class does not have unique id or even dates in the structure. Perhaps something that needs to be changed for the whole project, but definitely something that needs to be addressed now otherwise it cannot be connected to algorithm and shift domain pairs. Can add the type of shift in the id. If there are 2x identical shifts in the weekend shifts slots can be assigned to differentiate the two shifts.
Shift_id = DDMMYY_<dow>_<shift_type>_<slot>
Add a date attribute to Shift class, with None passed in in def
Actual dates added in a loop in build_calendar function. 
Add shift_id to shift class also with None passed in in def. 
Actual shift_id made inside build_calendar function with schema above.

Because the shifts are different lengths through the week, it might be more difficult to look at unordered pairs. Now options to abandon all pairs and look at single shifts as single variables. Or look at the weekday shifts as single variables and the weekend shifts as pairs that can have binary constraints already shrink the domain from the get go.

What would be computationally easier and what would be more scalable? What if suddenly there are 3 slots? Do some things automatically move the consistency checking?

I want to keep the unary and binary constraints I had put in this model and add to basic model 2 because it looks nice and neat and may be useful in the future. Instead of deleting.

## 17 - 19 September 2025

Break for course

## 20 September 2025

Update basic model 2 with the ordered unary and binary constraints

## 21 September 2025

Updated terminal commands with .bashrc (changing pythn3 to python)

## 22 September 2025

Long break to focus on clinical learning and shifts and shadowing. Needed some help accessing different files in the directory from sub-folders.

## 6 November 2025

Returned to finish project. Definitely will take time to think through concepts again and understand what I have done so far. A bit frustrating to have lapsed so much time. For now it will be important to just finish an MVP that I can hand in and if I wanted to I could work on another project to have live on a webpage somewhere if I want to carry on with the project. 

Today the focus is on reviewing the manual algorithm steps in the basic and intermediate models then to move on to practical implication.

## 13 November 2025

Made thoughts on how to implement int_model_1 (in algorithmarium doc)
--> first make each shift a variable and each has its own domain of doctors

Errors fixed:
-shift structure csv changed from friday long and short to 2x friday long calls
-shift_id name changed from ddmmyy to yymmdd
-shift_id name change for slots from counting the same shift_types to using the number in required_staff
-inside the Shift class for dated shifts, the number required will =1 for every shift as each oen is now separated

int_model set to check each shift prints correctly for a given range and does. 

Used a lot of time to change how the shift_ids are made and how public holidays will work in the different classes and functions.

Changed: DayType Class in calendar_utils

## 14 November 2025

Shift work

## 15 - 17 November 2025

Fixed calendar_utils, shift_calendar
Updated: Shift class and ShiftCalendar class so it works better with reauired_staff and slots in shifts for each day. --> Can use the shift_id in combination with slots for binary checking of people working at the same time.
Updated: Calendar Utilities and added handling a case where there are multiple public holidays consecutively. 


## 24 November 2025

Handling cases for consecutive public holidays. Added how the day of week from the csv input maps to day_type behaviour as well as how public holidays would behave (i.e Saturday or Sunday). Updated ShiftStructure, ShiftCalendar classes to handle new variable names. 