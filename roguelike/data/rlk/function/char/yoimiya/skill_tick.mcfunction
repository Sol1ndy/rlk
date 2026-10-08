scoreboard players remove @s yoiSk 1
scoreboard players operation #lp tmp = @s yoiSk
scoreboard players add #lp tmp 19
scoreboard players operation #lp tmp /= #st20 tmp
scoreboard players operation 염초정화 stacks = #lp tmp
scoreboard players display name 염초정화 stacks {text:"염초 정화의 춤",color:"#FF8A3D"}
execute if score @s yoiSk matches 0 run scoreboard players reset 염초정화 stacks
scoreboard players operation #lp tmp = @s yoiSk
scoreboard players operation #lp tmp %= #st4 tmp
execute if score #lp tmp matches 0 run particle minecraft:small_flame ~ ~0.9 ~ 0.35 0.5 0.35 0.01 2
