scoreboard players set #hold tmp 1
scoreboard players remove @s cmT 1
particle minecraft:snowflake ~ ~1 ~ 0.5 0.7 0.5 0.02 2
particle minecraft:dust{color:[0.6,0.9,1.0],scale:1.2} ~ ~2.3 ~ 0.2 0.2 0.2 0 2
execute if score @s cmT matches ..0 run function rlk:cm/im/cast
