import io
import omg
import sys

from PIL import Image

from utils.palette import get_palette, check_if_colors_are_in_palette
from utils.texture import check_if_flat


def filter_baker():
    """
    Given:
    - a WAD with TX_ textures stored as PNGs;
    - a PLAYPAL extracted lump file;
    produces another WAD where only the textures fitting exactly the palette are kept. Moreover, all 64x64 opaque tex-
    tures are stored as flats.

    Based on my wish to have a vanilla-compatible Baker's Texture Pack for Heretic.
    """
    baker_path = sys.argv[1]
    palette_path = sys.argv[2]
    out_path = sys.argv[3]
    
    palette = get_palette(palette_path)
        
    wad = omg.WAD(baker_path)
    new_wad = omg.WAD()
    for lump_name, lump in wad.ztextures.items():
        image = Image.open(io.BytesIO(lump.data)).convert('RGBA')
        
        colors = image.getcolors()
        if check_if_colors_are_in_palette(colors, palette):
            print(lump_name)
            if check_if_flat(image):
                new_wad.flats[lump_name] = lump.copy()
            else:
                new_wad.patches[lump_name] = lump.copy()
    new_wad.to_file(out_path)


if __name__ == '__main__':
    filter_baker()
