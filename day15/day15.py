with open("day15.txt", "r") as file:
    plaintext = file.read()
    plaintext = plaintext.strip('\n')

steps = plaintext.split(',')

def transform_step(step):
    if '-' in step:
        return step[:-1], -1
    else:
        return step.split('=')

# Part 1 Solution:
def hash(string):
    current_value = 0
    for i, char in enumerate(string):
        current_value += ord(char) # ASCII val of character
        current_value *= 17
        current_value = current_value % 256
    return current_value
    
hash_sum = 0
for step in steps:
    hash_sum += hash(step)
print(f"Part 1's sum of hashing results: {hash_sum}")

# Part 2 Solution:

# List of boxes, each with a list of ordered focal lengths
boxes = [[] for _ in range(256)]
# Dict storing the last time a given label's lens is removed
last_removals = {}
# Dict storing the final focal lengths for each labels' lens
last_updates = {}

n = len(steps)
for i in range(n - 1, -1, -1):
    step = steps[i]
    if '-' in step:
        label = step[:-1]
        # If it's the first time seeing the label:
        if label not in last_removals:
            last_removals[label] = i
    else:
        label, focal_length = step.split('=')
        # The first entry we find for a label will be the
        # final update as we are iterating backwards
        if label not in last_updates:
            last_updates[label] = int(focal_length)

# Go through each step, and add the hast to the respective box
# if either it is the first time seeing the label and there are no
# removal steps for the label in the list or it is the first time
# adding a lense since the last removal. This means all the lenses
# will be in the correct order. Then use the last_updates dictionary
# to give each lense its final focal length value.
for i, step in enumerate(steps):
    if '-' in step:
        pass
    else:
        label, focal_length = step.split('=')
        if label not in last_removals or i > last_removals[label]:
            # i is never >= n, so this label's lense has found its final place
            last_removals[label] = n 
            current_box = boxes[hash(label)]
            current_box.append(last_updates[label])

# Final calculation according to problem statement
# the +1's are to convert the indexing to 1-based
focusing_power = 0
for i, box in enumerate(boxes):
    box_num = i + 1
    for j, focal_len in enumerate(box):
        focusing_power += box_num*(j + 1)*focal_len

print(f"Part 2's resulting focusing power: {focusing_power}")
