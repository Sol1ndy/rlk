# (core resume hook; FIX STATE-3) the kit cleared every attack decal at the pause: a geyser still ahead gets its
# water-swirl outline again with the ticks it has left (the module clock froze with the fight).
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_az_xlgk,limit=1] run return 0
scoreboard players operation #axlR mb = #axlGD mb
scoreboard players operation #axlR mb -= #azClk mb
execute if score #axlR mb matches ..0 run return 0
data modify storage rlk:mboss az.tl set value {r:30,tell:22,nd:0,hold:3}
data modify storage rlk:mboss az.tl.el set value 2
execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #axlR mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_xlgk,limit=1] run function rlk:mboss/azhdaha/fx/tele/swirl_o with storage rlk:mboss az.tl
