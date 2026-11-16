"""Sequences of the field-pattern author (stage 2; specs scratchpad mb3/spec S1_field_enter.md, S2_field_end.md,
S3_break_groggy_recover.md, S5_meter_hud.md): the field opening (the halo flip, the warp-out flash, the glitch, the
warp-in, the unfold, the banner's pebbles, the settle's gold streaks), the field's ambience while it holds, the
pack-up after an unbroken field, the break (역장 붕괴) -> groggy 200 t -> recover, and the first field's low-gravity
notice of the meter HUD.

Visual and audio only. The core keeps every mechanic of these sequences (the clocks and states, the clips, the
untargetable warp and the teleport, the meter protocol of fg_contract.md section 15, low gravity, the damage cut, the
hitboxes, the HUD lines) and calls one function here from each hook (the lines marked "[seq_f: field author]" in
core.py):

    services(): field_in TL   -> seq_f.field_in(g, tl)    fx lines on the field opening's clock (service 20)
    services(): field_out TL  -> seq_f.field_out(g, tl)   fx lines + the rig's look/idle at the clip's dock (service 22)
    field/opened              -> #fgCool SETTLE           the settle before the opening waves (spec S1 F2, Q10)
    field/close               -> look/idle only outside the pack-up (it moved to the dock, Q14)
    field/open                -> seq_f/unfold             (also the instant field of the tests and reloads)
    field/banner              -> seq_f/banner
    field/tick                -> seq_f/field/tick         (every module tick while #fgField >= 1)
    brk/begin                 -> seq_f/brk/start          (#fgT 0 of the break)
    brk/tick                  -> seq_f/brk/tick           (#fgT = the break clip tick)
    brk/burst                 -> seq_f/brk/burst
    groggy/begin              -> seq_f/groggy/begin
    groggy/tick               -> seq_f/groggy/tick        (#fgT 1..200)
    recover/begin             -> seq_f/recover/begin
    recover/tick (the flip)   -> seq_f/recover/flip

Every tick comes from the rig manifest (ev_or / clip_len with the stub's defaults), every height from its anchors
(api.rest_anchor / api.f_clip_anchor, defaults = the spec's numbers). Files: F:mboss/fieldgen/seq_f/** (written
through gen.w, owned by the module generator like every G: path). Butterfly lessons: the warp-out flash plays at the
rig's hide tick (spec S1 F1: no empty tick); the field has one lift-off flash (wave_drop's; with the stub rig the
pack-up's 0); no card at the player's eyes (PL-1: the pebbles at the feet, the flashes on the title line); a recipe and
its own single layers never play on the same event (FX-4).
"""
from . import api as A
from .api import CY, L, ev_or, clip_len, rest_anchor, f_clip_anchor, f_body_pos

SEQ = 'seq_f'
PLAYER = '@e[tag=rlk_body,limit=1]'
SETTLE = 40                     # field/opened: #fgCool before the opening waves (spec S1 F2, Q10)
STREAKS = (13, 28)              # the settle's gold streaks, ticks after the opening's end (opening clock 70 / 85)
CORE_H = A.CORE_FIELD_H         # 4.1


def ex(cond, line):
    """`line` under the execute sub-commands `cond` (merged when the line is an execute itself)."""
    if line.startswith('execute '):
        return f'execute {cond} {line[len("execute "):]}'
    return f'execute {cond} run {line}'


def h(y):
    return L.num(float(y), 3)


def at_y(y, line):
    return f'execute positioned ~ ~{h(y)} ~ run {line}'


def floor(line):
    return f'execute positioned ~ {CY} ~ run {line}'


def body_rot(pos, line):
    return f'execute rotated as @s rotated ~ 0 positioned {pos} run {line}'


def fn(rel):
    return f'function {A.NS}{SEQ}/{rel}'


def emit(g):
    from . import core as C                                  # the core's clock constants (already imported)
    field_fns(g, C)
    break_fns(g, C)


