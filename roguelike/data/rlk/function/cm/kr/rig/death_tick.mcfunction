function rlk:cm/kr/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 4 run function rlk:cm/kr/rig/pose/61
execute if score @s cmAD matches 9 run function rlk:cm/kr/rig/pose/62
execute if score @s cmAD matches 13 run function rlk:cm/kr/rig/pose/63
execute if score @s cmAD matches 13 run particle minecraft:large_smoke ~ ~0.4 ~ 0.6 0.1 0.3 0.02 16
execute if score @s cmAD matches 18.. run kill @e[tag=rlk_kr_this]
tag @e[tag=rlk_kr_this] add rlk_cmsync
tag @e[tag=rlk_kr_this] remove rlk_kr_this
