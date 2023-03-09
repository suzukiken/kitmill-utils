import math
from decimal import Decimal, setcontext, getcontext, Context, ROUND_HALF_EVEN, ROUND_HALF_DOWN
from string import Template

def corner(start_deg, end_deg, start_x, start_y, radius, tool_width):
	codes = []
	for deg in range(start_deg, end_deg, -3):
		sinval = math.sin(math.radians(deg))
		sindec = (Decimal(sinval) * Decimal(radius + tool_width / 2) + Decimal(start_x)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		cosval = math.cos(math.radians(deg))
		cosdec = (Decimal(cosval) * Decimal(radius + tool_width / 2) + Decimal(start_y)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		codes.append(f'G01 X{sindec}Y{cosdec}')
	return '\n'.join(codes)

def rect(width, height, radius, depth, tool_width, adjustment):
	codes = []
	rad_minus = radius - adjustment
	rad_plus = radius + adjustment
	offset = tool_width / 2
	codes.append(corner(270, 180, rad_minus, rad_minus, radius, tool_width))
	codes.append(corner(180, 90, width - rad_plus, rad_minus, radius, tool_width))
	codes.append(corner(90, 0, width - rad_plus, height - rad_plus, radius, tool_width))
	codes.append(corner(360, 270, rad_minus, height - rad_plus, radius, tool_width))
	codes.append(position(- tool_width / 2 - adjustment, rad_minus))
	return '\n'.join(codes)
	
def position(x_posi, y_posi):
	fx_posi = (Decimal(x_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	fy_posi = (Decimal(y_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	return f'G01 X{fx_posi}Y{fy_posi}'

def generate(width, height, radius=1.6, tool_width=0.8, depth=1.8, feed_depth=0.2):
	adjustment = 0.1
	start_x = - tool_width / 2 - adjustment
	start_y = radius - adjustment
	code = ''
	current_depth = (- Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	codes = []
	code += position(start_x, start_y) + "\n"
	while - depth <= current_depth:
		codes.append(f'G01 Z{current_depth}')
		codes.append(rect(width, height, radius, current_depth, tool_width, adjustment))
		current_depth = (Decimal(current_depth) - Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	code += '\n'.join(codes)
	return code




