# As the broken flower, at it: the safe dome r 8 grows from the flower in 8 t (dome_tick). The bubble is the rig prop
# (rig/prop/dome: 8 displays on fixed yaws, one closed double-sided shell); it starts at a tenth of its size.
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_tm_dome]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_dome"]}
scoreboard players set @e[tag=rlk_rd_dome] rdTime 0
function rlk:boss/raiden/rig/prop/dome
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm_dome
execute as @e[tag=rlk_rd_tm_dome] run data merge entity @s {transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f],right_rotation:[0f,0f,0f,1f]}}
function rlk:boss/raiden/fx/mangeop_dome
