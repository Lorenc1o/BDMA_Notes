import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def read_xls(file):
    """
    Read a xls file and return a numpy array
    """
    return np.array(pd.read_excel(file, header=None))

def read_csv(file):
    """
    Read a csv file and return a numpy array
    """
    return np.array(pd.read_csv(file))

def VisualizeBinaryRelation(matrix):
    """
    Visualize a binary relation as a graph
    Name the nodes with letters starting from A
    """
    # Create a graph
    G = nx.DiGraph()

    # Add nodes
    m = matrix.shape[0]
    for i in range(m):
        G.add_node(chr(ord('A') + i))

    # Add edges
    for i in range(m):
        for j in range(m):
            if matrix[i, j] == 1:
                G.add_edge(chr(ord('A') + i), chr(ord('A') + j))

    # Visualize the graph
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=800, edge_color='black')
    plt.show()

def CompleteCheck(matrix):
    """
    Check if the binary relation is complete
    """
    m = matrix.shape[0]
    for i in range(m):
        for j in range(m):
            if matrix[i, j] == 0 and matrix[j, i] == 0:
                return False
    return True

def ReflexiveCheck(matrix):
    """
    Check if the binary relation is reflexive
    """
    m = matrix.shape[0]
    for i in range(m):
        if matrix[i, i] == 0:
            return False
    return True

def AssymetricCheck(matrix):
    """
    Check if the binary relation is assymetric
    """
    m = matrix.shape[0]
    for i in range(m):
        for j in range(m):
            if matrix[i, j] == 1 and matrix[j, i] == 1:
                return False
    return True

def SymmetricCheck(matrix):
    """
    Check if the binary relation is symmetric
    """
    m = matrix.shape[0]
    for i in range(m):
        for j in range(m):
            if matrix[i, j] != matrix[j, i]:
                return False
    return True

def AntisymmetricCheck(matrix):
    """
    Check if the binary relation is antisymmetric
    """
    m = matrix.shape[0]
    for i in range(m):
        for j in range(m):
            if matrix[i, j] == 1 and matrix[j, i] == 1 and i != j:
                return False
    return True

def TransitiveCheck(matrix):
    """
    Check if the binary relation is transitive
    """
    m = matrix.shape[0]
    for i in range(m):
        for j in range(m):
            if matrix[i, j] == 1:
                for k in range(m):
                    if matrix[j, k] == 1 and matrix[i, k] == 0:
                        return False
    return True

def NegativetransitiveCheck(matrix):
    """
    Check if the binary relation is negative transitive
    """
    m = matrix.shape[0]
    for i in range(m):
        for j in range(m):
            if matrix[i, j] == 0:
                for k in range(m):
                    if matrix[j, k] == 0 and matrix[i, k] == 1:
                        return False
    return True

def CompleteOrderCheck(matrix):
    """
    Check if the binary relation is a complete order: complete, antisymmetric and transitive
    """
    return CompleteCheck(matrix) and AntisymmetricCheck(matrix) and TransitiveCheck(matrix)

def CompletePreOrderCheck(matrix):
    """
    Check if the binary relation is a complete preorder: complete and transitive
    """
    return CompleteCheck(matrix) and TransitiveCheck(matrix)

def StrictRelation(matrix):
    """
    Returns the asymmetric part of the binary relation
    """
    m = matrix.shape[0]
    ret = np.zeros([m, m])
    for i in range(m):
        for j in range(m):
            if matrix[i, j] == 1 and matrix[j, i] == 0:
                ret[i, j] = 1
    return ret

def IndifferenceRelation(matrix):
    """
    Returns the symmetric part of the binary relation
    """
    m = matrix.shape[0]
    ret = np.zeros(matrix.shape)
    for i in range(m):
        for j in range(m):
            if matrix[i, j] == 1 and matrix[j, i] == 1:
                ret[i, j] = 1
    return ret

def dfs_cycle_check(matrix, node, visited, visiting):
    """
    Check if there is a cycle starting from the given node
    """
    visiting.add(node)
    for neighbor, isConnected in enumerate(matrix[node]):
        if isConnected:
            if neighbor in visiting:
                return True  # Cycle found
            if neighbor not in visited:
                if dfs_cycle_check(matrix, neighbor, visited, visiting):
                    return True  # Cycle found
    visiting.remove(node)
    visited.add(node)
    return False  # No cycle found from this node

