function rlk:cm/sh/rig/select
scoreboard players add @s cmAD 1
execute if score @s cmAD matches 4 run function rlk:cm/sh/rig/pose/81
execute if score @s cmAD matches 8 run function rlk:cm/sh/rig/pose/82
execute if score @s cmAD matches 11 run function rlk:cm/sh/rig/pose/83
execute if score @s cmAD matches 15.. run kill @e[tag=rlk_sh_this]
tag @e[tag=rlk_sh_this] remove rlk_sh_this
