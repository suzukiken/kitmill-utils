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

def merge_content(data_strings):

    lines = []
    
    for data_string in data_strings:
        picking = False
        for line in data_string.splitlines():
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


a = """
G21
G61
G90
G00 Z1.0000
G00 X0.0000 Y00.0000
M03
G4 P1
abc
def
M05
"""

b = """
G21
G61
G90
G00 Z1.0000
G00 X0.0000 Y00.0000
M03
G4 P1
efg
hij
M05
"""

print(merge_content([a, b]))



