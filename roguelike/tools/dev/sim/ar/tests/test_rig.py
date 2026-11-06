#!/usr/bin/env python3
"""test_rig.py [--dp ROGUELIKE] [--rp RP] [--rebuild] — the S2 suite of the 아를레키노 (Arlecchino) rig and sequences.

  manifest     api.check_manifest (26 parts in order, the 41 clips with identical len / loop / events / forms), parents == the
               stub, clip ids, looks, anchors, UUIDs, every api.RIG_CALLS + play/start per clip + face/set exist, budgets
  models       phase 1 shows the avatar's item models rlk:player_motion/arle/<part> and rlk:player_motion/weapons/scythe (named
               by the rig, never written: the RP files are byte-identical to the release RP S:tk/rp, nothing under
               player_motion is in the rig's output dirs); P2 arm boxes 4 px wide with the classic UVs, the avatar's 3 px;
               the embedded skin (tools/arlecchino_skin_p2.mjs) and the RP's skin_p2.png equal S:ar/src/skin_33.png byte for byte
  shipped      every clip replayed from its key files (data merge with interpolation, the form guards) for each form it is
               compiled for: no shown model point below the feet at any tick (body, both scythes and their blade tips, the
               wing / leg segments, cup, saucer; hulls from the RP's item models), no part turning more than 120 degrees in a
               tick (a 0-tick snap excepted), every point inside the culling box
  runtime      (mcsim) spawn = 26 parts + the shadow, tags, UUIDs; tick advances; play/<clip> queues and runs every clip;
               look/* idempotent; state/hidden scales every part to 0; anchor/<name> moves the one rlk_kn_anchor marker;
               rig/kill and rig/uninstall leave no part, no marker, no rig storage
  seq          seq.py builds with a dummy Writer, writes only seq/<name>/{start,tick,cancel}, every #sq tick it uses lies
               inside its clip, start plays the clip, #sqdone at the end, every rig function it calls exists, cancel has no
               executor-relative command, no music / phase / invulnerability lines, the titles and the push ring at their events
  --rebuild    runs the builder twice and checks the outputs are byte-identical
"""
import argparse
import base64
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

S = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
ap = argparse.ArgumentParser()
ap.add_argument('--dp', default=os.environ.get('KN_DP', str(S / 'ar/wt_i1/roguelike')))
ap.add_argument('--rp', default=str(S / 'ar/rp_s2'))
ap.add_argument('--ref-rp', default=str(S / 'tk/rp'))
ap.add_argument('--rebuild', action='store_true')
A = ap.parse_args()
DP, RP, REF = Path(A.dp), Path(A.rp), Path(A.ref_rp)
sys.path.insert(0, str(DP / 'tools'))
sys.path.insert(0, str(S / 'mb3/tests'))
import mcsim  # noqa: E402
from mboss_arlecchino import api, seq  # noqa: E402

RIG = DP / 'data/rlk/function/boss/arlecchino/rig'
NS = 'rlk:boss/arlecchino/rig'
MAN = json.loads((DP / 'tools/arlecchino_rig_manifest.json').read_text())
STUB = json.loads((DP / 'tools/mboss_arlecchino/stub_rig_manifest.json').read_text())
UU = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
FAIL, OK = [], []


def check(label, cond, detail=''):
    (OK if cond else FAIL).append(label)
    if not cond:
        print('FAIL ' + label + (('  ' + detail) if detail else ''))


if A.rebuild:
    def snap():
        h = hashlib.sha1()
        for root in (RIG, RP / 'assets/rlk/models/item/mboss/arlecchino', RP / 'assets/rlk/items/mboss/arlecchino', RP / 'assets/rlk/textures/mboss/arlecchino'):
            for p in sorted(root.rglob('*')):
                if p.is_file():
                    h.update(str(p.relative_to(root)).encode()); h.update(p.read_bytes())
        for p in (DP / 'tools/arlecchino_rig_manifest.json', RP / 'assets/minecraft/atlases/items.json'):
            h.update(p.read_bytes())
        return h.hexdigest()
    hs = []
    for _ in range(2):
        r = subprocess.run(['node', 'tools/build_arlecchino_rig.mjs', '--resourcepack', str(RP)], cwd=DP, capture_output=True, text=True)
        check('rebuild: the builder runs', r.returncode == 0, r.stderr[-400:])
        hs.append(snap())
    check('rebuild: two builds byte-identical (rig functions, RP models / items / textures, atlas, manifest)', hs[0] == hs[1])
    MAN = json.loads((DP / 'tools/arlecchino_rig_manifest.json').read_text())

# ================================================================ manifest vs contract
try:
    api.check_manifest(MAN)
    check('manifest: api.check_manifest (parts, clip len / loop / events / form, anchors)', True)
