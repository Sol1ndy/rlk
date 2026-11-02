# D1 블러드 돌진 (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt kn.
scoreboard players set #done kn 0
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig_stub/play/d1
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 0.3 0.6 0.3 0 16 force @a[tag=player]
execute at @s run playsound minecraft:entity.ravager.roar hostile @a[tag=player] ~ ~ ~ 0.4 1.8 0.13
execute at @s run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
