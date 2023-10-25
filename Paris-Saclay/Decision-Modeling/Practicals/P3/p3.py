import openpyxl
import random
import string
import heapq

def create_voting_profiles():
    # Create a new workbook
    wb = openpyxl.Workbook()
    # Select the active worksheet
    ws = wb.active
    # Define the voting profiles
    profiles = [
        [5, ['a', 'b', 'c', 'd']],
        [4, ['a', 'c', 'b', 'd']],
        [2, ['d', 'b', 'a', 'c']],
        [6, ['d', 'b', 'c', 'a']],
        [8, ['c', 'b', 'a', 'd']],
        [2, ['d', 'c', 'b', 'a']]
    ]
    # Write the voting profiles to the worksheet
    for profile in profiles:
        for _ in range(profile[0]):
            ws.append(profile[1])
    # Save the workbook, overwriting the previous file
    wb.save('data.xlsx')

def read_voting_profiles(datafile):
    # Open the workbook
    wb = openpyxl.load_workbook(datafile)
    # Select the active worksheet
    ws = wb.active
    # Read the voting profiles
    profiles = {}
    for row in ws.iter_rows(min_row=1, max_col=4):
        profile = ''
        for cell in row:
            profile += cell.value
        
        if profile not in profiles.keys():
            profiles[profile] = 1
        else:
            profiles[profile] += 1
    
    return profiles

def SimpleMajorityRulefor2(profiles,a = 'a', b = 'b'):
    '''
    Given a set of voting profiles, and two alternatives a and b, return the winner according to the simple majority rule
    '''
    # Initialize the votes
    votes = {a: 0, b: 0}
    # Count the votes, X gets a vote if X is preferred to Y in the profile
    try:
        for profile in profiles:
            a_idx = profile.index(a)
            b_idx = profile.index(b)
            if a_idx < b_idx:
                votes[a] += profiles[profile]
            else:
                votes[b] += profiles[profile]
        # Return the winner
        if votes[a] > votes[b]:
            return a
        else:
            return b
    except:
        print('\033[91mInvalid alternatives!\033[00m')
        return None
    
def Plurality(profiles):
    '''
    Given a set of profiles, return the winner according to the plurality rule.
    In case of a tie, resolve it by lexicographic order.
    '''
    # Initialize the votes
    votes = {}
    # Count the votes
    for profile in profiles:
        if profile[0] not in votes.keys():
            votes[profile[0]] = 1
        else:
            votes[profile[0]] += 1
    # Return the winner, in case of a tie, resolve it by lexicographic order
    return max(votes, key=lambda x: (votes[x], x))

def PluralityRunoff(profiles):
    '''
    Given a set of profiles, return the winner according to the plurality runoff rule.
    In case of a tie, resolve it by lexicographic order.
    '''
    # Initialize the votes for the first round
    votes = {}
    # Count the votes for the first round
    for profile in profiles:
        if profile[0] not in votes.keys():
            votes[profile[0]] = 1
        else:
            votes[profile[0]] += 1
    # Second round: Find the two candidates with the most votes
    first_round = [max(votes, key=lambda x: (votes[x], x))]

    # If in the first round there is a candidate with more than half of the votes, return it
    if votes[first_round[0]] > sum(votes.values())/2:
        return first_round[0]
    
    votes.pop(first_round[0])
    first_round.append(max(votes, key=lambda x: (votes[x], x)))
    # Return the winner of the second round
    return SimpleMajorityRulefor2(profiles, first_round[0], first_round[1])

