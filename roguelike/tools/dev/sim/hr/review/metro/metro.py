#!/usr/bin/env python3
"""metro.py: review H-A HA-03 (lane HFA, 11-11) — the metronome table of a gauntlet's strikes and the local search used for G2.

    python3 metro.py table <s1> <s2> ...                     best perfect parries per period 2-40 (any start >= T - 200)
    python3 metro.py search <lo> <hi> <seed> <iters> [g2]    local search (G2's cut spacing with g2): fewest periods / starts at 4

The model is fm.c (the shipped F rules); tests/test_metro.py checks the chosen strikes with the real F functions. G2 rows
from strikes: g2rows() (the old A13_SCRIPT's move order and offsets: D -> contact clip + 11, the vanish before D2).
"""
import ctypes
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SO = HERE / 'fm.so'
if not SO.exists():
    subprocess.run(['gcc', '-O2', '-shared', '-fPIC', '-o', str(SO), str(HERE / 'fm.c')], check=True)
_L = ctypes.CDLL(str(SO))


def evaluate(strikes, kmin=8, kmax=30, lo=-200):
    """(worst, {k: (best PP, starts with >= 4, starts with >= 5)})"""
    n, K = len(strikes), kmax - kmin + 1
    a, b, c = (ctypes.c_int * K)(), (ctypes.c_int * K)(), (ctypes.c_int * K)()
    w = _L.eval((ctypes.c_int * n)(*strikes), n, kmin, kmax, lo, a, b, c)
    return w, {kmin + i: (a[i], b[i], c[i]) for i in range(K)}


G2_BASE = [30, 44, 58, 86, 114, 128, 156, 172, 186, 200, 216]
G2_GMIN = [14, 14, 24, 20, 14, 23, 14, 14, 14, 14]


def g2rows(s):
    s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11 = s
    d1, d1b, d2, d4 = s1 - 14, s4 - 14, s5 - 14, s7 - 14
    assert d1 >= 8 and d1b >= s3 + 9 and d2 >= s4 + 7 and d4 >= s6 + 10, (d1, d1b, d2, d4)
    vanish = min(s4 - 3 + 12, d2 - 2)
    return [(0, 'A8.T', 'g_tell', None), (d1, 'D1', 'g_dash', (d1, s1 - 7, s1)), (s1 - 3, 'A8.1', 'g_ring', (s1, s2 - 7, s2)),
            (s2 - 9, 'A8.2', 'g_rise', (s2, s3 - 7, s3)), (s3 - 9, 'A8.3', 'g_leap', None), (d1b, 'D1', 'g_dash', (d1b, s4 - 7, s4)),
            (s4 - 3, 'A8.1', 'g_ring', None), (d2, 'D2', 'g_glide', (d2, s5 - 7, s5)), (s5 - 3, 'A8.4', 'g_sweep', (s5, s6 - 7, s6)),
            (s6 - 6, 'A8.5', 'g_x', None), (d4, 'D4', 'g_run', (d4, s7 - 7, s7)), (s7 - 3, 'A8.6', 'g_wrap', (s7, s8 - 7, s8)),
            (s8 - 3, 'A8.7', 'g_dome', (s8, s9 - 7, s9)), (s9 - 3, 'A8.7', 'g_dome', (s9, s10 - 7, s10)),
            (s10 - 3, 'A8.7', 'g_dome', (s10, s11 - 7, s11)), (s11 - 5, 'A8.8', 'g_vert', None), (236, 'A8.9', 'g_dive', None),
            (242, 'judge', None, None)], vanish


def search(lo, hi, seed, iters, gmin, base):
    rnd = random.Random(seed)

    def cost(s):
        _w, d = evaluate(s, 2, 40)
        c5 = sum(v[2] for v in d.values())
        n4 = sum(1 for k, v in d.items() if 8 <= k <= 30 and v[0] >= 4)
        c4m = sum(v[1] for k, v in d.items() if 8 <= k <= 30)
        c4o = sum(v[1] for k, v in d.items() if not 8 <= k <= 30)
        return 1000 * c5 + 10 * n4 + c4m + 0.2 * c4o + 0.05 * sum(abs(a - b) for a, b in zip(s, base))

    def ok(s):
        return s[0] >= lo and s[-1] <= hi and all(b - a >= g for a, b, g in zip(s, s[1:], gmin))
    best = None
    for r in range(iters):
        cur = list(base) if best is None else [x + (rnd.choice([-4, -3, -2, 2, 3, 4]) if rnd.random() < 0.3 else 0) for x in best[1]]
        if not ok(cur):
            continue
        c = cost(cur)
        while True:
            nb = [s for j in range(len(cur)) for d in (-3, -2, -1, 1, 2, 3) for s in [cur[:j] + [cur[j] + d] + cur[j + 1:]] if ok(s)]
            c2, s2 = min(((cost(s), s) for s in nb), key=lambda x: x[0])
            if c2 >= c:
                break
            c, cur = c2, s2
        if best is None or c < best[0]:
            best = (c, cur)
            print(r, round(c, 2), cur, flush=True)
    return best


if __name__ == '__main__':
    if sys.argv[1] == 'table':
        s = [int(x) for x in sys.argv[2:]]
        _w, d = evaluate(s, 2, 40)
        print(' '.join(f'{k}:{v[0]}' for k, v in d.items()))
        print('starts at 4+ (8-30):', {k: v[1] for k, v in d.items() if 8 <= k <= 30 and v[1]})
    else:
        lo, hi, seed, iters = (int(x) for x in sys.argv[2:6])
        g2 = len(sys.argv) > 6
        search(lo, hi, seed, iters, G2_GMIN if g2 else [14] * 8, G2_BASE if g2 else [30, 46, 64, 94, 110, 138, 164, 180, 196])
