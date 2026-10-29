# K resume: the sky arcs over the lock (kit cards, cleared on pause) for the rest of their 16 t.
execute unless score #k_s tk matches 5 run return 0
execute if score #k_c tk matches 16.. run return 0
scoreboard players set #k_t tk 16
scoreboard players operation #k_t tk -= #k_c tk
data modify storage rlk:tk air.k set value {r:35,t:1}
execute store result storage rlk:tk air.k.t int 1 run scoreboard players get #k_t tk
execute at @e[type=minecraft:marker,tag=rlk_tk_klock,limit=1] run function rlk:boss/tachy/fx/p/sky_arcs with storage rlk:tk air.k
