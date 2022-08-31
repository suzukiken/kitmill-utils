'''
G01 Z1.0000
G01 X51.5500Y57.6000
G01 Z-1.8000
G01 X2.0000Y57.6000
G01 X1.8744Y57.5967
G01 X1.7491Y57.5869
G01 X1.6246Y57.5705
G01 X1.5010Y57.5476
G01 X1.3788Y57.5182
G01 X1.2584Y57.4825
G01 X1.1399Y57.4406
G01 X1.0238Y57.3925
G01 X0.9104Y57.3384
G01 X0.8000Y57.2785
G01 X0.6929Y57.2128
G01 X0.5893Y57.1416
G01 X0.4896Y57.0652
G01 X0.3941Y56.9835
G01 X0.3029Y56.8971
G01 X0.2165Y56.8059
G01 X0.1348Y56.7104
G01 X0.0584Y56.6107
G01 X-0.0128Y56.5071
G01 X-0.0785Y56.4000
G01 X-0.1384Y56.2896
G01 X-0.1925Y56.1762
G01 X-0.2406Y56.0601
G01 X-0.2825Y55.9416
G01 X-0.3182Y55.8212
G01 X-0.3476Y55.6990
G01 X-0.3705Y55.5754
G01 X-0.3869Y55.4509
G01 X-0.3967Y55.3256
G01 X-0.4000Y29.3000
G01 Z1.0000
G01 X-0.4000Y28.3000
G01 Z-1.8000
G01 X-0.4000Y2.4000
G00 X-0.4000Y2.4000
G00 Z1.0000
G00 X0Y0
M05
'''
import re
import math

minx = 9999999999999
maxx = - 9999999999999
miny = 9999999999999
maxy = - 9999999999999

with open("c.ncd") as f:
	lines = f.readlines()
	for line in lines:
		print(line.strip())
		mat = re.match(r"G01 X([-.0-9]+)Y([-.0-9]+).*", line.strip())
		if mat:
			print(mat.group(1))
			print(mat.group(2))
			if float(mat.group(1)) < minx:
				minx = float(mat.group(1))
			if maxx < float(mat.group(1)):
				maxx = float(mat.group(1))
			if float(mat.group(2)) < miny:
				miny = float(mat.group(2))
			if maxy < float(mat.group(2)):
				maxy = float(mat.group(2))

print(minx)
print(maxx)
print(miny)
print(maxy)

width = abs(maxx - minx)
height = abs(maxy - miny)

print(width)
print(height)