except AssertionError as e:
    check('manifest: api.check_manifest', False, str(e))
check('manifest: parents == the stub', [(p['name'], p['parent']) for p in MAN['parts']] == [(p['name'], p['parent']) for p in STUB['parts']])
check('manifest: clip ids == api.CLIP_ORDER', [n for n, _ in sorted(MAN['clips'].items(), key=lambda kv: kv[1]['id'])] == list(api.CLIP_ORDER))
check('manifest: looks == api.LOOKS', MAN['looks'] == {k: list(v) for k, v in api.LOOKS.items()})
check('manifest: anchors == api.ANCHORS', MAN['anchors'] == list(api.ANCHORS))
check('manifest: size / height / hip == api', (MAN['size'], MAN['height'], MAN['hip_y']) == (api.SIZE, api.HEIGHT, api.HIP_Y))
check('manifest: UUIDs', all(p['uuid'] == api.RIG_UUID.format(i) for i, p in enumerate(MAN['parts'])) and MAN['shadow']['uuid'] == api.RIG_UUID.format(0x40))
check('manifest: P1 body models = the avatar\'s, P2 = rlk:mboss/arlecchino/p2/*, scythes = the avatar scythe',
      all(MAN['parts'][i]['model']['p1'] == api.AVATAR_MODEL[p] and MAN['parts'][i]['model']['p2'] == api.P2_MODEL[p] for i, p in enumerate(api.BODY))
      and all(p['model']['p1'] == p['model']['p2'] == api.SCYTHE_MODEL for p in MAN['parts'] if p['name'].startswith('scythe')))
B = MAN['budgets']
check(f'budget: atlas <= 0.15 M px ({B["atlas_px"]})', B['atlas_px'] <= 150000)
check(f'budget: elements at rest <= 6500 ({B["elements_at_rest"]})', max(B['elements_at_rest'].values()) <= 6500)
calls = list(api.RIG_CALLS) + [f'play/{c}' for c in api.CLIPS] + [f'start/{c}' for c in api.CLIPS] + list(api.RIG_MACRO_CALLS)
missing = [c for c in calls if not (RIG / f'{c}.mcfunction').exists()]
check('functions: every rig call exists (api.RIG_CALLS, play / start per clip, face/set)', not missing, ', '.join(missing[:10]))
check('functions: face/set is a macro with $(yaw)', '$(yaw)' in (RIG / 'face/set.mcfunction').read_text())
allfn = {str(p.relative_to(RIG))[:-11]: p.read_text() for p in RIG.rglob('*.mcfunction')}
refs = set(re.findall(r'function (rlk:[a-z0-9_/]+)', '\n'.join(allfn.values())))
bad = [r for r in refs if r.startswith(NS + '/') and r[len(NS) + 1:] not in allfn]
check('functions: every rig-internal reference exists', not bad, ', '.join(sorted(bad)[:8]))
ext = sorted(r for r in refs if not r.startswith(NS + '/'))
check('functions: the rig calls no function outside rig/** (stand-alone load)', not ext, str(ext[:5]))
neg = [n for n, t in allfn.items() if re.search(r'scoreboard players (add|remove) \S+ \S+ -\d', t)]
check('functions: no negative add / remove literals', not neg, ', '.join(neg[:5]))
objs = set(re.findall(r'scoreboard objectives add (\S+)', allfn['init']))
check(f'objectives: knRig* only ({len(objs)})', objs and all(o.startswith('knRig') for o in objs), str(sorted(objs)))
check('objectives: uninstall removes every init objective', objs == set(re.findall(r'scoreboard objectives remove (\S+)', allfn['uninstall'])))
upper = [n for n, t in allfn.items() if re.search(r'"rlk:[^"]*[A-Z][^"]*"', t)]
check('functions: lowercase resource ids', not upper, str(upper[:3]))
sp = allfn['spawn']
summons = re.findall(r'summon minecraft:item_display ~ ~ ~ \{UUID:\[I;([-\d,]+)\],Tags:(\[[^\]]*\])', sp)
check(f'spawn: 27 item displays (26 parts + the shadow) ({len(summons)})', len(summons) == 27)
tagbad = []
for p in MAN['parts']:
    tags = next((json.loads(tg) for u, tg in summons if [int(x) for x in u.split(',')][3] == p['nn']), None)
    if tags != ['rlk_room', 'rlk_mb_aux', 'rlk_mb_part', 'rlk_kn_part', 'rlk_kn_' + p['name']]:
        tagbad.append(f'{p["name"]} {tags}')
