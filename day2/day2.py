# Part 1 solution

# Dict to find max number of each cube color allowed
cubes = {}
cubes['red'] = 12
cubes['green'] = 13
cubes['blue'] = 14

def is_possible(cube_sets):
    """
    For a given set of colors and amounts,
    return True if it is possible to draw this
    specific set given the known cube counts.
    """
    for cube_set in cube_sets:
        for cube_grouping in cube_set.split(', '):
            amount, color = cube_grouping.split()
            amount = int(amount)
            if amount > cubes[color]:
                return False
    return True

with open('day2.txt', 'r') as file:
    score = 0
    for line in file:
        game_num, game = line.split(':')
        game_num = int(game_num.split()[1])
        cube_sets = game.split('; ')
        if is_possible(cube_sets):
            score += game_num
    print(f"Part 1's score: {score}")

# Part 2 solution

def get_power(cube_sets):
    """
    Returns the minimum amount of each color
    in order to make the set of draws possible.
    """
    cubes = {'red': 0, 'green': 0, 'blue': 0}

    for cube_set in cube_sets:
        for cube_grouping in cube_set.split(', '):
            amount, color = cube_grouping.split()
            amount = int(amount)
            cubes[color] = max(cubes[color], amount)

    return cubes['red']*cubes['green']*cubes['blue']

with open('day2.txt', 'r') as file: 
    score = 0
    for line in file:
        game_num, game = line.split(':')
        game_num = int(game_num.split()[1])
        cube_sets = game.split('; ')
        score += get_power(cube_sets)
print(f"Part 2's score: {score}")
