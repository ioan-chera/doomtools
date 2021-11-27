import sys

from utils.palette import find_closest_color, get_palette
from utils.texture import Patch


def convert_patch_palette():
    """
    Converts a DOOM patch from a palette to another
    """
    source_patch_path = sys.argv[1]
    source_palette_path = sys.argv[2]
    target_palette_path = sys.argv[3]
    target_patch_path = sys.argv[4]

    source_patch = Patch(path=source_patch_path)
    source_palette = get_palette(source_palette_path)
    target_palette = get_palette(target_palette_path)
    target_patch = Patch(patch=source_patch)

    conversion_cache = {}

    for column in target_patch.columns:
        for post in column.posts:
            for index, value in enumerate(post.data):
                rgb = source_palette[value]
                target_index, _ = find_closest_color(rgb, target_palette, cache=conversion_cache)
                post.data[index] = target_index
    target_patch.save_to_path(target_patch_path)


if __name__ == '__main__':
    convert_patch_palette()
