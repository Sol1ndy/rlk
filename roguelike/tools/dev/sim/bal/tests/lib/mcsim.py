#!/usr/bin/env python3
"""Tiny mcfunction interpreter for offline logic tests (scratch tool, not shipped).

Supports what the mid-boss libraries need: scoreboard players set/add/remove/operation/reset/get,
execute (as/at/positioned [abs|~|^]/rotated/facing entity/if|unless score|entity|data storage/
store result|success score|entity|storage .. run), return [run|fail|N], function [{..}|with storage],
summon marker/others (tags, position, Rotation from NBT), kill, tag, tp (pos/rot, entity), data get
entity Pos/Rotation/storage paths, data modify storage set value/from, macro lines. Unknown commands
(particle, playsound, title, ...) are ignored and counted.
"""
import json
import math
import re
from pathlib import Path


def i32(v):
    v &= 0xffffffff
    return v - (1 << 32) if v & 0x80000000 else v


class Ent:
    _n = 0

    def __init__(self, etype, pos, rot=(0.0, 0.0), tags=()):
        Ent._n += 1
        self.id = Ent._n
        self.etype = etype
        self.pos = list(pos)
        self.rot = list(rot)
        self.tags = set(tags)
        self.alive = True
        self.data = {}


class Ctx:
    def __init__(self, ex, pos, rot):
        self.ex, self.pos, self.rot = ex, tuple(pos), tuple(rot)

    def copy(self, **kw):
        c = Ctx(self.ex, self.pos, self.rot)
        c.anc = getattr(self, 'anc', False)
        for k, v in kw.items():
            setattr(c, k, v)
        return c


def split(s):
    toks, cur, depth, q = [], '', 0, None
    for c in s:
        if q:
            cur += c
            if c == q:
                q = None
        elif c in '"\'':
            q = c
            cur += c
        elif c in '[{':
            depth += 1
            cur += c
        elif c in ']}':
            depth -= 1
            cur += c
        elif c == ' ' and depth == 0:
            if cur:
                toks.append(cur)
            cur = ''
        else:
            cur += c
    if cur:
        toks.append(cur)
    return toks


class Return(Exception):
    def __init__(self, v):
        self.v = v


