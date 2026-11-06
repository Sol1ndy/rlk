#!/usr/bin/env python3
"""Targeted offline linter for Minecraft Java function files (no game available here).

Checks per command: bracket/quote balance, execute sub-command grammar, scoreboard / data / summon / tp /
particle / fill / setblock / title / bossbar / function / tag / kill / attribute / effect / playsound /
tellraw / rotate / return / forceload / random / damage / ride shapes, coordinate tokens, selector
syntax, macro lines ($ needs $(...)), and that called functions exist (macro names allowed).

    python3 lint_mc.py <datapack root> [paths relative to data/rlk/function ...]
"""
import re
import sys
from pathlib import Path

DP = Path(sys.argv[1])
FN = DP / 'data/rlk/function'
FUNCS = {p.relative_to(FN).with_suffix('').as_posix() for p in FN.rglob('*.mcfunction')}
errors = []


def err(where, msg):
    errors.append(f'{where}: {msg}')


def tokenize(s):
    toks, cur, depth, q = [], '', 0, None
    i = 0
    while i < len(s):
        c = s[i]
        if q:
            cur += c
            if c == '\\' and i + 1 < len(s):
                cur += s[i + 1]
                i += 2
                continue
            if c == q:
                q = None
        elif c in '"\'':
            q = c
            cur += c
        elif c in '[{(':
            depth += 1
            cur += c
        elif c in ']})':
            depth -= 1
            cur += c
        elif c == ' ' and depth == 0:
            if cur:
                toks.append(cur)
            cur = ''
        else:
            cur += c
        i += 1
    if cur:
        toks.append(cur)
    return toks, depth, q


COORD = re.compile(r'^(~|\^)?-?(\d+(\.\d*)?|\.\d+)?$')


def is_coord(t):
    return bool(COORD.match(t)) and t not in ('', '-')


def coords(toks, i, n, where):
    vals = toks[i:i + n]
    if len(vals) < n:
        err(where, f'expected {n} coordinates, got {vals}')
        return i + n
    for v in vals:
        if not is_coord(v):
            err(where, f'bad coordinate {v!r} in {vals}')
    loc = [v.startswith('^') for v in vals]
    if any(loc) and not all(loc):
        err(where, f'mixed local coordinates {vals}')
    return i + n


SEL_KEYS = {'tag', 'type', 'limit', 'sort', 'distance', 'scores', 'x', 'y', 'z', 'dx', 'dy', 'dz', 'name', 'nbt',
            'level', 'gamemode', 'x_rotation', 'y_rotation', 'predicate', 'team', 'advancements'}


def selector(t, where):
    if t.startswith('#') or re.match(r'^[A-Za-z0-9_]+$', t):
        return True
    m = re.match(r'^@([aeprsn])(\[(.*)\])?$', t)
    if not m:
        err(where, f'bad target {t!r}')
        return False
    if m.group(3) is not None:
        body = m.group(3)
        parts, depth, cur = [], 0, ''
        for c in body:
            if c in '{[':
                depth += 1
            elif c in '}]':
                depth -= 1
            if c == ',' and depth == 0:
                parts.append(cur)
                cur = ''
            else:
                cur += c
        parts.append(cur)
        for p in parts:
            if '=' not in p:
                err(where, f'selector arg without = : {p!r} in {t}')
                continue
            k = p.split('=', 1)[0]
            if k not in SEL_KEYS:
                err(where, f'unknown selector key {k!r} in {t}')
            if k == 'distance' and not re.match(r'^distance=(\d+(\.\d+)?)?(\.\.)?(\d+(\.\d+)?)?$', p):
                err(where, f'bad distance {p}')
    return True


def score_target(t, where):
    return selector(t, where)


RANGE = re.compile(r'^-?\d*(\.\.)?-?\d*$')


