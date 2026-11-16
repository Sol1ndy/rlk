# @s = feather: 0.7 b/tick in two checked 0.35 b steps
tag @s add rlk_cmsync
scoreboard players remove @s cmT 1
scoreboard players set #c2s tmp 2
function rlk:cm/rv/fe_move
execute at @s run particle minecraft:small_flame ~ ~ ~ 0.03 0.03 0.03 0 1
execute if score @s cmT matches ..0 run kill @s
