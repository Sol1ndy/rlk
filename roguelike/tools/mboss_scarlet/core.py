"""Core of the 홍련 (Scarlet) module (OWNER: S3; plan S:hr/PLAN.md §3.0, §3.8, §4.6, §5, §6.6-6.7, §7.3; contract
S:hr/contract.md §3): the 17 hooks + test/help, init (objective hr), the phase machine intro -> P1 -> CS1 -> SQ1 -> A8 ->
(deflect) CS2 -> down -> kipup -> P2 | (fail) fail-60 -> P2 -> (5 %) lead_stand / lead_down -> A13 -> (deflect) CS3 ->
the kill -> death (CS4 + the event coda) | (fail) the instant death -> (revive) A13 again; the floors, the invulnerable
windows, the counter cinematic's HP steps (#sq_sig), the down window, the look requests (#hrLook), the decor props, the
HUD (the under bar, the intro's skip prompt + input), pause / resume / reload / cleanup per PLAN §3.8 / §5.6, the kit
wiring (contract §3.3), the tests; the stand-ins while another stage's files are missing: rig_stub/** (S2a), the
sequences core/sq/** (S2b) and the gauntlets core/gs/** (S4).

#ph = api.PH. #pat = a running pattern (s3lib.TID: P1 1-7, R1-R3 11-13, the gauntlets 21 / 27), else 0. #sqn = the running
sequence (s3lib.SEQ_ID, index of api.SEQS + 1) on the clock #sq (0 at its start, + 1 before each tick); #sqdone 1 ends it.
#gk = the gauntlet of the current chain (1 A8 / 2 A13; the counter cinematic's repel {at} and the lead_stand {g} follow it),
#gres its judge (1 deflect / 2 fail), #grs a gauntlet restart pending at resume (1 lead_stand {g}, 2 the revive wait, 3 the
judged deflect goes on to the counter cinematic; F1: 4 the judged A8 fail goes on to P2, 5 a lethal fail pending). #fl the reserved floor step (1 CS1, 2 the A13 lead-in), #flw the down
window's 40 t wait. #inv the core's invulnerable window (rlk_mb_inv = #inv or the ghost tag or A6 ticks 0-4: core/inv).
"""
import math

import help_lib as H

from . import api
from . import s3lib as S
from .s3lib import sset, fn, part, placed

L, K = api.L, api.K
OBJ = api.OBJ
NS = api.NS
CY = api.CY
PH = api.PH
TID = S.TID
GAUNT = api.GAUNTLETS
SEQ_FIGHT = ('cs1', 'lead60', 'repel', 'lead5', 'lead_re')     # sequences of the fight state (#mbSt 1)
INTRO_LEN = api.SEQ_LEN['intro']
TAGS_ALL = sorted(set(api.TAGS.values()))        # I1 (s3-5): S3's extra tags are in api.TAGS now


class Ctx:
    """What the build knows: the present patterns (S3's P1 + S4's), the S4 files written, the services (S2b's)."""

    def __init__(self, pats, w4, services):
        self.pats = {p.key: p for p in pats}
        self.present = sorted(self.pats, key=lambda k: TID[k])
        self.w4 = w4
        self.services = {s.name: s for s in services}

    def written(self, W, rel):
        return (api.L.FN / f'{api.ROOT}/{rel}.mcfunction').resolve() in W.out.written

    def pat_file(self, W3, key, rel):
        W = self.w4 if key in api.P2 else W3
        return self.written(W, f'p/{key}/{rel}')


def at_body(cmd):
    return f'execute as {S.BODY} at @s run {cmd}'


def seq(ctx, name, part_, args=None):
    """S2b's seq/<name>/<part> or the core stand-in core/sq/<name>/<part> (args: the macro args of start)."""
    base = f'seq/{name}/{part_}' if name in ctx.services else f'core/sq/{name}/{part_}'
    if args:
        return fn(base) + ' {' + ','.join(f'{k}:{v}' for k, v in args.items()) + '}'
    return fn(base)


def gcall(ctx, g, part_):
    """S4's gauntlet p/<g>/<part> or the core stand-in core/gs/<g>/<part>."""
    return fn(f'p/{g}/{part_}' if g in ctx.pats else f'core/gs/{g}/{part_}')


def yaw_to(a, b):
    """The Minecraft yaw that looks from point a to point b (x, z)."""
    return round(math.degrees(math.atan2(-(b[0] - a[0]), b[2] - a[2])) % 360, 2)


def look_req(look):
    """The look request line (api.arena_look: '' until S1K's theme exists)."""
    return [x for x in (api.arena_look(look),) if x]


def warn(on):
    return S.hud('warn', on=int(on))


def seat_gone():
    """The seat stone goes (V2, HR-52): re-looked `bare` first, so its bottle / cup (the kit's staying items) go with it in the
    same tick; the kit itself only checks for them every 10 t (they left its per-tick prop chain)."""
    tg = api.TAGS['deco_seat_rock']
    bare = K.prop('seat_rock', look='bare')
    return ([f'execute as @e[type=minecraft:item_display,tag={tg}] run {bare}'] if bare else []) + [f'kill @e[tag={tg}]']


def seq_hold(grs):
    """After the restarts of a paused / reloaded gauntlet (#grs 1 lead_stand, 3 repel; 2 = the revive stance, no sequence).
    I1 (s3-10): a sequence (re)started outside the module tick (resume runs before it in the same game tick, /reload before
    the next one) gets its clock held one tick (#sq -1): that module tick shows clip tick 0 at #sq 0 (the sequence contract:
    #sq = the shown clip tick) instead of running the start and its tick 1 before the first rig/tick. The /reload restarts
    of CS1 / SQ1 / the lead-ins hold it the same way (core/re/*)."""
    return [f'execute if score {grs} {OBJ} matches {v} run {sset("#sq", -1)}' for v in (1, 3)]


# F1 (HR-01 / HR-07, lead decisions 11-05): what a paused / reloaded gauntlet goes on with besides the restart (#grs 1) and
# the two judged windows (#grs 2 / 3): #grs 4 = the A8 fail was judged (ULT60_LETHAL false; its 500 per-mille hit landed)
# -> P2 at once; #grs 5 = a lethal gauntlet (A13 with ULT5_LETHAL, A8 with ULT60_LETHAL) was paused after its last
# counting cut's pip window closed (strike + 1) with pips left -> the fail stays pending and lands as soon as the player is
# back and alive (core/g/fail_now: the fatal -> the revive path); before that strike the restart rule (PLAN §3.8 / §5.6).
LETHAL = {g: bool(api.ULT60_LETHAL if g == 'a8' else api.ULT5_LETHAL) for g in GAUNT}
PEND_T = {g: max(c[2] for _t, _s, _cl, c in api.SCRIPTS[g] if c) + 1 for g in GAUNT}
PLAYER_BACK = ('if entity @a[tag=player,limit=1] unless entity @a[tag=player,scores={dead=1}] '
               'unless entity @a[tag=player,scores={rnDie=1..}]')


def grs_go(reload=False):
    """The resume / reload lines of #grs 4 and 5 (a reload applies the pending fail only when the player is back and
    alive; else #grs 5 waits for the framework's resume)."""
    out = []
    if not api.ULT60_LETHAL:
        out.append(f'execute if score #grs {OBJ} matches 4 run {fn("core/p2/from_fail")}')
    if any(LETHAL.values()):
        out.append(f'execute if score #grs {OBJ} matches 5 {PLAYER_BACK + " " if reload else ""}run {fn("core/g/fail_now")}')
    return out


def music_to(ph):
    """api.music(ph) unless that phase already plays (a replay of the same phase would restart the track)."""
    return f'execute unless score #mbMusPh mb matches {ph} run {api.music(ph)}'


