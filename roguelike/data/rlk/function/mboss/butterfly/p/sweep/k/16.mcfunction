# sweep clock 16
function rlk:mboss/butterfly/rig_stub/face/player
scoreboard players set #bfDMax mb 50
scoreboard players set #bfDKeep mb 20
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p13a
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p13a] remove rlk_mb_bf_dest
scoreboard players set #hzAct mb 5
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 4
scoreboard players set #hzY1 mb 25
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p13a,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/sector {r:45,a:90,tell:12,dmg:160}
