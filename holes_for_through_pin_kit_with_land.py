from decimal import Decimal, ROUND_HALF_EVEN
import math

datas = []
datas.append('(header)')
datas.append('G21G61G90')
datas.append('G00 Z5.000')
datas.append('G00 X0.000 Y0.000')
datas.append('M03')
datas.append('G00 Z1.000')

def hole(x=0.0, y=0.0, dia=1.0, dep=2.0, tw=0.8):
    lines = []
    ed = Decimal(0.2)
    sd = Decimal(0.0)
    twd = Decimal(tw)
    rad = (Decimal(dia) - twd) / 2
    ddep = Decimal(dep)
    dx = Decimal(x) - rad
    dy = Decimal(y)
    
    # move
    lines.append(f'G00 X{dx:.3f} Y{dy:.3f}')

    while sd < ddep:
        sd += ed
        # down
        lines.append(f'G01 Z-{sd:.3f} F100.000')
        # circle
        lines.append(f'G02 X{dx:.3f} Y{dy:.3f} I{rad:.3f} J0.000 F300.000')

    # up
    lines.append('G00 Z1.000')
    return lines


def land(x=0.0, y=0.0, dia=1.0, tw=0.8):
    lines = []

    rad = (Decimal(dia) + Decimal(tw)) / 2
    dx = Decimal(x)
    dy = Decimal(y)
    ddep = Decimal(0.1)
    dx = Decimal(x) - rad
    dy = Decimal(y)

    # move
    lines.append(f'G00 X{dx:.3f} Y{dy:.3f}')
    # down
    lines.append(f'G01 Z-{ddep:.3f} F100.000')
    # circle
    lines.append(f'G02 X{dx:.3f} Y{dy:.3f} I{rad:.3f} J0.000 F200.000')
    # up
    lines.append('G00 Z1.000')
    return lines


dep = 2.0
tool = 0.8

matrix_for_8 = [
    # [ x, y, dia]
    [ 0, 0, 0.91, 1.8], # (0.91mmの穴をあける)
    [ 3, 0, 0.91, 1.8],
    [ 6, 0, 0.91, 1.8],
    [ 9, 0, 0.91, 1.8],
    [12, 0, 0.91, 1.8],
    [ 0, 3, 0.92, 1.8], # (0.92mmの穴をあける)
    [ 3, 3, 0.92, 1.8],
    [ 6, 3, 0.92, 1.8],
    [ 9, 3, 0.92, 1.8],
    [12, 3, 0.92, 1.8],
    [ 0, 6, 0.93, 1.8], # (0.93mmの穴をあける)
    [ 3, 6, 0.93, 1.8],
    [ 6, 6, 0.93, 1.8],
    [ 9, 6, 0.93, 1.8],
    [12, 6, 0.93, 1.8],
]

matrix_for_10 = [
    [ 0, 9, 1.11, 2.0], # (1.11mmの穴をあける)
    [ 3, 9, 1.11, 2.0],
    [ 6, 9, 1.11, 2.0],
    [ 9, 9, 1.11, 2.0],
    [12, 9, 1.11, 2.0],
    [ 0,12, 1.12, 2.0], # (1.12mmの穴をあける)
    [ 3,12, 1.12, 2.0],
    [ 6,12, 1.12, 2.0],
    [ 9,12, 1.12, 2.0],
    [12,12, 1.12, 2.0],
    [ 0,15, 1.13, 2.0], # (1.13mmの穴をあける)
    [ 3,15, 1.13, 2.0],
    [ 6,15, 1.13, 2.0],
    [ 9,15, 1.13, 2.0],
    [12,15, 1.13, 2.0],
]

for hl in matrix_for_8:
    datas += land(hl[0], hl[1], hl[3], tw=tool)

for hl in matrix_for_10:
    datas += land(hl[0], hl[1], hl[3], tw=tool)

for hl in matrix_for_8:
    datas += hole(hl[0], hl[1], hl[2], dep=dep, tw=tool)

for hl in matrix_for_10:
    datas += hole(hl[0], hl[1], hl[2], dep=dep, tw=tool)

datas.append('(Footer)')
datas.append('G61')
datas.append('G00 Z5.000')
datas.append('G00 X0.000 Y0.000')
datas.append('M30')

print("\n".join(datas))