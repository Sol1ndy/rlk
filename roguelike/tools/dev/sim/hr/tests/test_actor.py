#!/usr/bin/env python3
"""test_actor.py <dp> [--rp RP] [--ref-rp RP] [--rebuild] [section ...] — the suite of the cutscene actor (lane H3; hr_design.md
§4.2, §4.3, §5.3, §6.3). Run from a copy of tools/dev/sim outside the datapack (sim README 1). <dp> = the roguelike/ to test.

  static   char/cine/**: every referenced function exists, no negative literal in scoreboard add / remove, lowercase ids, macro
           lines carry a macro, only the objective `cine` and the storage rlk:cine, every part key addresses a part UUID
  spawn    for each of the 7 characters (#charN 1, 3-8): spawn makes the root and 11 displays with that character's part models
           and the one cine_sword, fixed UUIDs, the tags, at the stage position and yaw; called again it makes no second set;
           a character change rebuilds; with --rp: every item definition, model and skin exists, the 4 new characters' models
           are the rig characters' boxes on their own skin, cine_sword is the sword model, the atlas has the skins
  hide     spawn and every tick hide the avatar (invisibility, empty hands), a rig character's displays and a floating catalyst
           (view range 0); stop restores all of it, leaves no entity, no tag, no storage, no objective; stop twice; stop without
           an actor; the actor killed from outside (mboss cleanup, a room wipe, /reload) -> the next tick restores the avatar
  clips    the manifest: the 5 lengths of the contract, per-tick columns, shift inside the limits at every tick and (0, 0, 0)
           at the hand-back ticks (cs0 1440, cs1 720, repel 140, ending 330-1372, coda), no sole under the floor, the contacts
           of §4.3 within tolerance, two-hand ticks, repel 129 == ending 0, ending 1372 == coda 0, the last pose of cs0 / cs1 /
           repel / coda == the idle; from the debug poses: no part turns more than 120 degrees in a tick
  replay   (mcsim + a model of the client's display interpolation) every clip played tick by tick from play + #cavT: what
           the client shows at each tick == the built pose of that tick (0.02 b, 2.5 degrees), no key re-sends an unchanged
           transform (26.3 would replay the last interpolation), #cavT past the end holds the last frame without commands,
           a frozen #cavT sends nothing
  jumps    the skips: cs0 -> 1290 and cs1 -> 566 from an earlier tick show that frame at once and track on; a jump to any
           tick lands within 40 ticks; backward jumps; repel 129 -> play ending at 0 changes nothing on screen; a clip change
  face     face {yaw} turns the root and the parts to the yaw in 12 ticks, the short way round
  --rebuild  the generator run twice in a scratch copy (tools + a copy of --rp): both runs byte-identical, and identical to the
           tree's char/cine/**, char/motion/**, tools/player_motion/** (generated outputs are never edited by hand); with
           --ref-rp: every file of the reference pack is unchanged but the item atlas, which only gains the 4 skins
"""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'cb' / 'tests' / 'lib'))
import mcsim  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('dp')
ap.add_argument('--rp')
ap.add_argument('--ref-rp')
ap.add_argument('--rebuild', action='store_true')
ap.add_argument('sections', nargs='*')
A = ap.parse_args()
DP = Path(A.dp).resolve()
FN = DP / 'data/rlk/function'
CINE = FN / 'char/cine'
MAN = json.loads((DP / 'tools/player_motion/cine/manifest.json').read_text(encoding='utf8'))
PARTS = MAN['parts']
UUIDS = [MAN['uuid'].replace('{:02x}', f'{i:02x}') for i in range(len(PARTS))]
CONTRACT = {'cs0': 1440, 'cs1': 720, 'repel': 140, 'ending': 1372, 'coda': 120}
LIMIT = {'fwd': 2.5, 'back': 1.5, 'side': 1.5, 'cs0_back': 6.0, 'air': 7.0}
CHARS = {1: ('lumine', 'lumine'), 3: ('skirk', 'skirk'), 4: ('clorinde', 'clorinde'), 5: ('arle', 'arlecchino'), 6: ('navia', 'navia'), 7: ('ronova', 'ronova'), 8: ('nefer', 'nefer')}
RIG = {3, 5, 6}
ok = bad = 0
FAILS = []


def check(name, cond, detail=''):
    global ok, bad
    if cond:
        ok += 1
    else:
        bad += 1
        FAILS.append(name)
        print(f'FAIL {name}' + (f' :: {detail}' if detail else ''))


def want(sec):
    return not A.sections or sec in A.sections


# ---------------------------------------------------------------------------------------------------------------- quaternions
def qmul(a, b):
    x, y, z, w = a
    X, Y, Z, W = b
    return [w * X + x * W + y * Z - z * Y, w * Y - x * Z + y * W + z * X, w * Z + x * Y - y * X + z * W, w * W - x * X - y * Y - z * Z]


def qang(a, b):
    d = abs(sum(x * y for x, y in zip(a, b))) / (math.hypot(*a) * math.hypot(*b))
    return 2 * math.degrees(math.acos(min(1.0, d)))


def slerp(a, b, u):
    d = sum(x * y for x, y in zip(a, b))
    if d < 0:
        b, d = [-x for x in b], -d
    if d > .9995:
        r = [x + (y - x) * u for x, y in zip(a, b)]
    else:
        th = math.acos(d)
        s = math.sin(th)
        r = [(x * math.sin((1 - u) * th) + y * math.sin(u * th)) / s for x, y in zip(a, b)]
    n = math.hypot(*r)
    return [x / n for x in r]


