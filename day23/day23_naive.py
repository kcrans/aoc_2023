# Naive backtracing solution that only finishes in a somewhat reasonable time for Part 1
import copy
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

def pretty_print(path):
    new_map = copy.deepcopy(trail_map)
    for x, y in path:
        new_map[x][y] = '0'
    for row in new_map:
        print("".join(row))
    print('-------------')

current_max = 0
pos_stack = [start]
path = []

while len(pos_stack) > 0:
    current_pos = pos_stack[-1]
    path.append(current_pos)
    x, y = current_pos
    #print(x, y, len(pos_stack), len(path))
    terrain_type = trail_map[x][y]
    back_trace = True
    if (x, y) == end:
        current_max = max(current_max, len(path) - 1)
#        print(len(path) - 1)
#        pretty_print(path)
    elif terrain_type in slopes:
        delta_x, delta_y = slopes[terrain_type]
        next_coords = (x + delta_x, y + delta_y)
        if next_coords not in path:
            back_trace = False
            pos_stack.append(next_coords)
    else:
        for delta_x, delta_y in next_moves:
            x0, y0 = x + delta_x, y + delta_y
            if x0 >= 0 and x0 <= m - 1 and y0 >= 0 and y0 <= n - 1:
                if (x0, y0) not in path and trail_map[x0][y0] != '#':
                    back_trace = False
                    pos_stack.append((x0, y0))
    if back_trace:
        while len(path) > 0 and path[-1] == pos_stack[-1]: 
            path.pop()
            pos_stack.pop()

print(current_max)
