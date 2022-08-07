#!/usr/bin/python3

import re
from decimal import Decimal

y_max = 90.0
z_max = 3.30
z_move_height = 1.0
z_start_move_height = 10.0
feed_depth = 0.2
current_depth = 0.0

header = f'''(Header)
G21G61G90
G00Z{z_start_move_height:.3f}
G00X0.000Y0.000
M03
'''

footer = f'''(Footer)
G61
G00Z{z_start_move_height:.3f}
G00X0.000Y0.000
M30
'''

code = ''
code += header

code += f'G00 Z{z_move_height:.3f}\n'
code += f'G00 X{0:.3f} Y{0:.3f}\n'

while current_depth <= z_max:
	code += f'G01 Z-{current_depth:.3f} F100.000\n'
	code += f'G01 X{0:.3f} Y{y_max:.3f} F300.000\n'
	current_depth += feed_depth
	code += f'G01 Z-{current_depth:.3f} F100.000\n'
	code += f'G01 X{0:.3f} Y{0:.3f} F300.000\n'
	current_depth += feed_depth

code += footer

print(code)