def build(W, ctx):
    w = W.w
    present = ctx.present
    # ---------------------------------------------------------------------------------------------- init / vars
    w('init', ['# The module objective + constants (spawn, reload; idempotent). Removed by uninstall.',
               f'scoreboard objectives add {OBJ} dummy']
      + [sset(f'#c{c}', c) for c in S.CONSTS] + [sset('#cn1', -1), sset('#cn1000', -1000)])
    consts = {f'#c{c}' for c in S.CONSTS} | {'#cn1', '#cn1000'}
    w('core/vars', ['# Every core fake player to its fight-start value (spawn; never the event scores api.EV_FP).']
      + [sset(k, 0) for k in S.FP if k not in consts] + [sset('#skip', 0), sset('#hud', 1)])
    # ---------------------------------------------------------------------------------------------- spawn / setup
    seat = api.SEAT_POS
    yaw_moon = yaw_to(seat, api.MOON_POS)
    w('spawn', [
        '# Hook spawn (@s = the arena marker at C of hr_field, rotated as it). The body (mboss/body: husk scale 1.0, click',
        f'# shield 1.2 x 2.4, miniboss economy, rlk_mb_inv in the intro) sits on her rock {api.xyz(seat)}',
        '# facing the moon, her back to the player arriving at start (PLAN §3.1). The event scores are cleared (PLAN §7.3.1).',
        '# F2 round 1 (V2R-02): the boss bars off from her spawn on (fight_vars has just cleared #mbBarOff; with the',
        '# framework\'s start_go show guarded by it, CS0 never shows a bar; core/intro/begin repeats it, intro/done ends it).',
        f'execute positioned {api.xyz(seat)} rotated {L.num(yaw_moon)} 0 run function rlk:mboss/body',
        at_body(fn('core/setup')), api.bars(0)] + [sset(k, 0) for k in api.EV_FP])
    w('core/setup', ['# @s = the new body: module state, the floors, the rig (normal form, P1 look, the blade off), the decor props;',
                     '# she draws her own yellow warning tells: the framework\'s unparriable glint is off (#mbNpOwn mb 1, combat overhaul C).',
                     'scoreboard players set #mbNpOwn mb 1', fn('init'), fn('core/vars'), fn('core/floors'), api.rig('init'), api.rig('spawn'), fn('core/looks'),
                     fn('core/deco'), 'data modify storage rlk:mboss sub set value []'])
    w('core/looks', ['# The rig looks the module owns (form, phase, blade, state) for the current phase (@s = body; reload, tests).',
                     api.rig('look/form/normal'),
                     f'execute if score #ph {OBJ} matches ..{PH["p1"]} run {api.rig("look/phase/p1")}',
                     f'execute if score #ph {OBJ} matches {PH["cs1"]}.. run {api.rig("look/phase/p2")}',
                     api.rig('look/blade/off'), api.rig('state/normal')])
    w('core/floors', [f'# The HP floors (absolute) from her max HP (@s = body): #fl60 = {api.FLOOR_P1} per mille, #fl5 = {api.FLOOR_ULT}.']
      + S.pm_of('#fl60', '@s', 'mhpM', api.FLOOR_P1) + S.pm_of('#fl5', '@s', 'mhpM', api.FLOOR_ULT))
    deco(W)
    # ---------------------------------------------------------------------------------------------- the intro
    w('intro_tick', [
        f'# Hook intro_tick (@s = body, #mbT 1..; rlk_mb_inv): the intro (seq/intro or the stand-in, {INTRO_LEN} t) on #sq, the skip',
        '# input, the look requests; the fight at its end (#sqdone) or at the framework cap.',
        f'execute if score #mbT mb matches 1 run {fn("core/intro/begin")}',
        f'execute unless score #mbT mb matches 1 run scoreboard players add #sq {OBJ} 1',
        S.gate('unless score #mbT mb matches 1', seq(ctx, 'intro', 'tick')),
        f'execute if score #sq_sig {OBJ} matches 1.. run {sset("#sq_sig", 0)}',
        fn('core/skip'),
        f'execute if score #sqdone {OBJ} matches 1 run {fn("core/intro/done")}',
        f'execute if score #sq {OBJ} matches {INTRO_LEN + 2}.. run {fn("core/intro/done")}',
        fn('core/look'), api.rig('tick')])
    w('core/intro/begin', ['# Intro tick 0 (@s = body). F2 (HR-29): the boss bars off for CS0 (the original shows no HUD until control;',
                           '# core/intro/done brings them back).', sset('#ph', PH['intro']), sset('#sq', 0), sset('#sqdone', 0),
                           sset('#sq_sig', 0), sset('#sqn', S.SEQ_ID['intro']), sset('#skip', 0), sset('#inv', 1), api.bars(0),
                           seq(ctx, 'intro', 'start')])
    w('core/intro/done', [
        '# The intro is over (its end, the framework cap, a reload or a test; @s = body): the fight state, P1 with the 60 % floor,',
        '# the title / music 1 (the end state of the full intro), the skip prompt gone, the boss bars back (F2, HR-29: they fill',
        '# over the first 1.5 s of the fight, the bars hook).',
        'function rlk:mboss/intro_end',
        f'execute unless score #ph {OBJ} matches {PH["intro"]} run return 0',
        fn('core/skip_clear'), api.bars(1),
        sset('#ph', PH['p1']), sset('#sqn', 0), sset('#sq', 0), sset('#sqdone', 0), sset('#pat', 0), sset('#inv', 0),
        sset('#rp', 0), L.title(*api.TITLE), music_to(1), fn('core/floors'),
        f'scoreboard players operation #mbFloor mb = #fl60 {OBJ}',
        *seat_gone(),
        fn('ai/phase'), fn('core/looks'), fn('ai/rec_start'), sset('#rec', 20)])
    w('core/intro/reload', ['# /reload during the intro: straight to the end of E12 (standing, the sword drawn, the rock gone,',
                            '# the title shown, music 1).',
                            seq(ctx, 'intro', 'cancel'), fn('core/intro/done')])
    skip_files(W, ctx)
    # ---------------------------------------------------------------------------------------------- the fight tick
    w('tick', ['# Hook tick (@s = body, at it, fight state #mbSt 1): the phase machine, then the rig tick (the shown clip tick ==',
               '# the pattern / sequence clock).',
               f'execute if score #ph {OBJ} matches {PH["intro"]} run {fn("core/intro/done")}',
               fn('core/fight'), api.rig('tick')])
    amb1, amb2 = K.p('ambient_p1'), K.p('ambient_p2')
    w('core/fight', [
        '# One fight tick (@s = body): the module clock, the look requests, the floor, the state of the phase, the arena ambience,',
        '# invulnerability.',
        f'scoreboard players add #clk {OBJ} 1',
        fn('core/look'),
        f'execute if score #mbFloorHit mb matches 1 run {fn("core/floor_hit")}',
        f'execute if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run {fn("core/floor_hit")}',
        fn('core/state')]
      + ([fn('core/amb')] if amb1 and amb2 else [])
      + [f'execute if score #mbSt mb matches 1 run {fn("core/inv")}'])
    if amb1 and amb2:
        # I1b (request s1k-2; PLAN §6.3 / §6.4): the kit's arena ambience at each player on the module clock
        w('core/amb', [
            f'# The arena ambience (@s = body; PLAN §6.3 / §6.4): ambient_p1 every {AMB_EVERY[0]} t at each player in P1, ambient_p2',
            f'# every {AMB_EVERY[1]} t in P2, the down window and the gauntlets; none in a sequence (it stages its own effects).',
            f'scoreboard players operation #t {OBJ} = #clk {OBJ}',
            f'execute if score #ph {OBJ} matches {PH["p1"]} run return run {fn("core/amb1")}',
            f'execute if score #ph {OBJ} matches {PH["a8"]}..{PH["a13"]} unless score #ph {OBJ} matches {PH["cs2"]} '
            f'unless score #ph {OBJ} matches {PH["lead"]} run {fn("core/amb2")}'])
        w('core/amb1', [f'# ambient_p1 at each player every {AMB_EVERY[0]} t of the module clock (#t = #clk).',
                        f'scoreboard players operation #t {OBJ} %= #c{AMB_EVERY[0]} {OBJ}',
                        f'execute if score #t {OBJ} matches 0 at @a[tag=player] rotated ~ 0 run {amb1}'])
        w('core/amb2', [f'# ambient_p2 at each player every {AMB_EVERY[1]} t of the module clock (#t = #clk).',
                        f'scoreboard players set #t2 {OBJ} {AMB_EVERY[1]}',
                        f'scoreboard players operation #t {OBJ} %= #t2 {OBJ}',
                        f'execute if score #t {OBJ} matches 0 at @a[tag=player] rotated ~ 0 run {amb2}'])
    w('core/state', [
        '# The state of the phase (@s = body).',
        f'execute if score #rp {OBJ} matches 1 run return run {fn("core/replay/tick")}',
        f'execute if score #ph {OBJ} matches {PH["p1"]} run return run {fn("core/fp")}',
        f'execute if score #ph {OBJ} matches {PH["p2"]} run return run {fn("core/fp")}',
        f'execute if score #ph {OBJ} matches {PH["a8"]} run return run {fn("core/g/tick")}',
        f'execute if score #ph {OBJ} matches {PH["a13"]} run return run {fn("core/g/tick")}',
        f'execute if score #ph {OBJ} matches {PH["down"]} run return run {fn("core/down/tick")}',
        f'execute if score #rvw {OBJ} matches 1.. run return run {fn("core/revive/tick")}',
        f'execute if score #sqn {OBJ} matches 1.. run return run {fn("core/seq/tick")}'])
    w('core/inv', [
        '# rlk_mb_inv of the body (@s = body, after the state): the core window (#inv: CS1 -> CS2 / the A8 fail, the kipup, the',
        '# lead-ins -> CS4, the intro replay), the ghost form (rlk_hr_ghost, S4), A6 ticks 0-4; else hittable.',
        f'execute if score #inv {OBJ} matches 1.. run return run tag @s add rlk_mb_inv',
        f'execute if entity @s[tag={api.TAGS["ghost"]}] run return run tag @s add rlk_mb_inv',
        f'execute if score #pat {OBJ} matches {TID["a6"]} if score #pt {OBJ} matches {api.A6_TRIGGER["inv"][0]}..{api.A6_TRIGGER["inv"][1]} '
        f'run return run tag @s add rlk_mb_inv',
        'tag @s remove rlk_mb_inv'])
    w('core/floor_hit', [
        '# A hit reached the floor (#mbFloorHit, framework) or her HP sits on it (@s = body): the step is reserved for the next',
        '# decision (#fl 1 CS1 in P1, 2 the A13 lead-in in P2); in the down window lead_down follows 40 t later (#flw).',
        'scoreboard players set #mbFloorHit mb 0',
        f'execute unless score #fl {OBJ} matches 0 run return 0',
        f'execute if score #ph {OBJ} matches {PH["p1"]} run return run {sset("#fl", 1)}',
        f'execute if score #ph {OBJ} matches {PH["down"]} if score #kip {OBJ} matches 0 run {sset("#flw", api.DOWN_FLOOR_WAIT)}',
        f'execute if score #ph {OBJ} matches {PH["down"]} run return run {sset("#fl", 2)}',
        f'execute if score #ph {OBJ} matches {PH["p2"]} run {sset("#fl", 2)}'])
    # ---------------------------------------------------------------------------------------------- P1 / P2
    w('core/fp', [
        '# A fight-phase tick (P1 / P2; @s = body): the phase clock, AI samples, the triggers (A6, the counter, the flinch), then',
        '# the running pattern or the recovery. F1 (HR-04): while a floor step is reserved (#fl) neither trigger starts a move',
        '# (CS1 / the A13 lead-in come at the next decision; ai/phase drops the flags at the next fight phase).',
        f'scoreboard players add #ai_pht {OBJ} 1',
        f'scoreboard players operation #t {OBJ} = #clk {OBJ}',
        f'scoreboard players operation #t {OBJ} %= #c5 {OBJ}',
        f'execute if score #t {OBJ} matches 0 run {fn("ai/sample")}',
        f'execute if score #a6q {OBJ} matches 1 if score #fl {OBJ} matches 0 if function {NS}ai/a6 run return 0',
        f'execute if score #ctr {OBJ} matches 1 if score #pat {OBJ} matches 0 if score #fl {OBJ} matches 0 if function {NS}ai/counter run return 0',
        f'execute if score #flq {OBJ} matches 1 run {fn("core/flinch")}',
        f'execute if score #pat {OBJ} matches 1.. run return run {fn("core/pat_tick")}',
        f'execute if score #lock {OBJ} matches 1 run return 0',
        fn('ai/recover')])
    w('core/flinch', [f'# Every {api.COUNTER_TRIGGER["flinch_every"]}th hit taken in recovery: the flinch clip (6 t, no step).',
                      sset('#flq', 0), f'execute unless score #pat {OBJ} matches 0 run return 0', sset('#ai_fl', 6),
                      api.play('flinch')])
    w('core/hit_rec', [
        f'# A player hit on her while she recovers / idles (on_hit; scores only): the last 4 hit times (#h1..#h4); {api.COUNTER_TRIGGER["hits"]}',
        f'# in {api.COUNTER_TRIGGER["window"]} t -> the counter trigger (#ctr, resolved by the next fight tick); every {api.COUNTER_TRIGGER["flinch_every"]}th -> the flinch.',
        f'scoreboard players operation #h4 {OBJ} = #h3 {OBJ}', f'scoreboard players operation #h3 {OBJ} = #h2 {OBJ}',
        f'scoreboard players operation #h2 {OBJ} = #h1 {OBJ}', f'scoreboard players operation #h1 {OBJ} = #clk {OBJ}',
        f'scoreboard players add #hits {OBJ} 1',
        f'scoreboard players operation #t5 {OBJ} = #hits {OBJ}',
        f'scoreboard players set #t4 {OBJ} {api.COUNTER_TRIGGER["flinch_every"]}',
        f'scoreboard players operation #t5 {OBJ} %= #t4 {OBJ}',
        f'execute if score #t5 {OBJ} matches 0 run {sset("#flq", 1)}',
        f'execute if score #hits {OBJ} matches ..{api.COUNTER_TRIGGER["hits"] - 1} run return 0',
        f'scoreboard players operation #t5 {OBJ} = #clk {OBJ}',
        f'scoreboard players operation #t5 {OBJ} -= #h4 {OBJ}',
        f'execute if score #t5 {OBJ} matches ..{api.COUNTER_TRIGGER["window"]} run {sset("#ctr", 1)}'])
    pattern_files(W, ctx)
    phase_files(W, ctx)
    seq_runner(W, ctx)
    look_files(W)
    helper_files(W)
    hooks(W, ctx)
    tests(W, ctx)
    stand_in_seqs(W, ctx)
    stand_in_gauntlets(W, ctx)
    if not api.rig_real():
        rig_stub(W)


# ================================================================================================== decor props
# I1b (request s1k-2): the arena ambience period in P1 / in P2, the down window and the gauntlets (PLAN §6.3 / §6.4)
AMB_EVERY = (10, 6)
assert AMB_EVERY[0] in S.CONSTS
# I1b: the decor props' looks per arena look (PLAN §6.3 / §6.4 / §6.5 "kit props"; core/look/go re-looks them with the job)
DECO_LOOK = {'moon': ('p1', 'bud'), 'crimson': ('p2', 'bloom'), 'dark': ('off', 'bloom')}


