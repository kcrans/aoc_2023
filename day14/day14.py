from collections import defaultdict
with open("day14.txt", "r") as file:
    mirrors = [list(line) for line in file.read().strip('\n').split('\n')]

m, n = len(mirrors), len(mirrors[0])
def calc_load(mirrors):
    total_sum = 0
    for col in range(n):
        load = m
        for dist, row in enumerate(mirrors):
            if row[col] == 'O':
                #print(load)
                total_sum += load
                load -= 1
            elif row[col] == "#":
                load = m - (dist + 1)
            else:
                pass
    return total_sum
print(f"Part 1's total loads: {calc_load(mirrors)}")
def calc_load_naive(mirrors):
    total_sum = 0
    for col in range(n):
        for dist, row in enumerate(mirrors):
            if row[col] == 'O':
                total_sum += m - dist
    return total_sum
states = []
state_loads = {}
new_mirrors = [["." for j in range(n)] for i in range(m)]
while True:
    increment = 1
    for col in range(n):
        new_index = 0
        for row in range(m):
            if mirrors[row][col] == 'O':
                new_mirrors[new_index][col] = 'O'
                new_index += increment
            elif mirrors[row][col] == "#":
                new_mirrors[row][col] = '#'
                new_index = row + increment
            else:
                pass
    for i in range(m):
        for j in range(n):
            mirrors[i][j] = new_mirrors[i][j]
            new_mirrors[i][j] = '.'
    increment = 1
    for row in range(m):
        new_index = 0
        for col in range(n):
            if mirrors[row][col] == 'O':
                new_mirrors[row][new_index] = 'O'
                new_index += increment
            elif mirrors[row][col] == "#":
                new_mirrors[row][col] = '#'
                new_index = col + increment
            else:
                pass
    for i in range(m):
        for j in range(n):
            mirrors[i][j] = new_mirrors[i][j]
            new_mirrors[i][j] = '.'
    increment = -1
    for col in range(n):
        new_index = m - 1
        for row in range(m - 1, -1, -1):
            if mirrors[row][col] == 'O':
                new_mirrors[new_index][col] = 'O'
                new_index += increment
            elif mirrors[row][col] == "#":
                new_mirrors[row][col] = '#'
                new_index = row + increment
            else:
                pass
    for i in range(m):
        for j in range(n):
            mirrors[i][j] = new_mirrors[i][j]
            new_mirrors[i][j] = '.'
    increment = -1
    for row in range(m):
        new_index = n - 1
        for col in range(n - 1, -1, -1):
            if mirrors[row][col] == 'O':
                new_mirrors[row][new_index] = 'O'
                new_index += increment
            elif mirrors[row][col] == "#":
                new_mirrors[row][col] = '#'
                new_index = col + increment
            else:
                pass
    for i in range(m):
         for j in range(n):
            mirrors[i][j] = new_mirrors[i][j]
            new_mirrors[i][j] = '.'
    #for row in mirrors:
    #    print("".join(row))
    #print(f"{num}-------------------")
    key = "".join(["".join(row) for row in mirrors])
    if key in states:
        start_of_cycle = states.index(key)
        print(f"key's value: {state_loads[key]}\n")
        break
    else:
        states.append(key)
        state_loads[key] = calc_load_naive(mirrors)
        #print(f"key's value: {state_loads[key]}\n")
        #for row in mirrors:
        #    print("".join(row))

num_iters = 1000000000
time_in_cycle = num_iters - (start_of_cycle + 1)
print([state_loads[state] for state in states], start_of_cycle)

#for state in states:
#    print(state_loads[state])
final_index = time_in_cycle % (len(states) - start_of_cycle)
#print(final_index, time_in_cycle, start_of_cycle)
final_mirror = states[start_of_cycle + final_index]
print(state_loads[final_mirror])
