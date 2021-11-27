import math
import sys


def get_colors(palette):
    colors = []
    for i in range(256):
        colors.append(tuple(palette[3 * i:3 * i + 3]))
    return colors


def rgb_to_yuv(color):
    """
    https://docs.microsoft.com/en-us/windows/win32/medfound/recommended-8-bit-yuv-formats-for-video-rendering
    """
    R, G, B = color
    Y = ((66 * R + 129 * G + 25 * B + 128) >> 8) + 16
    U = ((-38 * R - 74 * G + 112 * B + 128) >> 8) + 128
    V = ((112 * R - 94 * G - 18 * B + 128) >> 8) + 128
    return Y, U, V


def yuv_to_rgb(color):
    def clip(a):
        return max(0, min(a, 255))

    Y, U, V = color
    C = Y - 16
    D = U - 128
    E = V - 128
    R = clip(round(1.164383 * C + 1.596027 * E))
    G = clip(round(1.164383 * C - (0.391762 * D) - (0.812968 * E)))
    B = clip(round(1.164383 * C + 2.017232 * D))
    return R, G, B


def inverse_luminance(color):
    yuv = rgb_to_yuv(color)
    yuv_inverse = (255 - yuv[0], yuv[1], yuv[2])
    return yuv_to_rgb(yuv_inverse)


def toggled_chrominance(color):
    yuv = rgb_to_yuv(color)
    yuv_toggled = (yuv[0], yuv[2], yuv[1])
    return yuv_to_rgb(yuv_toggled)


def distance2(color1, color2):
    return (color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2


def closest(color, palette):
    mindist = 1e100
    mincol = None
    for index, candidate in enumerate(palette):
        dist = distance2(color, candidate)
        if dist < mindist:
            mindist = dist
            mincol = index
    return mincol


def run_doompal():
    palette_path = sys.argv[1]
    colormap_path = sys.argv[2]
    dest_path = sys.argv[3]
    command = None
    if len(sys.argv) > 4:
        command = sys.argv[4]

    with open(palette_path, 'rb') as f:
        palette_raw = f.read()

    with open(colormap_path, 'rb') as f:
        colormap = f.read()

    colormap_out = list(colormap)

    palette = get_colors(palette_raw)
    for index, color in enumerate(palette):
        if command == 'toggle':
            inv_color = toggled_chrominance(color)
        elif command == 'inverse_toggle':
            inv_color = inverse_luminance(toggled_chrominance(color))
        else:
            inv_color = inverse_luminance(color)
        inv_pos = closest(inv_color, palette)
        colormap_out[32 * 256 + index] = inv_pos

    with open(dest_path, 'wb') as f:
        f.write(bytes(colormap_out))


if __name__ == '__main__':
    run_doompal()
