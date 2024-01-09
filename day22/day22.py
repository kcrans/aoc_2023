# Part 1 Solution:

from collections import defaultdict

# I am going to store all the coordinates for the bricks in a single list
# The format for a given brick will be:
# ((x1, x2, y1, y2), z1, z2)
# Where each sublist is a range of coordinates a brick occupies along each dimmension
# In order to standardize everything, I will make each range be sorted in ascending order
# I.e. (2, 7) instead of (7, 2)

bricks = []
with open('day22.txt', 'r') as file:
    for line in file:
        left, right = line.strip('\n').split('~')
        left_coords = left.split(',')
        right_coords = right.split(',')
        x1, y1, z1 = (int(coord) for coord in left_coords) 
        x2, y2, z2 = (int(coord) for coord in right_coords)
        bricks.append(((x1, x2, y1, y2), z1, z2))

# Now sort the list in ascending order according to the mininum z value
# I.e. sort the list so that we can loop through all bricks starting from the brick positioned the lowest
# to the highest brick (where position is defined by the bottom of the brick)

bricks.sort(key = lambda brick : brick[1])

def intersect(brick_a, brick_b):
    """
    Returns True if two bricks would intersect each other in the x-y plane
    Which happens if there is overlap in both their x and y coordinates
    I.e.
    (    a    )      (   b   ) 
    or
    (    b   )       (     a       )
    and then the two respective vertical cases
    """
    a_x1, a_x2, a_y1, a_y2 = brick_a
    b_x1, b_x2, b_y1, b_y2 = brick_b
    if a_x1 > b_x2 or a_x2 < b_x1 or a_y1 > b_y2 or a_y2 < b_y1:
            return False
    # Otherwise there is some intersetion along each dimmension
    return True

# Once we find the resting position of a brick, add it to this list:
fallen_bricks = []

# This dictionary tells us for each brick which other bricks are directly beneath it
# once the bricks have fallen. The identifier for each brick is its final coordinates.
bricks_below = {}
# Likewise this dictionary keeps track of higher bricks resting on a given brick
bricks_above = defaultdict(list)

for brick in bricks:
    # Check if the brick would land on any of the bricks below it
    has_fallen = False 
    num_supports = 0 # Number of lower bricks which prop up this brick once it has fallen
    # Loop over all bricks that this brick could possibly land on
    # sorted in ascending order according to their heights
    for next_brick in reversed(fallen_bricks):
        if intersect(brick[0], next_brick[0]):
            if has_fallen:
                if next_brick[2] == new_z - 1:
                    bricks_below[resting_brick].append(next_brick)
                    bricks_above[next_brick].append(resting_brick)
                    continue
            else:
                # First brick seen below our brick of choice which our brick can land on
                # Hence the sorting means it will be one of the bricks which our brick lands on
                has_fallen = True
                new_z = next_brick[2] + 1
                dist = brick[2] - brick[1]
                resting_brick = (brick[0], new_z, new_z + dist)
                bricks_below[resting_brick] = [next_brick]
                bricks_above[next_brick].append(resting_brick)
    if has_fallen:
        fallen_bricks.append(resting_brick)
        fallen_bricks.sort(key = lambda fallen_brick: fallen_brick[2])
    # If we don't find any bricks below this brick which it can land on
    else:
        # Brick must land on the ground then
        dist = brick[2] - brick[1]
        resting_brick = (brick[0], 1, 1 + dist)
        fallen_bricks.append(resting_brick)
        fallen_bricks.sort(key = lambda fallen_brick: fallen_brick[2])
        bricks_below[resting_brick] = []

unbreakable_bricks = set()
for key, value in bricks_below.items():
    if len(value) == 1:
        unbreakable_bricks.add(value[0])
i = len(unbreakable_bricks)

print(f"Part 1 number of bricks that can be disintegrated: {len(bricks) - i}")

# Part 2 Solution:

def recurse(support_set, brick):
    """
    Takes in a set of 'fragile' bricks which will fall and adds any bricks higher up
    which also would fall if the root brick was destroyed. It does this using a 
    recursive breadth-first search.
    """
    if all(brick_below in support_set for brick_below in bricks_below[brick]):
        support_set.add(brick)
        for next_brick in bricks_above[brick]:
            recurse(support_set, next_brick)
    return None

total = 0
# Loop through all breaks cannot be removed without causing other bricks to fall
for starting_brick in unbreakable_bricks:
    # Use a set to keep track of bricks which will fall if the first brick is disintegrated
    supports = {starting_brick}
    for brick_above in bricks_above[starting_brick]: # Visit all bricks above
        recurse(supports, brick_above)
    total += len(supports) - 1 # Ignore the original brick in the count

print(f"Part 2's sum of total number of bricks that would fall: {total}")
