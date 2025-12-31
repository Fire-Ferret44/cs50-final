# Call Roster Generator

#### Video Demo: https://youtu.be/HYBaAVBuR5o

#### Description

Creating fair and efficient work rosters can be an exhausting and repetitive task, often done manually under time pressure. This project was born from a desire to streamline and automate that process in an effort to free up time and make it as un-biased as possible.

The Call Roster Generator aims to provide an simple backend system that takes user input and generates multiple, optimized, balanced roster suggestions. Metadata will then also be calculated and printed as a summary to check fairness.

Besides the scheduler logic, there are various different parts of the project that needed to be thought through. For example, parsing user input, the different classes for the doctors, shifts, calendar etc, date and calendar logic and how public holidays change day behaviour and shift needs. 

Here is the structure of the project:

## Project Structure

```
cs50-final/
├── .gitignore
├── app.py
├── DESIGN.md
├── main.py
├── README.md
├── requirements.txt
├── data/
│   ├── input/
│   │   ├── doctors.csv
│   │   ├── int_doctors.csv
│   │   ├── int_leave.csv
│   │   ├── in_pairing_constraints.csv
│   │   ├── leave.csv
│   │   ├── pairing_constraints.csv
│   │   ├── preferences.csv
│   │   ├── public_holidays_2025.csv
│   │   ├── schedule_period.csv
│   │   └── shift_structure.csv
│   ├── user_input/
│   │   └── uploaded_file_[number].csv (multiple per usage)
│   └── __init__.py
├── docs/
│   ├── algorithmarium.md
│   └── thought-journal.md
├── models/
│   ├── doctor.py
│   ├── metadata.py
│   ├── shift_calendar.py
│   ├── shift_structure.py
│   └── shift.py
├── scheduler/
│   ├── __init__.py
│   ├── random_scheduler.py
│   └── scheduler.py
├── services/
│   ├── load_inputs.py
│   └── metadata_generator.py
├── static/
│   ├── calendar_icon.ico
│   └── styles.css
├── templates/
│   ├── apology.html
│   ├── create.html
│   ├── generate.html
│   ├── index.html
│   ├── layout.html
│   └── result.html
├── tests/
│   ├── algorithmarium/
│   │   ├── basic_model_1.py
│   │   ├── basic_model_2.py
│   │   ├── basic_pulp_practise.py
│   │   └── int_model_1.py
│   ├── input/
│   │   ├── doctors.5_1.csv
│   │   └── shifts.10,1_1.csv
│   └── test_doctor.py
├── utility/
│   ├── __init__.py
│   ├── calendar_utils.py
│   ├── date_utils.py
│   ├── file_parser_utils.py
│   ├── filereader_utils.py
│   ├── flask_utils.py
│   └── formatter_utils.py
└── venv/
```
### Features

- Accept user input via CSV uploads
- Parses CSV files
- Generates a balanced, optomised roster from input with metadata.
- Output metadata summaries (e.g. total hours, weekend shifts)
- Export final rosters to downloadable text file

### Technologies Used

- WSL (Ubuntu): running Linux tools on Windows
- VS Code: development environment
- Python: core backend logic, scheduling algorithms
- Flask: lightweight web framework
- HTML: for front-end functionality
- Bootstrap / CSS: front-end styling
- Git / GitHub: version control

## Solver
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

## Thoughts and Takeaways

Initially the scope of this project was a lot larger (you can read about it in DESIGN.md which I have have kept as a legacy file). It including logins and different features being accessed by differently tiered users (E.g. an admin that create the roster request with parameters and then users that are being allocated shifts) that use room codes. The biggest out of scope part was trying to do weighted constraints in the solver. It became quickly evident that I would not get there in time.

I have noted what I worked on and what I did each day in the "thought-journal.md" file under docs.

A lot of the struggles I had were with syntax and interacting with the wrong thing. E.g. class vs dictionary vs list vs tuple. And then remembering what I called from where with which dependencies. I spent a lot of time on date and calendar logic.

All of the ideas I had put into the project where my own, but for many different aspects I used AI to review code or correct syntax mistakes or help understand why I was not getting certain expected outputs when I was doing my code. CoPilot also automatically filled in chunks of the code I was thinking about writing. The specific areas where this happened have not been commented out, but this was the case for the majority of the files.

You can access my workings, ideas and day-to-day input on the project in the thought-journal.md and algorithmarium.md under docs/.

That was CS50!