TF = re.compile(r'transformation:\{translation:\[([^\]]*)\],left_rotation:\[([^\]]*)\],scale:\[([^\]]*)\]')


def parse_tf(s):
    m = TF.search(s)
    if not m:
        return None
    f = lambda g: [float(x.rstrip('f')) for x in g.split(',')]
    return {'t': f(m.group(1)), 'q': f(m.group(2)), 's': f(m.group(3))}


def tf_dist(a, b):
    return math.dist(a['t'], b['t']), qang(a['q'], b['q'])


# ---------------------------------------------------------------------------------------------------------------- the world
class World(mcsim.Sim):
    """mcsim + what char/cine/** uses: fixed UUIDs, display NBT (transformation, view_range, the item model), effects, hand
    items, the scoreboard objective list, and a model of the client's display interpolation per part."""

    def __init__(self):
        super().__init__(FN)
        self.now = 0
        self.objectives = set()
        self.resend = []
        self.merges = 0
        self.log = []

    def load(self, fid):
        if not fid.startswith('rlk:char/cine') and not fid.startswith('rlk:view/av_unwrap'):
            self.log.append(('call', fid))
            return []
        if fid.startswith('rlk:view/'):
            self.log.append(('call', fid))
            return []
        return super().load(fid)

    def select(self, sel, ctx):
        if re.fullmatch(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', sel):
            return [e for e in self.ents if e.alive and e.data.get('_uuid') == sel]
        return super().select(sel, ctx)

    def shown(self, e, now=None):
        d = e.data['disp']
        now = self.now if now is None else now
        if d['dur'] <= 0:
            return d['b']
        u = max(0.0, min(1.0, (now - d['t0']) / d['dur']))
        a, b = d['a'], d['b']
        return {'t': [x + (y - x) * u for x, y in zip(a['t'], b['t'])], 'q': slerp(a['q'], b['q'], u), 's': [x + (y - x) * u for x, y in zip(a['s'], b['s'])]}

    def cmd(self, t, ctx):
        c = t[0]
        if c == 'scoreboard' and t[1] == 'objectives':
            if t[2] == 'add':
                self.objectives.add(t[3])
            elif t[2] == 'remove':
                self.objectives.discard(t[3])
                for k in [k for k in self.scores if k[1] == t[3]]:
                    del self.scores[k]
            return 1
        if c == 'scoreboard' and t[1] == 'players' and 'cine' in (t[4:5] + t[7:8]) and 'cine' not in self.objectives:
            return 0                                    # the game: unknown objective, the command fails
        if c == 'summon':
            nbt = t[5] if len(t) > 5 else '{}'
            m = re.search(r'UUID:\[I;(-?\d+),(-?\d+),(-?\d+),(-?\d+)\]', nbt)
            uuid = None
            if m:
                h = ''.join(f'{int(x) & 0xffffffff:08x}' for x in m.groups())
                uuid = f'{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}'
                if self.select(uuid, ctx):
                    raise RuntimeError('summon with an existing UUID ' + uuid)
            r = super().cmd(t, ctx)
            e = self.ents[-1]
            e.data['_uuid'] = uuid
            e.data['nbt'] = nbt
            m = re.search(r'"minecraft:item_model":"([^"]+)"', nbt)
            e.data['model'] = m.group(1) if m else None
            m = re.search(r'view_range:([\d.]+)f', nbt)
            e.data['view_range'] = float(m.group(1)) if m else 1.0
            tf = parse_tf(nbt)
            if tf:
                e.data['tf'] = tf
                e.data['disp'] = {'a': tf, 'b': tf, 't0': self.now, 'dur': 0}
            return r
        if c == 'data' and t[1] == 'merge' and t[2] == 'entity':
            for e in (self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]):
                self.merges += 1
                m = re.search(r'view_range:([\d.]+)f', t[4])
                if m:
                    e.data['view_range'] = float(m.group(1))
                tf = parse_tf(t[4])
                if tf:
                    dur = int(re.search(r'interpolation_duration:(\d+)', t[4]).group(1))
                    if tf == e.data.get('tf') and dur > 0:    # with a duration the client would replay its last interpolation
                        self.resend.append((self.now, e.data.get('_uuid')))
                    cur = self.shown(e)
                    e.data['tf'] = tf
                    e.data['disp'] = {'a': cur, 'b': tf, 't0': self.now, 'dur': dur}
            return 1
        if c == 'data' and t[1] == 'remove' and t[2] == 'storage':
            self.storage.get(t[3], {}).pop(t[4], None)
            return 1
        if c == 'effect':
            for e in self.select(t[2], ctx):
                if t[1] == 'give':
                    e.data['invis'] = self.now + (10 ** 9 if t[4] == 'infinite' else int(t[4]) * 20)
                else:
                    e.data.pop('invis', None)
            return 1
        if c == 'item' and t[1] == 'replace':
            for e in self.select(t[3], ctx):
                e.data.setdefault('hand', {})[t[4]] = 'air' if t[5] == 'with' and 'air' in t[6] else 'item'
            return 1
        return super().cmd(t, ctx)


def world(charn=3, rig_displays=False, catalyst=None):
    w = World()
    w.setsc('#charN', 'tmp', charn)
    pl = mcsim.Ent('player', (100.5, 64.0, 200.5), (30.0, 10.0), ['player'])
    av = mcsim.Ent('mannequin', (100.5, 64.0, 200.5), (30.0, 0.0), ['rlk_view', 'rlk_av', 'rlk_body'])
    av.data['hand'] = {'weapon.mainhand': 'item'}
    w.ents += [pl, av]
    w.player, w.av = pl, av
    if rig_displays:
        for i in range(11):
            e = mcsim.Ent('item_display', av.pos, (30.0, 0.0), ['rlk_view', 'rlk_pm', f'rlk_pm_{i}'])
            e.data['view_range'] = 1.5
            w.ents.append(e)
        w.setsc(('e', pl.id), 'pmVisible', 1)
        av.data['invis'] = 10 ** 9
        av.data['hand'] = {'weapon.mainhand': 'air'}
    if catalyst:
        for i in range(5):
            e = mcsim.Ent('block_display', av.pos, (0.0, 0.0), [catalyst])
            e.data['view_range'] = 1.0
            w.ents.append(e)
    return w