def CondorcetVoting(profiles):
    '''
    Given a set of profiles, return the winner according to the Condorcet voting rule.
    If there is no Condorcet winner, return None.
    '''
    # Get the alternatives
    alternatives = []
    # It's enough to check the first profile
    key_profile = list(profiles.keys())[0]
    for alternative in key_profile:
        alternatives.append(alternative)

    # Initialize the votes
    votes = {}
    # Count the votes
    for i in range(len(alternatives)-1):
        for j in range(i+1, len(alternatives)):
            winner = SimpleMajorityRulefor2(profiles, alternatives[i], alternatives[j])
            if winner not in votes.keys():
                votes[winner] = 1
            else:
                votes[winner] += 1
    # Return the winner, if there is no Condorcet winner, return None
    if max(votes.values()) == len(alternatives) - 1:
        return max(votes, key=lambda x: (votes[x], x))
    else:
        return None

def BordaVoting(profiles):
    '''
    Given a set of profiles, return the winner according to the Borda voting rule.
    In case of a tie, resolve it by lexicographic order.
    '''
    # Initialize the votes
    votes = {}
    # Count the votes
    for profile in profiles:
        for i in range(len(profile)):
            if profile[i] not in votes.keys():
                votes[profile[i]] = (i+1)*profiles[profile]
            else:
                votes[profile[i]] += (i+1)*profiles[profile]
    # Return the winner, in case of a tie, resolve it by lexicographic order
    return min(votes, key=lambda x: (votes[x], x))

def generateRandomProfile(m=6):
    '''
    Generate a random profile with m alternatives
    '''
    alternatives = list(string.ascii_lowercase)[:m]
    random.shuffle(alternatives)
    # Return the profile as a string
    return ''.join(alternatives)

def generateRandomProfiles(n=40, m=6, thr=0.25):
    '''
    Generate n random profiles with m alternatives
    '''
    gen_profiles = {}
    profile = None
    thr = thr / min(100,n)
    for _ in range(n):
        rnd = random.random()
        if rnd < thr or profile == None:
            profile = generateRandomProfile(m)
        if profile not in gen_profiles.keys():
            gen_profiles[profile] = 1
        else:
            gen_profiles[profile] += 1
    return gen_profiles

def check_preferences(profiles):
    '''
    Check if at least 10% of voters have different preferences
    If the maximum number of voters with the same preferences is greater than 90% of the total number of voters, return False
    '''
    max_votes = max(profiles.values())
    if max_votes > 0.9*sum(profiles.values()):
        return False
    else:
        return True
    
def check_candidates(profiles):
    '''
    Check it no more than 70% of voters have the same best candidate
    If the number of voters with the best candidate is greater than 70% of the total number of voters, return False
    '''
    best_candidates = {}
    for profile in profiles:
        if profile[0] not in best_candidates.keys():
            best_candidates[profile[0]] = profiles[profile]
        else:
            best_candidates[profile[0]] += profiles[profile]
    max_votes = max(best_candidates.values())
    if max_votes > 0.7*sum(profiles.values()):
        return False
    else:
        return True
    
def validate(profiles):
    '''
    Validate the profiles
    '''
    if check_preferences(profiles) and check_candidates(profiles):
        return True
    else:
        return False
    
def generateValidProfiles(n=40, m=6):
    '''
    Generate n valid profiles with m alternatives
    '''
    profiles = generateRandomProfiles(n, m)
    while not validate(profiles):
        profiles = generateRandomProfiles(n, m)
    return profiles

def allWinner(n=40, m=6):
    '''
    Generate a profile with n voters and m candidates in which the winner wins all the types of voting rules
    '''
    while True:
        profiles = generateValidProfiles(n, m)
        if Plurality(profiles) == PluralityRunoff(profiles) == CondorcetVoting(profiles) == BordaVoting(profiles):
            return profiles
        
def eachWinner(n=40, m=6):
    '''
    Generate a profile with n voters and m candidates in which a different candidate wins each type of voting rule
    '''
    while True:
        profiles = generateValidProfiles(n, m)
        if CondorcetVoting(profiles) is None:
            continue

        if Plurality(profiles) != PluralityRunoff(profiles) != CondorcetVoting(profiles) != BordaVoting(profiles):
            return profiles
        
