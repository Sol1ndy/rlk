function rlk:cm/pc/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 14 run function rlk:cm/pc/rig/pose/61
execute if score @s cmAD matches 14 run particle minecraft:block{block_state:"minecraft:smooth_quartz"} ~ ~0.4 ~ 0.8 0.2 0.8 0 30
execute if score @s cmAD matches 22.. run kill @e[tag=rlk_pc_this]
tag @e[tag=rlk_pc_this] add rlk_cmsync
tag @e[tag=rlk_pc_this] remove rlk_pc_this
