# Macro {k}: one landing point here (marker apL k); the first three of a volley make their disc hazard now.
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p35","rlk_mb_ap_p35d","rlk_mb_ap_p35n"]}
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_ap_p35n] apL $(k)
tag @e[type=minecraft:marker,tag=rlk_mb_ap_p35n] remove rlk_mb_ap_p35n
execute unless score #apq35J mb matches 3.. run function rlk:boss/apep/p/spiral/land_hz {tell:12}
scoreboard players add #apq35J mb 1