###################################
# Here, we perform the generation #
# using genetic algorithms        #
###################################
# 1. Representation: Each voter's preference is a list of candidates, and each solution is a list of all voters' preferences.
def generate_random_solution(num_voters, num_candidates):
    return generateRandomProfiles(num_voters, num_candidates)

def calculate_fitness(solution, n=40, m=6):
    # Initialize variables to hold information about the current solution.
    candidate_wins = {candidate: 0 for candidate in list(string.ascii_lowercase)[:m]}
    profile_counts = {}
    top_candidate_counts = {candidate: 0 for candidate in list(string.ascii_lowercase)[:m]}

    for profile in solution:
        # Update the count for the voter's top candidate.
        top_candidate_counts[profile[0]] += solution[profile]

        # Serialize the voter's rankings to a profile string and update the profile count.
        profile_counts[profile] = profile_counts.get(profile, 0) + 1

    # Simulate voting to see which candidate wins in each method.
    # Plurality:
    winner = Plurality(solution)
    candidate_wins[winner] += 1
    winner = PluralityRunoff(solution)
    candidate_wins[winner] += 1
    winner = CondorcetVoting(solution)
    if winner is not None:
        candidate_wins[winner] += 1
    winner = BordaVoting(solution)
    candidate_wins[winner] += 1

    # Check how many voting methods resulted in the same winner.
    max_wins = max(candidate_wins.values())
    consistent_wins = 1 if max_wins == 4 else 0  # Assign a high reward if one candidate wins all methods.

    # Check if the profiles are diverse enough.
    max_same_profile = max(profile_counts.values())
    diverse_profiles = 1 if max_same_profile / n < 0.9 else 0

    # Check if no single candidate is the top preference for too many voters.
    max_same_top_candidate = max(top_candidate_counts.values())
    diverse_top_candidate = 1 if max_same_top_candidate / n < 0.7 else 0

    # Combine the individual scores into an overall fitness score. 
    # The weights for each component can be adjusted depending on their importance.
    fitness = (3 * consistent_wins + 2 * diverse_profiles + diverse_top_candidate)

    return fitness

def select_parents(population, fitnesses):
    # Calculate the total fitness of all individuals in the population.
    total_fitness = sum(fitnesses)
    
    # If all solutions are equally unfit, random selection can be performed
    if total_fitness == 0:
        return random.choice(population), random.choice(population)

    # Normalize individual fitnesses between 0 and 1.
    normalized_fitnesses = [f / total_fitness for f in fitnesses]

    # Calculate the cumulative probability for each individual.
    cumulative_prob = [sum(normalized_fitnesses[:i+1]) for i in range(len(normalized_fitnesses))]

    # Select two parents via roulette wheel selection.
    parents = []
    for _ in range(2):  # Doing this twice to select two parents
        # Generate a random number and find the first individual that has a higher cumulative probability.
        rand = random.random()
        for i in range(len(cumulative_prob)):
            if rand <= cumulative_prob[i]:
                parents.append(population[i])
                break

    return parents[0], parents[1]  # return the two selected parents

