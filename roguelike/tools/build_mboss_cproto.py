#!/usr/bin/env python3
"""The chapter proto boss "cproto" (시험용 수호자): proves the chapter mode (AZ-CM) end to end.

    python3 tools/build_mboss_cproto.py

Registry entry: tools/mboss_registry.json id "cproto", n 98, kind chapter, ch [] and route false (never routed: only
/function rlk:mboss/test/chapter {id:"cproto"} reaches it), arena cp_test, two hit proxies, RES {"0":30,"5":30,"*":10},
pools [60, 40], music in two phases. Owns F:mboss/cproto/** (deleted and rewritten) and writes its static rig manifest
tools/mboss_cproto_rig_manifest.json (schema v1, "source": "stub"; the core compiles the proxies from it).

What it exercises (scratchpad az/contract/cm.md 15.1; plan 1.2 R15):
  prep        the gate texts and a per-map roll (cprep.cproto), an entrance glyph prop with a self-stopping glow chain
  spawn       mboss/cb/body (no miniboss, rlk_mb_big, rlk_mb_noshield, husk scale 0.1, RES), proxies core + tail
  pools       phase 1 = 60 % of #mbTot with a 1-HP floor (#mbFloor); the floor hit -> phase 2: repool 40 %, title
              swap, music phase 2, a 20-t cine; phase 2 can die
  rig         a tiny anchor rig: clip / tick on the body (mbS / mbT, the manifest's clip_obj / tick_obj) and two block
              displays; clips idle (loop), sweep, sink, rise (proxy columns move, park, come back)
  patterns    every 70 t: 1 slam disc at the lockv lead point, 2 the push ring, 3 a mask hazard with two safe circles
  test {id}   1 mask, 2 pl_dot, 3 push ring, 4 lockv slam, 5 mv/local readout, 6 a #pjNoDodge projectile, 7 cine 40 t,
              8 / 9 the arena looks lit / plain, 10 cb/lose, 11 to phase 2, 20 / 21 / 22 / 23 px states inv /
              tail_only / normal / an unknown one, 30 push capsule on / off, 31 / 32 / 33 clips sink / rise / sweep,
              40 title swap, 41 music phase 2, 42 music stop, 50 an aux with per-element RES, 60 a lingering disc
              extended by hz/extend
"""
import json
import help_lib as H
import mboss_lib as L

ID = 'cproto'
REG = L.load_registry()
B = next(b for b in REG['boss'] if b['id'] == ID)
AR = L.arena_of(B, REG)
CY = AR['cy']
P = f'rlk:mboss/{ID}/'
out = L.Out(owned_dirs=[f'mboss/{ID}'])
TH = L.theme_module(AR['theme'])     # tools/mboss_arena_cp_test.py (S1-CM's own theme: always present)
SPAWN = TH.POINTS['spawn']           # (540.0, 201.0, 8.0, 0.0): the body faces south, toward the arrival
GLYPH = TH.entrance_layout()['glyphs']['upper'][:3]    # the stele west of the gate


def w(name, text):
    out.write(f'mboss/{ID}/{name}', text if isinstance(text, list) else text.strip('\n'))


def fn(name):
    return 'function ' + P + name


