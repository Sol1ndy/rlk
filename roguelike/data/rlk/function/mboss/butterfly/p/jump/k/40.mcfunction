# jump clock 40
function rlk:mboss/butterfly/u/lockp
tag @e[type=minecraft:marker,tag=rlk_mb_bf_lock] add rlk_mb_bf_p2b
tag @e[type=minecraft:marker,tag=rlk_mb_bf_p2b] remove rlk_mb_bf_lock
scoreboard players set #hzKB mb 4
scoreboard players set #hzSfx mb 1
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p2b,limit=1] run function rlk:mboss/hz/disc {r:25,tell:10,dmg:140}
playsound minecraft:block.conduit.activate hostile @a[tag=player] ~ ~ ~ 0.4 1.8 0.13
