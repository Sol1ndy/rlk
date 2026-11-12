# @s = the boss: the seed leaves her hand and reaches the player in 4 t.
execute positioned ^-0.6 ^1.6 ^0.8 run function rlk:boss/raiden/rig/prop/seed
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm_seed
tag @e[tag=rlk_rd_prop_new] add rlk_rd_shadow
data merge entity @e[tag=rlk_rd_tm_seed,limit=1] {teleport_duration:4}
function rlk:boss/raiden/fx/snd/shadow_seed
