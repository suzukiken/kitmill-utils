#!/usr/bin/python3

import re
from decimal import Decimal

x_min = 30.0
x_max = 40.0
y_min = 30.0
y_max = 40.0
z_cut_depth = 2.0
z_move_height = 10.0
z_start_move_height = 10.0
feed_depth = 0.1

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

current_depth = 0.0

code += f'G00 Z{z_move_height:.3f}\n'
code += f'G00 X{x_min:.3f} Y{y_min:.3f}\n'

while current_depth <= z_cut_depth:
	code += f'G01 Z-{current_depth:.3f} F100.000\n'
	code += f'G01 X{x_min:.3f} Y{y_max:.3f} F300.000\n'
	current_depth += feed_depth
	code += f'G01 Z-{current_depth:.3f} F100.000\n'
	code += f'G01 X{x_min:.3f} Y{y_min:.3f} F300.000\n'
	current_depth += feed_depth

#code += f'G00 Z{z_move_height:.3f}\n'
#code += f'G00 X{x_min:.3f} Y{y_min:.3f}\n'

current_depth = 0.0

while current_depth <= z_cut_depth:
	code += f'G01 Z-{current_depth:.3f} F100.000\n'
	code += f'G01 X{x_max:.3f} Y{y_min:.3f} F300.000\n'
	current_depth += feed_depth
	code += f'G01 Z-{current_depth:.3f} F100.000\n'
	code += f'G01 X{x_min:.3f} Y{y_min:.3f} F300.000\n'
	current_depth += feed_depth

line_interval_length = 5.0
line_length = 30.0
line_num = 3

for i in range(line_num):
    x_start = x_min + line_interval_length * i
    x_end = x_start
    y_start = 0
    y_end = line_length
    code += 'G00 Z1.000\n'
    code += f'G00 X{x_start:.3f} Y{y_start:.3f}\n'
    code += 'G01 Z-0.150 F100.000\n'
    code += f'G01 X{x_end:.3f} Y{y_end:.3f} F300.000\n'

for i in range(line_num):
    x_start = 0
    x_end = line_length
    y_start = y_min + line_interval_length * i
    y_end = y_start
    code += 'G00 Z1.000\n'
    code += f'G00 X{x_start:.3f} Y{y_start:.3f}\n'
    code += 'G01 Z-0.150 F100.000\n'
    code += f'G01 X{x_end:.3f} Y{y_end:.3f} F300.000\n'

code += footer

print(code)