STAGE = ((104.25, 64.0, 203.75), (55.0, 0.0))


def run(w, fid, macro=None, at=None):
    pos, rot = at or (w.player.pos, w.player.rot)
    return w.call(fid, mcsim.Ctx(w.player, pos, rot), macro)


def spawn(w):
    run(w, 'rlk:char/cine/spawn', at=STAGE)


def tick(w, t):
    """one server tick of a sequence: the module writes its clock, then calls char/cine/tick"""
    w.now += 1
    if 'cine' in w.objectives:
        w.setsc('#cavT', 'cine', t)
    run(w, 'rlk:char/cine/tick')


def parts(w):
    return [e for e in w.ents if e.alive and 'rlk_cine_part' in e.tags]


def roots(w):
    return [e for e in w.ents if e.alive and 'rlk_cine_root' in e.tags]


# reference poses: the builder's debug datapack (--rebuild writes one) or, without it, the manifest columns only
DBG = None


def ref_pose(clip, t):
    f = DBG / 'data/rlk/function/cine_dbg' / clip / f'{t}.mcfunction'
    out = {}
    for line in f.read_text().splitlines():
        m = re.match(r'data merge entity (\S+) ', line)
        out[m.group(1)] = parse_tf(line)
    return out


# ================================================================================================================ static
if want('static'):
    files = sorted(CINE.rglob('*.mcfunction'))
    check('static: char/cine has the 5 calls', all((CINE / f'{n}.mcfunction').exists() for n in ('spawn', 'play', 'tick', 'face', 'stop')))
    ids = {'rlk:char/cine/' + str(f.relative_to(CINE))[:-11] for f in files}
    refs, neg, upper, macro, objs, stor, uu = set(), [], [], [], set(), set(), set()
    for f in files:
        for ln in f.read_text(encoding='utf8').splitlines():
            if not ln or ln.startswith('#'):
                continue
            for m in re.finditer(r'function (rlk:[a-z0-9_/.$()]+)', ln):
                refs.add(m.group(1))
            if re.search(r'scoreboard players (add|remove) \S+ \S+ -', ln):
                neg.append(f.name)
            if re.search(r'rlk:[^ "{\[]*[A-Z]', ln):
                upper.append(ln[:60])
            if ln.startswith('$') != ('$(' in ln):
                macro.append(ln[:60])
            for m in re.finditer(r'scoreboard players \S+ \S+ (\S+)', ln):
                objs.add(m.group(1))
            for m in re.finditer(r'(?:if|unless) score \S+ (\S+)', ln):
                objs.add(m.group(1))
            for m in re.finditer(r'storage (rlk:\w+)', ln):
                stor.add(m.group(1))
            for m in re.finditer(r'data merge entity ([0-9a-f-]{36})', ln):
                uu.add(m.group(1))
    missing = [r for r in refs if '$(' not in r and r not in ids and not (FN / (r[4:] + '.mcfunction')).exists()]
    check('static: every referenced function exists', not missing, str(missing[:5]))
    check('static: play reaches c/<clip>/sel for the 5 clips', all((CINE / 'c' / c / 'sel.mcfunction').exists() for c in CONTRACT))
    check('static: no negative literal in scoreboard add / remove', not neg, str(neg[:3]))
    check('static: lowercase resource ids', not upper, str(upper[:3]))
    check('static: macro lines carry a macro and only they start with $', not macro, str(macro[:3]))
    check('static: objectives cine (+ tmp for #charN, pmVisible / pmActive of the rig)', objs <= {'cine', 'tmp', 'pmVisible', 'pmActive'}, str(objs))
    check('static: storage rlk:cine only', stor == {'rlk:cine'}, str(stor))
    check('static: part keys address the 11 part UUIDs', uu == set(UUIDS), str(uu ^ set(UUIDS)))
    check('static: manifest calls / tags / objective', MAN['objective'] == 'cine' and MAN['tags']['root'] == 'rlk_cine_root' and MAN['tags']['part'] == 'rlk_cine_part'
          and MAN['calls']['spawn'] == 'rlk:char/cine/spawn' and MAN['fake_players']['tick'] == '#cavT')

