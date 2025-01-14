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

matrix = [
    # [ x, y, dia]
    [  0,  0, 0.85, 2.0], # (0.85mmの穴をあける)
    [  5,  0, 0.85, 2.2],
    [ 10,  0, 0.85, 2.4],
    [ 15,  0, 0.85, 2.6],
    [  0,  5, 0.95, 2.0], # (0.95mmの穴をあける)
    [  5,  5, 0.95, 2.2],
    [ 10,  5, 0.95, 2.4],
    [ 15,  5, 0.95, 2.6],
    [  0, 10, 1.20, 3.2], # (1.20mmの穴をあける)
    [  5, 10, 1.20, 3.4],
    [ 10, 10, 1.20, 3.6],
    [ 15, 10, 1.20, 3.8],
]

for hl in matrix:
    datas += land(hl[0], hl[1], hl[3], tw=tool)

for hl in matrix:
    datas += hole(hl[0], hl[1], hl[2], dep=dep, tw=tool)

datas.append('(Footer)')
datas.append('G61')
datas.append('G00 Z5.000')
datas.append('G00 X0.000 Y0.000')
datas.append('M30')

print("\n".join(datas))