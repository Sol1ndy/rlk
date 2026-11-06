particle minecraft:electric_spark ~ ~0.9 ~ 0.1 0.3 0.1 0.03 2
particle minecraft:dust{color:[0.72,0.45,1.0],scale:1.3} ~ ~1 ~ 0.05 0.25 0.05 0 2
execute if score #c2h tmp matches 0 if entity @e[tag=rlk_body,distance=..1.3] run scoreboard players set #c2h tmp 1
scoreboard players remove #wN tmp 1
execute if score #wN tmp matches 0.. positioned ^ ^ ^0.5 run function rlk:cm/kr/a_ray
