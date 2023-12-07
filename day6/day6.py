with open("day6.txt", "r") as f:
    data = f.read().strip('\n')
time_str, dist_str = data.split('\n')

# Part 1
times = [int(time) for time in time_str.split()[1:]]
dists = [int(dist) for dist in dist_str.split()[1:]]

# Brute force method
counts_product = 1
for time, dist in zip(times, dists):
    count = 0 # Counts number of ways to beat a high score
              # for a given race
    for hold_time in range(0, time + 1):
        speed = hold_time
        dist_gone = speed*(time - hold_time)
        if dist_gone > dist:
            count += 1
    counts_product *= count

print(f"Part 1's Score Product: {counts_product}")

# Part 2:
time = int("".join(time_str.split()[1:]))
dist = int("".join(dist_str.split()[1:]))

def calc_dist(time_held: int) -> int:
    return time_held*(time - time_held)

# Using binary search
half_time = time // 2
left, right = 0, half_time

def bin_search(left, right, time):
    while left < right:
        if right == left + 1:
            if dist < calc_dist(left):
                return left
            else:
                return right
                
        middle = (right + left) // 2
        middle_dist = calc_dist(middle)
        left_dist, right_dist = calc_dist(left), calc_dist(right)   
        
        if dist > middle_dist:
            left = middle
        else:
            right = middle
    return -1
    
index = bin_search(left, right, time)
# There are time + different holding times, so if we 
# subtract 2 times the index of the first distance that
# beats the reference, we will have the count of all possible
# distances that "win" the race
count = time + 1 - (2*index)
print(f"Part 2's Score: {count}")
