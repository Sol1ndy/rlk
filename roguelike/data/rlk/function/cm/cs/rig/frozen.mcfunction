# frozen: hold the current pose, still clear the hurt flash
execute if score @s cmAH matches 1 as @e[tag=rlk_cs_this,tag=rlk_cs_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_cs_this] remove rlk_cs_this
