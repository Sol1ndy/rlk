# The direction marker along the player's velocity (#mbVx #mbVz mb/t from mv/lockv): it faces B + 20 v.
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p4b,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p4","rlk_mb_az_p4t","rlk_mb_az_p4v"]}
execute store result score #aq4X mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_p4b,limit=1] Pos[0] 1000
execute store result score #aq4Z mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_p4b,limit=1] Pos[2] 1000
scoreboard players set #aq4K mb 20
scoreboard players operation #aq4T mb = #mbVx mb
scoreboard players operation #aq4T mb *= #aq4K mb
scoreboard players operation #aq4X mb += #aq4T mb
scoreboard players operation #aq4T mb = #mbVz mb
scoreboard players operation #aq4T mb *= #aq4K mb
scoreboard players operation #aq4Z mb += #aq4T mb
execute store result entity @e[type=minecraft:marker,tag=rlk_mb_az_p4v,limit=1] Pos[0] double 0.001 run scoreboard players get #aq4X mb
execute store result entity @e[type=minecraft:marker,tag=rlk_mb_az_p4v,limit=1] Pos[2] double 0.001 run scoreboard players get #aq4Z mb
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p4dir,limit=1] at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_az_p4v,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0
