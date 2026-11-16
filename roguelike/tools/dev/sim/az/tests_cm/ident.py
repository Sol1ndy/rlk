#!/usr/bin/env python3
"""Byte identity of everything the chapter mode (AZ-CM, S1-CM) must not change, against the release it merges into:
22ba247 (= M0 039b911 + the 10-20 telegraph rule / field generator DMG release; that release changed only the
Guardian / butterfly / fieldgen modules, their kits, load's build stamp and the README, so every "M0" text named below
is still M0's text). Re-pinned from 039b911 to 22ba247 when wip/az-cm merged the release (AZ-CM merge prep).

    python3 ident.py <datapack root> [base commit, default 22ba247] [--save]

1. The mid-boss modules' generated outputs: every file of F:mboss/guardian/**, F:mboss/butterfly/**,
   F:mboss/fieldgen/**, F:mboss/proto/** (incl. their rig/ folders) equals the base commit's (same file set, same bytes).
2. The plaza arena: F:mboss/arena/{ensure,build,build_plaza,rebuild,clear} byte-identical; the plaza per-arena functions
   F:mboss/ar/plaza/{oob,sweep,ok,clamp,clamp_step,leash} carry exactly the command lines of the M0 functions they
   replace (mboss/oob, arena_sweep, mv/ok, mv/clamp, mv/clamp_step, mv/leash; comments aside, the clamp recursion's
   own name mv/clamp_step -> ar/plaza/clamp_step), cm.md 6.1; 2b also maps marker (the summon line of M0 start and
   reload), full_rim (the rim lines of M0 hz/d/full), box_absorb (the gold line of M0 won), fl_on / fl_off (the
   forceload lines of M0 start_unloaded / uninstall) and loaded (M0 start's single `loaded` test). 2c: mv/ok, mv/leash
   and mv/clamp are the plaza lines behind one chapter-arena line (`execute if score #mbAr mb matches 1.. run return
   run function rlk:mboss/ar/<fn>`, the CM fix round's IDENTITY-1), so a mid-boss pays no dispatcher frame.
3. Sources: every file of tools/ in the base commit is unchanged except the files S1-CM owns (cm.md 1.1: the core,
   lib, arena generator, registry, pack check, boss bar generator); S1-CM's new files are listed, nothing else is new.
   (The mid-boss generators import mboss_lib, whose changes are additive; 1. proves their outputs unchanged.)
4. Raiden and the other hand-written engine files: every file outside data/rlk/function/{mboss,room/cboss}/ and
   tools/ equals the base, except the cm.md 16 shared-edit files (and the audit mirror line, README "챕터 보스").
   4d pins the CONTENT of those edits: the zero-context diff of every changed or new engine file against the base must
   equal baseline/shared_edits.diff (a stray line in combat/apply, take_damage or gold_drop fails here). After a
   reviewed change of the cm.md 16 table: `python3 ident.py <dp> --save` rewrites the pin (check the diff of the pin).
"""
import difflib
import subprocess
import sys
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
SAVE = '--save' in sys.argv
DP = Path(ARGS[0]).resolve()
BASE = ARGS[1] if len(ARGS) > 1 else '22ba247'
PIN = Path(__file__).resolve().parent / 'baseline/shared_edits.diff'
FAIL = []
F = 'data/rlk/function/'
OWNED_TOOLS = {'build_bossbar.py', 'build_cboss_rooms.py', 'build_mboss_arena.py', 'build_mboss_core.py', 'check_mboss_pack.py',
               'mboss_arena_cp_test.py', 'mboss_lib.py', 'mboss_registry.json', 'build_mboss_cproto.py',
               'mboss_cproto_rig_manifest.json'}
NEW_TOOLS = {'build_cboss_rooms.py', 'mboss_arena_cp_test.py', 'build_mboss_cproto.py', 'mboss_cproto_rig_manifest.json'}
SHARED = {  # cm.md 16 (+ the 9.6 audit mirror): hand-written files S1-CM edits
    'room/pick/boss', 'room/boss_spawn', 'room/zone_build', 'room/zone_patch', 'room/zone_floor', 'room/wave_start',
    'room/zone_enter', 'room/obj/click', 'room/combat_clear', 'combat/gold_drop', 'combat/apply', 'combat/melee_begin',
    'combat/clear_atkflags', 'element/rx_run', 'element/lunar/hit', 'element/dot', 'player/take_damage', 'mob/shield_ensure',
    'char/navia/pellet_go', 'room/map_mobs', 'room/remove', 'run/start', 'run/end', 'char/arlecchino/skill_hit'}
