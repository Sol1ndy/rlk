# @s = the boss: the dark sphere with the eye round her (2.5 b).
execute positioned ~ ~1.6 ~ run function rlk:boss/raiden/rig/prop/seed
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm_sphere
data merge entity @e[tag=rlk_rd_tm_sphere,limit=1] {transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.5f,2.5f,2.5f],right_rotation:[0f,0f,0f,1f]}}
