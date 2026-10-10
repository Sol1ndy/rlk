function rlk:cm/sw/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 3 run function rlk:cm/sw/rig/pose/51
execute if score @s cmAD matches 7 run function rlk:cm/sw/rig/pose/52
execute if score @s cmAD matches 10 run function rlk:cm/sw/rig/pose/53
execute if score @s cmAD matches 14.. run kill @e[tag=rlk_sw_this]
tag @e[tag=rlk_sw_this] remove rlk_sw_this