# =============================================================================================
# S1 the field opening (service 20; clock = warp_out tick, 34 + t = warp_in_field tick t)
def field_in(g, tl):
    """Register the opening's fx on the core's field_in TL (@s = body, at it)."""
    from . import core as C
    hide = ev_or('warp_out', 'hide', C.WARP_OUT - 1)
    halo = rest_anchor('cruise', 'halo', (0, rest_anchor('cruise', 'ring_centre', (0, 4.5, 0))[1] + 1.6, 0))[1]
    tl.at(0, body_rot(f'^ ^{h(halo)} ^', g.fx('halo_flip')), g.snd('halo_flip'))
    tl.at(6, g.sound('block.beacon.power_select', 0.8, 1.2))
    tl.at(hide, floor(g.fx('warp_out')), g.snd('warp_out'),
          'execute if entity @a[tag=player,distance=..8] run ' + g.khud('flash_white'))
    old = 'execute at @e[type=minecraft:marker,tag=rlk_mb_fg_fxw,limit=1] run '
    for t in range(C.WARP_OUT + 1, C.WARP_LEN, 5):          # 14 19 24 29: violet glitch over the old spot
        tl.at(t, old + g.fx('glitch'))
    tl.at(C.WARP_OUT + 3, old + g.snd('glitch'))
    folded = f_clip_anchor('warp_in_field', 'in', 'ring_centre', (0, 5.8, 0))[1]
    tl.at(C.WARP_LEN, at_y(folded, g.fx('warp_in')), floor(g.fx('warp_pillar')), g.snd('warp_in'))
    for t in range(C.FIN_UNFOLD + 4, C.FIN_UNFOLD + 13, 4):    # 39 43 47: violet crackle under the unfolding core
        tl.at(t, at_y(CORE_H + 0.3, g.fx('field_idle')))
    field = C.WARP_LEN + ev_or('warp_in_field', 'field', 17)  # 51: the field form, link beams + the violet column
    me = f_body_pos(rest_anchor('field', 'medal_e', (3.85, 4.1, 0.0)))
    mg = f_body_pos(rest_anchor('field', 'medal_g', (-3.85, 4.1, 0.0)))
    if C.FIN_UNFOLD < field < C.FIN_LEN:
        tl.at(field, body_rot(me, g.fx('spark')), body_rot(mg, g.fx('spark')), g.sound('block.beacon.activate', 0.5, 0.7))


# =============================================================================================
# S2 the pack-up (service 22, clip field_end; the meter / low gravity / cut end at 0 in the core's field/close)
def field_out(g, tl):
    """Register the pack-up's fx on the core's field_out TL (@s = body at the centre); look/idle at the dock."""
    from . import core as C
    n = C.FOUT_LEN
    lances = C.FOUT_LANCES
    horiz = ev_or('field_end', 'horiz', min(40, n - 30))
    pack = C.FOUT_PACK
    dock = ev_or('field_end', 'dock', min(72, n - 6))
    packed = ev_or('field_end', 'packed', n - 2)
    assert 0 < lances < horiz < pack < dock < packed <= n, (lances, horiz, pack, dock, packed, n)
    zero = [g.snd('rise_hum')]
    if 'wave_drop' not in A.CLIPS:              # the field's one lift-off flash (wave_drop has it when the rig does)
        zero = [floor(g.fx('lift_off')), g.snd('lift_off'), g.snd('rise_hum')]
    tl.at(0, *zero)
    # the lances start out at `lances` (the pack-up sound) and reach 5.6 b by `horiz`, where they turn horizontal: the
    # sparks there, on the medallions in their X frames (the manifest's horiz anchors; fix round FID-9)
    me = f_body_pos(f_clip_anchor('field_end', 'horiz', 'medal_e', (5.6, 5.45, -0.175)))
    mg = f_body_pos(f_clip_anchor('field_end', 'horiz', 'medal_g', (-5.6, 5.45, -0.163)))
    tl.at(lances, g.snd('pack_up'))
    tl.at(horiz, body_rot(me, g.fx('spark')), body_rot(mg, g.fx('spark')), g.sound('block.chain.place', 0.6, 0.9))
    py = f_clip_anchor('field_end', 'pack', 'ring_centre', (0, 6.2, 0))[1]
    tl.at(pack, body_rot(f'^ ^{h(py)} ^', g.fx('pack_up')), g.snd('core_flip'))
    tl.at(pack + 10, g.sound('block.chain.step', 0.6, 0.7))
    dy = f_clip_anchor('field_end', 'dock', 'ring_centre', (0, 5.0, 0))[1]
    tl.at(dock, g.look('idle'), body_rot(f'^ ^{h(dy)} ^', g.fx('pack_up')), g.snd('revert'))
    tl.at(packed, g.sound('block.crafter.craft', 0.5, 1.1))
    return dock


