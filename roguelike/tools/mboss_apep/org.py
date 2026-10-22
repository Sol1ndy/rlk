"""The organism runtime of the revival stage (plan 7.6.4-7.6.7, 8.2; AP-REV) and the 둥지 walls: AP:org/**, AP:wall/**.

Organisms are framework aux husks (aux/spawn: HP = #apTot x the per mille of api.ORG_PM, RES Dendro 20 / others 10 through
#auxRes / #auxResEl / #auxResElV, the click shield and the HP-bar height of the org manifest's kind, FN-29) tagged
rlk_mb_ap_org + rlk_mb_ap_<kind>, apK = the kind id, carrying the real AP-ORG models as passengers (om/<kind>/spawn as the
husk: ride_y 2.0, RORG-1). The stage (revival.py, rev/tick, phase 2 only) runs org/tick as every organism husk once per
tick (RORG-3): the model clip step (om/tick), then the kind's state machine on apS / apT. Facing: the husk turns (tp /
step_flat) and om/face turns the passengers (a tp of a passenger would dismount it).

Every spawn (waves, the time-out, tests 23-28 through the waves' own path) is a 20 t spawn marker (kit spawn_marker) and
then a 10 t emergence (rlk_mb_inv: untargetable until solid). Kills: the module reads rlk_mb_broken (aux/take) and pays
the progress (api.REV basic_kill / kill: +300 basic / +1300 the others since AP-FIX) at once, the energy particles (char/particles el 7; 파괴 n 4), the
kind's death clip, then removes the husk and its passengers (no XP / gold / heal orbs: aux kills pay none; never a
true_hit). Swallowed basics and a 파괴 that blew pay nothing.

Hazards (all Dendro, quiet: the 10-20 telegraph rule makes every organism row *none*, plan 14): O1 the melee cone at the
Heart, O2 the ranged bolt (pj, body-blockable; the module ends it within 1.5 b of the Heart's bulb box = the Heart hit),
O6a the 포식성 burst, O6b its bites (chains 1 / 2, singles), O7 the 파괴 blast. Each shows its readable motion tell (the
lean, the crown flare and the bolt in flight, the inflating pod, the chain-start flare, the fuse) and an impact fx at the
hit tick. The 둥지 walls are barrier blocks recorded per block (rlk_mb_ap_wallb markers) and removed exactly; never in
the player's body box + 1 b, never within 1 b of an organism, never inside the Heart's wall exclusion, only inside the
walk disc, only in phase 2; wall/clear also runs the arena's barrier safety sweep (FN-26).

No text of advice (the no-tips rule, ap_contract 2.5): no first-time hints. The 양육 immunity is NURTURE_MODE 'A'
(the 양육 itself, rlk_mb_ap_imm, while it holds >= 1 link; the core's aux_hit makes it take nothing, "면역").
"""
import math

from .api import Gen, K, ORGS
from . import api as A

L = A.L
n = L.num
R = A.REV
NS = A.NS
CX, CY, CZ = A.CENTRE[0], A.CY, A.CENTRE[2]
CEN = f'{n(CX)} {CY} {n(CZ)}'
FP = A.FOOTPRINT
KID = A.KIND_ID
PLAYER = A.PLAYER                                   # @e[tag=rlk_body,limit=1]: the player's body
PL_FACE = f'facing entity {PLAYER} feet'
HEART_FACE = f'facing entity {A.HEART_M} feet'           # the Heart marker sits at the centre on the floor
HEAD = '# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.'

EMERGE = 10                                         # plan 7.6.3: a 10 t emergence, untargetable until solid
MARK_T = int(A.ORG['spawn']['marker_ticks'])        # 20 t spawn marker before the husk appears
SOCKS = [(int(s['id']), float(s['bearing']), float(s['r'])) for s in FP['sockets']]
SOCK_R = SOCKS[0][2]                                # 3.4
WAIT_R = float(FP['wait_ring'])                     # 4.5
DSTOP_R = float(FP['destr_stop']['r'])              # 2.6
DSTOP_B = [float(b) for b in FP['destr_stop']['bearings']]
WALL_EX = float(FP['wall_exclusion'])               # 4.6: no barrier block inside
RANGED_R = 12.6                                     # plan 7.6.5: ranged basics stop on r 11-13 (the r 12 spawn ring)
NEST_KEEP = (4.0, 8.0)                              # the 둥지 keeps 4-8 b from the player
NEST_BLINK = (12.0, 5.0)                            # beyond 12 b it blinks to 5 b from the player
PRED_RING = (3.0, 5.0)                              # the 포식성 circles the player at 3-5 b
PRED_REACH = 1.5                                    # it swallows a basic at <= 1.5 b
PRED_CLOSE = 2.0                                    # before a bite it closes to 2 b (the lunge prep)
PRED_DASH = 1.5                                     # the close-in dash (b/t) of the 2 t before a bite's lock
SPD = {'basic': R['basic_spd'], 'destr': R['destr_spd'], 'pred': 0.15, 'nest': 0.15}
DIE = {k: A.org_clip(k, {'basic': 'org_die', 'nurt': 'nurt_die', 'guard': 'guard_die', 'nest': 'org_die', 'destr': 'org_die',
                         'pred': 'org_die'}[k])['len'] for k in A.KINDS}
SHIELD_COL = '#8FD8FF'                              # the absorbed number (plan 7.6.6: sky-blue)

# The hazards of the organisms (plan 8.2, areas x1.2), ticks on the organism's own state clock; tele none everywhere
# (plan 14 10-20 table) -> no kit decal, #hzQuiet 1, an impact fx at the hit tick. pat_rev.py checks this table.
HZ = {
    'o1': dict(kind='sector', r=3.1, a=27, tell=10, dmg=A.DMG['o1'], dmg_buff=A.DMG['o1_buffed'], kb=A.KB['light'],
               heart=R['basic_hit'], heart_buff=R['buffed_hit'], tele='none',
               tell_src='basic_melee lean 0-10 (the bell leans back, then bumps into the Heart)'),
    'o2': dict(kind='pj', spd=0.75, hr=0.7, life=20, y=1.6, made=12, dmg=A.DMG['o2'], dmg_buff=A.DMG['o2_buffed'],
               heart=R['basic_hit'], heart_buff=R['buffed_hit'], tele='none',
               tell_src='basic_ranged: pivot t0 (o2_pivot), crown flare t3 (o2_charge), crown open 5-12; the bolt in flight'),
    'o6a': dict(kind='disc', r=3.6, tell=10, dmg=A.DMG['o6_burst'], kb=A.KB['default'], made=32, hit=42, tele='none',
                tell_src='the bud 12-32 (core lit) and the pod inflating 32-42 (pred_inflate, o6_inflate)'),
    'o6b': dict(kind='sector', r=2.6, a=24, tell=10, chain=(A.DMG['o6_chain1'], A.DMG['o6_chain2'], A.DMG['o6_chain3'],
                A.DMG['o6_chain4']), single=A.DMG['o6_single'], unemp_pct=A.O6_UNEMPOWERED_PCT, kb=A.KB['light'],
                chain_hits=(12, 18, 24, 30), single_hit=14, tele='none',
                tell_src='the chain-start flare (fish_flare look + o6_swim) 12 t before bite 1; singles: the flare + dash-in 12 t before'),
    'o7': dict(kind='disc', r=3.6, tell=R['destr_blast_at'], dmg=A.DMG['o7'], kb=A.KB['heavy'], heart=R['destr_blast'],
               tele='none', tell_src='the fuse 0-56 (pulses every 9 t, every 4 t from 36; o7_primed) + the suck 56-61'),
}
CHAIN_HITS = HZ['o6b']['chain_hits']
SINGLE_HIT = HZ['o6b']['single_hit']
BITE_CLIP_LEAD = 4                                  # the clips' first snap (hit_1 / hit) is at clip t4: started 4 t before


def sc(name, v):
    return f'scoreboard players set {name} mb {int(v)}'


def es(obj, v):
    return f'scoreboard players set @s {obj} {int(v)}'


def bpt(r, b):
    """The floor point at radius r, compass bearing b (0 north -z, 90 east +x) round the arena centre."""
    return (CX + r * math.sin(math.radians(b)), CZ - r * math.cos(math.radians(b)))


def at_centre(r, neg=False):
    """execute prefix: @s within r of the centre (`unless` when neg)."""
    return f'execute positioned {CEN} {"unless" if neg else "if"} entity @s[distance=..{n(r)}]'


def om(kind, rel):
    return f'function {NS}om/{kind}/{rel}'


def unemp(v):
    return int(round(v * A.O6_UNEMPOWERED_PCT / 100.0))


