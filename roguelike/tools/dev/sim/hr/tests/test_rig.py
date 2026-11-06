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
             like a vanilla sword in the gui (hilt lower left, tip upper right), lies flat on the ground above the floor; F-I
             (HR-03): the guard card on the guard plate; the item definition selects on display_context (gui / fixed / ground
             -> the slot icon item_sword_icon, the hands / item_display none -> the rig model); the icon: rig sprites only, the
             manifest's transforms, lit front; at GUI x 2 every lit row but the two end corners >= 2 px, >= 100 px, one piece
             (the rig model's hairline printed for comparison); inside the 16 x 16 slot and spanning it; long parts >= 2 GUI
             px wide; points like a vanilla sword; dropped: upright, half size, over the floor
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
  S2d        (the player avatar's body; only when the manifest carries `skeleton` / `dims` / `support` / `retarget`, else
             "skipped (manifest without ...)"; the dims above then come from the manifest)
  body       the 15 body models (head, torso, pelvis, upper arms, forearms with every hand, thighs, shins) equal the player
             avatar's two elements exactly (from / to and the six face UVs): head / legs / slim arms = the RP's
             player_motion/skirk models, torso / pelvis = skirk's body rows 0..9 / 9..12 (a test-local spec table when an RP
             file is absent); the arm boxes' width == the skin's arm layout (slim: the last two columns of every arm region
             transparent -> 3-px arms); every body part at display scale 1
  skeleton   the manifest skeleton == design §1.1; the rest chain (seam, neck, shoulders, elbows, hip joints, knees) within
             1e-3; the idle-t0 head top 2.00 +- 0.03
  contract   api HEIGHT / HAT_TOP / SWORD_LEN / SCABBARD_LEN / ITEM_SWORD_LEN / ITEM_SWORD_SCALE / BRIM_D == the built dims;
             the registry pair == api.BOSS (scale 1.0); hit h - the idle hull top in [0.05, 0.12]
  contacts   on the shipped replay per the manifest `support` spans: planted feet, lying (gaps <= 0.06), seat (the thighs on
             the stone, nothing in it), kneel, touch; the stone items, the floor hat, the brim holds, hilt / throat, lips,
             two hands (reported, fail > 0.12)
  float      air spans stay up (core lowest >= min(0.5 S_LEG lowRef, 0.05)); the last-resort lift <= 0.005 on contact ticks;
             ghost ticks exempt
  blade      every tick: no blade sample > 0.05 b inside head / torso / pelvis (the ticks > 0.01 counted)
  held       the held sword's pivot at the left grip; sheathe ticks on the scabbard axis; the hat in hand 0.62 from the right
             grip; the cup under the right fist; the bottle's neck in the left fist; hilt_sheathed == the scabbard pivot
  hats       worn on the head axis, back clear of head / torso, world clear of the body and the floor, no jump > 0.15 b at a
             non-cut switch; strings: idle t0 >= 0.005 outside the head's outer layer
  angles     node tools/scarlet_retarget.mjs --dump all: every angle channel == the source outside the declared patches
  retarget   every correction within its bound, IK stretch <= 1.0005, contact shortfalls per kind (the per-clip table printed)
  couplings  the cs1 petal path follows the built head anchor; seq.S0 / SWORD_R == api / manifest
  cine seam  (F-I, HR-31) CS3 at 5 % -> CS4 (repel 102 -> ending 0): the body's anchors meet (the head <= 0.25 b), the hat
             moves only under the ending's tick-0 hard cut (seq/ending/start: ovl white / black, in 0, hold >= 2)
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
# S2d: the player avatar's body (the new sections run only when the manifest carries these blocks)
DIMS, SKEL, SUPT, RET = (MAN.get(k) for k in ('dims', 'skeleton', 'support', 'retarget'))
if DIMS:
    SW_TIP, SW_LO, SW_DS = DIMS['sword']['tip'], DIMS['sword']['blade_lo'], DIMS['sword']['display_scale']
    SC_TIP, SC_DS = DIMS['scabbard']['L'], DIMS['scabbard']['display_scale']
    SC_HAND_P, SC_HAND_R = (0, -.30, 0), .30
else:                               # S2c's figure
    SW_TIP, SW_LO, SW_DS, SC_TIP, SC_DS, SC_HAND_P, SC_HAND_R = 1.93, .185, 1.5, 1.82, 1.5, (0, -.4, 0), .35

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
      and MAN['shadow']['uuid'] == api.RIG_UUID.format(api.SHADOW_NN) and MAN['shadow']['radius'] == api.SHADOW_R)
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
_sr = ('%g' % api.SHADOW_R).lstrip('0') if api.SHADOW_R < 1 else '%g' % api.SHADOW_R
check(f'spawn: the shadow helper (nn 0x40, radius {api.SHADOW_R}, not an rlk_mb_part)', sh and f'shadow_radius:{_sr}f' in sh and 'rlk_mb_part' not in sh_tags
      and 'rlk_hr_part' in sh_tags, sh[:160])
ids = [v[0] for v in by_nn.values()]
check('spawn: UUID high ints 524c4b4d-4852-4400-8000', all(i[:3] == [0x524c4b4d, 0x48524400, -0x80000000] for i in ids), str(ids[:1]))
spawn_models = set(re.findall(r'"minecraft:item_model":"([^"]+)"', sp))
check('spawn: every part spawns with its default model', all(f'rlk:mboss/scarlet/{p["model"]}' in spawn_models for p in MAN['parts']))


# ================================================================ models
def item_model(item_id, context=None):
    """the model an item definition shows (a display_context select: the case holding `context`, else its fallback)"""
    ns, path = item_id.split(':')
    it = json.loads((RP / f'assets/{ns}/items/{path}.json').read_text())['model']
    if it.get('type') == 'minecraft:select':
        it = next((c['model'] for c in it['cases'] if context in c['when']), it['fallback'])
    mid = it['model']
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
    sq = [e for e in m['elements'] if e['to'][0] - e['from'][0] > .6 * api.BRIM_D * 16 and e['to'][1] - e['from'][1] < .05]
    ys = sorted(e['from'][1] for e in sq)
    turns = sorted(round((e.get('rotation', {}).get('angle', 0)) % 90, 1) for e in sq)
    steps = [b - a for a, b in zip(ys, ys[1:])]
    if not (len(sq) == 4 and all(abs(s - .048) < 1e-3 for s in steps) and turns == [0, 22.5, 45, 67.5]
            and abs((sq[0]['to'][0] - sq[0]['from'][0]) / 16 - api.BRIM_D) < .01):
        brim_bad.append(f'{hm}: {len(sq)} squares, steps {steps}, turns {turns}')
