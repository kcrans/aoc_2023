import numpy as np
from heapq import *

with open("day17.txt", "r") as f:
    loss_map = np.array([[int(x) for x in row.strip('\n')] for row in f])
m, n = len(loss_map), len(loss_map[0])

# Keep track of next possible cells to visit
# Stored in a heap so the cell with the smallest cost can easily be found
frontier = []

x, y, cost = 0, 0, 0

for delta_y in 1, 2, 3:
    next_cost = sum(loss_map[x, (y + 1):(y + delta_y + 1)])
    heappush(frontier, (next_cost, x, y + delta_y, 'H'))
for delta_x in 1, 2, 3:
    next_cost = sum(loss_map[(x + 1):(x + delta_x + 1), y])
    heappush(frontier, (next_cost, x + delta_x, y, 'V'))
seen = set()
seen.add((0, 0, 'H'))
seen.add((0, 0, 'V'))
h_costs = np.zeros((m, n)) 
v_costs = np.zeros((m, n))
final_costs = {}
final_costs['H'] = h_costs
final_costs['V'] = v_costs
#while (x != m - 1) or (y != n - 1):
while len(frontier) > 0:
    last_cost, x, y, last_axis  = heappop(frontier)
    if (x, y, last_axis) in seen:
        continue
    else:
        seen.add((x, y, last_axis))
    final_costs[last_axis][x][y] = last_cost
    if last_axis == 'H':
        above = range(x - 1, max(x - 4, -1), -1 )
        below = range(x + 1, min(x + 4, m))
        next_cost = last_cost
        for next_x in above:
            next_cost += loss_map[next_x][y]
            if ((next_x, y, 'V')) not in seen:
                heappush(frontier, (next_cost, next_x, y, 'V'))
        next_cost = last_cost
        for next_x in below:
            next_cost += loss_map[next_x][y]
            if ((next_x, y, 'V')) not in seen:
                heappush(frontier, (next_cost, next_x, y, 'V'))
    else: # last_axis == 'V'
        left = range(y - 1, max(y - 4, -1), -1)
        right = range(y + 1, min(y + 4, n))
        next_cost = last_cost
        for next_y in left:
            next_cost += loss_map[x][next_y]
            if ((x, next_y, 'H')) not in seen:
                heappush(frontier, (next_cost, x, next_y, 'H'))
        next_cost = last_cost
        for next_y in right:
            next_cost += loss_map[x][next_y]
            if ((x, next_y, 'H')) not in seen:
                heappush(frontier, (next_cost, x, next_y, 'H'))

print(min(h_costs[-1][-1], v_costs[-1][-1]))
