#!/usr/bin/env python3
"""Where the fx kit's H4 vacuum-blade prop (fx/prop/vblade) draws, in the prop's frame (+x left, +y up, +z = flight),
against the framework blade hit (#pjShape 1: rows 0.9 below and 0.3 above the prop, hr each side across the flight).

    python3 vblade_check.py <worktree roguelike> <resource pack>
"""
import math
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

WT, RP = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(WT / 'tools'))
import build_mboss_bf_fx as K  # noqa: E402

line = (WT / 'data/rlk/function/mboss/butterfly/fx/prop/vblade.mcfunction').read_text().split('\n')[-2]
kind = re.search(r'bf_kit/([a-z_]+)', line).group(1)
tr = re.search(r'transformation:\{translation:\[([^\]]*)\],left_rotation:\[([^\]]*)\],scale:\[([^\]]*)\]', line)
T, Q, S = ([float(v.rstrip('f')) for v in g.split(',')] for g in tr.groups())


def qrot(q, v):
    x, y, z, w = q
    u = np.array([x, y, z])
    return 2 * np.dot(u, v) * u + (w * w - np.dot(u, u)) * v + 2 * w * np.cross(u, v)


plane, (w, h), (a0, a1, b0, b1) = K.KINDS[kind][0], K.KINDS[kind][1], K.KINDS[kind][2]
img = np.asarray(Image.open(RP / f'assets/rlk/textures/mboss/bf_kit/{kind}.png').convert('RGBA')).astype(float) / 255
pts = []
for j in range(h):
    for i in range(w):
        if img[j, i, 3] < 0.1:
            continue
        a = a0 + (i + 0.5) / w * (a1 - a0)
        b = b1 - (j + 0.5) / h * (b1 - b0)
        p = np.array([-a, 0.0, b]) if plane == 'flat' else np.array([-a, b, 0.0])
        pts.append(np.array(T) + qrot(Q, p * np.array(S)))
P = np.array(pts)
lo, hi = P.min(0), P.max(0)
print(f'vblade = {kind}, translation {T}, left_rotation {Q}, scale {S}')
print(f'  across the flight (x): {lo[0]:+.2f} .. {hi[0]:+.2f}   (width {hi[0] - lo[0]:.2f} b; hit: -1.50 .. +1.50 with hr 1.5)')
print(f'  height above the prop (y): {lo[1]:+.2f} .. {hi[1]:+.2f}   (floor = -0.90 when the prop flies 0.9 above it; '
      f'hit rows -0.90 and +0.30)')
print(f'  along the flight (z): {lo[2]:+.2f} .. {hi[2]:+.2f}')
for yy in (-0.9, 0.3, 1.5):
    band = P[np.abs(P[:, 1] - yy) < 0.15]
    if len(band):
        print(f'  at y {yy:+.1f}: x {band[:, 0].min():+.2f} .. {band[:, 0].max():+.2f}')
    else:
        print(f'  at y {yy:+.1f}: nothing drawn')
