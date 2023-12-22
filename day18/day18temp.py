import sys
import numpy as np

np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=np.inf)

dig_plan = []

def convert_num_dir(num):
    match num:
        case '0': 
            return 'R'
        case '1': 
            return 'D'
        case '2': 
            return 'L'
        case '3': 
            return 'U'

with open("day18.txt", "r") as file:
    for line in file:
        old_direction, old_length, color = line.strip('\n').split(' ')
        data = color.strip('(#)')
        length = int(data[:-1], base=16)
        direction = convert_num_dir(data[-1]) 
        dig_plan.append((direction, length ))

n = len(dig_plan)
            
min_x = 0
max_x = 0
min_y = 0
max_y = 0

x_coord = 0
y_coord = 0
for direction, length in dig_plan:
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

print(min_x, max_x, min_y, max_y)



