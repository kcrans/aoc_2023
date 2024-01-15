from collections import deque

# Part 1 Solution:
with open("day21.txt", "r") as file:
    farm = [list(line.strip('\n')) for line in file]

m = len(farm)
n = len(farm[0])

# Convert the matrix into a matrix of ints where garden plots are
# 0's, rocks are 1's and the starting position is a 1.
mod_map = [[0 for j in range(n)] for i in range(m)]
for i in range(m):
    for j in range(n):
        if farm[i][j] == 'S':
            mod_map[i][j] = 1
            start_x, start_y = i, j
        elif farm[i][j] == '#':
            mod_map[i][j] = -1


def print_farm(current_step):
    """
    Used for debugging, this helper function prints the garden
    in stdout with a readable format
    """
    for row in mod_map:
        line = ""
        for num in row:
            if num == -1:
                line += '#'
            elif num == current_step:
                line += 'O'
            else:
                line += '.'
        print(line)
    print('_'*n)

num_steps = 64 
step_parity = num_steps % 2

queue = deque([(start_x, start_y)])
for step in range(1, num_steps + 1):
    parity = step % 2
    num_starts = len(queue)
#    print(num_starts, step)
    for start in range(num_starts):
        x, y = queue.popleft()
        # Check west
        if x > 0 and mod_map[x - 1][y] == 0:
            mod_map[x - 1][y] = step
            queue.append((x - 1, y))
        # Check east
        if x < m - 1 and mod_map[x + 1][y] == 0:
            mod_map[x + 1][y] = step
            queue.append((x + 1, y))
        # Check north
        if y > 0 and mod_map[x][y - 1] == 0:
            mod_map[x][y - 1] = step
            queue.append((x, y - 1))
        # Check south
        if y < n - 1 and mod_map[x][y + 1] == 0:
            mod_map[x][y + 1] = step
            queue.append((x, y + 1))

mod_map[start_x][start_y] = 2
num_blocks = 0
for row in mod_map:
    for block in row:
        if block > 0 and block % 2 == step_parity:
            num_blocks += 1
print(f"Part 1 total number of garden plots reachable in 64 steps: {num_blocks}")

# Part 2 Solution:
num_steps = 26501365 # (2*131) + 65 

def get_counts(start_x, start_y, min_dist = 0, max_dist = num_steps):
    """
    For a given starting position, this function will return
    the number of even and odd tiles reached with min_dist <= x <= max_dist steps
    """
    mod_map = [[0 for j in range(n)] for i in range(m)]
    for x in range(m):
        for y in range(n):
            if x == start_x and y == start_y:
                mod_map[x][y] = -1
            elif farm[x][y] == '#':
                mod_map[x][y] = -1

    # Use a queue for breadth first search
    # We don't really backtrack though because if we have already visited a node
    # with a different (shorter-or-equal) path there isn't any reason to keep on
    # exploring from that node because we already will have started that.
    queue = deque([(start_x, start_y)])
    step = 0
    while len(queue) > 0:
        step += 1
        # Go through all blocks
        num_starts = len(queue)
        for start in range(num_starts):
            x, y = queue.popleft()
            # Check west
            if x > 0 and mod_map[x - 1][y] == 0:
                mod_map[x - 1][y] = step
                queue.append((x - 1, y))
            # Check east
            if x < m - 1 and mod_map[x + 1][y] == 0:
                mod_map[x + 1][y] = step
                queue.append((x + 1, y))
            # Check north
            if y > 0 and mod_map[x][y - 1] == 0:
                mod_map[x][y - 1] = step
                queue.append((x, y - 1))
            # Check south
            if y < n - 1 and mod_map[x][y + 1] == 0:
                mod_map[x][y + 1] = step
                queue.append((x, y + 1))

    mod_map[start_x][start_y] = 2 # 2 instead of 0 to differentiate from stone blocks
    num_even_blocks = 0
    num_odd_blocks = 0
    for row in mod_map:
        for block in row:
            if block > min_dist and block <= max_dist:
                if block % 2 == 0:
                    num_even_blocks += 1
                else:
                    num_odd_blocks += 1

    return num_even_blocks, num_odd_blocks


# As n = m is even, the distance from the center straight to an edge is:
center_dist = n // 2

# After looking at the input data, I noticed a few things:
# * There is a 'highway' with a crossing at the center spot so you can go straight in a ordinal direction without running into rocks
# * The border of each map is a clear trail all around
# * Hence the fastest way to get to another block is just to take these "roads"
print(f"Distance from center to side: {center_dist}")

# Also, looking at this:
# 
#             0
#             0
#             0
#             0
#             0
#             0
# 0 0 0 0 0 0 X 0 0 0 0 0 0 
#             0
#             0
#             0
#             0
#             0
#             0
num_maps_across = (num_steps - center_dist) // n
print(f"Number of maps from center to top: {num_maps_across}")

# Now thinking in terms of maps of blocks, consider the parites of all the blocks cotained within
# Each block has a matching block on each of the 4 adjacent maps. The length/width of a map is
# 131, so each corresponding block will have to take a net 131 + 2*v steps along one axis and net 0 + 2*w along the other
# I.e. 131 is odd and 0 is even which means the distance is odd so each corresponding block will have opposite parity.
# How many completely explored maps will there be?
#               0
#       X      0X0
# 0 -> X0X -> 0X0X0
#       X      0X0
#               0

# The outer ring will have maps that are not complete, so
# we just need to count how many odd and even maps there are
# that are a distance of num_maps_across - 1 away from the center
complete_radius = num_maps_across - 1

num_regular = (complete_radius) ** 2 # First map in the center is normal
num_flipped = (complete_radius + 1) ** 2 # Next set of maps will be flipped

# For a full map, the number of odd and even tiles will be:
num_plots = get_counts(start_x, start_y)
print('Num of plots reached from a full map:', num_plots, 'Num of regular and fipped maps:', num_regular, num_flipped)

reg_parity = num_steps % 2
alt_parity = (num_steps + 1 ) % 2
print(reg_parity, alt_parity)
total = (num_regular * num_plots[reg_parity]) + (num_flipped * num_plots[alt_parity])
print('total', total, 'num steps', num_steps)

# Now let's move on to partial maps
next_parity = (num_maps_across) % 2
last_parity = complete_radius % 2
print(f'parity last and next {last_parity}, {next_parity}')

for x, y in (m - 1, center_dist), (center_dist, 0), (0, center_dist), (center_dist, n - 1):
    print(f"{x}, {y}, with distance {m - 1} : {get_counts(x, y, 0, m - 1)}")
    total += get_counts(x, y, 0, m - 1)[next_parity]

num_tri_per_side = num_maps_across 
num_pent_per_side = num_maps_across - 1

print('num of tris + pents per side', num_tri_per_side, num_pent_per_side)

steps_left_tri = n - center_dist - 2
steps_left_pent = (2*n) - center_dist - 2

# cycle through the sides: upper-right, upper-left, lower-right, lower-left 
for x, y in (m - 1, 0), (m - 1, n - 1), (0, 0), (0, n - 1):
    total += num_tri_per_side * get_counts(x, y, 0, steps_left_tri)[next_parity]
    total += num_pent_per_side * get_counts(x, y, 0, steps_left_pent)[last_parity]
    print(f"{x}, {y}, with distance {steps_left_tri} and {num_tri_per_side} times : {get_counts(x, y, 0, steps_left_tri)}")


print(total)
