#!/usr/bin/python3

header = '''(Header)
G21G61G90
G00Z5.000
G00X0.000Y00.000
M03
'''

circle_1 = '''(circle1)
G00 Z1.000
G00 X1.700 Y3.780
G01 Z-0.150 F100.000
G01 X2.104 Y3.709 F300.000
X2.460 Y3.914
X2.600 Y4.300
X2.460 Y4.686
X2.104 Y4.891
X1.700 Y4.820
X1.436 Y4.505
X1.436 Y4.095
X1.700 Y3.780
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
code += circle_1
code += footer

print(code)

