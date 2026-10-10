function rlk:cm/im/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 3 run function rlk:cm/im/rig/pose/61
execute if score @s cmAD matches 7 run function rlk:cm/im/rig/pose/62
execute if score @s cmAD matches 10 run function rlk:cm/im/rig/pose/63
execute if score @s cmAD matches 14.. run kill @e[tag=rlk_im_this]
tag @e[tag=rlk_im_this] remove rlk_im_this
