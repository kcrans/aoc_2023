with open("day21.txt", "r") as file:
    farm = [list(line.strip('\n')) for line in file]
m = len(farm)
n = len(farm[0])
mod_farm = [[0 for j in range(n)] for i in range(m)]

def print_farm(current_step):
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

for i in range(m):
    for j in range(n):
        if farm[i][j] == 'S':
            mod_farm[i][j] = 1
            farm[i][j] = 'O'
            start_x, start_y = i, j
        elif farm[i][j] == '#':
            mod_farm[i][j] = -1

num_steps = 64
#print_farm(1)

for step in range(1, num_steps + 1):
    num_locs = 0
    for i in range(m):
        for j in range(n):
            if mod_farm[i][j] == step or mod_farm[i][j] == step + 2:
                for i_0, j_0 in (max(i - 1, 0), j), (i, min(j + 1, m - 1)), (min(i + 1, m - 1), j), (i, max(j - 1, 0)):
                        if i_0 == i and j_0 == j:
                            continue
                        elif mod_farm[i_0][j_0] == -1:
                            continue
                        elif mod_farm[i_0][j_0] == step:
                            num_locs += 1
                            mod_farm[i_0][j_0] = step + 2
                        elif mod_farm[i_0][j_0] < step:
                            num_locs += 1
                            mod_farm[i_0][j_0] = step + 1
#    for line in mod_farm:
#        print(line)
#    break
    for i in range(m):
        for j in range(n):
            if mod_farm[i][j] == step + 2:
                mod_farm[i][j] = step + 1
 #   print_farm(step + 1)
    print(num_locs)


