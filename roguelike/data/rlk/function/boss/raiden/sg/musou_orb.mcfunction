summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_sgorb","rlk_rd_sgnew","rlk_rd_sg","rlk_rd_tmp","rlk_raiden_aux","rlk_room"]}
$scoreboard players set @e[tag=rlk_rd_sgnew] rdSgDx $(k)
tag @e[tag=rlk_rd_sgnew] remove rlk_rd_sgnew
execute positioned ~ ~1.5 ~ run function rlk:boss/raiden/rig/prop/musou_orb
tag @e[tag=rlk_rd_prop_new] add rlk_rd_sg
tag @e[tag=rlk_rd_prop_new] add rlk_rd_tmp
tag @e[tag=rlk_rd_prop_new] add rlk_rd_sgorbp
$scoreboard players set @e[tag=rlk_rd_prop_new] rdSgDx $(k)
function rlk:boss/raiden/fx/bolt
