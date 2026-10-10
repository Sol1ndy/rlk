function rlk:cm/cn/rig/select
tag @e[tag=rlk_cn_this] add rlk_cn_dying
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_cn_this,tag=rlk_cn_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/cn/rig/pose/50
tag @e[tag=rlk_cn_this] remove rlk_cn_this
