# @s = the boss: the pair centre on the player, a hand 2.8 b to each side (palms in), its pivot 1.6 b up (the hand
# reaches 0.25 b above the floor, never below it).
kill @e[tag=rlk_rd_clap]
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_tmp","rlk_rd_tm","rlk_rd_tm_clapc","rlk_rd_clap"]}
execute at @e[tag=rlk_rd_tm_clapc,limit=1] facing entity @s feet rotated ~180 0 positioned ^2.8 ^1.6 ^ run function rlk:boss/raiden/rig/prop/clap_l
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm
tag @e[tag=rlk_rd_prop_new] add rlk_rd_clap
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm_hl
execute at @e[tag=rlk_rd_tm_clapc,limit=1] facing entity @s feet rotated ~180 0 positioned ^-2.8 ^1.6 ^ run function rlk:boss/raiden/rig/prop/clap_r
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm
tag @e[tag=rlk_rd_prop_new] add rlk_rd_clap
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm_hr
function rlk:boss/raiden/fx/snd/clap_summon
