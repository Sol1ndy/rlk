# @s = shuriken: 0.9 b/tick in three checked 0.3 b steps; spins in its own plane
tag @s add rlk_cmsync
scoreboard players remove @s cmT 1
scoreboard players add @s cmAF 1
execute if score @s cmAF matches 3.. run scoreboard players set @s cmAF 0
execute if score @s cmAF matches 0 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0f,0f,1f]}}
execute if score @s cmAF matches 1 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0.86603f,0f,0.5f]}}
execute if score @s cmAF matches 2 run data merge entity @s {start_interpolation:0,transformation:{left_rotation:[0f,0.86603f,0f,-0.5f]}}
scoreboard players set #c2s tmp 3
function rlk:cm/nj/shu_move
execute if score @s cmT matches ..0 run kill @s
