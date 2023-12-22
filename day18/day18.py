import sys
import numpy as np

np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=np.inf)

dig_plan = []
with open("day18.txt", "r") as file:
    for line in file:
        direction, length, color = line.strip('\n').split(' ')
        length = int(length)
        color = color.strip('(#)')
        dig_plan.append((direction, length, color))

n = len(dig_plan)
horz_types = {}
last_instruction = dig_plan[-1]
if last_instruction[0] in 'RL': 
    if dig_plan[-2][0] == dig_plan[0][0]:
        horz_types[last_instruction] = 'line'
    else:
        horz_types[last_instruction] = 'bend'
     

for i in range(0, n-1):
    instruction = dig_plan[i]
    if instruction[0] in 'RL':
        if dig_plan[i-1][0] == dig_plan[i+1][0]:
            horz_types[instruction] = 'line'
        else:
            horz_types[instruction] = 'bend'
            
min_x = 0
max_x = 0
min_y = 0
max_y = 0

x_coord = 0
y_coord = 0
for direction, length, color in dig_plan:
    if direction == 'R':
        x_coord += length
        max_x = max(x_coord, max_x)
    elif direction == 'L':
        x_coord -= length
        min_x = min(x_coord, min_x)
    elif direction == 'U':
        y_coord -= length
        min_y = min(y_coord, min_y)
    elif direction == 'D':
        y_coord += length
        max_y = max(y_coord, max_y)

terrain = np.array([[0 for x in range(min_x, max_x + 1)] for y in range(min_y, max_y + 1)])
print(np.shape(terrain))
x, y = -1*min(min_x, 0), -1*min(min_y, 0)

for direction, length, color in dig_plan:
    delta_x, delta_y = 0, 0
    if direction == 'R':
        delta_x = length
        terrain[y][x] = 1
        for x_0 in range(x + 1, x + delta_x + 1):
            terrain[y][x_0] = -1
        if horz_types[(direction, length, color)] == 'bend':
            terrain[y][x + delta_x] = 1
    elif direction == 'L':
        delta_x = -1*length
        terrain[y][x + delta_x] = 1
        for x_0 in range(x, x + delta_x, -1):
            terrain[y][x_0] = -1
        if horz_types[(direction, length, color)] == 'bend':
            terrain[y][x] = 1
    elif direction == 'U':
        delta_y = -1*length
        for y_0 in range(y - 1, y + delta_y, -1):
            terrain[y_0][x] = 1
    elif direction == 'D':
        delta_y = length
        for y_0 in range(y + 1, y + delta_y):
            terrain[y_0][x] = 1
    x = x + delta_x
    y = y + delta_y


for row in terrain:
    for digit in row:
        char = ' ' if digit == 0 else 'a'
        print(char, end='')
    print('\n', end='')
total_count = 0
for y in range(len(terrain)):
    edge_seen = 0
    x = 0
    while x < len(terrain[0]):
        if terrain[y][x] == 1:
            edge_seen += 1
            total_count += 1
            x += 1
        elif terrain[y][x] == -1:
            total_count += 1
            x += 1
        else:
            blank_count = 0
            while x < len(terrain[0]) and terrain[y][x] == 0:
                blank_count += 1
                x += 1
            if not (x == len(terrain[0])) and (edge_seen % 2) == 1:
                total_count += blank_count
print(total_count)
