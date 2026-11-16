"""Raiden (나루카미) hazard / FX kit v2: shared tables and the Python API pattern generators call (owner S1-KIT,
plan rd/plan.md B.0, B.3, D.1). build_raiden_hazards.py and build_raiden_hazard_vfx.py read the tables; the encounter
generators (raiden_enc/*, build_raiden_illusions.py, ...) emit commands with hz() / decal() / fx() / snd().

HAZARD API v2 (B.0). A hazard is a marker tagged rlk_rd_hazard at a floor point with a frozen yaw. It hits at its
`tell` (rdWind) tick; it is quiet unless `decal` names a B.3 kind; at the hit a separate strike display is summoned
(every static hazard, quiet or not) and the decal is killed. Travelling kinds (sweep / slab / orb) launch at `tell`:
their cards are summoned TRAVEL_GAP ticks before they start moving and then receive ONE interpolation (translation and
scale linear in time); the server test uses the same speed, so no per-tick visual commands run. User 10-22 (the 7th
금강괴멸파 volley, three rings at once, was sometimes invisible): a client that gets a display's spawn and its
interpolated transformation before it has ticked that display once shows the END state at once (the rings sat out at
the wall, behind it); in the busiest tick of the fight (72 ring cards) the two packets could land in one client tick.
So the cards appear min(tell, gap) ticks before the launch and start to move gap ticks after their summon; a hazard
created less than `gap` ticks before its launch (every tell-1 hazard) shows its cards at the front of that later tick
(a lead of at most gap - 1 ticks, never a lag) and moves them over the rest of the travel.

    hz(kind, tell=.., dmg=.., <shape params>, <flags>)  ->  one command line (call it where the hazard should be:
                                                            `execute positioned .. rotated .. run ` + hz(..))
  kind        params (blocks / degrees / blocks per tick)            test
  disk        r                                                       horizontal distance <= r + tol
  annulus     r, rmin=0, half=180 (half angle about the yaw)          rmin - tol <= d <= r + tol, |angle| <= half
  rect        len, wid, off=0, yawoff=0                               off - tol <= forward <= off + len + tol, |side| <= wid/2 + tol
  to_wall     wid                                                     rect from the origin along the yaw to the arena wall
                                                                      (radius 24 about rlk_raiden_arena, len <= 47, fixed at creation)
  sweep       r0, v, band, half=180, reach=26                         front F = r0 + v * (age - tell): F - band - tol <= d <= F + tol
  slab        d0, v, w, depth=1, height=2.5, reach=24                 front F = d0 + v * t: F - depth - tol <= forward <= F + tol, |side| <= w + tol
  orb         d0, v, r, reach=24, y=0.8                               disk of radius r around forward = d0 + v * t
  follow      r, v, every=20, life                                    disk chasing the player at v b/t (from creation); a hit every `every` t from tell
  field       r, every=10, life                                       DoT disk, a hit every `every` t from tell while alive
  safe_dome   r                                                       outside the dome: fatal (player/die); inside: dmg
  flags: decal=None|'ring'|'rings3'|'disc_pale'|'band'|'pool'|'aura'  dlife=0 (decal killed at age dlife, else at the hit)
         nododge (dash i-frames ignored), jump (vertical band -0.5..+0.75), kb=<blocks> (push away from the origin through
         the engine knock-back path; never a tp), lift (kb +2 steps; the engine has no vertical push), hits=n (max hits,
         0 = unlimited; default 1, follow / field 0), every=t, detached (survives hazard/finish), group (all hazards of the current group share one
         hit: call hz_group() first), tol=0.3, strike=None|'burst'|'bolt'|'arc'|'slash'|'wall'|'field'|'none', sound,
         wave=None|'/'|'\\'|'-' (slab only, rd-sync: the card is a crescent sword wave of light, its chord tilted 45 deg
         rising to her left '/', to her right '\\' (as the player sees it: / and \\), or level '-', instead of the slab wall),
         sm=None|'lr'|'rl'|'chop'|'thrust'|'rise' (strike motion, rd-sync: the strike follows the swing that makes the hit:
         'lr' / 'rl' sweeps into place from her left / right side of the hazard's yaw (SM_SWEEP degrees, the blade's trail),
         'chop' drops in from above, 'thrust' runs out from the origin along the yaw, 'rise' grows up from the floor)

FX CUES (D.1): fx(cue) -> `function rlk:boss/raiden/fx/<cue>` plays the cue's vanilla sound recipe (SOUNDS) and, for
the cues below, summons timed cards (they need no cleanup; `kill @e[tag=rlk_rd_fx]` clears them):
  star (4-point star + 1 b ring flash), blink_out / blink_in, switch_hoop / switch_burst (27 / 28; the vortex is the rig prop),
  bolt / bolt_big (sky bolt + shock ring), crystal, parry (gold waist crescent), counter_cue (black line),
  guard_shatter (white-violet shatter burst + short white flash), guard_beam (soft gold light beam that comes down on
  her and is gone after 12 t; sg/stun_tick plays it 13 t into the guard-break stun), eye_spawn (cyan sky beam),
  eye_break, eye_blast, musou_slash,
  glaive_throw (pink beam), bomb (flash + ink), iai_charge, danjeol_halo, danjeol_column, clap_star, shadow_palm,
  vajra_pulse, mangeop_dome, mangeop_slash, mangeop_clash (the 만겁 katana meets the dome), transform_burst; with
  macro arguments: twirl {life} (polearm ring; call fx/snd/twirl_beat every 6 t), eye_glow {r,life} (cyan danger
  dome), crystal_line {len}, crystal_ring {r},
  musou_dark {life} / mangeop_tint {life} (whole-field tint, run at the arena centre). Every other SOUNDS key is a
  sound-only cue. snd(cue) plays only the recipe.
State decals (not hazards): decal('ring'|'rings3'|'disc_pale'|'band'|'pool'|'aura'|'stagger', r=.., life=..) ->
  fx/decal/d<k> {sx,sz,life} (tags rlk_rd_sdecal, rlk_rd_sdecal_<kind>; life 99999 = until killed); decal('tint',
  life=..) -> the whole-field tint card (24.6 b radius at the execution point; run it at the arena centre).

Runtime contract (rdsim reads it): rdShape = 20 + kind id; rdWind = tell; rdDamage; rdHLife; rdHId;
tags rlk_rd_quiet / rlk_rd_nododge / rlk_rd_jump / rlk_rd_detached / rlk_rd_lift; decal displays rlk_rd_decal +
rlk_rd_decal_<kind> with rdVId = rdHId; strike displays rlk_rd_strike; #rdNoDodge rd is 1 around a nododge hurt.
Lifecycle: function rlk:boss/raiden/hazard/finish kills every hazard that is not detached (call it from `finish`);
killing rlk_rd_hazard markers + hazard/vfx_world (as pause / transform_start / test do today) removes everything.
"""
import math

