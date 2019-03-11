def dijkstra(start, goal):
    graph = {'aA': {'aC': 96, 'bA': 72},
             'aC': {'aA': 96, 'aE': 10, 'bC': 72},
             'aE': {'aC': 120, 'bE': 72},
             'aG': {'aI': 120, 'bG': 72},
             'aI': {'aG': 120, 'aK': 96, 'bI': 72},
             'aK': {'aI': 96, 'bK': 72},

             'bA': {'aA': 72, 'bC': 96, 'cA': 60},
             'bC': {'bA': 96, 'aC': 72, 'bD': 60, 'cC': 60},
             'bD': {'bC': 60, 'bE': 60, 'cD': 60},
             'bE': {'bD': 60, 'aE': 72, 'bG': 60},
             'bG': {'bE': 60, 'aG': 72, 'bH': 60},
             'bH': {'bG': 60, 'bI': 60, 'cH': 60},
             'bI': {'bH': 60, 'aI': 72, 'bK': 96, 'cI': 60},
             'bK': {'aK': 72, 'bI': 96, 'cK': 60},

             'cA': {'bA': 60, 'cC': 96},
             'cC': {'cA': 96, 'bC': 60, 'fC': 120},
             'cD': {'bD': 60, 'cE': 60},
             'cE': {'cD': 60, 'dE': 60},
             'cG': {'cH': 60, 'dG': 60},
             'cH': {'cG': 60, 'bH': 60},
             'cI': {'bH': 60, 'cK': 96, 'fI': 120},
             'cK': {'cI': 96, 'bK': 60},

             'dD': {'dE': 60, 'fD': 60},
             'dE': {'dD': 60, 'cE': 60, 'dF': 36},
             'dF': {'dE': 36, 'dG': 24, 'gF': 84},
             'dG': {'dF': 24, 'cG': 60, 'dH': 60},
             'dH': {'dG': 60, 'fH': 60},

             'eE': {'fE': 24},
             'eG': {'fG': 24},

             'fA': {'fC': 96},
             'fC': {'fA': 96, 'cC': 120, 'fD': 60, 'iC': 120},
             'fD': {'fC': 60, 'dD': 60, 'hD': 60},
             'fE': {'eE': 24, 'gE': 24},
             'fG': {'eG': 24, 'gG': 24},
             'fH': {'dH': 60, 'fI': 60, 'hH': 60},
             'fI': {'fH': 60, 'cI': 120, 'fK': 96, 'iI': 120},
             'fK': {'fI': 96},

             'gE': {'fE': 24, 'gF': 36},
             'gF': {'gE': 96, 'dF': 84, 'gG': 24},
             'gG': {'gF': 24, 'fG': 24},

             'hD': {'fD': 60, 'hH': 160, 'iD': 60},
             'hH': {'hD': 160, 'fH': 60, 'iH': 60},

             'iA': {'iC': 96, 'jA': 60},
             'iC': {'iA': 96, 'fC': 120, 'iD': 60, 'jC': 60},
             'iD': {'iC': 60, 'hD': 60, 'iE': 60},
             'iE': {'iD': 60, 'jE': 60},
             'iG': {'iH': 60, 'jG': 60},
             'iH': {'iG': 60, 'iI': 60, 'hH': 60},
             'iI': {'iH': 60, 'fI': 120, 'iK': 96, 'jI': 60},
             'iK': {'iI': 96, 'jK': 60},

             'jA': {'iA': 60, 'jB': 36},
             'jB': {'jA': 36, 'kB': 60},
             'jC': {'iC': 60, 'jD': 60, 'kC': 60},
             'jD': {'jC': 60, 'jE': 60, 'kD': 60},
             'jE': {'jD': 60, 'iE': 60, 'jF': 36},
             'jF': {'jE': 36, 'jG': 24},
             'jG': {'jF': 24, 'iG': 60, 'jH': 60},
             'jH': {'jG': 60, 'kH': 60, 'jI': 60},
             'jI': {'jH': 60, 'iI': 60, 'kI': 60},
             'jJ': {'jK': 36, 'kJ': 60},
             'jK': {'jJ': 36, 'iK': 60},

             'kA': {'kB': 36, 'iA': 60},
             'kB': {'kA': 36, 'jB': 60, 'kC': 60},
             'kC': {'kB': 60, 'jC': 60},
             'kD': {'jD': 60, 'kE': 60},
             'kE': {'kD': 60, 'lE': 60},
             'kG': {'kH': 60, 'lG': 60},
             'kH': {'kG': 60, 'jH': 60},
             'kI': {'jI': 60, 'kJ': 60},
             'kJ': {'kI': 60, 'jJ': 60, 'kK': 36},
             'kK': {'kJ': 36, 'lK': 60},

             'lA': {'kA': 60, 'lE': 228},
             'lE': {'lA': 228, 'kE': 60, 'lG': 60},
             'lG': {'lE': 60,  'kG': 60, 'lK': 228},
             'lK': {'lG': 228, 'kK': 60},
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
    graph = {'aA': {'aC': 96, 'bA': 72},
             'aC': {'aA': 96, 'aE': 10, 'bC': 72},
             'aE': {'aC': 120, 'bE': 72},
             'aG': {'aI': 120, 'bG': 72},
             'aI': {'aG': 120, 'aK': 96, 'bI': 72},
             'aK': {'aI': 96, 'bK': 72},

             'bA': {'aA': 72, 'bC': 96, 'cA': 60},
             'bC': {'bA': 96, 'aC': 72, 'bD': 60, 'cC': 60},
             'bD': {'bC': 60, 'bE': 60, 'cD': 60},
             'bE': {'bD': 60, 'aE': 72, 'bG': 60},
             'bG': {'bE': 60, 'aG': 72, 'bH': 60},
             'bH': {'bG': 60, 'bI': 60, 'cH': 60},
             'bI': {'bH': 60, 'aI': 72, 'bK': 96, 'cI': 60},
             'bK': {'aK': 72, 'bI': 96, 'cK': 60},

             'cA': {'bA': 60, 'cC': 96},
             'cC': {'cA': 96, 'bC': 60, 'fC': 120},
             'cD': {'bD': 60, 'cE': 60},
             'cE': {'cD': 60, 'dE': 60},
             'cG': {'cH': 60, 'dG': 60},
             'cH': {'cG': 60, 'bH': 60},
             'cI': {'bH': 60, 'cK': 96, 'fI': 120},
             'cK': {'cI': 96, 'bK': 60},

             'dD': {'dE': 60, 'fD': 60},
             'dE': {'dD': 60, 'cE': 60, 'dF': 36},
             'dF': {'dE': 36, 'dG': 24, 'gF': 84},
             'dG': {'dF': 24, 'cG': 60, 'dH': 60},
             'dH': {'dG': 60, 'fH': 60},

             'eE': {'fE': 24},
             'eG': {'fG': 24},

             'fA': {'fC': 96},
             'fC': {'fA': 96, 'cC': 120, 'fD': 60, 'iC': 120},
             'fD': {'fC': 60, 'dD': 60, 'hD': 60},
             'fE': {'eE': 24, 'gE': 24},
             'fG': {'eG': 24, 'gG': 24},
             'fH': {'dH': 60, 'fI': 60, 'hH': 60},
             'fI': {'fH': 60, 'cI': 120, 'fK': 96, 'iI': 120},
             'fK': {'fI': 96},

             'gE': {'fE': 24, 'gF': 36},
             'gF': {'gE': 96, 'dF': 84, 'gG': 24},
             'gG': {'gF': 24, 'fG': 24},

             'hD': {'fD': 60, 'hH': 160, 'iD': 60},
             'hH': {'hD': 160, 'fH': 60, 'iH': 60},

             'iA': {'iC': 96, 'jA': 60},
             'iC': {'iA': 96, 'fC': 120, 'iD': 60, 'jC': 60},
             'iD': {'iC': 60, 'hD': 60, 'iE': 60},
             'iE': {'iD': 60, 'jE': 60},
             'iG': {'iH': 60, 'jG': 60},
             'iH': {'iG': 60, 'iI': 60, 'hH': 60},
             'iI': {'iH': 60, 'fI': 120, 'iK': 96, 'jI': 60},
             'iK': {'iI': 96, 'jK': 60},

             'jA': {'iA': 60, 'jB': 36},
             'jB': {'jA': 36, 'kB': 60},
             'jC': {'iC': 60, 'jD': 60, 'kC': 60},
             'jD': {'jC': 60, 'jE': 60, 'kD': 60},
             'jE': {'jD': 60, 'iE': 60, 'jF': 36},
             'jF': {'jE': 36, 'jG': 24},
             'jG': {'jF': 24, 'iG': 60, 'jH': 60},
             'jH': {'jG': 60, 'kH': 60, 'jI': 60},
             'jI': {'jH': 60, 'iI': 60, 'kI': 60},
             'jJ': {'jK': 36, 'kJ': 60},
             'jK': {'jJ': 36, 'iK': 60},

             'kA': {'kB': 36, 'iA': 60},
             'kB': {'kA': 36, 'jB': 60, 'kC': 60},
             'kC': {'kB': 60, 'jC': 60},
             'kD': {'jD': 60, 'kE': 60},
             'kE': {'kD': 60, 'lE': 60},
             'kG': {'kH': 60, 'lG': 60},
             'kH': {'kG': 60, 'jH': 60},
             'kI': {'jI': 60, 'kJ': 60},
             'kJ': {'kI': 60, 'jJ': 60, 'kK': 36},
             'kK': {'kJ': 36, 'lK': 60},

             'lA': {'kA': 60, 'lE': 228},
             'lE': {'lA': 228, 'kE': 60, 'lG': 60},
             'lG': {'lE': 60, 'kG': 60, 'lK': 228},
             'lK': {'lG': 228, 'kK': 60},
             }
    return graph
