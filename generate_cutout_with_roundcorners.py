import math
from decimal import Decimal, setcontext, getcontext, Context, ROUND_HALF_EVEN, ROUND_HALF_DOWN

radius = 2
width = 50
height = 30
feed_depth = 0.2
depth = 1.8

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

def one_surface(width, height, radius):
	codes = []
	codes.append(corner(270, 180, 0, 0, radius))
	codes.append(corner(180, 90, width, 0, radius))
	codes.append(corner(90, 0, width, height, radius))
	codes.append(corner(360, 270, 0, height, radius))
	return '\n'.join(codes)

print(header)

current_depth = (- Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)

while - depth <= current_depth :
	print(f'G01 Z{current_depth}')
	print(one_surface(width, height, radius))
	current_depth = (Decimal(current_depth) - Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)

print(footer)