def emit(g):
    F = g.fn
    hz = Gen.hz_opts
    step = L.step_flat
    snd = K.snd
    fx = K.fx

    # ================================================================ spawning
    for k, rec in A.KINDS.items():
        pm = A.ORG_PM[k]
        sh = rec.get('shield') or {}
        bar = float(rec['hp_bar_y']) - float(A.ORG['passenger']['ride_y']) - 0.25
        g.w(f'org/spawn_{k}', [
            HEAD, f'# A {rec["name"]} ({k}, apK {rec["id"]}) at the execution point (any executor; tests 23-28, the pending spawn',
            f'# markers): HP {pm} per mille of #apTot, RES Dendro {A.ORG_RES["dendro"]} / others {A.ORG_RES["other"]} (U2), the click shield',
            f'# {sh.get("w")} x {sh.get("h")} and the HP bar {rec["hp_bar_y"]} b above the feet (FN-29), the models (om/{k}/spawn).',
            'scoreboard players operation #auxHp mb = #apTot mb', sc('#apX', pm),
            'scoreboard players operation #auxHp mb *= #apX mb', 'scoreboard players operation #auxHp mb /= #c1000 mb',
            'execute if score #auxHp mb matches ..0 run scoreboard players set #auxHp mb 1',
            sc('#auxRes', A.ORG_RES['other']), sc('#auxResEl', 7), sc('#auxResElV', A.ORG_RES['dendro']),
            *L.aux_opts(shield_w=float(sh.get('w', 1.2)), shield_h=float(sh.get('h', 2.2)), bar_y=bar),
            f'execute positioned ~ {CY} ~ run function rlk:mboss/aux/spawn',
            f'execute as @e[type=minecraft:husk,tag=rlk_mb_auxlast,limit=1] at @s run {F("org/init_" + k)}'])
        init = [HEAD, f'# @s = the new {k} aux husk, at it: tags, kind, state 0 (emerging, untargetable), its id, facing the Heart, the',
                '# models riding it (om/<kind>/spawn plays the spawn clip with the 4 t scale-in).',
                'tag @s add rlk_mb_ap_org', f'tag @s add rlk_mb_ap_{k}', 'tag @s add rlk_mb_inv',
                es('apK', rec['id']), es('apS', 0), es('apT', 0), es('apShd', 0), es('apTok', 0), es('apL', 0),
                es('apSock', -1 if k == 'basic' else 0),
                f'execute at @s {HEART_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~']
        if k != 'basic':
            init += ['scoreboard players add #apOrgN mb 1', 'scoreboard players operation @s apL = #apOrgN mb']
        else:
            init += ['# melee / ranged: #apOArg 0 / 1 (wave 1: 2 + 2), otherwise 50 / 50',
                     'scoreboard players operation #apX mb = #apOArg mb',
                     'execute unless score #apX mb matches 0..1 store result score #apX mb run random value 0..1',
                     'execute if score #apX mb matches 1 run tag @s add rlk_mb_ap_rng']
        init += [om(k, 'spawn'), sc('#apOArg', -1), sc('#apHudQ', 1)]
        g.w(f'org/init_{k}', init)

    g.w('org/mark', [HEAD, '# Macro {k,a}: a pending spawn of kind apK k (a = the basic\'s melee 0 / ranged 1, -1 random) at the execution',
                     f'# point: the kit spawn marker (pale wireframe dome) for {MARK_T} t, then the organism (org/pend).',
                     f'execute positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om",'
                     '"rlk_mb_ap_ospawn","rlk_mb_ap_new"]}',
                     '$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apK $(k)',
                     '$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apS $(a)',
                     'scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apT 0',
                     'tag @e[type=minecraft:marker,tag=rlk_mb_ap_new] remove rlk_mb_ap_new',
                     f'execute positioned ~ {CY} ~ run {fx("spawn_marker")}',
                     f'execute positioned ~ {CY} ~ run {snd("spawn_marker")}'])
    g.w('org/pend_tick', [HEAD, '# Any executor, once per tick (T1 t116-136, phase 2): the pending spawn markers age; at '
                          f'{MARK_T} t the organism appears.',
                          f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn] at @s run {F("org/pend")}'])
    pend = ['# @s = a pending spawn marker, at it.', 'scoreboard players add @s apT 1',
            f'execute if score @s apT matches ..{MARK_T - 1} run return 0',
            'scoreboard players operation #apOArg mb = @s apS']
    pend += [f'execute if score @s apK matches {rec["id"]} run {F("org/spawn_" + k)}' for k, rec in A.KINDS.items()]
    pend += ['kill @s']
    g.w('org/pend', pend)

    g.w('org/consts', ['# The stage\'s constants (rev/tick, every tick: cheap and robust to /reload).', sc('#apM1', -1), sc('#apC5', 5),
                       sc('#apC14', 14), sc('#apC16', 16)])
    marks = [HEAD, '# The stage markers (rev/ready, rev/reload; at the floor, rlk_mb_aux): the 3 cradle sockets (rlk_mb_ap_skm<i>, r 3.4 at',
             f'# {[b for _, b, _ in SOCKS]}) and the 3 파괴 stops (rlk_mb_ap_dstop, r {DSTOP_R:g} at {DSTOP_B}) of the Heart footprint.',
             F('org/marks_kill')]
    for i, b, r in SOCKS:
        x, z = bpt(r, b)
        marks.append(f'summon minecraft:marker {n(x, 3)} {CY} {n(z, 3)} {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_skm",'
                     f'"rlk_mb_ap_skm{i}"]}}')
    for b in DSTOP_B:
        x, z = bpt(DSTOP_R, b)
        marks.append(f'summon minecraft:marker {n(x, 3)} {CY} {n(z, 3)} {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_dstop"]}}')
    g.w('org/marks', marks)
    g.w('org/marks_kill', ['kill @e[type=minecraft:marker,tag=rlk_mb_ap_skm]', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_dstop]'])

    # ================================================================ the tick
    g.w('org/tick', [HEAD, '# Any executor, once per phase-2 tick (rev/tick): every organism husk runs its kind\'s tick (dispatch by tag: one',
                     '# selector per kind instead of a per-organism dispatch, the command budget at the cap).']
        + [f'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_{k}] at @s run {F(f"org/{k}/tick")}' for k in A.KINDS])
    for k in A.KINDS:
        g.w(f'org/{k}/tick', [
            f'# @s = a {k} husk, at it (once per tick): a new break pays and starts dying; the clock; the model clip step',
            f'# (om/{k}/tick, RORG-3); dying / emerging; the state machine.',
            f'execute if entity @s[tag=rlk_mb_broken] unless entity @s[tag=rlk_mb_ap_dying] run {F("org/broke")}',
            'scoreboard players add @s apT 1',
            f'function {NS}om/{k}/tick',
            f'execute if entity @s[tag=rlk_mb_ap_dying] run return run {F("org/dying")}',
            f'execute if score @s apS matches 0 run return run {F("org/emerge")}',
            F(f'org/{k}/run')])
    em = ['# @s = an emerging organism (apS 0): solid after the emergence; then the kind\'s first state.',
          f'execute if score @s apT matches ..{EMERGE - 1} run return 0',
          'tag @s remove rlk_mb_inv', es('apS', 1), es('apT', 0)]
    em += [f'execute if score @s apK matches {rec["id"]} run return run {F(f"org/{k}/enter")}' for k, rec in A.KINDS.items()]
    g.w('org/emerge', em)

    # ---------------------------------------------------------------- kills and removal
    g.w('org/broke', [
        HEAD, '# @s = an organism the player broke (rlk_mb_broken from aux/take, or the 양육\'s self-destruct): dying (untargetable),',
        '# its slot / socket freed; the progress at once (api.REV basic_kill / kill; never for a 파괴 that blew), the energy',
        '# particles, the kind\'s death (clip, fx, links, shields).',
        'tag @s add rlk_mb_ap_dying', 'tag @s add rlk_mb_inv', es('apT', 0),
        'tag @s remove rlk_mb_ap_tok', 'tag @s remove rlk_mb_ap_sk0', 'tag @s remove rlk_mb_ap_sk1', 'tag @s remove rlk_mb_ap_sk2',
        f'execute unless entity @s[tag=rlk_mb_ap_spent] if score @s apK matches 1 run function {NS}heart/add {{v:{R["basic_kill"]}}}',
        f'execute unless entity @s[tag=rlk_mb_ap_spent] unless score @s apK matches 1 run function {NS}heart/add {{v:{R["kill"]}}}',
        f'execute unless entity @s[tag=rlk_mb_ap_spent] unless score @s apK matches {KID["destr"]} positioned ~ ~0.8 ~ run function rlk:char/particles {{n:1,el:7}}',
        f'execute unless entity @s[tag=rlk_mb_ap_spent] if score @s apK matches {KID["destr"]} positioned ~ ~0.8 ~ run function rlk:char/particles {{n:4,el:7}}']
        + [f'execute if score @s apK matches {rec["id"]} run return run {F(f"org/{k}/die")}' for k, rec in A.KINDS.items()])
    dy = ['# @s = a dying organism: its death clip plays (om/tick); removed at the clip end. A 파괴 that blew is flung 2.5 b',
          '# away from the Heart over its first 5 t.',
          f'execute if entity @s[tag=rlk_mb_ap_spent] if score @s apT matches ..5 {HEART_FACE} rotated ~180 0 run {step(0.5)}']
    dy += [f'execute if score @s apK matches {rec["id"]} if score @s apT matches {DIE[k]}.. run return run {F("org/remove")}'
           for k, rec in A.KINDS.items()]
    g.w('org/dying', dy)
    g.w('org/remove', ['# @s = an organism husk: its passengers (the models, the HP bar) first, then itself (no rewards).',
                       'execute on passengers run kill @s', 'kill @s'])
    g.w('org/clear', [HEAD, '# Every organism, its models and the stage\'s loose entities (pending spawns, bolts, the organisms\' hazards); no',
                      '# progress (cleanup, the CS, a failure strike, death, the phase jumps; idempotent, any executor). The fixed',
                      '# objects (the Heart, domes, stalks, walls: rlk_ap_om_obj) are not touched here.',
                      f'execute as {ORGS} run function {NS}om/kill',
                      f'execute as {ORGS} on passengers run kill @s', f'kill {ORGS}',
                      'kill @e[tag=rlk_ap_om,tag=!rlk_ap_om_obj]',
                      'kill @e[type=minecraft:marker,tag=rlk_mb_ap_ospawn]', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_cand]',
                      'kill @e[type=minecraft:item_display,tag=rlk_mb_ap_bolt]', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_ohz]',
                      'kill @e[type=minecraft:marker,tag=rlk_mb_ap_wlock]', sc('#apSlots', 0)])
    g.w('org/burst_all', [HEAD, '# Every living organism bursts (a failure strike, the CS wilt; no progress): its burst fx at it, two at once,',
                          '# the rest queued (a marker each, two per tick from the service\'s tick: org/burst_q; perf, AP-I2: six bursts',
                          '# with the strike / wilt tick passed the 3000-commands budget).',
                          f'execute as {ORGS.replace("]", ",limit=2]")} at @s positioned ~ ~0.6 ~ run {fx("org_burst")}',
                          f'execute as {ORGS.replace("]", ",limit=2]")} run tag @s add rlk_mb_ap_burst',
                          f'execute as {ORGS.replace("]", ",tag=!rlk_mb_ap_burst]")} at @s run summon minecraft:marker ~ ~0.6 ~ '
                          '{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_burstq"]}'])
    g.w('org/burst_q', [HEAD, '# Any executor (the failure strike and the CS ticks): two queued organism bursts.',
                        f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_burstq,limit=2] at @s run {F("org/burst_one")}'])
    g.w('org/burst_one', [HEAD, f'# @s = a queued burst marker, at it.', fx('org_burst'), 'kill @s'])
    g.w('org/freeze', [HEAD, '# Pause in phase 2: the organisms are NoAI husks stepped only by the module tick (off while paused). The walls',
                       '# are cleared by wall/clear; a 둥지 in its cast goes back to flying and re-casts later.',
                       f'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_nest,scores={{apS=2}}] run {F("org/nest/abort")}',
                       sc('#apSlots', 0)])

    # ---------------------------------------------------------------- the hit hook (shields)
    g.w('org/aux_hit', [
        HEAD, '# @s = an organism inside combat/apply (#dmg tmp after RES, #elem tmp; the core\'s aux_hit made an immune 양육 take',
        f'# nothing first). A shielded basic (수호, plan 7.6.6): the pool apShd (= {R["shield_mult"]} x its max HP) absorbs first, Pyro x'
        f'{R["pyro_vs_shield_pct"] / 100:g} against it;',
        '# the absorbed part shows sky-blue with the shield sound (#mbAuxDone 1); a break pops the overlay and passes the rest on.',
        'execute unless entity @s[tag=rlk_mb_ap_org] run return 0',
        'execute unless entity @s[tag=rlk_mb_ap_shd] run return 0',
        'execute unless score @s apShd matches 1.. run return 0',
        'scoreboard players operation #apSd mb = #dmg tmp',
        f'execute if score #elem tmp matches 1 run scoreboard players set #apY mb {R["pyro_vs_shield_pct"]}',
        'execute if score #elem tmp matches 1 run scoreboard players operation #apSd mb *= #apY mb',
        'execute if score #elem tmp matches 1 run scoreboard players operation #apSd mb /= #c100 mb',
        'execute if score #apSd mb matches ..0 run return 0',
        f'execute if score #apSd mb >= @s apShd run return run {F("org/basic/shd_break")}',
        'scoreboard players operation @s apShd -= #apSd mb',
        F('org/basic/shd_num'), f'execute positioned ~ ~1 ~ run {snd("shield_hit")}',
        'scoreboard players set #mbAuxDone mb 1'])
    g.w('org/basic/shd_num', ['# The absorbed amount #apSd as a sky-blue number above @s (the dmgText look of aux/immune).',
                              'execute store result storage rlk:mboss ap.o.d int 1 run scoreboard players get #apSd mb',
                              f'function {NS}org/basic/shd_txt with storage rlk:mboss ap.o'])
    g.w('org/basic/shd_txt', ['$summon minecraft:text_display ~ ~1.9 ~ {billboard:"center",Tags:["dmgText"],background:0,'
                              'brightness:{sky:15,block:15},shadow:true,alignment:"center",see_through:true,'
                              f'text:{{text:"$(d)",color:"{SHIELD_COL}"}},transformation:{{translation:[0f,0f,0f],'
                              'left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.1f,1.1f,1.1f]}}'])
    g.w('org/basic/shd_break', [
        '# @s = a shielded basic whose pool breaks on this hit: the rest of the hit (in HP terms) goes on to its HP.',
        'scoreboard players operation #apSd mb -= @s apShd',
        f'execute if score #elem tmp matches 1 run scoreboard players set #apY mb {R["pyro_vs_shield_pct"]}',
        'execute if score #elem tmp matches 1 run scoreboard players operation #apSd mb *= #c100 mb',
        'execute if score #elem tmp matches 1 run scoreboard players operation #apSd mb /= #apY mb',
        'scoreboard players operation #apZ mb = @s apShd', F('org/basic/shd_off'),
        f'execute at @s positioned ~ ~0.8 ~ run {fx("shield_pop")}', f'execute at @s run {snd("o3_pop")}',
        'scoreboard players operation #dmg tmp = #apSd mb',
        'execute if score #dmg tmp matches ..0 run scoreboard players set #mbAuxDone mb 1'])
    g.w('org/basic/shd_on', ['# @s = a basic: the 수호 shield (plan 7.6.6): pool = 5 x its max HP, the overlay, the pop.',
                             'execute if entity @s[tag=rlk_mb_ap_shd] run return 0', 'tag @s add rlk_mb_ap_shd',
                             'scoreboard players operation @s apShd = @s mhpM', sc('#apY', R['shield_mult']),
                             'scoreboard players operation @s apShd *= #apY mb', om('basic', 'shield/on'),
                             f'execute at @s positioned ~ ~0.8 ~ run {fx("shield_pop")}', f'execute at @s run {snd("o3_pop")}'])
    g.w('org/basic/shd_off', ['# @s = a basic: the shield gone (pool 0, overlay off).', 'tag @s remove rlk_mb_ap_shd', es('apShd', 0),
                              om('basic', 'shield/off')])

    # ================================================================ 기본 basic
    melee_every, ranged_every = R['melee_every'], R['ranged_every']
    g.w('org/basic/enter', ['# @s = a basic that just became solid: a 수호 alive within r 10 shields it (plan 7.6.5).',
                            'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_guard,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,distance=..10] '
                            f'run {F("org/basic/shd_on")}'])
    g.w('org/basic/run', [
        '# @s = a basic: 1 walk to the Heart, 2 to its socket, 3 wait on the ring, 4 melee loop, 5 lying down, 6 lying (no slot),',
        '# 7 the ranged loop, 8 held by a 포식성. Never chases the player.',
        f'execute if score @s apS matches 4 run return run {F("org/basic/melee")}',
        f'execute if score @s apS matches 7 run return run {F("org/basic/fire")}',
        f'execute if score @s apS matches 1 run return run {F("org/basic/walk")}',
        f'execute if score @s apS matches 2 run return run {F("org/basic/sock")}',
        f'execute if score @s apS matches 3 run return run {F("org/basic/wait")}',
        f'execute if score @s apS matches 5 run return run {F("org/basic/lie")}',
        f'execute if score @s apS matches 6 run return run {F("org/basic/ridle")}'])
    g.w('org/basic/walk', [
        f'# Walking to the Heart at {SPD["basic"]} b/t (bell, bobbing): melee to the wait ring r {WAIT_R} (then a socket), ranged to r '
        f'{RANGED_R} (lies down).',
        f'execute if entity @s[tag=!rlk_mb_ap_rng] {at_centre(WAIT_R + 0.2)[8:]} at @s run return run {F("org/basic/arrive")}',
        f'execute if entity @s[tag=rlk_mb_ap_rng] {at_centre(RANGED_R)[8:]} at @s run return run {F("org/basic/lie_go")}',
        f'execute {HEART_FACE} run {step(SPD["basic"])}', f'function {NS}om/face'])
    g.w('org/basic/arrive', ['# A melee basic on the wait ring: a socket + an attack slot if one is free, else it waits here.',
                             es('apT', 0), es('apS', 3), F('org/basic/try')])
    g.w('org/basic/try', [f'# @s = a melee basic: at most {R["slots"]} basics hold an attack slot (rlk_mb_ap_tok); the lowest free cradle '
                          'socket (r 3.4).',
                          'execute store result score #apX mb if entity @e[type=minecraft:husk,tag=rlk_mb_ap_tok]',
                          f'execute if score #apX mb matches {R["slots"]}.. run return fail']
        + [f'execute unless entity @e[type=minecraft:husk,tag=rlk_mb_ap_sk{i}] run return run {F(f"org/basic/take{i}")}' for i, _, _ in SOCKS]
        + ['return fail'])
    for i, b, r in SOCKS:
        x, z = bpt(r, b)
        g.w(f'org/basic/take{i}', [f'# Socket {i} (bearing {b:g}, r {r:g}) and a slot.', 'tag @s add rlk_mb_ap_tok', f'tag @s add rlk_mb_ap_sk{i}',
                                   es('apSock', i), es('apS', 2), es('apT', 0)])
    sock = ['# @s = a melee basic going to its socket (apSock): along the cradle (pushed out to r 3.4), then attacking.']
    for i, b, r in SOCKS:
        x, z = bpt(r, b)
        sock.append(f'execute if score @s apSock matches {i} if entity @e[type=minecraft:marker,tag=rlk_mb_ap_skm{i},distance=..0.25] '
                    f'run return run {F("org/basic/at_sock")}')
        sock.append(f'execute if score @s apSock matches {i} facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_skm{i},limit=1] feet '
                    f'run {step(SPD["basic"])}')
    sock += [F('org/basic/push_in'), f'function {NS}om/face']
    g.w('org/basic/sock', sock)
    g.w('org/basic/push_in', [f'# @s = an organism near the cradle: never inside r {SOCK_R} of the Heart (its root radius {FP["root_radius"]}).',
                              f'execute positioned {CEN} if entity @s[distance=..{n(SOCK_R - 0.01)}] facing entity @s feet rotated ~ 0 '
                              f'positioned ^ ^ ^{n(SOCK_R)} run tp @s ~ {CY} ~'])
    g.w('org/basic/at_sock', ['# At the socket: facing the Heart, the melee loop (the first lean 20 t later).',
                              f'execute at @s {HEART_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~', f'function {NS}om/face', es('apS', 4),
                              es('apT', melee_every - 20)])
    g.w('org/basic/wait', [f'# Waiting on the ring r {WAIT_R}: a socket and a slot are asked for every 10 t.',
                           f'execute if score @s apT matches 10.. run {F("org/basic/arrive")}'])
    # O1 melee: every 40 t holding the slot; lean 0-10 (basic_melee: lean back 0-5, bump, hit 10), the cone at the Heart
    o1 = HZ['o1']
    g.w('org/basic/melee', [
        f'# O1 (plan 8.2): every {melee_every} t holding a slot: basic_melee (the lean is the tell, 10 t), the cone hz/sector r {o1["r"]} '
        f'half {o1["a"]} at the Heart from the lean start; the strike t10: the Heart -{o1["heart"]} (buffed -{o1["heart_buff"]}).',
        f'execute if score @s apT matches {melee_every}.. run {F("org/basic/m_start")}',
        f'execute if score @s apT matches {o1["tell"]} run {F("org/basic/m_hit")}'])
    g.w('org/basic/m_start', [es('apT', 0), om('basic', 'play/basic_melee'),
                              f'execute at @s {HEART_FACE} rotated ~ 0 positioned ~ {CY} ~ run {F("org/basic/m_hz")}'])
    g.w('org/basic/m_hz', ['# The O1 cone at the floor point, rotated at the Heart (quiet: no decal, the lean is the tell).',
                           *hz(kb=o1['kb']),
                           f'execute if entity @s[tag=rlk_mb_ap_buff] run return run {L.hz_sector(o1["r"], o1["a"], o1["tell"], o1["dmg_buff"])}',
                           L.hz_sector(o1['r'], o1['a'], o1['tell'], o1['dmg'])])
    g.w('org/basic/m_hit', [
        '# The O1 strike: the Heart loses (a body-blocking player took the cone instead of nothing: the hazard is the framework\'s);',
        '# the hit sound and the kit\'s O1 impact preset at the cone (AP-I2, RREV-6).',
        f'execute if entity @s[tag=rlk_mb_ap_buff] run function {NS}heart/sub {{v:{o1["heart_buff"]}}}',
        f'execute unless entity @s[tag=rlk_mb_ap_buff] run function {NS}heart/sub {{v:{o1["heart"]}}}',
        f'execute at @s run {snd("o1_attack")}',
        f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^1.6 run {K.fx("o1_hit")}'])
    # O2 ranged
    o2 = HZ['o2']
    g.w('org/basic/lie_go', ['# A ranged basic on its ring: it lies down (basic_lie 10 t: bell -> bag), facing the Heart.',
                             es('apS', 5), es('apT', 0), 'tag @s add rlk_mb_ap_lie', f'execute at @s {HEART_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~',
                             f'function {NS}om/face',
                             om('basic', 'play/basic_lie')])
    g.w('org/basic/lie', [f'execute if score @s apT matches {A.org_clip("basic", "basic_lie")["len"]}.. run {F("org/basic/lie_done")}'])
    g.w('org/basic/lie_done', [es('apS', 6), es('apT', 10)])
    g.w('org/basic/ridle', ['# Lying, without a slot: a slot is asked for every 10 t (the first shot 20 t after it).',
                            'execute if score @s apT matches ..9 run return 0', es('apT', 0),
                            'execute store result score #apX mb if entity @e[type=minecraft:husk,tag=rlk_mb_ap_tok]',
                            f'execute if score #apX mb matches {R["slots"]}.. run return 0',
                            'tag @s add rlk_mb_ap_tok', es('apS', 7), es('apT', ranged_every - 20)])
    crown = '^ ^0.55 ^0.75'
    g.w('org/basic/fire', [
        f'# O2 (plan 8.2): every {ranged_every} t holding a slot: basic_ranged (pivot 0, crown flare 3, open 5-12), the bolt at t{o2["made"]}.',
        f'execute if score @s apT matches {ranged_every}.. run {F("org/basic/f_start")}',
        f'execute if score @s apT matches 3 at @s rotated as @s rotated ~ 0 positioned {crown} run {fx("crown_flare")}',
        f'execute if score @s apT matches 3 at @s run {snd("o2_charge")}',
        f'execute if score @s apT matches {o2["made"]} run {F("org/basic/f_bolt")}'])
    g.w('org/basic/f_start', [es('apT', 0), om('basic', 'play/basic_ranged'), f'execute at @s run {snd("o2_pivot")}'])
    life = o2['life']
    g.w('org/basic/f_bolt', [
        f'# The bolt: a seed-bolt prop (kit) flying {o2["spd"]} b/t straight at the Heart {o2["y"]} b up (pj sphere hr {o2["hr"]}, life {life}).',
        '# A player in its path takes it (pj_end 4: the Heart is spared); the stage ends it near the Heart (org/bolts).',
        f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^{n(o2["y"])} ^0.8 run summon minecraft:item_display ~ ~ ~ '
        '{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_opj","rlk_mb_ap_bolt","rlk_mb_ap_new"],teleport_duration:1,'
        'billboard:"center",item:{id:"minecraft:paper",count:1}}',
        'execute if entity @s[tag=rlk_mb_ap_buff] run tag @e[type=minecraft:item_display,tag=rlk_mb_ap_new] add rlk_mb_ap_bbuf',
        f'execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_new,limit=1] run {K.prop("seed_bolt")}',
        f'execute if entity @s[tag=rlk_mb_ap_buff] as @e[type=minecraft:item_display,tag=rlk_mb_ap_new,limit=1] at @s {HEART_FACE} '
        f'rotated ~ 0 run {F("org/basic/pj_b")}',
        f'execute unless entity @s[tag=rlk_mb_ap_buff] as @e[type=minecraft:item_display,tag=rlk_mb_ap_new,limit=1] at @s {HEART_FACE} '
        f'rotated ~ 0 run {F("org/basic/pj")}',
        'tag @e[type=minecraft:item_display,tag=rlk_mb_ap_new] remove rlk_mb_ap_new',
        f'execute at @s run {snd("o2_shoot")}'])
    g.w('org/basic/pj', [*Gen.pj_opts(kb=A.KB['light']), L.pj_launch(o2['spd'], life, o2['dmg'], o2['hr'])])
    g.w('org/basic/pj_b', [*Gen.pj_opts(kb=A.KB['light']), L.pj_launch(o2['spd'], life, o2['dmg_buff'], o2['hr'])])
    bb = FP['bulb_box']
    half = max(float(bb['l']), float(bb['w'])) / 2.0 + float(FP['bolt_end']['r'])
    y0 = CY + float(bb['centre_y']) - float(bb['h']) / 2.0 - float(FP['bolt_end']['r'])
    hy = float(bb['h']) + 2 * float(FP['bolt_end']['r'])
    g.w('org/bolts', [
        f'# Any executor, every phase-2 tick: a bolt within {FP["bolt_end"]["r"]} b of the Heart\'s bulb box (a {2 * half:.1f} b square, '
        f'y {y0:.2f}..{y0 + hy:.2f}) hits the Heart',
        '# and ends; the comet trail every 2 t (#apClk2 = 0).',
        f'execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_bolt] positioned {n(CX - half, 3)} {n(y0, 3)} {n(CZ - half, 3)} '
        f'if entity @s[dx={n(2 * half - 1, 3)},dy={n(hy - 1, 3)},dz={n(2 * half - 1, 3)}] at @s run {F("org/bolt_hit")}',
        f'execute if score #apClk2 mb matches 0 as @e[type=minecraft:item_display,tag=rlk_mb_ap_bolt] at @s run {fx("comet_trail")}'])
    g.w('org/bolt_hit', ['# @s = a bolt at the Heart: the Heart loses (buffed -120), the hit sound, gone.',
                         f'execute if entity @s[tag=rlk_mb_ap_bbuf] run function {NS}heart/sub {{v:{o2["heart_buff"]}}}',
                         f'execute unless entity @s[tag=rlk_mb_ap_bbuf] run function {NS}heart/sub {{v:{o2["heart"]}}}',
                         snd('o2_hit'), 'kill @s'])
    g.w('org/pj_end', ['# Hook pj_end of an organism prop (@s = the bolt, #pjEv 1 wall / 2 life over / 4 hit the player): a bolt that',
                       '# struck the player ends there (#pjKeep 0: the Heart is spared, plan 7.6.1 body-blocking) with the hit sound; a',
                       '# dodged one flies on (harmless to the player) to the Heart.',
                       'execute unless score #pjEv mb matches 4 run return 0',
                       'execute if score #dodged tmp matches 1 run return 0',
                       'scoreboard players set #pjKeep mb 0', f'execute at @s run {snd("o2_hit")}'])
    g.w('org/basic/die', ['# @s = a basic broken by the player: the burst, its death clip; a buffed one costs its 양육 (link lost).',
                          om('basic', 'play/org_die'), f'execute at @s positioned ~ ~0.6 ~ run {fx("org_burst")}',
                          f'execute at @s run {snd("org_kill")}',
                          f'execute if entity @s[tag=rlk_mb_ap_shd] run {F("org/basic/shd_off")}',
                          f'execute if score @s apL matches 1.. run {F("org/nurt/lost_of")}'])
    g.w('org/basic/swallowed', ['# @s = the basic a 포식성 swallows (eat): gone silently, no progress, no burst; its link event fires.',
                                f'execute if score @s apL matches 1.. run {F("org/nurt/lost_of")}',
                                'execute on passengers run kill @s', 'kill @s'])
    g.w('org/basic/buff_on', ['# @s = a basic linked by a 양육: buffed look (bell buffed / bag_buffed), Heart hits -120, buffed coefficients.',
                              'tag @s add rlk_mb_ap_buff',
                              f'execute if entity @s[tag=rlk_mb_ap_lie] run return run {F("org/basic/look_bagb")}',
                              F('org/basic/look_buff')]
        + ([] if A.NURTURE_MODE == 'A' else ['tag @s add rlk_mb_ap_imm']))
    g.w('org/basic/buff_off', ['# @s = a basic whose 양육 died: the buff and its look gone.', 'tag @s remove rlk_mb_ap_buff', es('apL', 0),
                               f'execute if entity @s[tag=rlk_mb_ap_lie] run return run {F("org/basic/look_bag")}',
                               F('org/basic/look_bell')]
        + ([] if A.NURTURE_MODE == 'A' else ['tag @s remove rlk_mb_ap_imm']))
    for nm, look in (('look_buff', 'buffed'), ('look_bagb', 'bag_buffed'), ('look_bag', 'bag'), ('look_bell', 'bell')):
        g.w(f'org/basic/{nm}', [om('basic', f'look/{d}/{look}') for d in ('bulb', 'bulb_x', 'bulb_y')])

    # ================================================================ 수호 guard
    gcast = A.org_clip('guard', 'guard_cast')
    g.w('org/guard/enter', ['# The 수호 is solid: its first cast now.', F('org/guard/cast_go')])
    g.w('org/guard/cast_go', [es('apS', 1), es('apT', 0), om('guard', 'play/guard_cast'), f'execute at @s run {snd("o3_collapse")}'])
    g.w('org/guard/run', [
        f'# @s = a 수호 (immobile): 1 the cast (guard_cast: collapse 0, bud 7, regrow 16, shields {gcast["events"]["shields"]}), 2 idle; '
        f'recasts every {R["guard_recast"]} t on unshielded basics within r 10.',
        f'execute if score @s apS matches 1 run return run {F("org/guard/cast")}',
        'scoreboard players remove @s apTok 1',
        'execute if score @s apTok matches 1.. run return 0',
        f'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_shd,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,distance=..10] '
        f'run return run {F("org/guard/cast_go")}',
        es('apTok', 20)])
    g.w('org/guard/cast', [f'execute if score @s apT matches {gcast["events"]["regrow"]} at @s run {snd("o3_collapse")}',
                           f'execute if score @s apT matches {gcast["events"]["shields"]}.. run {F("org/guard/shields")}'])
    g.w('org/guard/shields', ['# The shields: every solid basic within r 10 without one (the orb flares; o3_cast).',
                              f'execute at @s run {snd("o3_cast")}',
                              'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_shd,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,'
                              f'distance=..10] run {F("org/basic/shd_on")}',
                              es('apS', 2), es('apTok', R['guard_recast'])])
    g.w('org/guard/die', ['# @s = a 수호 broken: guard_die (17 t), red embers + the black wisp; with no other 수호 alive every shield goes.',
                          om('guard', 'play/guard_die'), f'execute at @s positioned ~ ~1.5 ~ run {fx("guard_death")}',
                          f'execute at @s run {snd("o3_death")}',
                          'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_guard,tag=!rlk_mb_ap_dying] run return 0',
                          f'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=rlk_mb_ap_shd] run {F("org/basic/shd_pop")}'])
    g.w('org/basic/shd_pop', [F('org/basic/shd_off'), f'execute at @s positioned ~ ~0.8 ~ run {fx("shield_pop")}',
                              f'execute at @s run {snd("o3_pop")}'])

    # ================================================================ 양육 nurturing
    nb = A.org_clip('nurt', 'nurt_buff')
    teth = nb['events']['tethers']
    imm_self = A.NURTURE_MODE == 'A'
    g.w('org/nurt/enter', ['# The 양육 is solid (stationary on its r 7 point): its first link cast is due.', es('apTok', 0), es('apSock', 0),
                           F('org/nurt/imm')])
    g.w('org/nurt/run', [
        f'# @s = a 양육: links up to {R["nurt_links"]} basics within r 10 (nurt_buff tell {nb["len"]} t, tethers from {teth}); NURTURE_MODE '
        f'{A.NURTURE_MODE}: ' + ('immune itself (rlk_mb_ap_imm + the cylinder) while it holds >= 1 link (apSock = the links).'
                                 if imm_self else 'the buffed basics immune.'),
        f'execute if score #apClk8 mb matches 0 if score @s apSock matches 1.. run {F("org/nurt/tethers")}',
        f'execute if score #apClk40 mb matches 0 if score @s apSock matches 1.. at @s run {snd("o5_hum")}',
        f'execute if score @s apS matches 2 run return run {F("org/nurt/cast")}',
        'scoreboard players remove @s apTok 1',
        'execute if score @s apTok matches 1.. run return 0',
        f'execute if score @s apSock matches {R["nurt_links"]}.. run return run scoreboard players set @s apTok 20',
        f'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_buff,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,'
        f'tag=!rlk_mb_ap_prey,distance=..10] run return run {F("org/nurt/cast_go")}',
        es('apTok', 20)])
    imm = ['# The immunity (mode A) and the cylinder follow the link count.']
    if imm_self:
        imm += ['execute if score @s apSock matches 1.. run tag @s add rlk_mb_ap_imm',
                'execute unless score @s apSock matches 1.. run tag @s remove rlk_mb_ap_imm']
    imm += [f'execute if score @s apSock matches 1.. unless entity @s[tag=rlk_mb_ap_ring] run {F("org/nurt/ring_on")}',
            f'execute unless score @s apSock matches 1.. if entity @s[tag=rlk_mb_ap_ring] run {F("org/nurt/ring_off")}']
    g.w('org/nurt/imm', imm)
    g.w('org/nurt/ring_on', ['tag @s add rlk_mb_ap_ring', om('nurt', 'ring/on')])
    g.w('org/nurt/ring_off', ['tag @s remove rlk_mb_ap_ring', om('nurt', 'ring/off')])
    g.w('org/nurt/cast_go', [es('apS', 2), es('apT', 0), om('nurt', 'play/nurt_buff')])
    g.w('org/nurt/cast', [f'execute if score @s apT matches {teth} run {F("org/nurt/link")}',
                          f'execute if score @s apT matches {nb["len"]}.. run {F("org/nurt/cast_end")}'])
    g.w('org/nurt/cast_end', [es('apS', 1), es('apTok', R['nurt_relink'])])
    g.w('org/nurt/link', [
        '# The links (the cap tilted, the tethers from now): the nearest free basics within r 10, up to 3 links in all.',
        'scoreboard players operation #apX mb = @s apL',
        f'scoreboard players set #apY mb {R["nurt_links"]}', 'scoreboard players operation #apY mb -= @s apSock',
        'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_buff,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,'
        f'tag=!rlk_mb_ap_prey,distance=..10,sort=nearest,limit={R["nurt_links"]}] run {F("org/nurt/link1")}',
        f'scoreboard players set #apZ mb {R["nurt_links"]}', 'scoreboard players operation #apZ mb -= #apY mb',
        'scoreboard players operation @s apSock = #apZ mb', F('org/nurt/imm')])
    g.w('org/nurt/link1', ['# @s = a basic to link (#apY links left, #apX = the 양육\'s id).', 'execute if score #apY mb matches ..0 run return 0',
                           'scoreboard players operation @s apL = #apX mb', F('org/basic/buff_on'), 'scoreboard players remove #apY mb 1'])
    g.w('org/nurt/tethers', [
        '# @s = a linked 양육 (every 8 t, within the dust\'s 7-36 t life: the command budget at the cap, plan 7.6.4): a wavy',
        '# tether from its orb to each of its',
        '# basics (kit tether, len = the distance).',
        'scoreboard players operation #apX mb = @s apL', 'tag @s add rlk_mb_ap_me',
        'execute store result score #apNX mb run data get entity @s Pos[0] 10',
        'execute store result score #apNZ mb run data get entity @s Pos[2] 10',
        'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_buff] if score @s apL = #apX mb at @e[type=minecraft:husk,tag=rlk_mb_ap_me,'
        f'limit=1] positioned ~ ~2.0 ~ facing entity @s feet run {F("org/nurt/tether1")}',
        'tag @s remove rlk_mb_ap_me'])
    g.w('org/nurt/tether1', [
        '# @s = a linked basic; at the 양육 orb, rotated toward it: len ~ the horizontal distance (octagon estimate) + the drop.',
        'execute store result score #apDX mb run data get entity @s Pos[0] 10',
        'execute store result score #apDZ mb run data get entity @s Pos[2] 10',
        'scoreboard players operation #apDX mb -= #apNX mb', 'scoreboard players operation #apDZ mb -= #apNZ mb',
        'execute if score #apDX mb matches ..-1 run scoreboard players operation #apDX mb *= #apM1 mb',
        'execute if score #apDZ mb matches ..-1 run scoreboard players operation #apDZ mb *= #apM1 mb',
        'scoreboard players operation #apLn mb = #apDX mb', 'scoreboard players operation #apLn mb > #apDZ mb',
        'scoreboard players operation #apDX mb < #apDZ mb', 'scoreboard players operation #apDX mb *= #c2 mb',
        'scoreboard players operation #apDX mb /= #apC5 mb', 'scoreboard players operation #apLn mb += #apDX mb',
        'scoreboard players add #apLn mb 8',
        'execute store result storage rlk:mboss ap.o.len int 1 run scoreboard players get #apLn mb',
        f'function {K.FN}p/tether with storage rlk:mboss ap.o'])
    g.w('org/nurt/lost_of', [
        '# @s = a linked basic that died or was swallowed: its 양육 (apL) loses the link and 40 % of its max HP (the module break',
        '# on the 3rd: "자멸").', 'scoreboard players operation #apX mb = @s apL', es('apL', 0),
        f'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_nurt,tag=!rlk_mb_ap_dying] if score @s apL = #apX mb run {F("org/nurt/loss")}'])
    g.w('org/nurt/loss', [
        f'# @s = the 양육 that lost a link: one link fewer, -{R["nurt_loss_pct"]} % of its max HP (module mhpC); at 0 it self-destructs.',
        'scoreboard players remove @s apSock 1', 'execute if score @s apSock matches ..-1 run scoreboard players set @s apSock 0',
        'scoreboard players operation #apY mb = @s mhpM', f'scoreboard players set #apZ mb {R["nurt_loss_pct"]}',
        'scoreboard players operation #apY mb *= #apZ mb', 'scoreboard players operation #apY mb /= #c100 mb',
        'scoreboard players operation @s mhpC -= #apY mb', F('org/nurt/imm'),
        f'execute if score @s mhpC matches ..0 run {F("org/nurt/selfd")}'])
    g.w('org/nurt/selfd', ['# "자멸": the module break (aux/broke); org/broke pays REV kill next tick and plays the self-destruct.',
                           'tag @s add rlk_mb_ap_selfd', 'tag @s remove rlk_mb_ap_imm', 'function rlk:mboss/aux/broke'])
    g.w('org/nurt/die', ['# @s = a 양육 broken (killed, or its self-destruct): nurt_die (17 t); its basics lose the buff.',
                         om('nurt', 'play/nurt_die'), 'tag @s remove rlk_mb_ap_imm',
                         f'execute if entity @s[tag=rlk_mb_ap_ring] run {F("org/nurt/ring_off")}',
                         f'execute if entity @s[tag=rlk_mb_ap_selfd] at @s positioned ~ ~1.8 ~ run {fx("nurt_burst")}',
                         f'execute if entity @s[tag=rlk_mb_ap_selfd] at @s run {snd("o5_destruct")}',
                         f'execute unless entity @s[tag=rlk_mb_ap_selfd] at @s positioned ~ ~1.2 ~ run {fx("org_burst")}',
                         f'execute unless entity @s[tag=rlk_mb_ap_selfd] at @s run {snd("org_kill")}',
                         'scoreboard players operation #apX mb = @s apL', es('apSock', 0),
                         f'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_buff] if score @s apL = #apX mb run {F("org/basic/buff_off")}'])

    # ================================================================ 둥지 nesting
    blink = A.org_clip('nest', 'nest_blink')
    ncast = A.org_clip('nest', 'nest_cast')
    g.w('org/nest/enter', ['# The 둥지 is solid: flying, the first walls 60 t later.', es('apTok', R['nest_first'])])
    g.w('org/nest/run', [
        f'# @s = a 둥지: 1 flying (keeps {NEST_KEEP[0]:g}-{NEST_KEEP[1]:g} b from the player at {SPD["nest"]} b/t; blinks to {NEST_BLINK[1]:g} b when '
        f'> {NEST_BLINK[0]:g} b), 2 the wall cast',
        f'# ({ncast["len"]} t loop pose = the tell; walls at {ncast["events"]["walls"]}), 3 the blink ({blink["len"]} t). No attack.',
        f'execute if score @s apS matches 2 run return run {F("org/nest/cast")}',
        f'execute if score @s apS matches 3 run return run {F("org/nest/blink")}',
        F('org/nest/fly')])
    g.w('org/nest/fly', [
        f'execute unless entity @e[tag=rlk_body,distance=..{n(NEST_BLINK[0])}] run return run {F("org/nest/blink_go")}',
        f'execute unless entity @e[tag=rlk_body,distance=..{n(NEST_KEEP[1])}] {PL_FACE} run {step(SPD["nest"])}',
        f'execute if entity @e[tag=rlk_body,distance=..{n(NEST_KEEP[0])}] {PL_FACE} rotated ~180 0 run {step(SPD["nest"])}',
        f'function {NS}org/nest/push_out', f'execute at @s {PL_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~', f'function {NS}om/face',
        'scoreboard players operation #apM mb = @s apT', 'scoreboard players operation #apM mb %= #apC14 mb',
        f'execute if score #apM mb matches 0 at @s run {snd("o4_flap")}',
        'scoreboard players remove @s apTok 1',
        'execute if score @s apTok matches 1.. run return 0',
        '# never while a 파괴 is within 6 b of the Heart or fusing, never during a 포식성 bite chain',
        F('org/nest/flags'),
        'execute if score #apDNear mb matches 1 run return run scoreboard players set @s apTok 10',
        'execute if score #apPChain mb matches 1 run return run scoreboard players set @s apTok 10',
        f'execute unless score #apPh mb matches 2 run return run scoreboard players set @s apTok 10',
        F('org/nest/cast_go')])
    g.w('org/nest/flags', ['# The cast blockers (only when a cast is due): a 파괴 within 6 b of the Heart (fusing ones sit at r 2.6), a 포식성',
                           '# in a bite chain (apS 6).', sc('#apDNear', 0), sc('#apPChain', 0),
                           f'execute positioned {CEN} if entity @e[type=minecraft:husk,tag=rlk_mb_ap_destr,tag=!rlk_mb_ap_dying,distance=..6] '
                           'run scoreboard players set #apDNear mb 1',
                           'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_pred,scores={apS=6}] run scoreboard players set #apPChain mb 1'])
    g.w('org/nest/push_out', [f'# Never over the cradle: pushed out to r {n(WALL_EX)} of the Heart.',
                              f'execute positioned {CEN} if entity @s[distance=..{n(WALL_EX - 0.01)}] facing entity @s feet rotated ~ 0 '
                              f'positioned ^ ^ ^{n(WALL_EX)} run tp @s ~ {CY} ~'])
    g.w('org/nest/cast_go', [
        '# The wall cast (O4): nest_cast; the spots are locked now at the player\'s feet and facing (no decal: the loop pose is the',
        '# tell, plan 14); 30 %: one arc ahead of the player instead of three groups round them.',
        es('apS', 2), es('apT', 0), om('nest', 'play/nest_cast'),
        'kill @e[type=minecraft:marker,tag=rlk_mb_ap_new]',
        f'execute at {PLAYER} rotated as {PLAYER} rotated ~ 0 run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux",'
        '"rlk_mb_ap_om","rlk_mb_ap_wlock","rlk_mb_ap_new"]}',
        f'execute at {PLAYER} rotated as {PLAYER} rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_mb_ap_new,limit=1] run tp @s ~ {CY} ~ ~ 0',
        'scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_ap_new] apL = @s apL',
        'execute store result score #apR mb run random value 0..99',
        'execute if score #apR mb matches ..29 run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apS 1',
        'execute if score #apR mb matches 30.. run scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apS 0',
        'tag @e[type=minecraft:marker,tag=rlk_mb_ap_new] remove rlk_mb_ap_new'])
    g.w('org/nest/cast', [f'execute if score @s apT matches {ncast["events"]["walls"]}.. run {F("org/nest/walls")}'])
    g.w('org/nest/walls', ['# t12: the walls rise from the locked spots; flying again, the next cast 160 t later.',
                           'scoreboard players operation #apX mb = @s apL',
                           f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wlock] if score @s apL = #apX mb at @s run {F("wall/raise")}',
                           es('apS', 1), es('apTok', R['nest_every'])])
    g.w('org/nest/abort', ['# @s = a 둥지 whose cast was cut (pause): its lock gone, flying, re-cast later.',
                           'scoreboard players operation #apX mb = @s apL',
                           'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wlock] if score @s apL = #apX mb run kill @s',
                           es('apS', 1), es('apTok', R['nest_first']), om('nest', 'play/nest_fly')])
    g.w('org/nest/blink_go', [es('apS', 3), es('apT', 0), om('nest', 'play/nest_blink'),
                              f'execute at @s positioned ~ ~1.2 ~ run {fx("blink_flash")}'])
    g.w('org/nest/blink', [
        f'# The blink: out 0-2, moved at {blink["events"]["in"]} to {NEST_BLINK[1]:g} b from the player (on the player -> 둥지 line, inside the walk',
        '# disc, off the cradle), in 3-6.',
        f'execute if score @s apT matches {blink["events"]["in"]} at {PLAYER} facing entity @s feet rotated ~ 0 positioned ^ ^ ^{n(NEST_BLINK[1])} '
        f'run tp @s ~ {CY} ~',
        f'execute if score @s apT matches {blink["events"]["in"]} run function rlk:mboss/ar/clampw',
        f'execute if score @s apT matches {blink["events"]["in"]} run {F("org/nest/push_out")}',
        f'execute if score @s apT matches {blink["events"]["in"]} at @s {PL_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~',
        f'execute if score @s apT matches {blink["events"]["in"]} run function {NS}om/face',
        f'execute if score @s apT matches {blink["events"]["in"]} at @s positioned ~ ~1.2 ~ run {fx("blink_flash")}',
        f'execute if score @s apT matches {blink["len"]}.. run scoreboard players set @s apS 1'])
    g.w('org/nest/die', [om('nest', 'play/org_die'), f'execute at @s positioned ~ ~1.2 ~ run {fx("org_burst")}',
                         f'execute at @s run {snd("org_kill")}',
                         'scoreboard players operation #apX mb = @s apL',
                         'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wlock] if score @s apL = #apX mb run kill @s'])

    # ================================================================ 파괴 destruction
    o7 = HZ['o7']
    fuse = A.org_clip('destr', 'destr_fuse')
    suck = A.org_clip('destr', 'destr_suck')
    pulses = sorted({fuse['events'][e] for e in fuse['events'] if e.startswith('pulse')} | set(range(fuse['events']['fast'], fuse['len'], 4)))
    g.w('org/destr/enter', ['# The 파괴 is solid: it rolls to the Heart.'])
    g.w('org/destr/run', [
        f'# @s = a 파괴: 1 rolling to the nearest stop (r {DSTOP_R:g} off the socket bearings) at {SPD["destr"]} b/t, 2 the fuse (contact + '
        f'{o7["tell"]}: the blast).',
        f'execute if score @s apS matches 2 run return run {F("org/destr/fuse")}',
        f'execute if entity @e[type=minecraft:marker,tag=rlk_mb_ap_dstop,distance=..0.2] run return run {F("org/destr/contact")}',
        f'execute facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_dstop,sort=nearest,limit=1] feet run {step(SPD["destr"])}',
        f'function {NS}om/face',
        'scoreboard players operation #apM mb = @s apT', 'scoreboard players operation #apM mb %= #apK8 mb',
        f'execute if score #apM mb matches 0 at @s run {snd("o7_roll")}'])
    g.w('org/destr/contact', [
        f'# Contact: on the stop, facing the Heart; destr_fuse ({fuse["len"]} t) -> destr_suck ({suck["len"]}) -> the blast at contact + {o7["tell"]}:',
        f'# the blast disc r {o7["r"]} (quiet, made now with its {o7["tell"]} t tell; the fuse is the tell), the primed sound, the first pulse.',
        'tp @s @e[type=minecraft:marker,tag=rlk_mb_ap_dstop,sort=nearest,limit=1]', f'execute at @s {HEART_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~',
        f'function {NS}om/face',
        es('apS', 2), es('apT', 0), om('destr', 'play/destr_fuse'), f'execute at @s run {snd("o7_primed")}',
        f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run {fx("fuse_pulse")}',
        'scoreboard players operation #apX mb = @s apL',
        f'execute at @s positioned ~ {CY} ~ run {F("org/destr/hz")}'])
    g.w('org/destr/hz', [*hz(kb=o7['kb']), L.hz_disc(o7['r'], o7['tell'], o7['dmg']),
                         'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_ap_ohz',
                         'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run scoreboard players operation '
                         '@s apL = #apX mb'])
    fz = [f'# The fuse: pulses at {pulses}, the suck at {fuse["len"]}, the blast at {o7["tell"]}.']
    fz += [f'execute if score @s apT matches {t} at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^0.55 run {fx("fuse_pulse")}'
           for t in pulses if t > 0]
    fz += [f'execute if score @s apT matches {fuse["len"]} at @s run {snd("o7_suck")}',
           f'execute if score @s apT matches {o7["tell"]}.. run {F("org/destr/blast")}']
    g.w('org/destr/fuse', fz)
    g.w('org/destr/blast', [
        f'# The blast: the Heart -{o7["heart"]} (no progress for it), the green dome + sounds; it is spent (no pay) and tumbles away.',
        f'function {NS}heart/sub {{v:{o7["heart"]}}}', f'execute at @s run {snd("o7_blast")}',
        f'execute at @s positioned ~ {CY} ~ run {fx("blast_dome")}',
        'tag @s add rlk_mb_ap_spent', 'tag @s add rlk_mb_ap_dying', 'tag @s add rlk_mb_inv', es('apT', 0),
        om('destr', 'play/org_die')])
    g.w('org/destr/die', ['# @s = a 파괴 broken before the blast: its blast hazard is cancelled; the burst; org_die.',
                          'scoreboard players operation #apX mb = @s apL',
                          'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_ohz] if score @s apL = #apX mb run kill @s',
                          om('destr', 'play/org_die'), f'execute at @s positioned ~ ~0.6 ~ run {fx("org_burst")}',
                          f'execute at @s run {snd("org_kill")}'])

    # ================================================================ 포식성 predatory
    o6a, o6b = HZ['o6a'], HZ['o6b']
    sw = A.org_clip('pred', 'pred_swallow')
    eat = sw['events']['eat']
    PREY = ('@e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,tag=!rlk_mb_ap_prey,sort=nearest,limit=1]')
    g.w('org/pred/enter', ['# The 포식성 is solid: to the nearest basic (to swallow it), or, with none, it circles un-empowered.',
                           F('org/pred/decide')])
    g.w('org/pred/decide', [f'execute if entity {PREY} run return run scoreboard players set @s apS 1', F('org/pred/circle_go')])
    g.w('org/pred/circle_go', [es('apS', 4), es('apT', 0), 'execute store result score @s apTok run random value 40..60',
                               es('apSock', 1), om('pred', 'play/pred_swim')])
    g.w('org/pred/run', [
        '# @s = a 포식성: 1 seek a basic, 2 swallow -> bud -> inflate -> burst (O6a), 4 circle the player 3-5 b, 6 a bite chain (O6b,',
        '# apSock 1 / 2), 7 a single bite, 9 the gap before chain 2. The fish hovers 1.2 b up (the model).',
        f'execute if score @s apS matches 1 run return run {F("org/pred/seek")}',
        f'execute if score @s apS matches 2 run return run {F("org/pred/swallow")}',
        f'execute if score @s apS matches 6 run return run {F("org/pred/chain")}',
        f'execute if score @s apS matches 7 run return run {F("org/pred/single")}',
        f'execute if score @s apS matches 9 run return run {F("org/pred/gap")}',
        F('org/pred/circle')])
    g.w('org/pred/seek', [
        f'# Swimming at {SPD["pred"]} b/t to the nearest basic; at <= {PRED_REACH} b it swallows it.',
        f'execute unless entity {PREY} run return run {F("org/pred/circle_go")}',
        f'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,tag=!rlk_mb_ap_prey,'
        f'distance=..{n(PRED_REACH)}] run return run {F("org/pred/swallow_go")}',
        f'execute facing entity {PREY} feet run {step(SPD["pred"])}', F('org/basic/push_in'), f'function {NS}om/face',
        F('org/pred/swim_snd')])
    g.w('org/pred/swim_snd', ['scoreboard players operation #apM mb = @s apT', 'scoreboard players operation #apM mb %= #apC16 mb',
                              f'execute if score #apM mb matches 0 at @s run {snd("o6_swim")}'])
    g.w('org/pred/swallow_go', [
        f'# The swallow (pred_swallow {sw["len"]} t: rear 0-6, scoop 6-12, the basic removed at {eat}): the basic is held (its slot freed).',
        f'execute as {PREY} run {F("org/pred/hold")}',
        'execute at @s facing entity @e[type=minecraft:husk,tag=rlk_mb_ap_prey,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~',
        f'function {NS}om/face',
        es('apS', 2), es('apT', 0), om('pred', 'play/pred_swallow')])
    g.w('org/pred/hold', ['# @s = the basic being swallowed: held (no AI), its slot / socket freed.', 'tag @s add rlk_mb_ap_prey', es('apS', 8),
                          'tag @s remove rlk_mb_ap_tok', 'tag @s remove rlk_mb_ap_sk0', 'tag @s remove rlk_mb_ap_sk1',
                          'tag @s remove rlk_mb_ap_sk2'])
    g.w('org/pred/swallow', [
        f'# eat {eat} (gulp: no progress, its link event), the bud {eat}-{o6a["made"]}, inflate {o6a["made"]}-{o6a["hit"]} (the tell), the burst '
        f'{o6a["hit"]} (O6a r {o6a["r"]}).',
        f'execute if score @s apT matches {eat} run {F("org/pred/eat")}',
        f'execute if score @s apT matches {o6a["made"]} run {F("org/pred/inflate")}',
        f'execute if score @s apT matches {o6a["hit"]}.. run {F("org/pred/burst")}'])
    g.w('org/pred/eat', [
        '# The nearest held basic is eaten (silently); none left (killed meanwhile): no burst, it circles un-empowered.',
        f'execute unless entity @e[type=minecraft:husk,tag=rlk_mb_ap_prey,distance=..4] run return run {F("org/pred/circle_go")}',
        f'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_prey,distance=..4,sort=nearest,limit=1] run {F("org/basic/swallowed")}',
        'tag @s add rlk_mb_ap_pemp', f'execute at @s run {snd("o6_gulp")}', f'execute at @s run {snd("o6_bud")}'])
    g.w('org/pred/inflate', [om('pred', 'play/pred_inflate'), f'execute at @s run {snd("o6_inflate")}',
                             f'execute at @s positioned ~ {CY} ~ run {F("org/pred/hz_burst")}'])
    g.w('org/pred/hz_burst', [*hz(kb=o6a['kb']), L.hz_disc(o6a['r'], o6a['tell'], o6a['dmg']), Gen.tag_last_hz('rlk_mb_ap_ohz')])
    g.w('org/pred/burst', [f'execute at @s positioned ~ ~1.0 ~ run {fx("pred_burst")}', f'execute at @s run {snd("o6_burst")}',
                           F('org/pred/circle_go')])
    g.w('org/pred/circle', [
        f'# Circling the player at {PRED_RING[0]:g}-{PRED_RING[1]:g} b ({SPD["pred"]} b/t) until the next chain (apTok).',
        F('org/pred/orbit'),
        'scoreboard players remove @s apTok 1',
        f'execute if score @s apTok matches ..0 run {F("org/pred/chain_go")}'])
    g.w('org/pred/orbit', [
        f'execute unless entity @e[tag=rlk_body,distance=..{n(PRED_RING[1])}] {PL_FACE} run {step(SPD["pred"])}',
        f'execute if entity @e[tag=rlk_body,distance=..{n(PRED_RING[0])}] {PL_FACE} rotated ~180 0 run {step(SPD["pred"])}',
        f'execute if entity @e[tag=rlk_body,distance={n(PRED_RING[0])}..{n(PRED_RING[1])}] {PL_FACE} rotated ~90 0 run {step(SPD["pred"])}',
        F('org/basic/push_in'), f'execute at @s {PL_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~', f'function {NS}om/face',
        F('org/pred/swim_snd')])
    bite_dmg = {True: list(o6b['chain']), False: [unemp(v) for v in o6b['chain']]}
    single_dmg = {True: o6b['single'], False: unemp(o6b['single'])}
    g.w('org/pred/chain_go', [
        f'# A bite chain (O6b): the chain-start flare now (fish_flare + o6_swim) = the tell, {CHAIN_HITS[0]} t before bite 1; it closes to',
        f'# {PRED_CLOSE:g} b over 1-3; sectors r {o6b["r"]} half {o6b["a"]} locked at the player {o6b["tell"]} t before each bite at {CHAIN_HITS}.',
        es('apS', 6), es('apT', 0), f'execute at @s {PL_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~', f'function {NS}om/face',
        om('pred', 'look/body/fish_flare'), om('pred', 'look/body_x/fish_flare'), f'execute at @s run {snd("o6_swim")}'])
    ch = [f'# The chain (apSock 1 / 2): close in 1-3, sectors at {[t - o6b["tell"] for t in CHAIN_HITS]}, pred_bite_chain at '
          f'{CHAIN_HITS[0] - BITE_CLIP_LEAD} (snaps on the bites), bites (lunge 1.5 b) at {CHAIN_HITS}.',
          f'execute if score @s apT matches 1..2 unless entity @e[tag=rlk_body,distance=..{n(PRED_CLOSE)}] {PL_FACE} run {step(PRED_DASH)}',
          f'execute if score @s apT matches 1..2 run {F("org/basic/push_in")}',
          f'execute if score @s apT matches {CHAIN_HITS[0] - BITE_CLIP_LEAD} run {om("pred", "play/pred_bite_chain")}']
    for i, t in enumerate(CHAIN_HITS):
        ch.append(f'execute if score @s apT matches {t - o6b["tell"]} run {F(f"org/pred/bite_hz{i}")}')
        ch.append(f'execute if score @s apT matches {t} run {F("org/pred/bite_hit" + ("1" if i == 0 else ""))}')
    ch.append(f'execute if score @s apT matches {CHAIN_HITS[-1]}.. run {F("org/pred/chain_end")}')
    g.w('org/pred/chain', ch)
    for i in range(len(CHAIN_HITS)):
        g.w(f'org/pred/bite_hz{i}', [f'# Bite {i + 1} of the chain: the sector locked at the player now (the fish turns to it).',
                                     f'execute at @s {PL_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~', f'function {NS}om/face',
                                     f'execute if entity @s[tag=rlk_mb_ap_pemp] at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run '
                                     f'{F(f"org/pred/hzb_e{i}")}',
                                     f'execute unless entity @s[tag=rlk_mb_ap_pemp] at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run '
                                     f'{F(f"org/pred/hzb_u{i}")}'])
        for emp in (True, False):
            g.w(f'org/pred/hzb_{"e" if emp else "u"}{i}', [*hz(kb=o6b['kb']), L.hz_sector(o6b['r'], o6b['a'], o6b['tell'], bite_dmg[emp][i]),
                                                          Gen.tag_last_hz('rlk_mb_ap_ohz')])
    for emp in (True, False):
        g.w(f'org/pred/hzs_{"e" if emp else "u"}', [*hz(kb=o6b['kb']), L.hz_sector(o6b['r'], o6b['a'], o6b['tell'], single_dmg[emp]),
                                                    Gen.tag_last_hz('rlk_mb_ap_ohz')])
    for nm, s in (('bite_hit1', 'o6_bite_first'), ('bite_hit', 'o6_bite')):
        g.w(f'org/pred/{nm}', ['# A bite: the 1.5 b lunge along the locked aim, the white-yellow bite flash, the bite sound.',
                               f'execute rotated as @s rotated ~ 0 run {step(1.5)}', F('org/basic/push_in'),
                               f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^1.0 ^1.2 run {fx("bite_flash")}',
                               f'execute at @s run {snd(s)}'])
    g.w('org/pred/chain_end', [
        '# After chain 1: one single bite 14 t after its last bite, then 12 t, then chain 2; after chain 2: a single bite every 60 t.',
        om('pred', 'look/body/fish'), om('pred', 'look/body_x/fish'),
        es('apS', 7), es('apT', 0),
        f'execute if score @s apSock matches 1 run scoreboard players set @s apTok {SINGLE_HIT}',
        'execute if score @s apSock matches 2 run scoreboard players set @s apTok 60',
        'execute if score @s apSock matches 2 run scoreboard players set @s apSock 3'])
    g.w('org/pred/single', [
        f'# A single bite at apTok: the lunge prep from apTok - 12 (the flare + o6_swim, it dashes in to {PRED_CLOSE:g} b in 2 t), the sector',
        '# locked at apTok - 10, pred_bite at apTok - 4 (snap 4), the bite at apTok. Before the prep it circles.',
        'scoreboard players operation #apX mb = @s apTok', 'scoreboard players remove #apX mb 12',
        f'execute if score @s apT < #apX mb run return run {F("org/pred/orbit")}',
        f'execute if score @s apT = #apX mb run {F("org/pred/single_cue")}',
        'scoreboard players add #apX mb 2',
        f'execute if score @s apT < #apX mb unless entity @e[tag=rlk_body,distance=..{n(PRED_CLOSE)}] {PL_FACE} run {step(PRED_DASH)}',
        F('org/basic/push_in'),
        f'execute if score @s apT = #apX mb run {F("org/pred/single_hz")}',
        'scoreboard players add #apX mb 6',
        f'execute if score @s apT = #apX mb run {om("pred", "play/pred_bite")}',
        f'execute if score @s apT >= @s apTok run {F("org/pred/single_hit")}'])
    g.w('org/pred/single_cue', ['# The single bite\'s readable start (12 t before it): the spikes flare, the swim cue, facing the player.',
                                f'execute at @s {PL_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~', f'function {NS}om/face',
                                om('pred', 'look/body/fish_flare'), om('pred', 'look/body_x/fish_flare'), f'execute at @s run {snd("o6_swim")}'])
    g.w('org/pred/single_hz', ['# The single bite\'s sector, locked at the player (the fish turns to it).',
                               f'execute at @s {PL_FACE} rotated ~ 0 run tp @s ~ ~ ~ ~ ~', f'function {NS}om/face',
                               f'execute if entity @s[tag=rlk_mb_ap_pemp] at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run {F("org/pred/hzs_e")}',
                               f'execute unless entity @s[tag=rlk_mb_ap_pemp] at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run {F("org/pred/hzs_u")}'])
    g.w('org/pred/single_hit', [F('org/pred/bite_hit'), om('pred', 'look/body/fish'), om('pred', 'look/body_x/fish'),
                                f'execute if score @s apSock matches 1 run return run {F("org/pred/gap_go")}',
                                es('apT', 0), es('apTok', 60)])
    g.w('org/pred/gap_go', [es('apS', 9), es('apT', 0)])
    g.w('org/pred/gap', ['# 12 t after the single bite: chain 2.', F('org/pred/orbit'),
                         'execute if score @s apT matches 12.. run scoreboard players set @s apSock 2',
                         f'execute if score @s apT matches 12.. run {F("org/pred/chain_go")}'])
    g.w('org/pred/die', ['# @s = a 포식성 broken: its prey (held, not yet eaten) is freed; org_die; the burst.',
                         'execute as @e[type=minecraft:husk,tag=rlk_mb_ap_prey,distance=..4,sort=nearest,limit=1] run '
                         f'{F("org/pred/release")}',
                         om('pred', 'play/org_die'), f'execute at @s positioned ~ ~1.2 ~ run {fx("org_burst")}',
                         f'execute at @s run {snd("org_kill")}'])
    g.w('org/pred/release', ['tag @s remove rlk_mb_ap_prey', es('apS', 1), es('apT', 0)])

    # ================================================================ the walls (O4)
    walls_r, walls_r1 = 4.2, 3.6
    arc_half, blade_off = 30, 20
    raise_ = [HEAD, '# @s = a wall lock (the player\'s feet and facing at the cast start), at it, rotated as it: a new wall group (marker',
              f'# rlk_mb_ap_wall, its clock and id) and, by the lock\'s variant: 0 = three groups 120 deg apart at r {walls_r} round the feet,',
              f'# 1 = one arc at r {walls_r1} ahead; each group 3 blades over a 60 deg arc and barrier blocks along the arc (y 201-202).',
              'scoreboard players add #apWid mb 1',
              f'summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_wall","rlk_mb_ap_new"]}}',
              'scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_ap_new] apL = #apWid mb',
              'scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_new] apT 0',
              'tag @e[type=minecraft:marker,tag=rlk_mb_ap_new] remove rlk_mb_ap_new',
              f'execute if score @s apS matches 1 run function {NS}wall/arc1',
              f'execute unless score @s apS matches 1 run function {NS}wall/arc3',
              f'execute at @s run {snd("o4_rise")}', 'kill @s']
    g.w('wall/raise', raise_)
    for nm, groups, r in (('arc3', (0, 120, 240), walls_r), ('arc1', (0,), walls_r1)):
        lines = [f'# @s = the lock, at it: {len(groups)} group(s) at r {r}: blades at -{blade_off} / 0 / +{blade_off} deg, cells every 5 deg over '
                 f'+-{arc_half} deg.']
        for g0 in groups:
            for a in (-blade_off, 0, blade_off):
                lines.append(f'execute rotated ~{g0 + a} 0 positioned ^ ^ ^{n(r)} run function {NS}wall/blade')
            for a in range(-arc_half, arc_half + 1, 5):
                lines.append(f'execute rotated ~{g0 + a} 0 positioned ^ ^ ^{n(r)} align xz positioned ~0.5 {CY} ~0.5 run function {NS}wall/cell')
        g.w(f'wall/{nm}', lines)
    g.w('wall/blade', ['# A blade at a spot (facing outward = its face to the locked feet): only inside the walk disc and off the cradle.',
                       f'execute unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..{n(float(A.ARENA['walk']) - 1.0)}] run return 0',
                       f'execute if entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,distance=..{n(WALL_EX + 0.5)}] run return 0',
                       f'execute positioned ~ {CY} ~ run function {NS}om/wall/spawn',
                       'scoreboard players operation @e[type=minecraft:item_display,tag=rlk_ap_om_new,limit=1] apL = #apWid mb',
                       'tag @e[type=minecraft:item_display,tag=rlk_ap_om_new] remove rlk_ap_om_new'])
    cell_x = WALL_EX + 0.71
    g.w('wall/cell', [
        '# A barrier cell (at its centre, y 201): phase 2 only; inside the walk disc; no part inside the Heart\'s wall exclusion',
        f'# r {WALL_EX}; never in the player\'s body box + 1 b (the volume test); never within 1 b of an organism; replace air only;',
        '# each placed block recorded (rlk_mb_ap_wallb, the group id).',
        'execute unless score #apPh mb matches 2 run return 0',
        f'execute unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..{n(float(A.ARENA['walk']) - 1.0)}] run return 0',
        f'execute if entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,distance=..{n(cell_x)}] run return 0',
        'execute positioned ~-1.5 200 ~-1.5 if entity @e[tag=rlk_body,dx=2,dy=3,dz=2] run return 0',
        'execute positioned ~-1.5 200 ~-1.5 if entity @a[tag=player,dx=2,dy=3,dz=2] run return 0',
        'execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_org,distance=..1.5] run return 0',
        f'execute positioned ~ {CY} ~ if block ~ ~ ~ minecraft:air run function {NS}wall/put',
        f'execute positioned ~ {CY + 1} ~ if block ~ ~ ~ minecraft:air run function {NS}wall/put'])
    g.w('wall/put', ['setblock ~ ~ ~ minecraft:barrier',
                     'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_wallb","rlk_mb_ap_new"]}',
                     'scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_ap_new] apL = #apWid mb',
                     'tag @e[type=minecraft:marker,tag=rlk_mb_ap_new] remove rlk_mb_ap_new'])
    wrise, wfade = A.org_clip('wall', 'wall_rise'), A.org_clip('wall', 'wall_fade')
    life = 40
    g.w('wall/tick', [
        f'# Any executor, every phase-2 tick: each group\'s clock: stand {life} t, then its blocks go (exactly the recorded ones)',
        f'# and the blades dissolve ({wfade["len"]} t, motes). The core steps the blade clips (obj/tick, AP-I2 RREV-1).',
        f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wall] run {F("wall/group")}'])
    g.w('wall/group', ['scoreboard players add @s apT 1',
                       f'execute if score @s apT matches {life} run {F("wall/dissolve")}',
                       f'execute if score @s apT matches {life + wfade["len"]}.. run {F("wall/gone")}'])
    g.w('wall/dissolve', ['# @s = a wall group: its blocks removed (only the recorded ones that are still barrier), the blades fade.',
                          'scoreboard players operation #apX mb = @s apL',
                          f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wallb] if score @s apL = #apX mb at @s run {F("wall/unput")}',
                          f'execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_wall_blade] if score @s apL = #apX mb run {F("wall/fade1")}',
                          f'execute at @s run {snd("o4_fade")}'])
    g.w('wall/fade1', [f'function {NS}om/wall/play/wall_fade', f'execute at @s positioned ~ ~1.2 ~ run {fx("wall_motes")}'])
    g.w('wall/unput', ['execute if block ~ ~ ~ minecraft:barrier run setblock ~ ~ ~ minecraft:air', 'kill @s'])
    g.w('wall/gone', ['scoreboard players operation #apX mb = @s apL',
                      'execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_wall_blade] if score @s apL = #apX mb run kill @s',
                      'kill @s'])
    g.w('wall/clear', [HEAD, '# Every wall (pause, reload, cleanup, death, the CS, a failure strike, the phase jumps; idempotent, any executor):',
                       '# the recorded blocks first, then the blades, groups and locks; then the arena\'s barrier safety sweep (FN-26;',
                       '# its spans stay inside walk - 0.5, the rim barrier is never touched).',
                       f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wallb] at @s run {F("wall/unput")}',
                       f'function {NS}om/wall/kill_all', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_wall]',
                       'kill @e[type=minecraft:marker,tag=rlk_mb_ap_wlock]',
                       f'function rlk:mboss/arena/{A.AID}/sweep {{y0:{A.ARENA["sweep"]["y0"]},y1:{A.ARENA["sweep"]["y1"]}}}'])
    assert walls_r + 0.5 > 0 and wrise['len'] == 5
