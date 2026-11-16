function rlk:cm/cs/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 5 run function rlk:cm/cs/rig/pose/61
execute if score @s cmAD matches 10 run function rlk:cm/cs/rig/pose/62
execute if score @s cmAD matches 18 run function rlk:cm/cs/rig/pose/63
execute if score @s cmAD matches 18 run particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.4 ~ 0.8 0.3 0.8 0 30
execute if score @s cmAD matches 24.. run kill @e[tag=rlk_cs_this]
tag @e[tag=rlk_cs_this] add rlk_cmsync
tag @e[tag=rlk_cs_this] remove rlk_cs_this
