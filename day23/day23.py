import copy
from collections import defaultdict
# Part 1's Solution:
trail_map = []
with open("day23.txt", "r") as file:
    for line in file:
        trail_map.append(list(line.strip('\n')))

m, n = len(trail_map), len(trail_map[0])

# Find the coordinates for the start and end of the trail
for i in range(n):
    if trail_map[0][i] == '.':
        start = (0, i)
    if trail_map[m - 1][i] == '.':
        end = (m - 1, i)

slopes = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}
next_moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

# Now let's condense the map into only the trail junctions
# This is so we don't have to put each unit of a straight trail
# onto our stack.

junctions = defaultdict(list)

def follow_trail(last_coords, current_coords):
    distance = 1
    while True:
        i, j = current_coords
        num_connections = 0
        for delta_i, delta_j in next_moves:
            i0, j0 = i + delta_i, j + delta_j
            if i0 >= 0 and i0 <= m - 1 and j0 >= 0 and j0 <= n - 1:
                if trail_map[i0][j0] != '#' and (i0, j0) != last_coords:
                    next_coords = (i0, j0)
                    num_connections += 1
        if num_connections == 1:
            distance += 1
            last_coords = current_coords
            current_coords = next_coords
        else:
            return (current_coords, distance)


for i in range(m):
    for j in range(n):
        if trail_map[i][j] != '#':
            num_connections = 0
            for delta_i, delta_j in next_moves:
                i0, j0 = i + delta_i, j + delta_j
                if i0 >= 0 and i0 <= m - 1 and j0 >= 0 and j0 <= n - 1:
                    if trail_map[i0][j0] != '#':
                        num_connections += 1
            if num_connections >= 3:
                for delta_i, delta_j in next_moves:
                    i0, j0 = i + delta_i, j + delta_j
                    distance = 1
                    if i0 >= 0 and i0 <= m - 1 and j0 >= 0 and j0 <= n - 1 and trail_map[i0][j0] != '#':  
                        junctions[(i, j)].append(follow_trail((i, j), (i0, j0)))

first_junction, distance = follow_trail(start, (start[0] + 1, start[1]))

current_max = distance
pos_stack = [first_junction]
path = []

#print(junctions)
#print(len(junctions))
#print(2 ** (len(junctions)))
def get_distance(path):
    total_dist = distance
    path_len = len(path)
    for i in range(path_len - 1):
        incoming, outgoing = path[i], path[i + 1]
        for next_junction, dist in junctions[incoming]:
            if next_junction == outgoing:
                total_dist += dist
                break
    return total_dist

def pretty_print(path):
    new_map = copy.deepcopy(trail_map)
    new_map[start[0]][start[1]] = '0'
    i = 1
    for x, y in path:
        i += 1
        new_map[x][y] = str(i)
    for row in new_map:
        print("".join(row))
    print('-------------')

while len(pos_stack) > 0:
    #    print(pos_stack)
    current_pos = pos_stack[-1]
    path.append(current_pos)
    x, y = current_pos
    back_trace = True
    if (x, y) == end:
        current_max = max(current_max, get_distance(path))
        #print('end')
        #        print(len(path) - 1)
#        pretty_print(path)
    else:
        for next_coords, dist_from in junctions[current_pos]:
            if next_coords not in path: 
                back_trace = False
                pos_stack.append(next_coords)
    if back_trace:
        while len(path) > 0 and path[-1] == pos_stack[-1]: 
            path.pop()
            pos_stack.pop()

print(current_max)
