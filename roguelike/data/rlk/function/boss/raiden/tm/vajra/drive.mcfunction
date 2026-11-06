# @s = the boss: vajra {k} is driven into the floor at the centre + ({x}, {z}), with its base ring (state decal r 2.5).
$execute at @e[tag=rlk_raiden_arena,limit=1] positioned ~$(x) ~ ~$(z) run function rlk:boss/raiden/rig/prop/vajra
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tm_vajra
$scoreboard players set @e[tag=rlk_rd_prop_new,limit=1] rdTmV $(k)
$execute at @e[tag=rlk_raiden_arena,limit=1] positioned ~$(x) ~ ~$(z) run function rlk:boss/raiden/fx/vajra_drive
$execute at @e[tag=rlk_raiden_arena,limit=1] positioned ~$(x) ~ ~$(z) run function rlk:boss/raiden/fx/decal/d2 {sx:2.5,sz:2.5,life:$(life)}
