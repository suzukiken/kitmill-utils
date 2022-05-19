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

line_interval_length = 0.5
line_length = 4.0
line_num = 4
holi_block_num = 3
vart_block_num = 1

x_start = 2
x_end = 2
y_start = 16
y_end = 0

for hi in range(holi_block_num):
    for vi in range(vart_block_num):
        for i in range(line_num):
            x_start -= line_interval_length
            x_end -= line_interval_length
            y_end = y_start - line_length
            code += 'G00 Z1.000\n'
            code += f'G00 X{x_start:.3f} Y{y_start:.3f}\n'
            code += 'G01 Z-0.150 F100.000\n'
            code += f'G01 X{x_end:.3f} Y{y_end:.3f} F300.000\n'
        x_start -= 2
        x_end -= 2
    x_start = 2
    x_end = 2
    y_start -= 6
    y_end -= 6

code += footer

print(code)