check('spawn: part tags rlk_room rlk_mb_aux rlk_mb_part rlk_kn_part rlk_kn_<part>', not tagbad, str(tagbad[:3]))
cull = MAN['culling']
check('spawn: culling and view range as the manifest', sp.count(f'view_range:{MAN["view_range"]}f') == 27 and sp.count(f'width:{cull["width"]}f,height:{cull["height"]}f') == 27)
ids = [[int(x) for x in u.split(',')] for u, _ in summons]
check('spawn: UUID high ints 524c4b4d-4b4e-4100-8000', all(i[:3] == [0x524c4b4d, 0x4b4e4100, -0x80000000] for i in ids), str(ids[:1]))

# ================================================================ models: the avatar's reused, P2 classic arms, the skin
def item_model_path(item_id, rp=RP):
    ns, path = item_id.split(':')
    it = json.loads((rp / f'assets/{ns}/items/{path}.json').read_text())
    mid = it['model']['model']
    mns, mpath = mid.split(':')
    return rp / f'assets/{mns}/models/{mpath}.json'


reused = list(api.AVATAR_MODEL.values()) + [api.SCYTHE_MODEL]
same = []
for m in reused:
    a, b = item_model_path(m), item_model_path(m, REF)
    if a.read_bytes() != b.read_bytes() or (RP / f'assets/rlk/items/{m.split(":")[1]}.json').read_bytes() != (REF / f'assets/rlk/items/{m.split(":")[1]}.json').read_bytes():
        same.append(m)
check('models: the avatar\'s item models and the scythe are byte-identical to the release RP (named, never written)', not same, str(same[:3]))
spawn_ids = set(re.findall(r'"minecraft:item_model":"([^"]+)"', sp))
look_ids = set(re.findall(r'set value "(rlk:[^"]+)"', '\n'.join(allfn.values())))
check('models: the rig names rlk:player_motion/arle/<part> for every body part (spawn / look/form/p1)',
      all(api.AVATAR_MODEL[p] in spawn_ids | look_ids for p in api.BODY))
check('models: the rig writes nothing under player_motion (its RP dirs are mboss/arlecchino only)',
      not list((RP / 'assets/rlk/models/item/mboss/arlecchino').rglob('player_motion*')))
p2 = {p: json.loads((RP / f'assets/rlk/models/item/mboss/arlecchino/p2/{p}.json').read_text()) for p in api.BODY}
av = {p: json.loads(item_model_path(api.AVATAR_MODEL[p]).read_text()) for p in api.BODY}
w = lambda m: m['elements'][0]['to'][0] - m['elements'][0]['from'][0]
arms = [p for p in api.BODY if 'arm' in p]
check('models: P2 arms 4 px wide, the avatar\'s (P1) 3 px', all(w(p2[p]) == 4 for p in arms) and all(w(av[p]) == 3 for p in arms),
      str({p: (w(p2[p]), w(av[p])) for p in arms}))
uv = lambda m: m['elements'][0]['faces']['north']['uv']
check('models: P2 right arm classic UV (north face x 44..48 / 4), left arm (36..40 / 4)',
      uv(p2['right_arm'])[0] * 4 == 44 and uv(p2['right_arm'])[2] * 4 == 48 and uv(p2['left_arm'])[0] * 4 == 36 and uv(p2['left_arm'])[2] * 4 == 40,
      str((uv(p2['right_arm']), uv(p2['left_arm']))))
check('models: P2 legs / body / head boxes identical to the avatar\'s', all(p2[p]['elements'] == av[p]['elements'] for p in api.BODY if 'arm' not in p))
check('models: P2 parts textured rlk:mboss/arlecchino/skin_p2', all(m['textures']['skin'] == 'rlk:mboss/arlecchino/skin_p2' for m in p2.values()))
src = (S / 'ar/src/skin_33.png').read_bytes()
emb = re.search(r'SKIN_P2_B64 =\s*((?:\s*\'[A-Za-z0-9+/=]+\'\s*\+?)+);', (DP / 'tools/arlecchino_skin_p2.mjs').read_text())
dec = base64.b64decode(''.join(re.findall(r"'([A-Za-z0-9+/=]+)'", emb.group(1)))) if emb else b''
check('skin: the embedded P2 skin decodes to S:ar/src/skin_33.png byte for byte', dec == src, f'{len(dec)} vs {len(src)}')
check('skin: the RP texture skin_p2.png == skin_33.png', (RP / 'assets/rlk/textures/mboss/arlecchino/skin_p2.png').read_bytes() == src)
atlas = json.loads((RP / 'assets/minecraft/atlases/items.json').read_text())
srcs = {s.get('resource') for s in atlas['sources']}
need = {'rlk:mboss/arlecchino/' + n for n in MAN['sprites']}
check('atlas: every rig sprite has an items-atlas entry', need <= srcs, str(sorted(need - srcs)))

