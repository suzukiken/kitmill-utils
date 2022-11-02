import math
from decimal import Decimal, setcontext, getcontext, Context, ROUND_HALF_EVEN, ROUND_HALF_DOWN
from string import Template

'''
G21
G90
G94
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

'''
G21
G61
G90
G00 Z5.000
G00 X0.000 Y00.000
M03

G01 Z-0.150 F100.000
G01 X5.910 Y11.229 F300.000
X6.317 Y11.199
X6.716 Y11.290
G00 Z1.000
G00 X11.561 Y14.173
G01 Z-0.150 F100.000
G01 X11.880 Y13.919 F300.000
X12.260 Y13.769
'''

header = [
	"G21",
	"G61",
	"G90",
	"G00 Z5.0000",
	"00 X0.0000 Y00.0000",
	"M03",
	"G4 P1",
]

footer = [
	"M05",
]

# 上に戻る
def go_up(z_posi):
	fz_posi = (Decimal(z_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	return f'G00 Z{fz_posi}'

# 下に掘る
def go_down(z_posi, feed_rate):
	fz_posi = (Decimal(z_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	f_rate = (Decimal(feed_rate)).quantize(Decimal('0'), rounding=ROUND_HALF_EVEN)
	return f'G01 Z{fz_posi} F{f_rate}'

# 移動する
def move_to(x_posi, y_posi, feed_rate=None, follow=False):
	fx_posi = (Decimal(x_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	fy_posi = (Decimal(y_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	if feed_rate:
		f_rate = (Decimal(feed_rate)).quantize(Decimal('0'), rounding=ROUND_HALF_EVEN)
		if follow:
			return f'X{fx_posi} Y{fy_posi}'
		else:
			return f'G01 X{fx_posi} Y{fy_posi} F{f_rate}'
	else:
		return f'G00 X{fx_posi} Y{fy_posi}'

# 円を描く
def move_round(feed_deg, start_x, start_y, radius, tool_width, feed_rate, current_depth, ver_feed_rate):
	codes = []
	for deg in range(0, 360, feed_deg):
		sinval = math.sin(math.radians(deg))
		sindec = (Decimal(sinval) * Decimal(radius - tool_width / 2) + Decimal(start_x)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		cosval = math.cos(math.radians(deg))
		cosdec = (Decimal(cosval) * Decimal(radius - tool_width / 2) + Decimal(start_y)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
		if deg == 0:
			# 開始点
			codes.append(move_to(sindec, cosdec))
			# 掘る
			codes.append(go_down(current_depth, ver_feed_rate))
			codes.append(move_to(sindec, cosdec, feed_rate))
		else:
			codes.append(move_to(sindec, cosdec, feed_rate, True))
	return codes

def generate(radius, center_x, center_y, tool_width, depth, feed_depth, ver_feed_rate, holi_feed_rate, feed_deg):
	codes = header

	# 穴全体を、輪郭だけでなく、あけるために、必要なら径を変えて周回する。その径の配列
	actions = []

	# 何個刃が入るか 10%の重なりで
	if (radius * 2) == tool_width:
		#print(1)
		# センターに穴を開けておしまい
		actions.append({
			'circle': False,
			'radius': None
		})
	elif radius <= tool_width:
		#print(2)
		# 1週回っておしまい
		actions.append({
			'circle': True,
			'radius': radius
		})
	else:
		remainder = radius % (tool_width * 0.8)
		round_num = math.ceil(radius / (tool_width * 0.8))
		if remainder:
			#print(3, round_num)
			# 割り切れない場合、当分する
			for num in range(1, round_num):
				actions.append({
					'circle': True,
					'radius': float(Decimal(radius / round_num * num).quantize(Decimal('.1'), rounding=ROUND_HALF_EVEN))
				})
			actions.append({
				'circle': True,
				'radius': radius
			})
		else:
			#print(4, round_num)
			# 割り切れるなら
			# センターに穴をあけず、0.8掛けした刃の幅で並べる
			for num in range(1, round_num + 1):
				actions.append({
					'circle': True,
					'radius': tool_width * 0.8 * num
				})

	for action in actions:
		#print(action)		
		if action['circle']:
			# 開始深さ
			current_depth = (- Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
			f_depth = Decimal(feed_depth).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
			while - depth <= current_depth:
				# 円を描く
				codes += move_round(feed_deg, center_x, center_y, action['radius'], tool_width, holi_feed_rate, current_depth, ver_feed_rate)
				# もう１段深くする
				current_depth -= f_depth
			codes.append(go_up(1))
		else:
			# 開始点
			codes.append(move_to(center_x, center_y))
			codes.append(go_down(- depth, ver_feed_rate))
			codes.append(go_up(1))

	codes.append(move_to(0, 0))
	codes += footer
	return "\n".join(codes)


code = generate(radius=2, center_x=2.5, center_y=0, tool_width=4, depth=5, feed_depth=0.2, ver_feed_rate=100, holi_feed_rate=300, feed_deg=3)
print(code)
