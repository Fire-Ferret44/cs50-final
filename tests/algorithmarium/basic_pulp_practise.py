"""
First practise with small model and how to use pulp

Model: Weekday (incl Fri) Night Shifts with 3 Doctors (A, B, C)
- Days: Mon–Fri (1, 2, 3, 4, 5)
- Shifts: 16:00 to 08:00 (next morning)
- One doctor per night
- Max two shifts per week
- No back-to-back shifts
- Doctor B prefers to avoid Tuesday
"""

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus

doctors = ['A', 'B', 'C']
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

prob = LpProblem("Night_Shift_Schedule", LpMinimize) # Create the problem instance
x = LpVariable.dicts("shift", (doctors, days), cat="Binary") # Define binary variables: x[doc][day] == 1 if doc works that night

print("Startin scheduling...")

# Create objective: minimize
prob = LpProblem("Night_Shift_Schedule", LpMinimize)

# Constraint 1: Exactly one doctor per night
for day in days:
    prob += lpSum([x[doc][day] for doc in doctors]) == 1, f"One_shift_on_{day}" # Name constraints for clarity

# Constraint 2: No back-to-back shifts
for doc in doctors:
    for i in range(len(days) - 1):
        day1 = days[i]
        day2 = days[i + 1]
        prob += x[doc][day1] + x[doc][day2] <= 1, f"No_backtoback_{doc}_{day1}_{day2}"
    
# Constraint 3: Max 2 shifts per week
for doc in doctors:
    prob += lpSum([x[doc][day] for day in days]) <= 2, f"Max_2_shifts_{doc}"

# Constraint 4: Doctor B prefers to avoid Tuesday
prob += x["B"]["Tue"] == 0, "No_B_on_Tuesday"

# Soft constraint: Minimize Saturday shifts
penalty = lpSum([x[doc]["Sat"] for doc in doctors])
prob += penalty  # This will minimize the number of Saturday shifts overall

prob.solve()

print(f"Status: {LpStatus[prob.status]}")
for day in days:
    workers = [doc for doc in doctors if x[doc][day].varValue == 1]
    print(f"{day}: {', '.join(workers)}")
