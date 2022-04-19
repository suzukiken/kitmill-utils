#!/usr/bin/python3

import re
from decimal import Decimal

pattern_ads_line = re.compile(r"%AD(D[0-9]+)R,([0-9.]+)X([0-9.]+)\*%")
pattern_rid_line = re.compile(r"(D[0-9]+)\*")
pattern_plc_line = re.compile(r"X([-0-9]+)Y([-0-9]+)D03\*")
tool_mm = Decimal(0.5)
rdic = {}
places = {}
current_placement_rid = ''

x_max = 0
y_max = 0

header = '''(Header)
G21G61G90
G00Z5.000
G00X0.000Y0.000
M03
'''

footer = '''G00 Z1.000
(Footer)
G61
G00Z5.000
G00X0.000Y0.000
M30
'''

code = ''
code += header

with open('32u2_module-F_Paste.gbr', 'r') as f:
    for line in f.readlines():
        ads_match = pattern_ads_line.match(line)
        rid_match = pattern_rid_line.match(line)
        plc_match = pattern_plc_line.match(line)
        if ads_match:
            rid = ads_match.group(1)
            width = Decimal(ads_match.group(2))
            height = Decimal(ads_match.group(3))
            # decide dot, line or rect
            if width <= tool_mm and height <= tool_mm:
                # dot
                rdic[rid] = {
                    'type': 'dot',
                    'x': 0,
                    'y': 0
                }
            elif width <= tool_mm:
                # line
                rdic[rid] = {
                    'type': 'line',
                    'x': 0,
                    'y': height - tool_mm
                }
            elif height <= tool_mm:
                # line
                rdic[rid] = {
                    'type': 'line',
                    'x': width - tool_mm,
                    'y': 0
                }
            else:
                # rect
                rdic[rid] = {
                    'type': 'rect',
                    'x': width - tool_mm,
                    'y': height - tool_mm
                }
        elif rid_match:
            current_placement_rid = rid_match.group(1)
            places[current_placement_rid] = []
        elif current_placement_rid and plc_match:
            places[current_placement_rid].append([
                Decimal(plc_match.group(1)),
                Decimal(plc_match.group(2))
            ])
        elif line == 'M02*':
            current_placement_rid = ''


def line(x_start, y_start, x_end, y_end):
    code = 'G00 Z1.000\n'
    code += f'G00 X{x_start:.3f} Y{y_start:.3f}\n'
    code += 'G01 Z-0.150 F100.000\n'
    code += f'G01 X{x_end:.3f} Y{y_end:.3f} F300.000\n'
    return code


def rect(x_start, y_start, x_end, y_end):
    code = 'G00 Z1.000\n'
    code += f'G00 X{x_start:.3f} Y{y_start:.3f}\n'
    code += 'G01 Z-0.150 F100.000\n'
    code += f'G01 X{x_end:.3f} Y{y_start:.3f} F300.000\n'
    code += f'G01 X{x_end:.3f} Y{y_end:.3f} F300.000\n'
    code += f'G01 X{x_start:.3f} Y{y_end:.3f} F300.000\n'
    code += f'G01 X{x_start:.3f} Y{y_start:.3f} F300.000\n'
    return code


x_max = 90000000
y_max = -90000000

for rid in places:
    for place in places[rid]:
        x_posi = place[0] - x_max
        y_posi = place[1] - y_max
        x_posi /= 1000000
        y_posi /= 1000000
        if 0 < rdic[rid]['x'] and 0 < rdic[rid]['y']:
            x_start = x_posi - rdic[rid]['x'] / 2
            y_start = y_posi - rdic[rid]['y'] / 2
            x_end = x_posi + rdic[rid]['x'] / 2
            y_end = y_posi + rdic[rid]['y'] / 2
            code += rect(x_start, y_start, x_end, y_end)
        else:
            if 0 < rdic[rid]['x']:
                x_start = x_posi - rdic[rid]['x'] / 2
                x_end = x_posi + rdic[rid]['x'] / 2
            else:
                x_start = x_posi
                x_end = x_posi
            if 0 < rdic[rid]['y']:
                y_start = y_posi - rdic[rid]['y'] / 2
                y_end = y_posi + rdic[rid]['y'] / 2
            else:
                y_start = y_posi
                y_end = y_posi
            code += line(x_start, y_start, x_end, y_end)

code += footer


print(code)

