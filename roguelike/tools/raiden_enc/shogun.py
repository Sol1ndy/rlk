"""Raiden phase 0 (Shogun): patterns 1-7, the eyes. Owner: S2-SHOGUN (plan rd/plan.md E.0).

Data read by core.build(): BAG (phase-0 shuffle bag), REACH (close-in ranges), TICK_HIDE (rig-hide conditions).
"""
from .core import (anim, call, center, end, event, face, flat, gated, haz, obj, pattern, patterns,
                   sound, target, tell, write)

BAG = [1, 2, 3, 4, 5, 6, 7]
REACH = {1: (5.5, 4), 2: (16, 13)}
TICK_HIDE = ['execute if score @s rdPat matches 5 if score @s rdTime matches 1.. run scoreboard players set #rdHide rd 1']
# M1 seams read by core.build() (rd/s2_notes.md §3): pattern id ranges, extra objectives, pause / finish additions.
IDS = ['1..7']
OBJECTIVES = []
ON_PAUSE = []
ON_FINISH = []


def build():
    write('normal_dispatch',[f'execute if score @s rdPat matches {i} run '+call('patterns/'+str(i)) for i in range(1,8)])
    p=pattern(1,'4연격 · 가로 베기 세 번, 나기나타 내려찍기, 이어지는 검기')
    t=1
    for n in (3,4,3):
        event(p,t,face,flat,anim(2),haz(1,tell(8),9))
        event(p,t+tell(8),anim(n),sound('entity.player.attack.sweep',1,.7))
        t+=tell(8)+5
    # Fourth hit: the naginata is driven into the floor; lightning bursts around her and
    # falls where the player stands.
    hit=t+tell(10)
    event(p,t,face,flat,anim(5),haz(8,tell(10),15),target+haz(3,tell(10),12))
    event(p,hit,anim(6),sound('entity.lightning_bolt.impact',.9,.75),sound('item.trident.hit_ground',1,.6))
    # Half the time a flying sword wave follows (watch her to the end).
    p.append(f'execute if score @s rdTime matches {hit+2} store result score #rdFollow rd run random value 0..1')
    gated(p,hit+6,'if score #rdFollow rd matches 1',face,flat,anim(2),haz(13,tell(8),12))
    gated(p,hit+6+tell(8),'if score #rdFollow rd matches 1',anim(3),call('object_vfx/slash'),sound('entity.player.attack.sweep',1.1,.9))
    gated(p,hit+8,'if score #rdFollow rd matches 0',call('finish'))
    gated(p,hit+12+tell(8),'if score #rdFollow rd matches 1',call('finish'))
    p=pattern(2,'회전 참격 · 빠른 번개 칼날 세 개와 큰 초승달 검기')
    event(p,1,call('line/will'))
    # She spins in place throwing three fast blades at the player, then a big crescent.
    event(p,1,face,flat,anim(20),sound('entity.breeze.charge',.8,.8))
    # Blades leave every 6 ticks; each is marked tell(6) ticks before it flies.
    for t in [4,10,16]:
        event(p,t,face,flat,haz(13,tell(6),10))
        # Blades overlap; launch each wave from its own hazard marker (yaw locked at its tell).
        event(p,t+tell(6),f'execute as @e[tag=rlk_rd_hazard,scores={{rdShape=13,rdHAge={tell(6)-1}}},limit=1] at @s run '+call('object_vfx/slash'),sound('entity.breeze.shoot',.8,1.25))
    t=16+tell(6)+4
    event(p,t,face,flat,anim(2),haz(10,tell(10),18))
    event(p,t+tell(10),anim(3),call('object_vfx/slash'),sound('entity.player.attack.sweep',1.2,.6))
    end(p,t+tell(10)+8)
    p=pattern(3,'뇌명 · 순간이동 후 발도')
    event(p,1,call('line/noemyeong'))
    # Each scatter blink keeps the rig hidden for 8 ticks (reforms on blink start + 8).
    event(p,1,anim(21),sound('entity.breeze.charge',.8,.7),call('movement/blink_start'))
    t=10+tell(8)
    event(p,10,face,flat,anim(2),haz(2,tell(8),16));event(p,t,anim(6),sound('entity.player.attack.sweep',1.1,.65))
    event(p,t+6,call('movement/blink_start'));event(p,t+15,face,flat,anim(2),haz(1,tell(8),15))
    event(p,t+15+tell(8),anim(4));end(p,t+22+tell(8))
    p=pattern(4,'마가츠의 뇌안 · 하나를 파괴하고 빈 원으로 이동')
    event(p,1,anim(7),call('eyes_start'),call('line/eyes'))
    event(p,16,anim(8));event(p,40,call('eyes_arm'));event(p,59,anim(18));end(p,70)
    # Pattern 5 (분신 · 진짜 찾기) belongs to build_raiden_illusions.py; it ends itself.
    patterns[5]=[call('illusion/tick')]
    p=pattern(6,'낙뢰 · 표시된 자리에서 벗어나세요')
    event(p,1,call('line/command'))
    for k in range(4):
        t=1+k*(tell(9)+4)
        event(p,t,anim(7),target+haz(3,tell(9),12));event(p,t+tell(9),anim(8),sound('entity.lightning_bolt.impact',.7,.8))
    end(p,t+tell(9)+5)
    p=pattern(7,'몽상의 일심 · 가장자리의 번개 구슬 사이로 피하세요')
    # As in the original: she blinks to the centre, electro orbs fall along the outer edge,
    # then time stops and one cut covers nearly the whole arena (radius 19). The orbs burst
    # at the same moment, so the only cover is between them at the very edge.
    HIT=42
    event(p,1,call('line/calm'),center+call('movement/blink_to'),sound('entity.warden.sonic_charge',.6,1.4))
    event(p,10,anim(7))
    event(p,12,center+haz(14,HIT-12,30))
    for k in range(8):
        t=10+2*k
        event(p,t,center+f'execute rotated {45*k} 0 positioned ^ ^ ^21 run '+haz(3,HIT-t,10),
              center+f'execute rotated {45*k} 0 positioned ^ ^ ^21 run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2')
    event(p,HIT-4,call('line/sever_one'))
    event(p,HIT-2,sound('block.beacon.deactivate',.9,.5))
    event(p,HIT,anim(8),sound('entity.lightning_bolt.thunder',.9,.85))
    end(p,HIT+10)
    write('eyes_start',[call('object/clear'),
        center+'execute positioned ~-10 ~ ~-6 run '+obj(1,'electro_orb',3,1,.3),
        center+'execute positioned ~10 ~ ~-6 run '+obj(1,'electro_orb',3,2,.3),
        center+'execute positioned ~ ~ ~11 run '+obj(1,'electro_orb',3,3,.3),
        sound('block.beacon.activate',.7,.7)])
    write('eyes_arm',['execute as @e[tag=rlk_rd_object,scores={rdObjKind=1}] at @s run '+haz(12,18,34)])
