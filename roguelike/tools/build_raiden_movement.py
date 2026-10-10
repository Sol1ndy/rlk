"""Short walking intervals and display-only dispersed blink silhouettes.

The controller owns blink_relocate and hides/protects the actual boss whenever
rdBlink is 1..9. This module owns the departure/arrival art and its short life.
Every visible relocation of the boss goes through blink_start (destination: in
front of the player) or blink_to (destination: the execution position).
The ghost dissolves into horizontal fragments, lightning seams and speed
streaks, then reforms at the destination; no particles or copied imagery.
"""
from pathlib import Path
import argparse
import json
import math

SCALE = 8
COLORS = {name:'rlk:raiden/fx/'+name for name in
          ('void','violet','lavender','white','cyan','shadow','violet_dense',
           'glow','afterglow','floor','pearl','blue')}


def box(center, extent, color):
    return {'from':[round(8+(center[i]-extent[i]/2)*16/SCALE,5) for i in range(3)],
            'to':[round(8+(center[i]+extent[i]/2)*16/SCALE,5) for i in range(3)],
            'shade':False,
            'faces':{face:{'texture':'#'+color,'uv':[0,0,16,16]}
                     for face in ('north','south','east','west','up','down')}}


def stroke(mesh, points, width, color, core=False):
    for a,b in zip(points,points[1:]):
        steps=max(1,math.ceil(math.dist(a,b)/.14))
        for j in range(steps):
            p=[a[i]+(b[i]-a[i])*(j+.5)/steps for i in range(3)]
            extent=[abs(b[i]-a[i])/steps+width for i in range(3)]
            mesh.append(box(p,extent,color))
            if core:
                thin=[abs(b[i]-a[i])/steps+width*.27 for i in range(3)]
                thin[2]=extent[2]+.01
                mesh.append(box(p,thin,'white'))


def ghost(frame, armored=False):
    amount=frame/5
    scale=1.31 if armored else 1
    lift=1.05 if armored else 0
    parts=[((0,2.09,0),(.61,.61,.58)),
           ((0,1.38,0),(.62,.84,.34)),
           ((-.49,1.25,.025),(.25,.83,.25)),
           ((.49,1.25,.025),(.25,.83,.25)),
           ((-.16,.45,0),(.27,.86,.30)),
           ((.16,.45,0),(.27,.86,.30))]
    parts=[((c[0]*scale,c[1]*scale+lift,c[2]*scale),
            tuple(x*scale for x in size)) for c,size in parts]
    if armored:
        # Four extra arm silhouettes preserve the armored form's identity.
        parts += [((-.97,3.20,.15),(.85,.35,.38)),
                  ((-1.48,2.77,.45),(.40,.81,.43)),
                  ((1.00,3.17,.13),(.91,.35,.36)),
                  ((1.52,2.70,.47),(.43,.85,.43)),
                  ((-.91,3.66,-.37),(.76,.27,.28)),
                  ((-1.34,3.93,-.28),(.26,.63,.27)),
                  ((.92,3.68,-.37),(.78,.27,.28)),
                  ((1.36,3.90,-.27),(.27,.61,.27))]
    mesh=[]
    for part,(center,size) in enumerate(parts):
        slices=max(3,math.ceil(size[1]/.11))
        for layer in range(slices):
            seed=(part*17+layer*7)%23
            sign=-1 if (part+layer)%2 else 1
            band=size[1]/slices
            base=[center[0],center[1]-size[1]/2+(layer+.5)*band,center[2]]
            shift=[sign*(.35+seed/23*.9)*amount,
                   ((seed%7)-3)*.07*amount,
                   -(.36+seed/23*1.30)*amount]
            pos=[base[i]+shift[i] for i in range(3)]
            ext=[size[0]*(1-.72*amount),band*.77*(1-.3*amount),
                 size[2]*(1-.56*amount)]
            color=('void','violet_dense','blue','shadow')[(part+layer)%4]
            if frame>=4:color='afterglow' if layer%2 else 'violet'
            mesh.append(box(pos,ext,color))
            if layer%2==0:
                seam=[pos[0],pos[1]+ext[1]*.35,pos[2]+ext[2]/2+.008]
                mesh.append(box(seam,[ext[0]*.76,.018, .028],
                                'pearl' if frame<4 else 'lavender'))
            if amount>0 and layer%3==0:
                # Translucent strips make the fragments visibly move away.
                tail=[pos[0]-sign*.12*amount,pos[1]-.025,pos[2]-.28-amount*.4]
                mesh.append(box(tail,[ext[0]*.34,.026,.38+amount*.7],
                                'glow' if frame>=4 else 'violet'))
    # Charged head/weapon silhouette is broken into jagged seams, never a ball.
    for sign in (-1,1):
        y=1.40*scale+lift
        points=[(sign*.30*scale,y+.49,-.02),
                (sign*(.48+.16*amount)*scale,y+.30,-.22-.3*amount),
                (sign*(.34+.28*amount)*scale,y-.02,-.39-.6*amount),
                (sign*(.62+.38*amount)*scale,y-.36,-.65-.9*amount)]
        stroke(mesh,points,.033 if frame<4 else .022,
               'violet_dense' if frame<4 else 'afterglow',core=frame<4)
    if frame>0:
        for i in range(7):
            x=(i-3)*.22*scale
            y=(.23+(i%4)*.56)*scale+lift
            z=-.43-amount*.75
            mesh.append(box((x,y,z),(.028,.025,.45+amount*(.55+i%3*.17)),
                            'pearl' if i%3==0 and frame<4 else 'lavender'))
    return mesh


