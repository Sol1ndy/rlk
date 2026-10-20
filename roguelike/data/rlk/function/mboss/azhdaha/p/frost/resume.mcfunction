# Resume: the live circle's heptagram again with its remaining tell (the core cleared the decals).
scoreboard players operation #aq41W mb = #aq41B mb
scoreboard players operation #aq41W mb -= #azB3T mb
execute unless score #aq41W mb matches 1..22 run return 0
data modify storage rlk:mboss az.tl set value {r:75,el:4,hold:3}
execute store result storage rlk:mboss az.tl.tell int 1 run scoreboard players get #aq41W mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p41c,limit=1] run function rlk:mboss/azhdaha/fx/tele/heptagram with storage rlk:mboss az.tl
