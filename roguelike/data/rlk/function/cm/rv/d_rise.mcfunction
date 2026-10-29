scoreboard players operation @s cmT -= #eStep tmp
execute store result score #c2t tmp run scoreboard players get @s cmT
scoreboard players operation #c2t tmp %= #2 tmp
execute if score #c2t tmp matches 0 run function rlk:cm/rv/rise
execute if score @s cmT matches ..0 run function rlk:cm/rv/d_aim_start
