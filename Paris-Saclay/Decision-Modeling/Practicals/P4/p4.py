import openpyxl
import math

def excel_to_dict(filename):
    """Converts an Excel file to a dictionary.

    Args:
        filename (str): the name of the Excel file.

    Returns:
        dict: the dictionary corresponding to the Excel file.
            - The keys are the first column of the Excel file.
            - The values are dictionaries:
                - The keys are the column names of the Excel file.
                - The values are the values of the corresponding row.
    """
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    data = {}
    for row in ws.iter_rows(min_row=2):
        data[row[0].value] = {}
        for i in range(1, len(row)): 
            if row[i].value is not None:
                data[row[0].value][ws.cell(row=1, column=i+1).value] = row[i].value
    return data

def invertDict(d):
    """Inverts a dictionary of critiques. That is, the keys are the movies, and the values are dictionaries, where the keys are the persons and the values are the ratings.
    If a person has not rated a movie, we do not add the person to the dictionary.

    Args:
        d (dict): the dictionary to invert.

    Returns:
        dict: the inverted dictionary.
    """
    inverted = {}
    for person in d:
        for movie in d[person]:
            if movie not in inverted:
                inverted[movie] = {}
            inverted[movie][person] = d[person][movie]
    return inverted

def sim_distanceManhattan(person1, person2):
    """Computes the Manhattan distance between two persons.
    
    Args:
        person1 (dict): the first person.
        person2 (dict): the second person.

    Returns:
        float: the Manhattan distance between the two persons.
    """
    distance = 0
    for key in person1:
        if key in person2:
            distance += abs(person1[key] - person2[key])

    return distance

def sim_distanceEuclidean(person1, person2):
    """Computes the Euclidean distance between two persons.
    
    Args:
        person1 (dict): the first person.
        person2 (dict): the second person.

    Returns:
        float: the Euclidean distance between the two persons.
    """
    distance = 0
    for key in person1:
        if key in person2.keys():
            distance += (person1[key] - person2[key])**2

    return distance**0.5

def computeNearestNeighbor(person, critiques, dist="Eucl"):
    """Computes the nearest neighbor of a person.
    
    Args:
        person (dict): the person.
        critiques (dict): the dictionary of critiques.
        dist (str): the distance used to compute the nearest neighbor.

    Returns:
        list: ordered list of the nearest neighbors.
    """
    distances = []
    for critic in critiques:
        if critic != person:
            if dist == "Eucl":
                distances.append((critic, sim_distanceEuclidean(critiques[person], critiques[critic])))
            elif dist == "Manh":
                distances.append((critic, sim_distanceManhattan(critiques[person], critiques[critic])))
    distances.sort(key=lambda x: x[1])
    return distances

def recommendNearestNeighbor(person, critiques, dist="eucl"):
    """Computes the recommendations for a person based on the nearest neighbor.
    
    Args:
        person (dict): the person.
        critiques (dict): the dictionary of critiques.
        dist (str): the distance used to compute the nearest neighbor.

    Returns:
        list: the list of recommendations for the person.
    """
    recommendations = []
    nearest = computeNearestNeighbor(person, critiques, dist)[0][0]
    for movie in critiques[nearest]:
        if movie not in critiques[person]:
            recommendations.append((movie, critiques[nearest][movie]))
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations

def bestRecommend(person, critiques):
    """Computes the best recommendations for a person.
    
    Args:
        person (dict): the person.
        critiques (dict): the dictionary of critiques.

    Returns:
        list: the list of best recommendations for the person.
    """
    # For each movie not seen by the person, compute the weighted average of the ratings of the nearest neighbors.
    # The weight of a neighbor is the 1/(1 + distance to the person).
    # The rating of a neighbor is the rating of the movie by the neighbor.
    recommendations = []
    inverted = invertDict(critiques)
    for movie in inverted:
        if movie not in critiques[person]:
            total = 0
            s = 0
            for critic in inverted[movie]:
                total += inverted[movie][critic] / (1 + sim_distanceManhattan(critiques[person], critiques[critic]))
                s += 1 / (1 + sim_distanceManhattan(critiques[person], critiques[critic]))

            recommendations.append((movie, total / s))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations

def bestRecommentWithExp(person, critiques):
    """Computes the best recommendations for a person.
    
    Args:
        person (dict): the person.
        critiques (dict): the dictionary of critiques.

    Returns:
        list: the list of best recommendations for the person.
    """
    # For each movie not seen by the person, compute the weighted average of the ratings of the nearest neighbors.
    # The weight of a neighbor is the exp(-distance to the person).
    # The rating of a neighbor is the rating of the movie by the neighbor.
    recommendations = []
    inverted = invertDict(critiques)
    for movie in inverted:
        if movie not in critiques[person]:
            total = 0
            s = 0
            for critic in inverted[movie]:
                total += inverted[movie][critic] * math.exp(-sim_distanceManhattan(critiques[person], critiques[critic]))
                s += math.exp(-sim_distanceManhattan(critiques[person], critiques[critic]))

            recommendations.append((movie, total / s))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations

def pearson(person1, person2):
    """Computes the Pearson correlation coefficient between two persons.

    Args:
        person1 (dict): the first person.
        person2 (dict): the second person.

    Returns:
        float: the Pearson correlation coefficient between the two persons.
    """
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0

    n = 0
    for key in person1:
        if key in person2:
            n += 1
            x = person1[key]
            y = person2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += x**2
            sum_y2 += y**2

    denominator = math.sqrt(sum_x2 - (sum_x**2) / n) * math.sqrt(sum_y2 - (sum_y**2) / n)

    if denominator == 0:
        return 0

    return (sum_xy - (sum_x * sum_y) / n) / denominator

