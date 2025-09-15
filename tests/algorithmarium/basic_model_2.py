"""This is going to be the same as basic_model_1.py but with additional constraints and
balancing number of shifts per doctor. Basic model 2 for testing csp concepts."""

# Now: will try 7 doctors,20 shifts over 10 days.
# Constraints:
# - 2 doctors per shift
# - no doctor can work two shifts in a row
# - spread evenly throughout the shift
# - A is on leave 4, 5 and 6 
# - E is on leave for 7, 8, 9 and 10
# - D and E cannot work together
# - G must work with A, B or D

from itertools import combinations
import random

doctors = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
shifts = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

#Unary constraints:
leave = {
    'A': ['4', '5', '6'],
    'E': ['7', '8', '9', '10']
}

def unary_constraint(shift, doctor):
    """Return True if doctor can work this shift."""
    return shift not in leave.get(doctor, [])

def get_valid_pairs(shift, doctors):
    """Return possible pairs that can work together on a given shift"""
    # doctors not on leave
    available_doctors = [doc for doc in doctors if unary_constraint(shift, doc)]
    
    # generate unordered pairs after unary constraints
    pairs = combinations(available_doctors, 2)

    # create list of valid pairs after binary constraints
    valid_pairs = []
    for doc1, doc2 in pairs:
        # D and E cannot work together
        if (doc1, doc2) in [('D', 'E'), ('E', 'D')]:
            continue
        # G must work with A, B or D
        if doc1 == 'G' and doc2 not in ['A', 'B', 'D']:
            continue
        if doc2 == 'G' and doc1 not in ['A', 'B', 'D']:
            continue
        valid_pairs.append((doc1, doc2))
    return valid_pairs

"""Create dictionary of shift: valid doctor pairs"""
shift_pairs = {}
for shift in shifts:
    shift_pairs[shift] = get_valid_pairs(shift, doctors)

#for shift, pairs in shift_pairs.items(): #number of pairs per shift out of interest
#    print(f"Shift {shift}: {len(pairs)} valid pairs")

def sorted_shifts(shift_pairs):
    """Sort shifts by number of valid pairs (ascending)"""
    return sorted(shift_pairs.keys(), key=lambda s: len(shift_pairs[s]))

#initialise dictionary to count number of shifts per doctor
doc_count = {doc: 0 for doc in doctors} 

#Basic backtracking example:
def backtrack(assignment, shift_pairs, doc_count):
    #check if assignment is complete
    if len(assignment) == len(shifts):
        return assignment

    #next shift variable:
    var = select_unassigned_variable(assignment, shift_pairs)
    
    #sort doctors by least assigned shifts (assign least assigned next)
    sorted_pairs = sorted(shift_pairs[var], key=lambda pair: doc_count[pair[0]] + doc_count[pair[1]])
    
    #get all pairs with minimum sum of assigned shifts
    min_sum = min(doc_count[pair[0]] + doc_count[pair[1]] for pair in sorted_pairs)
    min_pairs = [pair for pair in sorted_pairs if doc_count[pair[0]] + doc_count[pair[1]] == min_sum]
    random.shuffle(min_pairs) #add variability

    #try next pair variable in sorted list:
    for pair in min_pairs:
        if consistent(pair, doc_count, assignment, var):
            #pruning adjacent domains (remove back-to-back shift possibilities)
            shift_pair_copy = {}
            adjacent_shifts = []

            #get adjacent shifts
            shift_index = shifts.index(var)
            if shift_index > 0:
                adjacent_shifts.append(shifts[shift_index - 1])
            if shift_index < len(shifts) - 1:
                adjacent_shifts.append(shifts[shift_index + 1])

            #check for dead ends early
            dead_end = False
            for a in adjacent_shifts:
                shift_pair_copy[a] = shift_pairs[a].copy()
                shift_pairs[a] = [p for p in shift_pairs[a] if pair[0] not in p and pair[1] not in p]
                if not shift_pairs[a]: #no valid pairs left
                    dead_end = True
                    break
            
            if dead_end:
                #undo pruning
                for s, original in shift_pair_copy.items():
                    shift_pairs[s] = original
                continue #if no dead ends continue

            #assign pair
            assignment[var] = pair
            
            #update doc_count
            doc_count[pair[0]] += 1
            doc_count[pair[1]] += 1
            
            #recurse 
            result = backtrack(assignment, shift_pairs, doc_count)
            if result is not None:
                return result
            
            #undo
            del assignment[var]
            doc_count[pair[0]] -= 1
            doc_count[pair[1]] -= 1
                
    return None

def select_unassigned_variable(assignment, shift_pairs):
    """Chooses a variable not yet assigned, in order starting with fewest valid pairs."""
    # for var in sorted_shifts(shift_pairs):
    #     if var not in assignment:
    #         return var
    # return None
    
    #randomised version to add variability
    unassigned = [s for s in (shift_pairs) if s not in assignment]
    
    #min number of valid pairs
    min_len = min(len(shift_pairs[s]) for s in unassigned)

    #all possible pairs with min len (if only 1, then 1)
    possible_vars = [s for s in unassigned if len(shift_pairs[s]) == min_len]

    #chooses randomly from possible vars
    return random.choice(possible_vars) if possible_vars else None

#add a max_shift so the distribution is more even
max_shifts = round(len(shifts) // len(doctors)) + 2

def consistent(pair, doc_count, assignment, var):
    """Check if the assignment is consistent with the constraints."""
    """Check no doctor is working both shifts in a day (double check as already checked in valid pairs)"""
    if pair[0] == pair[1]:
        return False

    """Check that no doctor has more than max_shifts assigned. """
    for doc in pair:
        if doc_count[doc] + 1 > max_shifts:
            return False
    
    """Check no doctor has back-to-back shifts."""
    #shift index to look at specific shifts surrounding current shift
    shift_index = shifts.index(var)

    #check previous shift
    if shift_index > 0:
        prev_shift = shifts[shift_index - 1]
        if prev_shift in assignment:
            if pair[0] in assignment[prev_shift] or pair[1] in assignment[prev_shift]:
                return False
    
    #check following shift
    if shift_index < len(shifts) - 1:
        next_shift = shifts[shift_index + 1]
        if next_shift in assignment:
            if pair[0] in assignment[next_shift] or pair[1] in assignment[next_shift]:
                return False

    #if no conflicts, return true
    return True

solution = backtrack({}, shift_pairs, {doc: 0 for doc in doctors})

for shift in sorted(solution.keys(), key=lambda x: int(x)):
    print(f"Shift {shift}: {solution[shift]}")
    
print("Shifts per doctor:", {doc: sum(1 for pair in solution.values() if doc in pair) for doc in doctors})
