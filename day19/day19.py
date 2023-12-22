import copy
with open("day19.txt", "r") as file:
    plain_txt = file.read().strip('\n')
    workflows, parts = plain_txt.split('\n\n')
# Part 1 Solution:
# Let x, m, a, s be represented by the indices 0, 1, 2, 3
convert_cat = {'x': 0, 'm': 1, 'a': 2, 's': 3}

workflows_dict = {}
for workflow in workflows.split('\n'):
    rule_list = []
    name, rules = workflow.split('{')
    rules = rules.strip('\n').strip('}').split(',')
    for rule in rules[:-1]: # The last rule is always the catch-all, and it must be treated separately
        compare = '<' if '<' in rule else '>'
        rating_category, rest = rule.split(compare)
        value, next_workflow = rest.split(':')
        rule_list.append((convert_cat[rating_category], compare, int(value), next_workflow))
    rule_list.append(rules[-1])
    workflows_dict[name] = rule_list

parts_list = []
for part in parts.split('\n'):
    string_ratings = [part_string.split('=') for part_string in part.strip('{}').split(',')]
    ratings = [int(rating) for rating_category, rating in string_ratings]
    parts_list.append(ratings)

total_sum = 0
for part in parts_list:
    workflow_name = 'in' # Always start with this workflow
    while workflow_name != 'A' and workflow_name != 'R':
        workflow = workflows_dict[workflow_name]
        for rating_category, comp_type, value, next_workflow in workflow[:-1]:
            if comp_type == '<':
                if part[rating_category] < value:
                    workflow_name = next_workflow
                    break
            elif comp_type == '>':
                if part[rating_category] > value:
                    workflow_name = next_workflow
                    break
        else:
            # If none of the comparison conditionals were met and we reached the end of the list
            workflow_name = workflow[-1]
    if workflow_name == 'A':
        total_sum += sum(part)
print(f"Part 1 rating numbers total accepted sum: {total_sum}")

# Part 2 Solution:
# Didn't even try the brute-force solution this time...

# Note that each rating for x, m, a, and s can take in values from 1 to 4000.
num_combos = 0

starting_range = [(1, 4000), (1, 4000), (1, 4000), (1, 4000)]
ranges = [(starting_range, 'in')]
while len(ranges) > 0:
    current_range, current_workflow_name = ranges.pop()
    # Reached an acceptance flag, so all values in range are valid
    if current_workflow_name == 'A':
        combos = 1
        for left, right in current_range:
            combos *= (right - left + 1)
        num_combos += combos
    # Reached a rejection flag, so none of the values in the range are vaild 
    elif current_workflow_name == 'R':
        continue
    else:
        workflow = workflows_dict[current_workflow_name]
        # Create a mutable list for keeping track of the ranges 
        # as we move through each step of the workflow
        left_over_range = [[x, y] for x, y in current_range]
        for rating_category, comp_type, value, next_workflow in workflow[:-1]:
            left, right = left_over_range[rating_category]
            # This will be the range which satisfies the given conditional
            # The rest of the range which fails the conditional is stored in left_over_range
            fork_range = [(x, y) for x, y in left_over_range]
            if comp_type == '<':
                fork_range[rating_category] = (left, min(right, value - 1))
                left_over_range[rating_category] = [value, right]
            elif comp_type == '>':
                fork_range[rating_category] = (max(left, value + 1), right)
                left_over_range[rating_category] = [left, value]
            ranges.append((fork_range, next_workflow))
        ranges.append(([(x, y) for x, y in left_over_range], workflow[-1]))
print(f"Part 2 number of distinct combinations which are accepted: {num_combos}")
