import copy
# Part 1 Solution:
seqs = []
with open('day9.txt', 'r') as file:
    for line in file:
        # Create a list of lists of integers
        seqs.append([int(string) for string in line.strip('\n').split()])

def right_sum(original_seqs):
    seqs = copy.deepcopy(original_seqs)
    great_sum = 0
    for seq in seqs:
        # Find pairwise differences n - 1 times
        for n in range(len(seq) - 1, -1, -1):
            # Store last difference in the nth position
            # Find all differences of differences below index n
            for i in range(n):
                seq[i] = seq[i+1] - seq[i]
        great_sum += sum(seq)
    return great_sum
print(f"Part 1's sum of extrapolated values: {right_sum(seqs)}")

def left_sum(original_seqs):
    seqs = copy.deepcopy(original_seqs)
    great_sum = 0
    for seq in seqs:
        n = len(seq)
        for i in range(n - 1):
            # Start from the end of the list and go down to 1, 2, , ...
            # Store the leftmost difference at index i + 1 (i = 0 is just the first list element)
            for j in range(n-1, i, -1):
                seq[j] = seq[j] - seq[j - 1]
        # Now we have a list of all the leftmost differences
        # So we will iterate starting from the end of the list
        # This time starting with zero we will have to subtract the difference below from the current value
        extrap = 0
        for x in reversed(seq):
            extrap = x - extrap
        great_sum += extrap
    return great_sum
print(f"Part 2's sum of extrapolated values: {left_sum(seqs)}")
print(f"Or just reverse the lists of numbers and feed the result into Part 1's solution: {right_sum([l[::-1 ]for l in seqs])}")
