"""Now we are gearing up a little bit.
Suggestions from previous model:
1. reviewing if pruning and working on copies is done safely and effectively.

Main aim of this model:
-Use current classes, functions and utilities from main project
-Work with real calendar period with April that has a public holiday
-Incorporate day types and shift_ids
-Use each shift as a variable rather than days with multiple shifts
-Balance hours and shift types over 21 days with 9 doctors
"""

#Now: will try 9 doctors, 42 shifts over 21 days.
#Constraints:
#- Mon-Thur = 1x long, 1x short shift (one doctor per shift)
#- Fri-Sun = 2x long shifts (one doctor per shift)
#- Public holiday = 2x long shifts (one doctor per shift)
#- no doctor can work two shifts in a row
#- D and E cannot work together
#- G must work with A, B, C or D (seniors)
#- A is on leave 1st to 4th
#- C is on leave 14th to 18th
#- E is on leave 14th to 15th
#- H has is on leave 9th and 10th
#- balance hours, balance long/short shifts, balance weekend shifts evenly
#- not on call adjacent weekend to leave

from collections import defaultdict
import random
from datetime import date, datetime, timedelta
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.shift_calendar import ShiftCalendar
from utility.calendar_utils import DayType
from services.load_inputs import (
    load_doctors,
    load_shift_structure,
    load_public_holidays,
)

#base_path = Path("data/input")
base_path = project_root / "data" / "input"

"""1 load doctors ("variables")"""
int_doctors = load_doctors(
    doctors_path=base_path / "int_doctors.csv",
    leave_path=base_path / "int_leave.csv",
    preferences_path=None,
    pairing_constraints_path=base_path / "int_pairing_constraints.csv",
)

doctors = list(int_doctors.keys())

"""2.1 load shift period"""
start_date = date(2025, 4, 1)
end_date = date(2025, 4, 21)

"""2.2 get shift slots ("nodes")"""
shift_structure = load_shift_structure(base_path / "shift_structure.csv", 0)
public_holidays = load_public_holidays(base_path)
day_type = DayType(public_holidays)
shift_calendar = ShiftCalendar(start_date, end_date, shift_structure, day_type)

shift_slots = []
shift_by_id = {}

for date, day_info in shift_calendar.calendar.items():
    for shift in day_info["shifts"]:
        shift_slots.append(shift.shift_id)
        shift_by_id[shift.shift_id] = shift

#Sort shift by date - normal sort as ymd format is already "alphabetical"
shift_slots.sort()

"""3. Generate initial domains for each shift slot"""
domains = {}
for shift_id in shift_slots:
    domains[shift_id] = doctors.copy()

"""3.1 Unary constraints"""
#3.1a Unary constraints: leave
def apply_leave_filter(shift_id, domain, int_doctors, shift_by_id):
    """Returns a list of doctors not on leave for the given shift"""
    shift = shift_by_id[shift_id]
    shift_date = shift.date

    valid_docs = []
    for doc in domain:
        doctor = int_doctors[doc]
        if shift_date not in doctor.leave_dates:
            valid_docs.append(doc)

    return valid_docs

#3.1b Unary constraint: doctors requiring overlap shifts cannot work non-overlap shifts
def apply_overlap_filter(shift_id, domain, int_doctors, shift_by_id):
    """Filters domains based on doctors requiring overlap"""
    shift = shift_by_id[shift_id]
    valid_docs = []

    for doc in domain:
        doctor = int_doctors[doc]

        if shift.overlap:
            valid_docs.append(doc)

        else:
            if not doctor.requires_overlap:
                valid_docs.append(doc)

    return valid_docs

"""3.2 Filter by unary constraints"""
for shift_id in shift_slots:
    domains[shift_id] = apply_leave_filter(
        shift_id,
        domains[shift_id],
        int_doctors,
        shift_by_id
    )

for shift_id in shift_slots:
    domains[shift_id] = apply_overlap_filter(
        shift_id,
        domains[shift_id],
        int_doctors,
        shift_by_id
    )

"""4. CSP solver framework"""

assignment = {}

doc_hours = {doc: 0 for doc in doctors} #to track number of assigned hours per doctor
doc_weekend_hours = {doc: 0 for doc in doctors} #to track number of assigned weekend hours per doctor

#4.1 Variable Selection: Minimum Remaining Values (MRV)
def select_unassigned_variable(assignment, domains):
    """Selects the unassigned variable with fewest remaining values in its domain."""
    unassigned = [var for var in domains if var not in assignment]
    mrv_var = min(unassigned, key=lambda var: len(domains[var]))

    #checks all mrv domains and selects randomly among ties
    candidates = [var for var in unassigned if len(domains[var]) == len(domains[mrv_var])]
    return random.choice(candidates)

#4.2 Value Ordering: Least Constraining Value (LCV)
def order_domain_values(shift_id, domains, doc_hours, doc_weekend_hours, shift_by_id):
    """Orders doctors for a shift based on least assigned hours (LCV)"""
    if not domains[shift_id]:
        return []

    shift = shift_by_id[shift_id]
    is_weekend = shift.date.weekday() >= 4 #this would include Friday-Sunday

    #sort by total assigned hours
    min_doc = min(domains[shift_id], key=lambda doc: doc_hours[doc])
    lowest_hours = doc_hours[min_doc]

    candidates = [doc for doc in domains[shift_id] if doc_hours[doc] == lowest_hours]

    if not is_weekend:
        random.shuffle(candidates)
        return candidates

    else:
        min_weekend_doc = min(candidates, key=lambda doc: doc_weekend_hours[doc])
        lowest_weekend_hours = doc_weekend_hours[min_weekend_doc]

        weekend_candidates = [doc for doc in candidates if doc_weekend_hours[doc] == lowest_weekend_hours]
        random.shuffle(weekend_candidates)
        return weekend_candidates

