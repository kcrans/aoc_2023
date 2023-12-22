from itertools import combinations
with open("day12.txt", "r") as file:
    records = [line.strip('\n') for line in file]

# Part 1 and 2 Solution:
spring_lists = []
groupings = []
for row in records:
    left, right = row.split()
    spring_lists.append(left)
    groupings.append([int(x) for x in right.split(',')])

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

def works_for_group(spring_list, i, group_len):
    if (i + group_len - 1) >= len(spring_list):
        return False

    else:
        for offset in range(1, group_len):
            if spring_list[i + offset] == '.':
                return False
        #print(i, group_len)
        if (i + group_len) == len(spring_list) or (spring_list[i + group_len] != '#'):
            return True
        return False

def recurse(spring_list, groups, i, group_i, n, m, memo):
    # Base Cases
    #print(i, group_i)
    if (i, group_i) in memo:
        return memo[(i, group_i)]
    if i >= n:
        if group_i == m:
            memo[(i, group_i)] = 1
            return 1
        else:
            memo[(i, group_i)] = 0 
            return 0
    elif group_i == m:
        if '#' in spring_list[i:]:
            memo[(i, group_i)] = 0 
            return 0
        else:
            memo[(i, group_i)] = 1
            return 1
    elif spring_list[i] == '#': # Must be the start of our current group
        if works_for_group(spring_list, i, groups[group_i]):
            memo[(i, group_i)] = recurse(spring_list, groups, (i + groups[group_i] + 1), group_i + 1, n, m, memo)
            return memo[(i, group_i)]
        else:
            memo[(i, group_i)] = 0 
            return 0
    elif spring_list[i] == '.':
        memo[(i, group_i)] = recurse(spring_list, groups, i + 1, group_i, n, m, memo)
        return memo[(i, group_i)]
    else: # ? case
        # Try replacing with '#'
        if works_for_group(spring_list, i, groups[group_i]):
            memo[(i, group_i)] = recurse(spring_list, groups, (i + groups[group_i] + 1), group_i + 1, n, m, memo) + recurse(spring_list, groups, i + 1, group_i, n, m, memo)
            return memo[(i, group_i)]
        else: # Replace with '.' and see if that works 
            memo[(i, group_i)] = recurse(spring_list, groups, i + 1, group_i, n, m, memo)
            return memo[(i, group_i)]

part1_total = 0
for spring_list, groups in zip(spring_lists, groupings):
    memo = {}
    num_args = recurse(spring_list, groups, 0, 0, len(spring_list), len(groups), memo)
    part1_total += num_args
print(f"Part 1's sum of possible arrangements: {part1_total}")
spring_lists = []
groupings = []
for row in records:
    left, right = row.split()
    spring_lists.append('?'.join([left for _ in range(5)]))
    groupings.append([int(x) for _ in range(5) for x in right.split(',')])

part2_total = 0
for spring_list, groups in zip(spring_lists, groupings):
#    print(spring_list)
    memo = {}
    num_args = recurse(spring_list, groups, 0, 0, len(spring_list), len(groups), memo)
#    print(num_args)
#    print("Memo len", len(memo))
    part2_total += num_args
print(f"Part 2's sum of possible arrangements: {part2_total}")
