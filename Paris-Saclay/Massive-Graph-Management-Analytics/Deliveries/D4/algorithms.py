import networkx as nx
import matplotlib.pyplot as plt

def show_matrix_from_dict(matrix_dict, size, name):
    matrix = [[0 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            matrix[i][j] = matrix_dict[i][j]
    
    print(name)
    for row in matrix:
        print(row)


def palla_algorithm(graph, k, verbose=False):
    # 1. Find all maximal cliques in G
    cliques = list(nx.find_cliques(graph))
    if verbose:
        print("Cliques:")
        print(cliques)
    # 2. Sort cliques by size
    cliques.sort(key=lambda clique: len(clique), reverse=True)
    cliques = [(i, clique) for i, clique in enumerate(cliques)]

    # 4. Create clique overlap matrix
    clique_overlap_matrix = {}
    for (i, clique) in cliques:
        clique_overlap_matrix[i] = {}
        for (j, other_clique) in cliques:
            if clique != other_clique:
                clique_overlap_matrix[i][j] = len(set(clique).intersection(set(other_clique)))
            else:
                clique_overlap_matrix[i][j] = len(clique)

    if verbose:
        show_matrix_from_dict(clique_overlap_matrix, len(cliques), "Clique overlap matrix")

    # 5. Compute clique connectivity matrix: C[i][j] = 1 if clique_overlap_matrix[i][j] >= k-1, 0 otherwise
    clique_connectivity_matrix = {}
    for (i, clique) in cliques:
        clique_connectivity_matrix[i] = {}
        for (j, other_clique) in cliques:
            if clique_overlap_matrix[i][j] >= k-1:
                clique_connectivity_matrix[i][j] = 1
            else:
                clique_connectivity_matrix[i][j] = 0

    if verbose:
        show_matrix_from_dict(clique_connectivity_matrix, len(cliques), "Clique connectivity matrix")

    # 7. Compute communities: merge cliques that are connected
    clique_communities = {i: set(clique) for (i, clique) in cliques}
    for (i, clique) in cliques:
        for (j, other_clique) in cliques:
            if clique_connectivity_matrix[i][j] == 1:
                clique_communities[i] = clique_communities[i].union(clique_communities[j])
                clique_communities[j] = clique_communities[i]

    # 8. Remove duplicate communities
    clique_communities = list(set([tuple(community) for community in clique_communities.values()]))
    communities = []

    # 9. Return communities as list of sets
    for community in clique_communities:
        communities.append(set(community))

    return communities

def show_graph(graph):
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()

def show_communities(graph, communities):
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'cyan']
    color_map = {}
    for i, community in enumerate(communities):
        for node in community:
            color_map[node] = colors[i]
    
    nx.draw(graph, node_color=[color_map[node] for node in graph.nodes()], with_labels=True, font_weight='bold')
    plt.show()

if __name__ == '__main__':
    #graph = nx.Graph()
    # Example 1: 1 community of size 4
    #graph.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (3, 4)])
    #print(palla_algorithm(graph, 3))
    #show_graph(graph)
    #show_communities(graph, palla_algorithm(graph, 3))

    # Example 2: 2 communities of size 4
    #graph.add_edges_from([(4, 5),(5, 6), (5, 7), (5, 8), (6, 7), (7, 8)])
    #print(palla_algorithm(graph, 3))
    #show_graph(graph)
    #show_communities(graph, palla_algorithm(graph, 3))

    # Example 3: from the slides
    graph2 = nx.Graph()
    graph2.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5), (5, 6), (4, 6), (6, 7), (6, 8), (6, 9), (6, 10), (7, 8), (7, 9), (8, 9), (8, 10), (9, 10)])
    show_graph(graph2)
    print(palla_algorithm(graph2, 4))
    show_communities(graph2, palla_algorithm(graph2, 3))

    # Example 4: from the slides
    graph3 = nx.Graph()
    graph3.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (2, 9), (2, 10), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (4, 7), (4, 9), (4, 8), (5, 6), (5, 7), (5, 9), (6, 7), (6, 9), (7, 9), (7, 8), (8, 9), (9, 10)])
    show_graph(graph3)
    communities = palla_algorithm(graph3, 3)
    print(communities)
    show_communities(graph3, communities)