#!/usr/bin/env python3
"""Measure the Guardian's spear and pelvis in the rig clips used by P5 / P6 / the fail spears
(owner: the P5/P6 pattern author).

    node tools/build_mboss_guardian_rig.mjs --resourcepack <RP> --datapack <scratch dir> --no-paint --debug-dp <DIR>
    git checkout tools/mboss_guardian_rig_manifest.json      # --no-paint rewrites its "textures" field
    python3 tools/mboss_guardian/p56_measure.py <DIR>

It reads the exact per-tick poses the rig generator writes for the offline renderer
(<DIR>/data/rlk/function/gd_dbg/<clip>/<t>.mcfunction) and writes p56_spear.json next to this file:
per clip, per tick, the spear's grip, tip, head (crescent root) and butt, plus the pelvis, in the
anchor frame (blocks; +x = her LEFT, +y up, +z forward; the anchor is the body on the floor at yaw 0,
so a point (x, y, z) is the local coordinate '^x ^y ^z' of 'execute at <body> rotated as <body>
rotated ~ 0'), or null while the rig spear is hidden (scale 0). p56.py puts the climbing cubes,
glints, beams and swing trails on these points, so the fx stay on the blade whatever the clip
does. Re-run both commands when the rig clips change.

Item display maths (vanilla ItemDisplayRenderer): model point v (pixels) is drawn at
Pos + T + L * S * R * Ry180(v / 16 - 0.5); the spear model's grip is the model centre (8, 8, 8),
the tip of the blade y 31.6 px, the crescent root about y 24 px and the butt finial y -1.9 px.
"""
import json
import re
import sys
from pathlib import Path

SPEAR_UUID = '524c4b4d-4247-4400-8000-000000000017'
PELVIS_UUID = '524c4b4d-4247-4400-8000-000000000001'
CLIPS = ('flyslam', 'sweep', 'sweep_e', 'chaos_fail', 'chaos_land', 'chaos_raise', 'chaos_hover', 'idle')
POINTS = {'grip': 8.0, 'tip': 31.6, 'head': 24.0, 'butt': -1.9}        # model y in pixels (x = z = 8)
OUT = Path(__file__).resolve().parent / 'p56_spear.json'


def qrot(q, v):
    x, y, z, w = q
    ix = w * v[0] + y * v[2] - z * v[1]
    iy = w * v[1] + z * v[0] - x * v[2]
    iz = w * v[2] + x * v[1] - y * v[0]
    iw = -x * v[0] - y * v[1] - z * v[2]
    return (ix * w + iw * -x + iy * -z - iz * -y,
            iy * w + iw * -y + iz * -x - ix * -z,
            iz * w + iw * -z + ix * -y - iy * -x)


def floats(s):
    return [float(v.rstrip('f')) for v in s.split(',')]


def pose(line):
    m = re.search(r'translation:\[([^\]]*)\],left_rotation:\[([^\]]*)\],scale:\[([^\]]*)\],right_rotation:\[([^\]]*)\]', line)
    return [floats(g) for g in m.groups()]


def measure(T, L, S, R):
    if max(abs(v) for v in S) < 1e-4:
        return None
    out = {}
    for name, py in POINTS.items():
        v = (0.0, py / 16 - 0.5, 0.0)
        v = qrot(R, v)
        v = (v[0] * S[0], v[1] * S[1], v[2] * S[2])
        v = qrot(L, v)
        out[name] = [round(T[i] + v[i], 3) for i in range(3)]
    return out


def main(dbg):
    base = Path(dbg) / 'data/rlk/function/gd_dbg'
    res = {}
    for clip in CLIPS:
        ticks = sorted(int(p.stem) for p in (base / clip).glob('*.mcfunction'))
        rows = []
        for t in ticks:
            lines = (base / clip / f'{t}.mcfunction').read_text(encoding='utf-8').split('\n')
            sp = measure(*pose(next(l for l in lines if SPEAR_UUID in l)))
            pv = pose(next(l for l in lines if PELVIS_UUID in l))[0]
            if sp is not None:
                sp['pelvis'] = [round(v, 3) for v in pv]
            rows.append(sp if sp is not None else {'pelvis': [round(v, 3) for v in pv]})
        res[clip] = rows
    OUT.write_text(json.dumps(res, separators=(',', ':')) + '\n', encoding='utf-8')
    print(f'wrote {OUT} ({", ".join(f"{c} {len(r)} t" for c, r in res.items())})')


if __name__ == '__main__':
    main(sys.argv[1])
