from string import Template
from json2gcode_hole import generate as hole_generate
from json2gcode_rect_roundcorners import generate as round_corner_rect_generate

header = [
	"G21",
	"G61",
	"G90",
	"G00 Z1.0000",
	"G00 X0.0000 Y00.0000",
	"M03",
	"G4 P1",
]

footer = [
	"M05",
]

code = '\n'.join(header)

code += hole_generate(
	radius=1.75, 
	center_x=7.5, 
	center_y=34, 
	tool_width=3, 
	depth=4.2, 
	feed_depth=0.2, 
	ver_feed_rate=100, 
	holi_feed_rate=300, 
	feed_deg=3)

code += round_corner_rect_generate(
	width=4.8, 
	height=20, 
	radius=2.4, 
	tool_width=3, 
	depth=4.2, 
	feed_depth=0.2)

code += '\n'.join(footer)

print(code)