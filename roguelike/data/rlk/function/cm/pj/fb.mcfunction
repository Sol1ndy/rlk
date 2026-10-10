scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run return run kill @s
scoreboard players set #pst tmp 2
function rlk:cm/pj/fb_step
particle minecraft:flame ~ ~ ~ 0.08 0.08 0.08 0.01 2
particle minecraft:smoke ~ ~ ~ 0 0 0 0 1