# ================================================================ shipped clips (replay of the key files)
def qmul(a, b):
    x, y, z, w_ = a
    X, Y, Z, W = b
    return [w_ * X + x * W + y * Z - z * Y, w_ * Y - x * Z + y * W + z * X, w_ * Z + x * Y - y * X + z * W, w_ * W - x * X - y * Y - z * Z]


def qrot(q, v):
    return qmul(qmul(q, [*v, 0]), [-q[0], -q[1], -q[2], q[3]])[:3]


def slerp(a, b, t):
    d = sum(x * y for x, y in zip(a, b))
    if d < 0:
        b, d = [-x for x in b], -d
    if d > .9995:
        r = [x + (y - x) * t for x, y in zip(a, b)]
        m = math.sqrt(sum(x * x for x in r))
        return [x / m for x in r]
    th = math.acos(d)
    s = math.sin(th)
    return [(x * math.sin((1 - t) * th) + y * math.sin(t * th)) / s for x, y in zip(a, b)]


def qangle(a, b):
    return 2 * math.degrees(math.acos(min(1, abs(sum(x * y for x, y in zip(a, b))))))


HULL = {}


def hull(item_id):
    """Corner points (block units about the pivot, after the client's Ry180, before the display transform) of an item model."""
    if item_id not in HULL:
        m = json.loads(item_model_path(item_id).read_text())
        pts = []
        for e in m['elements']:
            for x in (e['from'][0], e['to'][0]):
                for y in (e['from'][1], e['to'][1]):
                    for z in (e['from'][2], e['to'][2]):
                        P = [x, y, z]
                        r = e.get('rotation')
                        if r:
                            o, a = r['origin'], math.radians(r['angle'])
                            d = [P[i] - o[i] for i in range(3)]
                            c, s = math.cos(a), math.sin(a)
                            if r['axis'] == 'x':
                                d = [d[0], d[1] * c - d[2] * s, d[1] * s + d[2] * c]
                            elif r['axis'] == 'y':
                                d = [d[0] * c + d[2] * s, d[1], -d[0] * s + d[2] * c]
                            else:
                                d = [d[0] * c - d[1] * s, d[0] * s + d[1] * c, d[2]]
                            P = [d[i] + o[i] for i in range(3)]
                        pts.append((-(P[0] / 16 - .5), P[1] / 16 - .5, -(P[2] / 16 - .5)))
        HULL[item_id] = sorted(set(pts))
    return HULL[item_id]


NUM = re.compile(r'-?[\d.]+(?:e-?\d+)?')


def parse_tf(s):
    g = lambda k: [float(x) for x in NUM.findall(re.search(k + r':\[([^\]]*)\]', s).group(1))]
    return {'t': g('translation'), 'q': g('left_rotation'), 's': g('scale')}


UUID2PART = {p['uuid']: p['name'] for p in MAN['parts']}
FORM_ID = {f: i for i, f in enumerate(api.LOOKS['form'])}
KEY = re.compile(r'(?:execute (?:if score @s knRigForm matches (\d+)(?:\.\.(\d+))? )?(?:unless score @s knRig(?:Wr|Wl) matches 2 )?run )?'
                 r'data merge entity (\S+) \{start_interpolation:0,interpolation_duration:(\d+),transformation:(.*)\}$')


def shown_at(tgt, n, t):
    if n not in tgt:
        return None
    frm, to, t0, d = tgt[n]
    if d == 0 or t >= t0 + d or frm is None:
        return to
    u = (t - t0) / d
    return {'t': [a + (b - a) * u for a, b in zip(frm['t'], to['t'])], 'q': slerp(frm['q'], to['q'], u), 's': [a + (b - a) * u for a, b in zip(frm['s'], to['s'])]}


def replay(clip, form):
    """Per-tick shown transforms {part: (t, q, s)} of a clip from its key files for one form (weapons in hand)."""
    cd = RIG / 'c' / clip / 'k'
    L = MAN['clips'][clip]['len']
    fid = FORM_ID[form]
    tgt, out = {}, []
    for t in range(L + 1):
        f = cd / f'{t}.mcfunction'
        if f.exists():
            for line in f.read_text().splitlines():
                m = KEY.match(line)
                if not m or m.group(3) not in UUID2PART:
                    continue
                if m.group(1) is not None and not int(m.group(1)) <= fid <= int(m.group(2) or m.group(1)):
                    continue
                n = UUID2PART[m.group(3)]
                tgt[n] = (shown_at(tgt, n, t), parse_tf(m.group(5)), t, int(m.group(4)))
        out.append({n: (shown_at(tgt, n, t), tgt[n][3] == 0 and tgt[n][2] == t) for n in api.PARTS if n in tgt})
    return out


