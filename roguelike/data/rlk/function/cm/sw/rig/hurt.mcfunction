# Called at the existing confirmed-damage event, before the gameplay health check.
scoreboard players set @s cmAH 6
function rlk:cm/sw/rig/select
execute as @e[tag=rlk_sw_this,tag=rlk_sw_part] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_sw_this] remove rlk_sw_this
