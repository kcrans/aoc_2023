from collections import defaultdict
from heapq import *

# Store the graph in a dict of dicts
# Note that the graph is unweighted, but we will add weights
# during this algorithim when merging vertices
# Dicts and sets will allow O(1) lookups for specific vertices,
# which is useful with this algorithim

graph = defaultdict(lambda: defaultdict(int))
with open('day25.txt', 'r') as file:
    for line in file:
        source, connections_str = line.strip('\n').split(': ')
        for connection in connections_str.split(' '):
            graph[source][connection] = -1 # We use negatives because we will use a min-heap
            graph[connection][source] = -1
n = len(graph.keys())
# Let's implement the Stoer-Wagner algorithm, as we are basically looking for a min-cut
# It works by taking vertices s and t from the graph. Either they are on the same side
# in the global min-cut or they are separated. For the case where they share a side,
# we can make a recursive call but with s and t "merged" together. I.e. the new vertice
# st will have all the same edges as the union of s and t. This wont affect the calculation
# of min-cut because the edges going between the two groups wont change. The case where they 
# are on separate sides is equivalent to finiding a minimal s-t cut of the graph. We use a
# maximum adjacency search to determine a minimal s-t cut for arbitray s and t.
# This will take n - 1 iterations as for a given s, there are n - 1 other vertices
# which can take the place as a 't'. Each phase of calling 'min_cut_phases'
# will give us a s-t mincut for a different t (they are unique because the t is merged
# into the graph after each iteration, so the next iteration will have to use a different t)

def min_cut_phase(graph, first_vertex, merged_vertices):
    """
    Find a new s-t cut for G. Records the value of the cut.
    Then, it merges s and t together and returns the new graph.
    This is equivalent to moving on to the next possibility where
    s and t share the same side of the cut.
    """
    # Store in a heap the remaining vertices using the number of connections
    # to the subgraph A as the heap metric.
    C = [[connections[first_vertex], vertex] for vertex, connections in graph.items() if vertex != first_vertex]
    heapify(C)
    new_vertex = first_vertex

    # Find a s-t min cut for G. Works by greedily merging the vertex with the largest
    # number of connections to our current combo vertex(based off s).  
    for _ in range(len(graph) - 2):
#        print(C)
        new_vertex = heappop(C)[1]
        for weight_and_vertex in C:
            weight_and_vertex[0] += graph[weight_and_vertex[1]][new_vertex]
        heapify(C)    # Now we have A and two other vertices not merged into it
    # The s, t min cut is the final cut when we add the next vertice and at the end we will merge 
    # these two vertices together in the original graph
    s = new_vertex
    s_connections = graph[s]
    cut, t = heappop(C)
    t_connections = graph.pop(t)
    del s_connections[t]
    del t_connections[s]
    for connection, weight in t_connections.items():
        if weight < 0:
#            print(s_connections, graph[connection])
#            print(s, t, connection)
            s_connections[connection] += weight
            graph[connection][s] += graph[connection].pop(t)
    
    cut_group_size = merged_vertices[t]

    if t in merged_vertices:
        merged_vertices[s] += merged_vertices.pop(t)
    else:
        merged_vertices[s] += 1
    return (abs(cut), cut_group_size)


def min_cut(graph, first_vertex):
    """
    Takes in an undirected, non-weighted graph and returns
    a list of the edges to remove in order to get a min-cut
    """
    current_cut = len(graph[first_vertex])
    cut_group_size = len(graph) - 1
    merged_vertices = {vertex: 1 for vertex in graph.keys()}
    while len(graph) > 1:
        print(len(graph))
        new_cut, new_group_size = min_cut_phase(graph, first_vertex, merged_vertices)
        if new_cut < current_cut:
            current_cut = new_cut
            cut_group_size = new_group_size
            if current_cut == 3:
                break
    return (cut_group_size, n - cut_group_size)

print(min_cut(graph, list(graph.keys())[0]))
