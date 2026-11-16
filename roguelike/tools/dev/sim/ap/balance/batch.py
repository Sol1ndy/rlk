#!/usr/bin/env python3
"""batch.py: apfair runs over presets x seeds in parallel processes; one JSON per run in out/<label>/ (plan 12.4).

    python3 batch.py <datapack root> <preset[,preset...]> <label> [jobs]

Presets (plan 9.7 / 12.4):
  gd      the Guardian calibration: Lv4 item-less vs L4 (azfair.fight on the vendored azsim), stand none sword, melee
          walk sword, ranged walk bow0 (physical, as the plan's 160 / 116 / 96 reference), seeds 11 22 33, 3600 t
  apbase  phases 1 and 3 forced (100000 HP), 3600 t each: stand none sword, melee walk sword, ranged walk bow; seeds 1-3
  apdash  phases 1 and 3, melee dash sword + ranged dash bow (the perfect dasher row), seeds 1-3
  appos   phase 1, melee_front / melee_back walk sword (the positional row), seeds 1-3
  apttk   whole fight at real HP: melee walk sword, ranged walk bow, melee walk sword x1.75, seeds 1-3
  aprev   phase 2 (test 20 -> the stage end): plan sword / bow / catalyst (9 seeds: the failure gate), sword x1.75 and bow
          x2.5 (3 seeds: the bands), nearest sword (9 seeds), idle stand (3 seeds)
  apaft   Q2 casts (test 32 then 37) from a seeded spot 10-22 b out: dome / late / early melee walk, 9 seeds
  ap1022  (fix 10-22f) apbase + apdash + appos in one preset: the rows P4 (phase 1) and Q2 (phase 3) feed
  smoke   one short run of each mode
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))

S3, S9 = (1, 2, 3), tuple(range(1, 10))


def R(mode, policy, dodge, agent='plan', char='sword', mult=1.0, n=3600, q2mode='dome', seeds=S3):
    return [dict(mode=mode, policy=policy, dodge=dodge, agent=agent, char=char, mult=mult, n=n, q2mode=q2mode, seed=s)
            for s in seeds]


PRESETS = {
    'gd': R('gd', 'stand', 'none', char='sword', seeds=(11, 22, 33)) + R('gd', 'melee', 'walk', char='sword', seeds=(11, 22, 33))
          + R('gd', 'ranged', 'walk', char='bow0', seeds=(11, 22, 33)),
    'apbase': [r for m in ('p1', 'p3') for r in R(m, 'stand', 'none') + R(m, 'melee', 'walk') + R(m, 'ranged', 'walk', char='bow')],
    'apdash': [r for m in ('p1', 'p3') for r in R(m, 'melee', 'dash') + R(m, 'ranged', 'dash', char='bow')],
    'appos': R('p1', 'melee_front', 'walk') + R('p1', 'melee_back', 'walk'),
    'apttk': R('whole', 'melee', 'walk') + R('whole', 'ranged', 'walk', char='bow') + R('whole', 'melee', 'walk', mult=1.75),
    'aprev': (R('p2', 'melee', 'walk', seeds=S9) + R('p2', 'ranged', 'walk', char='bow', seeds=S9)
              + R('p2', 'ranged', 'walk', char='catalyst', seeds=S9) + R('p2', 'melee', 'walk', mult=1.75)
              + R('p2', 'ranged', 'walk', char='bow', mult=2.5) + R('p2', 'melee', 'walk', agent='nearest', seeds=S9)
              + R('p2', 'stand', 'none', agent='idle')),
    'apaft': [r for q in ('dome', 'late', 'early') for r in R('q2', 'melee', 'walk', n=600, q2mode=q, seeds=S9)],
    # fix 10-22f: the P4 / Q2 related rows again (phases 1 and 3 walkers / dashers and the positional pair)
    'ap1022': [r for m in ('p1', 'p3') for r in R(m, 'stand', 'none') + R(m, 'melee', 'walk') + R(m, 'ranged', 'walk', char='bow')]
              + [r for m in ('p1', 'p3') for r in R(m, 'melee', 'dash') + R(m, 'ranged', 'dash', char='bow')]
              + R('p1', 'melee_front', 'walk') + R('p1', 'melee_back', 'walk'),
    'smoke': R('p1', 'melee', 'walk', n=600, seeds=(1,)) + R('p3', 'melee', 'walk', n=600, seeds=(1,))
             + R('p2', 'melee', 'walk', seeds=(1,)) + R('q2', 'melee', 'walk', n=600, seeds=(1,)),
}


def name_of(r):
    return f'{r["mode"]}_{r["policy"]}_{r["dodge"]}_{r["agent"]}_{r["char"]}_x{r["mult"]}_{r["q2mode"]}_{r["seed"]}'


def one(args):
    dp, r, out = args
    import apfair
    res = apfair.run(Path(dp), **r)
    (Path(out) / (name_of(r) + '.json')).write_text(json.dumps(res, ensure_ascii=False), encoding='utf-8')
    return name_of(r), res['ticks'], res['end']


if __name__ == '__main__':
    dp = sys.argv[1]
    presets = sys.argv[2].split(',')
    label = sys.argv[3]
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else int(os.environ.get('JOBS', '3'))
    out = HERE / 'out' / label
    out.mkdir(parents=True, exist_ok=True)
    runs = [r for p in presets for r in PRESETS[p]]
    runs = [r for r in runs if not (out / (name_of(r) + '.json')).exists() or os.environ.get('REDO')]
    with ProcessPoolExecutor(jobs) as ex:
        for nm, ticks, end in ex.map(one, [(dp, r, str(out)) for r in runs]):
            print(f'{nm:70} {ticks:6} {end}', flush=True)
