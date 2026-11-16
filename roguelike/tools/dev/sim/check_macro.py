import re, sys
from pathlib import Path
root = Path('data')
fns = {}
for p in root.glob('*/function/**/*.mcfunction'):
    ns = p.parts[1]; rel = p.relative_to(root/ns/'function').with_suffix('')
    fns[f'{ns}:{rel.as_posix()}'] = p
keys = {}
bad = []
for fid, p in fns.items():
    ks = set()
    for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
        s = line.lstrip()
        if s.startswith('$'):
            found = re.findall(r'\$\(([A-Za-z0-9_]+)\)', s)
            if not found: bad.append(f'{p}:{i} $-line without $(key)')
            ks |= set(found)
        elif '$(' in s and not s.startswith('#'):
            bad.append(f'{p}:{i} $( in non-macro line')
    keys[fid] = ks
scope = sys.argv[1:]
calls = 0
for s in scope:
    for p in (Path(s).rglob('*.mcfunction') if Path(s).is_dir() else [Path(s)]):
        for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
            if line.lstrip().startswith('#'): continue
            for m in re.finditer(r'function ([a-z0-9_.-]+:[a-z0-9_./-]+)( \{[^}]*\})?', line):
                calls += 1
                fid, comp = m.group(1), m.group(2)
                need = keys.get(fid)
                if need is None: bad.append(f'{p}:{i} unknown {fid}'); continue
                given = set(re.findall(r'([A-Za-z0-9_]+):', comp)) if comp else set()
                if need and not comp: bad.append(f'{p}:{i} {fid} needs {sorted(need)} but called without args')
                elif need - given: bad.append(f'{p}:{i} {fid} missing {sorted(need-given)}')
                elif comp and not need: bad.append(f'{p}:{i} {fid} is not a macro but got {comp.strip()}')
for b in bad: print('BAD', b)
print('calls checked', calls, 'problems', len(bad))
