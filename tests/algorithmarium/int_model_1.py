"""Now we are gearing up a little bit.
Suggestions from previous model: 1. reviewing if pruning and working on copies is done safely and effectively.
2. WOrk more modularly with pairs. E.g. global list of pairs that then gets whittled with a unary constraints
function and then by a binary constraints function. Then flesh out possibilities for each shift
with a get_valid_pairs function.

Main aim of this model: bring in hours, long and short shifts and days of the week. For this we will look at 
3 weeks (21 days) starting on a Monday and 8 doctors with more hard constraints.
"""

#Now: will try 8 doctors, 42 shifts over 21 days.
#Constraints:
#- Mon-Thur = 1x long, 1x short shift (one doctor per shift)
#- Fri-Sun = 2x long shifts (one doctor per shift)
#- no doctor can work two shifts in a row
#- D and E cannot work together
#- G must work with A, B or D
#- A is on leave 4th to 8th
#- E is on leave 11th to 15th
#- H has is on leave 11th and 12th
#- C is on leave 15th to 21st
#- balance hours, balance long/short shifts, balance weekend shifts evenly

from itertools import combinations
import random
from datetime import datetime
import sys
from pathlib import Path
# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
from services.load_inputs import (
    load_shift_structure,
    load_shift_calendar,
)

"""1. get doctors"""
doctors = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

"""2. get shift slots ("nodes")"""
#TO DO: Import shift class and shift calendar structures from "utility" and "models"
#base_path = Path("data/input")
base_path = project_root / "data" / "input"
shift_structure = load_shift_structure(base_path / "shift_structure.csv", filenumber=0) #copied from main and load_inputs
shift_calendar = load_shift_calendar(base_path, filenumber=0) #copied from main and load_inputs
#TO DO: Get shift period into model and see what shifts required etc

"""3. get doctor pairs for shift slots ("domain")"""
all_pairs = list(combinations(doctors, 2))
#TO DO: but! list for Mon to Thur must be unordered pairs, Fri to Sun unordered

"""4. shrink domains with constraints"""
#4.1Unary constraints:
leave = {
    'A': ['4', '5', '6', '7', '8'],
    'E': ['11', '12', '13', '14', '15'],
    'H': ['11', '12'],
    'C': ['15', '16', '17', '18', '19', '20', '21']
}

def filter_unary_constraints(shift, pairs):
    """Filters pairs based on their availability E.g. leave"""
    valid_pairs = []
    for doc1, doc2 in pairs:
        if shift not in leave.get(doc1, []) and shift not in leave.get(doc2, []):
            valid_pairs.append((doc1, doc2))
    return valid_pairs

def filter_binary_constraints(pairs):
    #4.2 Binary constraints:
    """Filters pairs based on compatibility E.g. who can/can't work with who"""
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

def get_valid_pairs(shift, all_pairs):
    """Apply unary then binary constraints in order."""
    unary_filtered_pairs = filter_unary_constraints(shift, all_pairs)
    binary_filtered_pairs = filter_binary_constraints(unary_filtered_pairs)
    return binary_filtered_pairs

shift_pairs = {}
for shift in shift_pairs:
    shift_pairs[shift] = get_valid_pairs(shift, all_pairs)

print(shift_pairs)