def deco(W):
    """core/deco (spawn): the decor props of api.deco() through the kit (fx/prop/*), each an item_display summoned at its
    point, then rotated, then given its look; tag rlk_hr_deco + rlk_hr_deco_<name>. core/deco_re (reload): the moon halo
    and the lotus again in the look of the phase (the seat rock only belongs to the intro). Without the kit no prop.
    I1b verification round 2 (m1): the seat rock is summoned at exactly api.SEAT_POS (api.xyz), the point her body spawns on
    and the intro finds it at; the halo and the lotus keep their old form (the lotus points are never whole)."""
    d = api.deco()
    c = (api.CX, api.CY, api.CZ)
    tg = api.TAGS['deco']

    def one(name, pt, yaw, look, exact=False):
        cmd = K.prop(name, look=look)
        if not cmd:
            return []
        t = f'rlk_hr_deco_{name}'
        at = api.xyz(pt) if exact else f'{L.num(pt[0])} {L.num(pt[1])} {L.num(pt[2])}'
        return [f'summon minecraft:item_display {at} {{Tags:{S.tags_nbt(tg, t, "rlk_hr_dnew")}}}',
                f'execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] at @s run tp @s ~ ~ ~ {L.num(yaw)} 0',
                f'execute as @e[type=minecraft:item_display,tag=rlk_hr_dnew] run {cmd}',
                'tag @e[type=minecraft:item_display,tag=rlk_hr_dnew] remove rlk_hr_dnew']

    halo = d['moon_halo']
    yaw_halo = yaw_to(halo, c)
    # F2 (LF-01): the halo's point is whole (889 218 -33): written exactly (api.xyz), else the game puts it 0.5 b east and 0.5 b
    # further out (1.5 b in front of the moon disc instead of 1 b)
    lotus = []
    for i, p in enumerate(d['lotus']):
        lotus += one('lotus', p, (i * 47) % 360, 'bud')
    seat = d['seat_rock']
    seat_l = one('seat_rock', seat, yaw_to(seat, api.MOON_POS), 'bottle', exact=True)
    kill = [f'kill @e[type=minecraft:item_display,tag={tg}]']
    W.w('core/deco', ['# The decor props at spawn (PLAN §6.7): the moon halo (p1), 8 lotus buds, the seat rock (bottle).']
        + kill + one('moon_halo', halo, yaw_halo, 'p1', exact=True) + lotus + seat_l)
    bloom = []
    for i, p in enumerate(d['lotus']):
        bloom += one('lotus', p, (i * 47) % 360, 'bloom')
    W.w('core/deco_re', ['# The decor props after a /reload (aux entities are gone): the moon halo and the lotus of the phase (a',
                         '# look request then sets them to its look, core/look/go).']
        + kill + [S.gate(f'if score #ph {OBJ} matches ..{PH["p1"]}', x) for x in one('moon_halo', halo, yaw_halo, 'p1', exact=True) + lotus]
        + [S.gate(f'if score #ph {OBJ} matches {PH["cs1"]}..', x) for x in one('moon_halo', halo, yaw_halo, 'p2', exact=True) + bloom])
    W.w('core/deco_seat', ['# The seat rock again (the intro replay).'] + seat_gone() + seat_l)


# ================================================================================================== the skip
def skip_files(W, ctx):
    w = W.w
    lo, hi = api.SKIP_WINDOW
    prompt = []
    for s in range(api.SKIP_STEPS + 1):
        k = K.hud('skip', s=s)
        if k:
            prompt.append((s, [k]))
        else:
            # the actionbar stand-in while the kit is missing: the original's prompt verbatim + the control hint, the HUD held
            grey = ['#A8A8B0', '#BDBDC4', '#D0D0D6', '#E4E4E8', '#FFFFFF'][s]
            prompt.append((s, [f'title @a[tag=player] actionbar ["",{{text:"{api.SKIP_TEXT}",color:"{grey}"}},'
                               f'{{text:"{api.SKIP_HINT}",color:"{grey}"}}]',
                               'scoreboard players set @a[tag=player] hudHold 2']))
    clear = K.hud('skip', s=5) or 'title @a[tag=player] actionbar ""'
    rows = []
    for s, lines in prompt:
        a, b = (0, 0) if s == 0 else ((s - 1) * 5 + 1, s * 5 if s < api.SKIP_STEPS else api.SKIP_HOLD - 1)
        rows += [S.gate(f'if score #skip {OBJ} matches {a}..{b}', x) for x in lines]
    w('core/skip', [
        f'# The intro skip input (@s = body, every intro tick; PLAN §3.1): from {lo} to {hi} the prompt {api.SKIP_TEXT}{api.SKIP_HINT}',
        f'# (hudHold); holding sneak (rlk:in_sneak) brightens it in {api.SKIP_STEPS} steps of 5 t, a release resets the count;',
        f'# {api.SKIP_HOLD} t held -> the skip (seq/intro/skip, then #sq = {api.SKIP_T - 1}: the next tick plays intro_end from 0).',
        f'execute if score #skip {OBJ} matches ..-1 run return 0',
        f'execute if score #skp {OBJ} matches 1.. if score #sq {OBJ} = #skp {OBJ} run return run {fn("core/skip_go")}',
        f'execute if score #sq {OBJ} matches {hi + 1}.. run return run {fn("core/skip_clear")}',
        f'execute unless score #sq {OBJ} matches {lo}..{hi} run return 0',
        f'execute as {S.PL} if predicate rlk:in_sneak run scoreboard players add #skip {OBJ} 1',
        f'execute as {S.PL} unless predicate rlk:in_sneak run {sset("#skip", 0)}',
        f'execute if score #skip {OBJ} matches {api.SKIP_HOLD}.. run return run {fn("core/skip_go")}'] + rows)
    w('core/skip_go', ['# The skip (@s = body): the prompt gone, the sequence\'s skip (the black, the intro cleared, her E10 pose ≤ 7 b',
                       f'# from the player), then the clock jumps: the next tick is {api.SKIP_T} (intro_end 0, line 11).',
                       clear, sset('#skip', -1), sset('#skp', 0), seq(ctx, 'intro', 'skip'), sset('#sq', api.SKIP_T - 1)])
    w('core/skip_clear', ['# The skip prompt off for good (the window ended, the skip, the intro end).',
                          f'execute if score #skip {OBJ} matches ..-1 run return 0', clear, sset('#skip', -1)])


# ================================================================================================== patterns
def pattern_files(W, ctx):
    w = W.w
    present = ctx.present
    singles = [k for k in present if k not in GAUNT]
    pt = ['# The running pattern of a fight phase (@s = body): #pt + 1, p/<key>/tick, its end.', f'scoreboard players add #pt {OBJ} 1']
    for k in singles:
        pt.append(f'execute if score #pat {OBJ} matches {TID[k]} run {fn(f"p/{k}/tick")}')
    pt.append(f'execute if score #done {OBJ} matches 1 run {fn("core/pat_end")}')
    w('core/pat_tick', pt)
    for k in singles:
        start = [f'# Start {k.upper()} {api.PATTERN_NAMES[k]} (@s = body; the AI, the triggers, tests): the clock, the no-repeat memory, the',
                 '# cooldown of the fight phase.', fn('core/stop_move'), sset('#pat', TID[k]), sset('#pt', 0), sset('#done', 0),
                 sset('#hits', 0), f'scoreboard players operation #last2 {OBJ} = #last {OBJ}', sset('#last', TID[k])]
        for fp, ph in ((1, PH['p1']), (2, PH['p2'])):
            cd = api.COOLDOWN.get(k, {}).get(fp)
            if cd is not None:
                start += [f'execute if score #ph {OBJ} matches {ph} run scoreboard players operation #cd_{k} {OBJ} = #clk {OBJ}',
                          f'execute if score #ph {OBJ} matches {ph} run scoreboard players add #cd_{k} {OBJ} {cd}']
        if k == 'a6':
            for fp, ph in ((1, PH['p1']), (2, PH['p2'])):
                start += [f'execute if score #ph {OBJ} matches {ph} run scoreboard players operation #a6cd {OBJ} = #clk {OBJ}',
                          f'execute if score #ph {OBJ} matches {ph} run scoreboard players add #a6cd {OBJ} {api.A6_TRIGGER["cd"][fp]}']
            start.append('tag @s add rlk_mb_inv')
        start.append(fn(f'p/{k}/start'))
        w(f'core/start/{k}', start)
    for k in present:
        w(f'core/hz_tag/{k}', [f'# @s = a hazard of {k.upper()} just made: the pattern tags (its cancel kills it).',
                               f'tag @s add {api.TAGS["pat"]}', f'tag @s add {S.tag_p(k)}'])
    w('core/pat_end', [
        '# The pattern set #done (@s = body): the lock marker gone, on the floor, then the recovery (after A6: the decision',
        f'# at once, {api.A6_TRIGGER["next"]} t after the blink, with the far rule; PLAN §4.3).',
        sset('#done', 0), f'scoreboard players operation #dec {OBJ} = #pat {OBJ}', sset('#pat', 0), sset('#pt', 0),
        f'kill @e[type=minecraft:marker,tag={S.LOCK_T}]', fn('core/ground'),
        f'execute if score #dec {OBJ} matches {TID["a6"]} run {sset("#ai_ff", 1)}',
        f'execute if score #dec {OBJ} matches {TID["a6"]} run return run {fn("ai/decide")}',
        fn('ai/rec_start')])
    cd = ['# Cancel the running pattern / gauntlet (any executor; idempotent): its own cancel (hazards, markers, props, glide).']
    for k in present:
        cd.append(f'execute if score #pat {OBJ} matches {TID[k]} run {fn(f"p/{k}/cancel")}')
    for g in GAUNT:
        if g not in ctx.pats:
            cd.append(f'execute if score #pat {OBJ} matches {TID[g]} run {gcall(ctx, g, "cancel")}')
    w('core/cancel_d', cd)
    w('core/cancel_pat0', ['# Cancel the running pattern, no recovery (A6 interrupts a windup; @s = body).',
                           fn('core/cancel_d'), sset('#pat', 0), sset('#done', 0), sset('#pt', 0), fn('core/stop_move'),
                           f'kill @e[type=minecraft:marker,tag={S.LOCK_T}]', fn('core/ground')])
    w('core/cancel_pat', ['# Cancel the running pattern, then the recovery (reload, tests; @s = body).', fn('core/cancel_pat0'),
                          fn('ai/rec_start')])
    # Balance gauge (combat overhaul lane B, mboss_lib.BAL_HOOKS, registry "bal"; lane H rebuilds her on the new combat and
    # may replace this): the 100 t balance groggy knocks her on her back (clip down) and she kips up (kipup) in the last
    # KIPUP t, hittable all along (no #inv), then the recovery. Only in the fight phases (P1 / P2) from idle or a pattern
    # outside A6 (the blink) and the ghost forms; never with a floor step reserved, in a cutscene / sequence / replay /
    # revival wait, a gauntlet (A8 / A13), the down window, while invulnerable.
    kip = 20
    bal_pats = [0, 1, 2, 3, 4, 6, 7, 11, 12, 13]
    w('bal_ok', ['# @s = body: may the balance groggy start now?',
                 f'execute unless score #ph {OBJ} matches {PH["p1"]} unless score #ph {OBJ} matches {PH["p2"]} run return fail',
                 f'execute if score #rp {OBJ} matches 1.. run return fail',
                 f'execute if score #sqn {OBJ} matches 1.. run return fail',
                 f'execute if score #rvw {OBJ} matches 1.. run return fail',
                 f'execute if score #inv {OBJ} matches 1.. run return fail',
                 f'execute if score #fl {OBJ} matches 1.. run return fail',
                 'execute if entity @s[tag=rlk_hr_ghost] run return fail',
                 'execute if entity @s[tag=rlk_mb_inv] run return fail']
      + [f'execute if score #pat {OBJ} matches {i} run return 1' for i in bal_pats] + ['return fail'])
    w('bal_on', ['# @s = body: the pattern goes (no recovery yet), she falls on her back.',
                 fn('core/cancel_pat0'), api.play('down')])
    w('bal_tick', ['# @s = body, instead of the hook tick while groggy: the clock, the looks, the ambience, the rig (kipup at the end).',
                   f'scoreboard players add #clk {OBJ} 1', fn('core/look'), fn('core/amb'), fn('core/inv'),
                   f'execute if score @s grgT matches {kip} run {api.play("kipup")}',
                   api.rig('tick')])
    w('bal_off', ['# @s = body: the balance groggy is over: the recovery, then the AI.', fn('ai/rec_start')])


