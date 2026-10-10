function rlk:cm/im/rig/select
tag @e[tag=rlk_im_this] add rlk_im_dying
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_im_this,tag=rlk_im_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/im/rig/pose/60
tag @e[tag=rlk_im_this] remove rlk_im_this
