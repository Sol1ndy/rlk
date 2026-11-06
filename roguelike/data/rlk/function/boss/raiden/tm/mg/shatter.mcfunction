# @s = the boss: the dome shatters, the flower goes.
execute at @e[tag=rlk_rd_dome,limit=1] run function rlk:boss/raiden/fx/mangeop_shatter
execute at @e[tag=rlk_rd_dome,limit=1] run function rlk:boss/raiden/fx/crystal_ring {r:8}
kill @e[tag=rlk_rd_tm_dome]
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_tm_flower]
