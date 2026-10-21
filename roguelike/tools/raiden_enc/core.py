"""Raiden encounter core: helpers, balance constants, lifecycle, AI host (bag/choose/finish), damage in/out,
objects, blink helpers and the boss test commands. Owner: S2-SHOGUN (plan rd/plan.md E.0); the phase modules
(shogun.py, tenma.py) hand their bag, reach and tick/choose hooks in as data, so this file never names a phase-2 move.
Split out of the old monolithic build_raiden_encounter.py by S0 with byte-identical output; S2-SHOGUN: no walking
(idle 16 t, blink-only close-in), phase-0 timelines run from rdTime 0, the rig hides through rig/state/hidden, and the
phase-0 AI (shogun.py, F:boss/raiden/sg/) is called through the sg/* hooks.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'data/rlk/function/boss/raiden'
def write(name, lines):
    p = BASE/(name+'.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text((lines.strip() if isinstance(lines,str) else '\n'.join(lines))+'\n',encoding='utf-8')
def call(name): return 'function rlk:boss/raiden/'+name
def at(t,cmd): return cmd if cmd.startswith('#') else f'execute if score @s rdTime matches {t} at @s rotated as @s run {cmd}'
def sound(event,vol=1,pitch=.8):
    return f'playsound minecraft:{event} hostile @a[tag=player] ~ ~ ~ {vol} {pitch} 0.3'
def caption(text):
    return '# Pattern names intentionally stay out of the boss bar.'
def obj(kind,model,hp,oid,y=0):
    return call('object/create')+f' {{kind:{kind},model:"{model}",hp:{hp},id:{oid},y:{y}}}'

# ---- Lightning armor tuning --------------------------------------------------
# A continuously attacking player lands at most one armor drain per SHIELD_CD ticks
# (20/5 = 4 drains per second, multi-hit and DoT spam included); the armor also decays
# by 1 every 4 ticks (5 per second) except during the flower ultimate.
#   passive only      750 / 5            = 150 s
#   physical/thunder  750 / (5 + 4*2)    = 57.7 s
#   water/rock/wind   750 / (5 + 4*3)    = 44.1 s
#   grass             750 / (5 + 4*4)    = 35.7 s
#   fire/ice          750 / (5 + 4*6)    = 25.9 s
# A successful flower defence removes 190 (25% of the armor).
SHIELD_MAX = 750
SHIELD_CD = 5
FLOWER_BREAK = 190
# #elem: 0 physical 1 fire 2 water 3 thunder 4 ice 5 rock 6 wind 7 grass 8 void.
DRAIN_DEFAULT = 2
DRAIN = {1:6, 4:6, 2:3, 5:3, 6:3, 7:4}
DRAIN_REACTION = 1
# Malice energy: normal-phase ticks before the transformation (45 s, was 30 s).
RAGE_MAX = 900
# Like the original, every hit the boss lands also feeds the malice gauge (+3 s).
RAGE_HIT = 60
# Armour-break stun (original: about 15 s of collapse before she recovers).
EXHAUST = 300
# Transformation: scatter to the centre, then the transformation burst/clip.
TRANSFORM_FX = 1
TRANSFORM_LEN = 60              # the bar's fallback; tenma.T_LEN is the real length
# Close-range patterns and their reach: chosen farther than `start` blocks from the player (or nearer than
# REACH_MIN), she blinks to REACH_SPOT blocks in front of them (no walking, plan A.2) before the clock starts.
# The per-pattern reach tables are REACH / REACH_SPOT / REACH_MIN in shogun.py / tenma.py (merged in build()); the
# Shogun rows blink inside their own timelines instead.

objectives = ['rd','rdPhase','rdPat','rdTime','rdRage','rdShield','rdCycle','rdCool','rdPrev','rdTurns','rdHitCD','rdObjKind','rdObjId','rdObjHP','rdReal','rdOAge','rdPTime','rdShape','rdWind','rdHAge','rdHLife','rdDamage','rdHHit','rdFX','rdFZ','rdHId','rdVId','rdUltUsed','rdWalk','rdWalkDir','rdBlink','rdCam','rdDeath','rdDeathTime','rdHidden','rdGo','rdNext','rdWpn']

# ---- Pattern timeline helpers (shogun.py / tenma.py) -----------------------------
patterns = {}  # id -> timeline lines, filled by shogun.build() / tenma.build()
def pattern(i,title):
    lines=[at('1',caption(title))];patterns[i]=lines;return lines
def end(lines,t): lines.append(at(str(t),call('finish')))
face='execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet'
flat='execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0'
target='execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run '
center='execute at @e[tag=rlk_raiden_arena,limit=1] run '


def _rng(r): return r.replace('..', '~')


def build(shogun, tenma):
    """Write the core functions. shogun / tenma: the phase modules. Data they hand in (M1 seams, rd/s2_notes.md §3):
    BAG, REACH, TICK_HIDE, TICK_TAIL, CHOOSE_RULES (tenma), IDS (pattern id ranges of the phase, e.g. ['1..7']),
    OBJECTIVES (extra scoreboard objectives), ON_PAUSE / ON_FINISH (commands appended to pause / finish), and the
    optional close-in dicts REACH_SPOT {pid: d} (land d blocks in front of the player, toward her) and REACH_MIN
    {pid: lo} (also reposition when the player is nearer than lo). The phase-0 AI (bags, range fit, forced and
    reactive picks, guard, stuns, after-effects) lives in shogun.py under F:boss/raiden/sg/; core calls it through
    sg/{setup,reload,pause,choose,picked,incoming,tick,fx_off,stun_tick,rig_hide,rig_show,idle_clip}."""
    REACH = {**shogun.REACH, **tenma.REACH}
    REACH_SPOT = {**getattr(shogun, 'REACH_SPOT', {}), **getattr(tenma, 'REACH_SPOT', {})}
    REACH_MIN = {**getattr(shogun, 'REACH_MIN', {}), **getattr(tenma, 'REACH_MIN', {})}
    S_IDS, T_IDS = list(shogun.IDS), list(tenma.IDS)
    HI = max(int(r.split('..')[-1]) for r in S_IDS + T_IDS)
    write('init',[f'scoreboard objectives add {v} dummy' for v in objectives + shogun.OBJECTIVES + tenma.OBJECTIVES]+[
        'bossbar add rlk:narukami {text:"마가츠 미타케 나루카미노 미코토",color:"light_purple"}',
        'bossbar add rlk:narukami_state {text:"악연의 에너지",color:"light_purple"}',
        '# Resource-pack boss bar (tools/build_bossbar.py): white bars are transparent, the',
        '# names carry the level/name line and the drawn HP bar with its under bar.',
        'bossbar set rlk:narukami color white','bossbar set rlk:narukami_state color white',
        'bossbar set rlk:narukami style progress','bossbar set rlk:narukami_state style progress',
        call('bars_hide'),
        'scoreboard players set #rd100 rd 100','scoreboard players set #rd4 rd 4',
        'scoreboard players set #rd2 rd 2','scoreboard players set #rd3 rd 3','scoreboard players set #rd10 rd 10',
        call('camera/release_all'), call('rig/init'), call('vfx/init'), call('object_vfx/init'), call('movement/init'), 'kill @e[tag=rlk_raiden_aux]',
        'execute as @e[tag=rlk_raiden] at @s run '+call('reload')])
    write('reload','''
# A reload cancels pending danger volumes; it never refills boss health (the weapon and the switch after-effect stay).
execute if score @s rdDeath matches 1 run return run kill @s
scoreboard players set @s rdDeath 0
scoreboard players set @s rdDeathTime 0
scoreboard players set @s rdUltUsed 0
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdHidden 0
kill @e[tag=rlk_rd_blink_dest]
function rlk:boss/raiden/illusion/cleanup
attribute @s minecraft:scale base set 1.2
scoreboard players set @s rdPhase 0
scoreboard players set @s rdPat 0
scoreboard players set @s rdGo 0
scoreboard players set @s rdNext 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdRage 0
scoreboard players set @s rdCool 40
scoreboard players set @s rdHitCD 0
function rlk:boss/raiden/sg/reload
function rlk:boss/raiden/rig/spawn
function rlk:boss/raiden/sg/look
''')
    write('spawn','''
# Room boss spawn, position = arena center. One encounter is active at a time.
function rlk:boss/raiden/cleanup
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_zmob","rlk_newmob","rlk_m_boss","boss","rlk_raiden","rlk_rd_newboss"],PersistenceRequired:1b,NoAI:1b,Silent:1b,IsBaby:0b,CanPickUpLoot:0b,DeathLootTable:"minecraft:empty",CustomName:{text:"마가츠 미타케 나루카미노 미코토",color:"light_purple"},active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
execute as @e[tag=rlk_rd_newboss] at @s run function rlk:boss/raiden/setup
tag @e[tag=rlk_rd_newboss] remove rlk_rd_newboss
''')
    write('setup','''
function rlk:room/mob_init
attribute @s minecraft:attack_damage base set 0
attribute @s minecraft:movement_speed base set 0
function rlk:mob/setup
attribute @s minecraft:knockback_resistance base set 1
attribute @s minecraft:explosion_knockback_resistance base set 1
scoreboard players set @s rdCycle 0
scoreboard players set @s rdPrev 0
scoreboard players set @s rdTurns 0
# A new fight: random weapon (sword / polearm, 50/50), no switch after-effect yet (plan A.1, A.2).
function rlk:boss/raiden/sg/setup
function rlk:boss/raiden/reload
bossbar set rlk:narukami players @a[tag=player]
bossbar set rlk:narukami visible true
bossbar set rlk:narukami_state players @a[tag=player]
bossbar set rlk:narukami_state visible true
scoreboard players set #rdBar rd 1
title @a[tag=player] times 8 60 16
title @a[tag=player] subtitle {text:"라이덴의 이나즈마 전하",color:"white"}
title @a[tag=player] title {text:"마가츠 미타케 나루카미노 미코토",color:"light_purple",bold:true}
scoreboard players set @a[tag=player] vBig 84
scoreboard players set @a[tag=player] ttlT 84
scoreboard players set #rdCap rd 1
playsound minecraft:entity.wither.spawn hostile @a[tag=player] ~ ~ ~ 0.7 0.62 0.3
''')
    write('cleanup','''
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/caption/clear
function rlk:boss/raiden/illusion/cleanup
kill @e[tag=rlk_raiden_aux]
kill @e[tag=rlk_rd_tmp]
function rlk:boss/raiden/bars_hide
# A fight stopped mid-Tenma (test/stop, run end, uninstall) gives the arena its Shogun floor back.
execute if entity @e[tag=rlk_raiden_arena,limit=1] run function rlk:room/raiden/look_shogun
''')
    write('bars_hide','''
# Boss bars are server-global: hide them whenever no fight is shown (also from rlk:tick).
bossbar set rlk:narukami visible false
bossbar set rlk:narukami_state visible false
scoreboard players set #rdBar rd 0
''')
    write('world','''
execute unless entity @e[tag=rlk_raiden,limit=1] run return run function rlk:boss/raiden/cleanup
execute as @e[tag=rlk_raiden,scores={rdDeath=1},limit=1] at @s run return run function rlk:boss/raiden/death/tick
execute unless entity @a[tag=player,limit=1] run return 0
# A dead player means the run (or boss test) is lost: no bars on the death screen.
execute if entity @a[tag=player,scores={dead=1}] run function rlk:boss/raiden/bars_hide
execute if entity @a[tag=player,scores={dead=1}] run return run function rlk:boss/raiden/pause
execute if entity @a[tag=player,scores={rnDie=1..}] run return run function rlk:boss/raiden/pause
execute if entity @a[tag=player,scores={pkMode=1..}] run return run function rlk:boss/raiden/pause
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/tick
execute as @e[tag=rlk_rd_object] at @s run function rlk:boss/raiden/object/tick
execute as @e[tag=rlk_rd_hazard] at @s run function rlk:boss/raiden/hazard/tick
function rlk:boss/raiden/hazard/vfx_world
execute as @e[tag=rlk_rd_dome] at @s run function rlk:boss/raiden/dome_tick
function rlk:boss/raiden/vfx/world
function rlk:boss/raiden/object_vfx/world
function rlk:boss/raiden/orb/world
''')
    write('pause','''
# World (no @s): the player died, a run death is pending or the level-up screen is open. Runs every such tick.
function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
function rlk:boss/raiden/caption/clear
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
scoreboard players set @e[tag=rlk_raiden] rdBlink 0
scoreboard players set @e[tag=rlk_raiden] rdWalk 0
scoreboard players set @e[tag=rlk_raiden] rdGo 0
# Kit: every hazard and kit display (cue cards, decals); every pattern-scoped entity of both stages; rig props.
function rlk:boss/raiden/hazard/clear
kill @e[tag=rlk_rd_tmp]
function rlk:boss/raiden/rig/prop/clear
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_sfx]
function rlk:boss/raiden/object_vfx/clear
function rlk:boss/raiden/hazard/vfx_world
execute as @e[tag=rlk_raiden,scores={rdDeath=0}] run function rlk:boss/raiden/sg/pause
scoreboard players set @e[tag=rlk_raiden] rdPat 0
scoreboard players set @e[tag=rlk_raiden] rdTime 0
scoreboard players set @e[tag=rlk_raiden] rdCool 60
'''+'\n'.join(shogun.ON_PAUSE+tenma.ON_PAUSE))
    write('tick',f'''
# @s=real living boss; the invisible body owns damage, the displays own appearance.
execute if score @s rdDeath matches 1 run return run function rlk:boss/raiden/death/tick
data merge entity @s {{Motion:[0d,0d,0d],Fire:-1s}}
execute if score @s rdHitCD matches 1.. run scoreboard players remove @s rdHitCD 1
execute if score @s rdCool matches 1.. run scoreboard players remove @s rdCool 1
scoreboard players add @s rdTime 1
execute if score @s rdPhase matches 0 run scoreboard players add @s rdRage 1
# A full gauge waits for the running pattern (and any blink) to finish, then the boss transforms where she stands.
# The forced follow-ups (몽상의 일심 after 찰나의 포영, the multi eye after the single eye) come first.
execute if score @s rdPhase matches 0 if score @s rdRage matches {RAGE_MAX}.. if score @s rdPat matches 0 unless score @s rdBlink matches 1.. unless score @s rdNext matches 7 unless score @s rdSgEye matches 1.. run function rlk:boss/raiden/transform_start
execute if score @s rdPhase matches 1 run function rlk:boss/raiden/transform_tick
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/armor_tick
execute if score @s rdPhase matches 3 run function rlk:boss/raiden/exhausted_tick
execute if score @s rdPhase matches 0 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
execute if score @s rdPhase matches 2 if score @s rdPat matches 0 run function rlk:boss/raiden/idle
# A pattern that must close in first blinks (rdGo); its clock waits at 0 meanwhile.
execute if score @s rdGo matches 1.. if score @s rdPat matches 1..{HI} run function rlk:boss/raiden/close_in
# Phase-0 timelines run from rdTime 0 (the choose tick); phase-2 timelines from rdTime 1 (as in the release).
'''+''.join(f'execute if score @s rdGo matches 0 if score @s rdPat matches {r} run function rlk:boss/raiden/normal_dispatch\n' for r in S_IDS)
   +''.join(f'execute if score @s rdGo matches 0 if score @s rdPat matches {r} if score @s rdTime matches 1.. run function rlk:boss/raiden/armor_dispatch\n' for r in T_IDS)+f'''execute if score @s rdPat matches 99 if score @s rdTime matches 60.. run function rlk:boss/raiden/finish
# Stuns (rdPat 98: real clone found, single eye broken, guard broken), shogun.py.
execute if score @s rdPat matches 98 run function rlk:boss/raiden/sg/stun_tick
# Keep the body on the disc without snapping: slide back toward the centre, and only
# blink home if it is somehow far outside. Tracking uses the avatar, never the camera.
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..21] at @s facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.45 run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..26] unless score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_to
execute if score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_tick
# Phase-0 per-tick state (rear-hit memory, counter cooldown, the switch after-effects); off in every other phase.
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/tick
execute unless score @s rdPhase matches 0 if score @s rdSgFx matches 1.. run function rlk:boss/raiden/sg/fx_off
# Rig visibility: #rdHide 1 hides every part (rig/state/hidden, scale 0 where they stand; never moved) on the
# first hidden tick; the first visible tick queues the form's idle clip unless a clip is already queued.
scoreboard players set #rdHide rd 0
'''+'\n'.join(shogun.TICK_HIDE+tenma.TICK_HIDE)+'''
execute if score #rdHide rd matches 1 unless score @s rdHidden matches 1 run function rlk:boss/raiden/sg/rig_hide
execute if score #rdHide rd matches 0 if score @s rdHidden matches 1.. run function rlk:boss/raiden/sg/rig_show
execute if score #rdHide rd matches 0 at @s run function rlk:boss/raiden/rig/tick
execute if score #rdHide rd matches 1 at @s rotated as @s rotated ~ 0 run function rlk:boss/raiden/rig/follow
'''+'\n'.join(tenma.TICK_TAIL)+'''
function rlk:boss/raiden/bars
''')
    write('idle','''
# Between patterns (no walking, plan A.2): face the player, then choose. A queued rear check keeps her facing.
execute unless score @s rdSgRearQ matches 1 at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute unless score @s rdSgRearQ matches 1 at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute if score @s rdCool matches ..0 at @s run function rlk:boss/raiden/choose
''')
    # Phase-2 shuffle bag (tenma.BAG): every move once before any repeats, in random order; a refilled bag never starts
    # with the move just used. The phase-0 bags (one per weapon, with the range fit) are shogun.py's (sg/draw_*).
    T_BAG = tenma.BAG
    write('bag/count_2', ['scoreboard players set #rdCnt rd 0'] +
          [f'execute if score #rdB{i} rd matches 1 run scoreboard players add #rdCnt rd 1' for i in T_BAG])
    write('bag/fill_2', [f'scoreboard players set #rdB{i} rd 1' for i in T_BAG] +
          [f'execute if score @s rdPrev matches {i} run scoreboard players set #rdB{i} rd 0' for i in T_BAG] +
          [call('bag/count_2')])
    write('bag/draw_2', ['# As the boss: draw one move from the bag into rdPat.', call('bag/count_2'),
          'execute if score #rdCnt rd matches 0 run '+call('bag/fill_2'),
          'execute store result score #rdR rd run random value 0..9999',
          'scoreboard players operation #rdR rd %= #rdCnt rd',
          'scoreboard players add #rdR rd 1',
          'scoreboard players set #rdPick rd 0'] +
          sum(([f'execute if score #rdPick rd matches 0 if score #rdB{i} rd matches 1 run scoreboard players remove #rdR rd 1',
                f'execute if score #rdPick rd matches 0 if score #rdB{i} rd matches 1 if score #rdR rd matches 0 run scoreboard players set #rdPick rd {i}']
               for i in T_BAG), []) +
          ['scoreboard players operation @s rdPat = #rdPick rd'])
    write('choose','''
# As the boss at its feet (idle, rdCool 0). Phase 0: forced picks, reactive rear checks, then the weapon bag with
# the range fit (shogun.py sg/choose). Phase 2: the Tenma bag and tenma.CHOOSE_RULES.
scoreboard players set @s rdPat 0
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/choose
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/bag/draw_2
scoreboard players set @s rdNext 0
scoreboard players add @s rdTurns 1
scoreboard players operation #rdTurn rd = @s rdTurns
scoreboard players operation #rdTurn rd %= #rd4 rd
'''+'\n'.join(tenma.CHOOSE_RULES)+'''
# Boss test hooks (test/lock repeats, test/pattern once) only apply to the current phase.
'''+''.join(f'execute if score @s rdPhase matches {ph} if score #rd{h} rd matches {r} run scoreboard players operation @s rdPat = #rd{h} rd\n'
            for h in ('Lock', 'Force') for ph, ids in ((0, S_IDS), (2, T_IDS)) for r in ids)+'''execute if score @s rdPat = #rdForce rd run scoreboard players set #rdForce rd 0
# Whatever finally runs (bag, forced follow-up, ultimate, test hook) leaves the bag.
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/picked
'''+'\n'.join(f'execute if score @s rdPhase matches 2 if score @s rdPat matches {i} run scoreboard players set #rdB{i} rd 0' for i in T_BAG)+'''
scoreboard players operation @s rdPrev = @s rdPat
scoreboard players set @s rdTime 0
# Face the player; the rear checks (25, 26) strike straight behind her, so they keep her facing.
execute unless score @s rdPat matches 25..26 at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute unless score @s rdPat matches 25..26 at @s rotated as @s run tp @s ~ ~ ~ ~ 0
# A pattern chosen while the player is out of its reach (REACH start) or too near (REACH_MIN) blinks first.
scoreboard players set @s rdGo 0
'''+'\n'.join(f'execute if score @s rdPat matches {i} at @s unless entity @e[tag=rlk_body,distance=..{start}] run scoreboard players set @s rdGo 1' for i,(start,stop) in REACH.items())+'\n'
   +'\n'.join(f'execute if score @s rdPat matches {i} at @s if entity @e[tag=rlk_body,distance=..{lo}] run scoreboard players set @s rdGo 1' for i,lo in REACH_MIN.items())+'''
''')
    # Close-in: blink only (no walking, plan A.2): land REACH_SPOT[pid] (default: REACH stop - 1.5, at least 2) blocks
    # in front of the player, toward her, clamped to radius 20; the pattern clock starts when the blink is over.
    spots = {i: REACH_SPOT.get(i, max(2.0, stop - 1.5)) for i, (start, stop) in REACH.items()}
    for i, lo in REACH_MIN.items():
        spots.setdefault(i, REACH_SPOT.get(i, lo + 2))
    write('close_in',[
        '# As the boss with a chosen pattern that closes in first (rdGo 1..): the clock stays at 0 until the blink is over.',
        'scoreboard players set @s rdTime 0',
        'scoreboard players add @s rdGo 1',
        'execute if score @s rdGo matches 2 run return run function rlk:boss/raiden/close_blink',
        'execute unless score @s rdBlink matches 1.. run function rlk:boss/raiden/close_done',
    ])
    write('close_blink',[
        '# The destination marker in front of the player (toward her), then the blink (movement/blink_to clamps it).',
        'kill @e[tag=rlk_rd_blink_dest]']+[
        f'execute if score @s rdPat matches {i} at @e[tag=rlk_body,limit=1] facing entity @s feet rotated ~ 0 positioned ^ ^ ^{d:g} positioned ~ 201 ~ run function rlk:boss/raiden/movement/blink_to' for i, d in spots.items()]+[
        'execute unless score @s rdBlink matches 1.. run function rlk:boss/raiden/movement/blink_start',
    ])
    write('close_done',[
        'scoreboard players set @s rdGo 0',
        'execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet',
        'execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0',
    ])
    write('finish','''
# As the boss: the pattern is over. Non-detached hazards go (kit hazard/finish), pattern props go.
function rlk:boss/raiden/camera/release_all
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
function rlk:boss/raiden/caption/pattern_end
function rlk:boss/raiden/hazard/finish
kill @e[tag=rlk_rd_sg]
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdGo 0
kill @e[tag=rlk_rd_blink_dest]
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdCool 16
function rlk:boss/raiden/object/clear
kill @e[tag=rlk_rd_dome]
'''+'\n'.join(shogun.ON_FINISH+tenma.ON_FINISH))
    T_LEN = getattr(tenma, 'T_LEN', TRANSFORM_LEN)      # S2-TENMA: the transformation length (60 since S2)
    write('bars',f'''
function rlk:boss/raiden/line/tick
execute if score #rdCap rd matches 1 unless entity @a[tag=player,scores={{ttlT=1..}}] run function rlk:boss/raiden/caption/expire
bossbar set rlk:narukami players @a[tag=player]
bossbar set rlk:narukami visible true
bossbar set rlk:narukami_state players @a[tag=player]
bossbar set rlk:narukami_state visible true
scoreboard players set #rdBar rd 1
# Line 1: level and name (and the armour state). Line 2: the drawn HP bar, numbers on it,
# the white recent-damage trail, and under it the malice gauge / armour / recovery.
execute unless score @s rdPhase matches 2..3 run bossbar set rlk:narukami name [{{text:"Lv.",color:"#FFD86B",bold:true}},{{score:{{name:"@s",objective:"mlv"}},color:"#FFD86B",bold:true}},{{text:"  마가츠 미타케 나루카미노 미코토",color:"#E6C8FF"}}]
execute if score @s rdPhase matches 2 run bossbar set rlk:narukami name [{{text:"Lv.",color:"#FFD86B",bold:true}},{{score:{{name:"@s",objective:"mlv"}},color:"#FFD86B",bold:true}},{{text:"  마가츠 미타케 나루카미노 미코토",color:"#E6C8FF"}},{{text:"  · 번개 갑주",color:"#C58BFF"}}]
execute if score @s rdPhase matches 3 run bossbar set rlk:narukami name [{{text:"Lv.",color:"#FFD86B",bold:true}},{{score:{{name:"@s",objective:"mlv"}},color:"#FFD86B",bold:true}},{{text:"  마가츠 미타케 나루카미노 미코토",color:"#E6C8FF"}},{{text:"  · 갑주 파괴",color:"#7BD88F"}}]
scoreboard players operation #buHp bu = @s mhpC
scoreboard players operation #buMax bu = @s mhpM
scoreboard players set #buSubCol bu 0
execute if score @s rdPhase matches 0 run scoreboard players operation #buSub bu = @s rdRage
execute if score @s rdPhase matches 0 run scoreboard players set #buSubMax bu {RAGE_MAX}
execute if score @s rdPhase matches 0 run scoreboard players set #buSubCol bu 8
execute if score @s rdPhase matches 1 run scoreboard players operation #buSub bu = @s rdTime
execute if score @s rdPhase matches 1 run scoreboard players set #buSubMax bu {T_LEN}
execute if score @s rdPhase matches 1 run scoreboard players set #buSubCol bu 1
execute if score @s rdPhase matches 2 run scoreboard players operation #buSub bu = @s rdShield
execute if score @s rdPhase matches 2 run scoreboard players set #buSubMax bu {SHIELD_MAX}
execute if score @s rdPhase matches 2 run scoreboard players set #buSubCol bu 1
execute if score @s rdPhase matches 3 run scoreboard players operation #buSub bu = @s rdTime
execute if score @s rdPhase matches 3 run scoreboard players set #buSubMax bu {EXHAUST}
execute if score @s rdPhase matches 3 run scoreboard players set #buSubCol bu 9
function rlk:bossui/draw
bossbar set rlk:narukami_state name {{nbt:"line[]",storage:"rlk:bu",interpret:true,separator:""}}
''')
    write('incoming','''
# Called after normal damage/defense modifiers, before damage is deducted.
execute if score #dmg tmp matches ..0 run return 0
# Phase 0: rear-hit memory, the guard parry (번개 배리어) and the guard-break stun x1.5 (shogun.py).
execute if score @s rdPhase matches 0 run function rlk:boss/raiden/sg/incoming
execute if score @s rdPhase matches 2 run function rlk:boss/raiden/shield_hit
execute if score @s rdPhase matches 3 run scoreboard players operation #dmg tmp += #dmg tmp
# Guarantee the first transformation cannot be skipped by one enormous hit.
scoreboard players operation #rdFloor rd = @s mhpM
scoreboard players set #rdPct rd 55
scoreboard players operation #rdFloor rd *= #rdPct rd
scoreboard players operation #rdFloor rd /= #rd100 rd
scoreboard players operation #rdAfter rd = @s mhpC
scoreboard players operation #rdAfter rd -= #dmg tmp
execute if score @s rdPhase matches 0 if score @s rdCycle matches 0 if score #rdAfter rd <= #rdFloor rd run function rlk:boss/raiden/threshold
execute if score #dmg tmp matches 1.. run function rlk:boss/raiden/rig/flash
''')
    write('threshold',f'''
scoreboard players operation #dmg tmp = @s mhpC
scoreboard players operation #dmg tmp -= #rdFloor rd
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 0
scoreboard players set @s rdRage {RAGE_MAX}
''')
    write('hurt','''
# Hazard origin is the knockback source; cm handles avatar, defense and dash invulnerability.
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
# Boss damage multiplier (load: #bossDmgMul %), on top of the mob level scaling. Every
# hazard and the shadow bites set #cmDmg fresh before calling this.
scoreboard players operation #cmDmg tmp *= #bossDmgMul tmp
scoreboard players operation #cmDmg tmp /= #100 tmp
function rlk:cm/hit_pl
# A hit that lands (not dodged) feeds the malice gauge, like the original.
execute unless score #dodged tmp matches 1 as @e[tag=rlk_raiden,scores={rdPhase=0,rdDeath=0},limit=1] run scoreboard players add @s rdRage '''+str(RAGE_HIT)+'''
''')
    write('blink_relocate','''
# Hidden middle of a blink (movement/blink_tick). A destination marker wins; otherwise reform 5 blocks ahead of the
# player, or 5 blocks from the player toward the centre.
execute if entity @e[tag=rlk_rd_blink_dest,limit=1] run return run function rlk:boss/raiden/blink_dest
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_body,limit=1] rotated ~ 0 positioned ^ ^ ^5 positioned ~ 201 ~ run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] at @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_raiden_arena,limit=1] feet rotated ~ 0 positioned ^ ^ ^5 positioned ~ 201 ~ run tp @s ~ ~ ~
execute at @e[tag=rlk_raiden_arena,limit=1] unless entity @s[distance=..20] run tp @s ~ ~ ~
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
''')
    write('blink_dest','''
execute at @e[tag=rlk_rd_blink_dest,limit=1] run tp @s ~ ~ ~
kill @e[tag=rlk_rd_blink_dest]
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
''')
    write('blink',[call('movement/blink_start')])
    write('object/create','''
# At the desired ground point, as boss; kinds: 1 eye (id 10 = the single eye, 1..3 the multi eyes), 2 clone,
# 3 flower, 4 stake. Pattern-scoped: rlk_rd_tmp (pause) and object/clear (finish).
summon minecraft:husk ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_object","rlk_rd_objnew","rlk_mob","rlk_mapv"],NoAI:1b,NoGravity:1b,Silent:1b,PersistenceRequired:1b,CanPickUpLoot:0b,IsBaby:0b,DeathLootTable:"minecraft:empty",active_effects:[{id:"minecraft:invisibility",duration:-1,amplifier:0,show_particles:0b}]}
$scoreboard players set @e[tag=rlk_rd_objnew] rdObjKind $(kind)
$scoreboard players set @e[tag=rlk_rd_objnew] rdObjId $(id)
$scoreboard players set @e[tag=rlk_rd_objnew] rdObjHP $(hp)
scoreboard players set @e[tag=rlk_rd_objnew] rdHitCD 0
scoreboard players set @e[tag=rlk_rd_objnew] rdOAge 0
scoreboard players set @e[tag=rlk_rd_objnew] rdReal 0
scoreboard players set @e[tag=rlk_rd_objnew] mhpC 1000000
scoreboard players set @e[tag=rlk_rd_objnew] mhpM 1000000
scoreboard players set @e[tag=rlk_rd_objnew] mhp0 1000000
scoreboard players set @e[tag=rlk_rd_objnew] xpDrop 0
scoreboard players operation @e[tag=rlk_rd_objnew] mlv = @e[tag=rlk_raiden,limit=1] mlv
execute as @e[tag=rlk_rd_objnew] run attribute @s minecraft:max_health base set 1024
execute as @e[tag=rlk_rd_objnew] run data modify entity @s Health set value 1024f
execute as @e[tag=rlk_rd_objnew] run attribute @s minecraft:attack_damage base set 0
execute as @e[tag=rlk_rd_objnew] run attribute @s minecraft:knockback_resistance base set 1
team join rlk_cam @e[tag=rlk_rd_objnew]
$summon minecraft:item_display ~ ~$(y) ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_objvisual","rlk_rd_visnew"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/$(model)"}},item_display:"none",brightness:{sky:15,block:15},view_range:2f,transformation:{translation:[0f,0f,0f],scale:[1f,1f,1f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
$scoreboard players set @e[tag=rlk_rd_visnew] rdObjId $(id)
tag @e[tag=rlk_rd_visnew] remove rlk_rd_visnew
execute as @e[tag=rlk_rd_objnew,scores={rdObjKind=4}] run tag @s remove rlk_mob
execute as @e[tag=rlk_rd_objnew] at @s run function rlk:boss/raiden/object_vfx/create
execute as @e[tag=rlk_rd_objnew,scores={rdObjKind=3}] at @s run function rlk:boss/raiden/orb/create
tag @e[tag=rlk_rd_objnew] remove rlk_rd_objnew
''')
    write('object/tick','''
scoreboard players add @s rdOAge 1
execute if score @s rdHitCD matches 1.. run scoreboard players remove @s rdHitCD 1
data modify entity @s Health set value 1024f
data merge entity @s {Fire:-1s,Motion:[0d,0d,0d]}
execute unless score @s rdObjKind matches 4 run function rlk:mob/shield_ensure
execute if score @s rdObjKind matches 3 at @s run function rlk:boss/raiden/orb/tick
''')
    write('object/on_hit','''
# Gameplay objects count landed attacks, never award mob loot or proc an infinite HP pool.
scoreboard players set #hitLanded tmp 1
execute if score @s rdHitCD matches 1.. run return 0
execute if score @s rdObjKind matches 4 run return 0
scoreboard players set @s rdHitCD 4
scoreboard players set #rdObjectDrain rd 1
execute if score @s rdObjKind matches 3 if score #elem tmp matches 3 run scoreboard players set #rdObjectDrain rd 4
scoreboard players operation @s rdObjHP -= #rdObjectDrain rd
execute if score @s rdObjHP matches 1.. at @s run function rlk:boss/raiden/object_vfx/hit
playsound minecraft:entity.player.attack.knockback player @a[tag=player] ~ ~ ~ .65 .7 .2
execute if score @s rdObjHP matches ..0 run function rlk:boss/raiden/object/break
''')
    write('object/break','''
execute if score @s rdObjKind matches 3 run function rlk:boss/raiden/orb/remove
execute at @s run function rlk:boss/raiden/object_vfx/break
scoreboard players operation #rdObjectId rd = @s rdObjId
execute as @e[tag=rlk_rd_objvisual] if score @s rdObjId = #rdObjectId rd run kill @s
# An eye's armed danger circle disappears as soon as the eye is destroyed (its disk becomes the pocket).
execute if score @s rdObjKind matches 1 at @s as @e[tag=rlk_rd_hazard,distance=..0.2] run function rlk:boss/raiden/hazard/expire
execute if score @s rdObjKind matches 1 run scoreboard players remove @e[tag=rlk_raiden] rdRage 50
execute as @e[tag=rlk_raiden,scores={rdRage=..-1}] run scoreboard players set @s rdRage 0
# The single eye (id 10): 「간파했군.」 and the stun (shogun.py); a multi eye loses its glow.
execute if score @s rdObjKind matches 1 at @s run function rlk:boss/raiden/sg/eye_break
execute if score @s rdObjKind matches 3 at @s run function rlk:boss/raiden/dome_create
# As the broken clone object, before it is removed (build_raiden_illusions.py).
execute if score @s rdObjKind matches 2 at @s run function rlk:boss/raiden/illusion/on_break
kill @s
''')
    write('object/clear','''
function rlk:boss/raiden/orb/clear
kill @e[tag=rlk_rd_object]
kill @e[tag=rlk_rd_objvisual]
''')

    # ---- Boss test: fight only Narukami in the real boss room, no run needed ----------
    T='[{text:"[보스 테스트] ",color:"light_purple",bold:true},'
    def cmd_link(command,label=None,color='yellow'):
        return f'{{text:"{label or command}",color:"{color}",bold:false,click_event:{{action:"suggest_command",command:"{command}"}}}}'
    TEST='/function rlk:boss/raiden/test/'
    HELP=(T+'{text:"명령: ",color:"gray",bold:false},'
          +cmd_link(TEST+'start','start')+',{text:" 처음부터 · ",color:"gray",bold:false},'
          +cmd_link(TEST+'armored','armored')+',{text:" 갑주 단계 · ",color:"gray",bold:false},'
          +cmd_link(TEST+'pattern {id:11}','pattern {id:N}')+',{text:" 다음 패턴('+', '.join(_rng(r) for r in S_IDS+T_IDS)+') · ",color:"gray",bold:false},'
          +cmd_link(TEST+'lock {id:11}','lock {id:N}')+',{text:" 패턴 고정(0 해제) · ",color:"gray",bold:false},'
          +cmd_link(TEST+'level {lv:12}','level {lv:N}')+',{text:" 보스 레벨 · ",color:"gray",bold:false},'
          +cmd_link(TEST+'stop','stop')+',{text:" 종료 후 로비",color:"gray",bold:false}]')
    write('test/start','''
# /function rlk:boss/raiden/test/start (@s = 'player'): fight only Narukami, normal phase.
# Uses the real boss room (room/raiden layout in the forceloaded dungeon area) and the
# run flags (#active room 1) so room tick, death and cleanup flows all behave as in a run.
# Re-running restarts the fight. Player death or test/stop returns to the lobby.
execute unless entity @s[tag=player] run return run tellraw @s {text:"[보스 테스트] 'player' 태그가 있는 플레이어로 실행하세요.",color:"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s '''+T+'{text:"던전 구역이 준비되지 않았습니다. 먼저 ",color:"gray",bold:false},'+cmd_link('/function rlk:room/setup')+''',{text:" 을 실행하세요.",color:"gray",bold:false}]
execute if score #active room matches 1 unless score #rdTest rd matches 1 run return run tellraw @s '''+T+'{text:"진행 중인 런이 있습니다. ",color:"gray",bold:false},'+cmd_link('/function rlk:run/stop')+''',{text:" 후 다시 실행하세요.",color:"gray",bold:false}]
# Peaceful discards the husk body at once, which would read as an instant win.
execute store result score #rdDiff rd run difficulty
execute if score #rdDiff rd matches 0 run return run tellraw @s '''+T+'''{text:"난이도가 '평화로움'이면 나루카미가 나타나지 않습니다. /difficulty easy 이상으로 바꾼 뒤 다시 실행하세요.",color:"gray",bold:false}]
execute if score @s dead matches 1 run return 0
# The map screen restores its saved position/game mode on close: close it before moving.
execute if score @s vMap matches 1 run function rlk:view/map_close
execute if score @s pkMode matches 1.. run function rlk:lvup/exit
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:lobby/leave
scoreboard players set #rdTest rd 1
scoreboard players set #rdForce rd 0
scoreboard players set #rdLock rd 0
# Stage-2 boss slot (Narukami's planned stage): level = (chapter-1)*6 + mapIdx + 1 = 12
# (test/level changes it).
scoreboard players set #active room 1
scoreboard players set #chapter room 2
scoreboard players set #mapIdx room 5
scoreboard players set #mapType room 8
scoreboard players set #stDefer room 0
scoreboard players set @s rnRev 0
execute in minecraft:overworld run function rlk:room/gen
# Open the arena at once, put the player inside facing the centre, start the fight now.
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zid=2,zst=0}] run function rlk:room/zone_build
execute in minecraft:overworld run tp @s 0.5 201 14.5 180 0
function rlk:view/sync
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zid=2,zst=1}] at @s run function rlk:room/zone_enter
scoreboard players set #spawnT room 0
execute in minecraft:overworld as @e[tag=rlk_zone,scores={zid=2}] at @s run function rlk:room/mob_wave
scoreboard players operation @s curHealth = @s maxHealth
tellraw @s '''+T+'''{text:"나루카미 단독 전투를 시작합니다.",color:"white",bold:false}]
tellraw @s '''+HELP)
    write('test/armored','''
# /function rlk:boss/raiden/test/armored: fresh test fight, transformed straight away.
function rlk:boss/raiden/test/start
execute unless score #rdTest rd matches 1 run return 0
execute as @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] at @s run function rlk:boss/raiden/transform_start
tellraw @s '''+T+'{text:"바로 악요의 요고우 텐마(갑주 단계)로 변신합니다.",color:"white",bold:false}]')
    write('test/pattern','''
# /function rlk:boss/raiden/test/pattern {id:N}: N = '''+'/'.join(_rng(r) for r in S_IDS)+' (normal) or '+'/'.join(_rng(r) for r in T_IDS)+''' (armored), once.
$scoreboard players set #rdReq rd $(id)
execute store result score #rdOk rd run function rlk:boss/raiden/test/request
execute if score #rdOk rd matches 1 run scoreboard players operation #rdForce rd = #rdReq rd
execute if score #rdOk rd matches 1 run tellraw @s '''+T+'''{text:"다음 패턴: ",color:"gray",bold:false},{score:{name:"#rdReq",objective:"rd"},color:"yellow",bold:false}]''')
    write('test/lock','''
# /function rlk:boss/raiden/test/lock {id:N}: repeat pattern N whenever its phase allows; {id:0} unlocks.
$scoreboard players set #rdReq rd $(id)
execute if score #rdReq rd matches 0 run scoreboard players set #rdLock rd 0
execute if score #rdReq rd matches 0 run scoreboard players set #rdForce rd 0
execute if score #rdReq rd matches 0 run return run tellraw @s '''+T+'''{text:"패턴 고정을 해제했습니다.",color:"gray",bold:false}]
execute store result score #rdOk rd run function rlk:boss/raiden/test/request
execute if score #rdOk rd matches 1 run scoreboard players operation #rdLock rd = #rdReq rd
execute if score #rdOk rd matches 1 run tellraw @s '''+T+'''{text:"패턴 고정: ",color:"gray",bold:false},{score:{name:"#rdReq",objective:"rd"},color:"yellow",bold:false},{text:" (해제: lock {id:0})",color:"gray",bold:false}]''')
    write('test/request','''
# #rdReq = requested id. Starts a test if needed, aborts the current attack and switches
# phase so the request can run next. Returns 1 when accepted.
scoreboard players set #rdOk rd 0
'''+''.join(f'execute if score #rdReq rd matches {r} run scoreboard players set #rdOk rd 1\n' for r in S_IDS+T_IDS)+'''execute if score #rdOk rd matches 0 run tellraw @s '''+T+'''{text:"패턴 번호는 '''+', '.join(map(_rng, S_IDS))+'(일반) 또는 '+', '.join(map(_rng, T_IDS))+'''(갑주)입니다.",color:"red",bold:false}]
execute if score #rdOk rd matches 0 run return 0
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run function rlk:boss/raiden/test/start
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run return 0
execute as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/test/apply
return 1
''')
    write('test/apply','''
# @s = boss. Abort the running attack (same reset as a pause), then enter the right phase.
execute unless score @s rdPat matches 0 run function rlk:boss/raiden/pause
'''+''.join(f'execute if score #rdReq rd matches {r} if score @s rdPhase matches {ph} run function rlk:boss/raiden/transform_start\n' for r in T_IDS for ph in (0, 3))
   +''.join(f'execute if score #rdReq rd matches {r} if score @s rdPhase matches 1.. run function rlk:boss/raiden/test/to_normal\n' for r in S_IDS)+'''scoreboard players set @s rdWalk 0
execute unless score @s rdPhase matches 1 run scoreboard players set @s rdCool 2
''')
    write('test/to_normal','''
# @s = boss in phase 1/2/3: drop the armor state without the exhausted break. A test keeps the weapon: the forced
# switch that normal_return queues (tag rlk_rd_switch_due) is dropped again.
kill @e[tag=rlk_rd_hazard]
function rlk:boss/raiden/hazard/vfx_world
function rlk:boss/raiden/normal_return
tag @s remove rlk_rd_switch_due
''')
    write('test/level','''
# /function rlk:boss/raiden/test/level {lv:N}: set the boss level and refill its scaled HP.
$scoreboard players set #rdReq rd $(lv)
execute unless score #rdReq rd matches 1..999 run return run tellraw @s '''+T+'''{text:"레벨은 1 이상이어야 합니다.",color:"red",bold:false}]
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run function rlk:boss/raiden/test/start
execute unless entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] run return 0
execute as @e[tag=rlk_raiden,limit=1] run scoreboard players operation @s mlv = #rdReq rd
execute as @e[tag=rlk_raiden,limit=1] run function rlk:mob/level_apply
tellraw @s '''+T+'''{text:"보스 레벨 ",color:"gray",bold:false},{score:{name:"#rdReq",objective:"rd"},color:"yellow",bold:false},{text:" · 체력을 다시 채웠습니다.",color:"gray",bold:false}]''')
    write('test/stop','''
# /function rlk:boss/raiden/test/stop: remove the fight (bars included) and return to the lobby.
execute unless score #rdTest rd matches 1 run return run tellraw @s '''+T+'''{text:"진행 중인 보스 테스트가 없습니다.",color:"gray",bold:false}]
function rlk:boss/raiden/test/end
tellraw @a[tag=player] '''+T+'''{text:"보스 테스트를 끝내고 로비로 돌아왔습니다.",color:"gray",bold:false}]''')
    write('test/end','''
# Shared teardown: run flags off, room cleared (bars hidden by boss cleanup), lobby spawn.
scoreboard players set #rdTest rd 0
scoreboard players set #rdForce rd 0
scoreboard players set #rdLock rd 0
function rlk:run/end
function rlk:boss/raiden/cleanup
execute as @a[tag=player] run function rlk:lobby/go
''')
    write('test/defeat','''
# From player/hook_respawn (@s = respawned player): a lost test never fails/resets the run.
function rlk:boss/raiden/test/end
title @s times 10 40 15
title @s subtitle {text:"로비로 돌아왔습니다",color:"gray"}
title @s title {text:"보스 테스트 실패",color:"#E06A5A",bold:true}
scoreboard players set @s vBig 65
scoreboard players set @s ttlT 65
tellraw @s '''+T+'{text:"쓰러졌습니다. 다시 도전: ",color:"gray",bold:false},'+cmd_link(TEST+'start')+']')
    write('test/won','''
# From room/combat_clear (boss zone cleared) during a test: no next-chapter object.
tellraw @a[tag=player] '''+T+'{text:"나루카미 처치! ",color:"green",bold:false},'+cmd_link(TEST+'start','[다시 하기]')+',{text:" ",bold:false},'+cmd_link(TEST+'stop','[로비로]')+']')


def write_patterns():
    for i, p in patterns.items():
        write('patterns/'+str(i), p)