# ================================================================================================== phases
def phase_files(W, ctx):
    w = W.w
    # CS1 -> SQ1
    w('core/cs1/start', [
        '# CS1 (the next decision after the 60 % floor hit; @s = body): invulnerable until the end of CS2 / the A8 fail, cine',
        '# (every boss hit on the player refused) 0-213, the P1 hazards cancelled, the boss bars off (FN-f; the bars hook draws',
        '# nothing while #hud 0), the floor -> 5 %; the sequence cs1.',
        fn('core/cancel_d'), f'kill @e[tag={api.TAGS["pat"]}]', sset('#pat', 0), sset('#fl', 0), sset('#ph', PH['cs1']),
        sset('#inv', 1), 'tag @s add rlk_mb_inv', L.cine(True), api.bars(0), sset('#hud', 0),
        f'scoreboard players operation #mbFloor mb = #fl5 {OBJ}', fn('core/stop_move'), fn('core/ground'),
        fn('core/seq/cs1')])
    w('core/lead60/start', [
        '# lead60 tick 0 (CS1 ended, a reload in CS1 / lead60, tests; @s = body): cine off, the bars back with the shield 5/5',
        '# under them, the A8 chain (#gk 1; its fail is lethal only with ULT60_LETHAL: #warn).',
        L.cine(False), api.bars(1), sset('#hud', 1), fn('shield/arm'), sset('#ph', PH['lead60']), sset('#inv', 1),
        sset('#gk', S.GK['a8']), sset('#warn', int(api.ULT60_LETHAL)), fn('core/looks'), fn('core/seq/lead60')])
    # the gauntlets
    for g in GAUNT:
        w(f'core/g/start/{g}', [
            f'# {g.upper()} {api.PATTERN_NAMES[g]} from T0 (@s = body; SQ1 / a lead-in ended, tests): the gauntlet clock #pt, its judge',
            '# result cleared; invulnerable (the ghost body; only the scripted true damage passes).',
            fn('core/stop_move'), sset('#ph', PH[g]), sset('#gk', S.GK[g]), sset('#pat', TID[g]), sset('#pt', 0), sset('#done', 0),
            sset('#gres', 0), sset('#sqn', 0), sset('#inv', 1), 'tag @s add rlk_mb_inv',
            sset('#warn', int(api.ULT60_LETHAL if g == 'a8' else api.ULT5_LETHAL)), gcall(ctx, g, 'start')])
    gt = ['# A gauntlet tick (@s = body): #pt + 1, p/<g>/tick (or the stand-in), the pip windows (shield/tick), its end.',
          f'scoreboard players add #pt {OBJ} 1']
    for g in GAUNT:
        gt.append(f'execute if score #pat {OBJ} matches {TID[g]} run {gcall(ctx, g, "tick")}')
    gt += [fn('shield/tick'), f'execute if score #done {OBJ} matches 1 run {fn("core/g/end")}']
    w('core/g/tick', gt)
    w('core/g/end', [
        '# The gauntlet set #done (@s = body; S4: at REPEL_T after a deflect, at FAIL60_P2_T after the A8 fail): #gres decides.',
        '# A8: deflect -> CS2 (repel {at:60}); fail -> P2 (the fail-60 hit and g_reform were the gauntlet\'s). A13: deflect -> CS3',
        '# (repel {at:5}); fail (the instant death did not end the run) -> the revive stance -> A13 again. F1 (HR-06): a test\'s',
        '# forced fail (#pipoff, tests 23 / 29) applies to this one judge only.',
        sset('#done', 0), sset('#pat', 0), sset('#pt', 0), sset('#pipoff', 0),
        f'execute if score #gres {OBJ} matches 1 run return run {fn("core/repel/start")}',
        f'execute if score #gk {OBJ} matches {S.GK["a8"]} run return run {fn("core/p2/from_fail")}',
        fn('core/revive/start')])
    # the counter cinematic (CS2 / CS3)
    w('core/repel/start', [
        '# The counter cinematic (the judged deflect; @s = body): cine, invulnerable (only its scripted true damage passes), the',
        '# sequence repel {at:60} after A8 (CS2) / {at:5} after A13 (CS3); its HP steps come through #sq_sig.',
        fn('core/stop_move'), sset('#ph', PH['cs2']), f'execute if score #gk {OBJ} matches {S.GK["a13"]} run {sset("#ph", PH["cs3"])}',
        sset('#inv', 1), 'tag @s add rlk_mb_inv', L.cine(True), sset('#sqh', 0), sset('#gres', 0), fn('shield/off'),
        fn('core/seq/repel')])
    w('core/repel/end', [
        '# The counter cinematic ended (@s = body): cine off; CS2 -> the down window; CS3 -> the lethal true hit if its kick did',
        '# not land (it normally kills at 102: death_start took over before this).',
        L.cine(False),
        f'execute if score #ph {OBJ} matches {PH["cs3"]} run return run {fn("core/kill")}',
        fn('core/down/start')])
    w('core/kill', ['# The scripted kill (@s = body): true damage of her whole HP (Electro number): the kill -> death_start (CS4).',
                    f'scoreboard players set #mbTrueEl mb {api.ELEC}', 'function rlk:mboss/true_pct {pct:100}'])
    # the down window
    w('core/down/start', [
        f'# The down window after CS2 (@s = body): {api.DOWN_T} t on her back (clip down), normal damage, the under bar = the ticks',
        f'# left (gold); at its end the kipup ({api.KIPUP_T} t, invulnerable) -> P2 after {api.KIPUP_RECOVER} t; a hit reaching the',
        f'# 5 % floor -> lead_down {api.DOWN_FLOOR_WAIT} t later.',
        sset('#ph', PH['down']), sset('#sqn', 0), sset('#inv', 0), sset('#down', api.DOWN_T), sset('#flw', 0), sset('#kip', 0),
        sset('#fl', 0), api.play('down'),
        '# balance gauge (combat overhaul lane B): the down window refills it (a pending balance groggy is dropped)',
        'function rlk:bal/refill'])
    w('core/down/tick', [
        '# A down-window tick (@s = body): the kipup, the floor wait (lead_down at 0) or the timer.',
        f'execute if score #kip {OBJ} matches 1.. run return run {fn("core/kip/tick")}',
        f'execute if score #flw {OBJ} matches 1.. run scoreboard players remove #flw {OBJ} 1',
        f'execute if score #fl {OBJ} matches 2 if score #flw {OBJ} matches ..0 run return run {fn("core/lead/down")}',
        f'execute if score #fl {OBJ} matches 2 run return 0',
        f'scoreboard players remove #down {OBJ} 1',
        f'execute if score #down {OBJ} matches ..0 run {fn("core/kip/start")}'])
    w('core/kip/start', ['# The kipup (@s = body): invulnerable, the clip.', sset('#kip', api.KIPUP_T), sset('#down', 0),
                         sset('#inv', 1), 'tag @s add rlk_mb_inv', api.play('kipup')])
    w('core/kip/tick', [f'scoreboard players remove #kip {OBJ} 1',
                        f'execute if score #kip {OBJ} matches ..0 run {fn("core/p2/from_down")}'])
    # P2
    p2 = [sset('#ph', PH['p2']), sset('#sqn', 0), sset('#inv', 0), sset('#kip', 0), sset('#down', 0), sset('#flw', 0),
          sset('#pat', 0), sset('#gres', 0), fn('core/looks'), fn('ai/phase')]
    w('core/p2/from_down', ['# P2 after the kipup (@s = body): the P1 kit with the P2 recoveries + R1-R3, the 5 % floor kept.']
      + p2 + [fn('ai/rec_start'), sset('#rec', api.KIPUP_RECOVER)])
    w('core/p2/from_fail', [f'# P2 after the A8 fail (T + {api.FAIL60_P2_T}; @s = body): her HP unchanged, no counter, no down window.']
      + p2 + [fn('ai/rec_start'), sset('#rec', 1)])
    # the lead-ins
    for name, g, what in (('down', 'a13', 'lead5 (the 5 % floor reached in the down window)'), ('a13', 'a13', 'lead5 (the 5 % floor reached in P2)'),
                          ('re_a8', 'a8', 'lead_re {g:"a8"} (an A8 restart)'), ('re_a13', 'a13', 'lead_re {g:"a13"} (an A13 restart)')):
        sq = 'lead_re' if name.startswith('re_') else 'lead5'
        w(f'core/lead/{name}', [
            f'# The {what} -> {g.upper()} (@s = body): invulnerable to CS4 (A13) / CS2 (A8); the shield off until the refill beat',
            '# (#sq_sig refill -> shield/arm); the warning banner belongs to the sequence (when #warn: the gauntlet\'s fail is lethal).',
            fn('core/cancel_d'), f'kill @e[tag={api.TAGS["pat"]}]', sset('#pat', 0), fn('core/stop_move'), fn('core/ground'),
            sset('#ph', PH['lead']), sset('#gk', S.GK[g]), sset('#fl', 0), sset('#flw', 0), sset('#rvw', 0), sset('#kip', 0),
            sset('#inv', 1), 'tag @s add rlk_mb_inv', fn('shield/off'), L.cine(False),
            sset('#warn', int(api.ULT60_LETHAL if g == 'a8' else api.ULT5_LETHAL)),
            fn(f'core/seq/{sq}' + ('' if sq == 'lead5' else f'_{g}'))])
    w('core/revive/start', [
        f'# The instant death was survived (Ronova\'s revive; @s = body): the darkness lifted, she stands {L.num(api.REVIVE["dist"])} b from',
        f'# the player in her stance; {api.REVIVE["wait"]} t later lead_re {{g:"a13"}} -> A13 again (shield 5/5, the banner).',
        fn('core/cancel_d'), sset('#pat', 0), sset('#ph', PH['lead']), sset('#gk', S.GK['a13']), sset('#sqn', 0), sset('#inv', 1),
        'tag @s add rlk_mb_inv', fn('shield/off'), *warn(0), *look_req('crimson'), fn('core/stop_move'), fn('core/place8'),
        api.rig('look/form/normal'), api.play('idle2'), sset('#rvw', api.REVIVE['wait'])])
    w('core/revive/tick', ['# The revive stance (@s = body): she faces the player; lead_re {g:"a13"} when the wait ran out.',
                           'function rlk:mboss/mv/turn {max:10}', f'scoreboard players remove #rvw {OBJ} 1',
                           f'execute if score #rvw {OBJ} matches ..0 run {fn("core/lead/re_a13")}'])


# ================================================================================================== sequences
def seq_runner(W, ctx):
    w = W.w

    def start(name, args=None, sfx=''):
        return [f'# The sequence {name}{" " + str(args) if args else ""} from tick 0 (@s = body).',
                sset('#sqn', S.SEQ_ID[name]), sset('#sq', 0), sset('#sqdone', 0), sset('#sq_sig', 0), seq(ctx, name, 'start', args)]
    for name in ('cs1', 'lead60', 'lead5', 'ending', 'event'):
        w(f'core/seq/{name}', start(name))
    w('core/seq/repel', [f'# The counter cinematic by the chain: repel {{at:{S.AT_OF["a8"]}}} (CS2) / {{at:{S.AT_OF["a13"]}}} (CS3).',
                         f'execute if score #gk {OBJ} matches {S.GK["a13"]} run return run {fn("core/seq/repel_5")}',
                         fn('core/seq/repel_60')])
    for g in GAUNT:
        w(f'core/seq/repel_{S.AT_OF[g]}', start('repel', {'at': S.AT_OF[g]}))
        w(f'core/seq/lead_re_{g}', start('lead_re', {'g': f'"{g}"'}))
    tk = ['# A sequence tick of the fight state (@s = body): #sq + 1, seq/<name>/tick, its signal (#sq_sig, read right after the',
          '# tick), its end (#sqdone).', f'scoreboard players add #sq {OBJ} 1']
    for name in SEQ_FIGHT:
        tk.append(f'execute if score #sqn {OBJ} matches {S.SEQ_ID[name]} run {seq(ctx, name, "tick")}')
    tk += [f'execute if score #sq_sig {OBJ} matches 1.. run {fn("core/sig")}',
           'execute unless score #mbSt mb matches 1 run return 0',
           f'execute if score #sqdone {OBJ} matches 1 run {fn("core/seq/end")}']
    w('core/seq/tick', tk)
    w('core/seq/end', ['# A fight-state sequence ended (@s = body): the next step of the chain.',
                       sset('#sqdone', 0),
                       f'execute if score #sqn {OBJ} matches {S.SEQ_ID["cs1"]} run return run {fn("core/lead60/start")}',
                       f'execute if score #sqn {OBJ} matches {S.SEQ_ID["lead60"]} run return run {fn("core/g/start/a8")}',
                       f'execute if score #sqn {OBJ} matches {S.SEQ_ID["repel"]} run return run {fn("core/repel/end")}',
                       f'execute if score #gk {OBJ} matches {S.GK["a8"]} run return run {fn("core/g/start/a8")}',
                       fn('core/g/start/a13')])
    sig = ['# The sequence signal (@s = body, right after the tick that set it; api.SIG): repel hp1..hp3 -> the HP step of the',
           '# chain (api.COUNTER_PM per mille of mhpM, true damage; kill = true_pct 100), refill -> shield/arm. Reset to 0.',
           f'scoreboard players operation #t {OBJ} = #sq_sig {OBJ}', sset('#sq_sig', 0),
           f'execute if score #t {OBJ} matches {api.SIG["refill"]} run return run {fn("shield/arm")}',
           f'execute unless score #sqn {OBJ} matches {S.SEQ_ID["repel"]} run return 0',
           f'scoreboard players add #sqh {OBJ} 1']
    for g in GAUNT:
        at = S.AT_OF[g]
        for i, v in enumerate(api.COUNTER_PM[at]):
            sid = api.SIG[f'hp{i + 1}']
            cond = f'if score #gk {OBJ} matches {S.GK[g]} if score #t {OBJ} matches {sid}'
            sig.append(f'execute {cond} run return run {fn("core/kill") if v == "kill" else fn(f"core/hp/pm{v}")}')
    w('core/sig', sig)
    for v in sorted({v for vs in api.COUNTER_PM.values() for v in vs if v != 'kill'}):
        w(f'core/hp/pm{v}', [f'# A scripted HP step (@s = body): true damage of {v} per mille of her max HP (Electro number).']
          + S.pm_of('#mbTrue', '@s', 'mhpM', v, dst_obj='mb') + [f'scoreboard players set #mbTrueEl mb {api.ELEC}',
                                                                  'function rlk:mboss/true_hit'])