NS = 'rlk:boss/raiden/'
KINDS = {'disk': 1, 'annulus': 2, 'rect': 3, 'to_wall': 4, 'sweep': 5, 'slab': 6, 'orb': 7, 'follow': 8,
         'field': 9, 'safe_dome': 10}
SHAPE_BASE = 20                     # rdShape of a hazard = 20 + kind (1..14 were the release presets, removed in S3)
TRAVEL = (5, 6, 7)
ARENA_WALL_R = 24.0
SEG_DEG = 15                        # one ring segment card per 15 degrees (24 per full ring)
# ticks between a travelling hazard's card summon and their interpolation (module docstring; user 10-22): rings (24
# cards each, up to 72 in one tick) wait 3, the single-card slabs and orbs 2
TRAVEL_GAP = {'sweep': 3, 'slab': 2, 'orb': 2}

# B.3 decal kinds: id -> (tag kind, model, sizing).  'ring' resolves to the thin or the bold sprite by radius.
DECALS = {
    1: ('ring', 'dk_ring', 'radial'),
    2: ('ring', 'dk_ring_s', 'radial'),
    3: ('rings3', 'dk_rings3', 'radial'),
    4: ('disc_pale', 'dk_disc', 'radial'),
    5: ('band', 'dk_band', 'band'),
    6: ('pool', 'dk_pool', 'radial'),
    7: ('aura', 'dk_aura', 'radial'),
    8: ('ring', 'dk_stagger', 'radial'),
}
DECAL_IDS = {'ring': 1, 'ring_s': 2, 'rings3': 3, 'disc_pale': 4, 'band': 5, 'pool': 6, 'aura': 7, 'stagger': 8}
# Decals that open with the footage's spawn flash (the ring expands from 25 % over DECAL_INTRO ticks).
DECAL_INTRO = {1: 6, 2: 6, 3: 4, 8: 4}