# =============================================================================================
def field_fns(g, C):
    g.w(f'{SEQ}/unfold', [
        '# S1 the unfold (@s = body at the centre; field/open: the opening clock 35, the instant field of the tests):',
        '# the violet column grows under the core, tendrils, the springs and chains.',
        at_y(CORE_H + 0.7, g.fx('field_unfold')), g.snd('field_unfold')])
    g.w(f'{SEQ}/banner', [
        '# S1 the banner (@s = body; field/banner, low gravity from here): the first floating pebbles at the player\'s feet',
        '# (the kit\'s banner, icon and sound are the core\'s hud calls).',
        f'execute at {PLAYER} run ' + g.fx('pebbles')])
    note = C.BANNER_T + (C.FIN_BANNER - C.FIN_UNFOLD)        # #fgFirstT when the banner's 80 t hold ends
    assert note <= C.FIRST_T, (note, C.FIRST_T)             # the core's first-field clock must still be counting then
    g.w(f'{SEQ}/field/tick', [
        '# The field ambience (@s = body, every module tick while #fgField >= 1; frozen with the fight): pebbles at the',
        '# player\'s feet every 20 t while low gravity holds (never at the eyes; not during the waves: their fire bands,',
        '# three at once with the triple front, need the kit\'s card room, and a pebble card lives up to 66 t), the violet crackle under the core every',
        '# 20 t in the field form (not during the waves: their own fx), the field drone every 40 t, the settle\'s gold',
        f'# streaks {STREAKS[0]} / {STREAKS[1]} t after the opening (#fgCool from {SETTLE}), the first field\'s low-gravity notice',
        '# when the banner\'s hold ends (spec S5: what low gravity does).',
        'scoreboard players operation #fgM mb = #fgClk mb',
        'scoreboard players operation #fgM mb %= #fgK20 mb',
        f'execute if score #fgLowG mb matches 1 if score #fgM mb matches 0 unless score #fgPat mb matches 21 at {PLAYER} run '
        + g.fx('pebbles'),
        ex('if score #fgField mb matches 2..4 if score #fgM mb matches 10 unless score #fgPat mb matches 21',
           at_y(CORE_H, g.fx('field_idle'))),
        'scoreboard players operation #fgM mb = #fgClk mb',
        'scoreboard players operation #fgM mb %= #fgK40 mb',
        'execute if score #fgField mb matches 2..4 if score #fgM mb matches 20 run ' + g.snd('field_hum'),
        *[ex(f'if score #fgField mb matches 2 if score #fgPat mb matches 0 if score #fgCool mb matches {SETTLE - s + 1}',
             floor(g.fx('gold_streaks'))) for s in STREAKS],
        f'execute if score #fgFN mb matches 1 if score #fgFirstT mb matches {note} if score #fgLowG mb matches 1 run ' + g.khud('ab_lowg')])


