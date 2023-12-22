with open("day16.txt", "r") as file:
    layout = file.read().strip('\n').split('\n')
#print(layout)
n, m = len(layout), len(layout[0])
print(n, m)
dirs = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
def trace_path(x, y, direction, energized_matrix, beam_starts, starts_seen):
    while True:
        if x < 0 or x >= n or y < 0 or y >= m:
            return 0 
 #       print(x, y)
        energized_matrix[x][y] = 1
        match layout[x][y]:
            case '.':
                pass
            case '/':
                if direction == 'R':
                    direction = 'U'
                elif direction == 'L':
                    direction = 'D'
                elif direction == 'U':
                    direction = 'R'
                else:
                    direction = 'L'
            case '\\':
                if direction == 'R':
                    direction = 'D'
                elif direction == 'L':
                    direction = 'U'
                elif direction == 'U':
                    direction = 'L'
                else:
                    direction = 'R'
            case '|':
                if direction == 'R':
                    direction = 'U'
                    starts_seen.add((x - 1, y, 'U'))
                    if (x + 1, y, 'D') not in starts_seen:
                        starts_seen.add((x + 1, y, 'D'))
                        beam_starts.append((x + 1, y, 'D'))
                elif direction == 'L':
                    direction = 'U'
                    starts_seen.add((x - 1, y, 'U'))
                    if (x + 1, y, 'D') not in starts_seen:
                        starts_seen.add((x + 1, y, 'D'))
                        beam_starts.append((x + 1, y, 'D'))

                elif direction == 'U':
                    direction = 'U'
                else:
                    direction = 'D'
            case '-':
                if direction == 'R':
                    direction = 'R'
                elif direction == 'L':
                    direction = 'L'

                elif direction == 'U':
                    direction = 'L'
                    starts_seen.add((x, y - 1, 'L'))
                    if (x, y + 1, 'R') not in starts_seen:
                        starts_seen.add((x, y + 1, 'R'))
                        beam_starts.append((x, y + 1, 'R'))
                else:
                    direction = 'L'
                    starts_seen.add((x, y - 1, 'L'))
                    if (x, y + 1, 'R') not in starts_seen:
                        starts_seen.add((x, y + 1, 'R'))
                        beam_starts.append((x, y + 1, 'R'))
        
        dx, dy = dirs[direction]
        x += dx
        y += dy

def get_energy(start_x, start_y, start_dir):
    energized_matrix = [[0 for j in range(m)] for i in range(n)]
    beam_starts = [(start_x, start_y, start_dir)]
    starts_seen = set()

    while len(beam_starts) > 0:
        next_path = beam_starts.pop()
        trace_path(*next_path, energized_matrix, beam_starts, starts_seen)

    return sum([sum(row) for row in energized_matrix])
max_energy = 0
for i in range(n):
    max_energy = max(get_energy(i, 0, 'R'), get_energy(i, m - 1, 'L'), max_energy)
for i in range(m):
    max_energy = max(get_energy(0, i, 'D'), get_energy(n - 1, i, 'U'), max_energy)
print(max_energy)