# ================================================================================================== look requests
def look_files(W):
    w = W.w
    go = ['# A pending look request (#hrLook = api.LOOK_ID; @s any): the arena\'s look job now (no job is running), unless the',
          '# arena already stands in that look (its stamp; a job drops the stamp when it starts, so a cut one runs again).',
          f'scoreboard players operation #lk {OBJ} = #hrLook {OBJ}']
    for look, i in api.LOOK_ID.items():
        job = api.look_job(look)
        if job:
            # V2 (HR-51, D6-02): a pause after a deflect judge / a /reload from CS1 on asked for crimson again on a crimson arena
            # and rewrote it cell for cell (4 slices, ~7.2 k commands); the decor re-look below stays unconditional
            stamp = f'{api.AID}@{api.ARENA["ver"]}:{look}'
            go.append(f'execute if score #hrLook {OBJ} matches {i} unless data storage rlk:mboss {{built_{api.AID}:"{stamp}"}} '
                      f'in minecraft:overworld run {job}')
    # I1b: the decor props follow the look (PLAN §6.3-6.5 "kit props"): the halo p1 / p2 / off, the lotus bud / bloom
    for look, i in api.LOOK_ID.items():
        for name, lk in (('moon_halo', DECO_LOOK[look][0]), ('lotus', DECO_LOOK[look][1])):
            c = K.prop(name, look=lk)
            if c:
                go.append(f'execute if score #hrLook {OBJ} matches {i} as @e[type=minecraft:item_display,'
                          f'tag={api.TAGS["deco_" + name]}] run {c}')
    go.append(sset('#hrLook', 0))
    w('core/look/go', go)
    w('core/look', ['# The look request (PLAN §6.6): started at the first tick with no arena job (#mbArBuild 0), so a pause or a',
                    '# reload inside a running job can no longer leave the arena in the wrong look.',
                    f'execute if score #hrLook {OBJ} matches 1.. unless score #mbArBuild mb matches 1.. run {fn("core/look/go")}'])


# ================================================================================================== helpers
def helper_files(W):
    w = W.w
    w('core/stop_move', ['# The body stops gliding (@s = body).', 'execute if entity @s[tag=rlk_mb_mv] run function rlk:mboss/mv/stop'])
    w('core/ground', ['# Back on the floor at once if airborne (a cancelled leap; @s = body): the spot below when mv/ok, else C.',
                      fn('core/stop_move'),
                      f'execute store result score #t {OBJ} run data get entity @s Pos[1] 100',
                      f'execute if score #t {OBJ} matches ..{CY * 100 + 4} run return 0',
                      f'execute at @s positioned ~ {CY} ~ if function rlk:mboss/mv/ok run return run tp @s ~ ~ ~',
                      f'execute positioned as {S.ARENA_M} positioned ~ {CY} ~ run tp @s ~ ~ ~'])
    w('core/clamp', ['# @s = a marker on the floor: 0.5 b toward the arena axis until mv/ok passes there (at most 60 steps; the',
                     '# guaranteed fallback is the axis itself).',
                     'execute if function rlk:mboss/mv/ok run return 1',
                     f'scoreboard players add #t4 {OBJ} 1', f'execute if score #t4 {OBJ} matches 60.. run return 0',
                     f'execute facing entity {S.ARENA_M} feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
                     f'execute at @s run {fn("core/clamp")}'])
    w('core/dash/probe', [
        '# Dash / leap / blink probe (@s = body, rotated as the direction): the marker rlk_hr_dp walks forward on the floor in',
        '# 0.5 b steps while the next spot passes mv/ok (inside MOVE_R, feet and head free), at most #t steps; #t2 = steps.',
        f'kill @e[type=minecraft:marker,tag={S.PROBE_T}]',
        f'execute positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(api.TAGS["pat"], S.PROBE_T)}}}',
        f'execute as {S.PROBE_M} run tp @s ~ ~ ~ ~ 0',
        sset('#t2', 0),
        f'execute as {S.PROBE_M} at @s run {fn("core/dash/step")}'])
    w('core/dash/step', ['# One probe step (@s = the probe marker, at / rotated as it).',
                         f'execute if score #t2 {OBJ} >= #t {OBJ} run return 0',
                         'execute positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0',
                         'tp @s ^ ^ ^0.5', f'scoreboard players add #t2 {OBJ} 1', f'execute at @s run {fn("core/dash/step")}'])
    d = L.num(api.REVIVE['dist'])
    w('core/place8', [f'# @s = body: to a floor point {d} b from the player (on the player -> her line, else pulled toward the axis',
                      '# until mv/ok passes), facing the player.',
                      'kill @e[type=minecraft:marker,tag=rlk_hr_pl8]',
                      f'execute at {S.PLAYER} facing entity @s feet rotated ~ 0 positioned ^ ^ ^{d} positioned ~ {CY} ~ run summon '
                      f'minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt("rlk_hr_pl8")}}}',
                      sset('#t4', 0), f'execute as @e[type=minecraft:marker,tag=rlk_hr_pl8,limit=1] at @s run {fn("core/clamp")}',
                      'execute positioned as @e[type=minecraft:marker,tag=rlk_hr_pl8,limit=1] run tp @s ~ ~ ~',
                      'kill @e[type=minecraft:marker,tag=rlk_hr_pl8]', 'function rlk:mboss/mv/face'])


