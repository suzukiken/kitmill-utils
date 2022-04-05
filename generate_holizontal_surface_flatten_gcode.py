#!/usr/bin/python3

from datetime import datetime

code = ''
linenum = 100
x_max_mm = 152.000
y_max_mm = 202.000
y_step = 1.3
z_mm = 0.05
f_mm = 200
linenum_step = 10
interpolation_cmd = 'G1'

header = f'''( SufaceFlattener )
( File created: {datetime.now().isoformat()} )
( USBCNC Postprocessor )
( Material Size)
( X= {(x_max_mm + 2):.3f}, Y= {(y_max_mm + 2):.3f}, Z= {z_mm:.3f} )
()
(Toolpaths used in this file:)
(Pocket 1)
(Tools used in this file: Python)
(1 = Pocket {{2 mm}})
'''

linevalues_suffix = [
    'G00Z5.000',
    'G00Z5.000',
    'G00X0.000Y0.000',
    'M09',
    'M30',
]

end = '''%
'''

linevalues_prefix = [
    'G00G21G17G90G40G49',
    'G80',
    ' (Pocket {2 mm})',
    'G00G43Z5.000H1',
    'S18000M03',
    '(Toolpath:- SufaceFlattener 1)',
    '()',
    'G94',
    f'X0.000Y0.000F{f_mm:.1f}',
    'G00X0.000Y0.000Z5.000',
    f'G1Z-{z_mm:.3f}F50.0',
    f'G1X{x_max_mm:.3f}F{f_mm:.1f}',
]

code += header

for value in linevalues_prefix:
    code += f'N{linenum}{value}\n'
    linenum += linenum_step

y_current = y_step
x_toggle = False

while True:
    if (y_max_mm + y_step) < y_current:
        break
    code += f'N{linenum}{interpolation_cmd}Y{y_current:.3f}\n'
    linenum += linenum_step
    if x_toggle:
        x_current = x_max_mm
        x_toggle = False
    else:
        x_current = 0
        x_toggle = True
    code += f'N{linenum}{interpolation_cmd}X{x_current:.3f}\n'
    linenum += linenum_step
    y_current += y_step

for value in linevalues_suffix:
    code += f'N{linenum}{value}\n'
    linenum += linenum_step

code += end

print(code)

