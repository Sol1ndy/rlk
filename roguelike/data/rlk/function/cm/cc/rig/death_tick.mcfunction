function rlk:cm/cc/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 4 run function rlk:cm/cc/rig/pose/61
execute if score @s cmAD matches 9 run function rlk:cm/cc/rig/pose/62
execute if score @s cmAD matches 13 run function rlk:cm/cc/rig/pose/63
execute if score @s cmAD matches 18.. run kill @e[tag=rlk_cc_this]
tag @e[tag=rlk_cc_this] add rlk_cmsync
tag @e[tag=rlk_cc_this] remove rlk_cc_this
