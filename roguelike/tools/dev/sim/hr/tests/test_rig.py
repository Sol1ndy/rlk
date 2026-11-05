#!/usr/bin/env python3
"""test_rig.py [--dp ROGUELIKE] [--rp RP] [--rebuild] [-v] — the S2a suite of the 홍련 (Scarlet) rig (run from HR/tests, outside the
datapack; S2b takes it over with the manifest, api.HANDOVER).

  manifest   api.check_manifest (29 parts in order, the 47 clips with identical len / loop / events / ids, anchors, looks, calls),
             parents / re-parent table == api, the 39 S2a clips authored and the 8 cine clips owned by S2b, UUIDs, every
             api.RIG_CALLS + play / start per clip + face/set exist, function references, objectives hrRig* only, no negative
             add / remove literals, lowercase ids, budgets (atlas <= 0.15 M px, elements at rest <= 6 500)
  spawn      29 parts + the shadow (nn 0x40, not an rlk_mb_part), tags, UUID high ints, billboard fixed, view range 2,
             culling 8 x 8, brightness 13 (sword_glow 15)
  models     every part model and its ghost twin exist; ghost twins use only rlk:mboss/scarlet/ghost and the same elements;
             every element inside -16..32 with one rotation axis of -45 / -22.5 / 0 / 22.5 / 45; the brim = four squares
             0.003 b apart (not coplanar) at four distinct turns mod 90, its sprite painting only its own corner wedges (the
             four turns cover the ring once); atlas entries for every sprite
  item       rlk:mboss/scarlet/item_sword: rig textures only (0 extra px), the gui / hand / ground / fixed transforms, points
             like a vanilla sword in the gui (hilt lower left, tip upper right), lies flat on the ground above the floor
  shipped    every clip replayed from its key files (data merge with interpolation; the hand / face swaps it keys): no shown
             model point below the floor at any tick (blade and scabbard tips, the brim, the hair, the skirt panels and every
             other part, hulls from the RP's models), no part turning more than 120 degrees in a tick (a 0-tick snap excepted),
             every point inside the culling box; the blade points away from her sword arm and the hand-held scabbard away
             from her right arm (held props right); the blade tip >= 0.10 b over the floor in idle / idle2 / walk
  hats       the five hat states: look/hat/<state> stores hrRigHat and puts the hat where the state says (worn over the head,
             back behind the torso, hand beside the right hand, world on the floor, gone at scale 0); the clips key only
             contract states; `down` keeps it on the floor, `kipup` goes world -> hand -> worn
  runtime    (mcsim) spawn, tick, play/<clip> for all 47 clips, look/* idempotent, the form / phase / blade swaps,
             state/hidden, anchor/<name> moves the one rlk_hr_anchor marker, rig/kill and rig/uninstall leave nothing
  palette    PLAN §1.5: the base paints of the six roles keep CIE76 dE >= 10 from the original's (hat top #E6DCCF, bodysuit
             #E4E2E8, thigh-highs #CFCBD3, tasset #8E6CB4, gold strip #CDB78C, hair #DDD7E2), declared and measured on the
             sprites; with the user's skin (S2c) the body roles are the skin's own pixels (declared 'skin': exempt) and the
             check keeps the rig's own paints (the hat, the gold)
  skin       (S2c, when the manifest carries `skin`) the RP's skin.png is byte-identical to the user's file
             (HR/skin/scarlet_skin_64.png) and to the embedded tools/scarlet_skin.mjs (sha1), 64 x 64, its items-atlas entry
             and its 4 096 px in the ledger; every face of every skin-mapped model (head, torso, pelvis, arms, forearms with
             each hand, thighs, shins, the hair slabs) lands on its declared region and rows of the vanilla layout (base box
             -> base layer, second box -> outer layer); the outer box encloses the base box and stands out laterally; the
             hidden parts (model empty) stay at scale 0 and are keyed only at a clip's tick 0; the face overlays (calm none,
             smile / closed only their declared pixels); the ghost twins of skin faces show the whole gradient; no blade sample
             inside her torso / pelvis / head / upper arms / thighs / shins at any clip event (the hands hold the hilt and the
             scabbard by design)
  --rebuild  runs the builder twice: the rig functions, the RP mboss/scarlet files, the atlas and the manifest byte-identical
"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = Path('/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad')
ap = argparse.ArgumentParser()
# defaults: S2b's tree / RP when they exist (S2b takes the suite over), else S2a's
_wt = next((p for p in ('hr/wt_s2b/roguelike', 'hr/wt_s2a/roguelike') if (S / p).exists()), 'hr/wt_s2a/roguelike')
_rp = next((p for p in ('hr/rp_s2b', 'hr/rp_s2a') if (S / p).exists()), 'hr/rp_s2a')
ap.add_argument('--dp', default=os.environ.get('HR_DP', str(S / _wt)))
ap.add_argument('--rp', default=os.environ.get('HR_RP', str(S / _rp)))
ap.add_argument('--rebuild', action='store_true')
ap.add_argument('-v', action='store_true', help='list the passing checks too')
A = ap.parse_args()
DP, RP = Path(A.dp), Path(A.rp)
sys.path.insert(0, str(DP / 'tools'))
sys.path.insert(0, str(HERE / 'lib'))
import mcsim  # noqa: E402
from mboss_scarlet import api  # noqa: E402

RIG = DP / 'data/rlk/function/boss/scarlet/rig'
NS = 'rlk:boss/scarlet/rig'
MANP = DP / 'tools/scarlet_rig_manifest.json'
ASSETS = RP / 'assets/rlk'
UU = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
FAIL, OK = [], []


def check(label, cond, detail=''):
    (OK if cond else FAIL).append(label)
    if not cond:
        print('FAIL ' + label + (('  ' + str(detail)) if detail else ''))
    elif A.v:
        print('ok   ' + label)


if A.rebuild:
    def snap():
        h = hashlib.sha1()
        roots = [RIG] + [ASSETS / d / 'mboss/scarlet' for d in ('models/item', 'items', 'textures')]
        for root in roots:
            for p in sorted(root.rglob('*')):
                if p.is_file():
                    h.update(str(p.relative_to(root)).encode()); h.update(p.read_bytes())
        for p in (MANP, RP / 'assets/minecraft/atlases/items.json'):
            h.update(p.read_bytes())
        return h.hexdigest()
    hs = []
    for _ in range(2):
        r = subprocess.run(['node', 'tools/build_scarlet_rig.mjs', '--resourcepack', str(RP)], cwd=DP, capture_output=True, text=True)
        check('rebuild: the builder runs (strict: no floor / turn / budget error)', r.returncode == 0, r.stderr[-600:])
        hs.append(snap())
    check('rebuild: two builds byte-identical (rig functions, RP models / items / textures, atlas, manifest)', hs[0] == hs[1])

MAN = json.loads(MANP.read_text())
STUB = api.stub_manifest()

# ================================================================ manifest vs contract
try:
    api.check_manifest(MAN)
    check('manifest: api.check_manifest (parts, 47 clips len / loop / events / ids, anchors, looks, calls)', True)
except AssertionError as e:
    check('manifest: api.check_manifest', False, str(e))
check(f'manifest: 47 clips ({len(MAN["clips"])})', len(MAN['clips']) == 47 == len(api.CLIPS))
check('manifest: parents == api.PARENTS', {p['name']: p['parent'] for p in MAN['parts']} == dict(api.PARENTS))
check('manifest: the re-parent table == api.REPARENT', {(r['part'], r['look']): r['parent'] for r in MAN['reparent']} == dict(api.REPARENT))
own = {n: c['owner'] for n, c in MAN['clips'].items()}
check('manifest: owners == api.CLIP_OWNER', own == dict(api.CLIP_OWNER))
s2a = [n for n, o in api.CLIP_OWNER.items() if o == 'S2a']
check(f'manifest: the {len(s2a)} S2a clips are authored', len(s2a) == 39 and all(MAN['clips'][n]['authored'] for n in s2a),
      str([n for n in s2a if not MAN['clips'][n]['authored']]))
cine = MAN.get('cine_source', '')
check(f'manifest: the 8 cine clips come from S2b\'s tools/scarlet_cine.mjs or the built-in placeholder ({cine})',
      cine == 'tools/scarlet_cine.mjs' if (DP / 'tools/scarlet_cine.mjs').exists() else cine.startswith('placeholder'))
check('manifest: UUIDs api.RIG_UUID by part order, the shadow nn 0x40', all(p['uuid'] == api.RIG_UUID.format(i) and p['nn'] == i for i, p in enumerate(MAN['parts']))
      and MAN['shadow']['uuid'] == api.RIG_UUID.format(api.SHADOW_NN) and MAN['shadow']['radius'] == .9)
check('manifest: ghost texture == api.GHOST_MODEL, item model == api.ITEM_MODEL', MAN['ghost_texture'] == api.GHOST_MODEL and MAN['item_sword']['model'] == api.ITEM_MODEL)
B = MAN['budgets']
check(f'budget: atlas <= 0.15 M px ({B["atlas_px"]})', B['atlas_px'] <= 150000)
check(f'budget: elements at rest <= 6500 ({B["elements_at_rest"]})', max(B['elements_at_rest'].values()) <= 6500)
calls = list(api.RIG_CALLS) + [f'play/{c}' for c in api.CLIPS] + [f'start/{c}' for c in api.CLIPS] + list(api.RIG_MACRO_CALLS)
missing = [c for c in calls if not (RIG / f'{c}.mcfunction').exists()]
check(f'functions: every rig call exists (api.RIG_CALLS, play / start for the 47 clips, face/set) ({len(calls)})', not missing, ', '.join(missing[:10]))
check('functions: face/set is a macro with $(yaw)', '$(yaw)' in (RIG / 'face/set.mcfunction').read_text())
allfn = {str(p.relative_to(RIG))[:-11]: p.read_text() for p in RIG.rglob('*.mcfunction')}
refs = set(re.findall(r'function (rlk:[a-z0-9_/.-]+)', '\n'.join(allfn.values())))
bad = [r for r in refs if r.startswith(NS + '/') and r[len(NS) + 1:] not in allfn]
check('functions: every rig-internal reference exists', not bad, ', '.join(sorted(bad)[:8]))
ext = sorted(r for r in refs if not r.startswith(NS + '/'))
check('functions: the rig calls no function outside rig/** (stand-alone load)', not ext, str(ext[:5]))
neg = [n for n, t in allfn.items() if re.search(r'scoreboard players (add|remove) \S+ \S+ -\d', t)]
check('functions: no negative add / remove literals', not neg, ', '.join(neg[:5]))
objs = set(re.findall(r'scoreboard objectives add (\S+)', allfn['init']))
check(f'objectives: hrRig* only ({len(objs)})', objs and all(o.startswith('hrRig') for o in objs) and objs == set(MAN['objectives']), str(sorted(objs)))
check('objectives: uninstall removes every init objective', objs == set(re.findall(r'scoreboard objectives remove (\S+)', allfn['uninstall'])))
used = set(re.findall(r'@s (hrRig\w+)|#\w+ (hrRig\w+)', '\n'.join(allfn.values())))
check('objectives: every objective the rig uses is created by init', {a or b for a, b in used} <= objs, str({a or b for a, b in used} - objs))
upper = [n for n, t in allfn.items() if re.search(r'"rlk:[^"]*[A-Z][^"]*"', t)]
check('functions: lowercase resource ids', not upper, str(upper[:3]))
check(f'functions: count {len(allfn)} == the manifest\'s', len(allfn) == B['rig_functions'])

# ================================================================ spawn
sp = allfn['spawn']
summons = re.findall(r'summon minecraft:item_display ~ ~ ~ (\{UUID:\[I;([-\d,]+)\],.*)$', sp, re.M)
check(f'spawn: 30 item displays (29 parts + the shadow) ({len(summons)})', len(summons) == 30)
by_nn = {}
for full, u in summons:
    ints = [int(x) for x in u.split(',')]
    by_nn[ints[3]] = (ints, full)
tagbad, flagbad = [], []
for p in MAN['parts']:
    ints, full = by_nn.get(p['nn'], (None, ''))
    tags = json.loads(re.search(r'Tags:(\[[^\]]*\])', full).group(1)) if full else None
    if tags != ['rlk_room', 'rlk_mb_aux', 'rlk_mb_part', 'rlk_hr_part', 'rlk_hr_' + p['name']]:
        tagbad.append(f'{p["name"]} {tags}')
    want_b = 15 if p['name'] == 'sword_glow' else 13
    if not ('billboard:"fixed"' in full and 'view_range:2f' in full and 'width:8f,height:8f' in full and f'brightness:{{block:{want_b},sky:15}}' in full):
        flagbad.append(p['name'])
check('spawn: part tags rlk_room rlk_mb_aux rlk_mb_part rlk_hr_part rlk_hr_<part>', not tagbad, str(tagbad[:3]))
check('spawn: billboard fixed, view range 2, culling 8 x 8, block brightness 13 (sword_glow 15; sky 15)', not flagbad, str(flagbad[:5]))
sh = by_nn.get(api.SHADOW_NN, (None, ''))[1]
sh_tags = json.loads(re.search(r'Tags:(\[[^\]]*\])', sh).group(1)) if sh else []
check('spawn: the shadow helper (nn 0x40, radius 0.9, not an rlk_mb_part)', sh and 'shadow_radius:.9f' in sh and 'rlk_mb_part' not in sh_tags and 'rlk_hr_part' in sh_tags, sh[:160])
ids = [v[0] for v in by_nn.values()]
check('spawn: UUID high ints 524c4b4d-4852-4400-8000', all(i[:3] == [0x524c4b4d, 0x48524400, -0x80000000] for i in ids), str(ids[:1]))
spawn_models = set(re.findall(r'"minecraft:item_model":"([^"]+)"', sp))
check('spawn: every part spawns with its default model', all(f'rlk:mboss/scarlet/{p["model"]}' in spawn_models for p in MAN['parts']))


# ================================================================ models
def item_model(item_id):
    ns, path = item_id.split(':')
    it = json.loads((RP / f'assets/{ns}/items/{path}.json').read_text())
    mid = it['model']['model']
    mns, mpath = mid.split(':')
    return json.loads((RP / f'assets/{mns}/models/{mpath}.json').read_text())


ALL_MODELS = sorted({p['model'] for p in MAN['parts']} | {v for d in MAN['look_models']['hands'].values() for v in d.values()}
                    | set(MAN['look_models']['face'].values()) | {v for d in MAN['look_models']['phase'].values() for v in d.values()}
                    | set(MAN['look_models']['blade'].values()))
missing_m = [m for m in ALL_MODELS if not (ASSETS / f'items/mboss/scarlet/{m}.json').exists()]
check(f'models: every part / hand / face / phase / blade model has its item definition and model ({len(ALL_MODELS)})', not missing_m, str(missing_m))
GHOSTLESS = {'empty'} | {m for m in ALL_MODELS if m.startswith('glow_')}
ghost_bad, geo_bad = [], []
for m in ALL_MODELS:
    if m in GHOSTLESS:
        continue
    gp = ASSETS / f'items/mboss/scarlet/{m}_g.json'
    if not gp.exists():
        ghost_bad.append(m + ' (no ghost twin)')
        continue
    g, n = item_model(f'rlk:mboss/scarlet/{m}_g'), item_model(f'rlk:mboss/scarlet/{m}')
    tex = set(g['textures'].values())
    faces = [f for e in g['elements'] for f in e['faces'].values()]
    if tex != {api.GHOST_MODEL} or any(f['texture'] != '#ghost' or 'tintindex' in f for f in faces):
        ghost_bad.append(m)
    if [(e['from'], e['to'], e.get('rotation')) for e in g['elements']] != [(e['from'], e['to'], e.get('rotation')) for e in n['elements']]:
        geo_bad.append(m)
check('models: every part model has a ghost twin <model>_g using only rlk:mboss/scarlet/ghost (no tint)', not ghost_bad, str(ghost_bad[:5]))
check('models: ghost twins keep the geometry (same elements)', not geo_bad, str(geo_bad[:5]))
el_bad = []
for p in sorted((ASSETS / 'models/item/mboss/scarlet').glob('*.json')):
    m = json.loads(p.read_text())
    for e in m.get('elements', []):
        if min(e['from'] + e['to']) < -16 or max(e['from'] + e['to']) > 32:
            el_bad.append(f'{p.stem} bounds')
            break
        r = e.get('rotation')
        if r and (r['axis'] not in 'xyz' or r['angle'] not in (-45, -22.5, 0, 22.5, 45)):
            el_bad.append(f'{p.stem} rotation {r}')
            break
check('models: every element inside -16..32, one rotation axis of -45 / -22.5 / 0 / 22.5 / 45', not el_bad, str(el_bad[:5]))
brim_bad = []
for hm in ('hat_p1', 'hat_p2', 'hat_p1_g', 'hat_p2_g'):
    m = item_model(f'rlk:mboss/scarlet/{hm}')
    sq = [e for e in m['elements'] if e['to'][0] - e['from'][0] > 20 and e['to'][1] - e['from'][1] < .05]
    ys = sorted(e['from'][1] for e in sq)
    turns = sorted(round((e.get('rotation', {}).get('angle', 0)) % 90, 1) for e in sq)
    steps = [b - a for a, b in zip(ys, ys[1:])]
    if not (len(sq) == 4 and all(abs(s - .048) < 1e-3 for s in steps) and turns == [0, 22.5, 45, 67.5]
            and abs((sq[0]['to'][0] - sq[0]['from'][0]) / 16 - 1.6) < .01):
        brim_bad.append(f'{hm}: {len(sq)} squares, steps {steps}, turns {turns}')
check('models: the brim = four 1.60 b squares 0.003 b apart (no coplanar faces) at four turns 0 / 22.5 / 45 / 67.5 mod 90', not brim_bad, '; '.join(brim_bad))
try:
    from PIL import Image
    im = Image.open(ASSETS / 'textures/mboss/scarlet/brim.png').convert('RGBA')
    W_, H_ = im.size
    px = im.load()
    out_w, in_w, rib_soft = 0, 0, 0
    for y in range(H_):
        for x in range(W_):
            u, v = (x + .5) / W_ * 2 - 1, (y + .5) / H_ * 2 - 1
            r = math.hypot(u, v)
            if r < .3 or r > .97:
                continue
            a = math.degrees(math.atan2(v, u)) % 90
            dw = abs(a - 45)
            if dw > 11.25 + 3:
                out_w += px[x, y][3] > 0
            elif dw > 11.25:
                rib_soft += 0 < px[x, y][3] < 255
            elif dw < 10:
                in_w += px[x, y][3] == 0
    # the four squares' corner wedges (each +-11.25 deg about 45 + 90n, turned by 0 / 22.5 / 45 / 67.5) tile the ring once
    tiles = sorted(((45 + t - 11.25) % 90, (45 + t + 11.25) % 90) for t in (0, 22.5, 45, 67.5))
    check('models: the brim sprite paints only its corner wedges and the opaque boundary ribs (no stacked translucency where two squares meet)',
          out_w == 0 and rib_soft == 0, f'{out_w} px outside, {rib_soft} translucent rib px')
    check('models: the brim wedges are painted (the weave / ribs / rim inside +-10 deg; the mask holes are the weave pattern)', in_w < .5 * W_ * H_ * .2, f'{in_w} px empty')
    check('models: the four turned squares cover the ring exactly once (wedges 22.5 deg each, 22.5 deg apart)',
          all(abs(((b - a) % 90) - 22.5) < 1e-6 for a, b in tiles) and len({round(a, 3) for a, _ in tiles}) == 4)
except ImportError:
    check('models: PIL for the brim sprite', False)
atlas = json.loads((RP / 'assets/minecraft/atlases/items.json').read_text())
srcs = {s.get('resource') for s in atlas['sources']}
need = {f'rlk:mboss/scarlet/{n}' for n in MAN['sprites']}
check(f'atlas: every rig sprite has an items-atlas entry ({len(need)})', need <= srcs, str(sorted(need - srcs)[:5]))
on_disk = {p.stem for p in (ASSETS / 'textures/mboss/scarlet').glob('*.png')}
check('atlas: the sprite files == the manifest\'s sprites (nothing stale)', on_disk == set(MAN['sprites']), str(sorted(on_disk ^ set(MAN['sprites']))[:5]))
px_sum = 0
for n in MAN['sprites']:
    w, h = Image.open(ASSETS / f'textures/mboss/scarlet/{n}.png').size
    px_sum += w * h
check(f'atlas: the sprites measure {px_sum} px == the manifest budget', px_sum == B['atlas_px'])

# ================================================================ skin (S2c: the user's Minecraft skin on the body)
SK = MAN.get('skin')
if SK:
    import hashlib as _hl
    PART = {p['name']: p for p in MAN['parts']}
    USER_SKIN = S / 'hr/skin/scarlet_skin_64.png'
    sk_rp = (ASSETS / 'textures/mboss/scarlet/skin.png').read_bytes()
    check('skin: the RP skin.png is byte-identical to the user\'s file (HR/skin/scarlet_skin_64.png)', USER_SKIN.exists() and sk_rp == USER_SKIN.read_bytes())
    check('skin: ... and to the embedded tools/scarlet_skin.mjs (bytes, sha1)', len(sk_rp) == SK['bytes'] and _hl.sha1(sk_rp).hexdigest() == SK['sha1']
          and SK['sha1'] in (DP / 'tools/scarlet_skin.mjs').read_text())
    _sim = Image.open(ASSETS / 'textures/mboss/scarlet/skin.png')
    check('skin: 64 x 64 RGBA, items-atlas entry rlk:mboss/scarlet/skin, 4 096 px in the ledger', _sim.size == (64, 64) and _sim.mode == 'RGBA'
          and 'rlk:mboss/scarlet/skin' in srcs and MAN['sprites'].get('skin') == 4096 and SK['texture'] == 'rlk:mboss/scarlet/skin')

    def skin_uv(reg, start, end):
        u, v, w, h, d = reg
        f = lambda a, b, c, e: [round(a / 4, 4), round(b / 4, 4), round(c / 4, 4), round(e / 4, 4)]
        return {'east': f(u, v + d + start, u + d, v + d + end), 'north': f(u + d, v + d + start, u + d + w, v + d + end),
                'west': f(u + d + w, v + d + start, u + 2 * d + w, v + d + end), 'south': f(u + 2 * d + w, v + d + start, u + 2 * d + 2 * w, v + d + end),
                'up': f(u + d, v, u + d + w, v + d), 'down': f(u + d + w, v + d, u + d + 2 * w, v)}

    def hair_uv(v0, r0, r1):
        f = lambda a, b, c, e: [round(a / 4, 4), round(b / 4, 4), round(c / 4, 4), round(e / 4, 4)]
        y0, y1 = v0 + r0, v0 + r1
        return {'south': f(32, y0, 40, y1), 'north': f(40, y0, 32, y1), 'east': f(39, y0, 40, y1), 'west': f(32, y0, 33, y1),
                'up': f(32, y0, 40, min(y1, y0 + 1)), 'down': f(32, max(y0, y1 - 1), 40, y1)}
    uv_bad, lay_bad = [], []
    for m, (reg, r0, r1) in SK['map'].items():
        mm = item_model(f'rlk:mboss/scarlet/{m}')
        els = mm['elements']
        if len(els) != 2 or any(f['texture'] != '#skin' for e in els for f in e['faces'].values()) or mm['textures'].get('skin') != SK['texture']:
            uv_bad.append(f'{m}: {len(els)} elements / textures {mm["textures"]}')
            continue
        if reg == 'body_back':
            want = [hair_uv(20, r0, r1), hair_uv(36, r0, r1)]
        else:
            base, over = SK['regions'][reg]
            want = [skin_uv(base, r0, r1), skin_uv(over, r0, r1)]
        for e, w in zip(els, want):
            got = {k: f['uv'] for k, f in e['faces'].items()}
            off = [k for k in w if k not in got or any(abs(x - y) > 2e-3 for x, y in zip(got[k], w[k]))]
            if off or set(got) != set(w):
                uv_bad.append(f'{m}: {off}')
        b, o = els
        enclose = all(o['from'][i] <= b['from'][i] + 1e-6 and o['to'][i] >= b['to'][i] - 1e-6 for i in range(3))
        lateral = all(o['from'][i] < b['from'][i] - .05 and o['to'][i] > b['to'][i] + .05 for i in (0, 2))
        if not (enclose and lateral):
            lay_bad.append(m)
    check(f'skin: every face of the {len(SK["map"])} skin-mapped models lands on its declared region and rows (vanilla layout; base -> base layer, outer -> outer layer)',
          not uv_bad, '; '.join(uv_bad[:6]))
    check('skin: the outer layer present on every mapped model (the second box encloses the base box, out on the sides)', not lay_bad, str(lay_bad[:6]))
    need_m = {'head', 'torso', 'pelvis', 'arm_l', 'arm_r', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r', 'hair_tail_1', 'hair_tail_2'} | \
        {f'forearm_{s}_{k}' for s in 'lr' for k in ('open', 'grip', 'brim')}
    check('skin: the map covers the body (head, torso, pelvis, upper arms, forearms with every hand, thighs, shins, the hair)', need_m == set(SK['map']))
    check('skin: the parts the skin shows by default wear their skin models (head, torso, pelvis, arms, legs, hair)',
          all(PART[n]['model'] in SK['map'] for n in ('head', 'torso', 'pelvis', 'arm_l', 'arm_r', 'forearm_l', 'forearm_r', 'thigh_l', 'thigh_r',
                                                         'shin_l', 'shin_r', 'hair_tail_1', 'hair_tail_2')))
    gh_bad = []
    for m in SK['map']:
        g = item_model(f'rlk:mboss/scarlet/{m}_g')
        for e in g['elements']:
            for f in e['faces'].values():
                if sorted([round(f['uv'][0], 4), round(f['uv'][2], 4)]) != [0, round(16 / 3, 4)] or sorted([f['uv'][1], f['uv'][3]]) != [0, 16]:
                    gh_bad.append(m)
    check('skin: the ghost twins of the skin models show the whole ghost gradient on every face', not gh_bad, str(sorted(set(gh_bad))[:5]))
    hid = SK['hidden']
    check(f'skin: the hidden parts ({", ".join(hid)}) wear the empty model', hid and all(PART[n]['model'] == 'empty' for n in hid))
    UUIDN = {p['name']: p['uuid'] for p in MAN['parts']}
    late = sorted({f'{c}' for c in MAN['clips'] for f in (RIG / 'c' / c / 'k').glob('*.mcfunction')
                   if f.stem != '0' and any(UUIDN[n] in f.read_text() for n in hid)})
    check('skin: the hidden parts are keyed only at a clip\'s tick 0 (no keys after it)', not late, str(late[:5]))
    fc = item_model('rlk:mboss/scarlet/face_calm')
    fx = Image.open(ASSETS / 'textures/mboss/scarlet/face_fx.png').convert('RGBA')
    fxp = fx.load()
    want_px = set()
    for half, kind in ((0, 'closed'), (1, 'smile')):
        for c, r, w, h in SK['face_overlays'][kind]:
            for cc in range(c, c + w):
                for rr in range(r, r + h):
                    want_px.add((half, cc, rr))
    got_px = {(x // 16, (x % 16) // 2, y // 2) for y in range(16) for x in range(32) if fxp[x, y][3] > 0}
    check('skin: face overlays — calm none (the skin\'s own face), smile / closed paint only their declared pixels of the 8 x 8 face',
          not fc['elements'] and got_px <= want_px and len(item_model('rlk:mboss/scarlet/face_smile')['elements']) == len(SK['face_overlays']['smile'])
          and len(item_model('rlk:mboss/scarlet/face_closed')['elements']) == len(SK['face_overlays']['closed']), str(sorted(got_px - want_px)[:5]))

# ================================================================ item_sword
IS = item_model(api.ITEM_MODEL)
rig_tex = {f'rlk:mboss/scarlet/{n}' for n in MAN['sprites']}
other_tex = set()
for p in (ASSETS / 'models/item/mboss/scarlet').glob('*.json'):
    if p.stem != 'item_sword':
        other_tex |= set(json.loads(p.read_text()).get('textures', {}).values())
check('item: item_sword textures are rig sprites also used by the rig\'s own models (0 extra px)', set(IS['textures'].values()) <= rig_tex & other_tex,
      str(set(IS['textures'].values()) - (rig_tex & other_tex)))
D_ = IS.get('display', {})
need_d = ['thirdperson_righthand', 'thirdperson_lefthand', 'firstperson_righthand', 'firstperson_lefthand', 'gui', 'ground', 'fixed']
check('item: gui / hand / ground / fixed transforms', all(k in D_ for k in need_d), str([k for k in need_d if k not in D_]))


def rotp(P, r):
    """vanilla item display rotation: X then Y then Z (degrees) about the model centre."""
    x, y, z = P
    a, b, c = (math.radians(v) for v in r)
    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
    x, z = x * math.cos(b) + z * math.sin(b), -x * math.sin(b) + z * math.cos(b)
    x, y = x * math.cos(c) - y * math.sin(c), x * math.sin(c) + y * math.cos(c)
    return x, y, z


def el_pts(e):
    out = []
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
                out.append(P)
    return out


grip_c = [sum(c) / len(c) for c in zip(*[P for e in IS['elements'] if any(f['texture'] == '#grip' for f in e['faces'].values()) for P in el_pts(e)])]
scab_c = [sum(c) / len(c) for c in zip(*[P for e in IS['elements'] if any(f['texture'] == '#scab' for f in e['faces'].values()) for P in el_pts(e)])]
check('item: in the gui it points like a vanilla sword (the hilt lower left, the scabbard tip upper right)',
      grip_c[0] < scab_c[0] and grip_c[1] < scab_c[1], f'grip {grip_c[:2]} scab {scab_c[:2]}')
gd = D_.get('ground', {})
pts = [rotp([P[i] - 8 for i in range(3)], gd.get('rotation', [0, 0, 0])) for e in IS['elements'] for P in el_pts(e)]
sy = gd.get('scale', [1, 1, 1])[1]
low = min(p[1] * sy + gd.get('translation', [0, 0, 0])[1] for p in pts) / 16 + .25 * sy
check(f'item: on the ground it lies flat (rotation x 90) above the floor (lowest {low:.3f} b over the bob)', abs(abs(gd.get('rotation', [0])[0]) - 90) < 1e-6 and low >= 0)
fx = D_.get('fixed', {})
check('item: the fixed (frame) transform turns it to face the frame and fits (scale <= 1)', max(fx.get('scale', [9])) <= 1)

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


def hull(m):
    """Corner points (blocks about the pivot, after the client's Ry180, before the display transform) of rig model m."""
    if m not in HULL:
        mm = item_model(f'rlk:mboss/scarlet/{m}')
        HULL[m] = sorted({(-(P[0] / 16 - .5), P[1] / 16 - .5, -(P[2] / 16 - .5)) for e in mm.get('elements', []) for P in el_pts(e)})
    return HULL[m]


NUM = re.compile(r'-?[\d.]+(?:e-?\d+)?')


def parse_tf(s):
    g = lambda k: [float(x) for x in NUM.findall(re.search(k + r':\[([^\]]*)\]', s).group(1))]
    return {'t': g('translation'), 'q': g('left_rotation'), 's': g('scale')}


UUID2PART = {p['uuid']: p['name'] for p in MAN['parts']}
PART = {p['name']: p for p in MAN['parts']}
KEY = re.compile(r'data merge entity (\S+) \{start_interpolation:0,interpolation_duration:(\d+),transformation:(.*)\}$')
SWAP = re.compile(r'function ' + re.escape(NS) + r'/m/(forearm_l|forearm_r|face)/(\w+)$')
HAT_IDX = re.compile(r'scoreboard players set @s hrRigHat (\d)$')


def shown_at(tgt, n, t):
    frm, to, t0, d = tgt[n]
    if d == 0 or t >= t0 + d or frm is None:
        return to
    u = (t - t0) / d
    return {'t': [a + (b - a) * u for a, b in zip(frm['t'], to['t'])], 'q': slerp(frm['q'], to['q'], u), 's': [a + (b - a) * u for a, b in zip(frm['s'], to['s'])]}


def replay(clip):
    """Per tick: ({part: (shown transform, snapped this tick)}, {hand / face models}, hat state index) from the key files."""
    cd = RIG / 'c' / clip / 'k'
    L = MAN['clips'][clip]['len']
    tgt, out, mdl, hat = {}, [], {'forearm_l': PART['forearm_l']['model'], 'forearm_r': PART['forearm_r']['model'], 'face': PART['face']['model']}, None
    for t in range(L + 1):
        f = cd / f'{t}.mcfunction'
        if f.exists():
            for line in f.read_text().splitlines():
                m = KEY.match(line)
                if m and m.group(1) in UUID2PART:
                    n = UUID2PART[m.group(1)]
                    tgt[n] = (shown_at(tgt, n, t) if n in tgt else None, parse_tf(m.group(3)), t, int(m.group(2)))
                    continue
                m = SWAP.match(line)
                if m:
                    mdl[m.group(1)] = MAN['look_models']['hands'][m.group(1)][m.group(2)] if m.group(1) != 'face' else MAN['look_models']['face'][m.group(2)]
                m = HAT_IDX.match(line)
                if m:
                    hat = int(m.group(1))
        out.append(({n: (shown_at(tgt, n, t), tgt[n][3] == 0 and tgt[n][2] == t) for n in api.PARTS if n in tgt}, dict(mdl), hat))
    return out


def model_of(n, mdl):
    if n in mdl:
        return mdl[n]
    if n == 'sword_glow':
        return 'glow_lilac'
    return PART[n]['model']


def world(v, P):
    wv = qrot(v['q'], [P[i] * v['s'][i] for i in range(3)])
    return [v['t'][i] + wv[i] for i in range(3)]


GROUPS = {'blade': ['sword', 'sword_glow'], 'scabbard': ['scabbard', 'hilt_sheathed'], 'brim': ['hat'], 'hair': ['hair_tail_1', 'hair_tail_2', 'lock_r', 'lock_l'],
          'skirt': ['skirt_fl', 'skirt_fr', 'skirt_bl', 'skirt_br', 'sash_tails']}
floor_bad, step_bad, cull_bad, held_bad, low_by = [], [], [], [], {g: 9.0 for g in GROUPS}
idle_tip, REPLAY = {}, {}
W2, HH = MAN['culling']['width'] / 2, MAN['culling']['height']
for clip in MAN['clips']:
    frames = REPLAY[clip] = replay(clip)
    prev = {}
    for t, (fr, mdl, _) in enumerate(frames):
        wp = {}
        for n, (v, snap) in fr.items():
            if v is None or max(abs(x) for x in v['s']) < 1e-4:
                prev.pop(n, None)
                continue
            P = [world(v, Q) for Q in hull(model_of(n, mdl))]
            if not P:                   # a model with no element (the calm face overlay, empty)
                continue
            wp[n] = P
            ys = [p[1] for p in P]
            if min(ys) < -.012:
                floor_bad.append(f'{clip} t{t} {n} {min(ys):.3f}')
            for g, L in GROUPS.items():
                if n in L:
                    low_by[g] = min(low_by[g], min(ys))
            if any(math.hypot(p[0], p[2]) > W2 + .01 or p[1] > HH + .01 for p in P):
                cull_bad.append(f'{clip} t{t} {n}')
            if n in prev and not snap and qangle(prev[n], v['q']) > 120.5:
                step_bad.append(f'{clip} {n} t{t - 1}->{t} {qangle(prev[n], v["q"]):.0f}')
            prev[n] = v['q']
        # held props: the blade runs away from her left forearm, the hand-held scabbard away from her right forearm
        sw, fl = fr.get('sword', (None,))[0], fr.get('forearm_l', (None,))[0]
        if sw and fl and max(sw['s']) > 1e-4:
            tip = world(sw, (0, 1.93 / 1.5, 0))     # the blade axis is the model's +Y (scale 1.5: 1.93 b)
            d_tip, d_grip = math.dist(tip, fl['t']), math.dist(sw['t'], fl['t'])
            if d_tip < d_grip + .62 * 1.93 * sw['s'][1] / 1.5:     # a wrist bent back past ~130 deg (vis scales both)
                held_bad.append(f'{clip} t{t} blade {d_grip:.2f}->{d_tip:.2f}')
            if clip in ('idle', 'idle2', 'walk'):
                idle_tip[clip] = min(idle_tip.get(clip, 9), tip[1])
        sc, fr_ = fr.get('scabbard', (None,))[0], fr.get('forearm_r', (None,))[0]
        if sc and fr_ and max(sc['s']) > 1e-4 and math.dist(sc['t'], world(fr_, (0, -.4, 0))) < .35:
            stip = world(sc, (0, 1.82 / 1.5, 0))
            if math.dist(stip, fr_['t']) < math.dist(sc['t'], fr_['t']) + .55 * 1.82 * sc['s'][1] / 1.5:
                held_bad.append(f'{clip} t{t} scabbard')
check('shipped: no shown model point below the floor at any tick (all 47 clips; every part from the RP hulls)', not floor_bad,
      '; '.join(floor_bad[:6]) + f' ({len(floor_bad)})')
check('shipped: the lowest points of the named groups over every tick stay over the floor (' + ', '.join(f'{g} {v:.3f}' for g, v in low_by.items()) + ')',
      all(v >= -.012 for v in low_by.values()))
check('shipped: no part turns more than 120 degrees in a tick (0-tick snaps excepted)', not step_bad, '; '.join(step_bad[:6]) + f' ({len(step_bad)})')
check('shipped: every point inside the culling box (8 x 8)', not cull_bad, '; '.join(cull_bad[:6]) + f' ({len(cull_bad)})')
check('shipped: held props right (the blade runs away from her sword arm, the hand-held scabbard away from her right arm)', not held_bad, '; '.join(held_bad[:6]) + f' ({len(held_bad)})')
check('shipped: the blade tip >= 0.10 b over the floor in idle / idle2 / walk (' + ', '.join(f'{k} {v:.2f}' for k, v in idle_tip.items()) + ')',
      len(idle_tip) == 3 and all(v >= .10 - .005 for v in idle_tip.values()))
if SK:
    # no blade sample (guard -> tip) inside the base box of her torso / pelvis / head / upper arms / thighs / shins at a clip event
    BODYP = ['torso', 'pelvis', 'head', 'arm_l', 'arm_r', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r']

    def base_box(m):
        e = item_model(f'rlk:mboss/scarlet/{m}')['elements'][0]
        xs = sorted((-(e['from'][0] / 16 - .5), -(e['to'][0] / 16 - .5)))
        zs = sorted((-(e['from'][2] / 16 - .5), -(e['to'][2] / 16 - .5)))
        return [xs[0], e['from'][1] / 16 - .5, zs[0]], [xs[1], e['to'][1] / 16 - .5, zs[1]]
    BOX = {n: base_box(PART[n]['model']) for n in BODYP}
    thru, n_ev = [], 0
    for clip in MAN['clips']:
        for ev, te in MAN['clips'][clip]['events'].items():
            if te == 0:
                continue                # tick 0 blends from the previous clip's pose (the builder checks it as authored)
            fr = REPLAY[clip][te][0]
            sw = fr.get('sword', (None,))[0]
            if not sw or max(sw['s']) < 1e-4:
                continue
            n_ev += 1
            samples = [world(sw, (0, (.185 + (1.93 - .185) * k / 40) / 1.5, 0)) for k in range(41)]
            for n in BODYP:
                v = fr[n][0]
                if max(v['s']) < 1e-4:
                    continue
                lo, hi = BOX[n]
                iq = [-v['q'][0], -v['q'][1], -v['q'][2], v['q'][3]]
                deep = 0
                for P in samples:
                    L = qrot(iq, [P[i] - v['t'][i] for i in range(3)])
                    L = [L[i] / v['s'][i] for i in range(3)]
                    deep = max(deep, min(min(L[i] - lo[i], hi[i] - L[i]) for i in range(3)))
                if deep > .01:
                    thru.append(f'{clip} {ev}@{te} {n} {deep:.3f} b')
    check(f'skin: no blade through her body at the clip events (torso / pelvis / head / upper arms / thighs / shins, 1 cm in; '
          f'{n_ev} events with the blade out after tick 0)', not thru, '; '.join(thru[:6]) + f' ({len(thru)})')
ev_key = [c for c in api.CLIPS if any(not (RIG / f'c/{c}/k/{t}.mcfunction').exists() for t in [0])]
check('shipped: every clip keys its tick 0', not ev_key, str(ev_key))

# ================================================================ hats
HATS = list(api.LOOKS['hat'])
used_states = set()
for clip, frames in REPLAY.items():
    for _, _, h in frames:
        if h is not None:
            used_states.add(h)
check('hats: the clips key only contract hat states', used_states <= set(range(len(HATS))), str(used_states))
dn = REPLAY['down']
check('hats: down keeps the hat on the floor beside her (world) at every tick',
      all(fr['hat'][0]['t'][1] < .06 and h == HATS.index('world') for fr, _, h in dn), str([round(fr['hat'][0]['t'][1], 3) for fr, _, _ in dn][:5]))
kp = REPLAY['kipup']
seq_h = [h for _, _, h in kp]
ev = api.CLIPS['kipup'][2]
check('hats: kipup goes world -> hand (crouch) -> worn', seq_h[0] == HATS.index('world') and seq_h[ev['crouch']] == HATS.index('hand') and seq_h[-1] == HATS.index('worn'), str(seq_h))


# ================================================================ cine (S2b: the 8 cinematic clips of tools/scarlet_cine.mjs)
CINE = list(api.CINE_CLIPS)
STATE_RX = re.compile(r'scoreboard players set @s hrRig(Hat|Sw|Sc|Cu|Bo) (\d)$')
FACE_RX = re.compile(r'function ' + re.escape(NS) + r'/m/face/(\w+)$')
SVALS = {'Hat': list(api.LOOKS['hat']), 'Sw': list(api.LOOKS['sword']), 'Sc': list(api.LOOKS['scabbard']), 'Cu': list(api.PROP_STATES),
         'Bo': list(api.PROP_STATES)}


def states(clip):
    """Per tick the discrete states the shipped key files set: {Hat, Sw, Sc, Cu, Bo, face} (names)."""
    cur, out = {}, []
    for t in range(MAN['clips'][clip]['len'] + 1):
        f = RIG / 'c' / clip / 'k' / f'{t}.mcfunction'
        if f.exists():
            for line in f.read_text().splitlines():
                m = STATE_RX.match(line)
                if m:
                    cur[m.group(1)] = SVALS[m.group(1)][int(m.group(2))]
                m = FACE_RX.match(line)
                if m:
                    cur['face'] = m.group(1)
        out.append(dict(cur))
    return out


cs_ok = MAN.get('cine_source') == 'tools/scarlet_cine.mjs' and all(MAN['clips'][c]['authored'] for c in CINE)
check('cine: the 8 cinematic clips come from tools/scarlet_cine.mjs, authored (not the placeholder)', cs_ok, MAN.get('cine_source'))
src_bad = [c for c in CINE if not MAN['clips'][c]['source']]
check('cine: every cinematic clip names its footage / plan source', not src_bad, src_bad)
thin = {c: MAN['clips'][c]['key_files'] for c in CINE if MAN['clips'][c]['key_files'] < 12}
check('cine: every cinematic clip is animated (>= 12 key files each)', not thin, thin)
ST_ = {c: states(c) for c in CINE + ['ev_give', 'ev_toast', 'g_deflect', 'down', 'g_tell']}
E_ = lambda c, e: api.ev(c, e)
# the hat / sword / scabbard / prop / face states at the contract events (PLAN §3.1-§3.7)
WANT = [
    ('intro', 0, {'Hat': 'worn', 'Sw': 'sheathed', 'Sc': 'hip', 'Cu': 'hand', 'Bo': 'none'}),
    ('intro', E_('intro', 'pour') - 6, {'Bo': 'hand'}), ('intro', E_('intro', 'pour') + 22, {'Bo': 'none'}),
    ('intro', E_('intro', 'cup_down'), {'Cu': 'none'}), ('intro', E_('intro', 'scab_hand'), {'Sc': 'hand', 'Sw': 'sheathed'}),
    ('intro', 554, {'Hat': 'worn', 'Sc': 'hand', 'Cu': 'none', 'Bo': 'none'}),
    ('intro_end', 0, {'Hat': 'worn', 'Sw': 'sheathed', 'Sc': 'hand', 'Cu': 'none', 'Bo': 'none'}),
    ('intro_end', E_('intro_end', 'smile'), {'face': 'smile'}), ('intro_end', E_('intro_end', 'head_down'), {'face': 'calm'}),
    ('intro_end', E_('intro_end', 'draw') - 1, {'Sw': 'sheathed'}), ('intro_end', E_('intro_end', 'draw'), {'Sw': 'hand'}),
    ('intro_end', E_('intro_end', 'tuck') - 1, {'Sc': 'hand'}), ('intro_end', E_('intro_end', 'tuck'), {'Sc': 'hip'}),
    ('intro_end', 86, {'Hat': 'worn', 'Sw': 'hand', 'Sc': 'hip'}),
    ('cs1', 0, {'Hat': 'worn', 'Sw': 'hand', 'Sc': 'hip'}), ('cs1', E_('cs1', 'hat_back') - 1, {'Hat': 'worn'}),
    ('cs1', E_('cs1', 'hat_back'), {'Hat': 'back'}), ('cs1', E_('cs1', 'sheathe'), {'Hat': 'worn', 'Sw': 'sheathed'}),
    ('cs1', E_('cs1', 'slash'), {'Sw': 'hand'}), ('cs1', E_('cs1', 'hat_back2') - 1, {'Hat': 'worn'}),
    ('cs1', E_('cs1', 'hat_back2'), {'Hat': 'back'}), ('cs1', 213, {'Hat': 'back', 'Sw': 'hand'}),
    ('sq1', 0, {'Hat': 'back'}), ('sq1', E_('sq1', 'hat_hand'), {'Hat': 'hand'}), ('sq1', E_('sq1', 'hat_on') - 1, {'Hat': 'hand'}),
    ('sq1', E_('sq1', 'hat_on'), {'Hat': 'worn'}), ('sq1', 60, {'Hat': 'worn', 'Sw': 'hand', 'Sc': 'hip'}),
    ('repel', 0, {'Hat': 'worn'}), ('repel', E_('repel', 'hat_back'), {'Hat': 'back'}), ('repel', E_('repel', 'hat_off') - 1, {'Hat': 'back'}),
    ('repel', E_('repel', 'hat_off'), {'Hat': 'world'}), ('repel', 104, {'Hat': 'world', 'Sw': 'hand', 'Sc': 'hip'}),
    ('lead_down', 0, {'Hat': 'world'}), ('lead_down', E_('lead_down', 'hat_hand'), {'Hat': 'hand'}),
    ('lead_down', E_('lead_down', 'hat_on') - 1, {'Hat': 'hand'}), ('lead_down', E_('lead_down', 'hat_on'), {'Hat': 'worn'}),
    ('lead_down', 82, {'Hat': 'worn', 'Sw': 'hand', 'Sc': 'hip'}),
    ('lead_stand', 0, {'Hat': 'worn'}), ('lead_stand', E_('lead_stand', 'hat_hand'), {'Hat': 'hand'}),
    ('lead_stand', E_('lead_stand', 'hat_on') - 1, {'Hat': 'hand'}), ('lead_stand', E_('lead_stand', 'hat_on'), {'Hat': 'worn'}),
    ('lead_stand', 70, {'Hat': 'worn', 'Sw': 'hand', 'Sc': 'hip'}),
    ('ending', 0, {'Hat': 'world'}), ('ending', E_('ending', 'hat_on') - 1, {'Hat': 'hand'}), ('ending', E_('ending', 'hat_on'), {'Hat': 'worn'}),
    ('ending', E_('ending', 'scab_up'), {'Sc': 'hand'}), ('ending', E_('ending', 'seated') - 1, {'Sw': 'hand'}),
    ('ending', E_('ending', 'seated'), {'Sw': 'sheathed'}), ('ending', E_('ending', 'smile') + 2, {'face': 'smile'}),
    ('ending', E_('ending', 'l23'), {'face': 'closed'}), ('ending', E_('ending', 'eyes'), {'face': 'calm'}),
    ('ending', 1042, {'Hat': 'worn', 'Sw': 'sheathed', 'Sc': 'hand', 'face': 'calm'}),
]
st_bad = [(c, t, {k: ST_[c][t].get(k) for k in w}, w) for c, t, w in WANT if any(ST_[c][t].get(k) != v for k, v in w.items())]
check(f'cine: the hat / sword / scabbard / cup / bottle / face states at their events ({len(WANT)} points, PLAN §3.1-§3.7)', not st_bad, st_bad[:4])
# hand-overs: the anchor table (the solver's per-tick points) of the clip that hands over == the next clip's tick 0
AN = {}
for line in allfn['an/load'].splitlines():
    m = re.match(r'data modify storage rlk:hr rig\.an\[(\d+)\]\.(\w+) set value (\[.*\])$', line)
    if m:
        AN[(int(m.group(1)), m.group(2))] = [[float(v.lstrip('^') or 0) for v in s_.split()] for s_ in json.loads(m.group(3))]
cid = lambda c: MAN['clips'][c]['id']


def anchors_at(c, t):
    return {a: AN[(cid(c), a)][t] for a in api.ANCHORS}


TOL = {'head': .06, 'chest': .06, 'hat_crown': .12, 'hand_l': .12, 'hand_r': .12, 'scabbard_mouth': .14, 'blade_mid': .2, 'blade_tip': .25}
HANDOVER = [('intro', 554, 'intro_end', 0), ('cs1', 213, 'sq1', 0), ('g_deflect', 12, 'repel', 0), ('repel', 104, 'down', 0),
            ('down', 0, 'lead_down', 0), ('sq1', 60, 'g_tell', 0), ('lead_down', 82, 'g_tell', 0), ('lead_stand', 70, 'g_tell', 0),
            ('ending', 1042, 'ev_give', 0), ('ending', 1042, 'ev_toast', 0)]
ho_bad = []
for a, ta, b, tb in HANDOVER:
    A_, B_ = anchors_at(a, ta), anchors_at(b, tb)
    d = {k: round(math.dist(A_[k], B_[k]), 3) for k in api.ANCHORS}
    over_ = {k: v for k, v in d.items() if v > TOL[k]}
    if over_:
        ho_bad.append((f'{a}[{ta}] -> {b}[{tb}]', over_))
check(f'cine: the hand-over poses meet (anchors within 0.06-0.25 b: {", ".join(f"{a}->{b}" for a, _, b, _ in HANDOVER)})', not ho_bad, ho_bad)
# the ending ends in H_POSE's states (= ev_give / ev_toast tick 0) and the sq1 / lead-in ends in g_brim's hold (the right hand at the brim)
h_bad = [k for k in ('Hat', 'Sw', 'Sc', 'face') if ST_['ending'][1042].get(k) != ST_['ev_give'][0].get(k)]
check('cine: ending 1042 = ev_give / ev_toast 0 states (hat worn, sword sheathed, scabbard in hand, face calm)', not h_bad, h_bad)
# big swings keyed every tick (the spins, the draws, the slash, the flips, the throw, the cuts, the scabbard swings)
SWING = {'intro_end': [(44, 62)], 'cs1': [(6, 9), (162, 169)], 'repel': [(29, 43), (59, 75)],
         'ending': [(19, 26), (140, 146), (172, 174), (202, 204), (214, 216), (226, 228), (297, 304), (802, 810)]}
sw_bad = [(c, t) for c, spans in SWING.items() for a, b in spans for t in range(a, b + 1) if not (RIG / 'c' / c / 'k' / f'{t}.mcfunction').exists()]
check(f'cine: big swings keyed every tick ({sum(b - a + 1 for v in SWING.values() for a, b in v)} ticks in {sum(len(v) for v in SWING.values())} spans)', not sw_bad, str(sw_bad[:6]))
# per-clip numbers of the shipped replay (the gates above cover every clip; these are the cinematic clips' own)
cine_low, cine_turn = {}, {}
for c in CINE:
    frames, prev, lo, mt = REPLAY[c], {}, 9.0, 0.0
    for t, (fr, mdl, _) in enumerate(frames):
        for n, (v, snap) in fr.items():
            if v is None or max(abs(x) for x in v['s']) < 1e-4:
                prev.pop(n, None)
                continue
            lo = min(lo, min((world(v, Q)[1] for Q in hull(model_of(n, mdl))), default=9.0))
            if n in prev and not snap:
                mt = max(mt, qangle(prev[n], v['q']))
            prev[n] = v['q']
    cine_low[c], cine_turn[c] = round(lo, 3), round(mt, 1)
check('cine: shipped lowest points >= -0.012 b (' + ', '.join(f'{c} {v}' for c, v in cine_low.items()) + ')', all(v >= -.012 for v in cine_low.values()))
check('cine: shipped largest per-tick turns <= 120 deg (' + ', '.join(f'{c} {v}' for c, v in cine_turn.items()) + ')', all(v <= 120.5 for v in cine_turn.values()))
# seq.py (S2b) builds with a dummy Writer and writes only seq/** (PLAN §9.3)
try:
    import importlib
    from mboss_scarlet import seq as _seq
    _seq = importlib.reload(_seq)

    class _DW:
        def __init__(self):
            self.rels = []

        def w(self, rel, body):
            self.rels.append(rel)
    _w = _DW()
    for _s in _seq.SERVICES:
        _s.build(_w)
    check(f'seq: seq.py builds with a dummy Writer and writes only seq/** ({len(_w.rels)} files)', _w.rels and all(r.startswith('seq/') for r in _w.rels)
          and [s_.name for s_ in _seq.SERVICES] == list(api.SEQS))
except Exception as e:  # noqa: BLE001
    check('seq: seq.py builds', False, repr(e))


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
            for e in (self.select(t[3], ctx) if t[3] != '@s' else [ctx.ex]):
                o = e.data
                for p in path[:-1]:
                    o = o.setdefault(p, {})
                o[path[-1]] = val
            return 1
        if c == 'scoreboard' and t[1] == 'objectives':
            if t[2] == 'remove':
                self.scores = {k: v for k, v in self.scores.items() if k[1] != t[3]}
            return 1
        if c in ('particle', 'playsound', 'rotate'):
            return 1
        return super().cmd(t, ctx)


def parts(sim):
    return {next(t[len('rlk_hr_'):] for t in e.tags if t.startswith('rlk_hr_') and t != 'rlk_hr_part'): e
            for e in sim.ents if e.alive and 'rlk_hr_part' in e.tags}


def model(e):
    return e.data['item']['components']['minecraft:item_model']


try:
    sim = Sim(DP / 'data/rlk/function')
    anchor = mcsim.Ent('husk', [760.5, 201.0, 8.5], (180.0, 0.0), ['rlk_hr_body'])
    sim.ents.append(anchor)
    call = lambda f, m=None: sim.call(f'{NS}/{f}', mcsim.Ctx(anchor, tuple(anchor.pos), tuple(anchor.rot)), m)
    sc = lambda o: sim.sc(('e', anchor.id), o)
    call('spawn')
    P = parts(sim)
    check(f'runtime: spawn = 29 parts + the shadow ({len(P)})', len(P) == 30 and set(P) == set(api.PARTS) | {'shadow'})
    check('runtime: UUIDs as the manifest', all(P[p['name']].data.get('_uuid') == p['uuid'] for p in MAN['parts']))
    check('runtime: the parts stand on the anchor (follow)', all(math.dist(e.pos, anchor.pos) < 1e-6 for e in P.values()))
    an = sim.storage.get('rlk:hr', {}).get('rig', {}).get('an', [])
    check(f'runtime: the anchor table is loaded (rlk:hr rig.an, one entry per clip: {len(an)})', len(an) == len(api.CLIPS)
          and all(len(an[MAN['clips'][c]['id']]['hand_l']) == api.CLIPS[c][0] + 2 for c in api.CLIPS))
    for _ in range(5):
        call('tick')
    check('runtime: tick advances hrRigT (idle queued at spawn)', sc('hrRigT') == 4, str(sc('hrRigT')))
    bad = []
    for clip in api.CLIPS:
        call(f'play/{clip}')
        if sc('hrRigC') != MAN['clips'][clip]['id'] or sc('hrRigT') != -1:
            bad.append(clip)
        for _ in range(api.CLIPS[clip][0] + 2):
            call('tick')
        if sc('hrRigT') != api.CLIPS[clip][0] + 1 and not api.CLIPS[clip][1]:
            bad.append(clip + ' (end)')
    check('runtime: play/<clip> queues every clip (hrRigC = id, hrRigT -1) and every clip runs to its end', not bad, str(bad))
    call('start/idle')
    check('runtime: start/<clip> applies tick 0 now (hrRigT 0)', sc('hrRigT') == 0 and sc('hrRigC') == MAN['clips']['idle']['id'])
    snap = lambda: json.dumps({n: e.data for n, e in sorted(parts(sim).items())}, sort_keys=True) + json.dumps({o: sc(o) for o in sorted(objs)})
    idem = []
    for ch, vals in api.LOOKS.items():
        for v in vals:
            call(f'look/{ch}/{v}')
            a = snap()
            call(f'look/{ch}/{v}')
            if snap() != a:
                idem.append(f'{ch}/{v}')
    check('runtime: look/* idempotent', not idem, str(idem))
    call('look/form/ghost')
    P = parts(sim)
    twin = lambda m: m if m == 'empty' or m.startswith('glow_') else m + '_g'
    check('runtime: look/form/ghost swaps every shown part to its ghost twin', all(model(P[n]) == f'rlk:mboss/scarlet/{twin(PART[n]["model"])}' for n in ('torso', 'head', 'skirt_fl', 'sword', 'scabbard', 'thigh_l', 'hair_tail_1')),
          str([model(P[n]) for n in ('torso', 'head')]))
    call('look/form/normal')
    call('look/phase/p2')
    check('runtime: look/phase/p2 shows the P2 hat and sash', model(parts(sim)['hat']) == 'rlk:mboss/scarlet/hat_p2' and model(parts(sim)['sash_tails']) == 'rlk:mboss/scarlet/sash_p2')
    call('look/phase/p1')
    blades = []
    for v in api.LOOKS['blade']:
        call(f'look/blade/{v}')
        blades.append(model(parts(sim)['sword_glow']))
    check('runtime: look/blade/<v> swaps the glow card (off = empty)', blades == [f'rlk:mboss/scarlet/{MAN["look_models"]["blade"][v]}' for v in api.LOOKS['blade']], str(blades))
    call('look/blade/off')
    # the hat states
    hat_ok = []
    rest = {n: PART[n]['rest'] for n in ('head', 'torso', 'forearm_r')}
    for i, v in enumerate(HATS):
        call(f'look/hat/{v}')
        h = parts(sim)['hat'].data['transformation']
        tt, ss = h['translation'], h['scale']
        hd, to = rest['head']['t'], rest['torso']['t']
        ok = sc('hrRigHat') == i and {
            'worn': ss[0] > .5 and tt[1] > hd[1] + .25 and math.hypot(tt[0] - hd[0], tt[2] - hd[2]) < .3,
            'back': ss[0] > .5 and to[1] < tt[1] < hd[1] + .3 and tt[2] < to[2] - .1,
            'hand': ss[0] > .5 and math.dist(tt, rest['forearm_r']['t']) < 1.3 and tt[1] < hd[1],
            'world': ss[0] > .5 and tt[1] < .06,
            'gone': ss[0] < 1e-4}[v]
        hat_ok.append((v, ok))
    check('runtime: look/hat/<state> stores hrRigHat and places the hat (worn over the head, back behind the torso, hand beside '
          'the right hand, world on the floor, gone scale 0)', all(o for _, o in hat_ok), str(hat_ok))
    call('look/hat/worn')
    call('play/a1')
    for _ in range(api.CLIPS['a1'][2]['hit'] + 1):
        call('tick')
    moved = []
    for a in api.ANCHORS:
        call(f'anchor/{a}')
        mk = [e for e in sim.ents if e.alive and 'rlk_hr_anchor' in e.tags]
        moved.append((a, len(mk), tuple(round(x, 2) for x in mk[0].pos) if mk else None))
    check('runtime: anchor/<name> moves the one rlk_hr_anchor marker (8 distinct points within 4 b)',
          all(n == 1 for _, n, _ in moved) and len({p for _, _, p in moved}) == 8 and all(math.dist(p, anchor.pos) < 4 for _, _, p in moved), str(moved))
    call('state/hidden')
    check('runtime: state/hidden scales every part to 0', all(e.data.get('transformation', {}).get('scale') == [0.0, 0.0, 0.0] for n, e in parts(sim).items() if n != 'shadow'))
    call('state/normal')
    call('play/idle')
    call('tick')
    check('runtime: a clip shows a hidden rig again at its tick 0', sc('hrRigS') == 0 and max(parts(sim)['torso'].data['transformation']['scale']) > .5)
    call('kill')
    check('runtime: rig/kill leaves no part and no anchor marker', not parts(sim) and not [e for e in sim.ents if e.alive and 'rlk_hr_anchor' in e.tags])
    call('spawn')
    call('anchor/chest')
    call('uninstall')
    check('runtime: rig/uninstall leaves no part, no marker, no face marker, no rig objective, no rig storage',
          not parts(sim) and not [e for e in sim.ents if e.alive and ({'rlk_hr_anchor', 'rlk_hr_face'} & set(e.tags))]
          and 'rig' not in sim.storage.get('rlk:hr', {}) and not [k for k in sim.scores if k[1].startswith('hrRig')])
except Exception as e:  # noqa: BLE001
    import traceback
    traceback.print_exc()
    check('runtime: mcsim run', False, repr(e))


# ================================================================ palette (PLAN §1.5)
def lab(hx):
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = lambda c: c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    x, y, z = (.4124 * r + .3576 * g + .1805 * b) / .95047, .2126 * r + .7152 * g + .0722 * b, (.0193 * r + .1192 * g + .9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > .008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


dE = lambda a, b: math.dist(lab(a), lab(b))
ORIG = {'hat_top': '#E6DCCF', 'bodysuit': '#E4E2E8', 'thigh_highs': '#CFCBD3', 'tasset': '#8E6CB4', 'gold_strip': '#CDB78C', 'hair': '#DDD7E2'}
roles = MAN['paint_roles']
rows = []
for k, o in ORIG.items():
    cs = roles.get(k)
    if cs == 'skin':
        continue                    # S2c: the body roles are the user's own skin (its pixels as they are, the user's choice)
    cs = cs if isinstance(cs, list) else [cs]
    rows.append((k, min(dE(c, o) for c in cs) if cs and cs[0] else 0))
skin_roles = [k for k in ORIG if roles.get(k) == 'skin']
check('palette: the declared base paints of the rig\'s own roles keep dE >= 10 from the original (' + ', '.join(f'{k} {v:.1f}' for k, v in rows) + ')'
      + (f'; the user\'s skin: {", ".join(skin_roles)}' if skin_roles else ''), rows and all(v >= 10 for _, v in rows))
SPR = {'hat_top': ['brim', 'crown'], 'bodysuit': ['robe', 'torso_front'], 'thigh_highs': ['trouser'], 'tasset': ['vest', 'crimson'], 'gold_strip': ['brass'], 'hair': ['hair']}
meas = []
for k, sprs in SPR.items():
    if roles.get(k) == 'skin':
        continue
    for n in sprs:
        im = Image.open(ASSETS / f'textures/mboss/scarlet/{n}.png').convert('RGBA')
        pxs = [im.getpixel((x, y)) for y in range(im.size[1]) for x in range(im.size[0]) if im.getpixel((x, y))[3] > 128]
        avg = '#' + ''.join(f'{round(sum(p[i] for p in pxs) / len(pxs)):02x}' for i in range(3))
        meas.append((k, n, avg, dE(avg, ORIG[k])))
check('palette: the sprites\' mean colours keep dE >= 10 from the original role colours (' + ', '.join(f'{n} {v:.0f}' for _, n, _, v in meas) + ')',
      all(v >= 10 for *_, v in meas), str([m for m in meas if m[3] < 10]))
names = [p['name'] for p in MAN['parts']] + list(MAN['sprites']) + [p.stem for p in (ASSETS / 'models/item/mboss/scarlet').glob('*.json')]
check('originality: neutral part / model / sprite names (role names and scarlet only; checked against no franchise words)',
      all(re.fullmatch(r'[a-z0-9_]+', n) for n in names))

print(f'\n{len(OK)} passed, {len(FAIL)} failed')
sys.exit(1 if FAIL else 0)
