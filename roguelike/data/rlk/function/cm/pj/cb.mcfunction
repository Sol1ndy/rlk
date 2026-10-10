scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run return run function rlk:cm/pj/cb_boom
scoreboard players set #pst tmp 3
function rlk:cm/pj/cb_step
scoreboard players remove @s cmVy 30
execute at @s run particle minecraft:smoke ~ ~ ~ 0 0 0 0 1
