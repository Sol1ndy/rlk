# @s = brain, at @s (from cm/vis). Keeps the displays synced, faced and posed; AI lives in cm/rv/tick
function rlk:cm/rv/rig/select
execute store result score #c2n tmp if entity @e[tag=rlk_rv_this]
execute unless score #c2n tmp matches 11 run function rlk:cm/rv/rig/rebuild
tag @e[tag=rlk_rv_this] add rlk_cmsync
function rlk:cm/rv/rig/face
execute if score @s frzT matches 1.. run return run function rlk:cm/rv/rig/frozen
function rlk:cm/rv/rig/choose
execute unless score @s cmAP = #c2p tmp run function rlk:cm/rv/rig/apply
scoreboard players operation @s cmAP = #c2p tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_rv_this,tag=rlk_rv_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_rv_this] remove rlk_rv_this