# ---------------------------------------------------------------------------------------------
# Static rig manifest (schema v1, manifest.md 3-6; the framework reads proxies / uuids / states / capsules / runtime /
# clip px keys). Local frame: x = s (+ the boss's left), z = f (+ forward), blocks; [x, z, top] columns from the floor.
REST = {'core': [0.0, 0.0, 2.4], 'tail': [0.0, -2.4, 1.2]}
CLIPS = [
    {'id': 1, 'name': 'idle', 'len': 40, 'loop': True, 'next': None,
     'px': {'lerp': True, 'keys': {'0': REST, '20': {'core': [0.0, 0.0, 2.8], 'tail': [0.0, -2.4, 1.2]}, '39': REST}}},
    {'id': 2, 'name': 'sweep', 'len': 24, 'loop': False, 'next': 'idle',
     'px': {'lerp': True, 'keys': {'0': REST, '12': {'core': [0.0, 0.0, 2.4], 'tail': [2.4, -1.0, 1.4]}, '23': REST}}},
    {'id': 3, 'name': 'sink', 'len': 20, 'loop': False, 'next': None,
     'px': {'lerp': True, 'keys': {'0': REST, '19': {'core': [0.0, 0.0, 0.0], 'tail': [0.0, -2.4, 1.2]}}}},
    {'id': 4, 'name': 'rise', 'len': 20, 'loop': False, 'next': 'idle',
     'px': {'lerp': True, 'keys': {'0': {'core': [0.0, 0.0, 0.0], 'tail': [0.0, -2.4, 1.2]}, '19': REST}}},
]
BLOCK, INTS = '524c4b4d-4350-4400-8000-0000000000', [1380731725, 1129333760, -2147483648]
MANIFEST = {
    'schema': 1, 'boss': ID, 'source': 'stub',
    'runtime': {'ns': f'rlk:mboss/{ID}/rig/', 'clip_obj': 'mbS', 'tick_obj': 'mbT'},
    'uuids': {'block': BLOCK, 'ints': INTS, 'proxies': {'core': 65, 'tail': 66}},
    'proxies': {'layout': [
        {'name': 'core', 'part': 'core', 'point': [0, 0, 0], 'w': 2.0, 'top_margin': 0.4, 'tail_only': False, 'idx': 65,
         'uuid': BLOCK + '41', 'flash': 'all'},
        {'name': 'tail', 'part': 'tail', 'point': [0, 0, 0], 'w': 1.2, 'top_margin': 0.3, 'tail_only': True, 'idx': 66,
         'uuid': BLOCK + '42', 'flash': 'all'}],
        'rest': REST},
    'states': {
        'normal': {'px': ['core', 'tail'], 'vis': None, 'inv': False, 'capsules': ['body', 'tailcap']},
        'tail_only': {'px': ['tail'], 'vis': None, 'inv': False, 'capsules': []},
        'inv': {'px': [], 'vis': None, 'inv': True, 'capsules': []},
        'dead': {'px': [], 'vis': None, 'inv': True, 'capsules': []}},
    'capsules': {'body': {'f0': -1.2, 'f1': 1.2, 'hw': 1.2},
                 'tailcap': {'f0': -3.2, 'f1': -1.6, 'hw': 0.6, 'px': 'tail', 'top_max': 1.5}},
    'flash_groups': {'all': ['core', 'tail']},
    'clips': CLIPS,
}
(L.ROOT / f'tools/mboss_{ID}_rig_manifest.json').write_text(json.dumps(MANIFEST, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
CLEN = {c['id']: c['len'] for c in CLIPS}
CNEXT = {c['id']: next((d['id'] for d in CLIPS if d['name'] == c['next']), 0) if c['next'] else 0 for c in CLIPS}

# ---------------------------------------------------------------------------------------------
# Rig: the anchor's clip / tick (mbS / mbT on the body) + two block displays (core cube, tail block)
w('rig/spawn', f'''
# @s = body, at it: the two display parts (rlk_mb_aux: cleanup and /reload remove them).
kill @e[type=minecraft:block_display,tag=rlk_mb_{ID}_part]
summon minecraft:block_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_{ID}_part","rlk_mb_{ID}_core"],block_state:{{id:"minecraft:lodestone"}},teleport_duration:1,transformation:{{translation:[-0.8f,0f,-0.8f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.6f,2.2f,1.6f]}}}}
summon minecraft:block_display ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_{ID}_part","rlk_mb_{ID}_tail"],block_state:{{id:"minecraft:polished_deepslate"}},teleport_duration:1,transformation:{{translation:[-0.5f,0f,-2.9f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.0f,1.0f,1.0f]}}}}
execute unless score @s mbS matches 1.. run scoreboard players set @s mbS 1
execute unless score @s mbT matches -1.. run scoreboard players set @s mbT -1
{fn("rig/follow")}
''')
w('rig/follow', f'''
execute unless entity @e[type=minecraft:block_display,tag=rlk_mb_{ID}_core,limit=1] run return run {fn("rig/spawn")}
execute rotated as @s rotated ~ 0 run tp @e[type=minecraft:block_display,tag=rlk_mb_{ID}_part] ~ ~ ~ ~ 0
''')
w('rig/play', f'''
# {{c}} (@s = body): play clip c from its start next rig tick (tick -1 = queued: the proxies keep their offsets).
$scoreboard players set @s mbS $(c)
scoreboard players set @s mbT -1
''')
rig_tick = ['# @s = body: one rig tick (the pose of mbT is shown this tick); a clip that ends loops, goes on or holds.',
            'execute unless score @s mbT matches 0.. run return run scoreboard players set @s mbT 0',
            'scoreboard players add @s mbT 1']
for cid, ln in CLEN.items():
    nxt = CNEXT[cid]
    if next(c for c in CLIPS if c['id'] == cid)['loop']:
        rig_tick.append(f'execute if score @s mbS matches {cid} if score @s mbT matches {ln}.. run scoreboard players set @s mbT 0')
    elif nxt:
        rig_tick.append(f'execute if score @s mbS matches {cid} if score @s mbT matches {ln}.. run {fn("rig/play")} {{c:{nxt}}}')
    else:
        rig_tick.append(f'execute if score @s mbS matches {cid} if score @s mbT matches {ln}.. run scoreboard players set @s mbT {ln - 1}')
rig_tick.append(fn('rig/follow'))
w('rig/tick', rig_tick)
w('rig/glow', [f'execute as @e[type=minecraft:block_display,tag=rlk_mb_{ID}_part] run data merge entity @s {{Glowing:1b,glow_color_override:10476264}}'])
w('rig/unglow', [f'execute as @e[type=minecraft:block_display,tag=rlk_mb_{ID}_part] run data merge entity @s {{Glowing:0b}}'])

# ---------------------------------------------------------------------------------------------
# Prep (entrance) and the glyph glow chain
GATE = ('{item:"minecraft:lodestone",model:"minecraft:lodestone",item2:"minecraft:compass",model2:"minecraft:compass",'
        'l1:{text:"시험용 수호자",color:"#9FC6E8",bold:true},'
        'l2:{text:"챕터 보스 틀 점검 · 내성: 물리 30% · 바위 30% · 그 외 10%",color:"#D0D0D0",bold:false},'
        'l3:{text:"좌클릭으로 도전",color:"#A8A8A8",bold:false},n:' + str(B['n']) + '}')
w('prep', f'''
# Hook prep (@s = the kind-9 entrance zone marker, at it; cb/pp/{ID} cleared cprep.{ID} first): the gate texts, a per-map
# roll (kept by retries: the gate returns with the same cprep), the glyph prop on the stele and its glow chain.
data modify storage rlk:mboss cprep.{ID}.gate set value {GATE}
data modify storage rlk:mboss cprep.{ID}.title set value {{text:"시험용 수호자",color:"#9FC6E8",bold:true}}
data modify storage rlk:mboss cprep.{ID}.sub set value {{text:"챕터 보스 틀 점검용",color:"#E8E2D0"}}
execute store result storage rlk:mboss cprep.{ID}.roll int 1 run random value 1..4
kill @e[tag=rlk_mb_{ID}_glyph]
summon minecraft:text_display {L.num(GLYPH[0])} {L.num(GLYPH[1])} {L.num(GLYPH[2])} {{Tags:["rlk_room","rlk_mb_{ID}_glyph"],billboard:"vertical",brightness:{{sky:15,block:15}},background:0,text:{{text:"◇",color:"#9FC6E8"}},transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f]}}}}
schedule function {P}glow 10t replace
''')
w('glow', f'''
# Every 10 t while the entrance glyph prop exists (room/clear kills it; uninstall clears the schedule): a soft glow.
execute unless entity @e[tag=rlk_mb_{ID}_glyph,limit=1] run return 0
execute at @e[tag=rlk_mb_{ID}_glyph,limit=1] run particle minecraft:end_rod ~ ~0.2 ~ 0.15 0.2 0.15 0.01 2
schedule function {P}glow 10t replace
''')

# ---------------------------------------------------------------------------------------------
# Arena props (theme.md 4.1): the theme's props(look), spawned by the module at fight start, after its own look calls and
# in reload; tags rlk_mb_arena_prop rlk_mb_ar_<aid> rlk_mb_cp_ap_<group> (+ rlk_mb_aux); 'item:<id>' kinds = a plain item.
for look in AR['looks']:
    lines = [f'# The props of look {look} (@s any): the old ones go first.', f'kill @e[tag=rlk_mb_ar_{AR["aid"]}]']
    for pr in TH.props(look):
        assert pr['kind'].startswith('item:'), pr['kind']
        x, y, z = pr['pos']
        sc = pr['scale'] if isinstance(pr['scale'], (int, float)) else pr['scale'][0]
        lines.append(f'execute in minecraft:overworld run summon minecraft:item_display {L.num(x)} {L.num(y)} {L.num(z)} '
                     f'{{Tags:["rlk_mb_aux","rlk_mb_arena_prop","rlk_mb_ar_{AR["aid"]}","rlk_mb_cp_ap_{pr["group"]}"],'
                     f'Rotation:[{L.num(pr["yaw"])}f,{L.num(pr["pitch"])}f],brightness:{{sky:15,block:15}},'
                     f'item:{{id:"{pr["kind"][5:]}",count:1}},transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
                     f'right_rotation:[0f,0f,0f,1f],scale:[{L.num(sc)}f,{L.num(sc)}f,{L.num(sc)}f]}}}}')
    lines.append(f'scoreboard players set #cpLook mb {AR["looks"].index(look)}')
    w(f'props/{look}', lines)
w('props/now', [f'# The props of the current look (#cpLook: {", ".join(f"{i} {lk}" for i, lk in enumerate(AR["looks"]))}).']
  + [f'execute if score #cpLook mb matches {i} run return run {fn("props/" + lk)}' for i, lk in enumerate(AR['looks'])]
  + [fn('props/' + AR['looks'][0])])

# ---------------------------------------------------------------------------------------------
# Patterns (the module clock #cpT, every 70 t one of three)
w('choose', f'''
scoreboard players add #cpNext mb 1
execute if score #cpNext mb matches 4.. run scoreboard players set #cpNext mb 1
scoreboard players operation #cpPat mb = #cpNext mb
execute if score #mbLock mb matches 1..3 run scoreboard players operation #cpPat mb = #mbLock mb
scoreboard players set #cpT mb 0
''')
w('p/1', f'''
# 1: slam at the lockv lead point (lead 10 t), a 3.5 b disc.
execute if score #cpT mb matches 1 run {L.lockv(10)}
execute if score #cpT mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_lock,limit=1] positioned ~ {CY} ~ run {L.hz_disc(3.5, 24, 120)}
execute if score #cpT mb matches 1 run {fn("rig/play")} {{c:2}}
execute if score #cpT mb matches 40.. run scoreboard players set #cpPat mb 0
''')
w('p/2', f'''
# 2: the push ring around the body (within 6 b -> out to 6.5 b over 4 t), after a short tell.
execute if score #cpT mb matches 1 at @s positioned ~ {CY} ~ run {L.hz_disc(6.0, 16, 0)}
execute if score #cpT mb matches 16 at @s run {L.push_ring(6.0, 4)}
execute if score #cpT mb matches 40.. run scoreboard players set #cpPat mb 0
''')
w('p/3', f'''
# 3: the mask hazard: hit everywhere except within 2.5 b of its two safe markers (the body and a spot 5 b south).
execute if score #cpT mb matches 1 run {fn("mask")}
execute if score #cpT mb matches 50.. run scoreboard players set #cpPat mb 0
''')
w('mask', f'''
{L.hz_mask(2.5, 30, 110)[0]}
execute at @s positioned ~ {CY} ~ run {L.hz_mask(2.5, 30, 110)[1]}
execute at @s positioned ~ {CY} ~ run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_hzsafe","rlk_mb_{ID}_safe"]}}
execute at @s positioned ~ {CY} ~5 run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_hzsafe","rlk_mb_{ID}_safe"]}}
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_{ID}_safe,tag=!rlk_mb_{ID}_sg] mbHzSG = #hzLast mb
tag @e[type=minecraft:marker,tag=rlk_mb_{ID}_safe] add rlk_mb_{ID}_sg
''')
w('pattern', ['# @s = body: the running pattern (#cpT = its clock).', 'scoreboard players add #cpT mb 1']
  + [f'execute if score #cpPat mb matches {k} run {fn(f"p/{k}")}' for k in (1, 2, 3)])
w('phase2', f'''
# The phase-1 floor was reached (#mbFloorHit 1): the second pool (40 % of #mbTot), the title swap, the phase-2 music,
# a 20-t cine (boss hits refused); phase 2 has no floor.
scoreboard players set #cpPh mb 2
scoreboard players set #mbFloor mb 0
scoreboard players set #mbFloorHit mb 0
{L.repool(40)}
{L.title("시험용 수호자 · 2단계", "챕터 보스 틀 점검용", "#E8A0A0")}
{L.music(2)}
{L.cine(True)}
scoreboard players set #cpCine mb 20
function rlk:mboss/lib_clear
scoreboard players set #cpPat mb 0
{L.say('두 번째 판이다.', '#9FC6E8', 2, 30, 2)}
''')

# ---------------------------------------------------------------------------------------------
# Hooks
w('spawn', f'''
# Hook spawn (@s = the arena marker at the centre of cp_test): the chapter body at POINTS spawn, facing south.
execute positioned {L.num(SPAWN[0])} {L.num(SPAWN[1])} {L.num(SPAWN[2])} rotated {L.num(SPAWN[3])} 0 run function rlk:mboss/cb/body
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {fn("reload")}
scoreboard players set #cpPh mb 1
''')
w('reload', f'''
# Hook reload (@s = body): the rig, the module clocks; HP, the proxies (the framework) and the phase are kept.
scoreboard players set #cpPat mb 0
scoreboard players set #cpT mb 0
scoreboard players set #cpCool mb 40
scoreboard players set #cpFlash mb 0
execute unless score #cpPush mb matches 0..1 run scoreboard players set #cpPush mb 0
execute unless score #cpCine mb matches 0.. run scoreboard players set #cpCine mb 0
{fn("rig/spawn")}
execute if score #mbSt mb matches 1 run {fn("props/now")}
data modify storage rlk:mboss sub set value [{{text:"대기",color:"#8A8A8A"}}]
''')
w('intro_tick', f'''
# Hook intro_tick (@s = body, #mbT 1.. ; untargetable): 20 t, then the fight (proxies normal, music phase 1, the floor).
{fn("rig/tick")}
execute if score #mbT mb matches 1 run {L.say('챕터 보스 틀을 점검한다.', '#9FC6E8', 2, 24, 1)}
execute if score #mbT mb matches 20.. run {fn("start_fight")}
''')
w('start_fight', f'''
function rlk:mboss/intro_end
{L.px_state("normal")}
{L.music(1)}
scoreboard players set #mbFloor mb 1
scoreboard players set #cpLook mb 0
{fn("props/now")}
''')
w('tick', f'''
# Hook tick (@s = body, at it): rig, flash, cine clock, the phase switch, the push request, then idle / pattern.
{fn("rig/tick")}
execute if score #cpFlash mb matches 1.. run scoreboard players remove #cpFlash mb 1
execute if score #cpFlash mb matches 0 run {fn("rig/unglow")}
execute if score #cpFlash mb matches 0 run scoreboard players set #cpFlash mb -1
execute if score #cpCine mb matches 1.. run scoreboard players remove #cpCine mb 1
execute if score #cpCine mb matches 0 if score #mbCine mb matches 1 run {L.cine(False)}
execute if score #cpPh mb matches 1 if score #mbFloorHit mb matches 1 run {fn("phase2")}
execute if score #cpPush mb matches 1 run scoreboard players set #mbPushOn mb 1
execute if score #mbCine mb matches 1 run return 0
execute unless score #mbSt mb matches 1 run return 0
execute if score #cpPat mb matches 1.. run return run {fn("pattern")}
execute if score #cpCool mb matches 1.. run scoreboard players remove #cpCool mb 1
function rlk:mboss/mv/turn {{max:8}}
execute if score #cpCool mb matches ..0 run scoreboard players set #cpCool mb 70
execute if score #cpCool mb matches 70 run {fn("choose")}
''')
w('on_hit', f'''
# Hook on_hit (@s = body inside combat/apply; #mbPart = the proxy that was hit, 0 = the body directly): a short flash.
execute unless score #cpFlash mb matches 1.. run {fn("rig/glow")}
scoreboard players set #cpFlash mb 3
scoreboard players operation #cpLastPart mb = #mbPart mb
''')
w('aux_hit', '''
# Hook aux_hit: the framework default (pool, number, broken tag).
''')
w('incoming', '''
# Hook incoming (@s = body inside apply_mods; the framework floor runs after it): no extra modifiers.
''')
w('pause', f'''
{fn("rig/unglow")}
''')
w('resume', '''
# Hook resume: nothing to restore (the framework restarts the music).
''')
w('death_start', f'''
# Hook death_start (@s = body; hazards cleared, bars hidden, proxies in "dead", the music stopped).
scoreboard players set #cpPat mb 0
scoreboard players set #cpPush mb 0
{fn("rig/unglow")}
{fn("rig/play")} {{c:3}}
{L.say('...틀은 멀쩡하군.', '#9FC6E8', 2, 30, 2)}
{L.sound('block.beacon.deactivate', 0.8, 0.8)}
''')
w('death_tick', f'''
{fn("rig/tick")}
execute if score #mbT mb matches 10.. run particle minecraft:smoke ~ ~0.6 ~ 0.4 0.3 0.4 0.01 3 force @a[tag=player]
''')
w('cleanup', '''
# Hook cleanup (no executor; idempotent).
scoreboard players set #cpPat mb 0
scoreboard players set #cpT mb 0
scoreboard players set #cpPush mb 0
scoreboard players set #cpCine mb 0
scoreboard players set #cpFlash mb 0
''')
w('uninstall', f'''
# Hook uninstall: the entrance glow chain.
schedule clear {P}glow
''')
w('bars', '''
# Hook bars (@s = body): the phase on the sub-line, the pool split on the under-bar (gold), HP colour code 3 in phase 2.
execute if score #cpPh mb matches 2 run scoreboard players set #buHpCol bu 3
execute if score #cpPh mb matches 1 run data modify storage rlk:mboss sub set value [{text:"1단계",color:"#9FC6E8"}]
execute if score #cpPh mb matches 2 run data modify storage rlk:mboss sub set value [{text:"2단계",color:"#E8A0A0"}]
''')
w('hz_vis', '''
# Hook hz_vis: framework particle telegraphs only.
''')
w('pj_end', '''
# Hook pj_end: the test projectile is removed at its end (the default).
''')
TESTS = {
    1: [fn('mask')],
    2: L.pl_dot(30, 0),
    3: [f'execute at @s run {L.push_ring(6.0, 4)}'],
    4: [L.lockv(10), f'execute at @e[type=minecraft:marker,tag=rlk_mb_lock,limit=1] positioned ~ {CY} ~ run {L.hz_disc(3.0, 20, 100)}'],
    5: [L.local(), 'tellraw @a[tag=player] [{text:"[cproto] local f ",color:"gray"},{score:{name:"#mbLf",objective:"mb"},color:"yellow"},'
                   '{text:" s ",color:"gray"},{score:{name:"#mbLs",objective:"mb"},color:"yellow"}]'],
    6: [f'execute at @s positioned ~ ~1.2 ~ facing entity @e[tag=rlk_body,limit=1] feet run summon minecraft:block_display ~ ~ ~ '
        f'{{Tags:["rlk_room","rlk_mb_aux","rlk_mb_{ID}_pj"],block_state:{{id:"minecraft:magma_block"}},teleport_duration:1,'
        'transformation:{translation:[-0.25f,-0.25f,-0.25f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.5f,0.5f,0.5f]}}']
       + L.pj_opts(nododge=1)
       + [f'execute at @s positioned ~ ~1.2 ~ facing entity @e[tag=rlk_body,limit=1] feet as @e[tag=rlk_mb_{ID}_pj,tag=!rlk_mb_pj,limit=1] run {L.pj_launch(0.5, 60, 100, 0.5)}'],
    7: [L.cine(True), 'scoreboard players set #cpCine mb 40'],
    8: ['execute in minecraft:overworld run function rlk:mboss/arena/cp_test/look/lit', fn('props/lit')],
    9: ['execute in minecraft:overworld run function rlk:mboss/arena/cp_test/look/plain', fn('props/plain')],
    10: ['function rlk:mboss/cb/lose'],
    11: ['scoreboard players set #mbFloorHit mb 1'],
    20: [L.px_state('inv')], 21: [L.px_state('tail_only')], 22: [L.px_state('normal')], 23: [L.px_state('nosuch')],
    30: ['execute store success score #cpPush mb unless score #cpPush mb matches 1'],
    31: [fn('rig/play') + ' {c:3}'], 32: [fn('rig/play') + ' {c:4}'], 33: [fn('rig/play') + ' {c:2}'],
    40: [L.title('시험용 수호자 · 이름 교체', '챕터 보스 틀 점검용', '#C8E8A0')],
    41: [L.music(2)], 42: [L.music(0)],
    50: ['scoreboard players set #auxHpPct mb 5', 'scoreboard players set #auxRes mb 10', 'scoreboard players set #auxResEl mb 1',
         'scoreboard players set #auxResElV mb 50', f'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^4 positioned ~ {CY} ~ run function rlk:mboss/aux/spawn',
         f'tag @e[tag=rlk_mb_auxlast,limit=1] add rlk_mb_{ID}_aux'],
    60: [L.hz_opts(act=80, rearm=10)[0], L.hz_opts(act=80, rearm=10)[1], f'execute at @s positioned ~ {CY} ~4 run {L.hz_disc(2.0, 12, 30)}',
         f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run {L.hz_extend(40)}'],
}
test = ['# Hook test {id:N} (as the player, from /function rlk:mboss/test/pattern): the chapter-mode checks of cproto (docstring).',
        '$scoreboard players set #cpReq mb $(id)']
for k, lines in TESTS.items():
    if len(lines) == 1:
        test.append(f'execute if score #cpReq mb matches {k} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {lines[0]}')
    else:
        w(f't/{k}', [f'# test {k} (@s = body, at it)'] + lines)
        test.append(f'execute if score #cpReq mb matches {k} as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {fn(f"t/{k}")}')
test.append('scoreboard players set #cpReq mb 0')
w('test', test)
# Contract test/help (L.HELP_HOOKS): /function rlk:mboss/test/pattern {id:"help"} while this boss runs (names of TESTS).
TEST_NAMES = {1: '위험 지대(마스크)', 2: '플레이어 지속 피해', 3: '밀어내는 고리', 4: '예측 지점 내려찍기', 5: '로컬 좌표 읽기',
              6: '대시로 못 피하는 투사체', 7: '연출 40틱', 8: '경기장 밝은 모습', 9: '경기장 기본 모습', 10: '목표 패배 경로',
              11: '2단계로', 20: '판정 상태: 무적', 21: '판정 상태: 꼬리만', 22: '판정 상태: 보통', 23: '판정 상태: 없는 이름',
              30: '밀어내기 캡슐 켜고 끄기', 31: '동작: 가라앉기', 32: '동작: 떠오르기', 33: '동작: 휩쓸기', 40: '이름 교체',
              41: '음악 2단계', 42: '음악 끄기', 50: '원소별 저항이 있는 보조 개체', 60: '오래 남는 원판(hz/extend)'}
assert list(TEST_NAMES) == list(TESTS), 'TEST_NAMES must name every test id'
w('test/help', [H.head('/function rlk:mboss/test/pattern {id:…}', f'{B["name"]} 시험 번호')]
  + [H.row(f'/function rlk:mboss/test/pattern {{id:{k}}}', k, v) for k, v in TEST_NAMES.items()]
  + [H.note('lock {id:1~3}: 그 패턴만 반복(1 내려찍기 원판 · 2 밀어내는 고리 · 3 안전 원 둘인 위험 지대) · {id:0} 해제')])

missing = [h for h in L.HOOKS + L.HELP_HOOKS + L.CHAPTER_HOOKS if not (L.FN / f'mboss/{ID}/{h}.mcfunction').exists()]
assert not missing, missing
removed = out.clean()
print(f'mboss {ID}: {len(out.written)} functions ({len(CLIPS)} clips, {len(MANIFEST["proxies"]["layout"])} proxies), {removed} stale removed.')
