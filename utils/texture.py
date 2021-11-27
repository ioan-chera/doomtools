from PIL import Image


def check_if_flat(image: Image) -> bool:
    """
    Checks if the given PIL image is a vanilla flat (64x64). Textures with transparent pixels are also rejected.
    :param image the PIL image to check.
    :return True if flat.
    """
    if image.size != (64, 64):
        return False
    extrema = image.getextrema()
    if extrema[3][0] < 255:
        print("Flat but transparent")
        return False
    return True