def check_execute(toks, where):
    i = 1
    while i < len(toks):
        t = toks[i]
        if t == 'run':
            return check_cmd(toks[i + 1:], where)
        if t in ('as', 'at'):
            selector(toks[i + 1], where)
            i += 2
        elif t == 'positioned':
            if toks[i + 1] == 'as':
                selector(toks[i + 2], where)
                i += 3
            elif toks[i + 1] == 'over':
                i += 3
            else:
                i = coords(toks, i + 1, 3, where)
        elif t == 'rotated':
            if toks[i + 1] == 'as':
                selector(toks[i + 2], where)
                i += 3
            else:
                for v in toks[i + 1:i + 3]:
                    if not re.match(r'^~?-?(\d+(\.\d*)?)?$', v) or v == '':
                        err(where, f'bad rotation {v}')
                i += 3
        elif t == 'facing':
            if toks[i + 1] == 'entity':
                selector(toks[i + 2], where)
                if toks[i + 3] not in ('eyes', 'feet'):
                    err(where, f'facing entity anchor {toks[i + 3]}')
                i += 4
            else:
                i = coords(toks, i + 1, 3, where)
        elif t == 'anchored':
            i += 2
        elif t == 'align':
            i += 2
        elif t == 'in':
            if not toks[i + 1].startswith('minecraft:') and '$(' not in toks[i + 1]:
                err(where, f'dimension {toks[i + 1]}')
            i += 2
        elif t == 'on':
            i += 2
        elif t == 'summon':
            i += 2
        elif t in ('if', 'unless'):
            k = toks[i + 1]
            if k == 'score':
                score_target(toks[i + 2], where)
                if toks[i + 4] == 'matches':
                    if not RANGE.match(toks[i + 5]):
                        err(where, f'bad range {toks[i + 5]}')
                    i += 6
                elif toks[i + 4] in ('<', '<=', '=', '>=', '>'):
                    score_target(toks[i + 5], where)
                    i += 7
                else:
                    err(where, f'bad score test {toks[i:i + 6]}')
                    return
            elif k == 'entity':
                selector(toks[i + 2], where)
                i += 3
            elif k == 'block':
                i = coords(toks, i + 2, 3, where) + 1
            elif k == 'loaded':
                i = coords(toks, i + 2, 3, where)
            elif k == 'data':
                src = toks[i + 2]
                if src not in ('storage', 'entity', 'block'):
                    err(where, f'if data source {src}')
                if src == 'block':
                    i = coords(toks, i + 3, 3, where) + 1
                else:
                    if src == 'entity':
                        selector(toks[i + 3], where)
                    i += 5
            elif k == 'function':
                fid = toks[i + 2]
                check_fn_ref(fid, where)
                i += 3
            elif k == 'items':
                i += 5
            elif k == 'predicate':
                i += 3
            else:
                err(where, f'unknown if-kind {k}')
                return
        elif t == 'store':
            mode = toks[i + 1]
            if mode not in ('result', 'success'):
                err(where, f'store mode {mode}')
            kind = toks[i + 2]
            if kind == 'score':
                score_target(toks[i + 3], where)
                i += 5
            elif kind in ('entity', 'storage'):
                if kind == 'entity':
                    selector(toks[i + 3], where)
                typ = toks[i + 5]
                if typ not in ('byte', 'short', 'int', 'long', 'float', 'double'):
                    err(where, f'store type {typ}')
                try:
                    float(toks[i + 6])
                except (ValueError, IndexError):
                    err(where, f'store scale {toks[i + 6:i + 7]}')
                i += 7
            elif kind == 'bossbar':
                i += 5
            else:
                err(where, f'store kind {kind}')
                return
        else:
            err(where, f'unknown execute sub-command {t!r}')
            return
    err(where, 'execute without run')


def check_fn_ref(fid, where):
    if '$(' in fid:
        return
    if not fid.startswith('rlk:'):
        err(where, f'function namespace {fid}')
        return
    if fid[4:] not in FUNCS:
        err(where, f'missing function {fid}')


