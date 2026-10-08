particle minecraft:dust{color:[1.0,0.78,0.3],scale:1.1} ~ ~ ~ 0 0 0 0 1
particle minecraft:small_flame ~ ~ ~ 0 0 0 0 1
scoreboard players add #sn tmp 1
execute if score #sn tmp matches ..21 positioned ^ ^ ^0.5 run function rlk:char/navia/shell_line
