hailstones = []
with open('day24.txt', 'r') as file:
    for line in file:
        pos_str, vel_str = line.strip('\n').split(' @ ')
        position = tuple(int(coord) for coord in pos_str.split(', '))
        velocity = tuple(int(v_i) for v_i in vel_str.split(', '))
        hailstones.append((position, velocity))

# Looking at the data, none of the hailstones have a 0 component in their velocity vectors
# This means that we don't have to worry about lines parallel to any given axis
# As the constraints form boxes, we don't have to worry about lines intersecting the
# contraints parallel to a given side

min_x, max_x = 7, 27 
min_y, max_y = 7, 27

def crosses_test_area(px, py, pz, vx, vy, vz):
    starts_outside = True
    if min_x <= px and px <= max_x and min_y <= py and py <= max_y:
        starts_outside = False

    # Top
    # Right
    # Bottom
    # Left

def interval_intersect(a_t0, a_t1, b_t0, b_t1):
    if a_t1 < b_t0:
        return False
    elif b_t1 < a_t0:
        return False
    else:
        return True

# Let's only look at the paths (the line segments that could possibly intersect in the area specified)
path_segs = []
for position, velocity in hailstones:
    px, py, pz = position
    vx, vy, vz = velocity


print(path_segs)
intersections = 0

n = len(path_segs)
for i in range(n):
    x1, y1, x2, y2 = path_segs[i]
    for j in range(i + 1, n):
        x3, y3, x4, y4 = path_segs[j]

        denom = ((x1 - x2)*(y3 - y4)) - ((y1 - y2)*(x3 - x4))
        if denom == 0:
            continue
        else:
            num_a = ((x1 - x3)*(y3 - y4)) - ((y1 - y3)*(x3 - x4))
            num_b = ((x1 - x3)*(y1 - y2)) - ((y1 - y3)*(x1 - x2))
            t = num_a / denom
            u = num_b / denom
            if denom < 0:
                if 0 >= num_a and num_a >= denom:
                    if 0 >= num_b and num_b >= denom:
                        print(i, j)
                        print(x1 + t*(x2 - x1), y1 + t*(y2 - y1))
            else:
                if 0 <= num_a and num_a <= denom:
                    if 0 <= num_b and num_b <= denom:
                        print(i, j)
                        print(x1 + t*(x2 - x1), y1 + t*(y2 - y1))

