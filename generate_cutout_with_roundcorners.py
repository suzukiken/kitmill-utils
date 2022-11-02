import math
from decimal import Decimal, setcontext, getcontext, Context, ROUND_HALF_EVEN, ROUND_HALF_DOWN
from string import Template

'''
G21
G90
G94
F3.00
G00 Z1.0000
M03
G4 P1
G00 X0.0000Y2.0000
G01 Z-0.2000
G01 X0.1743Y1.9924
....
G01 X-0.1743Y1.9924
G00 X-0.1743Y1.9924
G00 Z1.0000
G00 X0Y0
M05
'''

header = '''G21
G90
G94
F3.00
G00 Z1.0000
M03
G4 P1
G00 X${x_posi}Y${y_posi}
'''

footer = '''
G00 X${x_posi}Y${y_posi}
G00 Z1.0000
G00 X0Y0
M05'''


def corner(start_deg, end_deg, start_x, start_y, radius, tool_width):
	codes = []
	for deg in range(start_deg, end_deg, -3):
		sinval = math.sin(math.radians(deg))
		sindec = (Decimal(sinval) * Decimal(radius + tool_width / 2) + Decimal(start_x)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		cosval = math.cos(math.radians(deg))
		cosdec = (Decimal(cosval) * Decimal(radius + tool_width / 2) + Decimal(start_y)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		codes.append(f'G01 X{sindec}Y{cosdec}')
	return '\n'.join(codes)

def tab(center_x, center_y, angle, depth, tab_width):
	codes = []
	cent_x = (Decimal(center_x)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	cent_y = (Decimal(center_y)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	if angle == 0 or angle == 180:
		start_x = (Decimal(center_x - tab_width / 2)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		end_x = (Decimal(center_x + tab_width / 2)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		if angle == 0:
			codes.append(f'G01 X{start_x}Y{cent_y}')
			codes.append(f'G01 Z1.0000')
			codes.append(f'G01 X{end_x}Y{cent_y}')
			codes.append(f'G01 Z{depth}')
		else:
			codes.append(f'G01 X{end_x}Y{cent_y}')
			codes.append(f'G01 Z1.0000')
			codes.append(f'G01 X{start_x}Y{cent_y}')
			codes.append(f'G01 Z{depth}')
	else:
		start_y = (Decimal(center_y - tab_width / 2)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		end_y = (Decimal(center_y + tab_width / 2)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		if angle == 90:
			codes.append(f'G01 X{cent_x}Y{start_y}')
			codes.append(f'G01 Z1.0000')
			codes.append(f'G01 X{cent_x}Y{end_y}')
			codes.append(f'G01 Z{depth}')
		else:
			codes.append(f'G01 X{cent_x}Y{end_y}')
			codes.append(f'G01 Z1.0000')
			codes.append(f'G01 X{cent_x}Y{start_y}')
			codes.append(f'G01 Z{depth}')
	return '\n'.join(codes)

def rect(width, height, radius, depth, tab_width, tool_width, adjustment):
	codes = []
	rad_minus = radius - adjustment
	rad_plus = radius + adjustment
	offset = tool_width / 2
	codes.append(corner(270, 180, rad_minus, rad_minus, radius, tool_width))
	codes.append(tab(width / 2 - offset - adjustment, - offset - adjustment, 0, depth, tab_width))
	codes.append(corner(180, 90, width - rad_plus, rad_minus, radius, tool_width))
	codes.append(tab(width + offset - adjustment, height / 2 - offset - adjustment, 90, depth, tab_width))
	codes.append(corner(90, 0, width - rad_plus, height - rad_plus, radius, tool_width))
	codes.append(tab(width / 2 - offset - adjustment, height + offset - adjustment, 180, depth, tab_width))
	codes.append(corner(360, 270, rad_minus, height - rad_plus, radius, tool_width))
	codes.append(tab(- offset - adjustment, height / 2 - offset - adjustment, 270, depth, tab_width))
	codes.append(position(- tool_width / 2 - adjustment, rad_minus))
	return '\n'.join(codes)
	
def position(x_posi, y_posi):
	fx_posi = (Decimal(x_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	fy_posi = (Decimal(y_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	return f'G01 X{fx_posi}Y{fy_posi}'

def generate(width, height, radius=1.6, tool_width=0.8, depth=1.8, tab_width=1.0, feed_depth=0.2):
	adjustment = 0.1
	start_x = - tool_width / 2 - adjustment
	start_y = radius - adjustment
	sth = Template(header)
	sh = sth.substitute(
		x_posi=(Decimal(start_x)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN),
		y_posi=(Decimal(start_y)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	)
	code = sh
	current_depth = (- Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	codes = []
	code += position(start_x, start_y) + "\n"
	while - depth <= current_depth:
		codes.append(f'G01 Z{current_depth}')
		codes.append(rect(width, height, radius, current_depth, tab_width, tool_width, adjustment))
		current_depth = (Decimal(current_depth) - Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	code += '\n'.join(codes)
	stf = Template(footer)
	sf = stf.substitute(
		x_posi=(Decimal(start_x)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN),
		y_posi=(Decimal(start_y)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	)
	code += sf
	return code


print(generate(102.5, 56))

