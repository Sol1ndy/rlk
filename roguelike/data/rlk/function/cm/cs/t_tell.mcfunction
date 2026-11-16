scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
particle minecraft:electric_spark ~ ~2.3 ~ 0.25 0.25 0.25 0.05 3
execute if score @s cmT matches ..6 unless entity @s[tag=rlk_c2_fix] run function rlk:cm/cs/t_lock
execute if entity @s[tag=rlk_c2_fix] run function rlk:cm/cs/t_line
execute if score @s cmT matches ..0 run function rlk:cm/cs/t_hit
