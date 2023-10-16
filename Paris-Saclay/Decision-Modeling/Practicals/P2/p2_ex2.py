from pulp import *

pulp.LpSolverDefault.msg = False

sites_info = [ # (site, duration, appretiations, cost)
                ['TE', 9/2, '*****', 15.50],
                ['ML', 3, '****', 12],
                ['AT', 1, '***', 9.5],
                ['MO', 2, '**', 11],
                ['JT', 3/2, '***', 0],
                ['CA', 2, '****', 10],
                ['CP', 5/2, '*', 10],
                ['CN', 2, '*****', 5],
                ['BS', 2, '****', 8],
                ['SC', 3/2, '*', 8.5],
                ['PC', 3/4, '***', 0],
                ['TM', 2, '**', 15],
                ['AC', 3/2, '*****', 0]
            ]

distances = [
            [0.0, 3.8, 2.1, 2.4, 3.5, 4.2, 5.0, 4.4, 5.5, 4.2, 2.5, 3.1, 1.9],
            [3.8, 0.0, 3.8, 1.1, 1.3, 3.3, 1.3, 1.1, 3.4, 0.8, 1.7, 2.5, 2.8],
            [2.1, 3.8, 0.0, 3.1, 3.0, 5.8, 4.8, 4.9, 4.3, 4.6, 2.2, 4.4, 1.0],
            [2.4, 1.1, 3.1, 0.0, 0.9, 3.1, 2.5, 2.0, 3.9, 1.8, 1.0, 2.3, 2.1],
            [3.5, 1.3, 3.0, 0.9, 0.0, 4.2, 2.0, 2.4, 2.7, 2.0, 1.0, 3.4, 2.1],
            [4.2, 3.3, 5.8, 3.1, 4.2, 0.0, 3.5, 2.7, 6.5, 2.6, 3.8, 1.3, 4.9],
            [5.0, 1.3, 4.8, 2.5, 2.0, 3.5, 0.0, .85, 3.7, 0.9, 2.7, 3.4, 3.8],
            [4.4, 1.1, 4.9, 2.0, 2.4, 2.7, .85, 0.0, 4.5, 0.4, 2.8, 2.7, 3.9],
            [5.5, 3.4, 4.3, 3.9, 2.7, 6.5, 3.7, 4.5, 0.0, 4.2, 3.3, 5.7, 3.8],
            [4.2, 0.8, 4.6, 1.8, 2.0, 2.6, 0.9, 0.4, 4.2, 0.0, 2.5, 2.6, 3.6],
            [2.5, 1.7, 2.2, 1.0, 1.0, 3.8, 2.7, 2.8, 3.3, 2.5, 0.0, 3.0, 1.2],
            [3.1, 2.5, 4.4, 2.3, 3.4, 1.3, 3.4, 2.7, 5.7, 2.6, 3.0, 0.0, 2.1],
            [1.9, 2.8, 1.0, 2.1, 2.1, 4.9, 3.8, 3.9, 3.8, 3.6, 1.2, 2.1, 0.0]                  
            ]

def baseprob():
    '''
    Problem:
    Mr. Doe wants to visit the maximum number of sites in 12 hours with a budget of 65€

    max Sum_i x_i
    s.t. Sum_i t_i*x_i <= 12
         Sum_i c_i*x_i <= 65
    '''

    prob = LpProblem("Visit the maximum number of sites in 12 hours with a budget of 65€", LpMaximize)

    x = [LpVariable(sites_info[i][0] + ":x"+str(i), 0, 1, LpInteger) for i in range(len(sites_info))]

    prob += lpSum(x), "Number of sites to visit; to be maximized"

    prob += lpSum([sites_info[i][1]*x[i] for i in range(len(sites_info))]) <= 12, "Time constraint"
    prob += lpSum([sites_info[i][3]*x[i] for i in range(len(sites_info))]) <= 65, "Budget constraint"

    return x, prob

def add_pref1(x, prob):
    '''
    Add the preference 1 to the problem, i.e.:
    Pref 1: if two sites are within 1 km, he prefer to visit both of them
    '''
    for i in range(len(sites_info)):
        for j in range(len(sites_info)):
            if distances[i][j] <= 1:
                prob += x[i] - x[j] <= 0, "Pref 1: if two sites are within 1 km, he prefer to visit both of them, sites "+str(i)+" and "+str(j)

def add_pref2(x, prob):
    '''
    Add the preference 2 to the problem, i.e.:
    Pref 2: he wants to visit TE and CA
    '''
    prob += x[0] == 1, "Pref 2: he wants to visit TE"
    prob += x[5] == 1, "Pref 2: he wants to visit CA"

def add_pref3(x, prob):
    '''
    Add the preference 3 to the problem, i.e.:
    Pref 3: if he visits CN, then he will not visit SC
    '''
    prob += x[7] + x[9] <= 1, "Pref 3: if he visits CN, then he will not visit SC"

def add_pref4(x, prob):
    '''
    Add the preference 4 to the problem, i.e.:
    Pref 4: he wants to visit TM
    '''
    prob += x[11] == 1, "Pref 4: he wants to visit TM"

