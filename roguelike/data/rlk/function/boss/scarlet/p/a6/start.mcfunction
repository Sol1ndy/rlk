# A6 후방 섬보 (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt hr.
scoreboard players set #done hr 0
function rlk:mboss/mv/face
function rlk:boss/scarlet/rig/play/a6
function rlk:boss/scarlet/p/a6/blink
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.3 ~ run particle minecraft:end_rod ~ ~ ~ 0.4 0.8 0.4 0.02 12 force @a[tag=player]
execute at @s run playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~ ~ 0.7 1.3 0.23
