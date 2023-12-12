# Part 1 and 2 Solution:
# Only difference is the expansion factor for empty rows/columns
with open('day11.txt', 'r') as f:
    rows = [line.strip('\n') for line in f]
def sum_distances(image: list[str], expansion_factor: int) -> int:
    """
    Takes in an "image" of space and returns the sum of the distances
    between unqiue pairs of galaxies. The expansion factor is the factor
    by which empty rows and columns of the image are expanded.
    """
    n, m = len(image), len(image[0])

    # Put the coordinates of all galaxies in a list
    # Will be sorted by the first coordinate (row #)
    galaxies = []
    for i in range(n):
        for j in range(m):
            if image[i][j] == '#':
                galaxies.append((i, j))
    # Store all galaxies with updated x coordinates in an new list
    x_galaxies = [galaxies[0]]
    offset = 0 
    for i in range(1, len(galaxies)):
        cur_galaxy = galaxies[i]
        last_galaxy = galaxies[i-1]
        # Find the number of empty rows between them:
        diff = cur_galaxy[0] - last_galaxy[0] - 1
        if diff >= 1:
            offset += (expansion_factor - 1)*diff
        x_galaxies.append((cur_galaxy[0] + offset, cur_galaxy[1]))

    # Sort list according to second coordinate (col #)
    x_galaxies.sort(key = lambda x : x[1])
    y_galaxies = [x_galaxies[0]]
    offset = 0
    for i in range(1, len(x_galaxies)):
        cur_galaxy = x_galaxies[i]
        last_galaxy = x_galaxies[i-1]
        diff = cur_galaxy[1] - last_galaxy[1] -1
        if diff >= 1:
            offset += (expansion_factor - 1)*diff
        y_galaxies.append((cur_galaxy[0], cur_galaxy[1] + offset))

    total_sum = 0
    for i, galaxy_a in enumerate(y_galaxies):
        for galaxy_b in y_galaxies[i + 1 :]:
            x_a, y_a = galaxy_a
            x_b, y_b = galaxy_b
            total_sum += abs(x_b - x_a) + abs(y_b - y_a)
    return total_sum

print(f"Part 1 Sum of distances: {sum_distances(rows, 2)}")
print(f"Part 2 Sum of distances: {sum_distances(rows, 1000000)}")
