import matplotlib.pyplot as plt
import numpy as np

hailstones = []
with open('day24.txt', 'r') as file:
    for line in file:
        pos_str, vel_str = line.strip('\n').split(' @ ')
        position = tuple(int(coord) for coord in pos_str.split(', '))
        velocity = tuple(int(v_i) for v_i in vel_str.split(', '))
        hailstones.append((position, velocity))
# Add the rock throw solution to the list of hailstones
hailstones.append(((24, 13, 10), (-3, 1, 2)))

# Number of steps to take for each hailstone and the rock
time_steps = 10

# Lists to hold the coordinates for each view of the 3d space

points = []

for position, velocity in hailstones:
    px, py, pz = position
    vx, vy, vz = velocity
    x_trajectory = [px]
    y_trajectory = [py]
    z_trajectory = [pz]
    for step in range(time_steps):
        px += vx
        py += vy
        pz += vz
        x_trajectory.append(px)
        y_trajectory.append(py)
        z_trajectory.append(pz)
    x_trajectory = np.array(x_trajectory)
    y_trajectory = np.array(y_trajectory)
    z_trajectory = np.array(z_trajectory)
 
    points.append((x_trajectory, y_trajectory, z_trajectory))


# Set a default line color
default_color = 'black'
default_dot_color = 'dimgray'

# Create subplots
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

n = len(points) - 1
# Plot each set of points for each plane
for i, (x, y, z) in enumerate(points):
    line_color = 'red' if i == n else default_color
    dot_color = 'orange' if i == n else default_dot_color
    # Fit lines through the points for each plane
    m_xy, b_xy = np.polyfit(x, y, 1)
    m_yz, b_yz = np.polyfit(y, z, 1)
    m_xz, b_xz = np.polyfit(x, z, 1)

    # Plot for X-Y plane
    axes[0].scatter(x, y, color=dot_color)
    axes[0].plot(x, m_xy*x + b_xy, color=line_color)

    # Plot for Y-Z plane
    axes[1].scatter(y, z, color=dot_color)
    axes[1].plot(y, m_yz*y + b_yz, color=line_color)

    # Plot for X-Z plane
    axes[2].scatter(x, z, color=dot_color)
    axes[2].plot(x, m_xz*x + b_xz, color=line_color)

# Customize the plots
axes[0].set_xlabel('X-axis')
axes[0].set_ylabel('Y-axis')
axes[0].set_title('X-Y Plane')

axes[1].set_xlabel('Y-axis')
axes[1].set_ylabel('Z-axis')
axes[1].set_title('Y-Z Plane')

axes[2].set_xlabel('X-axis')
axes[2].set_ylabel('Z-axis')
axes[2].set_title('X-Z Plane')

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('Part2ExampleTrajectories.png')

# Show the plots
plt.show()

