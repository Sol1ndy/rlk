# Color feedback only: this siege unit never plays a hit-stagger pose.
scoreboard players set @s cmAH 5
function rlk:cm/cn/rig/select
execute as @e[tag=rlk_cn_this,tag=rlk_cn_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_cn_this] remove rlk_cn_this
