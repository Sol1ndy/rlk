function rlk:cm/fm/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 3 run function rlk:cm/fm/rig/pose/61
execute if score @s cmAD matches 7 run function rlk:cm/fm/rig/pose/62
execute if score @s cmAD matches 10 run function rlk:cm/fm/rig/pose/63
execute if score @s cmAD matches 14.. run kill @e[tag=rlk_fm_this]
tag @e[tag=rlk_fm_this] remove rlk_fm_this