def model_of(n, form):
    p = next(p for p in MAN['parts'] if p['name'] == n)
    return p['model'][form]


floor_bad, step_bad, cull_bad, scythe_low = [], [], [], {}
W2, H = cull['width'] / 2, cull['height']
for clip, info in MAN['clips'].items():
    forms = info['compiled_forms']
    for form in forms:
        frames = replay(clip, form)
        prev = {}
        swap_t = {int(t) for t, f in (STUB['clips'][clip].get('formAt') or {}).items()} if False else set()
        for t, fr in enumerate(frames):
            # the form in force at tick t (t_p2 swaps to p2 at its 'swap' event)
            ff = 'p2' if clip == 't_p2' and t >= api.ev('t_p2', 'swap') else form
            for n, (v, snap) in fr.items():
                if v is None or max(abs(x) for x in v['s']) < 1e-4:
                    prev.pop(n, None)
                    continue
                pts = hull(model_of(n, ff))
                ys, rs = [], []
                for P in pts:
                    wv = qrot(v['q'], [P[i] * v['s'][i] for i in range(3)])
                    wp = [v['t'][i] + wv[i] for i in range(3)]
                    ys.append(wp[1])
                    rs.append((math.hypot(wp[0], wp[2]), wp[1]))
                if min(ys) < -.012:
                    floor_bad.append(f'{clip}[{form}] t{t} {n} {min(ys):.3f}')
                if n.startswith('scythe'):
                    scythe_low[clip] = min(scythe_low.get(clip, 9), min(ys))
                if any(r > W2 + .01 or y > H + .01 for r, y in rs):
                    cull_bad.append(f'{clip}[{form}] t{t} {n}')
                if n in prev and not snap and qangle(prev[n], v['q']) > 120.5:
                    step_bad.append(f'{clip}[{form}] {n} t{t - 1}->{t} {qangle(prev[n], v["q"]):.0f}')
                prev[n] = v['q']
check('shipped: no shown model point below the feet at any tick (every clip, every compiled form; body, scythes and blade tips, '
      'wings / legs, cup, saucer)', not floor_bad, '; '.join(floor_bad[:6]) + f' ({len(floor_bad)})')
check('shipped: no part turns more than 120 degrees in a tick', not step_bad, '; '.join(step_bad[:6]) + f' ({len(step_bad)})')
check('shipped: every point inside the culling box', not cull_bad, '; '.join(cull_bad[:6]) + f' ({len(cull_bad)})')
check(f'shipped: the scythes come within 0.1 b of the floor without dipping (stance, slams: lowest {min(scythe_low.values()):.3f} b)',
      0 <= min(scythe_low.values()) + .012 and min(scythe_low.values()) < .1)

# ================================================================ runtime (mcsim)
class Sim(mcsim.Sim):
    def ent_uuid(self, sel):
        return [e for e in self.ents if e.alive and e.data.get('_uuid') == sel]

    def select(self, sel, ctx):
        if UU.match(sel):
            return self.ent_uuid(sel)
        return super().select(sel, ctx)

    def holder(self, t, ctx):
        if UU.match(t):
            e = self.ent_uuid(t)
            return ('e', e[0].id) if e else ('u', t)
        return super().holder(t, ctx)

    def holders(self, t, ctx):
        if UU.match(t):
            return [self.holder(t, ctx)]
        return super().holders(t, ctx)

    @staticmethod
    def snbt2(s):
        s = s.replace('[I;', '[')
        s = re.sub(r'(?<=[:\[,])(-?)\.(\d)', r'\g<1>0.\2', s)
        return mcsim.Sim.snbt(s)

    def merge(self, dst, src):
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(dst.get(k), dict):
                self.merge(dst[k], v)
            else:
                dst[k] = json.loads(json.dumps(v))

    def cmd(self, t, ctx):
        c = t[0]
        if c == 'summon':
            pos = self.coords(t[2:5], ctx)
            nbt = self.snbt2(t[5]) if len(t) > 5 else {}
            e = mcsim.Ent(t[1].replace('minecraft:', ''), pos, tuple(nbt.get('Rotation', (0.0, 0.0))), nbt.get('Tags', []))
            e.data = {k: v for k, v in nbt.items() if k != 'Tags'}
            if 'UUID' in nbt:
                ints = [int(x) for x in nbt['UUID']]
                u = '-'.join([f'{ints[0] & 0xffffffff:08x}', f'{(ints[1] >> 16) & 0xffff:04x}', f'{ints[1] & 0xffff:04x}',
                              f'{(ints[2] >> 16) & 0xffff:04x}', f'{ints[2] & 0xffff:04x}{ints[3] & 0xffffffff:08x}'])
                if self.ent_uuid(u):
                    raise RuntimeError('summon with an existing UUID ' + u)
                e.data['_uuid'] = u
            self.ents.append(e)
            return 1
        if c == 'kill':
            for e in self.select(t[1], ctx):
                e.alive = False
            self.ents = [e for e in self.ents if e.alive]
            return 1
        if c == 'tp' and UU.match(t[1]):
            pos = self.coords(t[2:5], ctx)
            for e in self.select(t[1], ctx):
                e.pos = list(pos)
            return 1
        if c == 'data' and t[1] == 'merge' and t[2] == 'entity':
            v = self.snbt2(t[4])
            for e in self.select(t[3], ctx):
                self.merge(e.data, v)
            return 1
        if c == 'data' and t[1] == 'modify' and t[2] == 'entity' and len(t) > 7 and t[6] == 'value':
            path = [p.strip('"') for p in re.findall(r'"[^"]*"|[^.\[\]]+', t[4])]
            val = self.snbt2('{"v":' + t[7] + '}')['v']
            for e in self.select(t[3], ctx):
                o = e.data
                for p in path[:-1]:
                    o = o.setdefault(p, {})
                o[path[-1]] = val
            return 1
        if c == 'data' and t[1] == 'remove' and t[2] == 'storage':
            return super().cmd(t, ctx)
        if c == 'scoreboard' and t[1] == 'objectives':
            return 1
        if c in ('particle', 'playsound', 'rotate'):
            return 1
        return super().cmd(t, ctx)


