def dijkstra(start, goal):
    graph = {'aA': {'aC': 8, 'bA': 6},
             'aC': {'aA': 8, 'aE': 10, 'bC': 6},
             'aE': {'aC': 10, 'bE': 6},
             'aG': {'aI': 10, 'bG': 6},
             'aI': {'aG': 10, 'aK': 8, 'bI': 6},
             'aK': {'aI': 8, 'bK': 6},

             'bA': {'aA': 6, 'bC': 8, 'cA': 5},
             'bC': {'bA': 8, 'aC': 6, 'bD': 5, 'cC': 5},
             'bD': {'bC': 5, 'bE': 5, 'cD': 5},
             'bE': {'bD': 5, 'aE': 6, 'bG': 5},
             'bG': {'bE': 5, 'aG': 6, 'bH': 5},
             'bH': {'bG': 5, 'bI': 5, 'cH': 5},
             'bI': {'bH': 5, 'aI': 6, 'bK': 8, 'cI': 5},
             'bK': {'aK': 6, 'bI': 8, 'cK': 5},

             'cA': {'bA': 5, 'cC': 8},
             'cC': {'cA': 8, 'bC': 5, 'fC': 10},
             'cD': {'bD': 5, 'cE': 5},
             'cE': {'cD': 5, 'dE': 5},
             'cG': {'cH': 5, 'dG': 5},
             'cH': {'cG': 5, 'bH': 5},
             'cI': {'bH': 5, 'cK': 8, 'fI': 10},
             'cK': {'cI': 8, 'bK': 5},

             'dD': {'dE': 5, 'fD': 5},
             'dE': {'dD': 5, 'cE': 5, 'dF': 3},
             'dF': {'dE': 3, 'dG': 2, 'gF': 7},
             'dG': {'dF': 2, 'cG': 5, 'dH': 5},
             'dH': {'dG': 5, 'fH': 5},

             'eE': {'fE': 2},
             'eG': {'fG': 2},

             'fA': {'fC': 8},
             'fC': {'fA': 8, 'cC': 10, 'fD': 5, 'iC': 10},
             'fD': {'fC': 5, 'dD': 5, 'hD': 5},
             'fE': {'eE': 2, 'gE': 2},
             'fG': {'eG': 2, 'gG': 2},
             'fH': {'dH': 5, 'fI': 5, 'hH': 5},
             'fI': {'fH': 5, 'cI': 10, 'fK': 8, 'iI': 10},
             'fK': {'fI': 8},

             'gE': {'fE': 2, 'gF': 3},
             'gF': {'gE': 3, 'dF': 7, 'gG': 2},
             'gG': {'gF': 2, 'fG': 2},

             'hD': {'fD': 5, 'hH': 15, 'iD': 5},
             'hH': {'hD': 15, 'fH': 5, 'iH': 5},

             'iA': {'iC': 8, 'jA': 5},
             'iC': {'iA': 8, 'fC': 10, 'iD': 5, 'jC': 5},
             'iD': {'iC': 5, 'hD': 5, 'iE': 5},
             'iE': {'iD': 5, 'jE': 5},
             'iG': {'iH': 5, 'jG': 5},
             'iH': {'iG': 5, 'iI': 5, 'hH': 5},
             'iI': {'iH': 5, 'fI': 10, 'iK': 8, 'jI': 5},
             'iK': {'iI': 8, 'jK': 5},

             'jA': {'iA': 5, 'jB': 3},
             'jB': {'jA': 3, 'kB': 5},
             'jC': {'iC': 5, 'jD': 5, 'kC': 5},
             'jD': {'jC': 5, 'jE': 5, 'kD': 5},
             'jE': {'jD': 5, 'iE': 5, 'jF': 3},
             'jF': {'jE': 3, 'jG': 2},
             'jG': {'jF': 2, 'iG': 5, 'jH': 5},
             'jH': {'jG': 5, 'kH': 5, 'jI': 5},
             'jI': {'jH': 5, 'iI': 5, 'kI': 5},
             'jJ': {'jK': 3, 'kJ': 5},
             'jK': {'jJ': 3, 'iK': 5},

             'kA': {'kB': 3, 'iA': 5},
             'kB': {'kA': 3, 'jB': 5, 'kC': 5},
             'kC': {'kB': 5, 'jC': 5},
             'kD': {'jD': 5, 'kE': 5},
             'kE': {'kD': 5, 'lE': 5},
             'kG': {'kH': 5, 'lG': 5},
             'kH': {'kG': 5, 'jH': 5},
             'kI': {'jI': 5, 'kJ': 5},
             'kJ': {'kI': 5, 'jJ': 5, 'kK': 3},
             'kK': {'kJ': 3, 'lK': 5},

             'lA': {'kA': 5, 'lE': 19},
             'lE': {'lA': 19, 'kE': 5, 'lG': 5},
             'lG': {'lE': 5,  'kG': 5, 'lK': 19},
             'lK': {'lG': 19, 'kK': 5},
             }

    shortest_distance = {}
    predecessors = {}
    unseen_nodes = graph

    infinity = 9999999
    path = []

    for node in unseen_nodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0

    while unseen_nodes:
        min_node = None
        for node in unseen_nodes:
            if min_node is None:
                min_node = node
            elif shortest_distance[node] < shortest_distance[min_node]:
                min_node = node

        for child_node, weight in graph[min_node].items():
            if weight + shortest_distance[min_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = weight + shortest_distance[min_node]
                predecessors[child_node] = min_node
        unseen_nodes.pop(min_node)

    current_node = goal
    while current_node != start:
        try:
            path.insert(0, current_node)
            current_node = predecessors[current_node]
        except KeyError:
            print('Path not reachable')
            break

    path.insert(0, start)
    if shortest_distance[goal] != infinity:
        return path


def get_graph():
    graph = {'aA': {'aC': 8, 'bA': 6},
             'aC': {'aA': 8, 'aE': 10, 'bC': 6},
             'aE': {'aC': 10, 'bE': 6},
             'aG': {'aI': 10, 'bG': 6},
             'aI': {'aG': 10, 'aK': 8, 'bI': 6},
             'aK': {'aI': 8, 'bK': 6},

             'bA': {'aA': 6, 'bC': 8, 'cA': 5},
             'bC': {'bA': 8, 'aC': 6, 'bD': 5, 'cC': 5},
             'bD': {'bC': 5, 'bE': 5, 'cD': 5},
             'bE': {'bD': 5, 'aE': 6, 'bG': 5},
             'bG': {'bE': 5, 'aG': 6, 'bH': 5},
             'bH': {'bG': 5, 'bI': 5, 'cH': 5},
             'bI': {'bH': 5, 'aI': 6, 'bK': 8, 'cI': 5},
             'bK': {'aK': 6, 'bI': 8, 'cK': 5},

             'cA': {'bA': 5, 'cC': 8},
             'cC': {'cA': 8, 'bC': 5, 'fC': 10},
             'cD': {'bD': 5, 'cE': 5},
             'cE': {'cD': 5, 'dE': 5},
             'cG': {'cH': 5, 'dG': 5},
             'cH': {'cG': 5, 'bH': 5},
             'cI': {'bH': 5, 'cK': 8, 'fI': 10},
             'cK': {'cI': 8, 'bK': 5},

             'dD': {'dE': 5, 'fD': 5},
             'dE': {'dD': 5, 'cE': 5, 'dF': 3},
             'dF': {'dE': 3, 'dG': 2, 'gF': 7},
             'dG': {'dF': 2, 'cG': 5, 'dH': 5},
             'dH': {'dG': 5, 'fH': 5},

             'eE': {'fE': 2},
             'eG': {'fG': 2},

             'fA': {'fC': 8},
             'fC': {'fA': 8, 'cC': 10, 'fD': 5, 'iC': 10},
             'fD': {'fC': 5, 'dD': 5, 'hD': 5},
             'fE': {'eE': 2, 'gE': 2},
             'fG': {'eG': 2, 'gG': 2},
             'fH': {'dH': 5, 'fI': 5, 'hH': 5},
             'fI': {'fH': 5, 'cI': 10, 'fK': 8, 'iI': 10},
             'fK': {'fI': 8},

             'gE': {'fE': 2, 'gF': 3},
             'gF': {'gE': 3, 'dF': 7, 'gG': 2},
             'gG': {'gF': 2, 'fG': 2},

             'hD': {'fD': 5, 'hH': 15, 'iD': 5},
             'hH': {'hD': 15, 'fH': 5, 'iH': 5},

             'iA': {'iC': 8, 'jA': 5},
             'iC': {'iA': 8, 'fC': 10, 'iD': 5, 'jC': 5},
             'iD': {'iC': 5, 'hD': 5, 'iE': 5},
             'iE': {'iD': 5, 'jE': 5},
             'iG': {'iH': 5, 'jG': 5},
             'iH': {'iG': 5, 'iI': 5, 'hH': 5},
             'iI': {'iH': 5, 'fI': 10, 'iK': 8, 'jI': 5},
             'iK': {'iI': 8, 'jK': 5},

             'jA': {'iA': 5, 'jB': 3},
             'jB': {'jA': 3, 'kB': 5},
             'jC': {'iC': 5, 'jD': 5, 'kC': 5},
             'jD': {'jC': 5, 'jE': 5, 'kD': 5},
             'jE': {'jD': 5, 'iE': 5, 'jF': 3},
             'jF': {'jE': 3, 'jG': 2},
             'jG': {'jF': 2, 'iG': 5, 'jH': 5},
             'jH': {'jG': 5, 'kH': 5, 'jI': 5},
             'jI': {'jH': 5, 'iI': 5, 'kI': 5},
             'jJ': {'jK': 3, 'kJ': 5},
             'jK': {'jJ': 3, 'iK': 5},

             'kA': {'kB': 3, 'iA': 5},
             'kB': {'kA': 3, 'jB': 5, 'kC': 5},
             'kC': {'kB': 5, 'jC': 5},
             'kD': {'jD': 5, 'kE': 5},
             'kE': {'kD': 5, 'lE': 5},
             'kG': {'kH': 5, 'lG': 5},
             'kH': {'kG': 5, 'jH': 5},
             'kI': {'jI': 5, 'kJ': 5},
             'kJ': {'kI': 5, 'jJ': 5, 'kK': 3},
             'kK': {'kJ': 3, 'lK': 5},

             'lA': {'kA': 5, 'lE': 19},
             'lE': {'lA': 19, 'kE': 5, 'lG': 5},
             'lG': {'lE': 5, 'kG': 5, 'lK': 19},
             'lK': {'lG': 19, 'kK': 5},
             }
    return graph
