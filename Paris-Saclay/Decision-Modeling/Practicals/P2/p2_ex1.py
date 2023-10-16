# Problem:
# A toy manufacturing organization manufactures two types of toys A and B. 
# Both the toys are sold at 25 e and 20 e respectively.
# There are 2000 resource units available every day from which
#   the toy A requires 20 units while 
#   toy B requires 12 units. 
# Both of these toys require a production time of 5 minutes. 
# Total working hours are 9 hours a day. 
# What should be the manufacturing quantity for each of the pipes to maximize the profits?

# max 25*A + 20*B
# s.t. 20*A + 12*B <= 2000
#      5*A + 5*B <= 9*60

# Let's solve this problem using PuLP

from pulp import *

prob = LpProblem("Toy Manufacturing", LpMaximize)

A = LpVariable("Units of A", 0, None, LpInteger)
B = LpVariable("Units of B", 0, None, LpInteger)

prob += 25*A + 20*B, "Profit; to be maximized"

prob += 20*A + 12*B <= 2000, "Resource constraint"
prob += 5*A + 5*B <= 9*60, "Time constraint"

prob.solve()

print("Status:", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Total profit = ", value(prob.objective))