# E1 와리가리 베기 (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt kn.
scoreboard players set #done kn 0
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig_stub/play/e1
function rlk:boss/arlecchino/p/e1/spot
execute at @s run playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2
