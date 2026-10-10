function rlk:cm/ar/rig/select
tag @e[tag=rlk_ar_this] add rlk_ar_dying
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_ar_this,tag=rlk_ar_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/ar/rig/pose/60
tag @e[tag=rlk_ar_this] remove rlk_ar_this
