"""Mantle hazards of 타키 (Tachy): the falling feathers and the nova of G2 과부하 외피 (PLAN §4.2 M, §5.2). OWNER: S4.

PATTERNS = [api.Pattern('mantle', 20, ('mantle_hold', 'mantle_nova'), build)]; build(W) writes only p/mantle/**:
  p/mantle/feather          one glowing feather falling 8 b onto the player's current spot in 16 t (a visual pj, dmg 0)
                            and the quiet disc(1.8) T1 Electro under it striking as it lands (tell 16: no floor decal,
                            the falling feather is the tell). The core (S3 mantle/tick) calls it every
                            api.G2_FEATHER_EVERY t with @s = the body; the spot is found here (the player's feet, y CY).
  p/mantle/nova/{start,tick,cancel}   the 44 t nova of the failure path on the core's #pt (0 at start, + 1 before tick):
                            swell 0-40 (wings white-gold, rising charge), flash at 40, at 44 hz/full #hzQuiet 1,
                            dash-dodgeable (no #hzNoDodge), #hzPm 400 per mille of the player's max HP, non-lethal
                            (#hzPmL 0), Electro. #done tk 1 at 45, the tick after the hit landed (the transition the core
                            starts on #done cannot swallow it).
  p/mantle/cancel           every feather and its hazard, the nova (any executor; idempotent).
  p/mantle/pj_end, nova/resume   for the core to wire (requests/s4.md): the feather's landing burst, the swell redraw.
The gauge, the timers, the aura alternation, the break / stun and the phase step are the core's (S3 mantle/**).
"""
from . import api
from . import s3lib as S
from .p_air import (CY, OBJ, NS, PL, BODY, L, fn, sset, prop_lines, snd, fx, part, stop_sounds, GOLD, WHITE,
                    SPARK, num, AT_BODY)

KEY = 'mantle'
FEATHER, NOVA = api.HITS[KEY]
F_HR, F_SPD, F_LIFE = FEATHER[3]          # 1.8 b, 0.5 b/t, 16 t
F_H = F_SPD * F_LIFE                      # 8 b
NOVA_CLIP = 'mantle_nova'
SWELL, FLASH, HIT = (api.ev(NOVA_CLIP, e) for e in ('swell', 'flash', 'hit'))
NOVA_END = HIT + 1


