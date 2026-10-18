# dash clock 5
particle minecraft:dust{color:[0.714f,0.89f,0.353f],scale:0.8} ~ ~1.2 ~ 0.6 0.6 0.6 0 2 force @a[tag=player]
function rlk:mboss/butterfly/rig_stub/face/player
scoreboard players set #bfDMax mb 60
scoreboard players set #bfDKeep mb 10
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p3a
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p3a] remove rlk_mb_bf_dest
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] run function rlk:mboss/hz/disc {r:35,tell:10,dmg:130}
