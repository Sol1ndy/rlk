#!/usr/bin/env python3
"""psim.py: a per-function command counter for the player / item systems (scratch tool, never shipped).

mcsim (copy of tools/dev/sim/ar/tests/lib/mcsim.py, read only) + a real SNBT reader (from tools/dev/sim/hr/sr/srsim.py)
+ a player inventory model (slots, `if|unless items`, `clear`, `item replace|modify`, `give`) that fires the
inventory_changed advancement (rlk:player/inv/dirty) right after any command that changes a player slot (ItemCommands
broadcasts at once), + attribution: inclusive / self command counts per function id, macro instantiations per id with
the distinct argument sets seen.

Vendored for tools/dev/sim/cb/tests (lane R, 11-10) from tools/dev/plan/combat/perf_harness/psim.py with two changes: mcsim
is imported from this folder (lib/mcsim.py = that harness's copy of ar/tests/lib/mcsim.py: unset source scores read 0),
and `data modify storage ... set` that leaves the value as it was returns 0 (the game fails it: ERROR_MERGE_UNCHANGED;
`execute store success` loops such as items/migrate_loop rely on that).
"""
import collections
import copy
import json
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))          # (cb/tests/lib: the mcsim copy sits beside this file)
import mcsim  # noqa: E402
from mcsim import Ent, Ctx, split  # noqa: E402


# ------------------------------------------------------------------ SNBT (from srsim.py)
class Byte(int):
    pass


_NUM = re.compile(r'^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?([bBsSlLfFdD])?$')
_UNQ = re.compile(r'[A-Za-z0-9._+\-:]')


class _P:
    def __init__(self, s, i=0):
        self.s, self.i = s, i

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in ' \t\r\n':
            self.i += 1

    def peek(self):
        self.ws()
        return self.s[self.i] if self.i < len(self.s) else ''

    def eat(self, c):
        self.ws()
        if self.s[self.i] != c:
            raise ValueError(f'SNBT: expected {c!r} at {self.i}: {self.s[max(0, self.i - 30):self.i + 30]!r}')
        self.i += 1

    def string(self):
        q = self.s[self.i]
        self.i += 1
        out = []
        while True:
            c = self.s[self.i]
            if c == '\\':
                n = self.s[self.i + 1]
                if n == 'u':
                    out.append(chr(int(self.s[self.i + 2:self.i + 6], 16)))
                    self.i += 6
                    continue
                out.append({'n': '\n', 't': '\t'}.get(n, n))
                self.i += 2
                continue
            self.i += 1
            if c == q:
                return ''.join(out)
            out.append(c)

    def value(self):
        c = self.peek()
        if c == '{':
            self.i += 1
            d = {}
            if self.peek() == '}':
                self.i += 1
                return d
            while True:
                self.ws()
                k = self.string() if self.s[self.i] in '"\'' else self.word(key=True)
                self.eat(':')
                d[k] = self.value()
                if self.peek() == ',':
                    self.i += 1
                    if self.peek() == '}':
                        self.i += 1
                        return d
                    continue
                self.eat('}')
                return d
        if c == '[':
            self.i += 1
            self.ws()
            if re.match(r'[BIL];', self.s[self.i:self.i + 2]):
                self.i += 2
            lst = []
            if self.peek() == ']':
                self.i += 1
                return lst
            while True:
                lst.append(self.value())
                if self.peek() == ',':
                    self.i += 1
                    if self.peek() == ']':
                        self.i += 1
                        return lst
                    continue
                self.eat(']')
                return lst
        if c in '"\'':
            return self.string()
        w = self.word()
        if w in ('true', 'false'):
            return Byte(1 if w == 'true' else 0)
        m = _NUM.match(w)
        if m:
            suf = (m.group(1) or '').lower()
            body = w[:-1] if m.group(1) else w
            if suf == 'b':
                return Byte(int(float(body)))
            if suf in ('f', 'd') or '.' in body or 'e' in body.lower():
                return float(body)
            return int(body)
        return w

    def word(self, key=False):
        self.ws()
        j = self.i
        pat = re.compile(r'[A-Za-z0-9._+\-]') if key else _UNQ
        while self.i < len(self.s) and pat.match(self.s[self.i]):
            self.i += 1
        if j == self.i:
            raise ValueError(f'SNBT: unexpected {self.s[self.i:self.i + 20]!r} at {self.i}')
        return self.s[j:self.i]