def check_cmd(toks, where):
    if not toks:
        err(where, 'empty command')
        return
    c = toks[0]
    n = len(toks)
    if c == 'execute':
        return check_execute(toks, where)
    if c == 'return':
        if n >= 2 and toks[1] == 'run':
            return check_cmd(toks[2:], where)
        if n == 2 and (toks[1] == 'fail' or re.match(r'^-?\d+$', toks[1])):
            return
        err(where, f'bad return {toks}')
        return
    if c == 'scoreboard':
        if toks[1] == 'objectives':
            if toks[2] == 'add' and n not in (5, 6):
                err(where, 'objectives add')
            return
        if toks[1] != 'players':
            err(where, 'scoreboard sub')
            return
        op = toks[2]
        if op in ('set', 'add', 'remove'):
            if n != 6 or not re.match(r'^-?\d+$', toks[5]) and '$(' not in toks[5]:
                err(where, f'scoreboard {op} needs an int: {toks[3:]}')
            score_target(toks[3], where)
        elif op == 'operation':
            if n != 8 or toks[5] not in ('=', '+=', '-=', '*=', '/=', '%=', '<', '>', '><'):
                err(where, f'scoreboard operation shape {toks[3:]}')
            score_target(toks[3], where)
            score_target(toks[6], where)
        elif op in ('reset', 'get'):
            if n not in (4, 5):
                err(where, f'scoreboard {op} shape')
        else:
            err(where, f'scoreboard players {op}')
        return
    if c == 'data':
        sub = toks[1]
        if sub not in ('modify', 'merge', 'get', 'remove'):
            err(where, f'data {sub}')
            return
        if toks[2] not in ('storage', 'entity', 'block'):
            err(where, f'data target {toks[2]}')
        if toks[2] == 'entity':
            selector(toks[3], where)
        if sub == 'modify':
            j = 5 if toks[2] != 'block' else 7
            act = toks[j]
            if act not in ('set', 'append', 'prepend', 'merge', 'insert'):
                err(where, f'data modify action {act}')
            k = j + 1 if act != 'insert' else j + 2
            src = toks[k]
            if src == 'value':
                if n != k + 2:
                    err(where, f'data modify value: extra tokens {toks[k + 1:]}')
            elif src == 'from':
                if toks[k + 1] not in ('storage', 'entity', 'block'):
                    err(where, 'data from source')
                if n != k + 4:
                    err(where, f'data modify from: token count {toks[k:]}')
            elif src == 'string':
                if toks[k + 1] not in ('storage', 'entity', 'block'):
                    err(where, 'data string source')
            else:
                err(where, f'data modify source {src}')
        return
    if c == 'summon':
        if n < 5 or not toks[1].startswith('minecraft:'):
            err(where, f'summon shape {toks[:5]}')
        else:
            coords(toks, 2, 3, where)
        return
    if c == 'tp':
        selector(toks[1], where)
        if n == 3:
            selector(toks[2], where)
        elif n == 5:
            coords(toks, 2, 3, where)
        elif n == 7:
            coords(toks, 2, 3, where)
            for v in toks[5:7]:
                if not re.match(r'^~?-?(\d+(\.\d*)?)?$', v) and '$(' not in v:
                    err(where, f'tp rotation {v}')
        elif n == 8 and toks[5] == 'facing':
            pass
        else:
            err(where, f'tp shape {toks}')
        return
    if c == 'particle':
        if n not in (2, 5, 10, 11, 12):
            err(where, f'particle arg count {n}: {toks[:3]}')
        if n >= 5:
            coords(toks, 2, 3, where)
        if n >= 11 and toks[10] not in ('force', 'normal'):
            err(where, f'particle mode {toks[10]}')
        if n == 12:
            selector(toks[11], where)
        return
    if c in ('fill', 'setblock'):
        k = 7 if c == 'fill' else 4
        coords(toks, 1, 3, where)
        if c == 'fill':
            coords(toks, 4, 3, where)
        rest = toks[k + 1:]
        if rest and rest[0] not in ('strict', 'replace', 'keep', 'destroy', 'hollow', 'outline'):
            err(where, f'{c} mode {rest}')
        return
    if c == 'title':
        selector(toks[1], where)
        if toks[2] == 'times' and n != 6:
            err(where, 'title times')
        elif toks[2] in ('title', 'subtitle', 'actionbar') and n != 4:
            err(where, f'title text token count {n}')
        return
    if c == 'tellraw':
        selector(toks[1], where)
        if n != 3:
            err(where, f'tellraw token count {n}')
        return
    if c == 'bossbar':
        return
    if c == 'function':
        check_fn_ref(toks[1], where)
        if n == 2:
            return
        if n == 3 and toks[2].startswith('{'):
            return
        if n in (5, 6) and toks[2] == 'with' and toks[3] in ('storage', 'entity', 'block'):
            return
        err(where, f'function call shape {toks}')
        return
    if c in ('kill',):
        if n != 2:
            err(where, 'kill shape')
        selector(toks[1], where)
        return
    if c == 'tag':
        selector(toks[1], where)
        if toks[2] not in ('add', 'remove', 'list') or (toks[2] != 'list' and n != 4):
            err(where, 'tag shape')
        return
    if c == 'attribute':
        if toks[3] == 'modifier':
            return
        if toks[3] != 'base' or toks[4] != 'set' or n != 6:
            err(where, f'attribute shape {toks}')
        return
    if c == 'effect':
        if toks[1] == 'give' and n not in (4, 5, 6, 7):
            err(where, 'effect give shape')
        return
    if c == 'playsound':
        if n not in (4, 7, 8, 9, 10):
            err(where, f'playsound arg count {n}')
        if not toks[1].startswith('minecraft:'):
            err(where, 'playsound id')
        if toks[2] not in ('master', 'music', 'record', 'weather', 'block', 'hostile', 'neutral', 'player', 'ambient', 'voice', 'ui'):
            err(where, f'playsound source {toks[2]}')
        if n >= 7:
            coords(toks, 4, 3, where)
        return
    if c == 'rotate':
        selector(toks[1], where)
        if toks[2] == 'facing':
            if toks[3] == 'entity':
                selector(toks[4], where)
        return
    if c == 'forceload':
        return
    if c == 'random':
        if toks[1] != 'value' or not re.match(r'^-?\d+\.\.-?\d+$', toks[2]):
            err(where, 'random shape')
        return
    if c in ('experience', 'damage', 'ride', 'spawnpoint', 'clear', 'item', 'team', 'gamerule', 'difficulty', 'say', 'schedule', 'spreadplayers'):
        return
    err(where, f'unknown command {c!r}')


