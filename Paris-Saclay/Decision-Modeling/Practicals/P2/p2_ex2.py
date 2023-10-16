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

# Map the preference functions to dictionary keys for easy reference
preference_functions = {
    'pref1': add_pref1,
    'pref2': add_pref2,
    'pref3': add_pref3,
    'pref4': add_pref4,
    'pref5': add_pref5
}

def solve_with_preferences(preferences):
    '''
    Solve the problem with a list of specific preferences.

    preferences: list of strings, each one a key in preference_functions
    '''
    # Set up the base problem
    x, prob = baseprob()

    # Add the preferences
    for pref in preferences:
        if pref in preference_functions:
            preference_functions[pref](x, prob)  # call the relevant function
        else:
            print(f"Unknown preference: {pref}")

    # Solve the problem
    print(f"Solving the problem with preferences: {preferences}...")
    prob.solve()
    print("Solved!")
    print("Status:", LpStatus[prob.status])

    # We print the visited sites
    print("Sites to visit:")
    visited_sites = get_list(prob.variables())
    print(visited_sites)

    return visited_sites  # or any other information you want from the solution


def kendall_coef(r1, r2):
    '''
    Compute the Kendall coefficient between two rankings. We use kendall tau-b.
    
    r1, r2: lists of lists, where each sublist contains items of the same rank,
    ordered from highest to lowest rank.
    
    Returns the Kendall coefficient between r1 and r2.
    '''
    # Map each item to its rank in r1 and r2
    r1_map = {item: i for i, sublist in enumerate(r1) for item in sublist}
    r2_map = {item: i for i, sublist in enumerate(r2) for item in sublist}

    # Compute the Kendall distance
    n = sum(len(sublist) for sublist in r1)

    nc, nd = 0,0 # Number of concordant and discordant pairs

    # Avoid re-comparing the same pairs
    compared_pairs = set()

    for sublist1 in r1:
        for sublist2 in r1:
            for item1 in sublist1:
                for item2 in sublist2:
                    # Create a consistent identifier for a pair of items
                    pair = tuple(sorted((item1, item2)))

                    # Skip if we've already compared this pair
                    if item1 == item2 or pair in compared_pairs:
                        continue

                    compared_pairs.add(pair)

                    # Compare ranks
                    different_orders = (r1_map[item1] < r1_map[item2] and r2_map[item1] > r2_map[item2]) or \
                                       (r1_map[item1] > r1_map[item2] and r2_map[item1] < r2_map[item2])

                    same_rank_in_r1 = r1_map[item1] == r1_map[item2]

                    if different_orders or (same_rank_in_r1 and r2_map[item1] != r2_map[item2]):
                        nd += 1
                    else:
                        nc += 1

    # Compute tie corrections
    n0 = n*(n-1)/2
    n1 = sum(ti*(ti-1)/2 for sublist in r1 for ti in [len(sublist)])
    n2 = sum(tj*(tj-1)/2 for sublist in r2 for tj in [len(sublist)])

    return (nc-nd) / ((n0-n1)*(n0-n2))**0.5

