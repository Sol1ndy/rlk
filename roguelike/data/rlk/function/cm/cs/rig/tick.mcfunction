# @s = brain, at @s (from cm/vis). Keeps the displays synced, faced and posed; AI lives in cm/cs/tick
function rlk:cm/cs/rig/select
execute store result score #c2n tmp if entity @e[tag=rlk_cs_this]
execute unless score #c2n tmp matches 16 run function rlk:cm/cs/rig/rebuild
tag @e[tag=rlk_cs_this] add rlk_cmsync
function rlk:cm/cs/rig/face
execute if score @s frzT matches 1.. run return run function rlk:cm/cs/rig/frozen
function rlk:cm/cs/rig/choose
execute unless score @s cmAP = #c2p tmp run function rlk:cm/cs/rig/apply
scoreboard players operation @s cmAP = #c2p tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_cs_this,tag=rlk_cs_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_cs_this] remove rlk_cs_this
