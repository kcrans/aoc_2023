with open("day5.txt", "r") as f:
    raw_text = f.read().strip('\n')
# Split data into seeds string and the 7 maps:
text_chunks = raw_text.split('\n\n')
# Get all the seeds as ints:
seeds = [int(x) for x in text_chunks[0].split(' ')[1:]]

# Part 1

class RangeT:
    def __init__(self, dest_start: str, sour_start: str, length: str):
        """
        Range class that stores the start of the input range,
        the start of the output range, and the length
        """
        self.dest = int(dest_start)
        self.source = int(sour_start)
        self.length = int(length)
    def contains(self, num: int) -> int:
        """
        Returns the transformed number if
        source <= num <= source + length
        and -1 otherwise
        """
        if self.source <= num and num < self.source + self.length:
            return self.dest + (num - self.source)
        else:
            return -1

# Make a list containing lists of all the ranges
# for each stage of the process
great_arr = []
for text_chunk in text_chunks[1:]:
    ranges = []
    name, range_strings = text_chunk.split(':\n')
    range_strings = range_strings.split('\n')
    for string in range_strings:
        ranges.append(RangeT(*string.split()))
    great_arr.append(ranges)

# Loop over all seeds and for each seed loop
# over all stages and keep track of the smallest
# output seen so far
min_loc_num = None
for seed in seeds:
    val = seed
    for stage in great_arr:
        for trans_range in stage:
            if trans_range.contains(val) >= 0:
                val = trans_range.contains(val)
                break
        # Note that if none of the ranges contained val
        # val stays the same entering into the next stage
    if min_loc_num is None or val < min_loc_num:
        min_loc_num = val
        
print(f"Part 1's Lowest Location Number: {min_loc_num}")

# Part 2:

# Instead of storing a key range (they're ranges now!) as a start and 
# a length, I'm going to store the start and end (closed intervals)

seed_ranges = [(seeds[i], seeds[i] + seeds[i+1] - 1) for i in range(0,len(seeds),2)]
# Also, let's sort the ranges according to their left endpoint
# This will make it easier when mapping the ranges to new ranges
# in a given phase
seed_ranges.sort(key = lambda x : x[0])

# Likewise, let's transform the ranges in each phase
# We will go from (output_start, input_start, length)
# to ((input_start, input_end), offset)
# where offset is output_start - input_start
# i.e. what you add to the input to transition to the ouput

phases = []
for text_chunk in text_chunks[1:]:
    ranges = []
    name, range_strings = text_chunk.split(':\n')
    range_strings = range_strings.split('\n')
    for string in range_strings:
        dest, start, length = string.split()
        dest, start, length = int(dest), int(start), int(length)
        ranges.append(((start, start + length - 1), dest - start))
    # Put the ranges in ascending order
    ranges.sort(key = lambda x : x[0][0])
    phases.append(ranges)

# Now let's see where all the seed ranges end up:
current_ranges = seed_ranges
for phase in phases:
    new_intervals = []
    for interval in current_ranges:
        left, right = interval
        for mapping in phase:
            mleft, mright = mapping[0]
            offset = mapping[1]
            if left < mleft:
                offset = mapping[1]
                if right < mleft:
                    # (    )
                    #         [     ]
                    break
                elif mleft <= right  and right <= mright:
                    # (    )
                    #   [    ]
                    new_intervals.append((left, mleft - 1))
                    new_intervals.append((mleft + offset, right + offset))
                    break
                else:
                    # (            )
                    #     [    ]
                    new_intervals.append((left, mleft - 1))
                    new_intervals.append((mleft + offset, mright + offset))
                    left = mright + 1
            elif left >= mleft and left <= mright:
                if right <= mright:
                    #    (    )
                    # [         ]
                    new_intervals.append((left + offset, right + offset))
                    break
                else:
                    #      (        )
                    #   [       ]
                    new_intervals.append((left + offset, mright + offset))
                    left = mright + 1
            else:
                #           (      )
                # [   ]
                pass
        # If the interval starts beyond the end of the last range
        # or the interval ends before the start of the first range
        if left > mright or right < mleft:
            # Apply the identity transformation
            new_intervals.append((left, right))
    # Sort intervals going into next phase
    new_intervals.sort(key = lambda x: x[0])
    current_ranges = new_intervals
print(f"Part 2's Lowest Location Number: {current_ranges[0][0]}")
