import copy
# Part 1's Solution:
trail_map = []
with open("day23.txt", "r") as file:
    for line in file:
        trail_map.append(list(line.strip('\n')))

m, n = len(trail_map), len(trail_map[0])

for i in range(n):
    if trail_map[0][i] == '.':
        start = (0, i)
    if trail_map[m - 1][i] == '.':
        end = (m - 1, i)
print(start, end)

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

def backtrack(path):
    x, y = path[-1]
#    print(x, y)
    terrain_type = trail_map[x][y]
    if path[-1] == end:
        global current_max
        current_max = max(current_max, len(path) - 1)
        #print(len(path) - 1)
        #pretty_print(path)
    elif terrain_type in slopes:
        delta_x, delta_y = slopes[terrain_type]
        next_coords = (x + delta_x, y + delta_y)
        if next_coords not in path:
            path.append(next_coords)
            backtrack(path)
    else:
        for delta_x, delta_y in next_moves:
            x0, y0 = x + delta_x, y + delta_y
            if x0 >= 0 and x0 <= m - 1 and y0 >= 0 and y0 <= n - 1:
                if (x0, y0) not in path and trail_map[x0][y0] != '#':
                    path.append((x0, y0))
                    backtrack(path)
    path.pop()

backtrack([start])
print(current_max)