NEW_SHARED = {'room/obj/k_cboss', 'room/obj/k_cboss2', 'room/obj/k_cboss3', 'room/obj/k_cboss_fb'}
BOSSUI = {'bossui/draw', 'bossui/nums', 'bossui/hp_col'}       # tools/build_bossbar.py output (cm.md 11)
NEW_BOSSUI = {'bossui/nums', 'bossui/hp_col'}


# the base commit is read from S1-CM's worktree (the tested tree may be a plain copy without .git)
REPO = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad/az/wt_cm')
if not REPO.exists():                  # the worktree was removed after its merge: any clone of the repo has the commits
    REPO = Path('/home/user/rlk')        # (read-only git commands: archive / ls-tree / show)
PFX = 'roguelike/'


def git(*a):
    return subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, check=True).stdout


def base_files(rel):
    out = git('ls-tree', '-r', '--full-tree', '--name-only', BASE, PFX + rel).decode().split('\n')
    return {n[len(PFX):] for n in out if n}


def blob(rel):
    return git('show', f'{BASE}:{PFX}{rel}')


def tree_files(rel):
    p = DP / rel
    if p.is_file():
        return {rel}
    if not p.exists():
        return set()
    return {q.relative_to(DP).as_posix() for q in p.rglob('*') if q.is_file() and '__pycache__' not in q.parts}


def report(label, ok, info=''):
    print(('ok   ' if ok else 'FAIL ') + label, '' if ok else info)
    if not ok:
        FAIL.append(label)


def same(label, rels):
    base, now = set(), set()
    for rel in rels:
        base |= base_files(rel)
        now |= tree_files(rel)
    changed = [n for n in sorted(base & now) if blob(n) != (DP / n).read_bytes()]
    report(f'{label}: {len(now)} files byte-identical to {BASE}', base == now and not changed and bool(now),
           f'added {sorted(now - base)[:4]} ({len(now - base)}) gone {sorted(base - now)[:4]} ({len(base - now)}) changed {changed[:4]} ({len(changed)})')


# 1 module outputs
for mod in ('guardian', 'butterfly', 'fieldgen', 'proto'):
    same(f'1. F:mboss/{mod}/**', [F + f'mboss/{mod}'])

# 2 plaza
same('2a. plaza arena F:mboss/arena/{ensure,build,build_plaza,rebuild,clear}',
     [F + f'mboss/arena/{n}.mcfunction' for n in ('ensure', 'build', 'build_plaza', 'rebuild', 'clear')])


def cmds(text):
    return [l for l in text.split('\n') if l.strip() and not l.startswith('#')]


for new, old in (('oob', 'oob'), ('sweep', 'arena_sweep'), ('ok', 'mv/ok'), ('clamp', 'mv/clamp'), ('clamp_step', 'mv/clamp_step'),
                 ('leash', 'mv/leash')):
    a = cmds((DP / F / f'mboss/ar/plaza/{new}.mcfunction').read_text(encoding='utf-8'))
    b = cmds(blob(F + f'mboss/{old}.mcfunction').decode('utf-8').replace('rlk:mboss/mv/clamp_step', 'rlk:mboss/ar/plaza/clamp_step'))
    report(f'2b. ar/plaza/{new} = the command lines of M0 mboss/{old}', a == b and bool(a), [x for x in a if x not in b][:2])


def plaza(fn):
    return cmds((DP / F / f'mboss/ar/plaza/{fn}.mcfunction').read_text(encoding='utf-8'))


def m0_lines(fn, key):
    return [x for x in cmds(blob(F + f'mboss/{fn}.mcfunction').decode('utf-8')) if key in x]


for new, old, key in (('marker', 'start', 'summon minecraft:marker'), ('marker', 'reload', 'summon minecraft:marker'),
                      ('full_rim', 'hz/d/full', 'hz/p/c/'), ('box_absorb', 'won', 'rlk_gold'),
                      ('fl_on', 'start_unloaded', 'forceload add'), ('fl_off', 'uninstall', 'forceload remove')):
    b = m0_lines(old, key)
    report(f'2b. ar/plaza/{new} = the {key!r} line(s) of M0 mboss/{old}', plaza(new) == b and bool(b), (plaza(new), b))
