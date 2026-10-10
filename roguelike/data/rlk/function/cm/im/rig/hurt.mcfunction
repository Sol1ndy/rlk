scoreboard players set @s cmAH 6
function rlk:cm/im/rig/select
execute as @e[tag=rlk_im_this,tag=rlk_im_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_im_this] remove rlk_im_this
