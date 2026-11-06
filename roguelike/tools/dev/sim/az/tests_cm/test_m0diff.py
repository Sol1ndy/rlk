#!/usr/bin/env python3
"""test_m0diff.py: the mid-boss fights and the boss bar against M0, by behaviour (cm.md 15.5; CM fix round, review
findings IDENTITY-1 / IDENTITY-2 / IDENTITY-3).

    python3 test_m0diff.py <datapack root> [--base 22ba247] [--forces 99,1,2,3]

The base is the release the chapter mode merges into: 22ba247 = M0 039b911 + the 10-20 release (telegraph rule on
Guardian / butterfly / fieldgen, fieldgen DMG x1.5); re-pinned from 039b911 at the AZ-CM merge prep. "M0" below = that
base (the framework, plaza and bossui text are M0's, unchanged by the release).

The base commit's datapack (git archive of data/ and tools/mboss_registry.json from S1-CM's worktree, into tests_cm/tmp,
removed afterwards) and the tested tree run the same scenarios in azsim (lib/azsim.py) with the same seed, for every
mid-boss (#mbForce 99 proto, 1 Guardian, 2 butterfly, 3 fieldgen):

 A. fight: 1200 t, a basic strike (25, element cycling) every 6 t. The per-tick trace (player HP, boss HP, live entity
    count, player position, #mbSt, #mbOn) and the damage / dodge / hazard / projectile / rig / line logs are identical.
    The commands executed per tick may grow by at most CMD_BUDGET (the chapter-mode checks a mid-boss tick pays,
    IDENTITY-1: the two #mbMode gates of mboss/world, the one of mboss/bars, the #mbAr check of mv/leash, the proxy /
    RES self-tag tests of combat/apply per hit).
 B. kill (a strike of 60 every 5 t, to the end of the fight), cancel (the body /killed at 200 t, to the end), pause (the
    selection screen 100..160 t, 700 t), reload (mboss/init at 150 t, 700 t): the same per-tick trace, then the end state: every fake-player score of
    the base equal on the tree (scores only on the tree: NEW_FAKE), the live entities identical (type, tags, position)
    with identical scores (objectives only on the tree: NEW_OBJ), storage identical apart from the chapter-mode keys
    (NEW_STORAGE) and the schema-v2 fields of the reg[] / cur records (NEW_REC).
 C. bossui/draw (mcsim; Raiden's boss/raiden/bars and mboss/bars draw with it every tick): for 6 inputs with the options
    unset or 0, the line of the tree equals the base's byte for byte, at most DRAW_BUDGET more commands per draw
    (IDENTITY-3).
"""
import argparse
import copy
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import azsim as A  # noqa: E402
import mcsim  # noqa: E402
from mcsim import Ctx, Ent  # noqa: E402

REPO = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/az/wt_cm')
if not REPO.exists():                  # the worktree was removed after its merge: any clone of the repo has the commits
    REPO = Path('/home/user/rlk')        # (read-only git commands: archive / ls-tree / show)
CMD_BUDGET = 6.5        # extra commands per mid-boss fight tick (sim count; +15.9..+18.4 before the CM fix round)
DRAW_BUDGET = 6         # extra commands per bossui/draw with the options unset (sim count: the colour test, the nums
                        # call, the two resets; measured +6, was +15 before the fix round)
# chapter-mode names a mid-boss fight may hold on the tree only (cm.md 4.1 / 4.2 / 11 / 13, and their internal temporaries)
NEW_FAKE = {'#atkSeq', '#auxResEl', '#auxResElV', '#buHpCol', '#buNoNum', '#c280', '#cbAuto', '#cbForce', '#cbWait', '#hzNR',
            '#hzSafeG', '#mbAr', '#mbArBuild', '#mbArS10', '#mbArW10', '#mbCN', '#mbCine', '#mbDodgeEv', '#mbDodgeOk',
            '#mbFloor', '#mbFloorHit', '#mbHitEl', '#mbHitEv', '#mbHitRA', '#mbHitSh', '#mbHitSrc', '#mbLost', '#mbMode',
            '#mbMusPh', '#mbMusT', '#mbNRIn', '#mbNRNow', '#mbNoRx', '#mbPart', '#mbPoolPct', '#mbPushOn', '#mbPx', '#mbQi',
            '#mbRamp', '#mbShIn', '#mbSrc', '#mbSrcIn', '#mbTot', '#pjNR', '#pjNoDodge', '#pxIn',
            '#mbGrpL2',      # AZ FIX FAIR-3: the last group landed by a one-shot hit (#mbGrpL stays M0's)
            '#mbBarOff'}     # 홍련 FN-f (S1, I1 request s1-1): the module's bars-off flag, zeroed by fight_vars / cleanup_fight
