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

doctors = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
shifts = [] #populate with the classes and shift period functions I have already created

#Unary constraints:
leave = {
    'A': ['4', '5', '6', '7', '8'],
    'E': ['11', '12', '13', '14', '15'],
    'H': ['11', '12'],
    'C': ['15', '16', '17', '18', '19', '20', '21']
}

