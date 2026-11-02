# G1 죽음의 칼날 (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt kn.
scoreboard players set #done kn 0
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig_stub/play/g1
function rlk:boss/arlecchino/rig_stub/look/glow/crimson
execute at @s run playsound minecraft:block.respawn_anchor.set_spawn hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:entity.wither.shoot hostile @a[tag=player] ~ ~ ~ 0.4 0.6 0.13
