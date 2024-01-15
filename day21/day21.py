# Part 1 Solution:
with open("day21.txt", "r") as file:
    farm = [list(line.strip('\n')) for line in file]

m = len(farm)
n = len(farm[0])

# Convert the matrix into a matrix of ints where garden plots are
# 0's, rocks are 1's and the starting position is a 1.
mod_farm = [[0 for j in range(n)] for i in range(m)]
for i in range(m):
    for j in range(n):
        if farm[i][j] == 'S':
            mod_farm[i][j] = 1
            start_x, start_y = i, j
        elif farm[i][j] == '#':
            mod_farm[i][j] = -1


def print_farm(current_step):
    """
    Used for debugging, this helper function prints the garden
    in stdout with a readable format
    """
    for row in mod_farm:
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

num_steps = 6

for step in range(1, num_steps + 1):
    # For a given number of steps, keep track of the number of locations reached at the last step
    num_locs = 0
    # Loop through all tiles
    for i in range(m):
        for j in range(n):
            if mod_farm[i][j] == step or mod_farm[i][j] == step + 2:
                # Look at all neighboring tiles
                for i_0, j_0 in (max(i - 1, 0), j), (i, min(j + 1, m - 1)), (min(i + 1, m - 1), j), (i, max(j - 1, 0)):    
                    # Ignore the tile we are presently on
                    if i_0 == i and j_0 == j:
                        continue
                    # Ignore any rock tiles
                    elif mod_farm[i_0][j_0] == -1:
                        continue
                    # We found a tile that was visited last round
                    # We want to make sure we use it as a starting off point this round,
                    # so we mark it such that we can still visit it (step + 2)
                    elif mod_farm[i_0][j_0] == step:
                        num_locs += 1
                        mod_farm[i_0][j_0] = step + 2
                    # We found a tile that was not visited last round, so let's
                    # mark it in order to visit it next round
                    elif mod_farm[i_0][j_0] < step:
                        num_locs += 1
                        mod_farm[i_0][j_0] = step + 1
    # Loop back over the tiles and standarize them so that they are
    #
    for i in range(m):
        for j in range(n):
            if mod_farm[i][j] == step + 2:
                mod_farm[i][j] = step + 1
 #   print_farm(step + 1)
print(num_locs)


