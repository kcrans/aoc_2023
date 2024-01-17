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
num_steps = 26501365 # Note that this is an odd number 

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
assert n == m
assert start_x == start_y
# The distance from the center straight to an edge is:
center_dist = n - start_x - 1

# After looking at the input data, I noticed a few things:
# * There is a 'highway' with a crossing at the center spot so you can go straight in a ordinal direction without running into rocks
# * The border of each map is a clear trail all around
# * Hence the fastest way to get to another map is just to take these "roads"
# * I.e. the shortest path from anywhere in one map to anywhere in another map will use one of these highways

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

# Where O is a map and X is the starting map, we see that we can go
# total_number_of_steps - steps_to_first_edge north, south, east, or west
# Conviently, this value is divisible by the length/width of a map, so
# we can measure this distance in terms of the number of maps traversed.
assert (num_steps - center_dist) % n == 0
num_maps_across = (num_steps - center_dist) // n

# Now thinking in terms of maps of blocks, consider the parites of all the blocks cotained within a map
# Each block has a matching block on each of the 4 adjacent maps. The length/width of a map is
# 131, so each corresponding block will have to take a net 131 + 2*v steps along one axis and net 0 + 2*w along the other
# I.e. 131 is odd and 0 is even which means the distance is odd so each corresponding block will have opposite parity.
# How many completely explored maps will there be?
#                                     0
#                         X          0X0
#               0        X0X        0X0X0
#       X      0X0      X0X0X      0X0X0X0
# 0 -> X0X -> 0X0X0 -> X0X0X0X -> 0X0X0X0X0
#       X      0X0      X0X0X      0X0X0X0
#               0        X0X        0X0X0
#                         X          0X0
#                                     0
#
# 0     1       2         3           4
# Number of regular maps: 1, 1, 9, 9, 25
# Number of flipped maps: 0, 4, 4, 16, 16 
# In terms of i:
#               (i+1)^2,     i^2, (i+1)^2,     i^2, (i+1)^2
#                   i^2, (i+1)^2,     i^2, (i+1)^2,     i^2

# The outer ring will have maps that are not complete, so
# we just need to count how many odd and even maps there are
# that are a distance of num_maps_across - 1 away from the center
full_radius = num_maps_across - 1
is_even = full_radius % 2 == 0

num_regular = (full_radius + 1) ** 2 if is_even else (full_radius) ** 2
num_flipped = (full_radius) ** 2 if is_even else (full_radius + 1) ** 2

# For a full map, the number of odd and even tiles will be:
num_plots = get_counts(start_x, start_y)

# If you take an even number of steps, you'll want to add up the even counts for regular maps and odd counts for flipped maps
# Likewise, with an odd number of steps you'll sum up the odd counts for all the regular maps and even counts for the other
reg_parity = num_steps % 2 
alt_parity = (num_steps + 1 ) % 2
# Add all the full maps to our total
total = (num_regular * num_plots[reg_parity]) + (num_flipped * num_plots[alt_parity])

# Now let's move on to partial maps
next_parity = num_maps_across % 2 # Parity of outside ring
last_parity = full_radius % 2 # Parity of last ring of full maps

# Calculate the location counts for every ending point of the diamond: N, E, S, W
for x, y in (m - 1, center_dist), (center_dist, 0), (0, center_dist), (center_dist, n - 1):
    total += get_counts(x, y, 0, m - 1)[next_parity]

# ^ = triangle, / = pentagon
#   0^ /
#   0 0^ /
#   0 0 0^ /
#   0 0 0 0^
#   0 0 0 0 0
#   0 1 2 3 4 = nums_maps_across

num_tri_per_side = num_maps_across 
num_pent_per_side = num_maps_across - 1

steps_left_tri = n - center_dist - 2 # n - number it takes to get into the appropriate map
steps_left_pent = (2*n) - center_dist - 2 # We have to go a whole n further back than the case above

# cycle through the sides: upper-right, upper-left, lower-right, lower-left 
for x, y in (m - 1, 0), (m - 1, n - 1), (0, 0), (0, n - 1):
    total += num_tri_per_side * get_counts(x, y, 0, steps_left_tri)[next_parity]
    total += num_pent_per_side * get_counts(x, y, 0, steps_left_pent)[last_parity]

print(f"Part 2 total number of garden plots reachable in {num_steps} steps: {total}")
