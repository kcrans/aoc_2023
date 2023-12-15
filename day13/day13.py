with open("day13.txt", "r") as file:
    raw_text = file.read().strip('\n')
patterns = [pattern.split('\n') for pattern in raw_text.split('\n\n')]

# Part 1 Solution:
def is_reflection(pattern, side_a, side_b, end):
    """
    Starting with a given axis of reflection (represented by the two rows or cols on its sides)
    iterate outwards untill either a string is not perfectly reflected or the pattern's edges are reached
    """
    while side_a >= 0 and side_b <= end - 1:
        if pattern[side_a] != pattern[side_b]:
            return False
        side_a -= 1
        side_b += 1
    return True

def part_1(patterns):
    total_sum = 0
    for pattern in patterns:
        n, m = len(pattern), len(pattern[0])
        # Transform the pattern into two lists of strings that let us find
        # vertical and horizontal reflection axes respecitvely
        ver_pattern = [''.join([row[i] for row in pattern]) for i in range(m)]
        hor_pattern = pattern

        axis_found = False # Once an axis is found, we can move on to next pattern
        for location in range(0, m - 1):
            if axis_found:
                break
            elif is_reflection(ver_pattern, location, location + 1, m):
                axis_found = True
                total_sum += location + 1 # Add 1 because of 0-based indexing
        for location in range(0, n - 1):
            if axis_found:
                break
            if is_reflection(hor_pattern, location, location + 1, n):
                if axis_found:
                    break
                total_sum += 100*(location + 1)
    return total_sum

print(f"Part 1's number: {part_1(patterns)}")

def same_or_one_off(str_a, str_b):
    """
    Returns:
    0 if the strings are the same
    1 if there is exactly 1 difference
    -1 if there are 2 or more differences
    """
    diffs = 0
    for char_a, char_b in zip(str_a, str_b):
        if char_a != char_b:
            diffs += 1
    if diffs > 1:
        return -1
    elif diffs == 1:
        return 1
    else:
        return 0

def is_smudged_reflection(pattern, side_a, side_b, end):
    """
    Returns True if there is a reflection about the given axis
    and there is exactly one smudge/flipped char
    """
    num_smudges = 0
    while side_a >= 0 and side_b <= end - 1:
        comparison = same_or_one_off(pattern[side_a], pattern[side_b])
        if comparison == -1 or num_smudges > 1:
            # If strings are sufficiently different or we have already seen a smudge
            return False
        # If strings are the same, nothing is added to the count
        # If there is exactly one difference, increment the count
        num_smudges += comparison 
        side_a -= 1
        side_b += 1
    if num_smudges == 1:
        return True

def part2(patterns):
    total_sum = 0
    for pattern in patterns:
        n, m = len(pattern), len(pattern[0])
        ver_pattern = [''.join([row[i] for row in pattern]) for i in range(m)]
        hor_pattern = pattern

        axis_found = False
        for location in range(0, m - 1):
            if axis_found:
                break
            elif is_smudged_reflection(ver_pattern, location, location + 1, m):
                axis_found = True
                total_sum += location + 1
        for location in range(0, n - 1):
            if axis_found:
                break
            elif is_smudged_reflection(hor_pattern, location, location + 1, n):
                axis_found = True
                total_sum += 100*(location + 1)
    return total_sum
print(f"Part 2's number: {part2(patterns)}")
