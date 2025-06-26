# Call Roster Generator

#### Video Demo: <URL here> when ready

#### Description

Creating fair and efficient work rosters can be an exhausting and repetitive task, often done manually under time pressure. This project was born from a desire to streamline and automate that process - in effort to free up time and make it as un-biased as possible.

The Call Roster Generator aims to provide an intelligent backend system that takes user-defined constraints (e.g. working hours, preferences, seniority, etc.) and generates multiple, optimized, balanced roster suggestions. While it is currently designed with healthcare shifts in mind, it is generalizable to timetabling subjects for schools, assigning anaethetists in the theatre suite, or any setting that requires complex scheduling.

Ultimately, I want this tool to be not just a utility, but a launchpad for deeper learning in backend development, algorithms, and real-world application of Python and SQL — and eventually, a fully functional web application.

#### Features

- Accept user input via CSV uploads or web forms (planned)
- Automatically generate optimized, balanced rosters that can be edited
- Enforce constraints like fair hour distribution, senior/junior pairing, weekend preferences, etc.
- Output metadata summaries (e.g. total hours, weekend shifts, preference matches)
- Plan for secure, multi-user access via unique room keys
- Export final rosters to CSV or printable formats
- Future plan: fully interactive front-end web app (Flask-based)

#### Technologies Used

- WSL (Ubuntu): running Linux tools on Windows
- VS Code: development environment
- Python: core backend logic, scheduling algorithms
- SQLite: storing data
- Flask: lightweight web framework (planned)
- JavaScript / HTML: for front-end functionality (planned)
- Bootstrap / CSS: front-end styling (planned)
- Git / GitHub: version control and collaboration


## Project Structure

```
cs50-final/
├── .gitignore
├── app.py
├── main.py
├── DESIGN.md
├── README.md

├── data/
│   ├── input/
│   │   ├── doctors.csv
│   │   ├── leave.csv
│   │   ├── pairing_constraints.csv
│   │   ├── preferences.csv
│   │   ├── public_holidays_2025.csv
│   │   ├── schedule_period.csv
│   │   └── shift_structure.csv
│   └── __init__.py

├── scheduler/
│   ├── __init__.py
│   └── scheduler.py

├── utility/
│   ├── __init__.py
│   ├── day_type.py
│   ├── doctor.py
│   ├── load_inputs.py
│   ├── shift.py
│   ├── shift_calendar.py
│   └── shift_structure.py

├── tests/
│   ├── algorithmarium/
│   │   └── week1_basic_model.py 
│   └── test_doctor.py

├── docs/
│   └── thought-journal.md

├── venv/
```