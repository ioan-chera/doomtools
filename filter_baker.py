import io
import omg
import sys

from PIL import Image


def get_palette(path):
    with open(path, 'rb') as f:
        pal_raw = f.read(768)
    palette = []
    for index in range(256):
        rgb = tuple(int(pal_raw[n]) for n in range(3 * index, 3 * index + 3))
        palette.append(rgb)
    return palette
    
    
def check_if_colors_are_in_palette(colors, palette):
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


def check_if_flat(image):
    if image.size != (64, 64):
        return False
    extrema = image.getextrema()
    if extrema[3][0] < 255:
        print("Flat but transparent")
        return False    # flat
    return True
    


def filter_baker():
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