# =============================================================================================
# S3 the break (#fgT = the break clip tick), groggy (#fgT 0..200), recover (#fgT 0..15)
def break_fns(g, C):
    core0 = f_clip_anchor('break', 'bubble', 'core', (0, CORE_H, 0))[1]
    core5 = f_clip_anchor('break', 'burst', 'core', (0, CORE_H, 0))[1]
    corew = f_clip_anchor('break', 'wobble', 'core', (0, 3.5, 0))[1]
    slump = f_clip_anchor('break', 'slumped', 'core', (0, 2.5, 0))[1]
    # the break on the floor (fix round FID-1: #fgBrkLo 1, the rig's break_low): the same fx at its own core heights
    low = C.BRK_LOW
    lcore0 = f_clip_anchor(low, 'bubble', 'core', (0, 1.3, 0))[1] if low else core0
    lcore5 = f_clip_anchor(low, 'burst', 'core', (0, 1.3, 0))[1] if low else core5
    lcorew = f_clip_anchor(low, 'wobble', 'core', (0, 2.1, 0))[1] if low else corew

    def by(hi, lo_h, line_at):
        """line_at(h) under the break variant: the hover break at hi, break_low at lo_h (one line when equal)."""
        if not low or abs(hi - lo_h) < 0.05:
            return [line_at(hi)]
        return [ex('unless score #fgBrkLo mb matches 1', line_at(hi)), ex('if score #fgBrkLo mb matches 1', line_at(lo_h))]
    rec = f_clip_anchor('recover', 'flip', 'core', (0, 3.3, 0))[1]
    ring = f_clip_anchor('recover', 'flip', 'ring_centre', (0, 4.2, 0))[1]
    spark_t = C.BRK_WOBBLE + 10
    assert C.BRK_BURST < C.BRK_WOBBLE < spark_t < C.BRK_LEN, (C.BRK_BURST, C.BRK_WOBBLE, C.BRK_LEN)
    g.w(f'{SEQ}/brk/start', [
        '# S3 break 0 (@s = body; brk/begin after the 20th count: the hazards, decals, banner and meter are gone): the',
        '# cracked bubble lights up white-gold (at the grounded core for break_low: FID-1).',
        *by(core0, lcore0, lambda y: at_y(y, g.fx('bubble_glow'))), g.snd('break_glow')])
    g.w(f'{SEQ}/brk/burst', [
        f'# S3 break {C.BRK_BURST}: the bubble bursts (crack 4 is the core\'s): the flash and the glass shards at the core, the gold',
        '# spark ring at the floor, the cracked-bubble pop and a gold flat on the title line.',
        *by(core5, lcore5, lambda y: at_y(y, g.fx('break_burst'))), floor(g.fx('break_ring')), g.khud('pop_break'),
        g.khud('flash_gold'), g.snd('break_burst')])
    g.w(f'{SEQ}/brk/tick', [
        f'# S3 the break clip (@s = body, #fgT 1..{C.BRK_LEN}): the metallic groan of the tilt and wobble ({C.BRK_WOBBLE}), a spark and',
        f'# a chain creak as it sinks ({spark_t}).',
        f'execute if score #fgT mb matches {C.BRK_WOBBLE} run ' + g.snd('groggy_wobble'),
        *by((corew + slump) / 2, (lcorew + slump) / 2, lambda y: ex(f'if score #fgT mb matches {spark_t}', at_y(y, g.fx('spark')))),
        f'execute if score #fgT mb matches {spark_t} run ' + g.sound('block.chain.step', 0.5, 0.6)])
    g.w(f'{SEQ}/groggy/begin', [
        '# S3 groggy 0 (@s = body; also a reload / test 40): the device has sunk low: the dust ring, the power-down.',
        floor(g.fx('sink_dust')), g.sound('block.beacon.deactivate', 0.8, 0.7)])
    g.w(f'{SEQ}/groggy/tick', [
        f'# S3 groggy (@s = body, #fgT 1..{C.GROGGY}): slow sparks drip from the slumped core every 40 t (spec Q17), two creaks.',
        'scoreboard players operation #fgM mb = #fgT mb',
        'scoreboard players operation #fgM mb %= #fgK40 mb',
        ex('if score #fgM mb matches 20', at_y(slump, g.fx('groggy_sparks'))),
        'execute if score #fgM mb matches 20 run ' + g.snd('groggy_spark'),
        *[f'execute if score #fgT mb matches {t} run ' + g.sound('block.anvil.place', 0.3, 0.5) for t in (40, 120) if t < C.GROGGY]])
    g.w(f'{SEQ}/recover/begin', [
        '# S3 recover 0 (@s = body): re-level; the gold ring flash and the clockwork (" · 그로기" stays to the recovery\'s',
        '# end: the core drops it in ai/enter).',
        at_y(rec, g.fx('recover')), g.snd('recover')])
    g.w(f'{SEQ}/recover/flip', [
        f'# S3 recover {C.REC_FLIP} (@s = body): the core flips to the top.',
        at_y(ring, g.fx('spark')), g.snd('core_flip')])
