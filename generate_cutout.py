#!/usr/bin/python3

import re
from decimal import Decimal

x_max = 145.0
y_max = 102.0
tab_num = 3
tab_mm = 0.8
z_cut_depth = 2.0
z_move_height = 1.0
z_start_move_height = 10.0
tool_width = 2.0
feed_depth = 0.05
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
x_posi = x_max + tool_width / 2

y_mm = (y_max - tab_mm * (tab_num - 1)) / tab_num

while current_depth <= z_cut_depth:
	for i in range(tab_num):
		y_start_posi = (y_mm + tab_mm) * i
		y_end_posi = y_start_posi + y_mm
		code += f'G00 Z{z_move_height:.3f}\n'
		code += f'G00 X{x_posi:.3f} Y{y_start_posi:.3f}\n'
		code += f'G01 Z-{current_depth:.3f} F100.000\n'
		code += f'G01 X{x_posi:.3f} Y{y_end_posi:.3f} F300.000\n'
	current_depth += feed_depth
	for i in range(tab_num):
		y_start_posi = y_max - ((y_mm + tab_mm) * i)
		y_end_posi = y_start_posi - y_mm
		code += f'G00 Z{z_move_height:.3f}\n'
		code += f'G00 X{x_posi:.3f} Y{y_start_posi:.3f}\n'
		code += f'G01 Z-{current_depth:.3f} F100.000\n'
		code += f'G01 X{x_posi:.3f} Y{y_end_posi:.3f} F300.000\n'
	current_depth += feed_depth

code += footer

print(code)