def add_pref5(x, prob):
    '''
    Add the preference 5 to the problem, i.e.:
    Pref 5: if he visits ML, then he also visits CP
    '''
    prob += x[1] - x[6] <= 0, "Pref 5: if he visits ML, then he also visits CP"

def get_list(v):
    '''
    Return the list of sites to visit
    '''
    ListVisit = []
    i = 0
    for var in v:
        if var.varValue == 1:
            ListVisit.append(var.name[0:2])
        i += 1
    return ListVisit

def compare_solutions(sol1, sol2):
    '''
    Compare the changes between two solutions
    '''
    if set(sol1) == set(sol2):
        print("This solution is same as the base problem")
    else:
        print("This solution is different from the base problem")
        print("In this case, we change sites:")
        print(set(sol1) - set(sol2))
        print("To:")
        print(set(sol2) - set(sol1))

if __name__ == "__main__":
    print("Solving the problem without preferences...")
    x, prob = baseprob()

    prob.solve()

    print("Solved!")

    print("Status:", LpStatus[prob.status])

    # We print the visited sites
    print("Sites to visit:")
    v = prob.variables()
    ListVisit = get_list(prob.variables())
    print(ListVisit)

    print("----------------------------------------------")

    # Problem:
    # Mr. Doe has some preferences about the sites to visit
    # - Pref 1: if two sites are within 1 km, he prefer to visit both of them
    # - Pref 2: he wants to visit TE and CA
    # - Pref 3: if he visits CN, then he will not visit SC
    # - Pref 4: he wants to visit TM
    # - Pref 5: if he visits ML, then he also visits CP

    # We want to give the list of places for each preference

    # A) Solve the problem with each preference and compare the solutions with the base problem

    # 1:
    # Add restriction:
    # d(i,j)<=1 -> x_i=x_j

    print("Solving the problem with preference 1...")

    x, prob1 = baseprob()
    add_pref1(x, prob1)

    prob1.solve()

    print("Solved!")

    print("Status:", LpStatus[prob1.status])

    # We print the visited sites
    print("Sites to visit:")
    ListVisit1 = get_list(prob1.variables())
    print(ListVisit1)

    compare_solutions(ListVisit, ListVisit1)
    print("----------------------------------------------")

    # 2:
    # Add restriction:
    # x_TE = 1 and x_CA = 1

    print("Solving the problem with preference 2...")

    x, prob2 = baseprob()
    add_pref2(x, prob2)

    prob2.solve()

    print("Solved!")

    print("Status:", LpStatus[prob2.status])

    # We print the visited sites
    print("Sites to visit:")
    ListVisit2 = get_list(prob2.variables())
    print(ListVisit2)

    compare_solutions(ListVisit, ListVisit2)
    print("----------------------------------------------")

    # 3:
    # Add restriction:
    # x_CN = 1 -> x_SC = 0, linearized as x_CN + x_SC <= 1
    
    print("Solving the problem with preference 3...")

    x, prob3 = baseprob()
    add_pref3(x, prob3)

    prob3.solve()

    print("Solved!")

    print("Status:", LpStatus[prob3.status])

    # We print the visited sites
    print("Sites to visit:")
    ListVisit3 = get_list(prob3.variables())
    print(ListVisit3)

    compare_solutions(ListVisit, ListVisit3)
    print("----------------------------------------------")

    # 4:
    # Add restriction:
    # x_TM = 1

    print("Solving the problem with preference 4...")

    x, prob4 = baseprob()
    add_pref4(x, prob4)

    prob4.solve()
    
    print("Solved!")

    print("Status:", LpStatus[prob4.status])

    # We print the visited sites
    print("Sites to visit:")
    ListVisit4 = get_list(prob4.variables())
    print(ListVisit4)

    compare_solutions(ListVisit, ListVisit4)
    print("----------------------------------------------")

    # 5:
    # Add restriction:
    # ML -> CP, linearized as x_ML - x_CP <= 0

    print("Solving the problem with preference 5...")

    x, prob5 = baseprob()
    add_pref5(x, prob5)

    prob5.solve()

    print("Solved!")

    print("Status:", LpStatus[prob5.status])

    # We print the visited sites
    print("Sites to visit:")
    ListVisit5 = get_list(prob5.variables())
    print(ListVisit5)

    compare_solutions(ListVisit, ListVisit5)
    print("----------------------------------------------")

    # B) Solve the poblem for Preference 1 and 2 together

    print("Solving the problem with preference 1 and 2...")

    x, prob12 = baseprob()
    add_pref1(x, prob12)
    add_pref2(x, prob12)

    prob12.solve()

    print("Solved!")

    print("Status:", LpStatus[prob12.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit12 = get_list(prob12.variables())
    print(ListVisit12)

    compare_solutions(ListVisit, ListVisit12)
    print("----------------------------------------------")

    # C) Solve the poblem for Preference 1 and 3 together

    print("Solving the problem with preference 1 and 3...")

    x, prob13 = baseprob()
    add_pref1(x, prob13)
    add_pref3(x, prob13)

    prob13.solve()

    print("Solved!")

    print("Status:", LpStatus[prob13.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit13 = get_list(prob13.variables())
    print(ListVisit13)

    compare_solutions(ListVisit, ListVisit13)
    print("----------------------------------------------")

    # D) Solve the poblem for Preference 1 and 4 together

    print("Solving the problem with preference 1 and 4...")

    x, prob14 = baseprob()
    add_pref1(x, prob14)
    add_pref4(x, prob14)

    prob14.solve()

    print("Solved!")

    print("Status:", LpStatus[prob14.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit14 = get_list(prob14.variables())
    print(ListVisit14)

    compare_solutions(ListVisit, ListVisit14)
    print("----------------------------------------------")

    # E) Solve the poblem for Preference 2 and 5 together

    print("Solving the problem with preference 2 and 5...")

    x, prob25 = baseprob()
    add_pref2(x, prob25)
    add_pref5(x, prob25)

    prob25.solve()

    print("Solved!")

    print("Status:", LpStatus[prob25.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit25 = get_list(prob25.variables())
    print(ListVisit25)

    compare_solutions(ListVisit, ListVisit25)
    print("----------------------------------------------")

    # F) Solve the poblem for Preference 3 and 4 together

    print("Solving the problem with preference 3 and 4...")

    x, prob34 = baseprob()
    add_pref3(x, prob34)
    add_pref4(x, prob34)

    prob34.solve()

    print("Solved!")

    print("Status:", LpStatus[prob34.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit34 = get_list(prob34.variables())
    print(ListVisit34)

    compare_solutions(ListVisit, ListVisit34)
    print("----------------------------------------------")

    # G) Solve the poblem for Preference 4 and 5 together

    print("Solving the problem with preference 4 and 5...")

    x, prob45 = baseprob()
    add_pref4(x, prob45)
    add_pref5(x, prob45)

    prob45.solve()

    print("Solved!")

    print("Status:", LpStatus[prob45.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit45 = get_list(prob45.variables())
    print(ListVisit45)

    compare_solutions(ListVisit, ListVisit45)
    print("----------------------------------------------")

    # H) Solve the poblem for Preference 1, 2 and 4 together

    print("Solving the problem with preference 1, 2 and 4...")

    x, prob124 = baseprob()
    add_pref1(x, prob124)
    add_pref2(x, prob124)
    add_pref4(x, prob124)

    prob124.solve()

    print("Solved!")

    print("Status:", LpStatus[prob124.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit124 = get_list(prob124.variables())
    print(ListVisit124)

    compare_solutions(ListVisit, ListVisit124)
    print("----------------------------------------------")

    # I) Solve the poblem for Preference 2, 3 and 5 together

    print("Solving the problem with preference 2, 3 and 5...")

    x, prob235 = baseprob()
    add_pref2(x, prob235)
    add_pref3(x, prob235)
    add_pref5(x, prob235)

    prob235.solve()

    print("Solved!")

    print("Status:", LpStatus[prob235.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit235 = get_list(prob235.variables())
    print(ListVisit235)

    compare_solutions(ListVisit, ListVisit235)
    print("----------------------------------------------")

    # J) Solve the poblem for Preference 2, 3, 4 and 5 together

    print("Solving the problem with preference 2, 3, 4 and 5...")

    x, prob2345 = baseprob()
    add_pref2(x, prob2345)
    add_pref3(x, prob2345)
    add_pref4(x, prob2345)
    add_pref5(x, prob2345)

    prob2345.solve()

    print("Solved!")

    print("Status:", LpStatus[prob2345.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit2345 = get_list(prob2345.variables())
    print(ListVisit2345)

    compare_solutions(ListVisit, ListVisit2345)
    print("----------------------------------------------")

    # K) Solve the poblem for Preference 1, 2, 4 and 5 together

    print("Solving the problem with preference 1, 2, 4 and 5...")

    x, prob1245 = baseprob()
    add_pref1(x, prob1245)
    add_pref2(x, prob1245)
    add_pref4(x, prob1245)
    add_pref5(x, prob1245)

    prob1245.solve()

    print("Solved!")

    print("Status:", LpStatus[prob1245.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit1245 = get_list(prob1245.variables())
    print(ListVisit1245)

    compare_solutions(ListVisit, ListVisit1245)
    print("----------------------------------------------")

    # L) Solve the poblem for Preference 1, 2, 3, 4 and 5 together

    print("Solving the problem with preference 1, 2, 3, 4 and 5...")

    x, prob12345 = baseprob()
    add_pref1(x, prob12345)
    add_pref2(x, prob12345)
    add_pref3(x, prob12345)
    add_pref4(x, prob12345)
    add_pref5(x, prob12345)

    prob12345.solve()

    print("Solved!")

    print("Status:", LpStatus[prob12345.status])

    # We print the visited sites

    print("Sites to visit:")
    ListVisit12345 = get_list(prob12345.variables())
    print(ListVisit12345)

    compare_solutions(ListVisit, ListVisit12345)
    print("----------------------------------------------")