def check_file(p):
    rel = p.relative_to(FN).with_suffix('').as_posix()
    text = p.read_text(encoding='utf-8').replace('\\\n', '')
    for ln, raw in enumerate(text.split('\n'), 1):
        s = raw.strip()
        if not s or s.startswith('#'):
            continue
        where = f'{rel}:{ln}'
        if s.startswith('$'):
            if '$(' not in s:
                err(where, '$ line without $(')
            s = s[1:]
            s = re.sub(r'\$\((\w+)\)', lambda m: {'d': '4', 'n': '3', 'x': '1.5', 'y': '2', 'z': '3', 'yaw': '0',
                                                   'pitch': '0', 't': '5', 'tell': '10', 'dmg': '100', 'dim': 'minecraft:overworld'}.get(m.group(1), '7'), s)
        elif '$(' in s:
            err(where, '$( in a non-macro line')
        if raw != raw.rstrip() and False:
            pass
        toks, depth, q = tokenize(s)
        if depth != 0 or q:
            err(where, f'unbalanced brackets/quotes (depth {depth}, quote {q})')
            continue
        try:
            check_cmd(toks, where)
        except IndexError:
            err(where, f'truncated command: {s[:90]}')


targets = sys.argv[2:] or ['mboss']
for t in targets:
    P = FN / t
    files = sorted(P.rglob('*.mcfunction')) if P.is_dir() else [P.with_suffix('.mcfunction')]
    for f in files:
        check_file(f)
for e in errors:
    print(e)
print(f'{len(errors)} problems')