def hz_tag_lines(extra=None):
    out = [f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run '
           f'function {NS}p/mantle/hz_tag']
    if extra:
        out.append(f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add {extra}')
    return out


def build(W):
    assert F_LIFE >= api.TELL_MIN and abs(F_H - 8.0) < 1e-6, (F_LIFE, F_H)
    assert FEATHER[4] == api.FEATHER_TIER and FEATHER[5] == api.ELECTRO and NOVA[2] == 'full' and NOVA[5] == api.ELECTRO
    W.w('p/mantle/hz_tag', ['# @s = a mantle hazard just made: the pattern tags (p/mantle/cancel kills it).',
                            f'tag @s add {api.TAGS["pat"]}', f'tag @s add {S.tag_p(KEY)}', f'tag @s add {api.TAGS["air"]}'])
    # ---------------------------------------------------------------------------------------------- feathers
    disc = (L.hz_opts(quiet=1, sfx=0, el=api.ELECTRO)
            + [f'execute rotated 0 0 run {L.hz_disc(F_HR, F_LIFE, api.DMG[api.FEATHER_TIER])}'] + hz_tag_lines())
    W.w('p/mantle/feather', [
        f'# One mantle feather (@s = body, every {api.G2_FEATHER_EVERY} t of the mantle): it falls {num(F_H)} b onto the player\'s',
        f'# spot now in {F_LIFE} t; there the quiet disc {F_HR} {api.FEATHER_TIER} Electro strikes as it lands.',
        f'execute at {PL} positioned ~ {num(CY + F_H)} ~ rotated 0 90 run {fn("p/mantle/fall")}',
        f'execute at {PL} positioned ~ {CY} ~ run {fn("p/mantle/disc")}']
        + snd('feather_fall', f'at {PL} positioned ~ {num(CY + F_H)} ~'))
    W.w('p/mantle/fall', ['# The falling feather here (rotated straight down): a visual pj (dmg 0, no wall stop).']
        + prop_lines(KEY, 'feather', api.ELECTRO, 'rlk_tk_new')
        + [f'execute as @e[type=minecraft:item_display,tag=rlk_tk_new] run {fn("p/mantle/launch")}'])
    W.w('p/mantle/launch', ['# @s = the new feather display (rotated down).']
        + L.pj_opts(wall=0, shape=0) + [L.pj_launch(F_SPD, F_LIFE, 0, F_HR), 'tag @s remove rlk_tk_new'])
    W.w('p/mantle/disc', ['# The feather\'s hit on the floor here (strikes in 16 t).'] + disc)
    W.w('p/mantle/pj_end', [
        '# A feather landed (@s = the prop, #pjEv 2): a small golden-lightning burst (the core wires it: requests/s4.md).',
        'execute unless score #pjEv mb matches 1..2 run return 0']
        + fx('impact', [part(SPARK, 0.8, 0.2, 0.8, 0.15, 24), part(GOLD, 0.6, 0.1, 0.6, 0, 10)], 'at @s', el=api.ELECTRO))
    # ---------------------------------------------------------------------------------------------- nova
    swell = fx('nova_swell', [], AT_BODY + ' positioned ~ ~1.4 ~', t=FLASH - SWELL)
    W.w('p/mantle/nova/start', [
        f'# Nova (G2 failure; @s = body, #pt tk 0): {NOVA_CLIP} {api.CLIPS[NOVA_CLIP][0]} t, the wings swell {SWELL}-{FLASH}, flash {FLASH},',
        f'# the whole-arena hit at {HIT} (dash-dodgeable, {api.NOVA_PM} per mille, non-lethal, Electro).',
        sset('#done', 0), api.play(NOVA_CLIP)] + swell + snd('nova_swell'))
    tick = [f'# Nova tick (#pt tk 1..{NOVA_END}).']
    if not swell:
        tick.append(f'execute if score #pt {OBJ} matches {SWELL + 1}..{FLASH - 1} run {fn("p/mantle/nova/glow")}')
        W.w('p/mantle/nova/glow', ['# The swell stand-in (@s = body): white-gold motes gathering on the wings.',
                                   f'execute {AT_BODY} positioned ~ ~1.4 ~ run {part(WHITE, 1.2, 0.9, 1.2, 0.02, 3)}',
                                   f'execute {AT_BODY} positioned ~ ~1.4 ~ run {part(GOLD, 0.9, 0.7, 0.9, 0, 2)}'])
    flash = fx('nova_flash', [part(WHITE, 0.6, 0.8, 0.6, 0.3, 40)], AT_BODY + ' positioned ~ ~1.4 ~')
    W.w('p/mantle/nova/flash', ['# The flash (the last 4 t).'] + flash)
    hz = (L.hz_opts(quiet=1, sfx=0, el=api.ELECTRO, pm=api.NOVA_PM, pm_lethal=0)
          + [f'execute at @s rotated 0 0 positioned ~ {CY} ~ run {L.hz_full(1, 1)}'] + hz_tag_lines('rlk_tk_nova'))
    W.w('p/mantle/nova/hz', ['# The nova hazard (strikes next tick).'] + hz)
    blast = (fx('shock_ring', [part(GOLD, 6.0, 0.2, 6.0, 0, 120)], 'at @s positioned ~ ~0.2 ~', r=200)
             + fx('nova_flash', [part(SPARK, 3.0, 1.5, 3.0, 0.4, 80)], AT_BODY + ' positioned ~ ~1.4 ~')
             + snd('nova_blast'))
    W.w('p/mantle/nova/blast', ['# The nova hit (the hazard strikes this tick).'] + blast)
    tick += [f'execute if score #pt {OBJ} matches {FLASH} run {fn("p/mantle/nova/flash")}',
             f'execute if score #pt {OBJ} matches {HIT - 1} run {fn("p/mantle/nova/hz")}',
             f'execute if score #pt {OBJ} matches {HIT} run {fn("p/mantle/nova/blast")}',
             f'execute if score #pt {OBJ} matches {NOVA_END}.. run {sset("#done", 1)}']
    W.w('p/mantle/nova/tick', tick)
    W.w('p/mantle/nova/cancel', ['# Nova cancel (any executor; idempotent): its hazard, the swell sounds.',
                                 'kill @e[type=minecraft:marker,tag=rlk_tk_nova]'] + stop_sounds())
    if swell:
        W.w('p/mantle/nova/resume', [
            '# Nova resume (the kit swell cards were cleared on pause): the swell for the rest of its time.',
            f'execute unless score #pt {OBJ} matches ..{FLASH - 1} run return 0',
            f'scoreboard players set #mantle_t {OBJ} {FLASH}',
            f'scoreboard players operation #mantle_t {OBJ} -= #pt {OBJ}',
            f'data modify storage {api.STORAGE} air.nova set value {{t:1}}',
            f'execute store result storage {api.STORAGE} air.nova.t int 1 run scoreboard players get #mantle_t {OBJ}',
            f'execute as {BODY} {AT_BODY} positioned ~ ~1.4 ~ run function {NS}fx/p/nova_swell with storage {api.STORAGE} air.nova'])
    W.w('p/mantle/cancel', ['# Every mantle hazard (any executor; idempotent): the feathers, their discs, the nova.',
                            f'kill @e[tag={S.tag_p(KEY)}]'] + stop_sounds())


PATTERNS = [api.Pattern('mantle', S.TID['mantle'], ('mantle_hold', NOVA_CLIP), build,
                        notes='feathers every 36 t (core), the nova of the failure path')]