# 4. Crossover: Combine two solutions to make a new solution.
def crossover(parent1, parent2, n, crossover_rate=0.7):
    '''
    Combines two parent voting profiles into a single child profile, preferring profiles with higher counts.
    parent1, parent2: Dictionaries representing counts of different voting profiles.
    n: The total number of voters to be represented in the child.
    crossover_rate: The probability that crossover will occur.
    '''
    # If the random value exceeds the crossover rate, just pick one parent entirely at random for the next generation.
    if random.random() >= crossover_rate:
        return parent1 if random.random() < 0.5 else parent2

    # Merge the profiles from both parents, summing the counts for each profile.
    all_profiles = {}
    for profile, count in parent1.items():
        all_profiles[profile] = all_profiles.get(profile, 0) + count

    for profile, count in parent2.items():
        all_profiles[profile] = all_profiles.get(profile, 0) + count

    # Create a priority queue (as a max heap) so we can easily retrieve the profiles with the most votes.
    # The heap will contain tuples where the count is first (so it's sorted by count), then the profile.
    max_heap = [(-count, profile) for profile, count in all_profiles.items()]  # We use negative counts because heapq is a min-heap by default.
    heapq.heapify(max_heap)

    child = {}
    current_voters = 0  # Keep track of how many voters we've added to the child so far.

    while current_voters < n:
        if max_heap:  # If there are still profiles to process
            # Pop the profile with the most votes. Since we negated the counts earlier, we negate it again here to get the original count.
            count, profile = heapq.heappop(max_heap)
            original_count = -count  # Restore the original count by negating.

            # If adding this profile would exceed the number of voters, we adjust the count.
            # This avoids having more voters in the child than intended.
            if current_voters + original_count > n:
                original_count = n - current_voters  # Adjust the count to fill up the remaining "slots".

            # Add this profile to the child.
            child[profile] = original_count
            current_voters += original_count  # Update the count of voters added to the child so far.
        else:
            # In the unlikely event that we've run out of profiles, we would have to stop even if we haven't reached 'n' voters.
            break

    return child

    return child

# 5. Mutation: Randomly alter the solutions.
def mutate(solution, mutation_rate=0.1):
    for prefs in solution:
        if random.random() < mutation_rate:
            i, j = random.sample(range(len(prefs)), 2)
            prefs[i], prefs[j] = prefs[j], prefs[i]  # Swap two candidates for this voter.

# Bringing it all together
def run_genetic_algorithm(n=40, m=6, population_size=100, max_generations=1000):
    # Generate the initial population
    population = [generate_random_solution(n, m) for _ in range(population_size)]

    for _ in range(max_generations):
        # Calculate fitness for the population
        fitnesses = [calculate_fitness(solution, n, m) for solution in population]

        # Check for solution that satisfies all conditions, and could be considered as the 'winner'
        for solution, fitness in zip(population, fitnesses):
            if fitness >= 6:  # or meets your conditions in a way you define
                return solution

        # Create the next generation
        new_population = []
        while len(new_population) < n:
            parent1, parent2 = select_parents(population, fitnesses)
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        population = new_population

    print("No solution met all conditions in {} generations.".format(max_generations))
    # You might return the best solution found, even if it doesn't meet all conditions, or handle this case differently.