def parts(sim):
    return {next(t[len('rlk_kn_'):] for t in e.tags if t.startswith('rlk_kn_') and t not in ('rlk_kn_part',)): e
            for e in sim.ents if e.alive and 'rlk_kn_part' in e.tags}


try:
    sim = Sim(DP / 'data/rlk/function')
    anchor = mcsim.Ent('husk', [760.5, 201.0, 8.5], (180.0, 0.0), ['rlk_kn_body'])
    sim.ents.append(anchor)
    call = lambda f: sim.call(f'{NS}/{f}', mcsim.Ctx(anchor, tuple(anchor.pos), tuple(anchor.rot)))
    call('spawn')
    P = parts(sim)
    check(f'runtime: spawn = 26 parts + the shadow ({len(P)})', len(P) == 27 and set(P) == set(api.PARTS) | {'shadow'})
    check('runtime: the shadow is not an rlk_mb_part', 'rlk_mb_part' not in P['shadow'].tags)
    check('runtime: UUIDs as the manifest', all(P[p['name']].data.get('_uuid') == p['uuid'] for p in MAN['parts']))
    check('runtime: the anchor table is loaded (rlk:kn rig.an, one entry per clip)', len(sim.storage.get('rlk:kn', {}).get('rig', {}).get('an', [])) == len(api.CLIPS))
    for _ in range(5):
        call('tick')
    check('runtime: tick advances knRigT', sim.sc(('e', anchor.id), 'knRigT') == 4, str(sim.sc(('e', anchor.id), 'knRigT')))
    bad = []
    for clip in api.CLIPS:
        call(f'play/{clip}')
        if sim.sc(('e', anchor.id), 'knRigC') != api.CLIP_ORDER.index(clip) or sim.sc(('e', anchor.id), 'knRigT') != -1:
            bad.append(clip)
        for _ in range(api.CLIPS[clip][0] + 2):
            call('tick')
    check('runtime: play/<clip> queues every clip (knRigC = id, knRigT -1) and every clip runs to its end', not bad, str(bad))
    form_of = lambda: sim.sc(('e', anchor.id), 'knRigForm')
    call('play/t_p2')
    for _ in range(api.ev('t_p2', 'swap') + 2):
        call('tick')
    check('runtime: t_p2 swaps the form to p2 at its swap event (P2 body models)', form_of() == 1 and
          parts(sim)['head'].data['item']['components']['minecraft:item_model'] == api.P2_MODEL['head'])
    call('play/idle')
    call('tick')
    check('runtime: a p1 clip puts the form back to p1 at its tick 0 (the avatar models)', form_of() == 0 and
          parts(sim)['head'].data['item']['components']['minecraft:item_model'] == api.AVATAR_MODEL['head'])
    snap = lambda: json.dumps({n: e.data for n, e in sorted(parts(sim).items())}, sort_keys=True) + json.dumps({o: sim.sc(('e', anchor.id), o) for o in sorted(objs)})
    idem = []
    for ch, vals in api.LOOKS.items():
        for v in vals:
            call(f'look/{ch}/{v}')
            a = snap()
            call(f'look/{ch}/{v}')
            if snap() != a:
                idem.append(f'{ch}/{v}')
    check('runtime: look/* idempotent', not idem, str(idem))
    call('look/form/p2')
    check('runtime: look/form/p2 shows the blade legs and scythe_l', parts(sim)['leg_1a'].data['item']['components']['minecraft:item_model'] == 'rlk:mboss/arlecchino/leg_a'
          and parts(sim)['scythe_l'].data['item']['components']['minecraft:item_model'] == api.SCYTHE_MODEL)
    call('look/form/p1'); call('look/wings/open')
    check('runtime: look/wings/open (p1) shows the wing models', parts(sim)['leg_1a'].data['item']['components']['minecraft:item_model'] == 'rlk:mboss/arlecchino/wing_a')
    call('look/wings/off'); call('look/weapon_r/gone')
    check('runtime: look/weapon_r/gone hides scythe_r (empty model)', parts(sim)['scythe_r'].data['item']['components']['minecraft:item_model'] == 'rlk:mboss/arlecchino/empty')
    call('look/weapon_r/hand')
    call('play/a2')
    for _ in range(api.ev('a2', 'h1') + 1):
        call('tick')
    moved = []
    for a in api.ANCHORS:
        call(f'anchor/{a}')
        mk = [e for e in sim.ents if e.alive and 'rlk_kn_anchor' in e.tags]
        moved.append((a, len(mk), tuple(round(x, 2) for x in mk[0].pos) if mk else None))
    check('runtime: anchor/<name> moves the one rlk_kn_anchor marker (form p1: blade_l = hand_l, the other 6 distinct, within 4 b)',
          all(n == 1 for _, n, _ in moved) and len({p for _, _, p in moved}) == 6 and dict((a, p) for a, _, p in moved)['blade_l'] == dict((a, p) for a, _, p in moved)['hand_l']
          and all(math.dist(p, anchor.pos) < 4 for _, _, p in moved), str(moved))
    call('state/hidden')
    check('runtime: state/hidden scales every part to 0',
          all(e.data.get('transformation', {}).get('scale') == [0.0, 0.0, 0.0] for n, e in parts(sim).items() if n != 'shadow'))
    call('state/normal')
    call('kill')
    check('runtime: rig/kill leaves no part and no anchor marker', not parts(sim) and not [e for e in sim.ents if e.alive and 'rlk_kn_anchor' in e.tags])
    call('spawn')
    call('anchor/chest')
    call('uninstall')
    check('runtime: rig/uninstall leaves no part, no marker, no rig storage', not parts(sim) and not [e for e in sim.ents if e.alive and 'rlk_kn_anchor' in e.tags]
          and 'rig' not in sim.storage.get('rlk:kn', {}))
