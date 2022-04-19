#!/usr/bin/python3

import re
from decimal import Decimal

pattern_adline = re.compile(r"%ADD[0-9]+R,[0-9.]+X[0-9.]+\*%")
shrink_mm = '0.2'
newlines = []

with open('32u2_module-F_Paste.gbr', 'r') as f:
    for line in f.readlines():
        if pattern_adline.match(line):
            orig_width, orig_height = line.strip().replace('*%','').replace('%','').split(',')[1].split('X')
            shrinked_width, shrinked_height = map(lambda v: '{0:f}'.format(Decimal(v) - Decimal(shrink_mm)), (orig_width, orig_height))
            newline = line.replace(orig_width, shrinked_width).replace(orig_height, shrinked_height)
            newlines.append(newline)
        else:
            newlines.append(line)

with open('shrinked.gbr', 'w') as f:
    f.writelines(newlines)