# ================================================================================================================ spawn
if want('spawn'):
    for n, (key, skin) in CHARS.items():
        w = world(n)
        spawn(w)
        ps, rs = parts(w), roots(w)
        check(f'spawn {key}: 11 parts + the root', len(ps) == 11 and len(rs) == 1 and rs[0].etype == 'marker', f'{len(ps)} {len(rs)}')
        models = {e.data['_uuid']: e.data['model'] for e in ps}
        exp = {UUIDS[i]: ('rlk:player_motion/weapons/cine_sword' if p == 'weapon' else f'rlk:player_motion/{key}/{p}') for i, p in enumerate(PARTS)}
        check(f'spawn {key}: its part models and the one cine_sword', models == exp, str({k: v for k, v in models.items() if exp.get(k) != v}))
        check(f'spawn {key}: tags, type, at the stage position and yaw', all(e.etype == 'item_display' and {'rlk_room', 'rlk_mb_aux', 'rlk_cine_part'} <= e.tags and
              math.dist(e.pos, STAGE[0]) < 1e-9 and abs(e.rot[0] - STAGE[1][0]) < 1e-9 and e.rot[1] == 0 for e in ps) and math.dist(rs[0].pos, STAGE[0]) < 1e-9 and {'rlk_room', 'rlk_mb_aux'} <= rs[0].tags)
        check(f'spawn {key}: displays as the rig (fixed billboard, no shadow, teleport 1, view range 2, brightness 13 / 15)', all('billboard:"fixed"' in e.data['nbt'] and 'shadow_radius:0f' in e.data['nbt'] and
              'teleport_duration:1' in e.data['nbt'] and 'view_range:2f' in e.data['nbt'] and 'brightness:{block:13,sky:15}' in e.data['nbt'] for e in ps))
        spawn(w)
        check(f'spawn {key}: called again makes no second set', len(parts(w)) == 11 and len(roots(w)) == 1 and {e.id for e in parts(w)} == {e.id for e in ps})
        w.setsc('#charN', 'tmp', 3 if n != 3 else 4)
        spawn(w)
        other = 'skirk' if n != 3 else 'clorinde'
        check(f'spawn {key}: a character change rebuilds the parts', len(parts(w)) == 11 and all(e.data['model'].startswith(f'rlk:player_motion/{other}/') for e in parts(w) if 'cine_sword' not in e.data['model']))
    w = world(2)
    spawn(w)
    check('spawn: an unknown #charN falls back to a whole actor', len(parts(w)) == 11 and all(e.data['model'] for e in parts(w)))
    if A.rp:
        RP = Path(A.rp) / 'assets/rlk'
        atlas = json.loads((Path(A.rp) / 'assets/minecraft/atlases/items.json').read_text())['sources']
        res = [s.get('resource') for s in atlas if not s.get('sprite')]
        ref = {p: json.loads((RP / f'models/item/player_motion/skirk/{p}.json').read_text()) for p in PARTS if p != 'weapon'}
        for n, (key, skin) in CHARS.items():
            good = (RP / f'textures/skin/{skin}.png').exists() and res.count(f'rlk:skin/{skin}') == 1
            for p in PARTS:
                if p == 'weapon':
                    continue
                it = RP / f'items/player_motion/{key}/{p}.json'
                mo = RP / f'models/item/player_motion/{key}/{p}.json'
                if not (it.exists() and mo.exists()):
                    good = False
                    continue
                m = json.loads(mo.read_text())
                good &= json.loads(it.read_text())['model']['model'] == f'rlk:item/player_motion/{key}/{p}'
                good &= m['textures'] == {'skin': f'rlk:skin/{skin}', 'particle': f'rlk:skin/{skin}'} and m['elements'] == ref[p]['elements']
            check(f'rp {key}: part items, models (the avatar boxes on rlk:skin/{skin}), the skin and its atlas entry', good)
        cs = json.loads((RP / 'items/player_motion/weapons/cine_sword.json').read_text())
        check('rp: cine_sword is the player rig\'s sword model (0 new atlas px)', cs == {'model': {'type': 'minecraft:model', 'model': 'rlk:item/player_motion/weapons/sword'}} and (RP / 'models/item/player_motion/weapons/sword.json').exists())
        src = DP / 'tools/player_motion/cine/skin/lumine.png'
        check('rp: Lumine\'s skin is the file in git, 64 x 64', src.read_bytes() == (RP / 'textures/skin/lumine.png').read_bytes() and src.read_bytes()[16:24] == bytes([0, 0, 0, 64, 0, 0, 0, 64]))
        prof = (FN / 'char/lumine/def.mcfunction').read_text(encoding='utf8')
        import base64
        m = re.search(r'head:"([A-Za-z0-9+/=]+)"', prof)
        url = json.loads(base64.b64decode(m.group(1)))['textures']['SKIN']['url']
        print(f'  Lumine profile texture: {url}  (git copy sha1 {hashlib.sha1(src.read_bytes()).hexdigest()})')
        print(f'  atlas: {len(res)} unaliased sources; the actor adds rlk:skin/{{lumine,clorinde,ronova,nefer}} = 4 x 4096 px')

