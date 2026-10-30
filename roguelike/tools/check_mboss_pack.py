#!/usr/bin/env python3
"""Static checks for the mid-boss framework and its boss modules (run after the generators).

    python3 tools/check_mboss_pack.py

- every enabled registry entry has a module F:<fn root>/ (mboss_lib.fn_root: mboss/<id>, or boss/<id> for a chapter
  boss with "fn") with every contract hook (mboss_lib.HOOKS + HELP_HOOKS);
  macro hooks are macro functions, the others are not
- every generated dispatcher F:mboss/d/<hook> calls existing module functions
- every literal "function rlk:..." reference in F:mboss/**, the chapter-boss roots F:boss/<id>/** and the test aliases
  F:boss/test/** resolves; $(...) suffixed references
  (hz/p/c|r|b, pj/h) have their whole numeric family present
- '$' lines carry $(...) and $(...) appears only in '$' lines
- registry ids/numbers are unique and the arena constants agree with the generated arena
- chapter mode (AZ-CM, scratchpad az/contract/cm.md 15.4): every enabled chapter boss has the 17 hooks + prep (not a
  macro); the creg / cbyid lines of F:mboss/register match the registry's enabled chapter entries; every arenas{}
  entry has F:mboss/arena/<aid>/ensure with its stamp string ("<aid>@<ver>:<looks[0]>", or the stub "<aid>@0:stub" when
  its theme module is missing) and the full F:mboss/ar/<aid>/* set; no $(var) inside a function path (dynamic
  references only as a numeric suffix family, which must be contiguous); every proxy key file
  F:mboss/px/<id>/k/<clip>/<t> is reached by its clip's dispatch tree (no orphan from an older manifest); every
  function path under F:mboss, the boss/<id> roots, F:boss/test and F:room/cboss is a valid lower-case resource location
- special bosses (Tachy S1, scratchpad tk/PLAN.md §7-8): every enabled special has the 17 hooks + test/help (+
  mboss_lib.SPECIAL_HOOKS), the sreg / sbyid lines of F:mboss/register and #spN / #spRoll match the enabled special entries,
  each one has its F:mboss/sp/pp/<id>, sp/g/<id> and cb/inc/<id> (incoming through the floor) and every dispatcher
  F:mboss/d/<hook> names it; the frozen runtime names of contract §3.1 exist; the rift F:room/rift/** + room/obj/k_rift
  follow the same reference / macro / resource-location rules, and every shared hook line of tools/build_rift.py is in
  its file exactly once, right after the marker comment
Exit code 1 on any problem.
"""
import re
import sys
import mboss_lib as L

problems = []
REG = L.load_registry()
FN = L.FN
funcs = {p.relative_to(FN).with_suffix('').as_posix() for p in FN.rglob('*.mcfunction')}


def is_macro(rel):
    return any(l.lstrip().startswith('$') for l in (FN / (rel + '.mcfunction')).read_text(encoding='utf-8').split('\n'))


for b in L.enabled_bosses(REG):
    hooks = L.HOOKS + L.HELP_HOOKS + (L.CHAPTER_HOOKS if b.get('kind', 'mid') == 'chapter' else []) \
        + (L.SPECIAL_HOOKS if b.get('kind', 'mid') == 'special' else [])
    for h in hooks:
        rel = f'{L.fn_root(b)}/{h}'
        if rel not in funcs:
            problems.append(f'{b["id"]}: missing hook {rel}')
            continue
        want_macro = h in L.MACRO_HOOKS
        if want_macro != is_macro(rel):
            problems.append(f'{rel}: should {"" if want_macro else "not "}be a macro function')
for h in L.HOOKS + [h.replace('/', '_') for h in L.HELP_HOOKS]:
    rel = f'mboss/d/{h}'
    if rel not in funcs:
        problems.append(f'missing dispatcher {rel}')
