execute unless entity @e[type=minecraft:marker,tag=rlk_mb_az_orbc,distance=5.2..7.8] unless entity @e[type=minecraft:marker,tag=rlk_mb_az_orbc,distance=9.2..11.8] run return 0
scoreboard players add #aq41N mb 1
execute if score #aq41N mb matches 7.. run return 0
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-0.5
execute at @s run function rlk:mboss/azhdaha/p/frost/nudge_o
