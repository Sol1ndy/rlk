function rlk:cm/fm/rig/select
tag @e[tag=rlk_fm_this] add rlk_fm_dying
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_fm_this,tag=rlk_fm_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/fm/rig/pose/60
tag @e[tag=rlk_fm_this] remove rlk_fm_this
