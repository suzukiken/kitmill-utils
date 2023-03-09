import math
from decimal import Decimal, setcontext, getcontext, Context, ROUND_HALF_EVEN, ROUND_HALF_DOWN
from string import Template

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
			codes.append(move_to(sindec, cosdec, feed_rate))
			# 掘る
			codes.append(go_down(current_depth, ver_feed_rate))
			codes.append(move_to(sindec, cosdec, feed_rate))
		else:
			codes.append(move_to(sindec, cosdec, feed_rate, True))
	return codes

def generate(radius, center_x, center_y, tool_width, depth, feed_depth, ver_feed_rate, holi_feed_rate, feed_deg):
	codes = []
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
	return "\n".join(codes)