# ================================================================================================== hooks
def hooks(W, ctx):
    w = W.w
    present = ctx.present
    w('on_hit', [
        '# Hook on_hit (@s = body inside combat/apply, before apply_mods; scores only): a skill / burst hit flags the A6 trigger',
        '# (#skillDmg tmp 1; resolved by the next fight tick), a hit while she recovers / idles feeds the counter trigger.',
        f'execute if score #skillDmg tmp matches 1 run {sset("#a6q", 1)}',
        f'execute if score #pat {OBJ} matches 0 if score #ph {OBJ} matches {PH["p1"]} run {fn("core/hit_rec")}',
        f'execute if score #pat {OBJ} matches 0 if score #ph {OBJ} matches {PH["p2"]} run {fn("core/hit_rec")}'])
    w('aux_hit', ['# Hook aux_hit: 홍련 has no aux objects (framework default).'])
    w('incoming', ['# Hook incoming (@s = body inside combat/apply_mods; the framework floor runs after it): no damage multiplier',
                   '# (res {"*":10} like every element; the down window takes normal damage, PLAN §3.5).'])
    w('hz_vis', ['# Hook hz_vis: her hazards are quiet (#hzQuiet 1) and she has no floor decal of any kind (PLAN §1.4).'])
    pj = ['# Hook pj_end (@s = a projectile prop, #pjEv; #pjKeep preset): the pattern that launched it, if it has a pj_end.']
    for k in present:
        if ctx.pat_file(W, k, 'pj_end'):
            pj.append(f'execute if entity @s[tag={S.tag_p(k)}] run return run {fn(f"p/{k}/pj_end")}')
    w('pj_end', pj)
    # pause / resume
    pause = ['# Hook pause (the fight froze: dead, reviving, a menu, no player; @s = body): the kit cards go; a pattern\'s own pause;',
             '# a running gauntlet is cancelled (hazards, discs, ghost, the banner off, the darkness lifted) and restarts at resume',
             '# through lead_stand {g} from T0 with 5/5 (PLAN §3.8 / §5.6); after its fatal: the revive stance; after a judged',
             '# deflect: the counter cinematic; after the judged A8 fail: P2 at once (#grs 4, F1 HR-01); a lethal gauntlet paused',
             '# past its last counting cut with pips left: its fail at the resume (#grs 5, core/g/fail_now, F1 HR-07).']
    pause += [x for x in (K.fixed('clear'),) if x]
    resume = ['# Hook resume (@s = body): a pattern\'s own resume; what a paused gauntlet left (#grs): its restart (1), the revive',
              '# stance (2), the counter cinematic (3), P2 after the judged A8 fail (4), the pending lethal fail (5, core/g/fail_now).']
    for k in present:
        if k not in GAUNT and ctx.pat_file(W, k, 'pause'):
            pause.append(f'execute if score #pat {OBJ} matches {TID[k]} run {fn(f"p/{k}/pause")}')
        if k not in GAUNT and ctx.pat_file(W, k, 'resume'):
            resume.append(f'execute if score #pat {OBJ} matches {TID[k]} run {fn(f"p/{k}/resume")}')
    pause.append(f'execute if score #pat {OBJ} matches {min(TID[g] for g in GAUNT)}.. run {fn("core/g/pause")}')
    resume += [f'execute if score #grs {OBJ} matches 1 if score #gk {OBJ} matches {S.GK["a8"]} run {fn("core/lead/re_a8")}',
               f'execute if score #grs {OBJ} matches 1 if score #gk {OBJ} matches {S.GK["a13"]} run {fn("core/lead/re_a13")}',
               f'execute if score #grs {OBJ} matches 2 run {fn("core/revive/start")}',
               f'execute if score #grs {OBJ} matches 3 run {fn("core/repel/start")}',
               *grs_go(), *seq_hold('#grs'), sset('#grs', 0)]
    w('pause', pause)
    w('resume', resume)
    gp = ['# A gauntlet paused (@s = body): cancelled now; what resume does (#grs). F1: the judged A8 fail -> P2 (4, HR-01);',
          '# a lethal gauntlet past its last counting cut with pips left -> the fail pending (5, HR-07); a test\'s forced fail',
          '# (#pipoff) ends here (HR-06). Already cancelled (a /reload while the pause lasts: core/re/g): the first pause\'s',
          '# #grs stands (the shield and the clock are gone by now).',
          f'execute if score #pat {OBJ} matches 0 run return 0',
          sset('#grs', 1),
          f'execute if score #gres {OBJ} matches 1 run {sset("#grs", 3)}',
          f'execute if score #gres {OBJ} matches 2 if score #gk {OBJ} matches {S.GK["a13"]} run {sset("#grs", 2)}']
    if not api.ULT60_LETHAL:
        gp.append(f'execute if score #gres {OBJ} matches 2 if score #gk {OBJ} matches {S.GK["a8"]} run {sset("#grs", 4)}')
    for g in GAUNT:
        if LETHAL[g]:
            gp.append(f'execute if score #gres {OBJ} matches 0 if score #gk {OBJ} matches {S.GK[g]} if score {api.PIPS_FP} {OBJ} '
                      f'matches 1.. if score #pt {OBJ} matches {PEND_T[g]}.. run {sset("#grs", 5)}')
    w('core/g/pause', gp + [sset('#pipoff', 0),
                            fn('core/cancel_d'), sset('#pat', 0), sset('#pt', 0), sset('#done', 0), fn('shield/off'), *warn(0),
                            *look_req('crimson'), fn('core/stop_move'), fn('core/ground'), api.rig('look/form/normal'),
                            f'tag @s remove {api.TAGS["ghost"]}'])
    if any(LETHAL.values()):
        fnow = ['# F1 (HR-07, lead decision 11-05): the pending fail of a lethal gauntlet (#grs 5: paused / reloaded after its last',
                '# counting cut with pips left; @s = body, the player back and alive): the gauntlet\'s fail now (p/<g>/fail: the',
                '# instant death staged, ult/fatal as the player; Ronova\'s revive applies), then what follows the fatal there: A13 ->',
                '# the revive stance (lead_stand -> A13 again); A8 (ULT60_LETHAL) -> lead_stand {g:"a8"} (its clock held one tick).',
                sset('#grs', 0)]
        for g in GAUNT:
            if not LETHAL[g]:
                continue
            fail = fn(f'p/{g}/fail') if ctx.pat_file(W, g, 'fail') else f'execute as {S.PL} run {api.shield("fatal")}'
            fnow.append(S.gate(f'if score #gk {OBJ} matches {S.GK[g]}', fail))
            if g == 'a13':
                fnow.append(f'execute if score #gk {OBJ} matches {S.GK[g]} run return run {fn("core/revive/start")}')
            else:
                fnow += [f'execute if score #gk {OBJ} matches {S.GK[g]} run {fn("core/lead/re_a8")}',
                         f'execute if score #gk {OBJ} matches {S.GK[g]} run {sset("#sq", -1)}']
        w('core/g/fail_now', fnow)
    # stop everything of the fight state
    cancels = []
    for name in api.SEQS:
        cancels.append(f'execute if score #sqn {OBJ} matches {S.SEQ_ID[name]} run {seq(ctx, name, "cancel")}')
    w('core/stop_all', ['# Every state of the fight stops (death, cleanup, tests; any executor): the pattern / gauntlet, the running',
                        '# sequence, the shield, the pattern hazards and markers, the glide.',
                        fn('core/cancel_d')] + cancels
      + [sset('#pat', 0), sset('#pt', 0), sset('#done', 0), sset('#sqn', 0), sset('#sqdone', 0), sset('#sq_sig', 0),
         sset('#rvw', 0), sset('#kip', 0), sset('#flw', 0), sset('#grs', 0), sset('#rp', 0), fn('shield/off'),
         f'kill @e[tag={api.TAGS["pat"]}]', f'kill @e[tag={api.TAGS["cut"]}]', f'kill @e[type=minecraft:marker,tag={S.LOCK_T}]',
         f'execute as {S.BODY[:-1]},tag=rlk_mb_mv] run function rlk:mboss/mv/stop'])
    w('death_start', [
        '# Hook death_start (@s = body; the lethal hit: the framework cleared its libraries, hid the bars, stopped the music):',
        '# every fight state stops, the kit cards go, cine off, the event roll (PLAN §7.3.1), the ending CS4 (seq/ending).',
        fn('core/stop_all')] + [x for x in (K.fixed('clear'),) if x] + [
        *warn(0), L.cine(False), 'scoreboard players set #mbFloor mb 0', sset('#ph', PH['death']), sset('#hud', 0),
        fn('ev/roll'), fn('core/stop_move'), fn('core/ground'), fn('core/seq/ending')])
    w('death_tick', [
        '# Hook death_tick (@s = body, #mbT 1.. until cur.death = H + 122): the ending on #sq; at its end (#sqdone, H) the event',
        '# coda seq/event starts in the same tick (PLAN §7.1.2).',
        f'scoreboard players add #sq {OBJ} 1',
        f'execute if score #sqn {OBJ} matches {S.SEQ_ID["ending"]} run {seq(ctx, "ending", "tick")}',
        f'execute if score #sqn {OBJ} matches {S.SEQ_ID["event"]} run {seq(ctx, "event", "tick")}',
        f'execute if score #sq_sig {OBJ} matches 1.. run {sset("#sq_sig", 0)}',
        f'execute if score #sqn {OBJ} matches {S.SEQ_ID["ending"]} if score #sqdone {OBJ} matches 1 run {fn("core/seq/event")}',
        fn('core/look'), api.rig('tick')])
    kills = [f'kill @e[tag={t}]' for t in TAGS_ALL if t != api.TAGS['ghost']] + \
        [f'tag @e[tag={api.TAGS["ghost"]}] remove {api.TAGS["ghost"]}']
    # F3 (HR-05): every fake player of objective hr goes, not only the core's (S.FP): the patterns' #<key>_*, the ghost
    # helpers' #g_* / #r2_*, the sequences' #sq_* (contract §2 prefixes) — the event scores api.EV_FP are kept through a
    # save / `reset * hr` / restore (the reward hook reads them after this; tmp holders <name>K, removed again), and
    # storage seq.* (seq.g of lead_stand) goes with core.*
    keep = [f'scoreboard players add {k} {OBJ} 0' for k in api.EV_FP] \
        + [f'scoreboard players operation {k}K tmp = {k} {OBJ}' for k in api.EV_FP]
    resets = keep + [f'scoreboard players reset * {OBJ}'] \
        + [f'scoreboard players operation {k} {OBJ} = {k}K tmp' for k in api.EV_FP] \
        + [f'scoreboard players reset {k}K tmp' for k in api.EV_FP]
    cl = ['# Hook cleanup (no executor; idempotent; won / cancel / defeat / map change): every state, hazard and marker of the',
          '# module, the kit cards and HUD, the rig, every rlk_hr_* entity, every fake player of objective hr (init / spawn make',
          '# them again) and storage core.* / seq.*. Never the event scores (api.EV_FP, saved around `reset *`) nor ev.*: the',
          '# reward hook reads them after this.',
          fn('core/stop_all')]
    for name in api.SEQS:
        cl.append(seq(ctx, name, 'cancel'))
    cl += [x for x in (K.fixed('clear'),) if x] + S.hud('clear') + warn(0) + [at_body(api.rig('kill'))] + kills + resets \
        + [f'data remove storage {api.STORAGE} core', f'data remove storage {api.STORAGE} seq']
    w('cleanup', cl)
    un = ['# Hook uninstall (no executor; every enabled module): the kit, the rig, every rlk_hr_* entity, objective hr (incl. the',
          '# event scores), storage rlk:hr.']
    un += [x for x in (K.fixed('uninstall'), api.rig('uninstall')) if x] + kills + [f'scoreboard objectives remove {OBJ}'] \
        + [f'data remove storage {api.STORAGE} {k}' for k in sorted(api.STORAGE_KEYS)]
    w('uninstall', un)
    # reload
    w('reload', [
        '# Hook reload (@s = body after /reload: the rig parts, hazards, markers, props and kit cards are gone; scores are kept).',
        '# PLAN §3.8: intro -> its end; CS1 -> SQ1 tick 0; SQ1 / a lead-in -> restarted from 0 (crimson first); a gauntlet -> as',
        '# pause (lead_stand {g}); CS2 / CS3 -> their end (the rest of the HP steps); down -> on with <= 100 t; a P1 / P2 pattern',
        '# -> cancelled + the recovery. (The death state never gets here: the framework finishes it at once.)',
        fn('init'), api.rig('init'), api.rig('spawn'), sset('#lock', 0), fn('core/deco_re'),
        f'execute if score #ph {OBJ} matches {PH["intro"]} run return run {fn("core/intro/reload")}',
        f'execute if score #ph {OBJ} matches {PH["death"]} run return 0',
        fn('core/looks'),
        f'execute if score #rp {OBJ} matches 1 run {fn("core/replay/end")}',
        f'execute if score #ph {OBJ} matches {PH["p1"]} if score #pat {OBJ} matches 1.. run {fn("core/cancel_pat")}',
        f'execute if score #ph {OBJ} matches {PH["p2"]} if score #pat {OBJ} matches 1.. run {fn("core/cancel_pat")}',
        f'execute if score #ph {OBJ} matches {PH["cs1"]}.. run {fn("core/re/look")}',
        f'execute if score #ph {OBJ} matches {PH["cs1"]} run return run {fn("core/re/cs1")}',
        f'execute if score #ph {OBJ} matches {PH["lead60"]} run return run {fn("core/re/lead60")}',
        f'execute if score #ph {OBJ} matches {PH["a8"]} run return run {fn("core/re/g")}',
        f'execute if score #ph {OBJ} matches {PH["a13"]} run return run {fn("core/re/g")}',
        f'execute if score #ph {OBJ} matches {PH["cs2"]} run return run {fn("core/re/repel")}',
        f'execute if score #ph {OBJ} matches {PH["cs3"]} run return run {fn("core/re/repel")}',
        f'execute if score #ph {OBJ} matches {PH["down"]} run return run {fn("core/re/down")}',
        f'execute if score #ph {OBJ} matches {PH["lead"]} run return run {fn("core/re/lead")}'])
    w('core/re/look', ['# After a reload from CS1 on: the crimson look requested again (a job cut by the reload is redone).']
      + look_req('crimson'))
    w('core/re/cs1', ['# /reload in CS1: its end state = lead60 tick 0 (crimson, phase p2, music 2, the bars shown).',
                      seq(ctx, 'cs1', 'cancel'), sset('#sqn', 0), music_to(2), fn('core/lead60/start'), sset('#sq', -1)])
    w('core/re/lead60', ['# /reload in lead60: lead60 again from tick 0 (the crimson look first).', seq(ctx, 'lead60', 'cancel'), sset('#sqn', 0),
                         fn('core/lead60/start'), sset('#sq', -1)])
    w('core/re/g', ['# /reload in a gauntlet: as a pause (cancelled, the darkness lifted), then at once its restart (F1: or P2 after',
                    '# the judged A8 fail; a pending lethal fail lands now when the player is back and alive, else at the resume).',
                    fn('core/g/pause'),
                    f'execute if score #grs {OBJ} matches 1 if score #gk {OBJ} matches {S.GK["a8"]} run {fn("core/lead/re_a8")}',
                    f'execute if score #grs {OBJ} matches 1 if score #gk {OBJ} matches {S.GK["a13"]} run {fn("core/lead/re_a13")}',
                    f'execute if score #grs {OBJ} matches 2 run {fn("core/revive/start")}',
                    f'execute if score #grs {OBJ} matches 3 run {fn("core/repel/start")}', *grs_go(reload=True), *seq_hold('#grs'),
                    (f'execute unless score #grs {OBJ} matches 5 run {sset("#grs", 0)}' if any(LETHAL.values()) else sset('#grs', 0))])
    rest = ['# /reload in the counter cinematic: its end (the HP steps it had not applied yet, then CS2 -> the down window, CS3 ->',
            '# the lethal hit -> CS4).', seq(ctx, 'repel', 'cancel'), sset('#sqn', 0), L.cine(False)]
    for g in GAUNT:
        for i, v in enumerate(api.COUNTER_PM[S.AT_OF[g]]):
            if v == 'kill':
                continue
            rest.append(f'execute if score #gk {OBJ} matches {S.GK[g]} if score #sqh {OBJ} matches ..{i} run {fn(f"core/hp/pm{v}")}')
    rest += [f'execute if score #ph {OBJ} matches {PH["cs3"]} run return run {fn("core/kill")}', fn('core/down/start')]
    w('core/re/repel', rest)
    w('core/re/down', ['# /reload in the down window: it goes on with at most 100 t left (the kipup: P2).',
                       f'execute if score #kip {OBJ} matches 1.. run return run {fn("core/p2/from_down")}',
                       f'execute if score #down {OBJ} matches 101.. run {sset("#down", 100)}', api.play('down')])
    w('core/re/lead', ['# /reload in a lead-in / the revive stance: the lead-in again from 0 (the crimson look first), its clock held',
                       '# one tick (I1, s3-10).', fn('core/re/lead_go'), sset('#sq', -1)])
    w('core/re/lead_go', ['# /reload in a lead-in / the revive stance: which lead-in starts again.',
                       f'execute if score #rvw {OBJ} matches 1.. run return run {fn("core/lead/re_a13")}',
                       f'execute if score #sqn {OBJ} matches {S.SEQ_ID["lead5"]} run return run {fn("core/lead/a13")}',
                       f'execute if score #gk {OBJ} matches {S.GK["a8"]} run return run {fn("core/lead/re_a8")}',
                       fn('core/lead/re_a13')])
    # bars: the under bar
    w('bars', ['# Hook bars (@s = body, every tick in intro / fight while the bars are on): the under bar = the shield (electro, 5)',
               '# or the down timer (gold, 200); nothing while the module HUD is off (#hud 0: CS1). F2 (HR-29): the HP bar fills',
               '# over the first 30 t of the fight (mboss/bars_ramp: its intro ramp, here at control, the bars being off in CS0).',
               'execute if score #mbSt mb matches 1 if score #mbT mb matches ..29 run function rlk:mboss/bars_ramp',
               f'execute if score #hud {OBJ} matches 0 run return 0',
               f'execute if score #shb {OBJ} matches 1 run return run {fn("hud/bar_shield")}',
               f'execute if score #ph {OBJ} matches {PH["down"]} if score #kip {OBJ} matches 0 run {fn("hud/bar_down")}'])
    w('hud/bar_down', ['# The under bar = the down window\'s ticks left (gold, max api.DOWN_T).',
                       f'scoreboard players operation #buSub bu = #down {OBJ}', f'scoreboard players set #buSubMax bu {api.DOWN_T}',
                       f'scoreboard players set #buSubCol bu {api.BU_DOWN}'])
    # the intro replay (test 30 / 35)
    w('core/replay/start', ['# Test 30 / 35: the intro again in the fight (@s = body, invulnerable), then the fight goes on.',
                            fn('core/cancel_pat0'), fn('core/deco_seat'),
                            f'tp @s {api.xyz(api.SEAT_POS)} {L.num(yaw_to(api.SEAT_POS, api.MOON_POS))} 0',
                            sset('#rp', 1), sset('#inv', 1), sset('#sqn', S.SEQ_ID['intro']), sset('#sq', 0), sset('#sqdone', 0),
                            sset('#skip', 0), seq(ctx, 'intro', 'start')])
    w('core/replay/tick', [f'scoreboard players add #sq {OBJ} 1', seq(ctx, 'intro', 'tick'), sset('#sq_sig', 0), fn('core/skip'),
                           f'execute if score #sqdone {OBJ} matches 1 run return run {fn("core/replay/end")}',
                           f'execute if score #sq {OBJ} matches {INTRO_LEN + 2}.. run {fn("core/replay/end")}'])
    w('core/replay/end', [seq(ctx, 'intro', 'cancel'), fn('core/skip_clear'), sset('#rp', 0), sset('#sqn', 0), sset('#sq', 0),
                          sset('#sqdone', 0), sset('#skp', 0), *seat_gone(),
                          f'execute if score #ph {OBJ} matches {PH["p1"]} run {sset("#inv", 0)}',
                          f'execute if score #ph {OBJ} matches {PH["p2"]} run {sset("#inv", 0)}',
                          fn('core/looks'), fn('ai/rec_start')])


