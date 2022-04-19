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
                    'x': Decimal(0),
                    'y': Decimal(0)
                }
            elif width <= tool_mm:
                # line
                rdic[rid] = {
                    'type': 'line',
                    'x': Decimal(0),
                    'y': height - tool_mm
                }
            elif height <= tool_mm:
                # line
                rdic[rid] = {
                    'type': 'line',
                    'x': width - tool_mm,
                    'y': Decimal(0)
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

print(rdic)
print(places)