if __name__ == '__main__':
    datafile = input('Enter the path to the data file (default: data.xlsx) or input "create" to create a new data file: ')
    if datafile == '':
        datafile = 'data.xlsx'
    if datafile == 'create':
        create_voting_profiles()
    else:
        profiles = read_voting_profiles(datafile)
    
    option = ''

    while option != '0':
        option = ''
        option = input('\033[93mEnter the action you want to perform:\n'+
                    '\t1. Show the voting profiles\n'+
                    '\t2. Simple majority rule for two alternatives\n'+
                    '\t3. Plurality rule\n'+
                    '\t4. Plurality runoff rule\n'+
                    '\t5. Condorcet voting rule\n'+
                    '\t6. Borda voting rule\n'+
                    '\t7. Generate a profile that wins all (randomly)\n'+
                    '\t8. Generate a profile in which a different candidate wins each type of voting rule\n'+
                    '\t9. Generate a profile that wins all (genetic algorithm)'
                    '\t0. Exit\n'+
                    'Your choice: \033[00m')
        if option == '1':
            for profile in profiles: # profile is formatted: 'abcd' -> a>b>c>d
                formatted_profile = ''
                for alternative in profile:
                    formatted_profile += alternative + '>'
                print("There are", profiles[profile], "with profile", formatted_profile[:-1])
            input('\033[96mPress enter to continue...\033[00m')
        elif option == '2':
            a = input('Enter the first alternative: ')
            b = input('Enter the second alternative: ')
            winner = SimpleMajorityRulefor2(profiles, a, b)
            if winner != None:
                print('The winner is', winner)
            input('\033[96mPress enter to continue...\033[00m')
        elif option == '3':
            print("The winner is", Plurality(profiles), "according to the plurality rule.")
            input('\033[96mPress enter to continue...\033[00m')
        elif option == '4':
            print("The winner is", PluralityRunoff(profiles), "according to the plurality runoff rule.")
            input('\033[96mPress enter to continue...\033[00m')
        elif option == '5':
            winner = CondorcetVoting(profiles)
            if winner != None:
                print('The winner is', winner)
            else:
                print('There is no Condorcet winner.')
            input('\033[96mPress enter to continue...\033[00m')
        elif option == '6':
            print("The winner is", BordaVoting(profiles), "according to the Borda voting rule.")
            input('\033[96mPress enter to continue...\033[00m')
        elif option == '7':
            n = input('Enter the number of voters(default: 40): ')
            if n == '':
                n = 40
            else:
                n = int(n)
            m = input('Enter the number of candidates(default: 6): ')
            if m == '':
                m = 6
            else:
                m = int(m)
            print('Generating the profile...')
            gen_profiles = allWinner(n, m)
            for profile in gen_profiles: # profile is formatted: 'abcd' -> a>b>c>d
                formatted_profile = ''
                for alternative in profile:
                    formatted_profile += alternative + '>'
                print("\tThere are", gen_profiles[profile], "with profile", formatted_profile[:-1])
            print('The winner is', Plurality(profiles),'.')
            input('\033[96mPress enter to continue...\033[00m')
        elif option == '8':
            n = input('Enter the number of voters(default: 40): ')
            if n == '':
                n = 40
            else:
                n = int(n)
            m = input('Enter the number of candidates(default: 6): ')
            if m == '':
                m = 6
            else:
                m = int(m)
            print('Generating the profile...')
            gen_profiles = eachWinner(n, m)
            for profile in gen_profiles:
                formatted_profile = ''
                for alternative in profile:
                    formatted_profile += alternative + '>'
                print("\tThere are", gen_profiles[profile], "with profile", formatted_profile[:-1])
            print('The winner is', Plurality(gen_profiles),'according to the plurality rule.')
            print('The winner is', PluralityRunoff(gen_profiles),'according to the plurality runoff rule.')
            print('The winner is', CondorcetVoting(gen_profiles),'according to the Condorcet voting rule.')
            print('The winner is', BordaVoting(gen_profiles),'according to the Borda voting rule.')
            input('\033[96mPress enter to continue...\033[00m')
        elif option == '9':
            n = input('Enter the number of voters(default: 40): ')
            if n == '':
                n = 40
            else:
                n = int(n)
            m = input('Enter the number of candidates(default: 6): ')
            if m == '':
                m = 6
            else:
                m = int(m)
            print('Generating the profile...')
            gen_profiles = run_genetic_algorithm(n,m)
            for profile in gen_profiles: # profile is formatted: 'abcd' -> a>b>c>d
                formatted_profile = ''
                for alternative in profile:
                    formatted_profile += alternative + '>'
                print("\tThere are", gen_profiles[profile], "with profile", formatted_profile[:-1])
            print('The winner is', Plurality(gen_profiles),'according to the plurality rule.')
            print('The winner is', PluralityRunoff(gen_profiles),'according to the plurality runoff rule.')
            print('The winner is', CondorcetVoting(gen_profiles),'according to the Condorcet voting rule.')
            print('The winner is', BordaVoting(gen_profiles),'according to the Borda voting rule.')
            input('\033[96mPress enter to continue...\033[00m')
        elif option == '0':
            print('Bye!')
        else:
            print('\033[91mInvalid option!\033[00m')
            input('\033[96mPress enter to continue...\033[00m')


