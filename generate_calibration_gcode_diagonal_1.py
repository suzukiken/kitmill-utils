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

line_interval_length = 1.0
line_length = 5.0
line_num = 10

for i in range(line_num):
    x_start = line_interval_length * i
    x_end = line_interval_length * i + line_length
    y_start = 0
    y_end = line_length
    code += 'G00 Z1.000\n'
    code += f'G00 X{x_start:.3f} Y{y_start:.3f}\n'
    code += 'G01 Z-0.150 F100.000\n'
    code += f'G01 X{x_end:.3f} Y{y_end:.3f} F300.000\n'

code += footer

print(code)