# ================================================================================================== tests
def tests(W, ctx):
    w = W.w
    present = ctx.present
    w('test', ['# Hook test {id:N} (as the player, /function rlk:boss/test/pattern {id:N}); the list: test/help.',
               f'$scoreboard players set #tst {OBJ} $(id)', at_body(fn('test/run'))])
    run = ['# @s = body: the test #tst (api.TEST_IDS).']
    for k in present:
        if k in GAUNT:
            continue
        run.append(f'execute if score #tst {OBJ} matches {TID[k]} run return run {fn(f"test/go/{k}")}')
        need_p2 = [f'execute unless score #ph {OBJ} matches {PH["p2"]} run {fn("test/p2")}'] if k in api.P2 else []
        w(f'test/go/{k}', [f'# Test {TID[k]}: {k.upper()} now.', f'execute unless function {NS}core/force run return 0']
          + need_p2 + [fn(f'core/start/{k}')])
    table = {20: 'test/cs1', 21: 'test/a8', 22: 'test/a8_0', 23: 'test/a8_fail', 24: 'test/cs2', 25: 'test/down', 26: 'test/lead',
             27: 'test/a13', 28: 'test/a13_0', 29: 'test/a13_fail', 30: 'test/intro', 31: 'test/look_dark', 32: 'test/look_crimson',
             33: 'test/p2', 34: 'test/hp5', 35: 'test/skip100', 80: 'test/floor', 90: 'test/ev90', 91: 'test/ev91', 92: 'test/ev92',
             99: 'test/hold'}
    assert set(table) | {TID[k] for k in api.P1 + api.P2 if k not in GAUNT} == set(api.TEST_IDS), sorted(set(api.TEST_IDS) - set(table))
    for tid, rel in table.items():
        run.append(f'execute if score #tst {OBJ} matches {tid} run return run {fn(rel)}')
    w('test/run', run)
    w('core/force', [
        '# Tests: make the fight state ready for a forced step (@s = body): the intro ends, whatever runs stops (pattern,',
        '# gauntlet, sequence, replay), cine off. Returns 1.',
        f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
        fn('core/stop_all'), L.cine(False), fn('core/stop_move'), fn('core/ground'), sset('#lock', 0), 'return 1'])
    prep = ['# The chain context from P2 on (tests; @s = body): the 5 % floor, the bars and the module HUD on, phase p2 looks,',
            '# music 2, the crimson look.', f'scoreboard players operation #mbFloor mb = #fl5 {OBJ}', api.bars(1), sset('#hud', 1),
            sset('#fl', 0), sset('#ph', PH['p2']), fn('core/looks'), music_to(2)] + look_req('crimson')
    w('test/prep', prep)
    w('test/cs1', ['# Test 20: CS1 -> SQ1 -> A8 now.', f'execute unless function {NS}core/force run return 0', sset('#fl', 0),
                   fn('core/cs1/start')])
    for tid, g, pips, off in ((21, 'a8', None, 0), (22, 'a8', 0, 0), (23, 'a8', None, 1), (27, 'a13', None, 0), (28, 'a13', 0, 0),
                              (29, 'a13', None, 1)):
        name = {None: g, 0: f'{g}_0'}[pips] if not off else f'{g}_fail'
        what = {None: '5/5', 0: 'with 0 pips (the deflect)'}[pips] if not off else 'that fails (no pip can go)'
        w(f'test/{name}', [f'# Test {tid}: {g.upper()} now, {what}.', f'execute unless function {NS}core/force run return 0',
                           fn('test/prep'), fn('shield/arm')] + ([sset('#pips', 0)] if pips == 0 else [])
          + [sset('#pipoff', off), sset('#gk', S.GK[g]), fn(f'core/g/start/{g}')])
    w('test/cs2', ['# Test 24: the counter cinematic CS2 now (then the down window).', f'execute unless function {NS}core/force run return 0',
                   fn('test/prep'), sset('#gk', S.GK['a8']), fn('core/repel/start')])
    w('test/down', ['# Test 25: the down window now.', f'execute unless function {NS}core/force run return 0', fn('test/prep'),
                    fn('core/down/start')])
    w('test/lead', ['# Test 26: lead_stand {g:"a13"} -> A13.', f'execute unless function {NS}core/force run return 0', fn('test/prep'),
                    sset('#pipoff', 0), fn('core/lead/a13')])
    # F1 (HR-06): the replay hands the fight back to P1 / P2 only, so it refuses elsewhere (as 타키's core/force does in a
    # mantle / transition): from CS1, a gauntlet, the down window, a lead-in it would leave the phase with nothing running
    p12 = f'execute unless score #ph {OBJ} matches {PH["p1"]} unless score #ph {OBJ} matches {PH["p2"]} run return 0'
    w('test/intro', ['# Test 30: the intro again (invulnerable); only in P1 / P2.', p12, f'execute unless function {NS}core/force run return 0',
                     fn('core/replay/start')])
    w('test/skip100', [f'# Test 35: the intro again, skipped at its tick 100; only in P1 / P2.', p12,
                       f'execute unless function {NS}core/force run return 0', fn('core/replay/start'), sset('#skp', 100)])
    w('test/look_dark', ['# Test 31: the dark look on / off (crimson).',
                         *[S.gate(f'if score #lk {OBJ} matches {api.LOOK_ID["dark"]}', x) for x in look_req('crimson')],
                         f'execute if score #lk {OBJ} matches {api.LOOK_ID["dark"]} run return run {sset("#lk", api.LOOK_ID["crimson"])}',
                         *look_req('dark'), sset('#lk', api.LOOK_ID['dark'])])
    w('test/look_crimson', ['# Test 32: the crimson look.', *look_req('crimson'), sset('#lk', api.LOOK_ID['crimson'])])
    w('test/p2', ['# Test 33: P2 now (CS1 / A8 skipped).', f'execute unless function {NS}core/force run return 0', fn('test/prep'),
                  fn('core/p2/from_fail')])
    w('test/hp5', ['# Test 34: HP = the 5 % floor + 1.', f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
                   f'scoreboard players operation @s mhpC = #fl5 {OBJ}', 'scoreboard players add @s mhpC 1'])
    w('test/floor', ['# Test 80: HP = the next floor + 1 (P1: 60 %, later 5 %).', f'execute if score #mbSt mb matches 0 run {fn("core/intro/done")}',
                     f'execute if score #ph {OBJ} matches {PH["p1"]} run scoreboard players operation @s mhpC = #fl60 {OBJ}',
                     f'execute unless score #ph {OBJ} matches {PH["p1"]} run scoreboard players operation @s mhpC = #fl5 {OBJ}',
                     'scoreboard players add @s mhpC 1'])
    w('test/ev90', ['# Test 90: the next event is random again.', f'data remove storage {api.STORAGE} {api.EV_FORCE}'])
    for tid, br in ((91, 'item'), (92, 'buff')):
        w(f'test/ev{tid}', [f'# Test {tid}: the next event = {br} (then /function rlk:boss/test/kill plays the ending + the coda).',
                            f'data modify storage {api.STORAGE} {api.EV_FORCE} set value "{br}"'])
    w('test/hold', ['# Test 99: hold / release the AI (a running pattern finishes).',
                    f'execute if score #lock {OBJ} matches 1 run return run {sset("#lock", 0)}', sset('#lock', 1)])
    rows = [H.head('/function rlk:boss/test/pattern {id:…}', f'{api.NAME} 시험 번호')]
    for tid, name in api.TEST_HELP_NAMES.items():
        key = api.TEST_IDS[tid]
        if key in api.P1 + api.P2 and key not in present:
            continue
        rows.append(H.row(f'/function rlk:boss/test/pattern {{id:{tid}}}', tid, name))
    locks = [i for i in api.LOCK_IDS if api.TEST_IDS[i] in present]
    rows.append(H.note(f'lock {{id:{",".join(str(i) for i in locks)}}}: 그 패턴만 반복 · {{id:0}} 해제'))
    w('test/help', rows)


