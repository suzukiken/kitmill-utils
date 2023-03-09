from decimal import Decimal

header_codes = [
    '(Header)',
    'G21G61G90',
    'G00Z5.000',
    'G00X0.000Y00.000',
    'M03',
    'G00Z1.000',
]

footer_codes = [
    '(Footer)',
    'G61',
    'G00Z5.000',
    'G00X0.000Y00.000',
    'M30'
]

def generate_hole(diameter, x, y, d, tool, h_step, v_step, h_feed, v_feed):
    lines = []
    lines.append(f'(hole)')
    sx = x - diameter / 2 + tool / 2
    si = x - sx
    cd = start_depth
    lines.append(f'G00 X{sx:.3f} Y{y:.3f}')
    while d <= cd:
        cx = sx
        ci = si
        lines.append(f'(depth:{cd:.3f})')
        lines.append(f'G01 X{cx:.3f} Y{y:.3f} F300.000')
        lines.append(f'G01 Z{cd:.3f} F100.000')
        while 0 < ci:
            lines.append(f'G01 X{cx:.3f} Y{y:.3f} F300.000')
            lines.append(f'G02 X{cx:.3f} Y{y:.3f} I{ci:.3f} J0.000 F300.000')
            cx += h_step
            ci -= h_step
        cd -= v_step
    lines.append('G00 Z1.000')
    return lines

left_center_x = Decimal(0) # 5
right_center_x = Decimal(35) # 35
center_y = Decimal(0) # 40
start_depth = - Decimal(0.2)
dest_depth = - Decimal(8.6) # 8.6
tool_width = Decimal(3.0)
h_step = tool_width / 2
diameter = Decimal(5.0)

v_step = Decimal(0.2)
h_feed = Decimal(300)
v_feed = Decimal(100)

codes = []
codes += header_codes
codes += generate_hole(diameter=diameter, x=left_center_x, y=center_y, d=dest_depth, tool=tool_width, h_step=h_step, v_step=v_step, h_feed=h_feed, v_feed=v_feed)
codes += footer_codes

print('\n'.join(codes))