NEW_OBJ = {'mbRes0', 'mbRes1', 'mbRes2', 'mbRes3', 'mbRes4', 'mbRes5', 'mbRes6', 'mbRes7', 'mbRes8', 'mbHzNR', 'mbHzSG',
           'mbPjND', 'mbPjNR', 'mbPart'}
NEW_STORAGE = {'rlk:mboss': {'creg', 'cbyid'}}
NEW_REC = {'kind', 'ar', 'arena', 'px', 'pxBase', 'shield', 'res', 'phases', 'music', 'ch', 'route', 'theme'}
FAIL = []


def check(label, ok, info=''):
    print(('ok   ' if ok else 'FAIL ') + label + ('' if ok else f'  {str(info)[:600]}'))
    if not ok:
        FAIL.append(label)


def base_tree(base, tmp):
    """data/ + the registry of the base commit, from S1-CM's worktree (the tested tree may be a plain copy)."""
    arc = subprocess.run(['git', '-C', str(REPO), 'archive', base, 'roguelike/data', 'roguelike/tools/mboss_registry.json',
                          'roguelike/pack.mcmeta'], capture_output=True, check=True).stdout
    subprocess.run(['tar', '-x', '-C', str(tmp)], input=arc, check=True)
    return tmp / 'roguelike'


def counted(s):
    n = [0]
    orig = s.cmd

    def cmd(t, ctx):
        n[0] += 1
        return orig(t, ctx)
    s.cmd = cmd
    return n


def row(s, pl):
    b = A.body_of(s)
    return (s.t, s.sc(('e', pl.id), 'curHealth'), s.sc(('e', b.id), 'mhpC') if b and b.alive else None,
            len([e for e in s.ents if e.alive]), tuple(round(x, 3) for x in pl.pos), s.sc('#mbSt', 'mb'), s.sc('#mbOn', 'mb'))


def logs_of(s):
    return copy.deepcopy(dict(dmg=s.dmg, dodges=s.dodges, hz=s.hz, pjs=s.pjs, rig=s.rig, says=s.says))