# ================================================================================================== stand-ins: sequences
def stand_in_seqs(W, ctx):
    """core/sq/<name>/{start,tick,cancel} (+ intro skip) for every sequence S2b's seq.SERVICES does not provide yet: the
    clip(s), the length, the title / music at their events, the look requests, the signals (#sq_sig), the banner where
    the gauntlet's fail is lethal (#warn), the event coda's grant / title at E56 (api.ev_apply / ev_title)."""
    w = W.w
    E = api.ev

    def evs_of(name):
        d = {}
        if name == 'intro':
            n0 = api.CLIPS['intro'][0]
            d[n0] = [api.play('intro_end')] + S.line(11)
            d[n0 + E('intro_end', 'draw')] = [L.title(*api.TITLE)]
            d[n0 + E('intro_end', 'music')] = [music_to(1), 'kill @e[tag=rlk_hr_deco_seat_rock]']
            d[E('intro', 'turn')] = ['function rlk:mboss/mv/face']
            for t in range(E('intro', 'l6'), E('intro', 'l10') + 1, 12):
                d.setdefault(t, []).append(fn('core/sq/intro/walk'))
        elif name == 'cs1':
            d[E('cs1', 'recolour')] = [api.rig('look/phase/p2')] + look_req('crimson')
            d[E('cs1', 'music')] = [music_to(2)]
        elif name == 'lead60':
            if api.ULT60_LETHAL:
                d[1] = warn(1)
        elif name == 'repel':
            for i, e in enumerate(api.COUNTER_EV):
                d[E('repel', e)] = [sset('#sq_sig', api.SIG[f'hp{i + 1}'])]
        elif name in ('lead5', 'lead_re'):
            # hr_design §3.3: the refill beat (gauge 5/5) + the warning banner while the gauntlet's fail is lethal (#warn)
            d[E(name, 'refill')] = [sset('#sq_sig', api.SIG['refill'])] + [S.gate(f'if score #warn {OBJ} matches 1', x) for x in warn(1)]
        elif name == 'ending':
            d[E('ending', 'music')] = [api.music(3)]
        elif name == 'event':
            T = api.EV_T
            if api.EVENT['lines']:
                d[T['line']] = [S.gate(f'if score #hrEv {OBJ} matches 1', x) for x in S.line(24)] \
                    + [S.gate(f'if score #hrEv {OBJ} matches 2', x) for x in S.line(25)]
            d[T['leave']] = [api.play('ev_leave')]
            d[T['hide']] = [api.rig('state/hidden')]
            d[T['grant']] = [x for x in (api.ev_apply(), api.ev_title()) if x]
            d[T['black']] = [x for x in (K.ovl('black', 10, 12, 0),) if x]
        return {t: [x for x in v if x] for t, v in d.items() if [x for x in v if x]}

    for name in api.SEQS:
        if name in ctx.services:
            continue
        ln = api.SEQ_LEN[name]
        args = api.SEQ_ARGS.get(name, {})
        start = [f'# Stand-in sequence {name} (S2b\'s seq.py has none yet): the clip, {ln} t, the beats the core and the tests need.']
        if args:
            k = sorted(args)[0]
            start.append(f'$data modify storage {api.STORAGE} core.sq.{k} set value "$({k})"')
        start.append(sset('#sqdone', 0))
        if name == 'event':
            start += [api.rig('face/player'), f'execute if score #hrEv {OBJ} matches 1 run {api.play("ev_give")}',
                      f'execute unless score #hrEv {OBJ} matches 1 run {api.play("ev_toast")}']
        else:
            start.append(api.play(api.SEQ_CLIPS[name][0]))
        w(f'core/sq/{name}/start', start)
        tick = [f'# Stand-in {name} tick (#sq hr 1..{ln}).']
        for t, cmds in sorted(evs_of(name).items()):
            if len(cmds) == 1:
                tick.append(S.gate(f'if score #sq {OBJ} matches {t}', cmds[0]))
            else:
                w(f'core/sq/{name}/k/{t}', [f'# Stand-in {name} tick {t}.'] + cmds)
                tick.append(f'execute if score #sq {OBJ} matches {t} run {fn(f"core/sq/{name}/k/{t}")}')
        tick.append(f'execute if score #sq {OBJ} matches {ln}.. run {sset("#sqdone", 1)}')
        w(f'core/sq/{name}/tick', tick)
        w(f'core/sq/{name}/cancel', [f'# Stand-in {name} cancel (idempotent).'])
        if name == 'intro':
            w('core/sq/intro/walk', [
                '# Stand-in intro (E6-E9): a 12-t glide leg of 1.8 b toward the player while farther than 7 b (mv/ok-checked).',
                f'execute at @s if entity {S.PLAYER[:-1]},distance=..7] run return 0',
                f'execute at @s facing entity {S.PLAYER} feet rotated ~ 0 positioned ^ ^ ^1.8 positioned ~ {CY} ~ if function '
                f'rlk:mboss/mv/ok run function rlk:mboss/mv/glide {{t:12}}'])
            w('core/sq/intro/skip', [
                '# Stand-in skip (the core counted the hold): the black, the rock gone, her E10 end pose <= 7 b from the player',
                '# (on her line to the player, mv/ok), facing them; the core then jumps the clock.',
                *[x for x in (K.ovl('black', 0, 20, 6),) if x], 'kill @e[tag=rlk_hr_deco_seat_rock]', fn('core/stop_move'),
                'kill @e[type=minecraft:marker,tag=rlk_hr_near]',
                f'execute at {S.PLAYER} facing entity @s feet rotated ~ 0 positioned ^ ^ ^6.5 positioned ~ {CY} ~ run summon '
                f'minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt("rlk_hr_near")}}}',
                sset('#t4', 0), f'execute as @e[type=minecraft:marker,tag=rlk_hr_near,limit=1] at @s run {fn("core/clamp")}',
                f'execute at @s unless entity {S.PLAYER[:-1]},distance=..7] positioned as @e[type=minecraft:marker,tag=rlk_hr_near,limit=1] run tp @s ~ ~ ~',
                'kill @e[type=minecraft:marker,tag=rlk_hr_near]', 'function rlk:mboss/mv/face'])


# ================================================================================================== stand-ins: gauntlets
def stand_in_gauntlets(W, ctx):
    """core/gs/<g>/{start,tick,cancel} while S4's p_ghost.PATTERNS lacks the gauntlet: its clips at their script rows, no
    hazard (S4 owns the cuts), each counting cut's pip window at its lock (a marker rlk_hr_cut at the player's feet ->
    shield/cut {s}), the judge at JUDGE_T, then the branch: deflect -> #done at REPEL_T; A8 fail -> ult/fail60 at the
    player + g_reform, #done at FAIL60_P2_T; A13 fail -> ult/fatal on the player, #done 12 t later (a survived death)."""
    w = W.w
    for g in GAUNT:
        if g in ctx.pats:
            continue
        rows = api.SCRIPTS[g]
        jt, rt = api.JUDGE_T[g], api.REPEL_T[g]
        evs = {}
        for t, step, clip, c in rows:
            if t < 0:
                continue
            if clip:
                evs.setdefault(t, []).append(api.play(clip))
            if c:
                made, lock, strike, tier, kb = c
                evs.setdefault(lock, []).append(fn(f'core/gs/cut') + f' {{s:{strike}}}')
        evs.setdefault(jt, []).append(fn(f'core/gs/{g}/judge'))
        evs.setdefault(rt, []).append(f'execute if score #gres {OBJ} matches 1 run {sset("#done", 1)}')
        fail_done = api.FAIL60_P2_T if g == 'a8' else jt + 12
        evs.setdefault(fail_done, []).append(f'execute if score #gres {OBJ} matches 2 run {sset("#done", 1)}')
        w(f'core/gs/{g}/start', [f'# Stand-in gauntlet {g.upper()} (S4\'s p_ghost.py has none yet): T0.', api.play('g_tell')])
        tick = [f'# Stand-in {g.upper()} tick (#pt hr 1..).']
        for t, cmds in sorted(evs.items()):
            if len(cmds) == 1:
                tick.append(S.gate(f'if score #pt {OBJ} matches {t}', cmds[0]))
            else:
                w(f'core/gs/{g}/k/{t}', [f'# Stand-in {g.upper()} tick {t}.'] + cmds)
                tick.append(f'execute if score #pt {OBJ} matches {t} run {fn(f"core/gs/{g}/k/{t}")}')
        w(f'core/gs/{g}/tick', tick)
        judge = [f'# Stand-in {g.upper()} judge (T + {jt}): shield/judge; the darkness lifts and the banner goes; a fail runs its branch.',
                 fn('shield/judge'), *look_req('crimson'), *warn(0)]
        if g == 'a8':
            judge += [f'execute if score #gres {OBJ} matches 2 at {S.PLAYER} run {fn("ult/fail60")}',
                      f'execute if score #gres {OBJ} matches 2 run {api.play("g_reform")}']
        else:
            judge += [f'execute if score #gres {OBJ} matches 2 as {S.PL} run {fn("ult/fatal")}']
        w(f'core/gs/{g}/judge', judge)
        w(f'core/gs/{g}/cancel', [f'# Stand-in {g.upper()} cancel (idempotent): its cut markers, the pip windows, the banner.',
                                  f'kill @e[tag={S.tag_p(g)}]', f'kill @e[type=minecraft:marker,tag={api.TAGS["cut"]}]',
                                  'kill @e[type=minecraft:marker,tag=rlk_hr_pip]', *warn(0)])
    if any(g not in ctx.pats for g in GAUNT):
        w('core/gs/cut', ['# {s}: the stand-in cut at its lock (@s = body): a marker rlk_hr_cut at the player\'s feet registers the pip',
                          '# window of strike s (shield/cut as the marker, at it); it goes 2 t after the strike.',
                          f'execute at {S.PLAYER} run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(api.TAGS["pat"], api.TAGS["cut"], "rlk_hr_gsnew")}}}',
                          f'$execute as @e[type=minecraft:marker,tag=rlk_hr_gsnew,limit=1] at @s run function {NS}shield/cut {{s:$(s)}}',
                          'tag @e[type=minecraft:marker,tag=rlk_hr_gsnew] remove rlk_hr_gsnew'])


# ================================================================================================== the stand-in rig
# the built rig's idle-t0 anchors (^left ^up ^forward, rounded to 0.05; S2d: the player-size body, its slim arms and the level hat)
ANCHOR_OFF = {'hand_l': (0.15, 0.95, 0.25), 'hand_r': (-0.45, 0.8, 0.0), 'blade_tip': (-0.7, 0.15, 1.3),
              'blade_mid': (-0.3, 0.5, 0.85), 'scabbard_mouth': (-0.25, 0.95, 0.2), 'hat_crown': (0.0, api.HAT_TOP, 0.15),
              'head': (0.0, 1.75, 0.1), 'chest': (0.0, 1.2, 0.1)}


def rig_stub(W):
    """rig_stub/**: every rig call name of the contract while S2a's manifest is missing. play/<clip> and start/<clip> set
    #rigc hr to the clip id (#rigt -1: the next rig/tick shows tick 0); face/* turn the body; anchor/<a> places the one
    rlk_hr_anchor marker at a rough body offset (so the kit's anchor effects have a point); no visuals but a faint lilac
    column marking the body."""
    w = W.w
    assert set(ANCHOR_OFF) == set(api.ANCHORS)
    am = f'@e[type=minecraft:marker,tag={api.TAGS["anchor"]},limit=1]'
    for c in api.RIG_CALLS:
        if c == 'tick':
            w('rig_stub/tick', ['# Stand-in rig tick (@s = body): the shown clip tick #rigt hr; a faint column marks the body.',
                                f'scoreboard players add #rigt {OBJ} 1',
                                f'execute if score #rigt {OBJ} matches 0.. run particle {S.DUST["lilac"]} ~ ~1.1 ~ 0.12 0.5 0.12 0 2 force @a[tag=player]'])
        elif c == 'face/player':
            w('rig_stub/face/player', ['execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0'])
        elif c == 'face/track':
            w('rig_stub/face/track', ['function rlk:mboss/mv/turn {max:4}'])
        elif c == 'kill':
            w('rig_stub/kill', ['# Stand-in rig kill: the anchor marker.', f'kill @e[type=minecraft:marker,tag={api.TAGS["anchor"]}]'])
        elif c == 'uninstall':
            w('rig_stub/uninstall', ['# Stand-in rig uninstall: the anchor marker.', f'kill @e[type=minecraft:marker,tag={api.TAGS["anchor"]}]'])
        elif c.startswith('anchor/'):
            a = c.split('/')[1]
            x, y, z = ANCHOR_OFF[a]
            w(f'rig_stub/{c}', [f'# Stand-in anchor {a} (@s = body, at its feet): the rlk_hr_anchor marker at ^{x} ^{y} ^{z}.',
                                f'execute unless entity {am} run summon minecraft:marker ~ ~ ~ {{Tags:{S.tags_nbt(api.TAGS["anchor"])}}}',
                                f'execute at @s rotated as @s rotated ~ 0 positioned ^{L.num(x)} ^{L.num(y)} ^{L.num(z)} run tp {am} ~ ~ ~ ~ 0'])
        else:
            w(f'rig_stub/{c}', [f'# Stand-in rig call {c} (S2a\'s rig missing): no visuals.'])
    w('rig_stub/face/set', ['$tp @s ~ ~ ~ $(yaw) 0'])
    for clip in api.CLIPS:
        for kind in ('play', 'start'):
            w(f'rig_stub/{kind}/{clip}', [f'scoreboard players set #rigc {OBJ} {S.clip_id(clip)}',
                                          f'scoreboard players set #rigt {OBJ} {-1 if kind == "play" else 0}'])