# ================================================================================================================ hide
if want('hide'):
    for label, kw in (('lumine', dict(charn=1)), ('skirk (rig)', dict(charn=3, rig_displays=True)), ('ronova (catalyst)', dict(charn=7, catalyst='rlk_rncat')), ('nefer (catalyst)', dict(charn=8, catalyst='rlk_nfcat'))):
        w = world(**kw)
        pm = [e for e in w.ents if 'rlk_pm' in e.tags or e.etype == 'block_display']
        spawn(w)
        check(f'hide {label}: spawn hides the avatar (invisible, empty hands)', w.av.data.get('invis', 0) > w.now and w.av.data['hand'].get('weapon.mainhand') == 'air')
        check(f'hide {label}: the character\'s own displays out of view range', all(e.data['view_range'] == 0 for e in pm))
        run(w, 'rlk:char/cine/play', {'clip': 'cs1'})
        for t in range(30):
            if t == 10:                                  # the avatar's hand comes back (view/slow), new rig displays appear
                w.av.data['hand']['weapon.mainhand'] = 'item'
                if kw.get('rig_displays'):
                    e = mcsim.Ent('item_display', w.av.pos, (0.0, 0.0), ['rlk_pm'])
                    e.data['view_range'] = 1.5
                    w.ents.append(e)
                    pm.append(e)
            tick(w, t)
        check(f'hide {label}: held through the ticks (a returned hand item, a new rig display)', w.av.data.get('invis', 0) > w.now and w.av.data['hand']['weapon.mainhand'] == 'air' and all(e.data['view_range'] == 0 for e in pm))
        w.log.clear()
        run(w, 'rlk:char/cine/stop')
        left = [e for e in w.ents if e.alive and any(x.startswith('rlk_cine') for x in e.tags)]
        check(f'stop {label}: no entity, no tag, no storage, no objective left', not left and 'cine' not in w.objectives and not any(k[1] == 'cine' for k in w.scores) and not w.storage.get('rlk:cine'))
        if kw.get('rig_displays'):
            check(f'stop {label}: the rig displays back at view range 1.5, the avatar still hidden under its rig', all(e.data['view_range'] == 1.5 for e in pm) and w.av.data.get('invis', 0) > w.now)
        else:
            check(f'stop {label}: the avatar visible, its hand refilled, the catalyst back', 'invis' not in w.av.data and w.av.data['hand']['weapon.mainhand'] == ('air' if kw['charn'] in (7, 8) else 'item')
                  and ('call', 'rlk:view/av_unwrap') in w.log and all(e.data['view_range'] == 1.0 for e in pm))
        snap = (len(w.ents), dict(w.av.data.get('hand', {})), 'invis' in w.av.data)
        run(w, 'rlk:char/cine/stop')
        check(f'stop {label}: called twice changes nothing', snap == (len(w.ents), dict(w.av.data.get('hand', {})), 'invis' in w.av.data))
    w = world(1)
    n0 = len(w.ents)
    run(w, 'rlk:char/cine/stop')
    tick(w, 5)
    run(w, 'rlk:char/cine/face', {'yaw': 90})
    run(w, 'rlk:char/cine/stop')
    check('stop / tick / face without an actor: nothing happens, nothing left', len(w.ents) == n0 and 'invis' not in w.av.data and 'cine' not in w.objectives)
    for how, tag in (('mboss cleanup', 'rlk_mb_aux'), ('room wipe', 'rlk_room')):
        w = world(1)
        spawn(w)
        run(w, 'rlk:char/cine/play', {'clip': 'repel'})
        for t in range(12):
            tick(w, t)
        w.cmd(mcsim.split(f'kill @e[tag={tag}]'), mcsim.Ctx(None, (0, 0, 0), (0, 0)))
        check(f'exit ({how}): the actor is gone with the sweep', not parts(w) and not roots(w))
        tick(w, 12)
        check(f'exit ({how}): the next tick restores the avatar', 'invis' not in w.av.data and w.av.data['hand']['weapon.mainhand'] == 'item' and 'cine' not in w.objectives)
    w = world(1)
    spawn(w)
    w.now += 25                                          # the ticks stop without a stop (no module tick): 1 s later
    check('exit (no tick, no stop): the invisibility runs out by itself', w.av.data.get('invis', 0) <= w.now)
    w = world(1)
    run(w, 'rlk:char/cine/play', {'clip': 'ending'})
    spawn(w)
    check('play before spawn keeps the clip', w.sc('#cavC', 'cine') == MAN['clips']['ending']['id'])

