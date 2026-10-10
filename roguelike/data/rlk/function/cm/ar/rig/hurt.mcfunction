scoreboard players set @s cmAH 6
function rlk:cm/ar/rig/select
execute as @e[tag=rlk_ar_this,tag=rlk_ar_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_ar_this] remove rlk_ar_this
