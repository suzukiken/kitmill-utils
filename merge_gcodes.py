#!/usr/bin/python3

import sys

header = [
	"G21",
	"G61",
	"G90",
	"G00 Z1.0000",
	"G00 X0.0000 Y00.0000",
	"M03",
	"G4 P1",
]

footer = [
	"M05",
]

# find /Users/ken/Downloads/gcode-3 -name '*.ncd' -print0 | xargs -0 python3 /Users/ken/Downloads/kitmill-utils/merge_gcodes.py

def merge_content(file_paths):

    lines = []
    
    for file_path in file_paths:
        picking = False
        with open(file_path, 'r') as f:
            for line in f.readlines():
                striped = line.strip()
                if striped == 'G4 P1':
                    picking = True
                    lines.append("G00 Z1.0000")
                elif striped == 'M05':
                    picking = False
                elif picking:
                    lines.append(striped)

    lines = header + lines + footer
    
    return '\n'.join(lines)

args = sys.argv

print(merge_content(args[1:]))