# Strike visuals (summoned at the hit tick; life 10: flash, flicker, residue, fade). id -> (hot model, after model)
STRIKES = {
    1: ('burst', 'st_burst', 'st_burst_af'),
    2: ('bolt', 'st_bolt', 'st_burst_af'),
    3: ('arc45', 'st_arc45', 'st_arc45'),
    4: ('arc72', 'st_arc72', 'st_arc72'),
    5: ('arc112', 'st_arc112', 'st_arc112'),
    6: ('arc180', 'st_arc180', 'st_arc180'),
    7: ('slash', 'st_slash', 'st_slash_af'),
    8: ('wall', 'st_wall', 'st_slash_af'),
    9: ('field', 'st_field', 'st_field'),
}
STRIKE_IDS = {v[0]: k for k, v in STRIKES.items()}
STRIKE_YU = 8                       # strike models: 1 model y unit = 8 blocks (display scale y)
STRIKE_LIFE = 10
# Strike motions (rd-sync): the strike visual starts where the swing came from and reaches its final pose in its 3 t
# interpolation. id 0 = the plain expand.
STRIKE_MOTION = {'lr': 1, 'rl': 2, 'chop': 3, 'thrust': 4, 'rise': 5}
SM_SWEEP = 50                       # degrees the sweep strikes start off their centre line
# Crescent sword waves on slab hazards (rd-sync): rdHSv 2 / 3 / 4 = chord rising to her left (/ from the player),
# to her right (\), level. The crescent (tr_wave: the shallow wave_blade crescent, user 10-22j) is 1.9 * WAVE_R * the
# slab's half width from tip to tip, its centroid WAVE_Y up.
WAVES = {'/': 2, '\\': 3, '-': 4}
WAVE_R, WAVE_Y = 1.08, 2.6
# strike frames by remaining life (rdHLife counts down): colour (custom_model_data tint) or the after model
FLASH = {9: 0xC8B6EA, 8: 0xEDE4FF}
AFTER_AT, AFTER_TINT, FADE_AT, FADE_TINT = 7, 0xA898D8, 4, 0x6A5A98
# cue cards with a second stage (card(..., s2=...), tag rlk_rd_fxb) start it with this many ticks of life left
FX2_AT = 6


