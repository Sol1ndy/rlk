scoreboard players set @s cmAH 6
function rlk:cm/fm/rig/select
execute as @e[tag=rlk_fm_this,tag=rlk_fm_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_fm_this] remove rlk_fm_this
