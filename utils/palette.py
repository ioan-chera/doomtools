def get_palette(path):
    """
    Returns the PLAYPAL from path.
    """
    with open(path, 'rb') as f:
        pal_raw = f.read(768)
    palette = []
    for index in range(256):
        rgb = tuple(int(pal_raw[n]) for n in range(3 * index, 3 * index + 3))
        palette.append(rgb)
    return palette


def find_closest_color(rgb, palette):
    """
    Find the closest color
    """
    min_dist = 257 * 257 * 3
    min_index = None

    for index, pal_rgb in enumerate(palette):
        distance = sum((rgb[n] - pal_rgb[n]) ** 2 for n in range(3))
        if distance < min_dist:
            min_dist = distance
            min_index = index

    return min_index, palette[min_index]


def check_if_colors_are_in_palette(colors, palette):
    """
    True if list of colors (as returned by PIL image.getcolors) are in palette. Each color and palette entry must start
    with the same sequence of 3 color components.
    :param colors: list of items returned by image.getcolors
    :param palette: list of triples as read from a PLAYPAL
    :return True if compliant.
    """
    if colors is None:
        return False
    for pair in colors:
        color = pair[1]
        if not color[3]:
            continue
        if len(color) > 3:
            color = color[:3]
        if color not in palette:
            return False
    return True
