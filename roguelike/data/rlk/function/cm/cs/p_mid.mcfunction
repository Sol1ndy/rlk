scoreboard players set #hold tmp 1
scoreboard players operation @s cmT -= #eStep tmp
execute if score @s cmT matches ..0 run function rlk:cm/cs/p_hit2
