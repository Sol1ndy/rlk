#!/usr/bin/env python3
"""gen_check_hr.py: the generators that touch 홍련 (Scarlet): twice -> identical, the documented and the reverse order -> the
same tree, each writes only its owned paths (I1; scratchpad hr/i1_brief.md I1a step 7, hr/contract.md §1, PLAN §9.1;
the precedent R:tools/dev/sim/az/tests_cm/gen_check.py).

    python3 gen_check_hr.py <datapack root> --rp <unpacked resource pack> [-v]

The tested tree and the pack are only read: data/, tools/ (without tools/dev) and pack.mcmeta are copied for real (no hard
links: a generator writing outside its paths can never touch the tested tree) into ./tmp/gch_*, the pack into ./tmp/gch_*/rp;
both are removed at the end. The generators of this boss (contract §1 / PLAN §9.1 owners):

  core     tools/build_mboss_core.py            F:mboss/** (not arena/ nor the mid-boss module trees), F:boss/test/**
  arena    tools/build_mboss_arena.py           F:mboss/arena/**
  rig      node tools/build_scarlet_rig.mjs     F:boss/scarlet/rig/**, tools/scarlet_rig_manifest.json; the RP's
           --resourcepack <rp copy>             mboss/scarlet/** + the items-atlas entries (assets/minecraft/atlases/)
  kit      tools/build_mboss_hr_fx.py --skip-rp F:boss/scarlet/fx/**, tools/mboss_hr_fx_manifest.json (S1K; only once it
                                                exists: I1b)
  scarlet  tools/build_mboss_scarlet.py         F:boss/scarlet/** but rig/ and fx/
  check    tools/check_mboss_pack.py            nothing (0 problems)

  G1  each generator run twice: the first run reproduces the tested tree byte for byte, the second changes nothing
  G2  each run writes only the generator's owned paths (every other file of the copy keeps its bytes and its mtime)
  G3  the documented order (core -> arena -> rig -> [kit] -> scarlet -> check) and the reverse order, each from a copy whose
      F:boss/scarlet/** was wiped, give the tested tree
  G4  ownership: a stray file inside each owned folder (scarlet's core/ seq/ p/r1/, the rig's rig/, the arena's
      mboss/arena/hr_field/) is spared by every other generator and removed by its owner
  G5  the rig's resource-pack side twice into the pack copy: the second build changes no byte, the pack equals the given one
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if a != '-v']
VERBOSE = '-v' in sys.argv[1:]
RPSRC = None
if '--rp' in ARGS:
    i = ARGS.index('--rp')
    RPSRC = Path(ARGS[i + 1]).resolve()
    del ARGS[i:i + 2]
SRC = Path(ARGS[0]).resolve()
HERE = Path(__file__).resolve().parent
TMP = HERE / 'tmp'
FN = 'data/rlk/function/'
MID = ('guardian', 'butterfly', 'fieldgen', 'proto', 'cproto', 'spproto')
KIT = (SRC / 'tools/build_mboss_hr_fx.py').exists()
GENS = {'core': [sys.executable, 'tools/build_mboss_core.py'], 'arena': [sys.executable, 'tools/build_mboss_arena.py'],
        'rig': ['node', 'tools/build_scarlet_rig.mjs', '--resourcepack', '<RP>'],
        'kit': [sys.executable, 'tools/build_mboss_hr_fx.py', '--skip-rp'],
        'scarlet': [sys.executable, 'tools/build_mboss_scarlet.py'], 'check': [sys.executable, 'tools/check_mboss_pack.py']}
ORDER = ['core', 'arena', 'rig'] + (['kit'] if KIT else []) + ['scarlet', 'check']
FAIL, OK = [], []


def owned(gen, rel):
    """Does generator `gen` own the datapack-copy path `rel` (posix, relative to roguelike/)?"""
    if gen == 'core':
        if not rel.startswith(FN + 'mboss/'):
            return rel.startswith(FN + 'boss/test/')
        sub = rel[len(FN + 'mboss/'):]
        return not sub.startswith('arena/') and not any(sub.startswith(m + '/') for m in MID)
    if gen == 'arena':
        return rel.startswith(FN + 'mboss/arena/')
    if gen == 'rig':
        return rel.startswith(FN + 'boss/scarlet/rig/') or rel == 'tools/scarlet_rig_manifest.json'
    if gen == 'kit':
        return rel.startswith(FN + 'boss/scarlet/fx/') or rel == 'tools/mboss_hr_fx_manifest.json'
    if gen == 'scarlet':
        return rel.startswith(FN + 'boss/scarlet/') and not rel.startswith((FN + 'boss/scarlet/rig/', FN + 'boss/scarlet/fx/'))
    return False


def check(name, cond, detail=''):
    (OK if cond else FAIL).append(name)
    if not cond or VERBOSE:
        print(('ok   ' if cond else 'FAIL ') + name + ('' if cond or not detail else f'  {detail}'))


def copy_tree(src, dst):
    for d, dirs, files in os.walk(src):
        rel_d = Path(d).relative_to(src)
        dirs[:] = [x for x in dirs if x != '__pycache__' and not (rel_d == Path('.') and src.name == 'tools' and x == 'dev')]
        (dst / rel_d).mkdir(parents=True, exist_ok=True)
        for f in files:
            shutil.copy2(Path(d) / f, dst / rel_d / f)


def snap(root, with_time=False):
    """{rel: sha1} of data/ + tools/*manifest*.json (+ the mboss_scarlet stub); with_time: {rel: (sha1, mtime_ns)} of data/ +
    every file of tools/ (the writes check)."""
    out = {}
    tops = [root / 'data'] + ([root / 'tools'] if with_time else [])
    for top in tops:
        for d, _, files in os.walk(top):
            if '__pycache__' in d:
                continue
            for f in files:
                p = Path(d) / f
                rel = p.relative_to(root).as_posix()
                h = hashlib.sha1(p.read_bytes()).hexdigest()
                out[rel] = (h, p.stat().st_mtime_ns) if with_time else h
    if not with_time:
        for p in sorted((root / 'tools').glob('*manifest*.json')):
            out[p.relative_to(root).as_posix()] = hashlib.sha1(p.read_bytes()).hexdigest()
    return out


def rp_hash(rp):
    h = hashlib.sha1()
    for p in sorted(x for x in rp.rglob('*') if x.is_file()):
        h.update(p.relative_to(rp).as_posix().encode() + b'\0' + hashlib.sha1(p.read_bytes()).digest())
    return h.hexdigest()


def diff(ref, now):
    added = sorted(set(now) - set(ref))
    gone = sorted(set(ref) - set(now))
    changed = sorted(k for k in set(ref) & set(now) if ref[k] != now[k])
    return added, gone, changed


def same(name, ref, now):
    a, g, c = diff(ref, now)
    check(name, not (a or g or c), f'added {a[:4]} ({len(a)}) gone {g[:4]} ({len(g)}) changed {c[:4]} ({len(c)})')


def run(root, rp, gen):
    cmd = [rp.as_posix() if x == '<RP>' else x for x in GENS[gen]]
    r = subprocess.run(cmd, cwd=root, capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    ok = r.returncode == 0 and (gen != 'check' or ' 0 problem(s).' in r.stdout)
    if not ok:
        check(f'generator {gen} runs ({" ".join(GENS[gen][1:2])})', False, (r.stdout[-600:] + r.stderr[-900:]).strip())
    return ok


def run_watched(root, rp, gen):
    """Run `gen` and report every file outside its owned paths whose bytes or mtime changed (or that came / went)."""
    before = snap(root, with_time=True)
    ok = run(root, rp, gen)
    after = snap(root, with_time=True)
    a, g, c = diff(before, after)
    stray = [x for x in a + g + c if not owned(gen, x)]
    return ok, stray


def main():
    if not RPSRC:
        print('usage: gen_check_hr.py <datapack root> --rp <unpacked resource pack>')
        return 2
    ref = snap(SRC)
    rp_ref = rp_hash(RPSRC)
    print(f'gen_check_hr: tested tree {len(ref)} files; generators {", ".join(ORDER)}' + ('' if KIT else ' (no kit yet: I1b)'))
    TMP.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gch_', dir=TMP) as tmp:
        root, rp = Path(tmp) / 'roguelike', Path(tmp) / 'rp'
        root.mkdir()
        for part in ('data', 'tools'):
            copy_tree(SRC / part, root / part)
        shutil.copy2(SRC / 'pack.mcmeta', root / 'pack.mcmeta')
        shutil.copytree(RPSRC, rp)
        same('G0 the copy = the tested tree', ref, snap(root))
        # G1 / G2: every generator twice, watched
        for gen in ORDER:
            ok1, stray1 = run_watched(root, rp, gen)
            s1 = snap(root)
            ok2, stray2 = run_watched(root, rp, gen)
            same(f'G1 {gen}: the first run reproduces the tested tree', ref, s1)
            same(f'G1 {gen}: a second run changes nothing', s1, snap(root))
            check(f'G2 {gen}: writes only its owned paths (two runs)', ok1 and ok2 and not stray1 and not stray2,
                  (stray1 + stray2)[:6])
        # G5: the rig's RP side twice
        check('G5 the rig\'s resource-pack side, built twice into the pack copy: equal to the given pack, unchanged by the '
              'second build', rp_hash(rp) == rp_ref, (rp_hash(rp), rp_ref))
        # G3: wiped F:boss/scarlet, documented order and the reverse
        for name, order in (('documented', ORDER), ('reverse', [g for g in reversed(ORDER) if g != 'check'] + ['check'])):
            shutil.rmtree(root / FN / 'boss/scarlet')
            oks = [run(root, rp, g) for g in order]
            same(f'G3 F:boss/scarlet wiped, the {name} order ({" -> ".join(order)}) gives the tested tree', ref, snap(root))
            check(f'G3 {name}: every generator ran', all(oks))
        # G4: ownership probes
        strays = {'scarlet': [FN + 'boss/scarlet/core/zz_stray.mcfunction', FN + 'boss/scarlet/seq/zz_stray/k.mcfunction',
                              FN + 'boss/scarlet/p/r1/zz_stray.mcfunction'],
                  'rig': [FN + 'boss/scarlet/rig/zz_stray.mcfunction'],
                  'arena': [FN + 'mboss/arena/hr_field/zz_stray.mcfunction']}
        for owner, paths in strays.items():
            for rel in paths:
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                (root / rel).write_text('# stray\n', encoding='utf-8')
            others = [g for g in ORDER if g not in (owner, 'check')]
            for g in others:
                run(root, rp, g)
            spared = all((root / rel).exists() for rel in paths)
            run(root, rp, owner)
            removed = not any((root / rel).exists() for rel in paths)
            check(f'G4 {owner}: strays in its folders ({len(paths)}) spared by {", ".join(others)} and removed by {owner}',
                  spared and removed, (spared, removed))
            for rel in paths:
                if (root / rel).exists():
                    (root / rel).unlink()
        same('G4 after the probes the copy = the tested tree', ref, snap(root))
    n = len(OK) + len(FAIL)
    if FAIL:
        print(f'{len(FAIL)} GEN_CHECK_HR CHECK(S) FAILED: {FAIL}')
        return 1
    print(f'gen_check_hr: {len(OK)}/{n} passed; ALL GEN_CHECK_HR CHECKS PASSED')
    return 0


if __name__ == '__main__':
    sys.exit(main())
