# jump clock 33
function rlk:mboss/butterfly/rig_stub/face/player
scoreboard players set #bfDMax mb 35
scoreboard players set #bfDKeep mb 8
function rlk:mboss/butterfly/u/dest
tag @e[type=minecraft:marker,tag=rlk_mb_bf_dest] add rlk_mb_bf_p2a
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p2a] remove rlk_mb_bf_dest
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p2a,limit=1] run function rlk:mboss/mv/glide {t:22}
playsound minecraft:entity.breeze.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.1 0.2
