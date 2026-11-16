# confirmed damage (cm/flash hook): red tint for 6 ticks; glow parts stay bright
scoreboard players set @s cmAH 6
function rlk:cm/kr/rig/select
execute as @e[tag=rlk_kr_this,tag=rlk_kr_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16737903]}
tag @e[tag=rlk_kr_this] remove rlk_kr_this
