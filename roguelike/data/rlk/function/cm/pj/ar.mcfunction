scoreboard players remove @s cmT 1
execute if score @s cmT matches ..0 run return run kill @s
scoreboard players set #pst tmp 4
function rlk:cm/pj/ar_step
particle minecraft:crit ~ ~ ~ 0 0 0 0 1
