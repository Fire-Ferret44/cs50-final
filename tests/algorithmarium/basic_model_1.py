"""Basic model for testing csp concepts.
Initially we will try 5 doctors, 10 shifts over 10 days.
The only constraint is that no doctor can work two shifts in a row."""

doctors = ['A', 'B', 'C', 'D', 'E']
shifts = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

#Binary constraint --> i.e. value for 1 =/= value for 1 + 1

#Basic backtracking example:
def backtrack(assignment):
    #check if assignment is complete
    if len(assignment) == len(shifts):
        return assignment

    #make a dictionary of doctor: number of assigned shifts
    doc_count = {doc: 0 for doc in doctors}
    for assigned_doc in assignment.values():
        doc_count[assigned_doc] += 1
    
    #sort doctors by least assigned shifts (so that it can start assigning the least assigned next)
    sorted_doctors = sorted(doctors, key=lambda doc: doc_count[doc])

    #try a new variable in sorted list
    var = select_unassigned_variable(assignment)
    for value in sorted_doctors:
        new_assignment = assignment.copy()
        new_assignment[var] = value
        if consistent(new_assignment):
            result = backtrack(new_assignment)
            if result is not None:
                return result
    return None

def select_unassigned_variable(assignment):
    """Chooses a variable not yet assigned, in order."""
    for var in shifts:
        if var not in assignment:
            return var
    return None

#add a max_shift so the distribution is more even
max_shifts = round(len(shifts) // len(doctors))

def consistent(assignment):
    """Check if the assignment is consistent with the constraints."""
    for i in range(len(shifts) - 1):
        shift1 = shifts[i]
        shift2 = shifts[i + 1]
        if shift1 in assignment and shift2 in assignment:
            if assignment[shift1] == assignment[shift2]:
                return False
    
    """Check that no doctor has more than max_shifts assigned. """
    for value in doctors:
        count = sum(1 for v in assignment.values() if v == value)
        if count > max_shifts:
            return False

    #if no conflicts, return true
    return True

solution = backtrack({})
print("Assignment", solution)
