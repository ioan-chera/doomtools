import struct

from copy import deepcopy
from PIL import Image


class Post:
    def __init__(self):
        self.offset = 0
        self.data = []

    def get_storage_size(self):
        return 4 + len(self.data)

    def get_serializable_data(self):
        return struct.pack('BBB', self.offset, len(self.data), 0) + bytes(self.data + [0])


class Column:
    def __init__(self):
        self.posts = []

    def get_storage_size(self):
        return sum(post.get_storage_size() for post in self.posts) + 1


class Patch:
    """
    Doom patch
    """
    def __init__(self, path=None, patch=None):
        self.width = 0
        self.height = 0
        self.x_offset = 0
        self.y_offset = 0
        self.columns = []

        if path is not None:
            self.load_from_path(path)
        elif patch is not None:
            self.copy_from_patch(patch)

    def load_from_path(self, path):
        header_size = 8

        with open(path, 'rb') as f:
            raw = f.read()
        self.width, self.height, self.x_offset, self.y_offset = struct.unpack('HHhh', raw[:header_size])
        column_offsets = []
        for index in range(self.width):
            column_offsets.append(struct.unpack('I', raw[header_size + 4 * index:header_size + 4 * index + 4])[0])

        self.columns = []
        for offset in column_offsets:
            column = Column()
            pos = offset
            while True:
                topdelta = raw[pos]
                pos += 1
                if topdelta == 0xff:
                    break
                post = Post()
                post.offset = topdelta
                length = raw[pos]
                pos += 2
                post.data = list(raw[pos:pos + length])
                pos += length + 1
                column.posts.append(post)
            self.columns.append(column)

    def save_to_path(self, path):
        with open(path, 'wb') as f:
            f.write(struct.pack('HHhh', self.width, self.height, self.x_offset, self.y_offset))
            address = 8
            for column in self.columns:
                f.write(struct.pack('I', address))
                address += column.get_storage_size()
            for column in self.columns:
                for post in column.posts:
                    f.write(post.get_serializable_data())
                f.write(bytes([0xff]))

    def copy_from_patch(self, patch):
        self.width = patch.width
        self.height = patch.height
        self.x_offset = patch.x_offset
        self.y_offset = patch.y_offset
        self.columns = deepcopy(patch.columns)


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
        return False
    return True
