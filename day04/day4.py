from collections import defaultdict

# Part 1 Solution:

total = 0
with open("day4.txt", "r") as file:
    for line in file:
        card_str, info = line.split(': ')
        winning, yours = info.split(' | ')
        win_nums = {int(num) for num in winning.split()} # Set of winning numbers
        score = 1
        for num in yours.split():
            if int(num) in win_nums:
                score = score << 1 # Multiply by 2 
        total += (score >> 1) # Remove extra factor of 2
print(f'Part 1 Total Score: {total}')

# Part 2 Solution:

card_dict = defaultdict(int) # Default dict simplifies logic when updating nonexistent keys
with open("day4.txt", "r") as file:
    for line in file:
        card_str, info = line.split(': ')
        index = int(card_str.split()[-1])
        card_dict[index] += 1
        num_of_copies = card_dict[index]
        winning, yours = info.split(' | ')
        win_nums = {int(num) for num in winning.split()}
        score = 0
        # Find how many winnning numbers you have for each copy of the current card
        for num in yours.split():
            if int(num) in win_nums:
                score += 1
        # For next 'score' number of entries, win a copy for each copy of the current card
        for i in range(score):
            card_dict[index + i + 1] += num_of_copies
print(f'Part 2 Number of Cards: {sum(card_dict.values())}')
