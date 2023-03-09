import math
from decimal import Decimal, setcontext, getcontext, Context, ROUND_HALF_EVEN, ROUND_HALF_DOWN
from string import Template

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


# 円を描く
def move_round(feed_deg, start_x, start_y, radius, tool_width, h_feed, v_feed, dest_depth):
	codes = []
	for deg in range(0, 360+feed_deg, feed_deg):
		sinval = math.sin(math.radians(deg))
		sindec = (Decimal(sinval) * Decimal(radius + tool_width / 2) + Decimal(start_x)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		cosval = math.cos(math.radians(deg))
		cosdec = (Decimal(cosval) * Decimal(radius + tool_width / 2) + Decimal(start_y)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		fx_posi = (Decimal(sindec)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		fy_posi = (Decimal(cosdec)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		if deg == 0:
			# 開始点
			codes.append(f'G00 X{fx_posi:.3f} Y{fy_posi:.3f}')
			# 掘る
			codes.append(f'G01 Z{dest_depth:.3f} F{v_feed:.3f}')
			codes.append(f'G01 X{fx_posi:.3f} Y{fy_posi:.3f} F{h_feed:.3f}')
		else:
			codes.append(f'G01 X{fx_posi:.3f} Y{fy_posi:.3f} F{h_feed:.3f}')
	return codes


def generate_circle(diameter, left_x, bottom_y, dest_depth, tool_width, h_feed, v_feed, feed_deg):
    lines = []
    lines.append(f'(circle)')
    radius = diameter / 2
    start_x = left_x + radius + tool_width / 2 # center_x - diameter / 2 + tool_width / 2
    start_y = bottom_y + radius + tool_width / 2
    lines += move_round(feed_deg, start_x, start_y, radius, tool_width, h_feed, v_feed, dest_depth)
    lines.append('G00 Z1.000')
    return lines


left_x = Decimal(0) # 5
bottom_y = Decimal(0) # 40
dest_depth = - Decimal(0.15)
tool_width = Decimal(0.8)
h_step = tool_width / 2
diameter = Decimal(2.0) # 直径
feed_deg = 10

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
	v_feed=v_feed,
	feed_deg=feed_deg
)
codes += footer_codes

print('\n'.join(codes))
