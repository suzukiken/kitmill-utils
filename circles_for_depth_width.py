from decimal import Decimal, ROUND_HALF_EVEN
import math

datas = []
datas.append('(header)')
datas.append('G21G61G90')
datas.append('G00 Z5.000')
datas.append('G00 X0.000 Y0.000')
datas.append('M03')
datas.append('G00 Z1.000')


def land(x=0.0, y=0.0, dia=1.0, dep=0.1, tw=0.8):
    lines = []

    rad = (Decimal(dia) + Decimal(tw)) / 2
    dx = Decimal(x)
    dy = Decimal(y)
    dd = Decimal(dep)
    dx = Decimal(x) - rad
    dy = Decimal(y)

    # move
    lines.append(f'G00 X{dx:.3f} Y{dy:.3f}')
    # down
    lines.append(f'G01 Z-{dd:.3f} F100.000')
    # circle
    lines.append(f'G02 X{dx:.3f} Y{dy:.3f} I{rad:.3f} J0.000 F200.000')
    # up
    lines.append('G00 Z1.000')
    return lines


tool = 0.2

matrix = [
    [  0,  0, 2.0, 0.10, tool],
    [  4,  0, 2.0, 0.10, tool],
    [  8,  0, 2.0, 0.10, tool],
    [ 12,  0, 2.0, 0.10, tool],
    [ 16,  0, 2.0, 0.10, tool],
    [  0,  4, 2.0, 0.15, tool],
    [  4,  4, 2.0, 0.15, tool],
    [  8,  4, 2.0, 0.15, tool],
    [ 12,  4, 2.0, 0.15, tool],
    [ 16,  4, 2.0, 0.15, tool],
    [  0,  8, 2.0, 0.20, tool],
    [  4,  8, 2.0, 0.20, tool],
    [  8,  8, 2.0, 0.20, tool],
    [ 12,  8, 2.0, 0.20, tool],
    [ 16,  8, 2.0, 0.20, tool],
    [  0, 12, 2.0, 0.25, tool],
    [  4, 12, 2.0, 0.25, tool],
    [  8, 12, 2.0, 0.25, tool],
    [ 12, 12, 2.0, 0.25, tool],
    [ 16, 12, 2.0, 0.25, tool],
    [  0, 16, 2.0, 0.30, tool],
    [  4, 16, 2.0, 0.30, tool],
    [  8, 16, 2.0, 0.30, tool],
    [ 12, 16, 2.0, 0.30, tool],
    [ 16, 16, 2.0, 0.30, tool],
]


for hl in matrix:
    datas += land(hl[0], hl[1], hl[2], hl[3], tw=tool)


datas.append('(Footer)')
datas.append('G61')
datas.append('G00 Z5.000')
datas.append('G00 X0.000 Y0.000')
datas.append('M30')

print("\n".join(datas))

