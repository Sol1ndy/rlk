function rlk:cm/ar/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 3 run function rlk:cm/ar/rig/pose/61
execute if score @s cmAD matches 7 run function rlk:cm/ar/rig/pose/62
execute if score @s cmAD matches 10 run function rlk:cm/ar/rig/pose/63
execute if score @s cmAD matches 14.. run kill @e[tag=rlk_ar_this]
tag @e[tag=rlk_ar_this] remove rlk_ar_this