# every tree the framework and its modules generate: F:mboss/**, each module root outside it (boss/<id>), the aliases
ROOTS = ['mboss'] + sorted({L.fn_root(b) for b in REG['boss'] if not L.fn_root(b).startswith('mboss/')}) + ['boss/test']
# the rift (Tachy S1, tools/build_rift.py): its tree and its hover object
ROOTS += ['room/rift']
SCAN = [p for r in ROOTS if (FN / r).exists() for p in sorted((FN / r).rglob('*.mcfunction'))]
SCAN += [FN / 'room/obj/k_rift.mcfunction'] if (FN / 'room/obj/k_rift.mcfunction').exists() else []
for p in SCAN:
    rel = p.relative_to(FN).with_suffix('').as_posix()
    for i, line in enumerate(p.read_text(encoding='utf-8').split('\n'), 1):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('$') and '$(' not in s:
            problems.append(f'{rel}:{i} $ line without $(...)')
        if not s.startswith('$') and '$(' in s:
            problems.append(f'{rel}:{i} $(...) in a non-macro line')
        for m in re.finditer(r'function (rlk:[a-z0-9_./-]+)(\$\(\w+\))?', s):
            ref = m.group(1)[4:]
            if m.group(2):
                fam = [f for f in funcs if f.startswith(ref) and f[len(ref):].isdigit()]
                if not fam:
                    problems.append(f'{rel}:{i} no functions for dynamic reference {m.group(0)}')
                else:
                    nums = sorted(int(f[len(ref):]) for f in fam)
                    if nums != list(range(nums[0], nums[-1] + 1)):
                        problems.append(f'{rel}:{i} gaps in {ref}<n>: {nums[0]}..{nums[-1]}')
            elif ref not in funcs:
                problems.append(f'{rel}:{i} missing function rlk:{ref}')
# ranges the runtime clamps to
for fam, lo, hi in (('mboss/hz/p/c/', 1, 60), ('mboss/hz/p/r/', 1, 90), ('mboss/hz/p/b/', 1, 40), ('mboss/pj/h/', 1, 40)):
    missing = [n for n in range(lo, hi + 1) if f'{fam}{n}' not in funcs]
    if missing:
        problems.append(f'{fam}: missing {missing[:5]}...')
# chapter mode
reg_txt = (FN / 'mboss/register.mcfunction').read_text(encoding='utf-8') if (FN / 'mboss/register.mcfunction').exists() else ''
chaps = L.chapter_bosses(REG)
m = re.search(r'^data modify storage rlk:mboss creg set value \[(.*)\]$', reg_txt, re.M)
ids = re.findall(r'(?:^|\},)\{id:"([^"]+)"', m.group(1)) if m and m.group(1) else []
if sorted(ids) != sorted(b['id'] for b in chaps):
    problems.append(f'register: creg {ids} != enabled chapter entries {[b["id"] for b in chaps]}')
for b in chaps:
    if f'{b["id"]}:{{id:"{b["id"]}",n:{b["n"]},' not in reg_txt:
        problems.append(f'register: cbyid.{b["id"]} missing or stale')
for b in L.mid_bosses(REG):
    if f'id:"{b["id"]}"' in (m.group(1) if m else ''):
        problems.append(f'register: mid-boss {b["id"]} in creg')
AR_FNS = ['marker', 'oob', 'sweep', 'box_absorb', 'ok', 'clamp', 'clamp_step', 'clampw', 'clampw_step', 'leash',
          'full_rim', 'tp_in', 'fl_on', 'fl_off', 'loaded', 'ensure', 'test']
for aid, a in L.arenas(REG):
    for f in AR_FNS:
        if f'mboss/ar/{aid}/{f}' not in funcs:
            problems.append(f'arena {aid}: missing F:mboss/ar/{aid}/{f}')
    if aid == 'plaza':
        continue
    e = FN / f'mboss/arena/{aid}/ensure.mcfunction'
    want = f'{aid}@{a["ver"]}:{a["looks"][0]}' if L.theme_module(a['theme']) else f'{aid}@0:stub'
    if not e.exists() or want not in e.read_text(encoding='utf-8'):
        problems.append(f'arena {aid}: F:mboss/arena/{aid}/ensure missing or without the stamp {want}')
for p in SCAN + sorted((FN / 'room/cboss').rglob('*.mcfunction')):
    rel = p.relative_to(FN).with_suffix('').as_posix()
    for i, line in enumerate(p.read_text(encoding='utf-8').split('\n'), 1):
        if re.search(r'function rlk:[a-z0-9_./-]*\$\(\w+\)[a-z0-9_./-]', line):
            problems.append(f'{rel}:{i} $(var) inside a function path (use literal dispatch lines)')
for b in chaps:
    if not b.get('px'):
        continue
    base = f'mboss/px/{b["id"]}/'
    keys = {f for f in funcs if f.startswith(base + 'k/')}
    reached = set()
    for f in funcs:
        if f.startswith((base + 't/', base + 'c/')):
            reached |= set(re.findall(r'function rlk:(' + re.escape(base) + r'k/\d+/\d+)\b', (FN / (f + '.mcfunction')).read_text(encoding='utf-8')))
    for k in sorted(keys - reached):
        problems.append(f'{k}: proxy key file not reached by its clip dispatch (stale output?)')
