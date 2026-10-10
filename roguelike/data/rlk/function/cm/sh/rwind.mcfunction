scoreboard players set #hold tmp 1
function rlk:cm/sh/turn
scoreboard players remove @s cmT 1
particle minecraft:dust{color:[1.0,0.35,0.2],scale:1.0} ~ ~0.2 ~ 0.6 0 0.6 0 3
execute if score @s cmT matches ..0 run function rlk:cm/sh/rgo