except Exception as e:  # noqa: BLE001
    import traceback
    traceback.print_exc()
    check('runtime: mcsim run', False, repr(e))


# ================================================================ seq.py
class DummyWriter:
    def __init__(self):
        self.files = {}

    def w(self, rel, body):
        assert rel.startswith(api.OWN['S2seq']), rel
        self.files[rel] = body


Wd = DummyWriter()
try:
    for s in seq.SERVICES:
        s.build(Wd)
    check('seq: builds with a dummy Writer (owned prefix seq/ only)', True)
except AssertionError as e:
    check('seq: builds with a dummy Writer (owned prefixes only)', False, str(e))
check('seq: one Service per api.SEQS', [s.name for s in seq.SERVICES] == list(api.SEQS))
want = {f'seq/{n}/{p}' for n in api.SEQS for p in ('start', 'tick', 'cancel')}
check('seq: writes exactly seq/<name>/{start,tick,cancel}', set(Wd.files) == want, str(sorted(set(Wd.files) ^ want)))
over = []
for s in seq.SERVICES:
    ln = api.CLIPS[s.clip][0]
    for line in Wd.files[f'seq/{s.name}/tick']:
        for a in re.findall(r'#sq kn matches (\d+)(?!\.)', line):
            if int(a) > ln:
                over.append(f'{s.name} {a}')
    if f'{api.NS}rig/play/{s.clip}' not in ' '.join(Wd.files[f'seq/{s.name}/start']):
        over.append(f'{s.name}: start does not play {s.clip}')
    if not any(f'#sq kn matches {ln}..' in l and '#sqdone kn 1' in l for l in Wd.files[f'seq/{s.name}/tick']):
        over.append(f'{s.name}: no #sqdone at {ln}')
    if 'scoreboard players set #sqdone kn 0' not in Wd.files[f'seq/{s.name}/start']:
        over.append(f'{s.name}: start does not clear #sqdone')