ld = m0_lines('start', ' loaded ')
want = [ld[0].split(' run ')[0] + ' run return fail', 'return 1'] if len(ld) == 1 else None
report("2b. ar/plaza/loaded = M0 start's single `loaded` test (IDENTITY-5)", plaza('loaded') == want, (plaza('loaded'), ld))
for mv, old, fn in (('mv/ok', 'mv/ok', 'ok'), ('mv/leash', 'mv/leash', 'leash'), ('mv/clamp', 'mv/clamp', 'clamp')):
    a = cmds((DP / F / f'mboss/{mv}.mcfunction').read_text(encoding='utf-8'))
    b = cmds(blob(F + f'mboss/{old}.mcfunction').decode('utf-8').replace('rlk:mboss/mv/clamp_step', 'rlk:mboss/ar/plaza/clamp_step'))
    head = f'execute if score #mbAr mb matches 1.. run return run function rlk:mboss/ar/{fn}'
    report(f'2c. mboss/{mv} = one chapter-arena line, then the command lines of M0 mboss/{old}', a[:1] == [head] and a[1:] == b,
           (a[:2], b[:1]))

# 3 sources
base_t = {n.split('/', 1)[1] for n in base_files('tools')}
now_t = {n.split('/', 1)[1] for n in tree_files('tools')}
changed = sorted(n for n in base_t & now_t if n not in OWNED_TOOLS and blob('tools/' + n) != (DP / 'tools' / n).read_bytes())
report(f'3a. tools/: {len(base_t - OWNED_TOOLS)} files outside S1-CM\'s own unchanged', not changed and not (base_t - now_t), (changed[:5], sorted(base_t - now_t)[:5]))
report('3b. new tools files are exactly S1-CM\'s', now_t - base_t == NEW_TOOLS, sorted((now_t - base_t) ^ NEW_TOOLS))

# 4 engine files
base_d = {n for n in base_files('data') if not n.startswith((F + 'mboss/', F + 'room/cboss/'))}
now_d = {n for n in tree_files('data') if not n.startswith((F + 'mboss/', F + 'room/cboss/'))}


def fid(n):
    return n[len(F):-len('.mcfunction')] if n.startswith(F) and n.endswith('.mcfunction') else None


changed = sorted(n for n in base_d & now_d if blob(n) != (DP / n).read_bytes())
bad = [n for n in changed if fid(n) not in SHARED | BOSSUI]
report(f'4a. engine files: {len(base_d)} outside F:mboss / F:room/cboss; changed ones are only the cm.md 16 shared edits '
       f'({len(changed)}: {", ".join(sorted(fid(n) or n for n in changed))})', not bad, bad[:6])
added = sorted(fid(n) or n for n in now_d - base_d)
report('4b. new engine files: the gate objects k_cboss*, bossui/nums and bossui/hp_col only', set(added) == NEW_SHARED | NEW_BOSSUI, added)
report('4c. no engine file removed', not (base_d - now_d), sorted(base_d - now_d)[:5])


def edit_diff(rel):
    old = blob(rel).decode('utf-8').split('\n') if rel in base_d else []
    new = (DP / rel).read_text(encoding='utf-8').split('\n')
    body = [ln for ln in difflib.unified_diff(old, new, n=0, lineterm='') if not ln.startswith(('---', '+++'))]
    return [f'=== {rel}'] + body


edits = []
for rel in sorted(set(changed) | (now_d - base_d)):
    edits += edit_diff(rel)
text = '\n'.join(edits) + '\n'
if SAVE:
    PIN.write_text(text, encoding='utf-8')
    print(f'saved {PIN} ({len(edits)} lines)')
pin = PIN.read_text(encoding='utf-8') if PIN.exists() else ''
if text != pin:
    a, b = pin.split('\n'), text.split('\n')
    first = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    ctx = (a[max(0, first - 3):first + 2], b[max(0, first - 3):first + 2])
else:
    ctx = None
report(f'4d. the content of every shared edit (cm.md 16) and new engine file = the pinned diff baseline/shared_edits.diff '
       f'({sum(1 for x in edits if x.startswith("==="))} files, {sum(1 for x in edits if x[:1] in "+-")} lines)', text == pin,
       f'first difference at pin line {ctx and first + 1}: pinned {ctx and ctx[0]} | tree {ctx and ctx[1]}')
print('IDENTITY CHECKS PASSED' if not FAIL else f'{len(FAIL)} FAILED: {FAIL}')
sys.exit(1 if FAIL else 0)
