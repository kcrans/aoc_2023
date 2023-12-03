# Part 1 Solution:

arr = []
with open("day3.txt", "r") as file:
    for line in file:
        line = line.strip('\n')
        arr.append(list(line))

n = len(arr)
m = len(arr[0])

running_sum = 0
def search_for(i: int, j_0: int, j: int) -> bool:
    """
    Search along the border of a given set of digits
    and return True if any bordering cells are special characters
    other than '.'.
    """
    if i - 1 >= 0:
        for k in range(max(j_0-1, 0), min(j+2, n)):
            if arr[i-1][k] != '.' and not(arr[i-1][k].isdigit()):
                return True
    if i + 1 < m:
        for k in range(max(j_0-1, 0), min(j+2, n)):
            if arr[i+1][k] != '.' and not(arr[i+1][k].isdigit()):
                return True
    if j_0 > 0:
        if arr[i][j_0-1] != '.' and not(arr[i][j_0-1].isdigit()):
            return True
    if j < n - 1:
        if arr[i][j+1] != '.' and not(arr[i][j+1].isdigit()):
            return True
    else:
        return False

# Find all part numbers and add there value to the running sum
# if they border a special character according to the above function.
for i in range(n):
    j = 0
    while j < m:
        if arr[i][j].isdigit():
            num_str = arr[i][j]
            j_0 = j
            j += 1
            while j < m:
                if arr[i][j].isdigit():
                    num_str += arr[i][j]
                    j += 1
                else:
                    break
            if search_for(i, j_0, j-1):
                running_sum += int(num_str)
        j += 1
print(f"Part 1's Part Number Sum: {running_sum}")

# Part 2 Solution:

# Find all part numbers and replace the character digits
# with the integer value of the number
for i in range(n):
    j = 0
    while j < m:
        if arr[i][j].isdigit():
            num_str = arr[i][j]
            j_0 = j
            j += 1
            while j < m:
                if arr[i][j].isdigit():
                    num_str += arr[i][j]
                    j += 1
                else:
                    break
            num = int(num_str)
            for k in range(j_0, j):
                arr[i][k] = num
        j += 1

def check_touch(i: int, j: int) -> list[int]:
    """
    Given a pair of indices, return a list of all bordering
    numbers.
    """
    bordering_nums = []
    for i_0 in range(max(i-1, 0), min(i+2, n)):
        already_seen = False # Makes sure numbers aren't counted multiple times
        for j_0 in range(max(j-1, 0), min(j+2, m)):
            if not already_seen:
                if isinstance(arr[i_0][j_0], int):
                    bordering_nums.append(arr[i_0][j_0])
                    already_seen = True
            if isinstance(arr[i_0][j_0], str):
                # A string, so the number must haved ended
                already_seen = False
    return bordering_nums

ratio_sum = 0
for i in range(n):
    for j in range(m):
        if arr[i][j] == '*':
            bordering_nums = check_touch(i, j)
            if len(bordering_nums) == 2:
                gear_ratio = 1
                for gear in bordering_nums:
                    gear_ratio *= gear
                ratio_sum += gear_ratio
print(f"Part 1's Gear Ratio Sum: {ratio_sum}")