check('seq: every #sq tick inside its clip, start plays the clip and clears #sqdone, #sqdone at the clip end', not over, str(over))
rigrefs = set(re.findall(r'function rlk:boss/arlecchino/rig/([a-z0-9_/]+)', '\n'.join('\n'.join(v) for v in Wd.files.values())))
check(f'seq: every rig function it calls exists ({len(rigrefs)})', all((RIG / f'{r}.mcfunction').exists() for r in rigrefs), str(rigrefs))
check('seq: cancel has no executor-relative command', all(not re.search(r'@s|~', l) for n in api.SEQS for l in Wd.files[f'seq/{n}/cancel']))
forbidden = [l for v in Wd.files.values() for l in v if re.search(r'mboss/music|rlk_mb_inv|#ph kn|mboss/repool|mboss/cine', l)]
check('seq: no music / invulnerability / phase / repool / cine (core-owned)', not forbidden, str(forbidden[:3]))
it, tp = '\n'.join(Wd.files['seq/intro/tick']), '\n'.join(Wd.files['seq/t_p2/tick'])
check('seq: the intro title at title (mboss_lib.title, api.TITLE_P1)', f'#sq kn matches {api.ev("intro", "title")} at @s run function rlk:mboss/title {{title:"{api.TITLE_P1[0]}"' in it)
check('seq: the intro push ring at push (mboss_lib.push_ring)', f'#sq kn matches {api.ev("intro", "push")} at @s run function rlk:mboss/push/ring' in it)
check('seq: t_p2 title at title (api.TITLE_P2)', f'#sq kn matches {api.ev("t_p2", "title")} at @s run function rlk:mboss/title {{title:"{api.TITLE_P2[0]}"' in tp)
check('seq: t_p2 blindness at dark', f'#sq kn matches {api.ev("t_p2", "dark")} run effect give @a[tag=player] minecraft:blindness' in tp)
check('seq: t_p2 the arena look job crimson at dark when the arena exists (api.arena_look)',
      (api.arena_look('crimson') in tp) if api.arena_ready() else 'rlk:mboss/arena/' not in tp)
wisps = re.findall(r'summon minecraft:marker [^{]*\{Tags:(\[[^\]]*\])\}', '\n'.join(Wd.files['seq/intro/start']))
check('seq: the intro summons the three wisp markers (rlk_room rlk_mb_aux rlk_kn_prop rlk_kn_wisp rlk_kn_wisp_<i>)',
      len(wisps) == 3 and all({'rlk_room', 'rlk_mb_aux', 'rlk_kn_prop', 'rlk_kn_wisp'} <= set(json.loads(w)) for w in wisps))
posts = [l for l in Wd.files['seq/intro/tick'] if f'matches {api.ev("intro", "flee") + 20}..{api.CLIPS["intro"][0]} ' in l and 'rlk_kn_wisp_' in l]
ok_posts = []
# S5 (AR-01): over the post blocks = the theme's POINTS['wisps'] (y 204.6), from her at the marker's block centre (CX + 0.5,
# CZ + 0.5); the post cells sit at the bearings of api.WISP_POSTS (a block grid: within 3 deg), r ~28.5-29
sys.path.insert(0, str(Path(DP) / 'tools'))
import mboss_arena_fl_ruins as TH  # noqa: E402
for i, (b, r) in enumerate(api.WISP_POSTS):
    m = next((re.search(r'~(-?[\d.]+) ~(-?[\d.]+) ~(-?[\d.]+)', l) for l in posts if f'rlk_kn_wisp_{i},' in l), None)
    if m:
        x, y, z = (float(v) for v in m.groups())
        px, py, pz = TH.POINTS['wisps'][i][:3]
        ok_posts.append(abs(x - (px - api.CX - .5)) < .02 and abs(y - (py - api.CY)) < .02 and abs(z - (pz - api.CZ - .5)) < .02
                        and abs((math.degrees(math.atan2(x, -z)) - b + 180) % 360 - 180) < 3)
check('seq: the wisps hold their rim posts (over the post blocks, theme POINTS; bearings api.WISP_POSTS) from flee + 20 to '
      'the intro end', len(ok_posts) == 3 and all(ok_posts), str(posts[:3]))
kitless = [l for v in Wd.files.values() for l in v if 'fx/' in l and not api.KIT_MANIFEST.exists()]
check('seq: no kit reference while the kit manifest is missing (api.K stand-in)', not kitless, str(kitless[:2]))

print(f'\n{len(OK)} passed, {len(FAIL)} failed')
sys.exit(1 if FAIL else 0)