check(f'models: the brim = four {api.BRIM_D:.2f} b squares (api.BRIM_D) 0.003 b apart (no coplanar faces) at four turns 0 / 22.5 / 45 / 67.5 mod 90',
      not brim_bad, '; '.join(brim_bad))
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
    HAIR = () if SKEL else ('hair_tail_1', 'hair_tail_2')     # S2d hides the hair slabs (the skin's own back hair shows)
    need_m = {'head', 'torso', 'pelvis', 'arm_l', 'arm_r', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r', *HAIR} | \
        {f'forearm_{s}_{k}' for s in 'lr' for k in ('open', 'grip', 'brim')}
    check('skin: the map covers the body (head, torso, pelvis, upper arms, forearms with every hand, thighs, shins' + (', the hair)' if HAIR else ')'),
          need_m == set(SK['map']))
    check('skin: the parts the skin shows by default wear their skin models (head, torso, pelvis, arms, legs' + (', hair)' if HAIR else ')'),
          all(PART[n]['model'] in SK['map'] for n in ('head', 'torso', 'pelvis', 'arm_l', 'arm_r', 'forearm_l', 'forearm_r', 'thigh_l', 'thigh_r',
                                                         'shin_l', 'shin_r', *HAIR)))
    gh_bad = []
    for m in SK['map']:
        g = item_model(f'rlk:mboss/scarlet/{m}_g')
        for e in g['elements']:
            for f in e['faces'].values():
                if sorted([round(f['uv'][0], 4), round(f['uv'][2], 4)]) != [0, round(16 / 3, 4)] or sorted([f['uv'][1], f['uv'][3]]) != [0, 16]:
                    gh_bad.append(m)
    check('skin: the ghost twins of the skin models show the whole ghost gradient on every face', not gh_bad, str(sorted(set(gh_bad))[:5]))
    hid = SK['hidden']
    check(f'skin: the hidden parts ({", ".join(hid)}) wear the empty model', hid and all(PART[n]['model'] == 'empty' for n in hid)
          and (not SKEL or {'hair_tail_1', 'hair_tail_2'} <= set(hid)))
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
_ax = [scab_c[i] - grip_c[i] for i in range(3)]
_ax = [a / math.sqrt(sum(x * x for x in _ax)) for a in _ax]
_pr = [sum(P[i] * _ax[i] for i in range(3)) for e in IS['elements'] for P in el_pts(e)]
_units = max(_pr) - min(_pr)
check(f'item: in the gui it points like a vanilla sword (the hilt lower left, the scabbard tip upper right), {_units:.2f} units long '
      '(within 1 % of S2c\'s 23.57, so its display transforms still frame it)',
      grip_c[0] < scab_c[0] and grip_c[1] < scab_c[1] and abs(_units / 23.57 - 1) <= .01, f'grip {grip_c[:2]} scab {scab_c[:2]} units {_units:.2f}')
gd = D_.get('ground', {})
pts = [rotp([P[i] - 8 for i in range(3)], gd.get('rotation', [0, 0, 0])) for e in IS['elements'] for P in el_pts(e)]
sy = gd.get('scale', [1, 1, 1])[1]
low = min(p[1] * sy + gd.get('translation', [0, 0, 0])[1] for p in pts) / 16 + .25 * sy
check(f'item: on the ground it lies flat (rotation x 90) above the floor (lowest {low:.3f} b over the bob)', abs(abs(gd.get('rotation', [0])[0]) - 90) < 1e-6 and low >= 0)
fx = D_.get('fixed', {})
check('item: the fixed (frame) transform turns it to face the frame and fits (scale <= 1)', max(fx.get('scale', [9])) <= 1)
# F-I (HR-03, the D7 verifier's note): the guard's lotus card lies on the guard plate (the item's shift applied to it too)
_plate = [e for e in IS['elements'] if any(f['texture'] == '#iron' for f in e['faces'].values())]
_card = [e for e in IS['elements'] if any(f['texture'] == '#guard' for f in e['faces'].values())]
check('item: the guard card sits on the guard plate\'s top face (not up the scabbard: HR-03)', len(_plate) == 1 and len(_card) == 1
      and _plate[0]['to'][1] - 1e-3 <= _card[0]['from'][1] <= _plate[0]['to'][1] + .1,
      (_plate[0]['from'][1], _plate[0]['to'][1], _card[0]['from'][1]) if _plate and _card else (_plate, _card))

# ---------------------------------------------------------------- F-I (HR-03): the slot icon
# The lead's decision (11-05): items/item_sword.json selects on display_context; gui / fixed / ground show a dedicated chunky
# icon (our sword's silhouette, its long parts >= 2 GUI px wide at 16 x 16, readable at x 2), the hands keep the rig sword
_def = json.loads((ASSETS / 'items/mboss/scarlet/item_sword.json').read_text())['model']
_icon_id = MAN['item_sword'].get('icon', {}).get('model', '')
check('item: items/item_sword.json selects on display_context: gui / fixed / ground -> the icon model, the hands / item_display '
      'none (the fallback) -> the rig model', _def.get('type') == 'minecraft:select' and _def.get('property') == 'minecraft:display_context'
      and len(_def.get('cases', [])) == 1 and sorted(_def['cases'][0]['when']) == ['fixed', 'ground', 'gui']
      and _def['cases'][0]['model'].get('model') == 'rlk:item/mboss/scarlet/item_sword_icon' == 'rlk:item/' + _icon_id.split(':')[1]
      and _def.get('fallback', {}).get('model') == 'rlk:item/mboss/scarlet/item_sword', json.dumps(_def)[:200])
ICO = item_model(api.ITEM_MODEL, 'gui')
check('item: the icon\'s textures are rig sprites also used by the rig\'s own models (0 extra px)',
      set(ICO['textures'].values()) <= rig_tex & other_tex, str(set(ICO['textures'].values()) - (rig_tex & other_tex)))
check('item: the icon = the manifest\'s icon block (contexts, display transforms); gui lit front, as drawn (scale 1)',
      ICO.get('display') == MAN['item_sword']['icon']['display'] and ICO.get('gui_light') == 'front'
      and ICO['display'].get('gui', {}).get('scale') == [1, 1, 1] and ICO['display'].get('gui', {}).get('rotation') == [0, 0, 0])


def slot_raster(m, scale):
    """the model's gui context at GUI x `scale` (16 x scale px square, pixel centres, no AA: the GUI's item drawing); every
    face of every element (rotation, then display.gui about the centre); returns the lit-pixel rows"""
    g = m['display']['gui']
    n = 16 * scale
    lit = [[False] * n for _ in range(n)]
    for e in m['elements']:
        P = [rotp([(p[i] - 8) * g.get('scale', [1, 1, 1])[i] for i in range(3)], g.get('rotation', [0, 0, 0])) for p in el_pts(e)]
        Q = [(p[0] + 8 + g.get('translation', [0, 0, 0])[0], 8 - p[1] - g.get('translation', [0, 0, 0])[1]) for p in P]
        # the element's outline seen along z: the convex hull of its 8 projected corners
        pts = sorted(set((round(x, 6), round(y, 6)) for x, y in Q))
        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        lo, hi = [], []
        for p in pts:
            while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
                lo.pop()
            lo.append(p)
        for p in reversed(pts):
            while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
                hi.pop()
            hi.append(p)
        hull_ = lo[:-1] + hi[:-1]
        if len(hull_) < 3:
            continue
        for j in range(n):
            for i in range(n):
                x, y = (i + .5) / scale, (j + .5) / scale
                if all(cross(hull_[k], hull_[(k + 1) % len(hull_)], (x, y)) >= 0 for k in range(len(hull_))):
                    lit[j][i] = True
    return lit


def pieces(lit):
    n, seen, cnt = len(lit), set(), 0
    for j in range(n):
        for i in range(n):
            if lit[j][i] and (j, i) not in seen:
                cnt += 1
                st = [(j, i)]
                seen.add((j, i))
                while st:
                    a, b = st.pop()
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            u, v = a + da, b + db
                            if 0 <= u < n and 0 <= v < n and lit[u][v] and (u, v) not in seen:
                                seen.add((u, v))
                                st.append((u, v))
    return cnt


for _nm, _m in (('icon', ICO), ('rig model (the hands)', IS)):
    _L = slot_raster(_m, 2)
    _rows = [sum(r) for r in _L if any(r)]
    _mid = _rows[1:-1]          # the two end rows cut a corner of the diagonal (1 px, as a vanilla sword's tip)
    _ok = len(_rows) >= 3 and min(_mid) >= 2 and sum(_rows) >= 100 and pieces(_L) == 1
    msg = (f'item: {_nm} at GUI x 2 (32 x 32): {sum(_rows)} lit px in {len(_rows)} rows, the thinnest row between the two end '
           f'corners {min(_mid) if _mid else 0} px, {pieces(_L)} piece(s)')
    if _nm == 'icon':
        check(msg + ' (every lit row but the two end corners >= 2 px, >= 100 px, one piece: HR-03)', _ok)
    else:
        print('     (info) ' + msg + ' - the hairline the icon replaces in the slot')
_x1 = slot_raster(ICO, 1)
check('item: the icon fits the 16 x 16 slot (nothing drawn outside it) and spans it (>= 14 px each way)',
      all(0 <= (p[0] - 8) * 1 + 8 <= 16 and 0 <= 8 - (p[1] - 8) <= 16 for e in ICO['elements'] for p in el_pts(e))
      and sum(1 for i in range(16) if any(_x1[j][i] for j in range(16))) >= 14 and sum(1 for r in _x1 if any(r)) >= 14)
_long = [e for e in ICO['elements'] if e['to'][1] - e['from'][1] >= 3]
check('item: the icon\'s long parts (the scabbard, the grip) are >= 2 GUI px wide (HR-03: the rig model\'s 0.38)',
      _long and all((e['to'][0] - e['from'][0]) * ICO['display']['gui']['scale'][0] >= 2 for e in _long),
      [(e['to'][0] - e['from'][0], e['to'][1] - e['from'][1]) for e in _long])
_g = [P for e in ICO['elements'] if any(f['texture'] == '#grip' for f in e['faces'].values()) for P in el_pts(e)]
_s = [P for e in ICO['elements'] if any(f['texture'] == '#scab' for f in e['faces'].values()) for P in el_pts(e)]
_gc, _sc = ([sum(c) / len(c) for c in zip(*X)] for X in (_g, _s))
check('item: the icon points like a vanilla sword (the grip lower left, the scabbard tip upper right)', _gc[0] < _sc[0] and _gc[1] < _sc[1])
_gd = ICO['display'].get('ground', {})
_low = min(p[1] * _gd['scale'][1] + _gd['translation'][1] for e in ICO['elements'] for p in
           (rotp([P[i] - 8 for i in range(3)], _gd.get('rotation', [0, 0, 0])) for P in el_pts(e))) / 16 + .25 * _gd['scale'][1]
check(f'item: the dropped icon stands upright at the vanilla item\'s size (half) and stays over the floor (lowest {_low:.3f} b over the bob)',
      _gd.get('rotation') == [0, 0, 0] and _gd.get('scale') == [.5, .5, .5] and _low >= 0)

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
            tip = world(sw, (0, SW_TIP / SW_DS, 0))     # the blade axis is the model's +Y (at its display scale: SW_TIP b)
            d_tip, d_grip = math.dist(tip, fl['t']), math.dist(sw['t'], fl['t'])
            if d_tip < d_grip + .62 * SW_TIP * sw['s'][1] / SW_DS:     # a wrist bent back past ~130 deg (vis scales both)
                held_bad.append(f'{clip} t{t} blade {d_grip:.2f}->{d_tip:.2f}')
            if clip in ('idle', 'idle2', 'walk'):
                idle_tip[clip] = min(idle_tip.get(clip, 9), tip[1])
        sc, fr_ = fr.get('scabbard', (None,))[0], fr.get('forearm_r', (None,))[0]
        if sc and fr_ and max(sc['s']) > 1e-4 and math.dist(sc['t'], world(fr_, SC_HAND_P)) < SC_HAND_R:
            stip = world(sc, (0, SC_TIP / SC_DS, 0))
            if math.dist(stip, fr_['t']) < math.dist(sc['t'], fr_['t']) + .55 * SC_TIP * sc['s'][1] / SC_DS:
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
    BOX = {n: base_box(PART[n]['model']) for n in BODYP + ['forearm_r']}
    thru, n_ev = [], 0
    for clip in MAN['clips']:
        # S2d: where the right hand is free (manifest support.free_r) the blade keeps out of its forearm too
        free_r = {t for a, b in ((SUPT or {}).get(clip, {}).get('free_r') or []) for t in range(a, b + 1)}
        for ev, te in MAN['clips'][clip]['events'].items():
            if te == 0:
                continue                # tick 0 blends from the previous clip's pose (the builder checks it as authored)
            fr = REPLAY[clip][te][0]
            sw = fr.get('sword', (None,))[0]
            if not sw or max(sw['s']) < 1e-4:
                continue
            n_ev += 1
            samples = [world(sw, (0, (SW_LO + (SW_TIP - SW_LO) * k / 40) / SW_DS, 0)) for k in range(41)]
            for n in BODYP + (['forearm_r'] if te in free_r else []):
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
    check(f'skin: no blade through her body at the clip events (torso / pelvis / head / upper arms / thighs / shins, the free right forearm, 1 cm in; '
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
# F-I (HR-31, lead decision 11-05): CS3 at 5 % -> CS4 (the lethal kick at repel 102 starts the ending in the same tick). Her
# body meets; the hat goes from beside her (the repel's DOWN) over her face only under CS4's opening hard cut (seq.SEAM_CUT:
# a full-screen flash from the ending's tick 0, fully on while the hat's 1-t interpolation runs); under it the head settles
# 0.15 b into LY's chin-up rest (allowed up to 0.25 b there: a settle, not a jump), every other anchor within its TOL
SEAM = {('repel', 102, 'ending', 0): {'hat_crown': None, 'head': .25}}
for (a, ta, b, tb), cut in SEAM.items():
    A_, B_ = anchors_at(a, ta), anchors_at(b, tb)
    d = {k: round(math.dist(A_[k], B_[k]), 3) for k in api.ANCHORS}
    over_ = {k: v for k, v in d.items() if v > (cut[k] if k in cut and cut[k] is not None else 9e9 if k in cut else TOL[k])}
    st = (DP / f'data/rlk/function/boss/scarlet/seq/{b}/start.mcfunction')
    m_ = re.search(r'fx/hud/ovl \{g:"(white|black)",in:0,hold:(\d+),out:\d+\}', st.read_text() if st.exists() else '')
    check(f'cine: the seam {a}[{ta}] -> {b}[{tb}]: the body meets (anchors within 0.06-0.25 b, the head <= 0.25), the hat '
          f'({", ".join(f"{k} {d[k]} b" for k in cut)}) moves under a hard cut at {b} tick 0 (ovl white / black in 0, hold >= 2: '
          f'{m_.group(0) if m_ else None})', not over_ and m_ is not None and int(m_.group(2)) >= 2, over_)
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


# ================================================================ S2d: the player avatar's body (manifest dims / skeleton / support / retarget)
def skipped(sec, what):
    print(f'skipped {sec} (manifest without {what})')


def at(v, d):
    """The point d (blocks, along the part's own axes, unscaled) of a shown part transform (the display frame)."""
    r = qrot(v['q'], d)
    return [v['t'][i] + r[i] for i in range(3)]


def MZ(v):
    """Rig frame (the manifest's offsets / spots: +X her left, -Z forward) <-> the display frame of the key files (z mirrored)."""
    return [v[0], v[1], -v[2]]


def shown_v(fr, n):
    v = fr.get(n, (None,))[0]
    return v if v is not None and max(abs(x) for x in v['s']) > 1e-4 else None


def pts_of(fr, mdl, n):
    v = shown_v(fr, n)
    return [world(v, Q) for Q in hull(model_of(n, mdl))] if v else []


def str_pts(fr, mdl):
    """The hat strings' painted points (manifest dims.strings.painted, the authoring frame: z mirrored into the display frame),
    else the strings model's hull."""
    v = shown_v(fr, 'hat_strings')
    sp = ((MAN.get('dims') or {}).get('strings') or {}).get('painted')
    if not v or not sp:
        return pts_of(fr, mdl, 'hat_strings')
    return [world(v, (P[0], P[1], -P[2])) for P in sp]


def low_of(fr, mdl, names):
    ys = [p[1] for n in names for p in pts_of(fr, mdl, n)]
    return min(ys) if ys else 9.0


def box_of(m, k=0):
    """Element k of rig model m as a box (blocks about the pivot, after the client's Ry180)."""
    e = item_model(f'rlk:mboss/scarlet/{m}')['elements'][k]
    xs = sorted((-(e['from'][0] / 16 - .5), -(e['to'][0] / 16 - .5)))
    zs = sorted((-(e['from'][2] / 16 - .5), -(e['to'][2] / 16 - .5)))
    return [xs[0], e['from'][1] / 16 - .5, zs[0]], [xs[1], e['to'][1] / 16 - .5, zs[1]]


def depth_in(P, v, box):
    """How deep the point P lies inside the box of the part transform v (> 0 inside; blocks)."""
    lo, hi = box
    L = qrot([-v['q'][0], -v['q'][1], -v['q'][2], v['q'][3]], [P[i] - v['t'][i] for i in range(3)])
    L = [L[i] / v['s'][i] for i in range(3)]
    return min(min(L[i] - lo[i], hi[i] - L[i]) for i in range(3)) * min(v['s'])


def ticks(spans):
    return [t for a, b in spans for t in range(a, b + 1)]


VIS_HAT = {}


def hat_pts(fr, mdl):
    """The hat's visible points: the crown's corners and the brim's painted ring (radius dims.hat.R; the brim squares' corners
    outside it are transparent)."""
    v = shown_v(fr, 'hat')
    if not v:
        return []
    m = model_of('hat', mdl)
    if m not in VIS_HAT:
        R = DIMS['hat']['R']
        pts = hull(m)
        ys = sorted({round(P[1], 4) for P in pts if math.hypot(P[0], P[2]) > R + .01})
        VIS_HAT[m] = [P for P in pts if math.hypot(P[0], P[2]) <= R + .01] + \
            [(R * math.cos(k * math.pi / 16), y, R * math.sin(k * math.pi / 16)) for y in ys for k in range(32)]
    return [world(v, Q) for Q in VIS_HAT[m]]


def steady(clip):
    """The replay in game time: a loop clip's second cycle (its tick 0 / loop start blends from the cycle's end, as in game);
    a one-shot clip's first keys blend from the previous clip, so the ticks before they land are returned as `blend` (skipped
    by the S2d checks; the hand-over test covers them). Returns (frames as replay(), blend ticks)."""
    cd = RIG / 'c' / clip / 'k'
    L, loop = MAN['clips'][clip]['len'], MAN['clips'][clip]['loop']
    order = list(range(L + 1)) if not loop else list(range(L)) + list(range(loop[0], L)) + [loop[0]]
    tgt, mdl, hat, rec, first_end = {}, {'forearm_l': PART['forearm_l']['model'], 'forearm_r': PART['forearm_r']['model'],
                                          'face': PART['face']['model']}, None, {}, {}
    lines = {}
    for g, t in enumerate(order):
        if t not in lines:
            f = cd / f'{t}.mcfunction'
            lines[t] = f.read_text().splitlines() if f.exists() else []
        for line in lines[t]:
            m = KEY.match(line)
            if m and m.group(1) in UUID2PART:
                n = UUID2PART[m.group(1)]
                tgt[n] = (shown_at(tgt, n, g) if n in tgt else None, parse_tf(m.group(3)), g, int(m.group(2)))
                first_end.setdefault(n, g + int(m.group(2)))
                continue
            m = SWAP.match(line)
            if m:
                mdl[m.group(1)] = MAN['look_models']['hands'][m.group(1)][m.group(2)] if m.group(1) != 'face' else MAN['look_models']['face'][m.group(2)]
            m = HAT_IDX.match(line)
            if m:
                hat = int(m.group(1))
        tick = L if (loop and g == len(order) - 1) else t
        rec[tick] = ({n: (shown_at(tgt, n, g), tgt[n][3] == 0 and tgt[n][2] == g) for n in api.PARTS if n in tgt}, dict(mdl), hat)
    settle = max(first_end.values()) if first_end else 0
    blend = set(range(settle if not loop else min(settle, loop[0])))
    return [rec[t] for t in range(L + 1)], blend


BODY_PARTS = ['head', 'torso', 'pelvis', 'arm_l', 'arm_r', 'forearm_l', 'forearm_r', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r']
CORE_P = ['pelvis', 'torso', 'head', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r']

# ---------------------------------------------------------------- body: the avatar's elements, exactly
if SKEL:
    CLASSIC = {   # the player avatar (its slim 3-px arms; S2d round 2): base box (model units, pivot [8, 8, 8]), skin region, rows, outer inflate
        'head': ([4, 8, 4], [12, 16, 12], 'head', 0, 8, .5), 'torso': ([4, 8, 6], [12, 17, 10], 'body', 0, 9, .25),
        'pelvis': ([4, 8, 6], [12, 11, 10], 'body', 9, 12, .25),
        'arm_r': ([6.5, 4, 6], [9.5, 10, 10], 'arm_r', 0, 6, .25), 'arm_l': ([6.5, 4, 6], [9.5, 10, 10], 'arm_l', 0, 6, .25),
        'thigh_r': ([6, 2, 6], [10, 8, 10], 'leg_r', 0, 6, .25), 'thigh_l': ([6, 2, 6], [10, 8, 10], 'leg_l', 0, 6, .25),
        'shin_r': ([6, 2, 6], [10, 8, 10], 'leg_r', 6, 12, .25), 'shin_l': ([6, 2, 6], [10, 8, 10], 'leg_l', 6, 12, .25)}
    REGIONS = {'head': ((0, 0, 8, 8, 8), (32, 0, 8, 8, 8)), 'body': ((16, 16, 8, 12, 4), (16, 32, 8, 12, 4)),
               'arm_r': ((40, 16, 3, 12, 4), (40, 32, 3, 12, 4)), 'arm_l': ((32, 48, 3, 12, 4), (48, 48, 3, 12, 4)),
               'leg_r': ((0, 16, 4, 12, 4), (0, 32, 4, 12, 4)), 'leg_l': ((16, 48, 4, 12, 4), (0, 48, 4, 12, 4))}
    AV = {'head': ('player_motion/skirk/head', None), 'torso': ('player_motion/skirk/body', (0, 9)),
          'pelvis': ('player_motion/skirk/body', (9, 12)), 'arm_r': ('player_motion/skirk/right_arm', None),
          'arm_l': ('player_motion/skirk/left_arm', None), 'thigh_r': ('player_motion/skirk/right_leg', None),
          'thigh_l': ('player_motion/skirk/left_leg', None), 'shin_r': ('player_motion/skirk/right_shin', None),
          'shin_l': ('player_motion/skirk/left_shin', None)}
    for _s, _side in (('r', 'right'), ('l', 'left')):
        for _m in MAN['look_models']['hands'][f'forearm_{_s}'].values():
            AV[_m] = (f'player_motion/skirk/{_side}_forearm', None)
            CLASSIC[_m] = ([6.5, 2, 6], [9.5, 8, 10], f'arm_{_s}', 6, 12, .25)

    def skin_faces(reg, r0, r1):
        u, v, w, h, d = reg
        f = lambda a, b, c, e: [a / 4, b / 4, c / 4, e / 4]
        return {'east': f(u, v + d + r0, u + d, v + d + r1), 'north': f(u + d, v + d + r0, u + d + w, v + d + r1),
                'west': f(u + d + w, v + d + r0, u + 2 * d + w, v + d + r1), 'south': f(u + 2 * d + w, v + d + r0, u + 2 * d + 2 * w, v + d + r1),
                'up': f(u + d, v, u + d + w, v + d), 'down': f(u + d + w, v + d, u + d + 2 * w, v)}

    def classic(m):
        fr_, to_, reg, r0, r1, inf = CLASSIC[m]
        return [{'from': [x - i for x in fr_], 'to': [x + i for x in to_], 'uv': skin_faces(REGIONS[reg][k], r0, r1)}
                for k, i in ((0, 0), (1, inf))]

    def avatar(m):
        """The RP's avatar model of body model m (torso / pelvis: the body's rows r0..r1 moved onto the pivot), else None."""
        rel, rows = AV[m]
        p = ASSETS / f'models/item/{rel}.json'
        if not p.exists():
            return None
        els = json.loads(p.read_text())['elements']
        out = []
        for e in els:
            fr_, to_, uv = list(e['from']), list(e['to']), {k: list(f['uv']) for k, f in e['faces'].items()}
            if rows:
                r0, r1 = rows
                base = els[0]
                top, i, H = base['to'][1], base['from'][0] - e['from'][0], base['to'][1] - base['from'][1]
                shift = 8 - (top - r1)
                fr_[1], to_[1] = top - r1 - i + shift, top - r0 + i + shift
                for k in ('east', 'north', 'west', 'south'):
                    v0, v1 = uv[k][1], uv[k][3]
                    uv[k][1], uv[k][3] = v0 + (v1 - v0) * r0 / H, v0 + (v1 - v0) * r1 / H
            out.append({'from': fr_, 'to': to_, 'uv': uv})
        return out

    def same_els(els, want):
        if len(els) != len(want):
            return f'{len(els)} elements'
        for e, w in zip(els, want):
            if any(abs(a - b) > 1e-4 for a, b in zip(e['from'] + e['to'], w['from'] + w['to'])):
                return f'from / to {e["from"]} {e["to"]} vs {w["from"]} {w["to"]}'
            got = {k: (f['uv'] if 'faces' in e else f) for k, f in (e['faces'] if 'faces' in e else e['uv']).items()}
            if set(got) != set(w['uv']) or any(abs(a - b) > 1e-4 for k in got for a, b in zip(got[k], w['uv'][k])):
                return 'uv'
        return ''
    body_bad, n_rp, tab_bad = [], 0, []
    for m in sorted(AV):
        ref = avatar(m)
        if ref:
            n_rp += 1
            why = same_els(ref, classic(m))
            if why:
                tab_bad.append(f'{m}: {why}')
        why = same_els(item_model(f'rlk:mboss/scarlet/{m}')['elements'], ref or classic(m))
        if why:
            body_bad.append(f'{m}: {why}')
    check(f'body: the {len(AV)} body models equal the player avatar\'s two elements exactly (from / to, the six face UVs; {n_rp} against '
          f'the RP\'s avatar models, {len(AV) - n_rp} against the spec table)', len(AV) == 15 and not body_bad, '; '.join(body_bad[:5]))
    if n_rp:
        check(f'body: the test\'s spec table reproduces the RP\'s avatar models ({n_rp})', not tab_bad, '; '.join(tab_bad[:5]))
    # S2d round 2: the arm boxes' width follows the skin's own arm layout (a slim skin paints 3 + 3 columns on its arm tops and
    # leaves the last two columns of each arm region transparent; a classic skin paints 4 + 4 / 16)
    _skp = ASSETS / 'textures/mboss/scarlet/skin.png'
    if _skp.exists():
        from PIL import Image
        _sk = Image.open(_skp).convert('RGBA').load()
        _lay = {}
        for _rn, ((_u, _v, *_), (_ou, _ov, *_)) in (('arm_r', ((40, 16), (40, 32))), ('arm_l', ((32, 48), (48, 48)))):
            _tail = sum(_sk[x, y][3] > 0 for (u0, v0) in ((_u, _v), (_ou, _ov)) for x in (u0 + 14, u0 + 15) for y in range(v0 + 4, v0 + 16))
            _top = sum(_sk[x, y][3] > 0 for x in (_u + 10, _u + 11) for y in range(_v, _v + 4))
            _lay[_rn] = 3 if _tail == 0 and _top == 0 else 4
        _wid = {n: round(CLASSIC[n][1][0] - CLASSIC[n][0][0], 3) for n in ('arm_r', 'arm_l')}
        _got = {n: round(item_model(f'rlk:mboss/scarlet/{n}')['elements'][0]['to'][0] - item_model(f'rlk:mboss/scarlet/{n}')['elements'][0]['from'][0], 3) for n in ('arm_r', 'arm_l')}
        _reg = {n: MAN['skin']['regions'][n][0][2] for n in ('arm_r', 'arm_l')} if MAN.get('skin', {}).get('regions') else _lay
        check(f'body: the arm boxes match the skin\'s arm layout ({"slim 3-px" if set(_lay.values()) == {3} else "classic 4-px"}: the boxes '
              f'{_got}, the manifest regions w {_reg})', all(_got[n] == _lay[n] == _wid[n] == _reg[n] for n in _lay), str((_lay, _got, _reg)))
    sc_bad = [n for n in BODY_PARTS if PART[n].get('scale', 1) != 1 or any(abs(x - 1) > 1e-9 for x in PART[n]['rest']['s'])]
    check('body: every body part at display scale 1', not sc_bad, str(sc_bad))
else:
    skipped('body', 'skeleton')

# ---------------------------------------------------------------- skeleton
if SKEL:
    WANT_SK = {'hip_y': .765625, 'hipJ': [.125, 0, 0], 'waist': [0, .1875, 0], 'neckB': [0, .5625, 0], 'shoulder': [.34375, .4375, 0],
               'armU': .25, 'fore': .34375, 'thigh': .375, 'shin': .390625}
    flat = lambda v: v if isinstance(v, list) else [v]
    sk_bad = [k for k, v in WANT_SK.items() if k not in SKEL or len(flat(SKEL[k])) != len(flat(v))
              or any(abs(a - b) > 1e-9 for a, b in zip(flat(SKEL[k]), flat(v)))]
    check('skeleton: the manifest skeleton == design §1.1 (hip line .765625, hip joints ±.125, seam .1875, neck .5625, shoulders '
          '(±.34375, .4375: the avatar\'s slim shoulders), upper arm .25, fore .34375, thigh .375, shin .390625)', not sk_bad, str(sk_bad))
    RST = {n: PART[n]['rest'] for n in BODY_PARTS}
    sx, hj = SKEL['shoulder'], SKEL['hipJ']
    rel_ = lambda a, b, off: math.dist(RST[a]['t'], at(RST[b], off))
    chain = {'seam': rel_('torso', 'pelvis', SKEL['waist']), 'neck': rel_('head', 'torso', SKEL['neckB']),
             'shoulder_l': rel_('arm_l', 'torso', sx), 'shoulder_r': rel_('arm_r', 'torso', [-sx[0], sx[1], sx[2]]),
             'elbow_l': rel_('forearm_l', 'arm_l', [0, -SKEL['armU'], 0]), 'elbow_r': rel_('forearm_r', 'arm_r', [0, -SKEL['armU'], 0]),
             'hip_l': rel_('thigh_l', 'pelvis', hj), 'hip_r': rel_('thigh_r', 'pelvis', [-hj[0], hj[1], hj[2]]),
             'knee_l': rel_('shin_l', 'thigh_l', [0, -SKEL['thigh'], 0]), 'knee_r': rel_('shin_r', 'thigh_r', [0, -SKEL['thigh'], 0])}
    check(f'skeleton: the rest chain (seam + neck = 0.75 above the hip line, shoulders, elbows, hip joints, knees) within 1e-3 '
          f'(worst {max(chain.values()):.1e})', max(chain.values()) <= 1e-3, {k: round(v, 4) for k, v in chain.items() if v > 1e-3})
    _top = at(RST['head'], [0, .5, 0])[1]
    check(f'skeleton: the idle-t0 (rest) head base top {_top:.3f} == 2.00 ± 0.03', abs(_top - 2.0) <= .03)
else:
    skipped('skeleton', 'skeleton')

# ---------------------------------------------------------------- contract
if DIMS:
    pairs = [('HAT_TOP', DIMS['hat_top']), ('SWORD_LEN', DIMS['sword']['len']), ('SCABBARD_LEN', DIMS['scabbard']['L']),
             ('ITEM_SWORD_LEN', DIMS['item_sword']['len']), ('ITEM_SWORD_SCALE', DIMS['item_sword']['scale'])]
    c_bad = [f'{k} {getattr(api, k, None)} vs {v}' for k, v in pairs if getattr(api, k, None) is None or abs(getattr(api, k) - v) > .01]
    check(f'contract: api.HEIGHT {api.HEIGHT} within 0.02 of the idle-t0 head top {DIMS["height_idle"]}', abs(api.HEIGHT - DIMS['height_idle']) <= .02)
    check('contract: api HAT_TOP / SWORD_LEN / SCABBARD_LEN / ITEM_SWORD_LEN / ITEM_SWORD_SCALE == the built dims (±0.01)', not c_bad, c_bad)
    check(f'contract: api.BRIM_D {api.BRIM_D} == 2 x the hat radius {DIMS["hat"]["R"]}', abs(api.BRIM_D - 2 * DIMS['hat']['R']) <= .01)
    _reg = next(b for b in json.loads((DP / 'tools/mboss_registry.json').read_text())['boss'] if b['id'] == api.ID)
    check(f'contract: the registry pair (scale {_reg["scale"]}, hit {_reg["hit"]}) == api.BOSS, the player\'s size (scale 1.0)',
          (_reg['scale'], _reg['hit']) == (api.BOSS['scale'], api.BOSS['hit']) and _reg['scale'] == 1.0)
    _mg = api.BOSS['hit']['h'] - DIMS['hull_top']
    check(f'contract: hit h {api.BOSS["hit"]["h"]} - the idle hull top {DIMS["hull_top"]} = {_mg:.3f} in [0.05, 0.12]', .05 - 1e-9 <= _mg <= .12 + 1e-9)
else:
    skipped('contract', 'dims')

# ---------------------------------------------------------------- contacts / float / held / hats / blade (the shipped replay)
if SUPT and DIMS and SKEL:
    S_LEG = RET['factors']['S_LEG'] if RET else .6488
    CT = DIMS['contacts']
    GRIP = CT['grip']
    BB = {n: box_of(PART[n]['model']) for n in BODY_PARTS}
    HEAD_LAYER = box_of('head', 1)
    ST = DIMS['stone']
    HATS_ = list(api.LOOKS['hat'])
    HI = {h: i for i, h in enumerate(HATS_)}

    def grip_of(fr, side):
        v = shown_v(fr, 'forearm_l' if side > 0 else 'forearm_r')
        return at(v, [0, -GRIP, 0]) if v else None

    def yaw_of(fr):
        """Her yaw in the rig frame (the pelvis's forward, -Z, about +Y)."""
        f_ = MZ(qrot(fr['pelvis'][0]['q'], [0, 0, 1]))
        return math.atan2(-f_[0], -f_[2])

    def roty(v, a):
        c, s = math.cos(a), math.sin(a)
        return [v[0] * c + v[2] * s, v[1], -v[0] * s + v[2] * c]
    bad = {k: [] for k in ('feet', 'lie', 'seat', 'stone', 'kneel', 'touch', 'items', 'hatfloor', 'brim', 'hilt', 'throat', 'lips',
                           'twohand', 'air', 'lift', 'held', 'sheathe', 'hat_hand', 'cup', 'bottle', 'hilt_pivot', 'worn', 'back',
                           'world', 'jump', 'blade', 'hat_clear', 'strings', 'brim_head', 'first_key', 'hinge_arm', 'hinge_leg')}
    worst = {}

    def note(k, v):
        worst[k] = max(worst.get(k, 0), v)
    blade_soft, n_blade = 0, 0
    for clip in REPLAY:
        sp = SUPT.get(clip)
        if not sp:
            continue
        frames, blend = steady(clip)
        st_ = states(clip)
        ghost = set(ticks(sp['ghost'])) | blend
        sw_ticks = {}
        # S2d round 3 (C3-2): the elbow is the avatar's hinge: the upper arm's and the forearm's x axes (the hinge axis) agree
        # within 10 deg wherever the arm bends > 10 deg (blend-in, ghost, cut and post-cut ticks aside); the knees within 60 (the
        # legs keep a roll limit per segment: the kneel's knee lands in one tick, 47-54 deg there for a few ticks)
        cut_set = set(sp['cuts']) | {t + 1 for t in sp['cuts']}
        _u = lambda v: [x / (math.sqrt(sum(y * y for y in v)) or 1) for x in v]
        _ang = lambda a, b: math.degrees(math.acos(max(-1, min(1, sum(x * y for x, y in zip(_u(a), _u(b)))))))
        for t in range(len(frames)):
            if t in ghost or t in cut_set:
                continue
            fr = frames[t][0]
            for a_, b_, key, lim in (('arm_l', 'forearm_l', 'hinge_arm', 10), ('arm_r', 'forearm_r', 'hinge_arm', 10),
                                     ('thigh_l', 'shin_l', 'hinge_leg', 60), ('thigh_r', 'shin_r', 'hinge_leg', 60)):
                if a_ not in fr or b_ not in fr or min(fr[a_][0]['s']) < 1e-4 or min(fr[b_][0]['s']) < 1e-4:
                    continue
                qa_, qb_ = fr[a_][0]['q'], fr[b_][0]['q']
                bend = _ang(qrot(qa_, [0, 1, 0]), qrot(qb_, [0, 1, 0]))
                if bend <= 10:
                    continue
                hg = _ang(qrot(qa_, [1, 0, 0]), qrot(qb_, [1, 0, 0]))
                note(key, hg)
                if hg > lim:
                    bad[key].append(f'{clip} t{t} {b_} {hg:.0f} deg at a {bend:.0f}-deg bend')
        # planted feet: that side's shin hull lowest within ±0.012
        for side, key in ((1, 'feet_l'), (-1, 'feet_r')):
            for t in ticks(sp[key]):
                if t in ghost:
                    continue
                fr, mdl, _ = frames[t]
                lo = low_of(fr, mdl, ['shin_l' if side > 0 else 'shin_r'])
                note('feet', abs(lo))
                if abs(lo) > .012:
                    bad['feet'].append(f'{clip} t{t} {key} {lo:.3f}')
        for t in ticks(sp['lie']):
            fr, mdl, _ = frames[t]
            lo, lp, lt = low_of(fr, mdl, CORE_P), low_of(fr, mdl, ['pelvis']), low_of(fr, mdl, ['torso'])
            note('lie', lo)
            note('lie_gap', max(lp, lt))
            if lo > .012 or lp > .06 or lt > .06:
                bad['lie'].append(f'{clip} t{t} core {lo:.3f} pelvis {lp:.3f} torso {lt:.3f}')
        for t in ticks(sp['seat']):
            fr, mdl, _ = frames[t]
            lo = low_of(fr, mdl, ['thigh_l', 'thigh_r'])
            note('seat', abs(lo - DIMS['seat_top']))
            if abs(lo - DIMS['seat_top']) > .012:
                bad['seat'].append(f'{clip} t{t} thighs {lo:.3f}')
            yw = yaw_of(fr)
            deep = 0
            for n in CORE_P:
                for P in pts_of(fr, mdl, n):
                    L = roty(MZ(P), -yw)
                    deep = max(deep, min(L[0] + ST['half'], ST['half'] - L[0], L[1], ST['T'] - L[1], L[2] - ST['front'], ST['back'] - L[2]))
            note('stone_box', deep)
            if deep > .01:
                bad['stone'].append(f'{clip} t{t} {deep:.3f} in the stone')
        # kneeling: the knee end of shin_r (its points within 0.08 of the knee, as the solver's kneel root) on the floor from the
        # tick after the patch's full weight (the bend plane turns 40 deg / tick: the knee lands then), coming down at the first
        for a, b in sp['kneel']:
            for t in range(a, b + 1):
                fr, mdl, _ = frames[t]
                v = shown_v(fr, 'shin_r')
                lo = min(world(v, Q)[1] for Q in hull(model_of('shin_r', mdl)) if Q[1] >= -.08) if v else 9.0
                if t > a:
                    note('kneel', lo)
                if lo > (.012 if t > a else .25):
                    bad['kneel'].append(f'{clip} t{t} the knee {lo:.3f}')
        for t in ticks(sp['touch']):
            if t in ghost:
                continue
            fr, mdl, _ = frames[t]
            lo = low_of(fr, mdl, CORE_P)
            note('touch', lo)
            if lo > .012:
                bad['touch'].append(f'{clip} t{t} core {lo:.3f}')
        for t in ticks(sp['air']):
            fr, mdl, _ = frames[t]
            # (a partial lying / kneeling root keeps her share on its support: the support pass's airborne height x (1 - w_root))
            lo, need = low_of(fr, mdl, CORE_P), min(.5 * S_LEG * sp['low_ref'][t], .05) * (1 - (sp.get('w_root') or [0] * (t + 1))[t])
            if lo < need - 1e-6:
                bad['air'].append(f'{clip} t{t} core {lo:.3f} < {need:.3f}')
        support_t = set(ticks(sp['feet_l']) + ticks(sp['feet_r']) + ticks(sp['lie']) + ticks(sp['seat']) + ticks(sp['kneel'])
                        + ticks(sp['touch']) + [c[0] for c in sp['contacts']]) - ghost
        for t in sorted(support_t):
            lf = sp.get('lift', {}).get(str(t), 0)
            note('lift', lf)
            if lf > .005:
                bad['lift'].append(f'{clip} t{t} {lf:.3f}')
        # the hand contacts
        for c in sp['contacts']:
            t, kind, side = c[0], c[1], c[2]
            if t in ghost:
                continue
            fr, mdl, _ = frames[t]
            g = grip_of(fr, side)
            if g is None:
                continue
            if kind == 'stone':
                item = 'bottle' if side > 0 else 'cup'
                v = shown_v(fr, item)
                spot = MZ(roty(DIMS['seat_items'][item], yaw_of(fr)))
                if v:
                    d = math.dist(v['t'], spot)
                    note('items', d)
                    if d > .03:
                        bad['items'].append(f'{clip} t{t} {item} base {d:.3f} from its spot')
            elif kind == 'hatfloor':
                hv = shown_v(fr, 'hat')
                if hv and frames[t][2] == HI['world']:
                    h = hv['t']
                    hp = [h[0] - math.copysign(DIMS['hat']['R'] - CT['hat_floor_hold']['inset'], h[0]), h[1] + CT['hat_floor_hold']['up'], h[2]]
                    d = math.dist(g, hp)
                    note('hatfloor', d)
                    if d > .04:
                        bad['hatfloor'].append(f'{clip} t{t} {d:.3f}')
            elif kind == 'brim' and len(c) > 3:
                hv = shown_v(fr, 'hat')
                if hv:
                    bh = CT['brim_hold']
                    B = -side * c[3] * math.pi / 180
                    hp = at(hv, MZ([-math.sin(B) * bh['r'], 0, -math.cos(B) * bh['r']]))
                    hp[1] += bh['dy']
                    d = math.dist(g, hp)
                    note('brim', d)
                    if d > .04:
                        bad['brim'].append(f'{clip} t{t} {d:.3f}')
            elif kind in ('hilt', 'throat'):
                sv = shown_v(fr, 'scabbard')
                if sv:
                    d = math.dist(g, at(sv, [0, CT[kind], 0]))
                    note(kind, d)
                    if d > .04:
                        bad[kind].append(f'{clip} t{t} {d:.3f}')
            elif kind == 'lips':
                cv, hv = shown_v(fr, 'cup'), shown_v(fr, 'head')
                if cv and hv:
                    d = math.dist(at(cv, [0, CT['cup_centre'], 0]), at(hv, MZ(CT['lip_mouth'])))
                    note('lips', d)
                    if d > .05:
                        bad['lips'].append(f'{clip} t{t} {d:.3f}')
            elif kind == 'twohand':
                sv = shown_v(fr, 'sword')
                if sv:
                    d = math.dist(g, at(sv, [0, -CT['two_hand'], 0]))
                    note('twohand', d)
                    if d > .12:
                        bad['twohand'].append(f'{clip} t{t} {d:.3f}')
            elif kind == 'sheathe':
                sv, cv = shown_v(fr, 'sword'), shown_v(fr, 'scabbard')
                if sv and cv:
                    a1, a2 = qrot(sv['q'], [0, 1, 0]), qrot(cv['q'], [0, 1, 0])
                    ang = math.degrees(math.acos(max(-1, min(1, sum(x * y for x, y in zip(a1, a2))))))
                    dv = [sv['t'][i] - cv['t'][i] for i in range(3)]
                    along = sum(dv[i] * a2[i] for i in range(3))
                    off = math.dist(dv, [a2[i] * along for i in range(3)])
                    dg = math.dist(sv['t'], grip_of(fr, 1))
                    note('sheathe', max(off, dg - .02))
                    if ang > 3 or off > .02 or dg > .04:
                        bad['sheathe'].append(f'{clip} t{t} {ang:.1f} deg / {off:.3f} b off the axis, pivot {dg:.3f} from the grip')
        # the held sword's pivot at the left grip
        for t in ticks(sp.get('held', [])):
            if t in ghost:
                continue
            fr, mdl, _ = frames[t]
            sv, g = shown_v(fr, 'sword'), grip_of(fr, 1)
            if sv and g:
                d = math.dist(sv['t'], g)
                note('held', d)
                if d > .03:
                    bad['held'].append(f'{clip} t{t} {d:.3f}')
        # the hat states (the hand-over blends exempt: 4 t before a switch into worn / back, 4 t from a switch into hand; a cut
        # snaps the hat and the display holds that snap one tick)
        hs = [h for _, _, h in frames]
        cuts = set(sp.get('cuts', []))
        exempt = {t + d for t in cuts for d in (0, 1)}
        cut1 = {t + 1 for t in cuts}
        for t in range(1, len(hs)):
            if hs[t] != hs[t - 1] and hs[t] is not None and hs[t - 1] is not None:
                if t not in cuts:
                    if hs[t] in (HI['worn'], HI['back']):
                        exempt |= set(range(t - 4, t))
                    if hs[t] == HI['hand']:
                        exempt |= set(range(t, t + 4))
                    a, b = shown_v(frames[t - 1][0], 'hat'), shown_v(frames[t][0], 'hat')
                    if a and b:
                        d = math.dist(a['t'], b['t'])
                        note('jump', d)
                        if d > .15:
                            bad['jump'].append(f'{clip} t{t} {HATS_[hs[t - 1]]}->{HATS_[hs[t]]} {d:.3f}')
        pushed = {int(k) for k in (sp.get('hat_push') or {})}
        blends = exempt - {t + d for t in cuts for d in (0, 1)}
        for t, (fr, mdl, h) in enumerate(frames):
            hv = shown_v(fr, 'hat')
            if hv is None or h is None or t in ghost:
                continue
            # the hat in her hand and every hand-over / swing tick keep out of her head and torso (S2d: guard hatClear)
            if (h == HI['hand'] or t in blends) and 'hat_push' in sp:
                deep = max([depth_in(P, fr[n][0], BB[n]) for n in ('head', 'torso') for P in hat_pts(fr, mdl)] or [0])
                note('hat_clear', deep)
                if deep > .01:
                    bad['hat_clear'].append(f'{clip} t{t} {HATS_[h]} {deep:.3f}')
            if h == HI['hand'] and t not in exempt:
                g = grip_of(fr, -1)
                d = math.dist(hv['t'], g)
                if t in pushed:
                    # pushed clear of her head where the arm cannot follow (a player-size arm raised beside the head): reported
                    note('hat_hand_pushed', abs(d - DIMS['hat']['hand']))
                    continue
                note('hat_hand', abs(d - DIMS['hat']['hand']))
                if abs(d - DIMS['hat']['hand']) > .03:
                    bad['hat_hand'].append(f'{clip} t{t} {d:.3f}')
            elif h == HI['worn'] and t not in exempt:
                hd = fr['head'][0]
                up = qrot(hd['q'], [0, 1, 0])
                dv = [hv['t'][i] - hd['t'][i] for i in range(3)]
                along = sum(dv[i] * up[i] for i in range(3))
                off = math.dist(dv, [up[i] * along for i in range(3)])
                tilt = math.degrees(math.acos(max(-1, min(1, sum(x * y for x, y in zip(qrot(hv['q'], [0, 1, 0]), up))))))
                # the crown's bottom ring on the head's base top (S2d round 1: dims.hat.crown_y0 above the brim pivot; the solver puts
                # it 0.013 over the head, the keys' translation tolerance 0.012 lets what ships drift: 0..0.025 here)
                y_lo, y_hi = (.55, .60) if 'crown_y0' not in DIMS['hat'] else (DIMS['hat']['brim'][1] - .015, DIMS['hat']['brim'][1] + .015)
                gap = along + DIMS['hat'].get('crown_y0', 0) - BB['head'][1][1]
                note('crown_gap', gap)
                if not (y_lo <= along <= y_hi and off <= .03 and tilt <= 12 and ('crown_y0' not in DIMS['hat'] or -.005 <= gap <= .025)):
                    bad['worn'].append(f'{clip} t{t} {along:.3f} up, {off:.3f} off, {tilt:.0f} deg, crown gap {gap:.3f}')
                # S2d round 2 (VB3): the brim (its lowest square = the hat's pivot plane) >= 0.001 b over the base head's four top
                # corners as shipped (no depth fight with the head's top face)
                hlo, hhi = BB['head']
                hq = [-hv['q'][0], -hv['q'][1], -hv['q'][2], hv['q'][3]]
                bh = min(-qrot(hq, [P[i] - hv['t'][i] for i in range(3)])[1]
                         for P in (world(hd, (x, hhi[1], z)) for x in (hlo[0], hhi[0]) for z in (hlo[2], hhi[2])))
                worst['brim_head'] = min(worst.get('brim_head', 9), bh)
                if bh < .001:
                    bad['brim_head'].append(f'{clip} t{t} {bh:.4f}')
            elif h == HI['back'] and t not in exempt:
                deep = max([depth_in(P, fr[n][0], BB[n]) for n in ('head', 'torso') for P in hat_pts(fr, mdl)] or [0])
                note('back', deep)
                if deep > .01:
                    bad['back'].append(f'{clip} t{t} {deep:.3f} in the head / torso')
            elif h == HI['world'] and t not in cut1:
                P_ = hat_pts(fr, mdl)
                deep = max([depth_in(P, fr[n][0], BB[n]) for n in BODY_PARTS if shown_v(fr, n) for P in P_] or [0])
                lo = min(p[1] for p in P_) if P_ else 0
                note('world', deep)
                if deep > .01 or lo < -.012:
                    bad['world'].append(f'{clip} t{t} {deep:.3f} in the body, lowest {lo:.3f}')
            # the held props: the cup under the right fist, the bottle's neck in the left fist, the sheathed hilt on the scabbard
        for t, (fr, mdl, _) in enumerate(frames):
            if t in ghost:
                continue
            # the hat strings out of her head's outer layer (every tick; the solver keeps 0.005, the keys' interpolation 0.005 more);
            # S2d round 2: the painted strings (dims.strings.painted: both strands, the loop, the strand below it), else the cards' corners
            if shown_v(fr, 'hat_strings'):
                sd = max([depth_in(P, fr['head'][0], HEAD_LAYER) for P in str_pts(fr, mdl)] or [-1])
                note('strings', sd)
                if sd > .01 and t not in cut1:
                    bad['strings'].append(f'{clip} t{t} {sd:.3f}')
            if st_[t].get('Cu') == 'hand' and shown_v(fr, 'cup'):
                deep = max([depth_in(P, fr['forearm_r'][0], BB['forearm_r']) for P in pts_of(fr, mdl, 'cup')] or [0])
                note('cup', deep)
                if deep > .03:
                    bad['cup'].append(f'{clip} t{t} {deep:.3f}')
            if st_[t].get('Bo') == 'hand' and shown_v(fr, 'bottle'):
                bv, fl = fr['bottle'][0], fr['forearm_l'][0]
                top, base = at(bv, [0, max(p[1] for p in hull('bottle')), 0]), bv['t']
                if not (depth_in(top, fl, BB['forearm_l']) > 0 > depth_in(base, fl, BB['forearm_l'])):
                    bad['bottle'].append(f'{clip} t{t}')
            hv, cv = shown_v(fr, 'hilt_sheathed'), shown_v(fr, 'scabbard')
            if hv and cv and math.dist(hv['t'], cv['t']) > 1e-3:
                bad['hilt_pivot'].append(f'{clip} t{t}')
            # the blade, every tick: no sample > 0.05 b inside head / torso / pelvis (the hands hold the hilt by design)
            sv = shown_v(fr, 'sword')
            if sv:
                n_blade += 1
                samples = [world(sv, (0, (SW_LO + (SW_TIP - SW_LO) * k / 40) / SW_DS, 0)) for k in range(41)]
                deep = max(depth_in(P, fr[n][0], BB[n]) for n in ('head', 'torso', 'pelvis') if shown_v(fr, n) for P in samples)
                note('blade', deep)
                if deep > .01:
                    blade_soft += 1
                if deep > .05:
                    bad['blade'].append(f'{clip} t{t} {deep:.3f}')
    W_ = lambda k: f'{worst.get(k, 0):.3f}'
    lst = lambda k: '; '.join(bad[k][:5]) + f' ({len(bad[k])})'
    check(f'contacts: planted feet: the shin hull lowest within ±0.012 (worst {W_("feet")})', not bad['feet'], lst('feet'))
    check(f'contacts: lying: the core lowest <= 0.012, the pelvis and torso gaps <= 0.06 (worst {W_("lie")} / {W_("lie_gap")})', not bad['lie'], lst('lie'))
    check(f'contacts: seated: the thighs\' lowest within 0.012 of the stone top {DIMS["seat_top"]} (worst {W_("seat")})', not bad['seat'], lst('seat'))
    check(f'contacts: seated: no body / leg hull point > 0.01 inside the stone (worst {W_("stone_box")})', not bad['stone'], lst('stone'))
    check(f'contacts: kneeling: the knee end of shin_r <= 0.012 from the tick after the full weight, <= 0.25 at it (worst {W_("kneel")})',
          not bad['kneel'], lst('kneel'))
    check(f'contacts: touched (S2a touched): the core lowest <= 0.012 (worst {W_("touch")})', not bad['touch'], lst('touch'))
    check(f'contacts: the stone hands: the bottle / cup base within 0.03 of its spot (worst {W_("items")})', not bad['items'], lst('items'))
    check(f'contacts: the floor hat: the right grip within 0.04 of the brim\'s hold point (worst {W_("hatfloor")})', not bad['hatfloor'], lst('hatfloor'))
    check(f'contacts: the brim holds: the grip within 0.04 of the hold point (worst {W_("brim")})', not bad['brim'], lst('brim'))
    check(f'contacts: the sheathed hilt (left) / the throat (right) within 0.04 (worst {W_("hilt")} / {W_("throat")})',
          not bad['hilt'] and not bad['throat'], lst('hilt') + ' | ' + lst('throat'))
    check(f'contacts: the sip: the cup centre within 0.05 of the mouth point (worst {W_("lips")})', not bad['lips'], lst('lips'))
    check(f'contacts: two hands on the grip: reported {W_("twohand")} b (fail > 0.12)', not bad['twohand'], lst('twohand'))
    check('float: airborne spans stay up (the core lowest >= min(0.5 S_LEG lowRef, 0.05) x (1 - the root weight))', not bad['air'], lst('air'))
    check(f'float: the last-resort lift <= 0.005 on every contact tick (worst {W_("lift")})', not bad['lift'], lst('lift'))
    check(f'blade: every tick, no blade sample > 0.05 b inside her head / torso / pelvis (worst {W_("blade")}; {blade_soft} of {n_blade} '
          'ticks with the blade out > 0.01)', not bad['blade'], lst('blade'))
    check(f'held: the held sword\'s pivot at the left grip (<= 0.03; worst {W_("held")})', not bad['held'], lst('held'))
    check('held: sheathing: the blade on the scabbard axis (<= 3 deg / 0.02 b), the pivot within 0.04 of the left grip', not bad['sheathe'], lst('sheathe'))
    check(f'held: the hat in hand {DIMS["hat"]["hand"]} ± 0.03 from the right grip (worst {W_("hat_hand")}; where it was pushed clear of her '
          f'head the hand follows as far as the arm reaches: off by {W_("hat_hand_pushed")})', not bad['hat_hand'], lst('hat_hand'))
    check(f'held: the cup under the right fist (no cup point > 0.03 inside the forearm; worst {W_("cup")})', not bad['cup'], lst('cup'))
    check('held: the bottle by its neck (its top inside the left forearm\'s box, its base outside)', not bad['bottle'], lst('bottle'))
    check('held: hilt_sheathed pivot == the scabbard pivot', not bad['hilt_pivot'], lst('hilt_pivot'))
    check(f'hats: worn: the pivot dims.hat.brim ± 0.015 above the neck along the head axis, <= 0.03 off it, up within 12 deg of the head\'s, '
          f'the crown on the head (its bottom ring 0..0.025 over the head\'s base top as shipped; worst {W_("crown_gap")})', not bad['worn'], lst('worn'))
    if 'hat_push' in next(iter(SUPT.values())):
        check(f'hats: in her hand and at every hand-over / swing tick no visible hat point > 0.01 inside her head / torso (worst {W_("hat_clear")})',
              not bad['hat_clear'], lst('hat_clear'))
    if SKEL and 'brim' in DIMS['hat']:
        check(f'hats: worn: the brim >= 0.001 b over the base head\'s top corners on every shipped tick (closest '
              f'{worst.get("brim_head", 9):.4f})', not bad['brim_head'], lst('brim_head'))
        # S2d round 2 (C2-1): a one-shot clip's first keys blend the whole body in from the previous clip's pose, so the parts that
        # ride each other (head / face / hat / strings; the sword arm / sword / glow) must land together: their first keys end on
        # the same tick (the builder ends every part's first key at the first event from tick 2, else at the clip's blend; a part
        # whose own floor / planted-foot / dense keys split the blend-in earlier is reported, not failed)
        fk_bad, fk_info = [], []
        for clip in REPLAY:
            if MAN['clips'][clip]['loop']:
                continue
            f0 = RIG / 'c' / clip / 'k' / '0.mcfunction'
            durs = {}
            for line in (f0.read_text().splitlines() if f0.exists() else []):
                m = KEY.match(line)
                if m and m.group(1) in UUID2PART and UUID2PART[m.group(1)] not in MAN['skin']['hidden']:
                    durs[UUID2PART[m.group(1)]] = int(m.group(2))
            grp = [('head', 'face', 'hat', 'hat_strings'), ('arm_l', 'forearm_l', 'sword', 'sword_glow')]
            for g_ in grp:
                ds = {n: durs.get(n) for n in g_}
                if len(set(ds.values())) > 1:
                    fk_bad.append(f'{clip} {ds}')
            if len(set(d for d in durs.values() if d)) > 1:
                fk_info.append(clip)
        _n1 = sum(1 for c_ in REPLAY if not MAN['clips'][c_]['loop'])
        check(f'blend-in: in every one-shot clip the riders\' first keys end with their part\'s (head / face / hat / strings; arm_l / '
              f'forearm_l / sword / glow; {_n1 - len(fk_info)} of {_n1} clips with one first-key end for every shown part'
              f'{": not " + ", ".join(fk_info[:8]) if fk_info else ""})', not fk_bad, '; '.join(fk_bad[:6]))
        # S2d round 3 (C3-1): the clips the module starts from state/hidden (every part at scale 0 where it stood): g_dive after
        # g_vert's 'gone' (p_ghost.py), g_dash / g_glide / g_run / g_reform / a7_tell after a script vanish or a clip-end hide.
        # There is no pose to blend from, so every shown part's first key ends on the same tick: the whole body grows in together
        ph_bad = []
        for clip in ('g_dive', 'g_dash', 'g_glide', 'g_run', 'g_reform', 'a7_tell'):
            f0 = RIG / 'c' / clip / 'k' / '0.mcfunction'
            durs = {}
            for line in (f0.read_text().splitlines() if f0.exists() else []):
                m = KEY.match(line)
                if m and m.group(1) in UUID2PART and UUID2PART[m.group(1)] not in MAN['skin']['hidden'] and min(parse_tf(m.group(3))['s']) > 1e-4:
                    durs[UUID2PART[m.group(1)]] = int(m.group(2))
            if len(set(durs.values())) != 1:
                ph_bad.append(f'{clip} ' + ', '.join(f'{d}: {[n for n in durs if durs[n] == d]}' for d in sorted(set(durs.values()))))
        check('blend-in: the clips started from the hidden rig (g_dive, g_dash, g_glide, g_run, g_reform, a7_tell): every shown part\'s '
              'first key ends on the same tick', not ph_bad, '; '.join(ph_bad))
    if 'hinge_arm' in worst or bad['hinge_arm']:
        check(f'hinge: the upper arm and forearm x axes (the elbow\'s hinge axis) within 10 deg wherever the arm bends > 10 deg '
              f'(worst {worst.get("hinge_arm", 0):.1f})', not bad['hinge_arm'], lst('hinge_arm'))
        check(f'hinge: the thigh and shin x axes within 60 deg wherever the knee bends > 10 deg (the kneel\'s landing; worst '
              f'{worst.get("hinge_leg", 0):.1f})', not bad['hinge_leg'], lst('hinge_leg'))
    check(f'hats: back: no brim point > 0.01 inside the head / torso (worst {W_("back")})', not bad['back'], lst('back'))
    check(f'hats: world: no brim point > 0.01 inside a body box, lowest >= -0.012 (worst {W_("world")})', not bad['world'], lst('world'))
    check(f'hats: no jump > 0.15 b at a non-cut switch (worst {W_("jump")})', not bad['jump'], lst('jump'))
    i0 = REPLAY['idle'][0][0]
    _sd = max([depth_in(P, i0['head'][0], HEAD_LAYER) for P in str_pts(i0, REPLAY['idle'][0][1])] or [-1])
    check(f'strings: idle t0: the strings >= 0.005 outside the head\'s outer layer (closest {-_sd:.3f})', _sd <= -.005)
    check(f'strings: every tick of every clip no strings point > 0.01 inside the head\'s outer layer (deepest {W_("strings")})', not bad['strings'], lst('strings'))
    # the intro off the seat stone (S2d round 1): she rises forward over her feet and steps aside before the turn (seq.py SEAT_RISE /
    # SEAT_ASIDE glides, the turn by face/track at 12 deg / tick, either sense): no body / leg / prop point > 0.01 inside the stone
    # from tick 0 to the walk (then she walks to the player beside it)
    try:
        from mboss_scarlet import seq as _sq3
        RISE, ASIDE = _sq3.SEAT_RISE, _sq3.SEAT_ASIDE
    except Exception:  # noqa: BLE001
        RISE = ASIDE = None
    if RISE is not None:
        e_stand, e_turn, e_walk = api.ev('intro', 'stand'), api.ev('intro', 'turn'), api.ev('intro', 'scab_hand') + 12
        fr_i, _ = steady('intro')
        # (the cup and the bottle rest on the stone's top at its item spots: the stone-hand contacts check them)
        st_parts = ['pelvis', 'torso', 'thigh_l', 'thigh_r', 'shin_l', 'shin_r', 'arm_l', 'arm_r', 'forearm_l', 'forearm_r', 'scabbard',
                    'hilt_sheathed', 'sash_tails', 'sword']
        st_worst, st_bad = 0, []
        for t in range(e_walk):
            fr, mdl, _ = fr_i[t]
            u1, u2 = min(1, max(0, (t - e_stand) / 12)), min(1, max(0, (t - e_stand - 12) / 20))
            ax, az = -ASIDE * u2, -RISE * u1
            for sense in (1, -1):
                ph = math.radians(sense * min(180, max(0, (t - e_turn + 1) * 12)))
                deep = 0
                for n in st_parts:
                    for P in pts_of(fr, mdl, n):
                        L = roty(MZ(P), ph)
                        L = [L[0] + ax, L[1], L[2] + az]
                        deep = max(deep, min(L[0] + ST['half'], ST['half'] - L[0], L[1], ST['T'] - L[1], L[2] - ST['front'], ST['back'] - L[2]))
                st_worst = max(st_worst, deep)
                if deep > .01:
                    st_bad.append(f't{t} {deep:.3f}')
        check(f'seat stone: from tick 0 to the walk no body / leg / prop point > 0.01 inside the stone (she rises {RISE} b forward and steps '
              f'{ASIDE} b aside before the turn; worst {st_worst:.3f})', not st_bad, '; '.join(st_bad[:6]) + f' ({len(st_bad)})')
        # S2d round 2 (C2-2): the feet step with the aside glide (retarget PATCHES 'ASIDE'): a sole on the floor at two ticks in a row
        # keeps its spot in the world (its end centre <= 0.02 b per tick: the inclined shin of her rise still turns about its toe; a
        # plain slide is the glide's 0.055 b per tick), and every sole travels the glide's length with it
        a0 = e_stand + 12
        sole = lambda fr, n: world(fr[n][0], (0, -SKEL['shin'], 0))
        on_floor = lambda fr, mdl, n: low_of(fr, mdl, [n]) <= .012
        slide, moved, sl_w = [], {}, 0
        for n in ('shin_l', 'shin_r'):
            w0 = None
            for t in range(a0, a0 + 21):
                fr, mdl, _ = fr_i[t]
                P = MZ(sole(fr, n))
                W = [P[0] - ASIDE * min(1, max(0, (t - a0) / 20)), P[2]]
                if t > a0:
                    fp, mp, _ = fr_i[t - 1]
                    if on_floor(fr, mdl, n) and on_floor(fp, mp, n):
                        sl_w = max(sl_w, math.dist(W, w0))
                        if math.dist(W, w0) > .02:
                            slide.append(f'{n} t{t} {math.dist(W, w0):.3f}')
                else:
                    ws = W
                w0 = W
            moved[n] = round(math.dist(w0, ws), 2)
        _as = (RET or {}).get('aside') or {}
        check(f'seat stone: the rig\'s steps (retarget aside {_as}) match seq.py\'s glide (SEAT_ASIDE {ASIDE} b over 20 t from intro {a0})',
              _as.get('t0') == a0 and _as.get('len') == 20 and abs(_as.get('d', 0) - ASIDE) < 1e-9)
        check(f'seat stone: the feet step with the aside glide (no planted sole slides > 0.02 b per tick over intro {a0}-{a0 + 20}, worst '
              f'{sl_w:.3f}; each sole moves {moved} b with the {ASIDE}-b glide)', not slide and all(abs(v - ASIDE) <= .05 for v in moved.values()),
              '; '.join(slide[:6]) + f' ({len(slide)}) {moved}')
else:
    skipped('contacts / float / held / hats / strings / blade-every-tick', 'support / dims / skeleton')

# ---------------------------------------------------------------- angles kept (the retarget changes no source angle)
if RET:
    _r = subprocess.run(['node', 'tools/scarlet_retarget.mjs', '--dump', 'all'], cwd=DP, capture_output=True, text=True)
    try:
        DUMP = json.loads(_r.stdout)
    except ValueError:
        DUMP = None
    if DUMP is None:
        check('angles: node tools/scarlet_retarget.mjs --dump all runs', False, _r.stderr[-400:])
    else:
        def same_v(a, b):
            if isinstance(a, list) or isinstance(b, list):
                return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(abs(x - y) <= 1e-9 for x, y in zip(a, b))
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return abs(a - b) <= 1e-9
            return a == b
        spans = {}
        for P in DUMP['patches']:
            spans.setdefault(P['clip'], []).append((P['id'], P['span'][0], P['span'][1]))
        outside, used = [], set()
        for c, rows in DUMP['clips'].items():
            for row in rows:
                for k in row['src']:
                    if not same_v(row['src'][k], row['out'].get(k)):
                        hit_ = [pid for pid, a, b in spans.get(c, []) if a <= row['t'] <= b]
                        if hit_:
                            used.update(hit_)
                        else:
                            outside.append(f'{c} t{row["t"]} {k}')
        print('angles: the exempt spans (the declared patches): ' + ', '.join(f'{P["id"]} {P["clip"]} {P["span"][0]}-{P["span"][1]}' for P in DUMP['patches'])
              + f'; channels differ inside {", ".join(sorted(used))}')
        check(f'angles: every angle channel of the retarget + overlay pose == the source (1e-9) outside the declared patch spans '
              f'({sum(len(r) for r in DUMP["clips"].values())} ticks of {len(DUMP["clips"])} clips)', len(DUMP['clips']) == 47 and not outside,
              '; '.join(outside[:6]) + f' ({len(outside)})')
        check('angles: the exempt spans == the manifest PATCHES', [(P['id'], P['clip'], P['span']) for P in DUMP['patches']]
              == [(P['id'], P['clip'], [P['in'][0], P['out'][1]]) for P in RET['patches']])
else:
    skipped('angles', 'retarget')

# ---------------------------------------------------------------- retarget (the per-clip table)
if RET:
    LIM = {'floor': .04, 'stone': .04, 'hatfloor': .04, 'hat': .04, 'brim': .04, 'hilt': .04, 'throat': .04, 'lips': .05, 'sheathe': .04,
           'twohand': .12}
    r_bad, ct_worst = [], {}
    print('retarget: clip passes | corrections (deg; cm: drop bPush close hatBackZ hatPush hatClear; %: armUp) | contacts | stretch residue dy lift')
    for c, row in RET['clips'].items():
        for n, v in row['corrections'].items():
            if v > RET['bounds'][n.rstrip('+-')] + 1e-6:
                r_bad.append(f'{c} {n} {v} > {RET["bounds"][n.rstrip("+-")]}')
        if row['stretch'] > 1.0005:
            r_bad.append(f'{c} stretch {row["stretch"]}')
        for k, v in row['contacts'].items():
            ct_worst[k] = max(ct_worst.get(k, 0), v)
            if v > LIM.get(k, .04):
                r_bad.append(f'{c} {k} {v}')
        if row['corrections'] or row['contacts']:
            print(f'  {c} {row["passes"]} | ' + ' '.join(f'{k}:{v:g}' for k, v in row['corrections'].items()) + ' | '
                  + ' '.join(f'{k}:{v:.3f}' for k, v in row['contacts'].items())
                  + f' | {row["stretch"]:g} {row["blade_residue"]:g} {row["support_dy"]:g} {row["lift"]:g}')
    check(f'retarget: every correction within its bound, IK stretch <= 1.0005, contact shortfalls within their kind\'s limit '
          f'({", ".join(f"{k} {v:.3f}" for k, v in sorted(ct_worst.items()))})', not r_bad, '; '.join(r_bad[:6]))
else:
    skipped('retarget', 'retarget')

# ---------------------------------------------------------------- couplings (seq.py follows the built rig)
if RET and DIMS:
    import importlib
    from mboss_scarlet import seq as _sq
    _sq = importlib.reload(_sq)
    H = AN[(cid('cs1'), 'head')][114][1]
    E_P = api.ev('cs1', 'petal')
    PET = re.compile(r'positioned \^(-?[\d.]*) \^(-?[\d.]*) \^(-?[\d.]*)')

    def petal_ys(lines_at):
        """{tick: the petal's ^up} from the per-tick lines of seq/cs1 (k/<t>)."""
        out = {}
        for t, lines in lines_at.items():
            for ln in lines:
                if _sq.PETAL1 in ln and 'positioned ^' in ln:
                    m = PET.search(ln)
                    if m:
                        out[t] = float(m.group(2) or 0)
        return out
    # the built seq/cs1 carries the petal only with the kit (its prop): parse it there, else build cs1 with a stand-in prop
    built = {int(f.stem): f.read_text().splitlines() for f in (DP / 'data/rlk/function/boss/scarlet/seq/cs1/k').glob('*.mcfunction')}
    ys = petal_ys(built)
    src = 'the built seq/cs1'
    if not ys:
        _prop = _sq.K.prop
        _sq.K.prop = lambda *a, **k: 'function rlk:test/petal'
        try:
            class _CW:
                def __init__(self):
                    self.files = {}

                def w(self, rel, body):
                    self.files[rel] = body if isinstance(body, list) else str(body).splitlines()
            _cw = _CW()
            next(s_ for s_ in _sq.SERVICES if s_.name == 'cs1').build(_cw)
        finally:
            _sq.K.prop = _prop
        ys = petal_ys({int(rel.rsplit('/', 1)[1]): body for rel, body in _cw.files.items() if rel.startswith('seq/cs1/k/')})
        src = 'seq.py built with a stand-in petal prop (the kit is not in this tree)'
    want_y = {E_P: H + .25, E_P + 12: H + .125, E_P + 20: H - .375}
    got_y = {t: ys.get(t) for t in want_y}
    check(f'couplings: the cs1 petal path follows the built head anchor (H {H:.2f} at cs1 114; y at {", ".join(map(str, want_y))} = '
          f'{", ".join(str(v) for v in got_y.values())} vs H + 0.25 / + 0.125 / - 0.375; {src})',
          all(got_y[t] is not None and abs(got_y[t] - w) <= .03 for t, w in want_y.items()), str(sorted(ys.items())[:24]))
    check(f'couplings: seq.S0 {_sq.S0} == api.ITEM_SWORD_SCALE == the manifest item_sword display scale',
          _sq.S0 == api.ITEM_SWORD_SCALE == MAN['item_sword']['display_scale'])
    check(f'couplings: seq.SWORD_R {_sq.SWORD_R} == ITEM_SWORD_LEN / 2 / ITEM_SWORD_SCALE', abs(_sq.SWORD_R - api.ITEM_SWORD_LEN / 2 / api.ITEM_SWORD_SCALE) <= .001)
else:
    skipped('couplings', 'retarget / dims')


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