"""5. Consistency Checking Functions"""
#5.1 No doctor two shifts in one day
def violates_same_day(shift_id, doc, assignment, shift_by_id):
    """Checks if assigning doctor to shift violates same day constraint
       Returns True if violation occurs, False otherwise"""
    shift_date = shift_by_id[shift_id].date

    for assigned_shift_id, assigned_doc in assignment.items():
        if assigned_doc != doc:
            continue

        assigned_date = shift_by_id[assigned_shift_id].date
        if assigned_date == shift_date:
            return True

    return False

#5.2 No doctor two days in a row
def violates_consecutive_days(shift_id, doc, assignment, shift_by_id):
    """Checks if assigning doctor to shift violates consecutive days constraint
       Returns True if violation occurs, False otherwise"""
    shift_date = shift_by_id[shift_id].date

    for assigned_shift_id, assigned_doc in assignment.items():
        if assigned_doc != doc:
            continue

        assigned_date = shift_by_id[assigned_shift_id].date
        if abs((assigned_date - shift_date).days) == 1: #absolute value of timedelta 1 is consec.
            return True
    
    return False

#5.3 D and E cannot work together
def violates_avoid_pair(shift_id, doc, assignment, shift_by_id, int_doctors):
    """Checks if assigning doctor to shift violates avoid pair constraint
       Returns True if violation occurs, False otherwise"""
    shift_date = shift_by_id[shift_id].date
    doc_obj = int_doctors[doc]

    for assigned_shift_id, assigned_doc in assignment.items():
        assigned_date = shift_by_id[assigned_shift_id].date
        if assigned_date != shift_date:
            continue

        if assigned_doc in doc_obj.avoid_pair:
            return True

        if doc in int_doctors[assigned_doc].avoid_pair:
            return True

    return False

#5.4 G requires a pair from A-D
def violates_requires_pair(shift_id, doc, assignment, shift_by_id, int_doctors):
    """Checks if assigning doctor to shift violates requires pair constraint
       Returns True if violation occurs, False otherwise"""
    doc_obj = int_doctors[doc]

    if not doc_obj.requires_pair:
        return False

    shift_date = shift_by_id[shift_id].date
    required_partners = set(doc_obj.requires_pair)

    partner_found = False
    unassigned_shift_exists = False

    for other_shift_id, other_shift in shift_by_id.items():
        if other_shift.date != shift_date:
            continue

        if other_shift_id in assignment:
            assigned_doc = assignment[other_shift_id]
            if assigned_doc in required_partners:
                partner_found = True
        else:
            unassigned_shift_exists = True

    if partner_found:
        return False

    if unassigned_shift_exists:
        return False

    return True

"""6. Check consistency of assignment"""
def is_consistent(shift_id, doc, assignment, shift_by_id, int_doctors):
    if violates_same_day(shift_id, doc, assignment, shift_by_id):
        return False

    if violates_consecutive_days(shift_id, doc, assignment, shift_by_id):
        return False

    if violates_avoid_pair(shift_id, doc, assignment, shift_by_id, int_doctors):
        return False

    if violates_requires_pair(shift_id, doc, assignment, shift_by_id, int_doctors):
        return False

    return True

"""7. Backtracking Search Algorithm"""
def backtrack(assignment, domains):
    """Backtracking search algorithm to find a valid assignment"""
    if len(assignment) == len(domains):
        return assignment

    #Get the next shift with the MRV function
    shift_id = select_unassigned_variable(assignment, domains)

    #Try filling it with the LCV ordered doctors
    for doc in order_domain_values(
                shift_id,
                domains,
                doc_hours,
                doc_weekend_hours,
                shift_by_id
                ):
        if is_consistent(shift_id, doc, assignment, shift_by_id, int_doctors):
            assignment[shift_id] = doc
            doc_hours[doc] += shift_by_id[shift_id].hours

            if shift_by_id[shift_id].date.weekday() >= 4:
                doc_weekend_hours[doc] += shift_by_id[shift_id].hours

            result = backtrack(assignment, domains)
            if result is not None:
                return result

            #Backtrack
            del assignment[shift_id]
            doc_hours[doc] -= shift_by_id[shift_id].hours

            if shift_by_id[shift_id].date.weekday() >= 4:
                doc_weekend_hours[doc] -= shift_by_id[shift_id].hours

    return None

solution = backtrack(assignment, domains)

if solution is None:
    print("No solution found.")

else:
    print("Solution found:")
    for shift_id in sorted(solution.keys()):
        shift = shift_by_id[shift_id]
        doctor = solution[shift_id]
        print(f"Shift {shift_id} | Doctor {doctor}")

"""8. Iniitialise metadata tracking for doctors"""

doctor_stats = defaultdict(lambda: {
    "shifts": 0,
    "weekend_shifts": 0,
    "hours": 0,
})
for shift_id, doc in solution.items():
    shift = shift_by_id[shift_id]
    doctor_stats[doc]["shifts"] += 1
    doctor_stats[doc]["hours"] += shift.hours

    if shift.date.weekday() >= 4:
        doctor_stats[doc]["weekend_shifts"] += 1

print("\nDoctor Statistics:")
for doc, stats in doctor_stats.items():
    print(f"Doctor {doc}: Shifts={stats['shifts']}, Weekend Shifts={stats['weekend_shifts']}, Hours={stats['hours']}")
