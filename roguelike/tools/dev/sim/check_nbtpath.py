"""Validate NBT path arguments in a datapack against Minecraft's NbtPathArgument grammar.
usage: python3 check_nbtpath.py <datapack root>"""
import os, re, sys

UNQ_STOP = set(' .[]{}"\'')

def skip_compound(s, i):
    # s[i] == '{'; return index after matching '}' (quotes respected)
    depth = 0; q = None
    while i < len(s):
        c = s[i]
        if q:
            if c == '\\': i += 2; continue
            if c == q: q = None
        elif c in '"\'': q = c
        elif c in '{[': depth += 1
        elif c in '}]':
            depth -= 1
            if depth == 0: return i + 1
        i += 1
    raise ValueError('unclosed compound')

def read_name(s, i):
    if i < len(s) and s[i] in '"\'':
        q = s[i]; i += 1
        while i < len(s) and s[i] != q:
            i += 2 if s[i] == '\\' else 1
        if i >= len(s): raise ValueError('unclosed quote')
        return i + 1
    j = i
    while j < len(s) and s[j] not in UNQ_STOP: j += 1
    if j == i: raise ValueError(f'empty name at {i}')
    return j

def parse_path(s):
    """Return end index of the path starting at 0; raise on invalid syntax."""
    i = 0
    if s.startswith('{'):
        i = skip_compound(s, 0)
    elif s.startswith('['):
        pass
    else:
        i = read_name(s, 0)
        if i < len(s) and s[i] == '{': i = skip_compound(s, i)
    while i < len(s) and s[i] not in ' \t':
        c = s[i]
        if c == '.':
            i = read_name(s, i + 1)
            if i < len(s) and s[i] == '{': i = skip_compound(s, i)
        elif c == '[':
            if s[i + 1:i + 2] == ']': i += 2
            elif s[i + 1:i + 2] == '{':
                i = skip_compound(s, i + 1)
                if s[i:i + 1] != ']': raise ValueError(f'expected ] at {i}')
                i += 1
            else:
                m = re.match(r'-?\d+\]', s[i + 1:])
                if not m: raise ValueError(f'bad index at {i}')
                i += 1 + len(m.group(0))
        else:
            raise ValueError(f'invalid path element at {i}: ...{s[max(0,i-20):i+1]}<--')
    return i

def tokens(line):
    """Split respecting [], {}, quotes."""
    out = []; cur = ''; depth = 0; q = None
    for c in line:
        if q:
            cur += c
            if c == q: q = None
            continue
        if c in '"\'': q = c; cur += c; continue
        if c in '[{': depth += 1
        if c in ']}': depth -= 1
        if c == ' ' and depth == 0:
            if cur: out.append(cur); cur = ''
        else: cur += c
    if cur: out.append(cur)
    return out

def target_len(tk, i):
    # tk[i] in storage/entity/block; return number of tokens of the target incl. keyword
    return 4 if tk[i] == 'block' else 2

def paths_in(tk):
    res = []
    n = len(tk)
    for i, t in enumerate(tk):
        if t == 'data' and i + 1 < n and tk[i + 1] in ('get', 'remove', 'modify') and i + 2 < n and tk[i + 2] in ('storage', 'entity', 'block'):
            j = i + 2 + target_len(tk, i + 2)
            if j < n: res.append(tk[j])
            if tk[i + 1] == 'modify' and j + 2 < n and tk[j + 1] in ('set', 'append', 'prepend', 'merge', 'insert'):
                k = j + 2
                if tk[j + 1] == 'insert': k += 1
                if k < n and tk[k] in ('from', 'string') and k + 1 < n and tk[k + 1] in ('storage', 'entity', 'block'):
                    p = k + 1 + target_len(tk, k + 1)
                    if p < n: res.append(tk[p])
        if t in ('if', 'unless') and i + 2 < n and tk[i + 1] == 'data' and tk[i + 2] in ('storage', 'entity', 'block'):
            j = i + 2 + target_len(tk, i + 2)
            if j < n: res.append(tk[j])
        if t == 'store' and i + 2 < n and tk[i + 1] in ('result', 'success') and tk[i + 2] in ('storage', 'entity', 'block'):
            j = i + 2 + target_len(tk, i + 2)
            if j < n: res.append(tk[j])
        if t == 'with' and i + 1 < n and tk[i + 1] in ('storage', 'entity', 'block'):
            j = i + 1 + target_len(tk, i + 1)
            if j < n and tk[j] not in ('run',): res.append(tk[j])
    return res

def main(root):
    bad = 0; checked = 0
    for dp, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.mcfunction'): continue
            p = os.path.join(dp, f)
            for ln, line in enumerate(open(p, encoding='utf8'), 1):
                line = line.strip()
                if not line or line.startswith('#'): continue
                if line.startswith('$'): line = re.sub(r'\$\(\w+\)', '0', line[1:])
                for path in paths_in(tokens(line)):
                    checked += 1
                    try:
                        end = parse_path(path)
                        if end != len(path): raise ValueError(f'trailing text at {end}')
                    except Exception as e:
                        bad += 1
                        print(f'{os.path.relpath(p, root)}:{ln}: {path} -> {e}')
    print(f'nbt paths checked {checked}, invalid {bad}')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
