#!/usr/bin/python3

import re
from decimal import Decimal

pattern = re.compile(r".*X([-0-9.]+) Y([-0-9.]+).*")
x_offset_mm = 0.4
y_offset_mm = 0.4
newlines_front = []
newlines_bottom = []

with open('front.ncd', 'r') as f:
    for line in f.readlines():
        mat = pattern.match(line)
        if mat:
            org_x = mat.group(1)
            org_y = mat.group(2)
            dec_new_x = Decimal(org_x) + Decimal(x_offset_mm)
            dec_new_y = Decimal(org_y) + Decimal(y_offset_mm)
            new_x = f'{dec_new_x:.3f}'
            new_y = f'{dec_new_y:.3f}'
            print(org_x, org_y, new_x, new_y)
            newline = line.replace(org_x, new_x).replace(org_y, new_y)
            newlines_front.append(newline)
        else:
            print(line)
            newlines_front.append(line)

with open('front_offset.ncd', 'w') as f:
    f.writelines(newlines_front)

with open('bottom.ncd', 'r') as f:
    for line in f.readlines():
        mat = pattern.match(line)
        if mat:
            org_x = mat.group(1)
            org_y = mat.group(2)
            dec_new_x = Decimal(org_x) + Decimal(x_offset_mm)
            dec_new_y = Decimal(org_y) + Decimal(y_offset_mm)
            new_x = f'{dec_new_x:.3f}'
            new_y = f'{dec_new_y:.3f}'
            print(org_x, org_y, new_x, new_y)
            newline = line.replace(org_x, new_x).replace(org_y, new_y)
            newlines_bottom.append(newline)
        else:
            print(line)
            newlines_bottom.append(line)

with open('bottom_offset.ncd', 'w') as f:
    f.writelines(newlines_bottom)
