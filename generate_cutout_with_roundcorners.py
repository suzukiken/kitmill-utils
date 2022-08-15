import math
from decimal import Decimal, setcontext, getcontext, Context, ROUND_HALF_EVEN, ROUND_HALF_DOWN

radius = 2
width = 50
height = 30
feed_depth = 0.2
depth = 1.8
tab_width = 1.0

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
G00 X0.0000Y2.0000
G01 Z0.0000
'''

footer = '''G01 X0.0000Y2.0000
G00 X0.0000Y2.0000
G00 Z1.0000
G00 X0Y0
M05'''

def corner(start_deg, end_deg, start_x, start_y, radius):
	codes = []
	for deg in range(start_deg, end_deg, -3):
		sinval = math.sin(math.radians(deg))
		sindec = (Decimal(sinval) * Decimal(radius) + Decimal(start_x) + Decimal(radius)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		cosval = math.cos(math.radians(deg))
		cosdec = (Decimal(cosval) * Decimal(radius) + Decimal(start_y) + Decimal(radius)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		codes.append(f'G01 X{sindec}Y{cosdec}')
	return '\n'.join(codes)

def tab(center_x, center_y, angle, depth):
	codes = []
	if angle == 0 or angle == 180:
		start_x = center_x - tab_width / 2
		end_x = center_x + tab_width / 2
		center_y
		if angle == 0:
			codes.append(f'G01 X{start_x}Y{center_y}')
			codes.append(f'G01 Z1.0000')
			codes.append(f'G01 X{end_x}Y{center_y}')
			codes.append(f'G01 Z{depth}')
		else:
			codes.append(f'G01 X{end_x}Y{center_y}')
			codes.append(f'G01 Z1.0000')
			codes.append(f'G01 X{start_x}Y{center_y}')
			codes.append(f'G01 Z{depth}')
	else:
		start_y = center_y - tab_width / 2
		end_y = center_y + tab_width / 2
		if angle == 90:
			codes.append(f'G01 X{center_x}Y{start_y}')
			codes.append(f'G01 Z1.0000')
			codes.append(f'G01 X{center_x}Y{end_y}')
			codes.append(f'G01 Z{depth}')
		else:
			codes.append(f'G01 X{center_x}Y{end_y}')
			codes.append(f'G01 Z1.0000')
			codes.append(f'G01 X{center_x}Y{start_y}')
			codes.append(f'G01 Z{depth}')
	return '\n'.join(codes)

def rect(width, height, radius, depth):
	codes = []
	codes.append(corner(270, 180, 0, 0, radius))
	codes.append(tab(width / 2 + radius, 0, 0, depth))
	codes.append(corner(180, 90, width, 0, radius))
	codes.append(tab(width + radius * 2, height / 2 + radius, 90, depth))
	codes.append(corner(90, 0, width, height, radius))
	codes.append(tab(width / 2 + radius, height + radius * 2, 180, depth))
	codes.append(corner(360, 270, 0, height, radius))
	codes.append(tab(0, height / 2 + radius, 270, depth))
	return '\n'.join(codes)

print(header)

current_depth = (- Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)

while - depth <= current_depth :
	print(f'G01 Z{current_depth}')
	print(rect(width, height, radius, current_depth))
	current_depth = (Decimal(current_depth) - Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)

print(footer)

