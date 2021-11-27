import sys

HHE_LEVEL_NAME_MAP = {
    "Text 1252 ": "E1M1"
}


def quoted(string):
    return f'"{string}"'


def get_umapinfo_from_hhe(hhe_path):
    with open(hhe_path) as f:
        hhe = f.readlines()

    umapinfo = {}

    current_map_lump = None
    for line in hhe:
        for string, lump_name in HHE_LEVEL_NAME_MAP.items():
            if line.startswith(string):
                current_map_lump = lump_name
            elif current_map_lump is not None:
                level_name = line.strip()[7:]
                umapinfo.setdefault(current_map_lump, {})["levelname"] = quoted(level_name)
                current_map_lump = None
    return umapinfo


def write_umapinfo_to_file(umapinfo, path):
    with open(path, 'w') as f:
        for lump_name, level_info in umapinfo.items():
            f.write(f"map {lump_name} {{\n")
            for key, value in level_info.items():
                f.write(f"    {key} = {value}\n")
            f.write("}\n\n")


def hhe_to_umapinfo():
    hhe_path = sys.argv[1]
    umapinfo_path = sys.argv[2]
    umapinfo = get_umapinfo_from_hhe(hhe_path)
    write_umapinfo_to_file(umapinfo, umapinfo_path)


if __name__ == '__main__':
    hhe_to_umapinfo()
