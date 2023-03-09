#!/usr/bin/python3

import re
from decimal import Decimal
import sys

pattern = re.compile(r".*X([-0-9.]+) Y([-0-9.]+).*")

def process_file(filepath, offset_x, offset_y):
    newlines = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            mat = pattern.match(line)
            if mat:
                org_x = mat.group(1)
                org_y = mat.group(2)
                dec_new_x = Decimal(org_x) + Decimal(offset_x)
                dec_new_y = Decimal(org_y) + Decimal(offset_y)
                new_x = f'{dec_new_x:.3f}'
                new_y = f'{dec_new_y:.3f}'
                newline = line.replace(f'X{org_x}', f'X{new_x}').replace(f'Y{org_y}', f'Y{new_y}')
                newlines.append(newline)
            else:
                newlines.append(line)
    return newlines

def main():
    filepath = sys.argv[1]
    offset_x = sys.argv[2]
    offset_y = sys.argv[3]
    lines = process_file(filepath, offset_x, offset_y)
    print('\n'.join(lines))

if __name__ == '__main__':
    main()