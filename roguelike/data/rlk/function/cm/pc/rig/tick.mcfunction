# @s = brain, at @s (from cm/vis). Keeps the displays synced, faced and posed; AI lives in cm/pc/tick
function rlk:cm/pc/rig/select
execute store result score #c2n tmp if entity @e[tag=rlk_pc_this]
execute unless score #c2n tmp matches 14 run function rlk:cm/pc/rig/rebuild
tag @e[tag=rlk_pc_this] add rlk_cmsync
function rlk:cm/pc/rig/face
execute if score @s frzT matches 1.. run return run function rlk:cm/pc/rig/frozen
function rlk:cm/pc/rig/choose
execute unless score @s cmAP = #c2p tmp run function rlk:cm/pc/rig/apply
scoreboard players operation @s cmAP = #c2p tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_pc_this,tag=rlk_pc_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_pc_this] remove rlk_pc_this
