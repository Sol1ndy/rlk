function rlk:cm/nj/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 5 run function rlk:cm/nj/rig/pose/61
execute if score @s cmAD matches 5 run particle minecraft:large_smoke ~ ~0.8 ~ 0.35 0.5 0.35 0.02 30
execute if score @s cmAD matches 5 run particle minecraft:poof ~ ~0.8 ~ 0.35 0.5 0.35 0.02 12
execute if score @s cmAD matches 11.. run kill @e[tag=rlk_nj_this]
tag @e[tag=rlk_nj_this] add rlk_cmsync
tag @e[tag=rlk_nj_this] remove rlk_nj_this
