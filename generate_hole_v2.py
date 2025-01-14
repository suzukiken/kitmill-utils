import math
from decimal import Decimal, setcontext, getcontext, Context, ROUND_HALF_EVEN, ROUND_HALF_DOWN
from string import Template

header = [
    "G21",
    "G90",
    "G94 F500",
    "G00 Z1.0000",
    "G00 X0.0000 Y00.0000",
    "M03",
    "G4 P1",
]

footer = [
    "G00 Z1.0000",
    "G00 X0.0000 Y00.0000",
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
	return f'G01 Z{fz_posi}' # F{f_rate}

# 移動する
def move_to(x_posi, y_posi, feed_rate=None, follow=False):
	fx_posi = (Decimal(x_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	fy_posi = (Decimal(y_posi)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
	if feed_rate:
		f_rate = (Decimal(feed_rate)).quantize(Decimal('0'), rounding=ROUND_HALF_EVEN)
		if follow:
			return f'X{fx_posi} Y{fy_posi}'
		else:
			return f'G01 X{fx_posi} Y{fy_posi}' # F{f_rate}
	else:
		return f'G00 X{fx_posi} Y{fy_posi}'

# 円を描くv2
def generate_circle(diameter, left_x, bottom_y, dest_depth, tool_width, h_feed, v_feed):
    lines = []
    radius = diameter / 2 - tool_width / 2
    start_x = left_x - radius
    start_y = bottom_y
    lines.append(f'G00 X{start_x:.3f} Y{start_y:.3f}')
    lines.append(f'G01 Z{dest_depth:.3f} F{v_feed}')
    lines.append(f'G02 X{start_x:.3f} Y{start_y:.3f} I{radius:.3f} J0.000 F{h_feed}')
    return lines

def generate(radius, center_x, center_y, tool_width, depth, feed_depth, ver_feed_rate, holi_feed_rate, padding_rate):
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
		remainder = radius % (tool_width * padding_rate)
		round_num = math.ceil(radius / (tool_width * padding_rate))
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
			# センターに穴をあけず、padding_rate掛けした刃の幅で並べる
			for num in range(1, round_num + 1):
				actions.append({
					'circle': True,
					'radius': tool_width * padding_rate * num
				})

	for action in actions:
		#print(action)		
		if action['circle']:
			# 開始深さ
			current_depth = (- Decimal(feed_depth)).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
			f_depth = Decimal(feed_depth).quantize(Decimal('.0001'), rounding=ROUND_HALF_EVEN)
			while True:
				# 円を描く
				codes += generate_circle(
					diameter=action['radius'] * 2, 
					left_x=center_x, 
					bottom_y=center_y, 
					dest_depth=current_depth, 
					tool_width=tool_width, 
					h_feed=holi_feed_rate, 
					v_feed=ver_feed_rate
				)
				if current_depth < - depth:
					break
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


code = generate(
	radius=1.9, 
	center_x=0, 
	center_y=0, 
	tool_width=0.5, 
	depth=0.9, 
	feed_depth=0.5, 
	ver_feed_rate=100, 
	holi_feed_rate=500, 
	padding_rate=1
)

print(code)

# radius=2.5 is just for 5mm aluminium bar
# マイクロ超硬エンドミル 刃径2mmシャンク径3.175mm刃長8mm
# マイクロ超硬エンドミル 刃径3mmシャンク径3.175mm刃長9.5mm
# マイクロ超硬エンドミル 刃径1mmシャンク径3.175mm刃長6mm
# 土佐昌典VC 刃径0.8mm刃長3.5mm
# 土佐昌典FT 刃径0.5mm刃長2mm

