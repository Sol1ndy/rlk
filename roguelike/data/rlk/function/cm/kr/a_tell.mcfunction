scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute as @e[tag=rlk_kr_dst] if score @s cmId = #cid tmp run tag @s add rlk_cmsync
particle minecraft:electric_spark ^-0.45 ^1.3 ^0.6 0.1 0.25 0.1 0.02 2
execute if score @s cmT matches ..0 run function rlk:cm/kr/a_dash
