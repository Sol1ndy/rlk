function rlk:cm/rv/rig/select
scoreboard players add @s cmAD 1
execute if block ~ ~-0.4 ~ #rlk:cm_pass as @e[tag=rlk_rv_this] at @s run tp @s ~ ~-0.4 ~
execute if score @s cmAD matches 12 run function rlk:cm/rv/rig/pose/61
execute if score @s cmAD matches 22 run function rlk:cm/rv/rig/pose/62
execute if score @s cmAD matches 22 run particle minecraft:large_smoke ~ ~0.4 ~ 0.6 0.2 0.6 0.02 16
execute if score @s cmAD matches 28.. run kill @e[tag=rlk_rv_this]
tag @e[tag=rlk_rv_this] add rlk_cmsync
tag @e[tag=rlk_rv_this] remove rlk_rv_this
