# 20 파멸의 산사태 (WORKING STUB, S1-MOD): t0 the walk to <= 2 b of the centre (30 t), the clip at 40; fronts at [97, 117, 138, 158, 179] and wave 6 at 219 (nododge, low 0.7, outlines 20 t); end 243.
scoreboard players set #aq20W mb 0
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s positioned ~ 201 ~ unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..2,limit=1] run scoreboard players set #aq20W mb 1
execute if score #aq20W mb matches 1 at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] run function rlk:mboss/mv/glide {t:30}
execute if score #aq20W mb matches 1 run function rlk:mboss/azhdaha/rig/play/walk
execute unless score #aq20W mb matches 1 run function rlk:mboss/azhdaha/rig/play/idle
scoreboard players set #mbNoLeash mb 1
function rlk:mboss/azhdaha/fx/tele/ring {r0:176,r:180,tell:238,el:5,nd:2,hold:3}
function rlk:mboss/azhdaha/fx/tele/ring {r0:274,r:280,tell:238,el:5,nd:2,hold:3}
function rlk:mboss/azhdaha/fx/snd/slide_lift
scoreboard players set #azNoPush mb 1
function rlk:mboss/azhdaha/rig/face/track
