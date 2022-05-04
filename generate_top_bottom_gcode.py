#!/usr/bin/python3

header = '''(Header)
G21G61G90
G00Z5.000
G00X0.000Y00.000
M03
'''

footer = '''G00 Z1.000
(Footer)
G61
G00Z5.000
G00X0.000Y00.000
M30
'''

code = ''
code += header

line_interval_length = 5.0
line_length = 20.0
line_num = 5

for i in range(line_num):
    x_start = line_interval_length * i
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
    y_start = line_interval_length * i
    y_end = y_start
    code += 'G00 Z1.000\n'
    code += f'G00 X{x_start:.3f} Y{y_start:.3f}\n'
    code += 'G01 Z-0.150 F100.000\n'
    code += f'G01 X{x_end:.3f} Y{y_end:.3f} F300.000\n'

code += footer

print(code)

with open('front_check_place.ncd', 'w') as f:
    f.writelines(code)

code = ''
code += header

for n in range(line_num):
    for m in range(line_num):
        x_pos = line_interval_length * n
        y_pos = line_interval_length * m
        code += 'G00 Z1.000\n'
        code += f'G00 X{x_pos:.3f} Y{y_pos:.3f}\n'
        code += 'G01 Z-2.000 F100.000\n'

code += footer


with open('bottom_check_place.ncd', 'w') as f:
    f.writelines(code)
