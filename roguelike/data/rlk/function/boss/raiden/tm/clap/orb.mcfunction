# @s = the boss: the sphere shrinks into the orb that flies to the player (8 t).
kill @e[tag=rlk_rd_tm_sphere]
execute positioned ~ ~1.6 ~ run function rlk:boss/raiden/rig/prop/seed
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm_orb
data merge entity @e[tag=rlk_rd_tm_orb,limit=1] {teleport_duration:8}
