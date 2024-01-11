# Part 1 Solution:
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

min_x, max_x = 200000000000000, 400000000000000 
min_y, max_y = 200000000000000, 400000000000000

def crosses_test_area(px, py, pz, vx, vy, vz):
    """
    Takes in a starting position and velocity vector
    Returns the points of intersection if the path crosses the test area twice
    Returns the starting point and point of intersection if the path crosses the test area once
    Returns an empty array if it never crosses the test area
    """
    points = []

    # Top (the line y = max_y)
    t = (max_y - py)/vy
    if t >= 0:
        x_hat = px + t*vx
        if min_x <= x_hat and x_hat <= max_x:
            points.append(x_hat)
            points.append(max_y)
    # Right (the line x = max_x)
    t = (max_x - px)/vx
    if t >= 0:
        y_hat = py + t*vy
        if min_y <= y_hat and y_hat <= max_y:
            points.append(max_x)
            points.append(y_hat)
    
    # Bottom (the line y = min_y)
    t = (min_y - py)/vy
    if t >= 0:
        x_hat = px + t*vx
        if min_x <= x_hat and x_hat <= max_x:
            points.append(x_hat)
            points.append(min_y)
   
    # Left (the line x = min_x)
    t = (min_x - px)/vx
    if t >= 0:
        y_hat = py + t*vy
        if min_y <= y_hat and y_hat <= max_y:
            points.append(min_x)
            points.append(y_hat)
    if len(points) == 2:
        points.append(px)
        points.append(py)
    return points

# Let's only look at the paths (the line segments) that could possibly intersect in the area specified
path_segs = []
for position, velocity in hailstones:
    px, py, pz = position
    vx, vy, vz = velocity
    bounded_pts = crosses_test_area(px, py, pz, vx, vy, vz)
    if len(bounded_pts) == 4:
        path_segs.append(bounded_pts)

intersections = 0

n = len(path_segs)
for i in range(n): # Loop through each pair of line segments
    x1, y1, x2, y2 = path_segs[i]
    for j in range(i + 1, n):
        x3, y3, x4, y4 = path_segs[j]
        # Then perform a test of intersection for line segments
        # It is based off their Bezier form
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
                        intersections += 1
            else:
                if 0 <= num_a and num_a <= denom:
                    if 0 <= num_b and num_b <= denom:
                        intersections += 1
print(f"Part 1 number of intersections in test area: {intersections}")

# Part 2 Solution:
# It's basically a totally different problem!

