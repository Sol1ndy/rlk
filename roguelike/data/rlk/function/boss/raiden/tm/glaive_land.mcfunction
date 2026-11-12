# @s = the boss: the thrown glaive lands on the locked spot (pink beam) and stays planted (prop cut at the floor).
kill @e[tag=rlk_rd_tm_flyer]
execute at @e[tag=rlk_rd_tm_spot,limit=1] run function rlk:boss/raiden/fx/glaive_throw
execute at @e[tag=rlk_rd_tm_spot,limit=1] facing entity @s feet rotated ~180 0 run function rlk:boss/raiden/rig/prop/glaive_planted
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm_glaive
