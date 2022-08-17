'''
G04 #@! TF.GenerationSoftware,KiCad,Pcbnew,5.1.9+dfsg1-1~bpo10+1*
G04 #@! TF.CreationDate,2022-08-05T22:32:28+00:00*
G04 #@! TF.ProjectId,board,626f6172-642e-46b6-9963-61645f706362,rev?*
G04 #@! TF.SameCoordinates,Original*
G04 #@! TF.FileFunction,Profile,NP*
%FSLAX46Y46*%
G04 Gerber Fmt 4.6, Leading zero omitted, Abs format (unit mm)*
G04 Created by KiCad (PCBNEW 5.1.9+dfsg1-1~bpo10+1) date 2022-08-05 22:32:28*
%MOMM*%
%LPD*%
G01*
G04 APERTURE LIST*
G04 #@! TA.AperFunction,Profile*
%ADD10C,0.100000*%
G04 #@! TD*
G04 APERTURE END LIST*
D10*
X49000000Y-50500000D02*
X49000000Y-103500000D01*
X50500000Y-105000000D02*
X140500000Y-105000000D01*
X142000000Y-103500000D02*
X142000000Y-50500000D01*
X140500000Y-49000000D02*
X50500000Y-49000000D01*
X142000000Y-103500000D02*
G75*
G02*
X140500000Y-105000000I-1500000J0D01*
G01*
X50500000Y-105000000D02*
G75*
G02*
X49000000Y-103500000I0J1500000D01*
G01*
X49000000Y-50500000D02*
G75*
G02*
X50500000Y-49000000I1500000J0D01*
G01*
X142000000Y-50500000D02*
G75*
G03*
X140500000Y-49000000I-1500000J0D01*
G01*
M02*
'''
import re
import math

minx = 9999999999999
maxx = - 9999999999999
miny = 9999999999999
maxy = - 9999999999999

with open("board-Edge_Cuts.gm1") as f:
	lines = f.readlines()
	for line in lines:
		print(line.strip())
		mat = re.match(r"X([-0-9]+)Y([-0-9]+).*", line.strip())
		if mat:
			print(mat.group(1))
			print(mat.group(2))
			if int(mat.group(1)) < minx:
				minx = int(mat.group(1))
			if maxx < int(mat.group(1)):
				maxx = int(mat.group(1))
			if int(mat.group(2)) < miny:
				miny = int(mat.group(2))
			if maxy < int(mat.group(2)):
				maxy = int(mat.group(2))

print(minx)
print(maxx)
print(miny)
print(maxy)

width = abs(maxx - minx)
height = abs(maxy - miny)

print(width)
print(height)