# ================================================================================================================ clips
if want('clips'):
    check('clips: the 5 clips and lengths of the contract', {k: c['len'] for k, c in MAN['clips'].items()} == CONTRACT, str({k: c['len'] for k, c in MAN['clips'].items()}))
    check('clips: ids 1-5 in the order cs0 cs1 repel ending coda', [MAN['clips'][k]['id'] for k in CONTRACT] == [1, 2, 3, 4, 5])
    check('clips: the limits are the contract\'s', MAN['limit'] == LIMIT)
    for k, c in MAN['clips'].items():
        L, T = c['len'], c['tick']
        check(f'{k}: per-tick columns shift / hilt / tip / hand_r / hand_l, len + 1 rows', all(len(T[col]) == L + 1 for col in ('shift', 'hilt', 'tip', 'hand_r', 'hand_l', 'foot_r', 'foot_l')))
        out = [t for t, (r, u, f) in enumerate(T['shift']) if f > LIMIT['fwd'] + 1e-6 or f < -(LIMIT['cs0_back'] if k == 'cs0' else LIMIT['back']) - 1e-6 or abs(r) > LIMIT['side'] + 1e-6
               or u < -1e-6 or u > (LIMIT['air'] if k == 'ending' else 0) + 1e-6]
        check(f'{k}: shift inside the limits at every tick', not out, str(out[:5]))
        hb = {'cs0': [1440], 'cs1': [720], 'repel': [140], 'ending': list(range(330, 1373)), 'coda': [0, 120]}[k]
        check(f'{k}: shift (0, 0, 0) at the hand-back ticks', all(T['shift'][t] == [0, 0, 0] for t in hb))
        low = min(min(T['foot_r'][t][1], T['foot_l'][t][1]) for t in range(L + 1))
        check(f'{k}: no sole under the floor', low >= -.006, f'{low}')
        tipl = min(T['tip'][t][1] for t in range(L + 1))
        check(f'{k}: the blade\'s point never under the floor', tipl >= -.006, f'{tipl}')
        blade = max(abs(math.dist(T['hilt'][t], T['tip'][t]) - MAN['sword']['hilt_to_tip']) for t in range(L + 1))
        check(f'{k}: hilt -> tip is the sword\'s length at every tick, the grip in the right hand', blade < .003 and max(math.dist(T['hilt'][t], T['hand_r'][t]) for t in range(L + 1)) < .003, f'{blade}')
        for a, b in c['two_hands']:
            worst = 0
            for t in range(a, b + 1):
                u = MAN['sword']['left_hand'] / MAN['sword']['hilt_to_tip']
                p = [h + (q - h) * u for h, q in zip(T['hilt'][t], T['tip'][t])]
                worst = max(worst, math.dist(p, T['hand_l'][t]))
            check(f'{k}: two hands {a}-{b}: the left hand on the hilt under the right', worst <= .06, f'{worst:.3f}')
        for name, r in c['contact'].items():
            check(f'{k}: contact {name} within {r["tol"]}', r['worst'] <= r['tol'], f'{r["worst"]} at {r["at"]}')
    cont = {n: c for n, c in MAN['contact'].items()}
    check('clips: the 13 actor-side contacts of §4.3', set(cont) == {'K1', 'KR', 'KW', 'KH', 'KS', 'KK', 'KG', 'KE2', 'KE5', 'KA1', 'KA2', 'KA3', 'KA4'}
          and cont['K1']['p'] == [0, 1.45, .95] and cont['KR']['p'] == [0, 1.55, .65] and cont['KA4']['p'] == [0, 1.5, 3.45] and cont['KK']['p'] == [0, .35, 2.7])   # (round W: the locks apart, the exchange on the ground)
    # blade rows re-measured from the manifest columns (root of the blade .. tip)
    def seg(P, a, b):
        ab = [y - x for x, y in zip(a, b)]
        u = max(0, min(1, sum(d * (p - x) for d, p, x in zip(ab, P, a)) / sum(d * d for d in ab)))
        return math.dist(P, [x + d * u for x, d in zip(a, ab)])
    for name, c in cont.items():
        if c['what'] != 'blade':
            continue
        T = MAN['clips'][c['clip']]['tick']
        worst = max(seg(c['p'], T['hilt'][t], T['tip'][t]) for t in range(c['ticks'][0], c['ticks'][-1] + 1))
        check(f'{c["clip"]}: {name} on the blade\'s centre line (manifest columns)', worst <= c['tol'], f'{worst:.3f}')
    T = MAN['clips']['repel']['tick']
    check('repel: KW the left hand, KK the right sole (manifest columns)', max(math.dist(cont['KW']['p'], T['hand_l'][t]) for t in range(36, 49)) <= .12 and math.dist(cont['KK']['p'], T['foot_r'][129]) <= .12)
    for a, ta, b in (('repel', 129, 'ending'), ('ending', 1372, 'coda')):
        d = max(math.dist(MAN['clips'][a]['tick'][c][ta], MAN['clips'][b]['tick'][c][0]) for c in ('shift', 'hilt', 'tip', 'hand_r', 'hand_l', 'foot_r', 'foot_l', 'head'))
        check(f'clips: {a} {ta} == {b} 0', d <= .02, f'{d}')
    idle = {c: MAN['clips']['coda']['tick'][c][120] for c in ('hilt', 'tip', 'hand_r', 'hand_l', 'foot_r', 'foot_l', 'head')}
    for k, t in (('cs0', 1440), ('cs1', 720), ('repel', 140), ('coda', 0), ('ending', 1372)):
        d = max(math.dist(MAN['clips'][k]['tick'][c][t], idle[c]) for c in idle)
        check(f'{k}: tick {t} is the avatar\'s idle (standing, the sword low)', d <= .002, f'{d}')
    check('idle: upright, the feet under the hips, the sword low in the right hand, the point forward and down', abs(idle['head'][0]) < .01 and abs(idle['head'][2]) < .01 and 1.7 < idle['head'][1] < 1.8
          and idle['foot_r'][0] == .125 and idle['foot_l'][0] == -.125 and idle['hilt'][0] > .3 and idle['hilt'][1] < 1 and idle['tip'][2] > idle['hilt'][2] + 1 and .1 < idle['tip'][1] < idle['hilt'][1])
    check('clips: the walk is planted (cs0 20-100 has no declared slide) and the steps are listed', MAN['clips']['cs0']['slides'] == [] and MAN['clips']['cs0']['steps'][:10] == list(range(24, 97, 8)))

# ================================================================================================================ rebuild
TMP = HERE / 'tmp' / 'actor'
if A.rebuild or (want('replay') or want('jumps') or (want('clips') and False)):
    pass