for p in SCAN + sorted((FN / 'room/cboss').rglob('*.mcfunction')):
    rel = p.relative_to(FN).with_suffix('').as_posix()
    if not re.fullmatch(r'[a-z0-9_./-]+', rel):
        problems.append(f'{rel}: not a valid function resource location (lower case a-z 0-9 _ . / - only)')
# special bosses (Tachy S1)
specs = L.special_bosses(REG)
m = re.search(r'^data modify storage rlk:mboss sreg set value \[(.*)\]$', reg_txt, re.M)
ids = re.findall(r'(?:^|\},)\{id:"([^"]+)"', m.group(1)) if m and m.group(1) else []
if sorted(ids) != sorted(b['id'] for b in specs):
    problems.append(f'register: sreg {ids} != enabled special entries {[b["id"] for b in specs]}')
for k, v in (('#spN', len(specs)), ('#spRoll', sum(1 for b in specs if b['w'] >= 1))):
    if specs and f'scoreboard players set {k} mb {v}' not in reg_txt:
        problems.append(f'register: {k} mb {v} missing')
for b in specs:
    if f'{b["id"]}:{{id:"{b["id"]}",n:{b["n"]},' not in reg_txt:
        problems.append(f'register: sbyid.{b["id"]} missing or stale')
    for f in (f'mboss/sp/pp/{b["id"]}', f'mboss/sp/g/{b["id"]}', f'mboss/cb/inc/{b["id"]}'):
        if f not in funcs:
            problems.append(f'special {b["id"]}: missing F:{f}')
    for h in L.HOOKS:
        d = FN / f'mboss/d/{h}.mcfunction'
        if d.exists() and f'matches {b["n"]} run' not in d.read_text(encoding='utf-8') and h not in L.ALL_MODULE_HOOKS:
            problems.append(f'special {b["id"]}: dispatcher mboss/d/{h} does not name n {b["n"]}')
    if L.arena_of(b, REG)['aid'] == 'plaza':
        problems.append(f'special {b["id"]}: fights in the plaza (a special needs its own arena)')
for f in ['mboss/sp/' + n for n in ('roll', 'prep', 'gate', 'start_zone', 'start', 'wait', 'ret_rift', 'won', 'won_kill',
                                     'won_cancel', 'clear', 'reward', 'lvup', 'forget', 'run_reset')] \
        + ['mboss/test/' + n for n in ('rift', 'rift_id', 'rift_id_do', 'special', 'special_ch', 'help_special')] \
        + ['boss/test/' + n for n in ('rift', 'rift_id', 'special', 'special_ch')] \
        + ['room/rift/' + n for n in ('init', 'roll', 'arm', 'show', 'open', 'reopen', 'close', 'tick', 'enter', 'click',
                                       'forget', 'uninstall')] + ['room/obj/k_rift']:
    if f not in funcs:
        problems.append(f'missing frozen runtime name F:{f} (contract 3.1)')
try:
    import build_rift as BR
    for rel, _mode, _anchor, line in BR.HOOKS:
        lines = (FN / (rel + '.mcfunction')).read_text(encoding='utf-8').split('\n')
        at = [i for i, x in enumerate(lines) if x == line]
        if len(at) != 1 or at[0] == 0 or lines[at[0] - 1] != BR.MARK:
            problems.append(f'{rel}: rift hook line missing, doubled or unmarked: {line}')
        for ref in re.findall(r'function (rlk:[a-z0-9_./-]+)', line):
            if ref[4:] not in funcs:
                problems.append(f'{rel}: rift hook line names a missing function {ref}')
except ImportError as e:
    problems.append(f'tools/build_rift.py not importable: {e}')
A = REG['arena']
ens = (FN / 'mboss/arena/ensure.mcfunction')
if not ens.exists() or f'{A["theme"]}@{A["ver"]}' not in ens.read_text(encoding='utf-8'):
    problems.append('arena/ensure is missing or stale: run tools/build_mboss_arena.py')
for p in problems:
    print('PROBLEM', p)
print(f'check_mboss_pack: {len(L.mid_bosses(REG))} enabled mid-boss module(s), {len(chaps)} chapter boss module(s), '
      f'{len(specs)} special boss module(s), {len(L.arenas(REG))} arena(s), {len(problems)} problem(s).')
sys.exit(1 if problems else 0)
