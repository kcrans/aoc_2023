from collections import defaultdict

# Part 1 Solution:

# Read data and turn into a dictionary
# with hands as keys as bids as values
hands = {}
with open("day7.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        hand, bid = line.split()
        hands[hand] = int(bid)

# Card strings in descending order (rank)
valid_chars = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
n = len(valid_chars)
# Dictionary that associates a point value for each card
# Higher points imply better cards
translate = {valid_chars[i]: n - i for i in range(n)}

def type_of(hand: str) -> int:
    """
    Takes in a hand and returns its type as an int
    Five of a kind ->  7
    Four of a kind ->  6
    Full house ->      5
    Three of a kind -> 4
    Two pair ->        3
    One pair ->        2
    High card ->       1
    """
    char_dict = defaultdict(int)
    for char in hand:
        char_dict[char] += 1
    # One unique card, must be five of a kind
    if len(char_dict) == 1:
        return 7
    # Two unique cards
    elif len(char_dict) == 2:
        # One card appears 4 times <=> One card appears 1 time
        # So must be four of a kind
        # Trick: I use 'char' which was the last value of the for loop
        if char_dict[char] == 4 or char_dict[char] == 1:
            return 6
        # Otherwise one appears 3 and the other 2 times
        # So it will be a full house
        else:
            return 5
    # Three unique cards
    elif len(char_dict) == 3:
        vals = char_dict.values()
        # If one card appears 3 times, other 2 appear once each
        # This is three of a kind
        if 3 in vals:
            return 4
        # Otherwise two cards appear twice and one appears once
        # Which leaves us with a two pair
        else:
            return 3
    # If there are 4 unique cards, one card appears twice
    # So we have a one pair
    elif len(char_dict) == 4:
        return 2
    # Otherwise all cards are unique
    # Which we call a high card
    else:
        return 1

# Let's turn each hand into a list where the most signficant entry
# is the hand type, and the other entries in order are the translated
# card scores. When Python sorts this lexicographically we should
# get the correct order. The end of the list stores the hand's key.
encodings = []
for hand in hands.keys():
    encodings.append([type_of(hand)] + [translate[char] for char in hand] + [hand])
encodings.sort()

# Loop through all hand encodings in order and
# sum up the hands ranking multiplied with its bid
total_win = sum([hands[hand[-1]]*(i+1) for i, hand in enumerate(encodings)])
print(f"Part 1's total winnings: {total_win}")

# Part 2 Solution:
# Pretty similar to Part 1, only a few changes needed.
# I did get hung up a few bugs though

# Make J cards ranked the lowest:
valid_chars = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
translate = {valid_chars[i]: n - i for i in range(n)}

def type_of(hand: str) -> int:
    char_dict = defaultdict(int)
    for char in hand:
        char_dict[char] += 1

    # Check if a J card appears in the hand and if so
    # give all its occurences to whichever other card
    # appears most often (and remove all Js)
    if 'J' in char_dict and char_dict['J'] < 5:
        J_count = char_dict.pop('J')
        most_freq = max(char_dict, key = char_dict.get)
        char_dict[most_freq] += J_count

    if len(char_dict) == 1:
        return 7
    elif len(char_dict) == 2:
        # Explicitly look for a 4 in the counts as char could
        # be a 'J' so the previous method will not work
        vals = char_dict.values()
        if 4 in vals:
            return 6
        else:
            return 5
    elif len(char_dict) == 3:
        vals = char_dict.values()
        if 3 in vals:
            return 4
        else:
            return 3
    elif len(char_dict) == 4:
        return 2
    else:
        return 1

encodings = [[type_of(hand)] + [translate[char] for char in hand] + [hand] for hand in hands]
encodings.sort()

total_win = sum([hands[hand[-1]]*(i+1) for i, hand in enumerate(encodings)])
print(f"Part 2's total winnings: {total_win}")

from collections import Counter
order = 'J23456789TQKA'

L = [line.split() for line in open('day7.txt')]
L.sort(key=lambda x: [order.index(c) for c in x[0]])
L.sort(key=lambda x: max(sorted(Counter(x[0].replace('J', o)).values())[::-1] for o in order))

print(f'Improved solution found on Reddit: {sum(i * int(bid) for i, (_, bid) in enumerate(L, start=1))}')