if A.rebuild:
    assert A.rp, '--rebuild needs --rp'
    shutil.rmtree(TMP, ignore_errors=True)
    (TMP / 'dp/data/rlk/function').mkdir(parents=True)
    shutil.copytree(DP / 'tools', TMP / 'dp/tools', ignore=shutil.ignore_patterns('dev', '__pycache__'))
    shutil.copy(DP / 'pack.mcmeta', TMP / 'dp/pack.mcmeta')
    shutil.copytree(A.rp, TMP / 'rp')

    def tree_hash(root):
        h = hashlib.sha1()
        for f in sorted(p for p in Path(root).rglob('*') if p.is_file()):
            h.update(str(f.relative_to(root)).encode())
            h.update(f.read_bytes())
        return h.hexdigest()
    hs = []
    for i in range(2):
        r = subprocess.run(['node', str(TMP / 'dp/tools/build_player_rig.mjs'), '--datapack', str(TMP / 'dp'), '--resourcepack', str(TMP / 'rp'), '--cine-debug-dp', str(TMP / 'dbg')], capture_output=True, text=True)
        check(f'rebuild: run {i + 1} builds without an error or a warning', r.returncode == 0 and 'cine warning' not in r.stdout, (r.stderr or r.stdout)[-400:])
        hs.append((tree_hash(TMP / 'dp/data'), tree_hash(TMP / 'dp/tools/player_motion'), tree_hash(TMP / 'rp')))
    check('rebuild: two runs byte-identical (datapack, tools/player_motion, the pack)', hs[0] == hs[1], str(hs))
    for sub in ('data/rlk/function/char/cine', 'tools/player_motion'):
        a, b = tree_hash(TMP / 'dp' / sub), tree_hash(DP / sub)
        check(f'rebuild: {sub} of the tree is what the generator writes', a == b)
    mot = [p for p in (TMP / 'dp/data/rlk/function/char/motion').rglob('*') if p.is_file()]
    off = [str(p.relative_to(TMP / 'dp')) for p in mot if not (DP / p.relative_to(TMP / 'dp')).exists() or (DP / p.relative_to(TMP / 'dp')).read_bytes() != p.read_bytes()]
    check(f'rebuild: the player rig\'s own {len(mot)} files under char/motion are byte-identical to the tree\'s', not off and len(mot) > 2000, str(off[:4]))
    wrote = {str(p.relative_to(TMP / 'dp/data/rlk/function')).split('/')[1] for p in (TMP / 'dp/data/rlk/function').rglob('*.mcfunction')}
    check('rebuild: the generator writes only char/motion/** and char/cine/**', wrote == {'motion', 'cine'}, str(wrote))
    DBG = TMP / 'dbg'
    if A.ref_rp:
        ref, new = Path(A.ref_rp), TMP / 'rp'
        diff, added = [], []
        for f in sorted(p for p in new.rglob('*') if p.is_file()):
            rel = f.relative_to(new)
            if not (ref / rel).exists():
                added.append(str(rel))
            elif (ref / rel).read_bytes() != f.read_bytes():
                diff.append(str(rel))
        gone = [str(p.relative_to(ref)) for p in ref.rglob('*') if p.is_file() and not (new / p.relative_to(ref)).exists()]
        check('pack: every file of the reference pack is unchanged but the item atlas', diff == ['assets/minecraft/atlases/items.json'] and not gone, str(diff[:5]) + str(gone[:5]))
        exp = {'assets/rlk/textures/skin/lumine.png', 'assets/rlk/items/player_motion/weapons/cine_sword.json'} | {f'assets/rlk/{kind}/player_motion/{c}/{p}.json' for kind in ('items', 'models/item')
               for c in ('lumine', 'clorinde', 'ronova', 'nefer') for p in PARTS if p != 'weapon'}
        check('pack: added = Lumine\'s skin, cine_sword, the part items / models of the 4 characters (82 files)', set(added) == exp and len(exp) == 82, str(set(added) ^ exp))
        a0 = json.loads((ref / 'assets/minecraft/atlases/items.json').read_text())['sources']
        a1 = json.loads((new / 'assets/minecraft/atlases/items.json').read_text())['sources']
        key = lambda s: json.dumps(s, sort_keys=True)
        extra = sorted(set(map(key, a1)) - set(map(key, a0)))
        check('pack: the atlas only gains rlk:skin/{lumine,clorinde,ronova,nefer}', not (set(map(key, a0)) - set(map(key, a1))) and len(a1) == len(a0) + 4
              and [json.loads(x)['resource'] for x in extra] == ['rlk:skin/clorinde', 'rlk:skin/lumine', 'rlk:skin/nefer', 'rlk:skin/ronova'], str(extra))
        print('  atlas growth: 4 sources x 64 x 64 = 16 384 px')
elif (HERE / 'tmp/actor/dbg').exists():
    DBG = HERE / 'tmp/actor/dbg'

# ================================================================================================================ replay
TOL_T, TOL_R = .02, 2.5


def compare(w, clip, t, lag=False):
    """the worst part's distance to the built pose of tick t; lag: a part may still be one tick behind (the tick after a snap
    re-arms the running segments from the snapped pose: that one tick is made up by the segment's end)"""
    ref = ref_pose(clip, t)
    old = ref_pose(clip, t - 1) if lag and t > 0 else None
    wt = wr = 0
    for e in parts(w):
        dt, dr = tf_dist(w.shown(e), ref[e.data['_uuid']])
        if old:
            d2 = tf_dist(w.shown(e), old[e.data['_uuid']])
            if d2[0] <= TOL_T and d2[1] <= TOL_R:
                dt, dr = min(dt, d2[0]), min(dr, d2[1])
        wt, wr = max(wt, dt), max(wr, dr)
    return wt, wr