def pearsonRecommend(person, critiques):
    """Computes the recommendations for a person based on the Pearson correlation coefficient.
    
    Args:
        person (dict): the person.
        critiques (dict): the dictionary of critiques.

    Returns:
        list: the list of recommendations for the person.
    """
    closest = []
    for critic in critiques:
        if critic != person:
            closest.append((critic, pearson(critiques[person], critiques[critic])))
    closest.sort(key=lambda x: x[1], reverse=True)
    closest = closest[0]

    recommendations = []
    for movie in critiques[closest[0]]:
        if movie not in critiques[person]:
            recommendations.append((movie, critiques[closest[0]][movie]))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations, closest[0]
    
def cosineCorrelation(person1, person2):
    """ Computes the cosine correlation coefficient between two persons

    Args:
        person1 (dict): the first person
        person2 (dict): the second person

    Returns:
        float: the cosine correlation coefficient between two persons
    """
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0

    for key in person1:
        if key in person2:
            x = person1[key]
            y = person2[key]
            sum_xy += x * y
            sum_x2 += x**x
            sum_y2 += y**y
    
    denominator = math.sqrt(sum_x2) * math.sqrt(sum_y2)

    if denominator == 0:
        return 0

    return sum_xy / denominator

def cosineRecommend(person, critiques):
    """Computes the recommendations for a person based on the cosine correlation coefficient.
    
    Args:
        person (dict): the person.
        critiques (dict): the dictionary of critiques.

    Returns:
        list: the list of recommendations for the person.
    """
    closest = []
    for critic in critiques:
        if critic != person:
            closest.append((critic, cosineCorrelation(critiques[person], critiques[critic])))
    closest.sort(key=lambda x: x[1], reverse=True)
    closest = closest[0]

    recommendations = []
    for movie in critiques[closest[0]]:
        if movie not in critiques[person]:
            recommendations.append((movie, critiques[closest[0]][movie]))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations, closest[0]

if __name__ == "__main__":
    filename = "data.xlsx"

    # Exercise 1: Convert the Excel file to a dictionary.
    print("\033[93mReading Excel file...")
    critiques = excel_to_dict(filename)
    print("Done.\033[0m")
    print(critiques["Lisa Rose"])

    # Exercise 2: Find similar persons and compute recommendations.
    # a) Compute the Manhattan and Euclidean distances between Lisa Rose and Gene Seymour.
    print("\033[93mComputing Manhattan distance...\033[0m")
    print(sim_distanceManhattan(critiques["Lisa Rose"], critiques["Gene Seymour"]))
    print("\033[93mComputing Euclidean distance...\033[0m")
    print(sim_distanceEuclidean(critiques["Lisa Rose"], critiques["Gene Seymour"]))

    # b) Get recommendations based on nearest neighbors using Manhattan distance.
    print("\033[93mComputing nearest neighbors...\033[0m")
    print("For Lisa Rose:")
    print(computeNearestNeighbor("Lisa Rose", critiques, "Manh"))
    print("For Toby:")
    print(computeNearestNeighbor("Toby", critiques, "Manh"))
    print("\033[93mComputing recommendations...\033[0m")
    print("For Lisa Rose:")
    print(recommendNearestNeighbor("Lisa Rose", critiques, "Manh"))
    print("For Toby:")
    print(recommendNearestNeighbor("Toby", critiques, "Manh"))

    # c) 
    #   i) Rank the critics and recommend the best movies by using the weighted average of the ratings.
    print("\033[93mComputing best recommendations...\033[0m")
    print("For Anne:")
    print(bestRecommend("Anne", critiques))

    #   ii) Rank the critics and recommend the best movies by using the weighted average of the ratings and the exponential function.
    print("\033[93mComputing best recommendations with exponential function...\033[0m")
    print("For Anne:")
    print(bestRecommentWithExp("Anne", critiques))

    # d) Use the Pearson correlation coefficient to get recommendations
    print("\033[93mComputing Pearson recommendations...\033[0m")
    print("For Anne:")
    print(pearsonRecommend("Anne", critiques))

    # e) Use the cosine correlation coefficient to get recommendations
    print("\033[93mComputing cosine recommendations...\033[0m")
    print("For Anne:")
    print(cosineRecommend("Anne", critiques))

    # Exercise 3: Use the other dataset. data1.xlsx
    print("\033[93mReading Excel file...")
    critiques1 = excel_to_dict("data1.xlsx")
    print("Done.\033[0m")
    print(critiques1["Veronica"])

    # Get all different recommendations for Veronica and Hailey
    print("\033[93mComputing recommendations...\033[0m")
    print("For Veronica:")
    print("\tNearest neighbor:")
    print("\t\t"+recommendNearestNeighbor("Veronica", critiques1))
    print("\tBest:")
    print("\t\t"+bestRecommend("Veronica", critiques1))
    print("\tBest with exponential function:")  
    print("\t\t"+bestRecommentWithExp("Veronica", critiques1))
    print("\tPearson:")
    print("\t\t"+pearsonRecommend("Veronica", critiques1))
    print("\tCosine:")
    print("\t\t"+cosineRecommend("Veronica", critiques1))








