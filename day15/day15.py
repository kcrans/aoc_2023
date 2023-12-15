from collections import defaultdict

with open("day15.txt", "r") as file:
    plaintext = file.read()
    plaintext = plaintext.strip('\n')

lenses_to_remove = defaultdict(int)

steps = plaintext.split(',')
total_sum = 0
for step in steps:
    current_value = 0
    for i, char in enumerate(step):
        if char == '-':
            lenses_to_remove[step[:i]] += 1 
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256
    total_sum += current_value
print(total_sum)

boxes = [[] for _ in range(256)]

for step in steps:
    current_value = 0
    for char in step:
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256
    if '-' in step:
        pass
    else:
        label, focal_length = step.split('=')
        `
        current_box = boxes[current_value]


