#!/usr/bin/python3

import re
from decimal import Decimal

x_max = 0.0
y_max = 100.0
z_cut_depth = 1.6
z_move_height = 1.0
z_start_move_height = 10.0
tool_width = 3.0
current_depth = 0.0
copper_feed_depth = 0.1
normal_feed_depth = 0.2
tab_width = 0.5
copper_depth = 0.035

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

y_start = 0 + tab_width + tool_width / 2
y_end = y_max - tab_width - tool_width / 2

is_up = True

def cut():
	global is_up, code
	if is_up:
		code += f'G01 X{x_max:.3f} Y{y_end:.3f} F300.000\n'
		is_up = False
	else:
		code += f'G01 X{x_max:.3f} Y{y_start:.3f} F300.000\n'
		is_up = True
	return code

def dig(depth):
	global is_up, code
	code += f'G01 Z-{depth:.3f} F100.000\n'


# copper

while True:
	current_depth += copper_feed_depth
	dig(current_depth)
	cut()
	if copper_depth < current_depth:
		break

# middle

while True:
	if z_cut_depth < current_depth:
		break
	current_depth += normal_feed_depth
	dig(current_depth)
	cut()
		

code += footer

print(code)