def snbt_parse(s):
    p = _P(s)
    v = p.value()
    p.ws()
    if p.i != len(s):
        raise ValueError(f'SNBT: trailing text {s[p.i:p.i + 30]!r}')
    return v


def _q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def snbt_dump(v, top=False):
    if isinstance(v, Byte) or isinstance(v, bool):
        return f'{int(v)}b'
    if isinstance(v, str):
        return v if top else _q(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        if top:
            # a macro argument (MacroFunction.stringify, 26.3 bytecode): floats and doubles go through a DecimalFormat - no 'd'
            # suffix, no exponent (round W: player/dash_sub's ~$(dx) took '0.125d' here and the move was never simulated)
            t = ('%.15f' % v).rstrip('0').rstrip('.')
            return '0' if t in ('', '-0') else t
        return f'{v}d'
    if isinstance(v, dict):
        return '{' + ','.join((k if re.fullmatch(r'[A-Za-z0-9._+\-]+', k) else _q(k)) + ':' + snbt_dump(x)
                              for k, x in v.items()) + '}'
    if isinstance(v, list):
        return '[' + ','.join(snbt_dump(x) for x in v) + ']'
    raise TypeError(type(v))


def _sub(s, macro):
    return re.sub(r'\$\((\w+)\)', lambda m: snbt_dump(macro[m.group(1)], top=True), s)


# ------------------------------------------------------------------ item stacks / predicates
def _top_split(body):
    out, depth, cur, q = [], 0, '', None
    for c in body:
        if q:
            cur += c
            if c == '\\':
                continue
            if c == q:
                q = None
            continue
        if c in '"\'':
            q = c
        elif c in '{[':
            depth += 1
        elif c in '}]':
            depth -= 1
        if c == ',' and depth == 0:
            out.append(cur)
            cur = ''
        else:
            cur += c
    if cur.strip():
        out.append(cur)
    return out


def parse_stack(tok):
    """`id[comp=v,...]` -> (id, {comp: value})."""
    m = re.match(r'^([^\[]+)(?:\[(.*)\])?$', tok, re.S)
    iid, body = m.group(1), m.group(2)
    comps = {}
    if body:
        for part in _top_split(body):
            k, _, v = part.partition('=')
            k = k.strip()
            if not k.startswith('minecraft:'):
                k = 'minecraft:' + k
            try:
                comps[k] = snbt_parse(v.strip()) if v else Byte(1)
            except Exception:
                comps[k] = v.strip()
    if not iid.startswith('minecraft:') and not iid.startswith('*') and not iid.startswith('#'):
        iid = 'minecraft:' + iid
    return iid, comps


def nbt_match(actual, pat):
    if isinstance(pat, dict):
        return isinstance(actual, dict) and all(k in actual and nbt_match(actual[k], v) for k, v in pat.items())
    if isinstance(pat, list):
        return isinstance(actual, list) and all(any(nbt_match(a, p) for a in actual) for p in pat)
    return actual == pat


def parse_pred(tok):
    m = re.match(r'^([^\[]+)(?:\[(.*)\])?$', tok, re.S)
    iid, body = m.group(1), m.group(2)
    tests = []
    if body:
        for part in _top_split(body):
            part = part.strip()
            neg = part.startswith('!')
            if neg:
                part = part[1:]
            mm = re.match(r'^([a-z_:]+)\s*([~=])?\s*(.*)$', part, re.S)
            k, op, v = mm.group(1), mm.group(2), mm.group(3)
            if not k.startswith('minecraft:'):
                k = 'minecraft:' + k
            try:
                val = snbt_parse(v) if v else None
            except Exception:
                val = v
            tests.append((neg, k, op, val))
    if iid not in ('*',) and not iid.startswith('minecraft:') and not iid.startswith('#'):
        iid = 'minecraft:' + iid
    return iid, tests


def pred_ok(item, pred):
    iid, tests = pred
    if item is None:
        return False
    if iid != '*' and not iid.startswith('#') and item['id'] != iid:
        return False
    for neg, k, op, val in tests:
        have = k in item['c']
        if op is None:
            ok = have
        elif op == '~':
            ok = have and nbt_match(item['c'][k], val)
        else:
            ok = have and item['c'][k] == val
        if ok == neg:
            return False
    return True


SLOTS = [f'hotbar.{i}' for i in range(9)] + [f'inventory.{i}' for i in range(27)] + ['weapon.offhand', 'player.cursor']


def slot_names(spec):
    if spec == 'weapon.mainhand' or spec == 'weapon':
        return ['hotbar.0']
    if spec in ('container.*',):
        return [f'hotbar.{i}' for i in range(9)] + [f'inventory.{i}' for i in range(27)]
    m = re.match(r'^container\.(\d+)$', spec)
    if m:
        n = int(m.group(1))
        return [f'hotbar.{n}'] if n < 9 else [f'inventory.{n - 9}']
    if spec.endswith('.*'):
        pre = spec[:-1]
        return [s for s in SLOTS if s.startswith(pre)]
    return [spec]


# ------------------------------------------------------------------ the sim
class PSim(mcsim.Sim):
    def __init__(self, root):
        super().__init__(root)
        self.stack = []
        self.incl = collections.Counter()      # fid -> commands (inclusive)
        self.selfc = collections.Counter()     # fid -> commands (own lines)
        self.ncall = collections.Counter()
        self.macro_n = collections.Counter()   # fid -> macro instantiations
        self.macro_args = collections.defaultdict(set)
        self.macro_bytes = collections.Counter()  # fid -> characters of substituted macro lines
        self.macro_lines = collections.Counter()  # fid -> macro lines substituted (= parsed again in the game on a cache miss)
        self.n = 0
        self.inv_changes = 0
        self.inv_change_where = collections.Counter()
        self.player = None
        self.t = 0
        self.stub = set()
        self.errors = collections.Counter()

    snbt = staticmethod(snbt_parse)

    # attribution
    def call(self, fid, ctx, macro=None):
        if fid in self.stub:
            return 1
        self.ncall[fid] += 1
        lines = self.load(fid)
        if macro is not None and any(l.lstrip().startswith('$') for l in lines):
            self.macro_n[fid] += 1
            try:
                self.macro_args[fid].add(snbt_dump(macro))
            except Exception:
                pass
        self.stack.append(fid)
        try:
            for raw in lines:
                s = raw.strip()
                if not s or s.startswith('#'):
                    continue
                if s.startswith('$'):
                    s = _sub(s[1:], macro)
                    self.macro_bytes[fid] += len(s)
                    self.macro_lines[fid] += 1
                try:
                    self.cmd(split(s), ctx)
                except mcsim.Return:
                    raise
                except (NotImplementedError, KeyError, IndexError, ValueError, TypeError, AttributeError, RuntimeError,
                        ZeroDivisionError) as e:
                    self.errors[(fid, type(e).__name__, str(e)[:80])] += 1
        except mcsim.Return as r:
            return r.v
        finally:
            self.stack.pop()
        return 1

    def load(self, fid):
        if fid not in self.cache:
            p = self.root / (fid.split(':', 1)[1] + '.mcfunction')
            raw = p.read_text(encoding='utf-8').split('\n') if p.exists() else []
            out, acc = [], ''
            for l in raw:
                if l.rstrip().endswith('\\') and not l.lstrip().startswith('#'):
                    acc += l.rstrip()[:-1].strip() + ' ' if acc else l.rstrip()[:-1] + ' '
                    continue
                if acc:
                    out.append(acc + l.strip())
                    acc = ''
                else:
                    out.append(l)
            self.cache[fid] = out
        return self.cache[fid]

    def cmd(self, t, ctx):
        self.n += 1
        for f in set(self.stack):
            self.incl[f] += 1
        if self.stack:
            self.selfc[self.stack[-1]] += 1
        c = t[0]
        if c == 'scoreboard' and len(t) > 3 and t[1] == 'players' and t[2] == 'reset' and t[3] == '*':
            if len(t) > 4:
                for key in [key for key in self.scores if key[1] == t[4]]:
                    del self.scores[key]
            return 1
        if c == 'item':
            return self.c_item(t, ctx)
        if c == 'clear':
            return self.c_clear(t, ctx)
        if c == 'give':
            return self.c_give(t, ctx)
        if c == 'data' and len(t) > 6 and t[1] == 'modify' and t[2] == 'storage' and t[5] in ('merge', 'prepend', 'insert'):
            st = self.storage.setdefault(t[3], {})
            try:
                if t[5] == 'merge':
                    src = self.snbt(t[7]) if t[6] == 'value' else self.path_get(self.storage[t[8]], t[9])
                    try:
                        dst = self.path_get(st, t[4])
                    except KeyError:
                        self.path_set(st, t[4], {})
                        dst = self.path_get(st, t[4])
                    dst.update(copy.deepcopy(src))
                elif t[5] == 'prepend':
                    src = self.snbt(t[7]) if t[6] == 'value' else self.path_get(self.storage[t[8]], t[9])
                    try:
                        lst = self.path_get(st, t[4])
                    except KeyError:
                        lst = []
                        self.path_set(st, t[4], lst)
                    lst.insert(0, copy.deepcopy(src))
                else:
                    idx = int(t[6])
                    src = self.snbt(t[8]) if t[7] == 'value' else self.path_get(self.storage[t[9]], t[10])
                    lst = self.path_get(st, t[4])
                    lst.insert(idx, copy.deepcopy(src))
            except (KeyError, IndexError):
                return 0
            return 1
        if c == 'data' and len(t) > 6 and t[1] == 'modify' and t[2] == 'storage' and t[5] == 'set':
            # (lane R) the game fails `data modify ... set` that changes nothing (ERROR_MERGE_UNCHANGED): store success 0
            try:
                old = copy.deepcopy(self.path_get(self.storage.get(t[3], {}), t[4]))
            except (KeyError, IndexError, TypeError, ValueError):
                old = KeyError
            r = super().cmd(t, ctx)
            try:
                new = self.path_get(self.storage.get(t[3], {}), t[4])
            except (KeyError, IndexError, TypeError, ValueError):
                new = KeyError
            return 0 if old is not KeyError and new is not KeyError and old == new else r
        if c == 'data' and len(t) > 2 and t[1] == 'get' and t[2] == 'storage':
            try:
                return self.data_get(t[2:], ctx)
            except (KeyError, IndexError, TypeError):
                return 0
        return super().cmd(t, ctx)

    def data_get(self, toks, ctx):
        if toks[0] == 'storage':
            st = self.storage.get(toks[1], {})
            if len(toks) < 3:
                return 1
            sl = mcsim.nbt_slots(st, mcsim.nbt_nodes(toks[2]))
            if not sl:
                raise KeyError(toks[2])
            cc, k = sl[0]
            v = cc[k] if cc is not None else st
            scale = float(toks[3]) if len(toks) > 3 else 1.0
            if isinstance(v, (list, dict, str)):
                return len(v)
            return int(v * scale) if scale != 1.0 else (int(v) if not isinstance(v, float) else int(v))
        return super().data_get(toks, ctx)

    # ---------------------------------------------------------- inventory
    def inv_of(self, e):
        if e is None or e.etype != 'player':
            return None
        return e.data.setdefault('inv', {})

    def changed(self, where):
        self.inv_changes += 1
        self.inv_change_where[where] += 1
        p = self.player
        # inventory_changed -> rlk:player/inv/dirty, queued right after this command (ItemCommands.broadcastChanges)
        self.call('rlk:player/inv/dirty', Ctx(p, tuple(p.pos), tuple(p.rot)))

    def set_slot(self, e, slot, item, where):
        inv = self.inv_of(e)
        if inv is None:
            return False
        old = inv.get(slot)
        if item is None or item.get('count', 1) <= 0 or item['id'] == 'minecraft:air':
            if slot in inv:
                del inv[slot]
        else:
            inv[slot] = item
        if old != inv.get(slot) and slot != 'player.cursor':
            self.changed(where)
        return True

    def c_item(self, t, ctx):
        # item replace entity <sel> <slot> with <stack> [count] | from entity <sel> <slot> [modifier]
        # item modify entity <sel> <slot> <modifier>
        if t[2] != 'entity':
            return 1
        ents = self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]
        where = self.stack[-1] if self.stack else '?'
        n = 0
        for e in ents:
            if e is None:
                continue
            for slot in slot_names(t[4]):
                if t[1] == 'replace':
                    if t[5] == 'with':
                        iid, comps = parse_stack(t[6])
                        cnt = int(t[7]) if len(t) > 7 else 1
                        item = {'id': iid, 'c': comps, 'count': cnt}
                    else:
                        src = self.select(t[7], ctx) if t[7] != '@s' else [ctx.ex]
                        if not src:
                            continue
                        si = self.inv_of(src[0]) if src[0].etype == 'player' else src[0].data.setdefault('inv', {})
                        item = copy.deepcopy(si.get(slot_names(t[8])[0])) if si else None
                    if e.etype == 'player':
                        self.set_slot(e, slot, item, where)
                    else:
                        e.data.setdefault('inv', {})[slot] = item
                    n += 1
                else:
                    inv = self.inv_of(e) if e.etype == 'player' else e.data.setdefault('inv', {})
                    if not inv or slot not in inv or inv[slot] is None:
                        continue
                    new = copy.deepcopy(inv[slot])
                    mod = ' '.join(t[5:])
                    try:
                        m = snbt_parse(mod)
                    except Exception:
                        m = None
                    for mm in (m if isinstance(m, list) else [m]):
                        if isinstance(mm, dict) and mm.get('type', '').endswith('set_components'):
                            for k, v in mm.get('components', {}).items():
                                k2 = k if k.startswith('minecraft:') or k.startswith('!') else 'minecraft:' + k
                                if k2.startswith('!'):
                                    new['c'].pop(k2[1:], None)
                                else:
                                    new['c'][k2] = v
                        elif isinstance(mm, dict) and mm.get('type', '').endswith('set_count'):
                            cnt = mm.get('count')
                            new['count'] = int(cnt) if isinstance(cnt, (int, float)) else new['count']
                        elif isinstance(mm, dict) and mm.get('type', '').endswith('set_name'):
                            new['c']['minecraft:custom_name'] = mm.get('name')
                        elif isinstance(mm, dict) and mm.get('type', '').endswith('set_lore'):
                            new['c']['minecraft:lore'] = mm.get('lore')
                        else:
                            new['c']['_mod'] = new['c'].get('_mod', 0) + 1
                    if e.etype == 'player':
                        self.set_slot(e, slot, new, where)
                    else:
                        inv[slot] = new
                    n += 1
        return n

    def c_clear(self, t, ctx):
        ents = self.select(t[1], ctx) if len(t) > 1 and t[1] != '@s' else [ctx.ex]
        pred = parse_pred(t[2]) if len(t) > 2 else ('*', [])
        mx = int(t[3]) if len(t) > 3 else None
        where = self.stack[-1] if self.stack else '?'
        tot = 0
        for e in ents:
            inv = self.inv_of(e)
            if not inv:
                continue
            for slot in list(inv):
                it = inv[slot]
                if pred_ok(it, pred):
                    if mx == 0:
                        tot += it['count']
                        continue
                    take = it['count'] if mx is None else min(it['count'], mx - tot)
                    tot += take
                    left = dict(it, count=it['count'] - take)
                    self.set_slot(e, slot, left if left['count'] > 0 else None, where)
                    if mx is not None and tot >= mx:
                        break
        return tot

    def c_give(self, t, ctx):
        ents = self.select(t[1], ctx) if t[1] != '@s' else [ctx.ex]
        iid, comps = parse_stack(t[2])
        cnt = int(t[3]) if len(t) > 3 else 1
        where = self.stack[-1] if self.stack else '?'
        for e in ents:
            inv = self.inv_of(e)
            if inv is None:
                continue
            for slot in [f'hotbar.{i}' for i in range(9)] + [f'inventory.{i}' for i in range(27)]:
                if slot not in inv:
                    self.set_slot(e, slot, {'id': iid, 'c': comps, 'count': cnt}, where)
                    break
        return cnt

    def items_test(self, t, i, ctx):
        """`items entity <sel> <slots> <pred>` at t[i] -> (count, consumed tokens)."""
        if t[i + 1] == 'entity':
            ents = self.select(t[i + 2], ctx) if t[i + 2] != '@s' else [ctx.ex]
            slots, pred = t[i + 3], parse_pred(t[i + 4])
            cnt = 0
            for e in ents:
                inv = self.inv_of(e) if e is not None and e.etype == 'player' else (e.data.get('inv', {}) if e else {})
                for s in slot_names(slots):
                    it = (inv or {}).get(s)
                    if pred_ok(it, pred):
                        cnt += it['count']
            return cnt, 5
        return 0, 6                                    # items block <pos> <slots> <pred>

    def execute(self, t, ctx):
        i, stores, last = 0, [], 1
        while i < len(t):
            k = t[i]
            if k == 'run':
                v = self.cmd(t[i + 1:], ctx)
                for s in stores:
                    self.store(s, v, ctx)
                return v
            if k in ('if', 'unless') and t[i + 1] == 'items':
                cnt, n = self.items_test(t, i + 1, ctx)
                if (cnt > 0) == (k == 'unless'):
                    if i + 1 + n >= len(t):
                        for s_ in stores:
                            self.store(s_, 0, ctx)
                    return 0
                last = cnt if k == 'if' else 1
                i += 1 + n
                continue
            if k in ('if', 'unless') and t[i + 1] in ('predicate', 'dimension', 'biome'):
                ok = False
                n = 2 if t[i + 1] in ('predicate', 'dimension') else 5
                if ok == (k == 'unless'):
                    return 0
                i += 1 + n
                continue
            if k in ('if', 'unless') and t[i + 1] == 'data' and t[i + 2] == 'entity':
                ok = True
                if 'active_effects' in t[i + 4]:
                    ok = True
                if ok == (k == 'unless'):
                    return 0
                i += 5
                continue
            if k == 'on':
                return 0
            if k == 'align':
                i += 2
                continue
            if k == 'store':
                n = 4 if t[i + 2] == 'score' else 6
                stores.append(t[i + 1:i + 1 + n + 1] if t[i + 2] != 'score' else t[i + 1:i + 5])
                i += 1 + n
                continue
            if k in ('if', 'unless'):
                self._last = 1
                sub = self._one_cond(t, i, ctx)
                if sub is None:
                    if self._cond_end(t, i) and stores:
                        for s_ in stores:
                            self.store(s_, 0, ctx)
                    return 0
                i += sub
                last = getattr(self, '_last', 1)
                continue
            if k == 'as':
                ents = self.select(t[i + 1], ctx)
                if not ents:
                    return 0
                rest = t[i + 2:]
                v = 0
                for e in ents:
                    v = self.execute(rest, ctx.copy(ex=e))
                for s in stores:
                    self.store(s, v, ctx)
                return v
            if k in ('at', 'positioned', 'rotated', 'facing', 'in', 'anchored', 'summon'):
                nctx, n = self._one_mod(t, i, ctx)
                if nctx is None:
                    return 0
                ctx = nctx
                i += n
                continue
            raise NotImplementedError(k)
        for s in stores:
            self.store(s, last, ctx)
        return last

    def _cond_end(self, t, i):
        kind = t[i + 1]
        n = {'score': 6 if len(t) > i + 4 and t[i + 4] == 'matches' else 7, 'entity': 3, 'data': 5, 'function': 3,
             'loaded': 5, 'block': 6}.get(kind, 99)
        return i + n >= len(t)

    def _one_cond(self, t, i, ctx):
        neg = t[i] == 'unless'
        kind = t[i + 1]
        if kind == 'score':
            a = self.sc(self.holder(t[i + 2], ctx), t[i + 3])
            if t[i + 4] == 'matches':
                ok, n = self.in_range(a, t[i + 5]), 6
            else:
                b = self.sc(self.holder(t[i + 5], ctx), t[i + 6])
                op = t[i + 4]
                ok = a is not None and b is not None and {'<': a < b, '<=': a <= b, '=': a == b, '>=': a >= b, '>': a > b}[op]
                n = 7
        elif kind == 'entity':
            ok, n = bool(self.select(t[i + 2], ctx)), 3
            self._last = len(self.select(t[i + 2], ctx)) if ok else 0
        elif kind == 'data':
            if t[i + 2] == 'storage':
                try:
                    ok = bool(mcsim.nbt_slots(self.storage.get(t[i + 3], {}), mcsim.nbt_nodes(t[i + 4])))
                except (KeyError, IndexError, TypeError, ValueError):
                    ok = False
            else:
                ok = True
            n = 5
        elif kind == 'function':
            ok, n = bool(self.call(t[i + 2], ctx)), 3
        elif kind == 'loaded':
            ok, n = True, 5
        elif kind == 'block':
            ok, n = self.block_test(self.coords(t[i + 2:i + 5], ctx), t[i + 5]), 6
        elif kind == 'blocks':
            ok, n = True, 12 if t[i + 11:i + 12] else 11
        else:
            raise NotImplementedError(kind)
        return n if ok != neg else None

    def _one_mod(self, t, i, ctx):
        k = t[i]
        if k == 'at':
            ents = self.select(t[i + 1], ctx)
            if not ents:
                return None, 0
            return ctx.copy(pos=tuple(ents[0].pos), rot=tuple(ents[0].rot)), 2
        if k == 'positioned':
            if t[i + 1] == 'as':
                ents = self.select(t[i + 2], ctx)
                if not ents:
                    return None, 0
                return ctx.copy(pos=tuple(ents[0].pos)), 3
            if t[i + 1] == 'over':
                return ctx, 3
            return ctx.copy(pos=self.coords(t[i + 1:i + 4], ctx)), 4
        if k == 'rotated':
            if t[i + 1] == 'as':
                ents = self.select(t[i + 2], ctx)
                if not ents:
                    return None, 0
                return ctx.copy(rot=tuple(ents[0].rot)), 3
            # round W: the yaw / pitch are applied (~ relative, else absolute) as mcsim does - before, `rotated ~180 0` kept the old
            # rotation, so a local ^ ^ ^1 after it pointed the wrong way (player/dodge/away)
            try:
                r = [ctx.rot[j] + float(v[1:] or 0) if v.startswith('~') else float(v) for j, v in enumerate(t[i + 1:i + 3])]
            except ValueError:
                return ctx, 3
            return ctx.copy(rot=tuple(r)), 3
        if k == 'facing':
            if t[i + 1] == 'entity':
                ents = self.select(t[i + 2], ctx)
                if not ents:
                    return None, 0
                # round W: the rotation toward the entity (feet / eyes), as mcsim does
                e = ents[0]
                tgt = list(e.pos)
                if t[i + 3] == 'eyes':
                    tgt[1] += e.data.get('eye', 0.0)
                dx, dy, dz = (tgt[j] - ctx.pos[j] for j in range(3))
                if abs(dx) + abs(dy) + abs(dz) < 1e-9:
                    return ctx, 4
                yaw = math.degrees(math.atan2(-dx, dz))
                pitch = math.degrees(-math.atan2(dy, math.hypot(dx, dz)))
                return ctx.copy(rot=(yaw, pitch)), 4
            return ctx, 4
        if k == 'in':
            return ctx, 2
        if k == 'anchored':
            return ctx.copy(anc=(t[i + 1] == 'eyes')), 2
        if k == 'summon':
            e = Ent(t[i + 1].replace('minecraft:', ''), ctx.pos, ctx.rot, [])
            self.ents.append(e)
            return ctx.copy(ex=e), 2
        raise NotImplementedError(k)

    def store(self, spec, v, ctx):
        try:
            return super().store(spec, v, ctx)
        except (KeyError, IndexError, TypeError, ValueError):
            return None


def pctx(s):
    p = s.player
    return Ctx(p, tuple(p.pos), tuple(p.rot))
