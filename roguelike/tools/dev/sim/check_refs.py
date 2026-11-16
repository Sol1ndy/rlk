"""Static checks: function refs resolve, macro lines start with $, objectives exist."""
import re, sys, pathlib
dp = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/rlk/roguelike')
fn = dp / 'data'
funcs = {}
for p in fn.glob('*/function/**/*.mcfunction'):
    ns = p.relative_to(fn).parts[0]
    rel = p.relative_to(fn / ns / 'function').with_suffix('').as_posix()
    funcs[f'{ns}:{rel}'] = p
tags = {f'{p.relative_to(fn).parts[0]}:{p.relative_to(fn/p.relative_to(fn).parts[0]/"tags/function").with_suffix("").as_posix()}'
        for p in fn.glob('*/tags/function/**/*.json')}
missing, macro_bad = [], []
objs_created, objs_used = set(), set()
for name, p in funcs.items():
    for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if '$(' in s and not s.startswith('$'):
            macro_bad.append(f'{name}:{i}')
        for m in re.finditer(r'function (#?)([a-z0-9_.-]+:[a-z0-9_./-]+)', s):
            ref = m.group(2)
            if '$(' in ref:
                continue
            if m.group(1):
                if ref not in tags:
                    missing.append(f'{name}:{i} -> #{ref}')
            elif ref not in funcs:
                missing.append(f'{name}:{i} -> {ref}')
        for m in re.finditer(r'scoreboard objectives add (\S+)', s):
            objs_created.add(m.group(1))
        if name.startswith('rlk:boss/raiden'):
            for m in re.finditer(r'scoreboard players (?:set|add|remove|operation|get|reset) (\S+) (\S+)', s):
                objs_used.add(m.group(2))
            for m in re.finditer(r'if score (\S+) (\S+)', s):
                objs_used.add(m.group(2))
            for m in re.finditer(r'scores=\{([^}]*)\}', s):
                for kv in m.group(1).split(','):
                    if '=' in kv:
                        objs_used.add(kv.split('=')[0])
print('functions:', len(funcs))
print('missing refs:', len(missing))
for m in missing[:40]:
    print('  ', m)
print('macro lines without $:', macro_bad[:20])
und = sorted(o for o in objs_used if o not in objs_created and not o.startswith('$') and not o.startswith('#') and '(' not in o)
print('raiden objectives used but never created:', und)