if want('replay') or want('jumps'):
    if DBG is None:
        print('replay / jumps: skipped (no debug poses: run once with --rebuild --rp <rp>)')
    else:
        if want('clips'):
            for k, L in CONTRACT.items():
                worst, prev = 0, ref_pose(k, 0)
                for t in range(1, L + 1):
                    cur = ref_pose(k, t)
                    worst = max(worst, max(qang(prev[u]['q'], cur[u]['q']) for u in UUIDS))
                    prev = cur
                check(f'{k}: no part turns more than 120 degrees in a tick', worst <= 120, f'{worst:.0f}')
        if want('replay'):
            for k, L in CONTRACT.items():
                w = world(4)
                spawn(w)
                run(w, 'rlk:char/cine/play', {'clip': k})
                wt = wr = 0
                where = None
                for t in range(L + 1):
                    tick(w, t)
                    dt, dr = compare(w, k, t, lag=t <= 24)
                    if dt > wt or dr > wr:
                        where = t
                    wt, wr = max(wt, dt), max(wr, dr)
                check(f'replay {k}: the shown pose == the built pose at every tick ({wt:.3f} b, {wr:.2f} deg)', wt <= TOL_T and wr <= TOL_R, f'worst near t{where}')
                check(f'replay {k}: no key re-sends an unchanged transform', not w.resend, str(w.resend[:4]))
                m0 = w.merges
                for t in range(L + 1, L + 30):
                    tick(w, t)
                dt, dr = compare(w, k, L)
                check(f'replay {k}: #cavT past the end holds the last frame, no command sent', w.merges == m0 and dt <= TOL_T and dr <= TOL_R, f'{w.merges - m0} merges')
            w = world(4)
            spawn(w)
            run(w, 'rlk:char/cine/play', {'clip': 'cs1'})
            for t in range(21):
                tick(w, t)
            m0 = w.merges
            for _ in range(15):
                tick(w, 20)
            dt, dr = compare(w, 'cs1', 20)
            check('replay: a frozen #cavT sends nothing and the frame stays', w.merges == m0 and dt <= TOL_T and dr <= TOL_R)
            for t in range(21, 60):
                tick(w, t)
            dt, dr = compare(w, 'cs1', 59)
            check('replay: the clock resumes from the frozen tick', dt <= TOL_T and dr <= TOL_R)
            w = world(4)
            spawn(w)
            tick(w, 0)
            check('replay: tick without a clip keeps the spawn (idle) pose', w.merges == 0)
        if want('jumps'):
            for k, a, b in (('cs0', 100, 1290), ('cs1', 100, 566), ('cs0', 700, 1440), ('cs1', 300, 0), ('ending', 500, 1372)):
                w = world(4)
                spawn(w)
                run(w, 'rlk:char/cine/play', {'clip': k})
                for t in range(a + 1):
                    tick(w, t)
                tick(w, b)
                dt, dr = compare(w, k, b)
                check(f'jump {k} {a} -> {b}: that frame at once ({dt:.3f} b, {dr:.2f} deg)', dt <= 1e-3 and dr <= .05)
                wt = wr = 0
                for t in range(b + 1, min(CONTRACT[k], b + 80) + 1):
                    tick(w, t)
                    dt, dr = compare(w, k, t, lag=t <= b + 24)
                    wt, wr = max(wt, dt), max(wr, dr)
                check(f'jump {k} {a} -> {b}: tracks on from there ({wt:.3f} b, {wr:.2f} deg)', wt <= TOL_T and wr <= TOL_R and not w.resend, str(w.resend[:3]))
            for k, a, b in (('cs0', 30, 777), ('repel', 100, 43), ('ending', 10, 251), ('cs1', 0, 669)):
                w = world(4)
                spawn(w)
                run(w, 'rlk:char/cine/play', {'clip': k})
                for t in range(a + 1):
                    tick(w, t)
                wt = wr = 0
                for i, t in enumerate(range(b, min(CONTRACT[k], b + 80) + 1)):
                    tick(w, t)
                    if i >= 40:
                        dt, dr = compare(w, k, t)
                        wt, wr = max(wt, dt), max(wr, dr)
                check(f'jump {k} {a} -> {b} (any tick): lands within 40 ticks ({wt:.3f} b, {wr:.2f} deg)', wt <= TOL_T and wr <= TOL_R)
            w = world(4)
            spawn(w)
            run(w, 'rlk:char/cine/play', {'clip': 'cs1'})
            for t in list(range(0, 40)) + list(range(43, 60)):          # the module skips two ticks
                tick(w, t)
            dt, dr = compare(w, 'cs1', 59)
            check('jump: a short forward gap replays the keys between', dt <= TOL_T and dr <= TOL_R)
            w = world(4)
            spawn(w)
            run(w, 'rlk:char/cine/play', {'clip': 'repel'})
            for t in range(130):
                tick(w, t)
            before = {e.data['_uuid']: w.shown(e) for e in parts(w)}
            run(w, 'rlk:char/cine/play', {'clip': 'ending'})
            tick(w, 0)
            jump = max(max(tf_dist(w.shown(e), before[e.data['_uuid']])) for e in parts(w))
            dt, dr = compare(w, 'ending', 0)
            check(f'jump: repel 129 -> play ending, tick 0: nothing moves on screen ({jump:.3f})', jump <= .05 and dt <= 1e-3 and len(parts(w)) == 11)
            for t in range(1, 60):
                tick(w, t)
            dt, dr = compare(w, 'ending', 59)
            check('jump: the ending runs on after the clip change', dt <= TOL_T and dr <= TOL_R and not w.resend)

# ================================================================================================================ face
if want('face'):
    for y0, y1 in ((55.0, 100.0), (170.0, -170.0), (-30.0, 12.5)):
        w = world(1)
        run(w, 'rlk:char/cine/spawn', at=(STAGE[0], (y0, 0.0)))
        run(w, 'rlk:char/cine/play', {'clip': 'coda'})
        tick(w, 0)
        run(w, 'rlk:char/cine/face', {'yaw': y1})
        ys = []
        for t in range(1, 16):
            tick(w, t)
            ys.append(roots(w)[0].rot[0])
        d = lambda a, b: abs((a - b + 180) % 360 - 180)
        steps = [d(a, b) for a, b in zip([y0] + ys, ys)]
        check(f'face {y0:g} -> {y1:g}: there in 12 ticks, the short way, the parts with the root', d(ys[11], y1) < .2 and d(ys[14], y1) < .2 and max(steps) <= d(y0, y1) / 12 + .6
              and all(d(e.rot[0], ys[-1]) < 1e-6 for e in parts(w)) and all(math.dist(e.pos, STAGE[0]) < 1e-9 for e in parts(w)), f'{ys[11]} {max(steps):.2f}')

print(f'test_actor: {ok}/{ok + bad} passed' + (f' ({bad} FAILED: {FAILS[:6]})' if bad else ''))
sys.exit(1 if bad else 0)
