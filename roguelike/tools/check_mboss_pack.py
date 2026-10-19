#!/usr/bin/env python3
"""Static checks for the mid-boss framework and its boss modules (run after the generators).

    python3 tools/check_mboss_pack.py

- every enabled registry entry has a module F:mboss/<id>/ with every contract hook (mboss_lib.HOOKS);
  macro hooks are macro functions, the others are not
- every generated dispatcher F:mboss/d/<hook> calls existing module functions
- every literal "function rlk:..." reference in F:mboss/** resolves; $(...) suffixed references
  (hz/p/c|r|b, pj/h) have their whole numeric family present
- '$' lines carry $(...) and $(...) appears only in '$' lines
- registry ids/numbers are unique and the arena constants agree with the generated arena
- chapter mode (AZ-CM, scratchpad az/contract/cm.md 15.4): every enabled chapter boss has the 17 hooks + prep (not a
  macro); the creg / cbyid lines of F:mboss/register match the registry's enabled chapter entries; every arenas{}
  entry has F:mboss/arena/<aid>/ensure with its stamp string ("<aid>@<ver>:<looks[0]>", or the stub "<aid>@0:stub" when
  its theme module is missing) and the full F:mboss/ar/<aid>/* set; no $(var) inside a function path (dynamic
  references only as a numeric suffix family, which must be contiguous); every proxy key file
  F:mboss/px/<id>/k/<clip>/<t> is reached by its clip's dispatch tree (no orphan from an older manifest); every
  function path under F:mboss and F:room/cboss is a valid lower-case resource location
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
    hooks = L.HOOKS + (L.CHAPTER_HOOKS if b.get('kind', 'mid') == 'chapter' else [])
    for h in hooks:
        rel = f'mboss/{b["id"]}/{h}'
        if rel not in funcs:
            problems.append(f'{b["id"]}: missing hook {rel}')
            continue
        want_macro = h in L.MACRO_HOOKS
        if want_macro != is_macro(rel):
            problems.append(f'{rel}: should {"" if want_macro else "not "}be a macro function')
for h in L.HOOKS:
    rel = f'mboss/d/{h}'
    if rel not in funcs:
        problems.append(f'missing dispatcher {rel}')
for p in sorted((FN / 'mboss').rglob('*.mcfunction')):
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
for p in sorted((FN / 'mboss').rglob('*.mcfunction')) + sorted((FN / 'room/cboss').rglob('*.mcfunction')):
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
for p in sorted((FN / 'mboss').rglob('*.mcfunction')) + sorted((FN / 'room/cboss').rglob('*.mcfunction')):
    rel = p.relative_to(FN).with_suffix('').as_posix()
    if not re.fullmatch(r'[a-z0-9_./-]+', rel):
        problems.append(f'{rel}: not a valid function resource location (lower case a-z 0-9 _ . / - only)')
A = REG['arena']
ens = (FN / 'mboss/arena/ensure.mcfunction')
if not ens.exists() or f'{A["theme"]}@{A["ver"]}' not in ens.read_text(encoding='utf-8'):
    problems.append('arena/ensure is missing or stale: run tools/build_mboss_arena.py')
for p in problems:
    print('PROBLEM', p)
print(f'check_mboss_pack: {len(L.mid_bosses(REG))} enabled mid-boss module(s), {len(chaps)} chapter boss module(s), '
      f'{len(L.arenas(REG))} arena(s), {len(problems)} problem(s).')
sys.exit(1 if problems else 0)
