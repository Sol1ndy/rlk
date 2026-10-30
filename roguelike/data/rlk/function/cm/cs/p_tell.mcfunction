scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 run particle minecraft:crit ^-0.9 ^1 ^1.2 0.1 0.1 0.1 0 1
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 run particle minecraft:crit ^0.9 ^1 ^1.2 0.1 0.1 0.1 0 1
execute if score @s cmT matches 5 run playsound minecraft:item.crossbow.loading_middle master @a ~ ~ ~ 1 0.6
execute if score @s cmT matches ..0 run function rlk:cm/cs/p_hit1
