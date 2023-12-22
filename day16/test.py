with open('day16.txt') as f:
    grid = f.read().strip().split('\n')

directions = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
mirrors = {
    ('R', '/'): 'U',
    ('D', '/'): 'L',
    ('L', '/'): 'D',
    ('U', '/'): 'R',
    ('R', '\\'): 'D',
    ('U', '\\'): 'L',
    ('L', '\\'): 'U',
    ('D', '\\'): 'R'
}

def count_tiles(current_d: str, start_pos: tuple, energized: set) -> set:
    i, j = start_pos
    while 0 <= i < len(grid) and 0 <= j < len(grid[0]):
        if grid[i][j] in '/\\':
            current_d = mirrors[(current_d, grid[i][j])]
        # Stop looping
        if grid[i][j] in '-|' and (i, j) in energized:
            # print((i, j), current_d, grid[i][j])
            return energized
        energized.add((i, j))

        if grid[i][j] == '|' and current_d in 'LR':
            energized |= count_tiles('U', (i - 1, j), energized)
            energized |= count_tiles('D', (i + 1, j), energized)
            return energized
        elif grid[i][j] == '-' and current_d in 'UD':
            energized |= count_tiles('R', (i, j + 1), energized)
            energized |= count_tiles('L', (i, j - 1), energized)
            return energized

        i += directions[current_d][0]
        j += directions[current_d][1]
    else:
        return energized


result_1 = count_tiles('R', (0, 0), set())
print('Part 1:', len(result_1))
