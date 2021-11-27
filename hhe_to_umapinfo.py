import sys

HHE_LEVEL_NAME_MAP = {
    "Text 1252 ": "E1M1",
    "Text 1272 ": "E1M2",
    "Text 1292 ": "E1M3",
    "Text 1316 ": "E1M4",
    "Text 1340 ": "E1M5",
    "Text 1360 ": "E1M6",
    "Text 1384 ": "E1M7",
    "Text 1404 ": "E1M8",
    "Text 1424 ": "E1M9",
    "Text 1448 ": "E2M1",
    "Text 1468 ": "E2M2",
    "Text 1492 ": "E2M3",
    "Text 1520 ": "E2M4",
    "Text 1544 ": "E2M5",
    "Text 1568 ": "E2M6",
    "Text 1592 ": "E2M7",
    "Text 1616 ": "E2M8",
    "Text 1644 ": "E2M9",
    "Text 1664 ": "E3M1",
    "Text 1688 ": "E3M2",
    "Text 1708 ": "E3M3",
    "Text 1732 ": "E3M4",
    "Text 1760 ": "E3M5",
    "Text 1788 ": "E3M6",
    "Text 1816 ": "E3M7",
    "Text 1836 ": "E3M8",
    "Text 1860 ": "E3M9",
    "Text 1880 ": "E4M1",
    "Text 1900 ": "E4M2",
    "Text 1920 ": "E4M3",
    "Text 1940 ": "E4M4",
    "Text 1960 ": "E4M5",
    "Text 1980 ": "E4M6",
    "Text 2012 ": "E4M7",
    "Text 2044 ": "E4M8",
    "Text 2068 ": "E4M9",
    "Text 2088 ": "E5M1",
    "Text 2108 ": "E5M2",
    "Text 2124 ": "E5M3",
    "Text 2136 ": "E5M4",
    "Text 2156 ": "E5M5",
    "Text 2172 ": "E5M6",
    "Text 2192 ": "E5M7",
    "Text 2212 ": "E5M8",
    "Text 2240 ": "E5M9",
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
