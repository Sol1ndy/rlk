function rlk:cm/cn/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 4 run function rlk:cm/cn/rig/pose/51
execute if score @s cmAD matches 9 run function rlk:cm/cn/rig/pose/52
execute if score @s cmAD matches 14.. run kill @e[tag=rlk_cn_this]
tag @e[tag=rlk_cn_this] remove rlk_cn_this
