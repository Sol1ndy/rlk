# @s = the boss, tick 152: the screen-wide crescent; the sweeping katana strikes a held dome (the clash on the shell:
# flash, sparks, ripple, the heavy hit; the bubble swells for a tick and settles by 155) and cracks a quarter of the
# armour. The flower is spent.
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/mangeop_slash
execute if entity @e[tag=rlk_rd_dome,limit=1] run function rlk:boss/raiden/judgment_rig/clash
execute as @e[tag=rlk_rd_tm_dome] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[8.25f,8.25f,8.25f],right_rotation:[0f,0f,0f,1f]}}
execute if entity @e[tag=rlk_rd_dome,limit=1] run scoreboard players remove @s rdShield 190
function rlk:boss/raiden/object/clear