def has_cycle(matrix):
    """
    Check if the binary relation has a cycle
    """
    matrix = np.array(matrix)  # Convert to numpy array for easier indexing
    n = len(matrix)
    visited = set()
    for node in range(n):
        if node not in visited:
            visiting = set()
            if dfs_cycle_check(matrix, node, visited, visiting):
                return True  # Cycle found
    return False  # No cycle found

def Topologicalsorting(matrix):
    """
    Returns the topological sorting of the binary relation
    """
    if has_cycle(matrix):
        return None
    
    m = matrix.shape[0]
    ret = np.zeros(m)

    # Find the indegree of each node
    indegree = np.zeros(m)
    for i in range(m):
        for j in range(m):
            if matrix[i, j] == 1:
                indegree[j] += 1

    # Find the nodes with indegree 0
    queue = []
    for i in range(m):
        if indegree[i] == 0:
            queue.append(i)

    # Topological sorting
    cnt = 0 # The number of nodes that have been visited
    while queue:
        node = queue.pop(0) # Pop the first node
        ret[cnt] = node
        cnt += 1
        for i in range(m): # Update the indegree of the neighbors
            if matrix[node, i] == 1:
                indegree[i] -= 1
                if indegree[i] == 0: # If the indegree of a neighbor becomes 0, add it to the queue
                    queue.append(i)

    return ret

def TopologicalToMatrix(topo):
    """
    Convert a topological sorting to a binary relation
    """
    m = topo.shape[0]
    ret = np.zeros([m, m])
    for i in range(m):
        for j in range(i + 1, m):
            ret[int(topo[i]), int(topo[j])] = 1
    return ret

def VisualizeTopologicalSorting(matrix):
    """
    Show the topological sorting as a graph
    """
    topo = Topologicalsorting(matrix)
    if topo is None:
        print("The binary relation has a cycle, so we cannot find the topological sorting")
    else:
        VisualizeBinaryRelation(TopologicalToMatrix(topo))

def VisualizeTopologicalSorting_linear(matrix):
    """
    Show the topological sorting as a graph, but with a linear layout
    """
    topo = Topologicalsorting(matrix)
    if topo is None:
        print("The binary relation has a cycle, so we cannot find the topological sorting")
    else:
        # Create a graph
        G = nx.DiGraph()

        # Add nodes
        m = matrix.shape[0]
        for i in range(m):
            G.add_node(chr(ord('A') + i))

        # Add edges
        for i in range(m-1):
            G.add_edge(chr(ord('A') + i), chr(ord('A') + i + 1))

        # Visualize the graph
        nx.draw(G, with_labels=True, node_color='skyblue', node_size=800, edge_color='black', pos=nx.shell_layout(G))
        plt.show()


