# Missing owner: transfer the rig to a short-lived visual corpse, by cmId.
function rlk:cm/sw/rig/select
tag @e[tag=rlk_sw_this] add rlk_sw_dying
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_sw_this,tag=rlk_sw_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/sw/rig/pose/50
tag @e[tag=rlk_sw_this] remove rlk_sw_this
