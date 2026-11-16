#!/usr/bin/env python3
"""srsim.py: stage SR's own helpers for test_hwamu.py / test_moon.py (scratch tool, never shipped).

Builds on the vendored, unchanged sims in HR/tests/lib (mcsim <- fgsim <- azsim; S3's folder, read only): an azsim world
(`combat/apply`, `player/take_damage`, element reactions, the kill path run for real from the datapack) with the item's
own functions running for real too. Additions, all here (nothing in HR/tests/lib is edited):

- a real SNBT reader / writer (`snbt_parse`, `snbt_dump`): mcsim's regex+json reader cannot read single-quoted strings
  and stringifies compound macro arguments as Python reprs; SrSim uses these for `data modify ... value`, `if data`
  tests and every `$(...)` substitution (strings raw, numbers plain, compounds / lists as SNBT, as the game does);
- `if|unless items ...` (answer: `s.items_present`, default False) and `if|unless predicate ...` (False);
- logs: `s.log` (tick, kind, detail) for titles, tellraw, playsound (sound id, volume, pitch), particles, and every call
  of `rlk:snd/*`, `rlk:combat/apply_reset` (target id + #dmg #dmgBase #sub #elem #elU #icd #crit), `rlk:char/dmg_calc`,
  `rlk:player/update_item_macro` (the argument compound) and `rlk:items/proc/hw_*`;
- `time query gametime` = s.t + GT0;
- command counters: `s.n_strict` (every command, an `execute ... run X` counts X too) and `s.n_lines` (each command line
  run once).
Run every suite from HR/tests (outside the datapack).
"""
import copy
import math
import random
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HR / 'tests' / 'lib'))
import azsim as A  # noqa: E402
import fgsim as G  # noqa: E402
import mcsim  # noqa: E402
from mcsim import Ent, Ctx, split  # noqa: E402

C0 = G.C0
GT0 = 100000          # game time at sim tick 0 (`time query gametime` = s.t + GT0)


# ------------------------------------------------------------------------------------------------- SNBT
class Byte(int):
    """A byte tag (1b / 0b / true / false) - keeps the type for snbt_dump."""


_NUM = re.compile(r'^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?([bBsSlLfFdD])?$')
_UNQ = re.compile(r'[A-Za-z0-9._+\-]')


