# confirmed damage (cm/flash hook): red tint for 6 ticks; glowing parts stay bright
scoreboard players set @s cmAH 6
function rlk:cm/rv/rig/select
execute as @e[tag=rlk_rv_this,tag=rlk_rv_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_rv_this] remove rlk_rv_this