class Sim:
    def __init__(self, fn_root):
        self.root = Path(fn_root)
        self.scores = {}
        self.ents = []
        self.storage = {}
        self.ignored = {}
        self.cache = {}

    # ---------------------------------------------------------------- helpers
    def block_test(self, pos, pred):
        """`if block <pos> <pred>`: no world by default (every test passes); tests override it."""
        return True

    def sc(self, who, obj):
        return self.scores.get((who, obj))

    def setsc(self, who, obj, v):
        self.scores[(who, obj)] = i32(v)

    def holder(self, t, ctx):
        if t == '@s':
            return ('e', ctx.ex.id) if ctx.ex else None
        if t.startswith('@'):
            e = self.select(t, ctx)
            return ('e', e[0].id) if e else None
        return t

    def holders(self, t, ctx):
        if t.startswith('@') and t != '@s':
            return [('e', e.id) for e in self.select(t, ctx)]
        h = self.holder(t, ctx)
        return [h] if h else []

    def select(self, sel, ctx):
        m = re.match(r'^@([aesp])(?:\[(.*)\])?$', sel)
        kind, body = m.group(1), m.group(2) or ''
        if kind == 's' and not body:
            return [ctx.ex] if ctx.ex and ctx.ex.alive else []
        args = []
        depth, cur = 0, ''
        for c in body:
            if c in '{[':
                depth += 1
            elif c in '}]':
                depth -= 1
            if c == ',' and depth == 0:
                args.append(cur)
                cur = ''
            else:
                cur += c
        if cur:
            args.append(cur)
        res = [e for e in self.ents if e.alive]
        if kind == 's':
            res = [ctx.ex] if ctx.ex and ctx.ex.alive else []
        if kind in ('a', 'p'):
            res = [e for e in res if e.etype == 'player']
        limit, sort = None, None
        vol = {}
        for a in args:
            k, v = a.split('=', 1)
            if k in ('x', 'y', 'z', 'dx', 'dy', 'dz'):
                vol[k] = float(v)
        if any(k in vol for k in ('dx', 'dy', 'dz')):
            o = [vol.get('x', ctx.pos[0]), vol.get('y', ctx.pos[1]), vol.get('z', ctx.pos[2])]
            d = [vol.get('dx', 0.0), vol.get('dy', 0.0), vol.get('dz', 0.0)]
            lo = [o[i] + min(0, d[i]) for i in range(3)]
            hi = [o[i] + max(0, d[i]) + 1 for i in range(3)]

            def hit(e):
                hw, hh = e.data.get('hb', (0.6, 1.8))
                bl = [e.pos[0] - hw / 2, e.pos[1], e.pos[2] - hw / 2]
                bh = [e.pos[0] + hw / 2, e.pos[1] + hh, e.pos[2] + hw / 2]
                return all(bl[i] < hi[i] and bh[i] > lo[i] for i in range(3))
            res = [e for e in res if hit(e)]
        for a in args:
            k, v = a.split('=', 1)
            if k == 'tag':
                res = [e for e in res if (v[1:] not in e.tags) if v.startswith('!')] if v.startswith('!') else [e for e in res if v in e.tags]
            elif k == 'type':
                t = v.replace('minecraft:', '')
                res = [e for e in res if (e.etype != t[1:]) if t.startswith('!')] if t.startswith('!') else [e for e in res if e.etype == t]
            elif k == 'limit':
                limit = int(v)
            elif k == 'sort':
                sort = v
            elif k == 'distance':
                lo, _, hi = v.partition('..') if '..' in v else (v, '', v)
                lo = float(lo) if lo else -1
                hi = float(hi) if hi else 1e9
                res = [e for e in res if lo <= math.dist(e.pos, ctx.pos) <= hi]
            elif k == 'scores':
                for kv in v.strip('{}').split(','):
                    o, r = kv.split('=')
                    res = [e for e in res if self.in_range(self.sc(('e', e.id), o), r)]
            elif k in ('dx', 'dy', 'dz', 'x', 'y', 'z'):
                pass
        if sort == 'nearest':
            res.sort(key=lambda e: math.dist(e.pos, ctx.pos))
        if limit:
            res = res[:limit]
        return res

    @staticmethod
    def in_range(v, r):
        if v is None:
            return False
        if '..' in r:
            lo, hi = r.split('..')
            return (lo == '' or v >= int(lo)) and (hi == '' or v <= int(hi))
        return v == int(r)

    def local(self, ctx, l, u, f):
        yaw, pitch = map(math.radians, ctx.rot)
        fwd = (-math.sin(yaw) * math.cos(pitch), -math.sin(pitch), math.cos(yaw) * math.cos(pitch))
        left = (math.cos(yaw), 0.0, math.sin(yaw))
        up = (fwd[1] * left[2] - fwd[2] * left[1], fwd[2] * left[0] - fwd[0] * left[2], fwd[0] * left[1] - fwd[1] * left[0])
        # fwd x left is already the head's up vector (^ ^1 ^ = +y at pitch 0, as in game)
        return tuple(ctx.pos[i] + l * left[i] + u * up[i] + f * fwd[i] for i in range(3))

    def coords(self, toks, ctx):
        if toks[0].startswith('^'):
            v = [float(t[1:] or 0) for t in toks]
            if getattr(ctx, 'anc', False):     # execute anchored eyes: ^ is relative to the eyes
                eye = ctx.ex.data.get('eye', 1.62) if ctx.ex else 0.0
                ctx = ctx.copy(pos=(ctx.pos[0], ctx.pos[1] + eye, ctx.pos[2]))
            return self.local(ctx, *v)
        out = []
        for i, t in enumerate(toks):
            out.append(ctx.pos[i] + float(t[1:] or 0) if t.startswith('~') else float(t))
        return tuple(out)

    def path_get(self, obj, path):
        for part in re.findall(r'[^.\[\]]+|\[\d+\]', path):
            if part.startswith('['):
                obj = obj[int(part[1:-1])]
            else:
                obj = obj[part]
        return obj

    def data_get(self, toks, ctx):
        if toks[0] == 'entity':
            es = self.select(toks[1], ctx) if toks[1] != '@s' else [ctx.ex]
            e = es[0]
            path, scale = toks[2], float(toks[3]) if len(toks) > 3 else 1
            m = re.match(r'(Pos|Rotation)\[(\d)\]', path)
            if m:
                v = (e.pos if m.group(1) == 'Pos' else e.rot)[int(m.group(2))]
                return math.floor(v * scale)
            return math.floor(float(self.path_get(e.data, path.replace('data.', '', 1))) * scale)
        if toks[0] == 'storage':
            v = self.path_get(self.storage.get(toks[1], {}), toks[2])
            scale = float(toks[3]) if len(toks) > 3 else 1
            if isinstance(v, (list, dict, str)):
                return len(v)
            return math.floor(v * scale)
        raise NotImplementedError(toks)

    # ---------------------------------------------------------------- runner
    def load(self, fid):
        if fid not in self.cache:
            p = self.root / (fid.split(':', 1)[1] + '.mcfunction')
            self.cache[fid] = p.read_text(encoding='utf-8').split('\n')
        return self.cache[fid]

    def call(self, fid, ctx, macro=None):
        try:
            for raw in self.load(fid):
                s = raw.strip()
                if not s or s.startswith('#'):
                    continue
                if s.startswith('$'):
                    s = re.sub(r'\$\((\w+)\)', lambda m: str(macro[m.group(1)]), s[1:])
                self.cmd(split(s), ctx)
        except Return as r:
            return r.v
        return 1

    def cmd(self, t, ctx):
        c = t[0]
        if c == 'execute':
            return self.execute(t[1:], ctx)
        if c == 'return':
            if t[1] == 'run':
                v = self.cmd(t[2:], ctx)
                raise Return(v)
            if t[1] == 'fail':
                raise Return(0)
            raise Return(int(t[1]))
        if c == 'function':
            fid = t[1]
            macro = None
            if len(t) >= 3 and t[2].startswith('{'):
                macro = self.snbt(t[2])
            elif len(t) >= 5 and t[2] == 'with':
                if t[3] == 'storage':
                    macro = self.path_get(self.storage[t[4]], t[5]) if len(t) > 5 else self.storage[t[4]]
                else:
                    e = self.select(t[4], ctx) if t[4] != '@s' else [ctx.ex]
                    macro = e[0].data
            return self.call(fid, ctx, macro)
        if c == 'scoreboard' and t[1] == 'players':
            op = t[2]
            if op in ('set', 'add', 'remove'):
                for h in self.holders(t[3], ctx):
                    v = int(t[5])
                    cur = self.sc(h, t[4]) or 0
                    self.setsc(h, t[4], v if op == 'set' else cur + v if op == 'add' else cur - v)
                return 1
            if op == 'reset':
                for h in self.holders(t[3], ctx):
                    self.scores.pop((h, t[4]), None)
                return 1
            if op == 'get':
                return self.sc(self.holder(t[3], ctx), t[4])
            if op == 'operation':
                src = self.holder(t[6], ctx)
                b = self.sc(src, t[7])
                for h in self.holders(t[3], ctx):
                    a = self.sc(h, t[4]) or 0
                    o = t[5]
                    if b is None:
                        raise RuntimeError(f'unset source score {t[6]} {t[7]}')
                    if o == '=':
                        a = b
                    elif o == '+=':
                        a += b
                    elif o == '-=':
                        a -= b
                    elif o == '*=':
                        a *= b
                    elif o == '/=':
                        a = math.floor(a / b) if b else a
                    elif o == '%=':
                        a = a % b if b else a
                    elif o == '<':
                        a = min(a, b)
                    elif o == '>':
                        a = max(a, b)
                    self.setsc(h, t[4], a)
                return 1
        if c == 'random' and t[1] == 'value':
            import random
            a, b = t[2].split('..')
            return random.randint(int(a), int(b))
        if c == 'summon':
            pos = self.coords(t[2:5], ctx)
            nbt = t[5] if len(t) > 5 else '{}'
            tags = re.findall(r'"([^"]+)"', re.search(r'Tags:\[([^\]]*)\]', nbt).group(1)) if 'Tags:' in nbt else []
            rot = (0.0, 0.0)
            m = re.search(r'Rotation:\[(-?[\d.]+)f?,(-?[\d.]+)f?\]', nbt)
            if m:
                rot = (float(m.group(1)), float(m.group(2)))
            self.ents.append(Ent(t[1].replace('minecraft:', ''), pos, rot, tags))
            return 1
        if c == 'kill':
            for e in self.select(t[1], ctx):
                e.alive = False
            self.ents = [e for e in self.ents if e.alive]
            return 1
        if c == 'tag':
            for e in self.select(t[1], ctx):
                (e.tags.add if t[2] == 'add' else e.tags.discard)(t[3])
            return 1
        if c == 'tp':
            ents = self.select(t[1], ctx)
            if len(t) == 3:
                d = self.select(t[2], ctx)[0]
                for e in ents:
                    e.pos, e.rot = list(d.pos), list(d.rot)
                return 1
            pos = self.coords(t[2:5], ctx)
            for e in ents:
                e.pos = list(pos)
                if len(t) >= 7:
                    e.rot = [ctx.rot[0] + float(t[5][1:] or 0) if t[5].startswith('~') else float(t[5]),
                             ctx.rot[1] + float(t[6][1:] or 0) if t[6].startswith('~') else float(t[6])]
            return 1
        if c == 'data':
            if t[1] == 'get':
                return self.data_get(t[2:], ctx)
            if t[1] == 'modify' and t[2] == 'storage':
                st = self.storage.setdefault(t[3], {})
                path, act = t[4], t[5]
                if t[6] == 'value':
                    val = self.snbt(t[7])
                elif t[6] == 'from':
                    try:
                        if t[7] == 'storage':
                            val = self.path_get(self.storage[t[8]], t[9])
                        else:
                            e = (self.select(t[8], ctx) if t[8] != '@s' else [ctx.ex])
                            if not e:
                                return 0
                            e = e[0]
                            if t[9] == 'data':
                                val = e.data
                            elif t[9].startswith('data.'):
                                val = self.path_get(e.data, t[9][5:])
                            elif t[9] == 'Dimension':
                                val = 'minecraft:overworld'
                            else:
                                val = None
                    except (KeyError, IndexError):
                        return 0
                elif t[6] == 'string':
                    src = self.path_get(self.storage[t[8]], t[9])
                    a = int(t[10]) if len(t) > 10 else 0
                    b = int(t[11]) if len(t) > 11 else len(src)
                    val = src[a:b]
                import copy
                val = copy.deepcopy(val)
                if act == 'set':
                    self.path_set(st, path, val)
                elif act == 'append':
                    try:
                        lst = self.path_get(st, path)
                    except KeyError:
                        lst = []
                        self.path_set(st, path, lst)
                    lst.append(val)
                return 1
            if t[1] == 'remove' and t[2] == 'storage':
                st = self.storage.setdefault(t[3], {})
                parts = __import__('re').findall(r'[^.\[\]]+|\[\d+\]', t[4])
                try:
                    obj = st
                    for q in parts[:-1]:
                        obj = obj[int(q[1:-1])] if q.startswith('[') else obj[q]
                    last = parts[-1]
                    if last.startswith('['):
                        del obj[int(last[1:-1])]
                    else:
                        del obj[last]
                except (KeyError, IndexError):
                    return 0
                return 1
            if t[1] == 'modify' and t[2] == 'entity':
                e = (self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex])[0]
                if t[4].startswith('data.') and t[5] == 'set':
                    val = self.snbt(t[7]) if t[6] == 'value' else self.path_get(self.storage[t[8]], t[9])
                    e.data[t[4][5:]] = val
                return 1
            if t[1] == 'remove':
                return 1
        self.ignored[c] = self.ignored.get(c, 0) + 1
        return 1

    def match(self, actual, pat):
        if isinstance(pat, dict):
            return isinstance(actual, dict) and all(self.match(actual.get(k), v) for k, v in pat.items())
        if isinstance(pat, list):
            return isinstance(actual, list) and all(any(self.match(a, p) for a in actual) for p in pat)
        return actual == pat

    def path_set(self, obj, path, val):
        parts = re.findall(r'[^.\[\]]+|\[\d+\]', path)
        for p in parts[:-1]:
            obj = obj[int(p[1:-1])] if p.startswith('[') else obj.setdefault(p, {})
        last = parts[-1]
        if last.startswith('['):
            obj[int(last[1:-1])] = val
        else:
            obj[last] = val

    @staticmethod
    def snbt(s):
        t = re.sub(r'(?<=[{,])\s*([A-Za-z_][A-Za-z0-9_]*)\s*:', r'"\1":', s)
        t = re.sub(r'(-?\d+(?:\.\d+)?)[bBsSlLfFdD](?=[,\]}]|$)', r'\1', t)
        return json.loads(t)

    def store(self, spec, v, ctx):
        mode, kind = spec[0], spec[1]
        if mode == 'success':
            v = 1 if v else 0
        if v is None:
            v = 0
        if kind == 'score':
            for h in self.holders(spec[2], ctx):
                self.setsc(h, spec[3], int(v))
        elif kind == 'entity':
            e = (self.select(spec[2], ctx) if spec[2] != '@s' else [ctx.ex])[0]
            val = v * float(spec[5])
            m = re.match(r'(Pos|Rotation)\[(\d)\]', spec[3])
            if m:
                (e.pos if m.group(1) == 'Pos' else e.rot)[int(m.group(2))] = val
            elif spec[3].startswith('data.'):
                e.data[spec[3][5:]] = val if spec[4] in ('double', 'float') else int(val)
        elif kind == 'storage':
            val = v * float(spec[5])
            self.path_set(self.storage.setdefault(spec[2], {}), spec[3], val if spec[4] in ('double', 'float') else int(val))

    def execute(self, t, ctx):
        i, stores = 0, []
        while i < len(t):
            k = t[i]
            if k == 'run':
                v = self.cmd(t[i + 1:], ctx)
                for s in stores:
                    self.store(s, v, ctx)
                return v
            if k == 'as':
                ents = self.select(t[i + 1], ctx)
                if not ents:
                    return 0
                rest = t[i + 2:]
                last = 0
                for e in ents:
                    last = self.execute(rest, ctx.copy(ex=e))
                return last
            if k == 'at':
                ents = self.select(t[i + 1], ctx)
                if not ents:
                    return 0
                e = ents[0]
                ctx = ctx.copy(pos=tuple(e.pos), rot=tuple(e.rot))
                i += 2
            elif k == 'positioned':
                if t[i + 1] == 'as':
                    e = self.select(t[i + 2], ctx)[0]
                    ctx = ctx.copy(pos=tuple(e.pos))
                    i += 3
                else:
                    ctx = ctx.copy(pos=self.coords(t[i + 1:i + 4], ctx))
                    i += 4
            elif k == 'rotated':
                if t[i + 1] == 'as':
                    e = self.select(t[i + 2], ctx)[0]
                    ctx = ctx.copy(rot=tuple(e.rot))
                    i += 3
                else:
                    r = [ctx.rot[j] + float(v[1:] or 0) if v.startswith('~') else float(v) for j, v in enumerate(t[i + 1:i + 3])]
                    ctx = ctx.copy(rot=tuple(r))
                    i += 3
            elif k == 'facing':
                e = self.select(t[i + 2], ctx)[0]
                tgt = list(e.pos)
                if t[i + 3] == 'eyes':
                    tgt[1] += e.data.get('eye', 0.0)
                dx, dy, dz = (tgt[j] - ctx.pos[j] for j in range(3))
                yaw = math.degrees(math.atan2(-dx, dz))
                pitch = math.degrees(-math.atan2(dy, math.hypot(dx, dz)))
                ctx = ctx.copy(rot=(yaw, pitch))
                i += 4
            elif k == 'in':
                i += 2
            elif k == 'anchored':
                ctx = ctx.copy(anc=(t[i + 1] == 'eyes'))
                i += 2
            elif k in ('if', 'unless'):
                neg = k == 'unless'
                kind = t[i + 1]
                if kind == 'score':
                    a = self.sc(self.holder(t[i + 2], ctx), t[i + 3])
                    if t[i + 4] == 'matches':
                        ok = self.in_range(a, t[i + 5])
                        i += 6
                    else:
                        b = self.sc(self.holder(t[i + 5], ctx), t[i + 6])
                        op = t[i + 4]
                        ok = a is not None and b is not None and {'<': a < b, '<=': a <= b, '=': a == b, '>=': a >= b, '>': a > b}[op]
                        i += 7
                elif kind == 'entity':
                    ok = bool(self.select(t[i + 2], ctx))
                    i += 3
                elif kind == 'data':
                    try:
                        if t[i + 2] == 'storage':
                            st = self.storage.get(t[i + 3], {})
                            if t[i + 4].startswith('{'):
                                pat = self.snbt(t[i + 4])
                                ok = all(self.match(st.get(k), v) for k, v in pat.items())
                            elif '{' in t[i + 4]:            # path{filter}: the node at path must match the compound
                                pth, flt = t[i + 4].split('{', 1)
                                ok = self.match(self.path_get(st, pth), self.snbt('{' + flt))
                            else:
                                self.path_get(st, t[i + 4])
                                ok = True
                        else:
                            ok = True
                    except (KeyError, IndexError, TypeError):
                        ok = False
                    i += 5
                elif kind == 'function':
                    ok = bool(self.call(t[i + 2], ctx))
                    i += 3
                elif kind == 'loaded':
                    ok = True
                    i += 5
                elif kind == 'block':
                    ok = self.block_test(self.coords(t[i + 2:i + 5], ctx), t[i + 5])
                    i += 6
                else:
                    raise NotImplementedError(kind)
                if ok == neg:
                    return 0
            elif k == 'store':
                n = 4 if t[i + 2] == 'score' else 6
                stores.append(t[i + 1:i + 1 + n + 1] if t[i + 2] != 'score' else t[i + 1:i + 5])
                i += 1 + (4 if t[i + 2] == 'score' else 6)
            else:
                raise NotImplementedError(k)
        v = 1
        for s in stores:
            self.store(s, v, ctx)
        return v