# D.1 vanilla sound recipes: cue -> [(event, volume, pitch)] (every id is in the 26.3 sound_event registry; the kit
# test checks them against S:rd/tests/sound_ids.txt).
SOUNDS = {
    'star': [('block.amethyst_block.resonate', 1.0, 1.6), ('entity.firework_rocket.twinkle', 0.7, 1.4)],
    'blink_out': [('entity.enderman.teleport', 0.8, 1.4)],
    'blink_in': [('entity.illusioner.mirror_move', 0.9, 1.2)],
    'twirl': [('entity.player.attack.sweep', 0.9, 1.0), ('item.trident.riptide_1', 0.6, 1.6)],
    'twirl_beat': [('entity.player.attack.sweep', 0.8, 1.1)],
    'switch_hoop': [('block.respawn_anchor.charge', 1.0, 1.2)],
    'switch_burst': [('entity.lightning_bolt.impact', 1.0, 1.0), ('block.beacon.activate', 0.9, 1.5)],
    'bolt': [('entity.lightning_bolt.impact', 0.8, 1.2)],
    'bolt_big': [('entity.lightning_bolt.impact', 1.0, 1.0), ('entity.lightning_bolt.thunder', 0.5, 1.4)],
    'crystal': [('block.amethyst_cluster.break', 1.0, 1.0), ('block.glass.break', 0.6, 1.3)],
    'parry': [('item.shield.block', 1.0, 1.4)],
    'counter_cue': [('block.anvil.land', 0.4, 2.0)],
    'guard_shatter': [('block.glass.break', 1.0, 0.8)],
    'guard_beam': [('block.beacon.power_select', 0.9, 1.2)],
    'eye_spawn': [('block.beacon.activate', 1.0, 1.2)],
    'eye_glow': [('block.beacon.ambient', 1.0, 1.4)],
    'eye_break': [('block.amethyst_cluster.break', 1.0, 0.9)],
    'eye_blast': [('entity.generic.explode', 0.9, 1.4), ('entity.lightning_bolt.impact', 1.0, 1.0)],
    'musou_dark': [('entity.warden.sonic_charge', 1.0, 1.0)],
    'musou_slash': [('entity.warden.sonic_boom', 1.0, 1.0), ('entity.lightning_bolt.thunder', 0.8, 1.0)],
    'glaive_sweep': [('entity.player.attack.sweep', 1.0, 0.6), ('item.trident.throw', 0.7, 0.7)],
    'glaive_throw': [('item.trident.thunder', 0.8, 1.0)],
    'bomb_tell': [('block.respawn_anchor.charge', 0.9, 1.5)],
    'bomb': [('entity.generic.explode', 1.0, 1.0), ('entity.lightning_bolt.impact', 1.0, 1.0)],
    'iai_charge': [('block.beacon.power_select', 1.0, 1.6)],
    'iai_hit': [('entity.warden.sonic_boom', 1.0, 1.3)],
    'wave_slab': [('entity.breeze.wind_burst', 1.0, 1.4)],
    'wave_low': [('item.trident.riptide_3', 0.9, 0.7)],
    'danjeol_halo': [('block.beacon.activate', 1.0, 0.8)],
    'danjeol_column': [('entity.lightning_bolt.thunder', 0.5, 1.2)],
    'danjeol_band': [('block.respawn_anchor.set_spawn', 1.0, 1.2)],
    'danjeol_slam': [('entity.lightning_bolt.impact', 1.0, 1.0), ('entity.generic.explode', 1.0, 0.7)],
    'clap_summon': [('entity.evoker.prepare_summon', 1.0, 1.2)],
    'clap_star': [('block.amethyst_block.chime', 1.0, 2.0)],
    'clap': [('entity.iron_golem.attack', 1.0, 0.6), ('block.anvil.land', 0.7, 0.5)],
    'shadow_seed': [('entity.ender_eye.launch', 1.0, 1.0)],
    'shadow_loop': [('block.sculk.spread', 1.0, 1.0)],
    'shadow_tick': [('entity.lightning_bolt.impact', 0.3, 2.0)],
    'shadow_grow': [('block.sculk_shrieker.shriek', 0.9, 1.5)],
    'shadow_palm': [('entity.iron_golem.damage', 1.0, 0.5), ('entity.generic.explode', 0.9, 0.8)],
    'vajra_drive': [('block.anvil.land', 0.9, 0.6), ('entity.lightning_bolt.impact', 0.8, 1.0)],
    'vajra_current': [('block.beacon.ambient', 1.0, 1.8)],
    'vajra_pulse': [('block.conduit.attack.target', 1.0, 1.0)],
    'vajra_ring': [('entity.breeze.wind_burst', 1.0, 0.6)],
    'mangeop_vanish': [('entity.illusioner.mirror_move', 1.0, 0.6)],
    'mangeop_tint': [('block.beacon.deactivate', 1.0, 0.5)],
    'mangeop_flower': [('block.amethyst_block.resonate', 1.0, 1.0)],
    'mangeop_gauge': [('block.note_block.chime', 1.0, 1.0)],
    'mangeop_dome': [('block.beacon.power_select', 1.0, 1.6), ('block.glass.place', 1.0, 1.0)],
    'mangeop_slash': [('entity.lightning_bolt.thunder', 1.0, 1.0), ('entity.warden.sonic_boom', 1.0, 0.6)],
    'mangeop_shatter': [('block.glass.break', 1.0, 0.9), ('block.glass.break', 0.9, 1.1), ('block.glass.break', 0.8, 1.3)],
    # the 만겁 rift and arm (build_raiden_judgment_rig.mjs; the release's calamity sounds, d765bab)
    'mangeop_rift': [('block.beacon.ambient', 0.9, 0.5), ('block.glass.break', 0.6, 0.5)],
    'mangeop_void': [('block.portal.ambient', 0.9, 0.55), ('entity.wither.ambient', 0.6, 0.5)],
    # the katana strikes the dome (user 10-22h): a heavy blade-on-shield hit, the shell ringing under it
    'mangeop_clash': [('item.shield.block', 1.0, 0.5), ('block.anvil.land', 0.8, 0.55), ('entity.iron_golem.attack', 1.0, 0.6),
                      ('entity.generic.explode', 0.7, 0.75), ('block.amethyst_block.resonate', 0.9, 0.7)],
    'mangeop_crack': [('block.respawn_anchor.deplete', 0.6, 1.3), ('entity.iron_golem.damage', 0.6, 1.2)],
    'mangeop_close': [('block.beacon.deactivate', 0.8, 1.1)],
    'rush': [('item.trident.riptide_3', 1.0, 1.0)],
    'barrage': [('entity.player.attack.sweep', 1.0, 0.9), ('entity.player.attack.sweep', 0.9, 1.2)],
    'transform_ring': [('entity.lightning_bolt.thunder', 1.0, 1.0)],
    'transform_pillars': [('entity.wither.spawn', 0.4, 1.6)],
    'transform_burst': [('block.beacon.activate', 1.0, 1.0)],
}


