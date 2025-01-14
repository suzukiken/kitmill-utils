from decimal import Decimal, ROUND_HALF_EVEN
import math

datas = []
datas.append('(header)')
datas.append('G21G61G90')
datas.append('G00 Z5.000')
datas.append('G00 X0.000 Y0.000')
datas.append('M03')
datas.append('G00 Z1.000')


def land(x=0.0, y=0.0, dia=1.0):
    lines = []

    rad = Decimal(dia) / 2
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
    [    0,  0, 0.95, 1.4, 2.0, 2.3],
    [ 2.54,  0, 0.95, 1.4, 2.0, 2.3],
    [ 5.08,  0, 0.95, 1.4, 2.0, 2.3],
    [ 7.62,  0, 0.95, 1.4, 2.0, 2.3],
    [10.16,  0, 0.95, 1.4, 2.0, 2.3],
]


for hl in matrix:
    datas += land(hl[0], hl[1], hl[2])
    datas += land(hl[0], hl[1], hl[3])
    datas += land(hl[0], hl[1], hl[4])
    datas += land(hl[0], hl[1], hl[5])


datas.append('(Footer)')
datas.append('G61')
datas.append('G00 Z5.000')
datas.append('G00 X0.000 Y0.000')
datas.append('M30')

print("\n".join(datas))