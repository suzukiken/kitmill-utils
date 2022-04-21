#!/usr/bin/python3

import re
from decimal import Decimal

x_max = 145
y_max = 110
z_cut_depth = 0.25
z_move_height = 10
tool_width = 2.0
feed_depth = 0.05
current_depth = 0.0

header = f'''(Header)
G21G61G90
G00Z{z_move_height:.3f}
G00X0.000Y0.000
M03
'''

footer = f'''G00 Z{z_move_height:.3f}
(Footer)
G61
G00Z{z_move_height:.3f}
G00X0.000Y0.000
M30
'''

code = ''
code += header
x_posi = x_max + tool_width / 2

code += f'G00 Z{z_move_height:.3f}\n'
code += f'G00 X{x_posi:.3f} Y{0:.3f}\n'

while current_depth <= z_cut_depth:
	code += f'G01 Z-{current_depth:.3f} F100.000\n'
	code += f'G01 X{x_posi:.3f} Y{y_max:.3f} F300.000\n'
	current_depth += feed_depth
	code += f'G01 Z-{current_depth:.3f} F100.000\n'
	code += f'G01 X{x_posi:.3f} Y{0:.3f} F300.000\n'
	current_depth += feed_depth

code += footer

print(code)

