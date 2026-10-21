# @s = the boss: the dome cracks under the slash (a short shudder).
execute at @e[tag=rlk_rd_dome,limit=1] run function rlk:boss/raiden/fx/snd/crystal
execute as @e[tag=rlk_rd_tm_dome] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.4f,8.4f,8.4f],right_rotation:[0f,0f,0f,1f]}}
