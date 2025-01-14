from decimal import Decimal

header_codes = [
    "G21",
    "G61",
    "G90",
    "G94 F300",
    "G00 Z1.0000",
    "G00 X0.0000 Y00.0000",
    "M03",
    "G4 P1",
]

footer_codes = [
    "G00 Z1.0000",
    "G00 X0.0000 Y00.0000",
    "M05",
]


def generate_circle(diameter, left_x, bottom_y, dest_depth, tool_width, h_feed, v_feed):
    lines = []
    lines.append(f'(circle)')
    radius = diameter / 2 + tool_width / 2
    start_x = left_x # center_x - diameter / 2 + tool_width / 2
    start_y = bottom_y + radius
    lines.append(f'G00 X{start_x:.3f} Y{start_y:.3f}')
    lines.append(f'G01 Z{dest_depth:.3f} F100.000')
    lines.append(f'G02 X{start_x:.3f} Y{start_y:.3f} I{radius:.3f} J0.000 F300.000')
    lines.append('G00 Z1.000')
    return lines


left_x = Decimal(0) # 5
bottom_y = Decimal(0) # 40
dest_depth = - Decimal(0.15)
tool_width = Decimal(0.8)
h_step = tool_width / 2
diameter = Decimal(2.0) # 直径

h_feed = Decimal(300)
v_feed = Decimal(100)

codes = []
codes += header_codes
codes += generate_circle(
	diameter=diameter, 
	left_x=left_x, 
	bottom_y=bottom_y, 
	dest_depth=dest_depth, 
	tool_width=tool_width, 
	h_feed=h_feed, 
	v_feed=v_feed
)
codes += footer_codes

print('\n'.join(codes))