def _f(x):
    s = f'{x:.4f}'.rstrip('0').rstrip('.')
    return s if s not in ('-0', '') else '0'


def _mb(x):
    return int(round(x * 1000))


_SIN = lambda deg: int(round(math.sin(math.radians(deg)) * 1000))
_COS = lambda deg: int(round(math.cos(math.radians(deg)) * 1000))


def arc_strike(half):
    return 'arc45' if half <= 50 else 'arc72' if half <= 80 else 'arc112' if half <= 130 else 'arc180'


def seg_count(half):
    """Ring segment cards for a sweep of half angle `half` (cards are SEG_DEG wide, centred on k * SEG_DEG)."""
    return 24 if half >= 180 else 2 * int(max(0, half - SEG_DEG / 2) // SEG_DEG) + 1


def hz_args(kind, tell, dmg, *, r=0.0, rmin=0.0, half=180.0, len=0.0, wid=0.0, off=0.0, r0=0.0, v=0.0, band=1.0,
            d0=0.0, w=0.0, depth=1.0, height=2.5, reach=None, y=0.8, every=10, hits=None, decal=None, dlife=0,
            nododge=False, jump=False, kb=0.0, lift=False, detached=False, group=False, life=None, strike=None,
            sound=True, tol=0.3, sm=None, wave=None):
    """Macro compound for hazard/new (all values integers: milliblocks, micro-blocks per tick for speeds)."""
    k = KINDS[kind]
    if hits is None:
        hits = 0 if kind in ('follow', 'field') else 1
    assert tell >= 1, 'tell >= 1 (the hit tick counts from the creation tick)'
    a = b = c = d = e = f = 0
    seg = 0
    travel = 0
    if kind == 'disk' or kind == 'field' or kind == 'follow' or kind == 'safe_dome':
        assert r > 0
        a = _mb(r)
        e = _mb(r + (0 if kind == 'safe_dome' else tol)) ** 2
    elif kind == 'annulus':
        assert r > rmin >= 0 and 0 < half <= 180
        a, b, c, d = _mb(rmin), _mb(r), _SIN(half), _COS(half)
        e, f = _mb(r + tol) ** 2, _mb(max(0.0, rmin - tol)) ** 2
    elif kind in ('rect', 'to_wall'):
        assert wid > 0 and (len > 0 or kind == 'to_wall')
        a, b, c = _mb(len), _mb(wid / 2), _mb(off)
    elif kind == 'sweep':
        assert v > 0 and band > 0
        reach = 26.0 if reach is None else reach
        a, b, c, d, e = _mb(r0), int(round(v * 1e6)), _mb(band), _SIN(half), _COS(half)
        travel = int(math.ceil((reach - r0) / v - 1e-9))
        seg = seg_count(half)
    elif kind == 'slab':
        reach = 24.0 if reach is None else reach
        a, b, c, d, e = _mb(d0), int(round(v * 1e6)), _mb(w), _mb(depth), _mb(height)
        travel = int(math.ceil(max(0.0, reach - d0) / v - 1e-9))
    elif kind == 'orb':
        reach = 24.0 if reach is None else reach
        a, b, c, e = _mb(d0), int(round(v * 1e6)), _mb(r), _mb(y)
        d = _mb(r + tol)
        travel = int(math.ceil(max(0.0, reach - d0) / v - 1e-9))
    if kind == 'follow':
        b = int(round(v * 1e6))
    if travel:
        f = travel                  # travelling kinds keep their travel ticks in F
    if life is None:
        assert kind not in ('follow', 'field'), f'{kind} needs life'
        life = tell + (travel + 1 if travel else 11)
    if strike is None:
        strike = {'disk': 'burst', 'annulus': arc_strike(half), 'rect': 'slash', 'to_wall': 'wall',
                  'field': 'field'}.get(kind, 'none')
    sv = 0 if strike == 'none' else STRIKE_IDS[strike]
    if kind in ('sweep', 'slab', 'orb'):
        sv = seg if kind == 'sweep' else 1
        if kind == 'slab' and wave:
            sv = WAVES[wave]
    dk = 0
    if decal:
        dk = DECAL_IDS[decal]
        if decal == 'ring':
            dk = 1 if max(r, rmin) >= 6 else 2
    kbsteps = 0
    if kb or lift:
        kbsteps = 3
        while 0.1 * kbsteps * (kbsteps + 1) / 2 < kb:
            kbsteps += 1
        kbsteps += 2 if lift else 0
    assert sm is None or sm in STRIKE_MOTION, sm
    # travelling cards: summoned at rel sp (= -min(tell, gap)), moving from rel go (= gap - min(tell, gap) >= 0)
    lead = min(tell, TRAVEL_GAP[kind]) if travel else 0
    sp, go = -lead, (TRAVEL_GAP[kind] - lead if travel else 0)
    return dict(k=k, a=a, b=b, c=c, d=d, e=e, f=f, tol=_mb(tol), tell=tell, dmg=dmg, life=life, ev=max(1, every),
                max=hits, grp=1 if group else 0, dk=dk, dl=dlife, kb=kbsteps, sv=sv, sm=STRIKE_MOTION.get(sm, 0),
                go=go, sp=sp, snd=1 if sound else 0,
                nd=1 if nododge else 0, jp=1 if jump else 0, det=1 if detached else 0, lf=1 if lift else 0,
                fv=_f(v) if kind == 'follow' else '0')


def hz(kind, tell, dmg, yawoff=0, **kw):
    """One command: `function rlk:boss/raiden/hazard/new {...}` (prefixed with `execute rotated ~yawoff 0` if needed)."""
    args = hz_args(kind, tell, dmg, **kw)
    body = ','.join(f'{k}:{v}' for k, v in args.items())
    cmd = f'function {NS}hazard/new {{{body}}}'
    return f'execute rotated ~{_f(yawoff)} 0 run {cmd}' if yawoff else cmd


def hz_group():
    """Start a new hit-sharing group: every following hz(..., group=True) joins it until the next hz_group()."""
    return f'scoreboard players add #rdGrpSerial rd 1'


def decal(kind, r=1.0, life=40, wid=None, len=None):
    """A free-standing decal (not a hazard): state markers (stagger ring, guard aura, vajra base ring) or the
    whole-field tint. Killed by its life (ticks) or by `kill @e[tag=rlk_rd_sdecal_<kind>]`."""
    if kind == 'tint':
        return f'function {NS}fx/decal/tint {{life:{life}}}'
    dk = DECAL_IDS[kind]
    if kind == 'ring':
        dk = 1 if r >= 6 else 2
    sx = wid if wid is not None else r
    sz = len if len is not None else r
    return f'function {NS}fx/decal/d{dk} {{sx:{_f(sx)},sz:{_f(sz)},life:{life}}}'


def fx(cue, **macro):
    """A D.1 cue (visual + its sound recipe): `function rlk:boss/raiden/fx/<cue>` (run it at the cue's spot)."""
    if macro:
        return f'function {NS}fx/{cue} {{' + ','.join(f'{k}:{v}' for k, v in macro.items()) + '}'
    return f'function {NS}fx/{cue}'


def snd(cue):
    """Only the sound recipe of a cue: `function rlk:boss/raiden/fx/snd/<cue>`."""
    assert cue in SOUNDS, cue
    return f'function {NS}fx/snd/{cue}'
