#!/usr/bin/env python3
"""Generator order / idempotency check of the datapack with the chapter mode (AZ-CM, S1-CM; no change to the tested tree).

    python3 gen_check.py <worktree roguelike> [--rp <unpacked resource pack>]

(S1-CM's copy of scratchpad mb3/tests/gen_check.py: the chapter-mode generators join every order, cm.md 1.2:
core -> arena (plaza + every arenas{} entry) -> build_cboss_rooms -> proto -> cproto -> guardian -> bf kit -> butterfly
-> fg kit -> fieldgen.)

Copies the datapack (data/, tools/ without tools/dev, pack.mcmeta) to a temporary folder under scratchpad az/tests_cm/tmp and, there, runs
the Python generators in several orders. After each run every file under data/rlk/function/mboss/ and
data/rlk/function/room/cboss/ and the generator manifests (tools/*manifest*.json) must be byte-identical to the tested tree:

  1. the documented order (the tree is fully generated)
  2. the same again (a second rebuild changes nothing; a stale F:mboss/px/** output, i.e. a core run against an older
     manifest than the committed one, fails here)
  3. the reverse order (no generator depends on another's output or deletes it)
  4. / 5. F:mboss/butterfly wiped, butterfly -> kit and kit -> butterfly (unchanged from M0)
  7. / 8. F:mboss/fieldgen wiped, fieldgen -> fgkit and fgkit -> fieldgen, 7b the ownership probe (unchanged from M0)
  10. chapter-mode ownership: F:mboss/cproto/, F:mboss/arena/cp_test/ and F:room/cboss/ wiped, then cproto -> arena ->
      rooms rebuild them exactly; a stray file in each of those folders and in F:mboss/px/ is removed by its owner
      (cproto / arena / rooms / core) and spared by the others
  9. no generator wrote a file outside its own paths (every hard-linked file unchanged)

The rig generators (node tools/build_mboss_*_rig.mjs) need a resource pack and node; they own F:mboss/<id>/rig/** only
and are not run here (every Python generator above spares rig/). With --rp, each kit's resource-pack side and the boss
bar (tools/build_bossbar.py) are also built twice into a temporary copy of the pack: the second build must not change a
byte, and the kits' sprites, models, item definitions, fonts and atlas entries must be present.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path(sys.argv[1]).resolve()
RP = Path(sys.argv[sys.argv.index('--rp') + 1]).resolve() if '--rp' in sys.argv else None
FGKIT = (SRC / 'tools/build_mboss_fg_fx.py').exists()
GENS = {'core': ['tools/build_mboss_core.py'], 'arena': ['tools/build_mboss_arena.py'], 'proto': ['tools/build_mboss_proto.py'],
        'rooms': ['tools/build_cboss_rooms.py'], 'cproto': ['tools/build_mboss_cproto.py'],
        'guardian': ['tools/build_mboss_guardian.py'], 'kit': ['tools/build_mboss_bf_fx.py', '--skip-rp'],
        'butterfly': ['tools/build_mboss_butterfly.py'], 'fgkit': ['tools/build_mboss_fg_fx.py', '--skip-rp'],
        'fieldgen': ['tools/build_mboss_fieldgen.py']}
ORDER = ['core', 'arena', 'rooms', 'proto', 'cproto', 'guardian', 'kit', 'butterfly'] + (['fgkit'] if FGKIT else []) + ['fieldgen']
FAIL = []
# 11-03: + boss/test/ (build_mboss_core.py writes it; as a hard link the core run in the copy rewrote the tested tree's
# 13 boss/test/*.mcfunction in place, the cause of the old check-9 failure)
# round V integration (11-12): + data/rlk/advancement/mboss/ (lane VC: build_mboss_core.py writes FN-cam's tick advancement
# cam_post.json; hard-linked, check 9 failed on the merged tree and the tested tree's file was rewritten in place)
REAL_DP = ('data/rlk/function/mboss/', 'data/rlk/function/room/cboss/', 'data/rlk/function/bossui/',
           'data/rlk/function/boss/test/', 'data/rlk/advancement/mboss/', 'tools/')
TMP = Path(__file__).resolve().parent / 'tmp'
REAL_RP = ('assets/rlk/textures/mboss/bf_kit/', 'assets/rlk/models/item/mboss/bf_kit/', 'assets/rlk/items/mboss/bf_kit/',
           'assets/rlk/textures/mboss/fg_kit/', 'assets/rlk/models/item/mboss/fg_kit/', 'assets/rlk/items/mboss/fg_kit/',
           'assets/rlk/font/', 'assets/rlk/textures/font/mboss_bf/', 'assets/rlk/textures/font/mboss_fg/',
           'assets/minecraft/atlases/', 'assets/rlk/textures/font/bossbar/', 'assets/minecraft/textures/gui/sprites/boss_bar/')
LINKED = []                     # (path in the temporary tree, (inode, size, mtime_ns)) of every hard-linked file


def light_copy(src, dst, real):
    """Copy src to dst: files under the `real` prefixes (posix, relative) are copied, every other file hard-linked.
    11-03: tools/dev is never copied (this harness and its tmp/, where the copy is being built, may sit inside the tested
    tree as roguelike/tools/dev/sim; the walk would copy the copy without end)."""
    for d, dirs, files in os.walk(src):
        rel_d = Path(d).relative_to(src)
        dirs[:] = [x for x in dirs if x != '__pycache__' and not (rel_d == Path('.') and src.name == 'tools' and x == 'dev')]
        (dst / rel_d).mkdir(parents=True, exist_ok=True)
        for f in files:
            rel = (rel_d / f).as_posix()
            a, b = Path(d) / f, dst / rel_d / f
            if any(rel.startswith(p) for p in real):
                shutil.copy2(a, b)
            else:
                os.link(a, b)
                st = b.stat()
                LINKED.append((b, (st.st_ino, st.st_size, st.st_mtime_ns)))


def linked_unchanged(name):
    bad = []
    for p, sig in LINKED:
        try:
            st = p.stat()
        except FileNotFoundError:
            continue            # unlinking a hard link never touches the original
        if (st.st_ino, st.st_size, st.st_mtime_ns) != sig:
            bad.append(str(p))
    ok = not bad
    print(('ok   ' if ok else 'FAIL ') + name, '' if ok else f'{len(bad)} hard-linked files written: {bad[:4]}')
    if not ok:
        FAIL.append(name)


def snap(root):
    out = {}
    for base in (root / 'data/rlk/function/mboss', root / 'data/rlk/function/room/cboss'):
        for p in sorted(base.rglob('*')):
            if p.is_file():
                out[p.relative_to(root).as_posix()] = hashlib.sha1(p.read_bytes()).hexdigest()
    for p in sorted((root / 'tools').glob('*manifest*.json')):
        out[p.relative_to(root).as_posix()] = hashlib.sha1(p.read_bytes()).hexdigest()
    return out


def compare(name, ref, now):
    added = sorted(set(now) - set(ref))
    gone = sorted(set(ref) - set(now))
    changed = sorted(k for k in set(ref) & set(now) if ref[k] != now[k])
    ok = not (added or gone or changed)
    print(('ok   ' if ok else 'FAIL ') + name, '' if ok else f'added {added[:5]} ({len(added)}) gone {gone[:5]} ({len(gone)}) '
          f'changed {changed[:5]} ({len(changed)})')
    if not ok:
        FAIL.append(name)


def run(root, names):
    for n in names:
        r = subprocess.run([sys.executable] + GENS[n], cwd=root, capture_output=True, text=True)
        if r.returncode:
            print(f'FAIL generator {n}:\n{r.stdout[-800:]}{r.stderr[-1500:]}')
            FAIL.append(f'generator {n}')


def wipe(root, mod, keep):
    b = root / f'data/rlk/function/mboss/{mod}'
    for p in sorted(b.iterdir()):
        if p.name in keep:
            continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()


ref = snap(SRC)
TMP.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='gen_check_', dir=TMP) as tmp:
    root = Path(tmp) / 'roguelike'
    root.mkdir()
    for part in ('data', 'tools'):
        light_copy(SRC / part, root / part, [p[len(part) + 1:] for p in REAL_DP if p.startswith(part + '/')]
                   if part == 'data' else [''])
    shutil.copy(SRC / 'pack.mcmeta', root / 'pack.mcmeta')
    run(root, ORDER)
    compare('1. documented order ' + ' -> '.join(ORDER) + ' reproduces the tree', ref, snap(root))
    run(root, ORDER)
    compare('2. a second rebuild changes nothing', ref, snap(root))
    run(root, ORDER[::-1])
    compare('3. reverse order ' + ' -> '.join(ORDER[::-1]) + ' changes nothing', ref, snap(root))
    wipe(root, 'butterfly', ('rig',))
    run(root, ['butterfly', 'kit'])
    compare('4. F:mboss/butterfly wiped, butterfly -> kit rebuilds it exactly', ref, snap(root))
    wipe(root, 'butterfly', ('rig',))
    run(root, ['kit', 'butterfly'])
    compare('5. F:mboss/butterfly wiped, kit -> butterfly rebuilds it exactly (the core spares the kit)', ref, snap(root))
    fx = root / 'data/rlk/function/mboss/fieldgen/fx'
    if FGKIT:
        wipe(root, 'fieldgen', ('rig',))
        run(root, ['fieldgen', 'fgkit'])
        compare('7. F:mboss/fieldgen wiped (except rig/), fieldgen -> fgkit rebuilds it exactly', ref, snap(root))
        wipe(root, 'fieldgen', ('rig',))
        run(root, ['fgkit', 'fieldgen'])
        compare('8. F:mboss/fieldgen wiped again, fgkit -> fieldgen rebuilds it exactly (the core spares the kit)', ref, snap(root))
        kit_probe, core_probe = fx / 'p/kit_probe.mcfunction', fx / 'core_probe.mcfunction'
        for f in (kit_probe, core_probe):
            f.write_text('# a stray file\n', encoding='utf-8')
        run(root, ['fieldgen'])
        a = kit_probe.exists() and not core_probe.exists()
        run(root, ['fgkit'])
        ok = a and not kit_probe.exists()
        print(('ok   ' if ok else 'FAIL ') + '7b. the fieldgen core spares the kit\'s owned fx/ paths and cleans its own names '
              'under fx/; the kit cleans its own')
        if not ok:
            FAIL.append('7b')
        for f in (kit_probe, core_probe):
            f.unlink(missing_ok=True)
        compare('7c. after the probes the tree is exact again', ref, snap(root))
    else:
        wipe(root, 'fieldgen', ('rig', 'fx'))
        run(root, ['fieldgen'])
        compare('7. F:mboss/fieldgen wiped (except rig/, fx/), fieldgen rebuilds it exactly', ref, snap(root))
        fake = fx / 'kit_probe.mcfunction'
        fake.parent.mkdir(parents=True, exist_ok=True)
        fake.write_text('# a kit file\n', encoding='utf-8')
        run(root, ['fieldgen'])
        ok = fake.exists()
        print(('ok   ' if ok else 'FAIL ') + '7b. the fieldgen core spares fx/ (the kit\'s, wip/fg-fx)')
        if not ok:
            FAIL.append('7b')
        fake.unlink()
        fx.rmdir()
    # 10. chapter-mode ownership
    fn = root / 'data/rlk/function'
    for d in (fn / 'mboss/cproto', fn / 'mboss/arena/cp_test', fn / 'room/cboss'):
        shutil.rmtree(d)
    run(root, ['cproto', 'arena', 'rooms'])
    compare('10. F:mboss/cproto, F:mboss/arena/cp_test, F:room/cboss wiped: cproto -> arena -> rooms rebuild them exactly', ref, snap(root))
    probes = {'cproto': fn / 'mboss/cproto/zz_probe.mcfunction', 'arena': fn / 'mboss/arena/cp_test/zz_probe.mcfunction',
              'rooms': fn / 'room/cboss/zz_probe.mcfunction', 'core': fn / 'mboss/px/zz_probe.mcfunction'}
    for f in probes.values():
        f.write_text('# a stray file\n', encoding='utf-8')
    ok, left = True, set(probes)
    for owner in ('core', 'arena', 'rooms', 'cproto'):
        run(root, [owner])
        left.discard(owner)
        if probes[owner].exists():
            print(f'FAIL 10b. {owner} left its stray {probes[owner].relative_to(root)}')
            ok = False
        for o in left:
            if not probes[o].exists():
                print(f'FAIL 10b. {owner} removed the stray file of {o}')
                ok = False
    print(('ok   ' if ok else 'FAIL ') + '10b. each chapter-mode generator removes its own stray file and spares the others\'')
    if not ok:
        FAIL.append('10b')
    for f in probes.values():
        f.unlink(missing_ok=True)
    compare('10c. after the probes the tree is exact again', ref, snap(root))
    if RP:
        rp = Path(tmp) / 'rp'
        light_copy(RP, rp, REAL_RP)

        def rsnap():
            return {p.relative_to(rp).as_posix(): hashlib.sha1(p.read_bytes()).hexdigest() for p in sorted(rp.rglob('*')) if p.is_file()}
        kits = [('butterfly kit', 'tools/build_mboss_bf_fx.py')] + ([('field generator kit', 'tools/build_mboss_fg_fx.py')] if FGKIT else [])
        kits.append(('boss bar', 'tools/build_bossbar.py'))
        for label, gen in kits:
            for k in range(2):
                extra = [] if 'bossbar' in gen else ['--datapack', str(root)]
                r = subprocess.run([sys.executable, gen, '--resourcepack', str(rp)] + extra,
                                   cwd=root, capture_output=True, text=True)
                if r.returncode:
                    print(f'FAIL {label} RP build', r.stderr[-1500:])
                    FAIL.append(f'{label} RP build')
                if k == 0:
                    first = rsnap()
            compare(f'6. the {label} resource pack build twice: no change', first, rsnap())
        compare('6a. the datapack is still exact after the resource-pack builds', ref, snap(root))
        must = ['assets/rlk/font/mboss_bf.json', 'assets/rlk/textures/mboss/bf_kit/cres_lime.png',
                'assets/rlk/models/item/mboss/bf_kit/cres_lime.json', 'assets/rlk/items/mboss/bf_kit/cres_lime.json']
        if FGKIT:
            must += ['assets/rlk/font/mboss_fg.json', 'assets/rlk/textures/mboss/fg_kit/wave_band.png',
                     'assets/rlk/models/item/mboss/fg_kit/wave_band.json', 'assets/rlk/items/mboss/fg_kit/wave_band.json']
        miss = [m for m in must if not (rp / m).exists()]
        atlas = (rp / 'assets/minecraft/atlases/items.json').read_text(encoding='utf-8')
        old = [p for p in ('assets/rlk/textures/mboss/bf_fx', 'assets/rlk/items/mboss/bf_fx') if (rp / p).exists()]
        ok = (not miss and 'rlk:mboss/bf_kit/cres_lime' in atlas and 'rlk:mboss/bf_fx/' not in atlas and not old
              and (not FGKIT or 'rlk:mboss/fg_kit/wave_band' in atlas))
        print(('ok   ' if ok else 'FAIL ') + '6b. kit sprites, models, items, fonts and atlas entries present; the removed core engine '
              '(mboss/bf_fx) absent', f'missing {miss} old {old}' if not ok else '')
        if not ok:
            FAIL.append('6b')
    linked_unchanged('9. no generator wrote a file outside its own paths (every hard-linked file unchanged)')
print('GENERATOR CHECKS PASSED' if not FAIL else f'{len(FAIL)} FAILED: {FAIL}')
sys.exit(1 if FAIL else 0)
