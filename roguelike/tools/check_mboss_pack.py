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
    for h in L.HOOKS:
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
A = REG['arena']
ens = (FN / 'mboss/arena/ensure.mcfunction')
if not ens.exists() or f'{A["theme"]}@{A["ver"]}' not in ens.read_text(encoding='utf-8'):
    problems.append('arena/ensure is missing or stale: run tools/build_mboss_arena.py')
for p in problems:
    print('PROBLEM', p)
print(f'check_mboss_pack: {len(L.enabled_bosses(REG))} enabled mid-boss module(s), {len(problems)} problem(s).')
sys.exit(1 if problems else 0)
