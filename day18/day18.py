# Part 1 solution:
import sys
import numpy as np

# This will allow us to view the map completely when printed
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
horz_types = {} # Catogorize all instructions that move horizontally
last_instruction = dig_plan[-1] # Special case for last instruction in the closed loop
if last_instruction[0] in 'RL': 
    if dig_plan[-2][0] == dig_plan[0][0]:
        #   0 0 0 0    0     0
        #   0     0 or 0     0
        #   0     0    0 0 0 0
        horz_types[last_instruction] = 'line'
    else:
        #         0    0
        #   0 0 0 0 or 0 0 0 0
        #   0                0
        horz_types[last_instruction] = 'bend'
     

for i in range(0, n - 1):
    instruction = dig_plan[i]
    if instruction[0] in 'RL':
        if dig_plan[i - 1][0] == dig_plan[i + 1][0]:
            horz_types[instruction] = 'line'
        else:
            horz_types[instruction] = 'bend'
            
min_x, max_x, min_y, max_y = 0, 0, 0, 0
x_coord, y_coord = 0, 0 # Begining starts at 0, 0

# Find the dimmensions needed to make a compatible matrix
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
x, y = -1*min(min_x, 0), -1*min(min_y, 0) # Find where (0, 0) maps to in new array

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

def print_terrain(terrain):
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
print(f"Part 1's lagoon volume: {total_count} cubic meters")

# Part 2 Solution:
# We're going to use a totally different and much more effecient approach

def convert_num_dir(num):
    """Converts digits to directions according to problem statement """
    match num:
        case '0': # Right
            return (1, 0)
        case '1': # Down
            return (0, -1)
        case '2': # Left
            return (-1, 0)
        case '3': # Up
            return (0, 1)
current_point = (0, 0)
points = [current_point]
perimeter = 0
with open("day18.txt", "r") as file:
    for line in file:
        # Extract the hex code for colors and convert the first 
        # 5 digits to an integer, and the last digit to a direction
        old_direction, old_length, color = line.strip('\n').split(' ')
        data = color.strip('(#)')
        length = int(data[:-1], base=16)
        perimeter += length
        dx, dy = convert_num_dir(data[-1]) 
        x, y = current_point
        current_point = (x + length*dx, y + length*dy)
        points.append(current_point)
n = len(points) - 1
# First, let's use the shoelace forumla
area = 0.5*abs(sum(points[i][0]*points[i+1][1]for i in range(n)) - sum(points[i][1]*points[i+1][0] for i in range(n)))
# Then Pick's theorem:
print(f"Part 2's lagoon volume: {(perimeter//2) + int(area) + 1} cubic meters")

