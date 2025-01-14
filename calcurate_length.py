"""
python3 calcurate_length.py nc/front.nc
"""

import re
import sys
from decimal import Decimal 
import math

def main(argv):
	print(argv[1])
	with open(argv[1]) as f:
		lines = f.readlines()
		movecount = 0
		total = 0
		curr_x = curr_y = dest_x = dest_y = None
		for line in lines:
			striped_line = line.strip()
			print(f"line {striped_line}")
			mat = re.match(r"G00 X([-.0-9]+)Y([-.0-9]+).*", striped_line)
			if mat:
				curr_x = curr_y = dest_x = dest_y = None
				curr_x = Decimal(mat.group(1))
				curr_y = Decimal(mat.group(2))
				print("---------G00---------")
				print(curr_x)
				print(curr_y)
			# G01 X11.3945Y1.4127
			mat = re.match(r"G01 X([-.0-9]+)Y([-.0-9]+).*", striped_line)
			if mat:
				dest_x = Decimal(mat.group(1))
				dest_y = Decimal(mat.group(2))
				print(dest_x)
				print(dest_y)
				diff_x = dest_x - curr_x
				diff_y = dest_y - curr_y
				print(diff_x)
				print(diff_y)
				length = math.sqrt(diff_x * diff_x + diff_y * diff_y)
				print(length)
				total += length
				curr_x = dest_x
				curr_y = dest_y
				movecount += 1
		print(f"total {total}")
		print(f"movecount {movecount}")


if __name__ == '__main__':
	main(sys.argv)