def spearman_coef(r1, r2):
    '''
    Compute the Spearman coefficient between two rankings.
    
    r1, r2: lists of lists, where each sublist contains items of the same rank,
    ordered from highest to lowest rank.
    
    Returns the Spearman coefficient between r1 and r2.
    '''
    # Order the items in r1 and r2 alphabetically
    r1 = [sorted(sublist) for sublist in r1]
    r2 = [sorted(sublist) for sublist in r2]
    # Assign ranks in r1, handling ties appropriately by assigning the average rank
    r1_map = {}
    current_rank = 1  # Ranking starts at 1
    for sublist in r1:
        # Calculate the average rank for the items in the sublist
        avg_rank = sum(range(current_rank, current_rank + len(sublist))) / len(sublist)
        for item in sublist:
            r1_map[item] = avg_rank
        current_rank += len(sublist)  # Update the rank for the next position

    # Assign ranks in r2, handling ties appropriately by assigning the average rank
    r2_map = {}
    current_rank = 1  # Ranking starts at 1
    for sublist in r2:
        # Calculate the average rank for the items in the sublist
        avg_rank = sum(range(current_rank, current_rank + len(sublist))) / len(sublist)
        for item in sublist:
            r2_map[item] = avg_rank
        current_rank += len(sublist)
    
    # Compute the Spearman coefficient: spearman = cov(r1,r2)/[std(r1)*std(r2)]
    r1_vec = [r1_map[item] for sublist in r1 for item in sublist]
    r2_vec = [r2_map[item] for sublist in r1 for item in sublist]

    avg_1 = sum(r1_vec)/len(r1_vec)
    avg_2 = sum(r2_vec)/len(r2_vec)

    cov = sum((a - avg_1) * (b - avg_2) for (a,b) in zip(r1_vec, r2_vec)) / len(r1_vec)

    var_1 = sum([((x - avg_1)**2) for x in r1_vec]) / len(r1_vec)
    std_1 = var_1 ** 0.5

    var_2 = sum([((x - avg_2)**2) for x in r2_vec]) / len(r2_vec)
    std_2 = var_2 ** 0.5

    spearman = cov / (std_1 * std_2)

    return spearman

            

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

    ListVisit1 = solve_with_preferences(['pref1'])

    compare_solutions(ListVisit, ListVisit1)
    print("----------------------------------------------")

    # 2:
    # Add restriction:
    # x_TE = 1 and x_CA = 1

    ListVisit2 = solve_with_preferences(['pref2'])

    compare_solutions(ListVisit, ListVisit2)
    print("----------------------------------------------")

    # 3:
    # Add restriction:
    # x_CN = 1 -> x_SC = 0, linearized as x_CN + x_SC <= 1
    
    ListVisit3 = solve_with_preferences(['pref3'])

    compare_solutions(ListVisit, ListVisit3)
    print("----------------------------------------------")

    # 4:
    # Add restriction:
    # x_TM = 1

    ListVisit4 = solve_with_preferences(['pref4'])

    compare_solutions(ListVisit, ListVisit4)
    print("----------------------------------------------")

    # 5:
    # Add restriction:
    # ML -> CP, linearized as x_ML - x_CP <= 0

    ListVisit5 = solve_with_preferences(['pref5'])

    compare_solutions(ListVisit, ListVisit5)
    print("----------------------------------------------")

    # B) Solve the poblem for Preference 1 and 2 together

    ListVisit12 = solve_with_preferences(['pref1', 'pref2'])

    compare_solutions(ListVisit, ListVisit12)
    print("----------------------------------------------")

    # C) Solve the poblem for Preference 1 and 3 together

    ListVisit13 = solve_with_preferences(['pref1', 'pref3'])

    compare_solutions(ListVisit, ListVisit13)
    print("----------------------------------------------")

    # D) Solve the poblem for Preference 1 and 4 together

    ListVisit14 = solve_with_preferences(['pref1', 'pref4'])

    compare_solutions(ListVisit, ListVisit14)
    print("----------------------------------------------")

    # E) Solve the poblem for Preference 2 and 5 together

    ListVisit25 = solve_with_preferences(['pref2', 'pref5'])

    compare_solutions(ListVisit, ListVisit25)
    print("----------------------------------------------")

    # F) Solve the poblem for Preference 3 and 4 together

    ListVisit34 = solve_with_preferences(['pref3', 'pref4'])

    compare_solutions(ListVisit, ListVisit34)
    print("----------------------------------------------")

    # G) Solve the poblem for Preference 4 and 5 together

    ListVisit45 = solve_with_preferences(['pref4', 'pref5'])

    compare_solutions(ListVisit, ListVisit45)
    print("----------------------------------------------")

    # H) Solve the poblem for Preference 1, 2 and 4 together

    ListVisit124 = solve_with_preferences(['pref1', 'pref2', 'pref4'])

    compare_solutions(ListVisit, ListVisit124)
    print("----------------------------------------------")

    # I) Solve the poblem for Preference 2, 3 and 5 together

    ListVisit235 = solve_with_preferences(['pref2', 'pref3', 'pref5'])

    compare_solutions(ListVisit, ListVisit235)
    print("----------------------------------------------")

    # J) Solve the poblem for Preference 2, 3, 4 and 5 together

    ListVisit2345 = solve_with_preferences(['pref2', 'pref3', 'pref4', 'pref5'])

    compare_solutions(ListVisit, ListVisit2345)
    print("----------------------------------------------")

    # K) Solve the poblem for Preference 1, 2, 4 and 5 together

    ListVisit1245 = solve_with_preferences(['pref1', 'pref2', 'pref4', 'pref5'])

    compare_solutions(ListVisit, ListVisit1245)
    print("----------------------------------------------")

    # L) Solve the poblem for Preference 1, 2, 3, 4 and 5 together

    print("Solving the problem with preference 1, 2, 3, 4 and 5...")

    ListVisit12345 = solve_with_preferences(['pref1', 'pref2', 'pref3', 'pref4', 'pref5'])

    compare_solutions(ListVisit, ListVisit12345)
    print("----------------------------------------------")

    # Problem:
    # We can define different preference relations between the sites:
    # - DUR: the ranking of the sites according to their duration
    # - APP: the ranking of the sites according to their appretiations
    # - PRI: the ranking of the sites according to their price
    # We want to compare this rankings using the Kendall and Spearman distances

    # A) Compute each preference relation:

    # DUR: list of lists, [[l1],[l2],...], all sites with the same duration are in the same list and the lists are ordered by duration (from the longest to the shortest)

    print("Computing the preference relation DUR...")
    DUR = []
    for i in range(9):
        DUR.append([])
    for i in range(len(sites_info)):
        DUR[8-int(sites_info[i][1]*2-1)].append(sites_info[i][0])
    # Remove empty lists
    DUR = [x for x in DUR if x != []]
    print(DUR)

    # APP: list of lists, [[l1],[l2],...], all sites with the same appretiations are in the same list and the lists are ordered by appretiations (from the highest to the lowest)
    print("----------------------------------------------")
    print("Computing the preference relation APP...")
    APP = []
    for i in range(5):
        APP.append([])
    for i in range(len(sites_info)):
        APP[4-int(sites_info[i][2].count('*'))-1].append(sites_info[i][0])
    # Remove empty lists
    APP = [x for x in APP if x != []]
    print(APP)

    # PRI: list of lists, [[l1],[l2],...], all sites with the same price are in the same list and the lists are ordered by price (from the lowest to the highest)
    print("----------------------------------------------")
    print("Computing the preference relation PRI...")
    PRI = []
    for i in range(31):
        PRI.append([])
    for i in range(len(sites_info)):
        PRI[int(sites_info[i][3])].append(sites_info[i][0])
    # Remove empty lists
    PRI = [x for x in PRI if x != []]
    print(PRI)

    # B) Compute the Kendall and Spearman coefficients between each pair of preference relations
    # Kendall coefficient: 
    print("----------------------------------------------")
    print("The Kendall coefficient between DUR and APP is:")
    print(kendall_coef(DUR, APP))
    print("----------------------------------------------")
    print("The Kendall coefficient between DUR and PRI is:")
    print(kendall_coef(DUR, PRI))
    print("----------------------------------------------")
    print("The Kendall coefficient between APP and PRI is:")
    print(kendall_coef(APP, PRI))

    # Spearman coefficient:
    print("----------------------------------------------")
    print("The Spearman coefficient between DUR and APP is:")
    print(spearman_coef(DUR, APP))
    print("----------------------------------------------")
    print("The Spearman coefficient between DUR and PRI is:")
    print(spearman_coef(DUR, PRI))
    print("----------------------------------------------")
    print("The Spearman coefficient between APP and PRI is:")
    print(spearman_coef(APP, PRI))
    print("----------------------------------------------")
    print("Conclusion:")
    print("- High disagreement between DUR and the others:\n\tIn both metrics, DUR is quite strongly negatively related to the other rankings.\n\tThis is an indication that prices and appreciations are not taking the duration too much into account.")
    print("- Slight agreement between APP and PRI:\n\t both metrics, these two rankings present a slight possitive correlation.\n\tThis indicates that the visitors take the price into account for their appreciations.")
    print("- Agreement between the two metrics:\n\tThe two metrics present very similar results, increasing our confidence in the conclusions.")