if __name__ == '__main__':
    # Ask the user to input the file name
    file = input("Please enter the file name (default: data.xlsx): ")

    if file == "":
        file = "data.xlsx"

    # Read the file
    try:
        if file.endswith('.xls') or file.endswith('.xlsx'):
            matrix = read_xls(file)
        elif file.endswith('.csv'):
            matrix = read_csv(file)
        else:
            print("The file format is not supported")
            exit()
    except:
        print("The file does not exist")
        exit()

    while True:
        action = input(f"\033[31mPlease choose an action:\n1. Visualize the binary relation\n2. Check if the binary relation is complete\n3. Check if the binary relation is reflexive\n4. Check if the binary relation is assymetric\n5. Check if the binary relation is symmetric\n6. Check if the binary relation is antisymmetric\n7. Check if the binary relation is transitive\n8. Check if the binary relation is negative transitive\n9. Check if the binary relation is a complete order\n10. Check if the binary relation is a complete preorder\n11. Show the strict relation\n12. Show the indifference relation\n13. Show the topological sorting\n14. Read another file\n0. Exit\n\033[0m")
        
        try:
            if int(action) > 0 and int(action) < 15:
                print(f"\033[34mExecuting action " + action + " ..." + "\033[0m")
                if action == '1':
                    # Visualize the binary relation
                    VisualizeBinaryRelation(matrix)
                elif action == '2':
                    # Check if the binary relation is complete
                    if CompleteCheck(matrix):
                        print("The binary relation is complete")
                    else:
                        print("The binary relation is not complete")
                elif action == '3':
                    # Check if the binary relation is reflexive
                    if ReflexiveCheck(matrix):
                        print("The binary relation is reflexive")
                    else:
                        print("The binary relation is not reflexive")
                elif action == '4':
                    # Check if the binary relation is assymetric
                    if AssymetricCheck(matrix):
                        print("The binary relation is assymetric")
                    else:
                        print("The binary relation is not assymetric")
                elif action == '5':
                    # Check if the binary relation is symmetric
                    if SymmetricCheck(matrix):
                        print("The binary relation is symmetric")
                    else:
                        print("The binary relation is not symmetric")
                elif action == '6':
                    # Check if the binary relation is antisymmetric
                    if AntisymmetricCheck(matrix):
                        print("The binary relation is antisymmetric")
                    else:
                        print("The binary relation is not antisymmetric")
                elif action == '7':    
                    # Check if the binary relation is transitive
                    if TransitiveCheck(matrix):
                        print("The binary relation is transitive")
                    else:
                        print("The binary relation is not transitive")
                elif action == '8':
                    # Check if the binary relation is negative transitive
                    if NegativetransitiveCheck(matrix):
                        print("The binary relation is negative transitive")
                    else:
                        print("The binary relation is not negative transitive")
                elif action == '9':
                    # Check if the binary relation is a complete order
                    if CompleteOrderCheck(matrix):
                        print("The binary relation is a complete order")
                    else:
                        print("The binary relation is not a complete order")
                elif action == '10':
                    # Check if the binary relation is a complete preorder
                    if CompletePreOrderCheck(matrix):
                        print("The binary relation is a complete preorder")
                    else:
                        print("The binary relation is not a complete preorder")
                elif action == '11':
                    # Print the strict relation
                    print("The strict relation is: ")
                    print(StrictRelation(matrix))

                    # Show the strict relation
                    VisualizeBinaryRelation(StrictRelation(matrix))
                elif action == '12':

                    # Print the indifference relation
                    print("The indifference relation is: ")
                    print(IndifferenceRelation(matrix))

                    # Show the indifference relation
                    VisualizeBinaryRelation(IndifferenceRelation(matrix))
                elif action == '13':

                    # Print the topological sorting
                    topo = Topologicalsorting(matrix)

                    if topo is None:
                        print("The binary relation has a cycle, so we cannot find the topological sorting")
                    else:
                        print("The topological sorting is: ")
                        print(topo)

                        # Show the topological sorting
                        VisualizeBinaryRelation(TopologicalToMatrix(topo))

                        # Show the topological sorting with a linear layout
                        VisualizeTopologicalSorting_linear(matrix)
                elif action == '14':
                    # Read another file
                    file = input("\033[33mPlease enter the file name (default: data.xlsx): \033[0m")

                    if file == "":
                        file = "data.xlsx"
                    try:
                        # Read the file
                        if file.endswith('.xls') or file.endswith('.xlsx'):
                            matrix2 = read_xls(file)
                            matrix = matrix2
                        elif file.endswith('.csv'):
                            matrix2 = read_csv(file)
                            matrix = matrix2
                        else:
                            print("\033[33mThe file format is not supported, keeping previous matrix\033[0m")
                    except:
                        print("\033[33mThe file does not exist, keeping previous matrix\033[0m")

                else:
                    print("Invalid action")
                    continue
                
                print("\033[34mAction " + action + " executed successfully\033[0m")
                input("\033[35mPress enter to continue...\033[0m")
            elif int(action) == 0:
                # Exit
                print("\033[31mExiting...\033[0m")
                break
        except:
            print("\033[33mInvalid action, please enter a number between 0 and 14\033[0m")
            input("\033[35mPress enter to continue...\033[0m")
            continue