def build(datapack,resourcepack):
    dp,rp=Path(datapack),Path(resourcepack)
    out=dp/'data/rlk/function/boss/raiden/movement'
    def fn(name,lines):
        p=out/(name+'.mcfunction');p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    for armored in (False,True):
        profile='armored' if armored else 'normal'
        for frame in range(6):
            name=f'{profile}_{frame}'
            p=rp/f'assets/rlk/models/item/raiden/fx_movement/{name}.json'
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(json.dumps({'ambientocclusion':False,
                'textures':{**COLORS,'particle':COLORS['violet']},
                'elements':ghost(frame,armored)},separators=(',',':'))+'\n',encoding='utf-8')
            p=rp/f'assets/rlk/items/raiden/fx_movement/{name}.json'
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(json.dumps({'model':{'type':'minecraft:model',
                'model':f'rlk:item/raiden/fx_movement/{name}'}},separators=(',',':'))+'\n',encoding='utf-8')

    fn('init',[f'scoreboard objectives add {name} dummy' for name in
               ('rdBlink','rdWalk','rdWalkDir','rdMvAge','rdMvKind','rdMvPhase')])
    fn('cleanup',['kill @e[tag=rlk_rd_move_fx]',
                  'kill @e[tag=rlk_rd_blink_dest]',
                  'scoreboard players set @e[tag=rlk_raiden] rdBlink 0',
                  'scoreboard players set @e[tag=rlk_raiden] rdWalk 0'])
    fn('blink_start',[
        '# @s boss at its current position. Controller hides and protects rdBlink 1..9.',
        'execute if score @s rdBlink matches 1.. run return 0',
        'scoreboard players set @s rdWalk 0',
        'scoreboard players set @s rdBlink 1',
        'scoreboard players set @s rdAnim 21',
        'function rlk:boss/raiden/movement/depart',
        'playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~1 ~ 0.6 1.45 0.15',
    ])
    fn('blink_to',[
        '# @s boss; the execution position is the destination (e.g. positioned at the arena centre).',
        '# Scatter blink: depart art where the boss stands, hidden travel, the controller\'s',
        '# blink_relocate (rdBlink 4) consumes the rlk_rd_blink_dest marker, arrive art there.',
        'kill @e[tag=rlk_rd_blink_dest]',
        'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_blink_dest"]}',
        '# A blink that has not relocated yet simply takes the new destination.',
        'execute if score @s rdBlink matches 1..3 run return 0',
        'scoreboard players set @s rdBlink 0',
        'execute at @s run function rlk:boss/raiden/movement/blink_start',
    ])
    fn('blink_tick',[
        '# Called once as boss, before its rig; position is refreshed after relocation.',
        'execute unless score @s rdBlink matches 1.. run return 0',
        'execute if score @s rdBlink matches 4 run function rlk:boss/raiden/blink_relocate',
        'execute if score @s rdBlink matches 4 at @s run function rlk:boss/raiden/movement/arrive',
        'execute if score @s rdBlink matches 4 at @s run playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~1 ~ 0.22 1.75 0.1',
        'scoreboard players add @s rdBlink 1',
        'execute if score @s rdBlink matches 10.. run scoreboard players set @s rdBlink 0',
    ])
    for kind in ('depart','arrive'):
        fn(kind,['# Pure VFX helper: call as boss at @s; never moves the boss or changes rdBlink.',
                 '# Reused by the ultimate disappearance/return independently of ordinary blink.',
                 f'execute if score @s rdPhase matches 2 run function rlk:boss/raiden/movement/{kind}_armored',
                 f'execute unless score @s rdPhase matches 2 run function rlk:boss/raiden/movement/{kind}_normal'])
        for profile,phase in (('normal',0),('armored',2)):
            model=f'{profile}_{0 if kind=="depart" else 5}'
            fn(f'{kind}_{profile}',[
                'summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_move_fx","rlk_rd_mvnew"],'
                'NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:0,'
                'brightness:{block:15,sky:15},shadow_radius:0f,view_range:3f,width:10f,height:8f,'
                'transformation:{translation:[0f,0f,0f],scale:[8f,8f,8f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]},'
                'item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_movement/'+model+'"}}}',
                'data modify entity @e[tag=rlk_rd_mvnew,limit=1] Rotation set from entity @s Rotation',
                'data modify entity @e[tag=rlk_rd_mvnew,limit=1] Rotation[1] set value 0f',
                'scoreboard players set @e[tag=rlk_rd_mvnew] rdMvAge -1',
                f'scoreboard players set @e[tag=rlk_rd_mvnew] rdMvKind {1 if kind=="depart" else 2}',
                f'scoreboard players set @e[tag=rlk_rd_mvnew] rdMvPhase {phase}',
                'tag @e[tag=rlk_rd_mvnew] remove rlk_rd_mvnew',
            ])
    fn('world',['execute as @e[tag=rlk_rd_move_fx] at @s run function rlk:boss/raiden/movement/fx_tick'])
    lines=['scoreboard players add @s rdMvAge 1',
           'execute if score @s rdMvAge matches 6.. run return run kill @s']
    for profile,phase in (('normal',0),('armored',2)):
        for age in range(6):
            for kind in (1,2):
                frame=age if kind==1 else 5-age
                lines.append(f'execute if score @s rdMvPhase matches {phase} if score @s rdMvKind matches {kind} '
                             f'if score @s rdMvAge matches {age} run data modify entity @s '
                             f'item.components."minecraft:item_model" set value "rlk:raiden/fx_movement/{profile}_{frame}"')
    fn('fx_tick',lines)
    fn('walk_start',[
        '# A short tangential step between selected patterns, with the actual walk clip.',
        'scoreboard players set @s rdWalk 12',
        'execute store result score @s rdWalkDir run random value 0..1',
        'scoreboard players set @s rdAnim 1',
    ])
    fn('walk_tick',[
        'execute unless score @s rdWalk matches 1.. run return 0',
        'execute if score @s rdBlink matches 1.. run return 0',
        'execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet',
        'execute if score @s rdWalkDir matches 0 at @s rotated as @s rotated ~70 0 run tp @s ~ ~ ~ ~ 0',
        'execute if score @s rdWalkDir matches 1 at @s rotated as @s rotated ~-70 0 run tp @s ~ ~ ~ ~ 0',
        'scoreboard players set @s rdAnim 1',
        'execute at @s rotated as @s positioned ^ ^ ^0.11 if entity @e[tag=rlk_raiden_arena,distance=..20,limit=1] '
        'if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ minecraft:air run tp @s ~ ~ ~',
        'execute if score @s rdPhase matches 0 if score @s rdWalk matches 9 at @s run playsound minecraft:block.stone.step hostile @a[tag=player] ~ ~ ~ 0.35 0.85 0.05',
        'execute if score @s rdPhase matches 0 if score @s rdWalk matches 3 at @s run playsound minecraft:block.stone.step hostile @a[tag=player] ~ ~ ~ 0.3 0.95 0.05',
        'scoreboard players remove @s rdWalk 1',
        'execute if score @s rdWalk matches 0 run scoreboard players set @s rdAnim 0',
    ])
    print('Built walking helpers and 12 translucent silhouette-fragment blink models.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datapack',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--resourcepack',type=Path,required=True)
    args=parser.parse_args()
    build(args.datapack,args.resourcepack)
