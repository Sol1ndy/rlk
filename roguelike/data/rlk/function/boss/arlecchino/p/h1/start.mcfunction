# H1 연옥 그림자 분신 (S3, p1.py): pattern tick 0 (@s = the body, at it). Clock #pt kn.
scoreboard players set #done kn 0
function rlk:mboss/mv/face
function rlk:boss/arlecchino/rig_stub/play/h1
function rlk:boss/arlecchino/p/h1/web
execute at @s run playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2
execute at @s rotated as @s rotated ~ 0 positioned ~ ~3 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.1 3 0.1 0 30 force @a[tag=player]
