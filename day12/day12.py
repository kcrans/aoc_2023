from itertools import combinations

with open("day12.txt", "r") as file:
    records = [line.strip('\n') for line in file]
spring_lists = []
groupings = []
for row in records:
    left, right = row.split()
    spring_lists.append('?'.join([left for _ in range(5)]))
    groupings.append([int(x) for _ in range(5) for x in right.split(',')])

def is_valid(spring_list, valid_groups):
    n = len(spring_list)
    m = len(valid_groups)
    i = 0
    group_index = 0
    in_seq = False
    while i < n:
        if spring_list[i] == '#':
            if in_seq:
                count += 1
            else:
                in_seq = True
                count = 1
        else:
            if in_seq:
                in_seq = False
                if group_index == m or valid_groups[group_index] != count:
                    return False
                else:
                    count = 0
                    group_index += 1
        i += 1
    if in_seq and count != valid_groups[group_index]:
        return False
    return True

test_list = ["###.###", "...#...#..###.", ".#.###.#.######", "####.#...#...", "#....######..#####.", ".###.##....#"]
total = 0
for spring_list, valid_group in zip(spring_lists, groupings):
    print(spring_list, valid_group)
    broken_count = spring_list.count('#')
    unknown_count = spring_list.count('?')
    possible_locs = [i for i, char in enumerate(spring_list) if char == '?']
    base_string = spring_list.replace('?', '.')
    combos = combinations(possible_locs, sum(valid_group) - broken_count)
    count = 0
    for combo in combos:
        base_list = list(base_string)
        for index in combo:
            base_list[index] = '#'
        if is_valid("".join(base_list), valid_group):
            count += 1
    total += count
print(total)
