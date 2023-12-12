import math
# Part 1 Solution:

with open('day8.txt', 'r') as file:
    text = file.read()

split_text = text.strip('\n').split('\n')

instructs = split_text[0]

# Turn the network into a dicitonary with source nodes
# as keys and tuples of possible destinations as values
network = {}
for line in split_text[2:]:
    source_str, dest_str = line.split(' = ')
    left, right = dest_str.strip('()').split(', ')
    network[source_str] = (left, right)

# Start at 'AAA' and follow iterations of the instructions
# until you hit 'ZZZ'
current_node = 'AAA'
steps = 0
while current_node != 'ZZZ':
    for move in instructs:
        steps += 1
        next_ops = network[current_node]
        match move:
            case 'L': 
                current_node = next_ops[0]
            case 'R':
                current_node = next_ops[1]
print(f"Part 1's required number of steps: {steps}")

# Part 2 Solution:
starts = list(filter(lambda x : x[-1] == 'A', network.keys()))
cycles = []
# Loop through all starting locations and count how many
# steps it takes to reach a location ending in "Z"
for start in starts:
    steps = 0
    current_node = start
    while current_node[-1] != 'Z':
        for move in instructs:
            steps += 1
            next_ops = network[current_node]
            match move:
                case 'L':
                    current_node = next_ops[0]
                case 'R':
                    current_node = next_ops[1]
    cycles.append(steps)
:wq

print(f"Part 1's required number of steps: {math.lcm(*cycles)}")