class _P:
    def __init__(self, s):
        self.s, self.i = s, 0

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
                if n == 'x':
                    out.append(chr(int(self.s[self.i + 2:self.i + 4], 16)))
                    self.i += 4
                    continue
                out.append({'n': '\n', 't': '\t', 'r': '\r', 'b': '\b', 'f': '\f', 's': ' '}.get(n, n))
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
                k = self.string() if self.s[self.i] in '"\'' else self.word()
                self.eat(':')
                d[k] = self.value()
                if self.peek() == ',':
                    self.i += 1
                    if self.peek() == '}':          # trailing comma
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
                return Byte(int(body))
            if suf in ('f', 'd') or '.' in body or 'e' in body.lower():
                return float(body)
            return int(body)
        return w

    def word(self):
        self.ws()
        j = self.i
        while self.i < len(self.s) and _UNQ.match(self.s[self.i]):
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
    """The game's stringification of a tag (a top-level string is inserted raw by a macro)."""
    if isinstance(v, Byte) or isinstance(v, bool):
        return f'{int(v)}b'
    if isinstance(v, str):
        return v if top else _q(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f'{v}d'
    if isinstance(v, dict):
        return '{' + ','.join((k if re.fullmatch(r'[A-Za-z0-9._+\-]+', k) else _q(k)) + ':' + snbt_dump(x)
                              for k, x in v.items()) + '}'
    if isinstance(v, list):
        return '[' + ','.join(snbt_dump(x) for x in v) + ']'
    raise TypeError(type(v))


def render(c, args=None):
    """Plain text of a text component (text / extra / translate with fallback, %s and %% filled from with)."""
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return ''.join(render(x) for x in c)
    if isinstance(c, (int, float)):
        return str(c)
    out = ''
    if 'text' in c:
        out += c['text']
    elif 'translate' in c:
        fmt = c.get('fallback', c['translate'])
        w = list(c.get('with', []))
        k = iter(w)
        out += re.sub(r'%%|%s', lambda m: '%' if m.group(0) == '%%' else render(next(k)), fmt)
    for x in c.get('extra', []):
        out += render(x)
    return out


# ------------------------------------------------------------------------------------------------- the sim
STRIKES = ('rlk:items/proc/hw_ctr', 'rlk:items/proc/hw_slash')   # one-off damage (counter, 홍련일섬): costed apart


class SrSim(A.AzSim):
    def __init__(self, root):
        super().__init__(root)
        self.log = []
        self.n_strict = 0
        self.n_lines = 0
        self.items_present = False
        self.macro_calls = []          # (fid, args) of update_item_macro / other watched macro calls
        self.strike_cost = {}          # fid -> [commands of each call] for the one-off strikes (STRIKES)

    # SNBT: a real reader (mcsim calls self.snbt for `value` / `if data` patterns)
    def snbt(self, s):
        return snbt_parse(s)

    def cmd(self, t, ctx):
        self.n_strict += 1
        c = t[0]
        if c == 'execute':
            t = self._items_pred(t)
            if t is None:
                return 0
        if c == 'title':
            self.log.append((self.t, 'title', ' '.join(t[1:])))
        elif c == 'tellraw':
            self.log.append((self.t, 'tellraw', ' '.join(t[2:])))
        elif c == 'playsound':
            self.log.append((self.t, 'sound', (t[1], t[6] if len(t) > 6 else '', t[7] if len(t) > 7 else '')))
        elif c == 'particle':
            self.log.append((self.t, 'particle', (t[1], tuple(ctx.pos))))
        elif c == 'time' and len(t) > 2 and t[1] == 'query' and t[2] == 'gametime':
            return self.t + GT0                   # the world's game time: the sim tick + a fixed offset
        elif c == 'data' and len(t) > 6 and t[1] == 'modify' and t[2] == 'storage' and t[5] == 'merge':
            # `data modify storage <s> <path> merge value {...} | from storage <s2> <path2>` (mcsim has set / append only)
            st = self.storage.setdefault(t[3], {})
            try:
                src = self.snbt(t[7]) if t[6] == 'value' else self.path_get(self.storage[t[8]], t[9])
                dst = self.path_get(st, t[4])
            except (KeyError, IndexError):
                return 0
            dst.update(copy.deepcopy(src))
            return 1
        return super().cmd(t, ctx)

    def _items_pred(self, t):
        """`if|unless items <entity|block> <sel> <slot> <item>` and `if|unless predicate <id>` -> drop the clause when it
        passes, None (the execute fails) when it does not."""
        out, i = [], 0
        while i < len(t):
            if t[i] in ('if', 'unless') and i + 1 < len(t) and t[i + 1] in ('items', 'predicate'):
                neg = t[i] == 'unless'
                if t[i + 1] == 'items':
                    ok, n = self.items_present, 5
                else:
                    ok, n = False, 2
                if ok == neg:
                    return None
                i += 1 + n
                continue
            if t[i] == 'run':
                out += t[i:]
                break
            out.append(t[i])
            i += 1
        return out

    def call(self, fid, ctx, macro=None):
        if fid.startswith('rlk:snd/') or fid.startswith('rlk:items/proc/hw_') or fid in (
                'rlk:char/dmg_calc', 'rlk:player/hr_moon/apply', 'rlk:char/after_hit'):
            self.log.append((self.t, 'call', fid))
        if fid == 'rlk:combat/apply_reset' and ctx.ex is not None:
            g = lambda k, o='tmp': self.sc(k, o)  # noqa: E731
            self.log.append((self.t, 'apply', dict(target=ctx.ex.id, dmgBase=g('#dmgBase'), sub=g('#sub', 'itv'),
                                                    elem=g('#elem'), elU=g('#elU'), icd=g('#icd'), crit=g('#crit'),
                                                    skill=g('#skillDmg'), stun=g('#stunHit'))))
        if fid == 'rlk:player/update_item_macro':
            self.macro_calls.append((fid, copy.deepcopy(macro)))
        if fid in STRIKES:
            a = self.n_strict
            r = super().call(fid, ctx, macro)
            self.strike_cost[fid] = self.strike_cost.get(fid, []) + [self.n_strict - a]
            return r
        return super().call(fid, ctx, macro)


def _sub(s, macro):
    return re.sub(r'\$\((\w+)\)', lambda m: snbt_dump(macro[m.group(1)], top=True), s)


def _mc_call(self, fid, ctx, macro=None):
    """mcsim.Sim.call with the game's macro stringification and the line counter (used for SrSim through the class
    chain: AzSim.call -> super(G.FSim, self).call = mcsim.Sim.call)."""
    try:
        for raw in self.load(fid):
            s = raw.strip()
            if not s or s.startswith('#'):
                continue
            if s.startswith('$'):
                s = _sub(s[1:], macro)
            if isinstance(self, SrSim):
                self.n_lines += 1
            self.cmd(split(s), ctx)
    except mcsim.Return as r:
        return r.v
    return 1


mcsim.Sim.call = _mc_call     # module attribute only (the file is unchanged); every mcsim-based sim in this process


def run_line(s, line, ctx):
    """Run one command line as a function body line would (counted)."""
    s.n_lines += 1
    try:
        return s.cmd(split(line), ctx)
    except mcsim.Return as r:
        return r.v


# ------------------------------------------------------------------------------------------------- the world
def world(dp, seed=11, level=10, hp=None, atk=100, crit=0, critdmg=150, pos=(0.5, 64.0, 0.5)):
    """An azsim world on the datapack `dp` (the worktree's roguelike/, read only) with the item constants (tune/b10),
    rarity / star tables (items/register:6-12), the def of sword_hwamu and the engraving registry, and a first-person
    player (the player is the body) holding the item. Returns (s, player)."""
    s, zone, pl = A.setup(dp=dp, seed=seed, player_level=level, player_pos=pos, cls=SrSim)
    random.seed(seed)
    s.t = 0
    reg = (Path(dp) / 'data/rlk/function/items/register.mcfunction').read_text(encoding='utf-8').split('\n')
    s.cache['rlk:srtest/reg_tables'] = [l for l in reg[:13] if l.startswith('data modify storage rlk:items')]
    s.call('rlk:srtest/reg_tables', C0)
    s.storage.setdefault('rlk:items', {})['registry'] = {}
    s.storage['rlk:items']['ids'] = []
    s.call('rlk:items/mythic/sword_hwamu/def', C0)
    tune = (Path(dp) / 'data/rlk/function/items/tune/register.mcfunction').read_text(encoding='utf-8').split('\n')
    s.cache['rlk:srtest/tune_fac'] = [l for l in tune if l.startswith('data modify storage rlk:tune fac')]
    s.call('rlk:srtest/tune_fac', C0)
    s.storage['rlk:tune']['t'] = {}
    s.storage['rlk:tune']['ids'] = []
    s.call('rlk:items/tune/b10', C0)
    P = ('e', pl.id)
    hp = hp or 1000
    for o, v in (('it_sword_hwamu', 1), ('curHealth', hp), ('maxHealth', hp), ('atk', atk), ('critChance', crit),
                 ('critDamage', critdmg), ('level', level), ('hrMoon', 0), ('vBig', 0), ('dashInvT', 0)):
        s.setsc(P, o, v)
    for k, v in (('#10', 10), ('#100', 100), ('#1000', 1000), ('#500', 500), ('#2', 2), ('#31', 31)):
        if s.sc(k, 'tmp') is None:
            s.setsc(k, 'tmp', v)
    s.setsc('#sub', 'itv', 0)
    s.setsc('keen', 'engN', 0)
    return s, pl


def set_star(s, star):
    """The item at star 0-3 through the REAL engine: <id> enhL + items/tune/apply {id:"sword_hwamu"} (capture first)."""
    if not s.storage['rlk:tune']['t']['sword_hwamu'] or 'b' not in s.storage['rlk:tune']['t']['sword_hwamu'][0]:
        s.call('rlk:items/tune/capture', C0, {'id': 'sword_hwamu'})
    s.setsc('sword_hwamu', 'enhL', star)
    s.storage.setdefault('rlk:pinv', {}).setdefault('enh', {})['sword_hwamu'] = star
    s.call('rlk:items/tune/apply', C0, {'id': 'sword_hwamu'})


def mob(s, pos, hp=100000, lv=1, tags=('rlk_mob',), etype='husk'):
    e = Ent(etype, pos, (0.0, 0.0), tags=list(tags))
    s.ents.append(e)
    for o, v in (('mhpM', hp), ('mhpC', hp), ('mlv', lv), ('mres', 0), ('elAct', 0)):
        s.setsc(('e', e.id), o, v)
    return e


def pctx(s, pl):
    return Ctx(pl, tuple(pl.pos), tuple(pl.rot))


def hook_lines(dp, rel, needle):
    """The lines of a hand file that contain `needle` (non-comment)."""
    p = Path(dp) / 'data/rlk/function' / (rel + '.mcfunction')
    return [l for l in p.read_text(encoding='utf-8').split('\n') if needle in l and not l.lstrip().startswith('#')]


def sc(s, who, obj='itv'):
    return s.sc(who, obj)


FAILS = []


def ck(name, ok, info=''):
    if not ok:
        FAILS.append(name)
        print('FAIL', name, info)
    return ok


def summary(title, n):
    print(f'{title}: {n - len(FAILS)}/{n} passed' + ('' if not FAILS else f' — FAILED: {", ".join(FAILS)}'))
    return 1 if FAILS else 0
