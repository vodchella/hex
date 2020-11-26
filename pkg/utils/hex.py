def get_cube_from_xy(x, y):
    x1 = y - 1
    z1 = x - 1
    y1 = -x1 - z1
    return x1, y1, z1


def get_distance(x1, y1, x2, y2):
    c1 = get_cube_from_xy(x1, y1)
    c2 = get_cube_from_xy(x2, y2)
    return (abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])) / 2