def scen_fight(dp, force, ticks=1200, every=6, seed=1018):
    s, zone, pl = A.setup(force=force, dp=dp, seed=seed)
    for o in ('curHealth', 'maxHealth'):
        s.setsc(('e', pl.id), o, 1000000)
    n = counted(s)
    ok = A.to_fight(s, zone)
    c0 = n[0]
    rows = []
    for i in range(ticks):
        b = A.body_of(s)
        if every and b is not None and i % every == 0 and (s.sc('#mbSt', 'mb') or 0) == 1:
            A.strike(s, b, 25, elem=(i // every) % 8)
        A.world(s)
        rows.append(row(s, pl))
    return dict(ok=ok, rows=rows, logs=logs_of(s), cmds=n[0] - c0, ticks=ticks)


def scen_end(dp, force, mode, seed=1018):
    s, zone, pl = A.setup(force=force, dp=dp, seed=seed, hp=900)
    for o in ('curHealth', 'maxHealth'):
        s.setsc(('e', pl.id), o, 1000000)
    ok = A.to_fight(s, zone)
    rows = []
    for i in range(2000 if mode in ('kill', 'cancel') else 700):
        b = A.body_of(s)
        st = s.sc('#mbSt', 'mb') or 0
        if mode == 'kill' and b is not None and st == 1 and i % 5 == 0:
            A.strike(s, b, 60, elem=(i // 5) % 8)
        if mode == 'cancel' and i == 200 and b is not None:
            b.alive = False
            s.ents = [e for e in s.ents if e is not b]
        if mode == 'pause' and 100 <= i < 160:
            s.setsc(('e', pl.id), 'pkMode', 1)
        if mode == 'pause' and i == 160:
            s.setsc(('e', pl.id), 'pkMode', 0)
        if mode == 'reload' and i == 150:
            s.call('rlk:mboss/init', A.C0)
        A.world(s)
        rows.append(row(s, pl))
        if i > 300 and (s.sc('#mbLive', 'mb') or 0) == 0 and (s.sc('#combat', 'room') or 0) == 0:
            break
    return dict(ok=ok, rows=rows, logs=logs_of(s), s=s, xp=s.sc('#XP', 'azs') or 0)


def ent_key(e):
    return (e.etype, tuple(sorted(e.tags)), tuple(round(x, 2) for x in e.pos))


def end_state(s):
    live = {e.id: e for e in s.ents if e.alive}
    fake, ents = {}, {}
    for (h, o), v in s.scores.items():
        if isinstance(h, str):
            fake[(h, o)] = v
        elif isinstance(h, tuple) and h[1] in live:
            ents.setdefault(ent_key(live[h[1]]), {})[o] = v
    return fake, ents, sorted(ent_key(e) for e in live.values()), copy.deepcopy(s.storage)


def norm_rec(a, b):
    """(a, b) with the schema-v2 fields that only b (the tree) carries dropped from b."""
    if isinstance(a, dict) and isinstance(b, dict):
        b = {k: v for k, v in b.items() if k in a or k not in NEW_REC}
        return a, {k: (norm_rec(a[k], v)[1] if k in a else v) for k, v in b.items()}
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return a, [norm_rec(x, y)[1] for x, y in zip(a, b)]
    return a, b


def compare_end(label, r0, r1):
    f0, e0, l0, st0 = end_state(r0['s'])
    f1, e1, l1, st1 = end_state(r1['s'])
    gone = sorted(str(k) for k in f0 if k not in f1)
    diff = sorted(f'{k}: {f0[k]} -> {f1[k]}' for k in f0 if k in f1 and f0[k] != f1[k])
    extra = sorted(str(k) for k in f1 if k not in f0 and k[0] not in NEW_FAKE and k[1] not in NEW_OBJ)
    check(f'{label}: fake-player scores of the base equal on the tree (new ones only chapter-mode names)',
          not gone and not diff and not extra, (gone[:5], diff[:5], extra[:8]))
    check(f'{label}: live entities identical (type, tags, position)', l0 == l1, sorted(set(l0) ^ set(l1))[:4])
    bad = []
    for k in e0:
        a, b = e0[k], e1.get(k, {})
        bad += [f'{k[0]} {o}: {a[o]} -> {b.get(o)}' for o in a if a[o] != b.get(o)]
        bad += [f'{k[0]} +{o}' for o in b if o not in a and o not in NEW_OBJ]
    check(f'{label}: their scores identical (new objectives only chapter-mode ones)', not bad, bad[:6])
    sbad = []
    for ns in sorted(set(st0) | set(st1)):
        a, b = st0.get(ns, {}), st1.get(ns, {})
        sbad += [f'{ns} -{k}' for k in a if k not in b]
        sbad += [f'{ns} +{k}' for k in b if k not in a and k not in NEW_STORAGE.get(ns, set())]
        for k in a:
            if k in b and a[k] != b[k]:
                x, y = (norm_rec(a[k], b[k]) if k in ('reg', 'cur') else (a[k], b[k]))
                if x != y:
                    sbad.append(f'{ns} {k}: {str(x)[:120]} | {str(y)[:120]}')
    check(f'{label}: storage identical apart from the chapter-mode keys and the schema-v2 record fields', not sbad, sbad[:4])


def first_diff(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i, x, y
    return (min(len(a), len(b)), 'len', (len(a), len(b))) if len(a) != len(b) else None


# ------------------------------------------------------------------------------------------------- C bossui
def bu_consts(dp):
    out = []
    for ln in (dp / 'data/rlk/function/bossui/init.mcfunction').read_text(encoding='utf-8').split('\n'):
        m = re.match(r'scoreboard players set (#\w+) bu (-?\d+)', ln.strip())
        if m:
            out.append((m.group(1), int(m.group(2))))
    return out


def bu_draw(dp, hp, mx, trail, sub, subm, subc, opts):
    s = mcsim.Sim(dp / 'data/rlk/function')
    for k, v in bu_consts(dp):
        s.setsc(k, 'bu', v)
    b = Ent('husk', (0, 0, 0))
    s.ents.append(b)
    s.setsc(('e', b.id), 'buTrail', trail)
    for k, v in (('#buHp', hp), ('#buMax', mx), ('#buSub', sub), ('#buSubMax', subm), ('#buSubCol', subc)):
        s.setsc(k, 'bu', v)
    for k, v in opts.items():
        s.setsc(k, 'bu', v)
    n = counted(s)
    s.call('rlk:bossui/draw', Ctx(b, (0, 0, 0), (0, 0)))
    return json.dumps(s.storage.get('rlk:bu'), sort_keys=True, ensure_ascii=False), n[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dp')
    ap.add_argument('--base', default='22ba247')
    ap.add_argument('--forces', default='99,1,2,3')
    ap.add_argument('--modes', default='kill,cancel,pause,reload')
    args = ap.parse_args()
    dp = Path(args.dp).resolve()
    (HERE / 'tmp').mkdir(exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix='m0diff_', dir=HERE / 'tmp'))
    t0 = time.time()
    try:
        m0 = base_tree(args.base, tmp)
        print(f'== base {args.base} -> {m0} ({time.time() - t0:.0f} s)')
        forces = [int(x) for x in args.forces.split(',') if x]
        print('== A. fight traces and commands per tick')
        for f in forces:
            r0, r1 = scen_fight(m0, f), scen_fight(dp, f)
            fd = first_diff(r0['rows'], r1['rows'])
            check(f'A force {f}: the fight starts on both', r0['ok'] and r1['ok'])
            check(f'A force {f}: per-tick trace identical over {r0["ticks"]} t', fd is None, fd)
            dl = [k for k in r0['logs'] if r0['logs'][k] != r1['logs'][k]]
            check(f'A force {f}: dmg / dodge / hz / pj / rig / line logs identical', not dl, dl)
            per = (r1['cmds'] - r0['cmds']) / r0['ticks']
            check(f'A force {f}: commands per tick {r0["cmds"] / r0["ticks"]:.1f} -> {r1["cmds"] / r1["ticks"]:.1f} '
                  f'(+{per:.2f}/t, budget {CMD_BUDGET})', per <= CMD_BUDGET, per)
        print('== B. kill / cancel / pause / reload: traces and end states')
        for mode in [m for m in args.modes.split(',') if m]:
            for f in forces:
                r0, r1 = scen_end(m0, f, mode), scen_end(dp, f, mode)
                label = f'B {mode} force {f}'
                fd = first_diff(r0['rows'], r1['rows'])
                check(f'{label}: per-tick trace identical ({len(r0["rows"])} t, kill XP {r0["xp"]}/{r1["xp"]})',
                      fd is None and r0['ok'] and r1['ok'], fd)
                dl = [k for k in r0['logs'] if r0['logs'][k] != r1['logs'][k]]
                check(f'{label}: logs identical', not dl, dl)
                compare_end(label, r0, r1)
        print('== C. bossui/draw with the options unset')
        cases = [(5000, 9000, 6000, 300, 900, 8), (0, 100, 0, 0, 1, 0), (123456, 1000000, 200000, 52, 52, 1),
                 (1, 1, 1, 750, 750, 9), (77, 1000, 500, 0, 1, 0), (9999999, 9999999, 9999999, 3, 7, 4)]
        for c in cases:
            for opts in ({}, {'#buHpCol': 0, '#buNoNum': 0}):
                a, na = bu_draw(m0, *c, {})
                b, nb = bu_draw(dp, *c, opts)
                check(f'C draw {c} {opts or "unset"}: the line equals M0\'s; commands {na} -> {nb} (budget +{DRAW_BUDGET})',
                      a == b and nb - na <= DRAW_BUDGET, (a == b, nb - na))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'({time.time() - t0:.0f} s)')
    print('M0 DIFF CHECKS PASSED' if not FAIL else f'{len(FAIL)} FAILED: {FAIL[:12]}')
    sys.exit(1 if FAIL else 0)


if __name__ == '__main__':
    main()
