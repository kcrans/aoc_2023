# Part 1
def first_and_last_p1(line : str) -> int:
    """
    Iterate from left and right of a given string
    and find the first and last digits respectively.
    """
    val = 0
    for char in line:
        if char.isdigit():
            val += 10*int(char) # This digit goes in the 10s place
            break
    for char in line[::-1]:
        if char.isdigit():
            val += int(char)
            break
    return val

running_sum = 0
with open('day1.txt', 'r', encoding = "utf-8") as file:
    for line in file:
        running_sum += first_and_last_p1(line.strip('\n'))
        # Newline character shouldn't really make a difference
print(f'Part 1 sum: {running_sum}')

# Part 2
str_nums =  ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
rev_str_nums = [string[::-1] for string in str_nums] # For reverse search

def check_word(line: str, start: int, length: int, numbers: list) -> int:
    """
    Given a line and a particular starting index, loop through all possible
    word representations of the digits 0-9 and check to see if they start at
    that index in the line. Return int value if found and -1 if none match.
    """
    for i, string in enumerate(numbers):
        len_str = len(string)
        if len_str <= length - start and line[start:start+len_str] == string:
            return i + 1
    return -1
    
def first_num(line : str, numbers : list) -> int:
    """
    Loop through a line and if any character is a digit,
    immediately exit and return the integer value. Otherwise,
    check to see if the character is the beginning of a word
    representation of a digit. If so, return int value of word.
    """
    n = len(line)
    for index, char in enumerate(line):
        if char.isdigit():
            return int(char)
        word_check = check_word(line, index, n, numbers)
        if word_check != -1:
            return word_check
    return 0 # Should never be needed, but included for completeness
    
def first_and_last_p2(line: str) -> int:
    """
    Find the first and last digit in a given string (potentially the same)
    and return the combined two-digit number.
    """
    val = 10*first_num(line, str_nums)
    val += first_num(line[::-1], rev_str_nums)
    return val

running_sum = 0
with open('day1.txt', 'r', encoding = "utf-8") as file:
    for line in file:
        running_sum += first_and_last_p2(line)
print(f'Part 2 sum: {running_sum}')
