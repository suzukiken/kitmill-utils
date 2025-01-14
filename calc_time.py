import math
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_DOWN

p1 = (100, 200)
p2 = (200, 300)

feed = 300 # 300 mm per minute, 5 mm per second


def distance(p1, p2):
	dx = p2[0] - p1[0]
	dy = p2[1] - p1[1]
	dist = math.sqrt(dx * dx + dy * dy)
	return dist

def movetime(dist, feed):
	mm_per_sec = feed / 60
	return dist / mm_per_sec

print(distance(p1, p2))
print(movetime(distance(p1, p2), feed))