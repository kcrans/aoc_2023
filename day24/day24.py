import random
import numpy as np

# Part 1 Solution:
hailstones = []
with open('day24.txt', 'r') as file:
    for line in file:
        pos_str, vel_str = line.strip('\n').split(' @ ')
        data = tuple(int(p_or_v) for p_or_v in pos_str.split(', ') + vel_str.split(', '))
        hailstones.append(data)

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
for positions_and_velocities in hailstones:
    px, py, pz, vx, vy, vz = positions_and_velocities
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
# This is a hell of a problem -- look in the containing directory for my notes

num_hailstones = len(hailstones)

# We need to select three random, distinct hailstones
# We know this problem has a solution, so we can just keep on
# sampling until we get a well-determined, full-rank linear matrix equation
while True:
    # Ge [H_i, H_j, H_k]
    selected_hailstones = random.sample(hailstones, k = 3)
    #selected_hailstones = [hailstones[1], hailstones[2], hailstones[3]]

    M = [] # Matrix for our linear system
    b = []

    # We are going to end up with 6 equations in 6 unknowns
    # The first three we get from combining the contraints of S
    # with H_i and H_j. The last through we get from combining the
    # contraints of S with H_j and H_k. The calculations for both are 
    # identical except you replace H_i's data with H_k's.
    for offset in range(2):
        p_xi, p_yi, p_zi, v_xi, v_yi, v_zi = selected_hailstones[0 + offset]
        p_xj, p_yj, p_zj, v_xj, v_yj, v_zj = selected_hailstones[1 + offset]

        M.append([(v_yj - v_yi), (v_xi - v_xj), 0, (p_yi - p_yj), (p_xj - p_xi), 0])
        M.append([0, (v_zj - v_zi), (v_yi - v_yj), 0, (p_zi - p_zj), (p_yj - p_yi)])
        M.append([(v_zj - v_zi), 0, (v_xi - v_xj), (p_zi - p_zj), 0, (p_xj - p_xi)])
        # Now the three values to add to b are:
        b.append((p_yi*v_xi) - (p_xi*v_yi) - ( (p_yj*v_xj) - (p_xj*v_yj) ))
        b.append((p_zi*v_yi) - (p_yi*v_zi) - ( (p_zj*v_yj) - (p_yj*v_zj) ))
        b.append((p_zi*v_xi) - (p_xi*v_zi) - ( (p_zj*v_xj) - (p_xj*v_zj) ))
        # But note that this is just the cross product of
        # (p_xi, p_yi, p_zi, v_xi, v_yi, v_zi) and
        # (p_xj, p_yj, p_zj, v_xj, v_yj, v_ji)
        
    # If M is non-singular, we have found a solution
    M = np.array(M)
    b = np.array(b)

#    print(M)
#    print(b)
    try:
        solution = np.linalg.solve(M, b)
#        print(solution)
        break
    except LinAlgError:
        # M must be singular (Maybe one of the velocity components is shared?)
        continue

print(f"Part 2's sum of rock's X, Y, and Z coordinates: {sum(round(postion) for postion in solution[:3])}")
