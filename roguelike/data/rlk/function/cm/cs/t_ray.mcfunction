execute unless block ~ ~ ~ #rlk:dash_pass run return 0
particle minecraft:electric_spark ~ ~ ~ 0.08 0.08 0.08 0.02 2
execute if score #c2h tmp matches 0 positioned ~ ~-0.9 ~ if entity @e[tag=rlk_body,distance=..0.95] run scoreboard players set #c2h tmp 1
scoreboard players remove #n tmp 1
execute if score #n tmp matches 1.. positioned ^ ^ ^0.5 run function rlk:cm/cs/t_ray
