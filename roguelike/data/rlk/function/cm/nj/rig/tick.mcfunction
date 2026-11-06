# @s = brain, at @s (from cm/vis). Keeps the displays synced, faced and posed; AI lives in cm/nj/tick
function rlk:cm/nj/rig/select
execute store result score #c2n tmp if entity @e[tag=rlk_nj_this]
execute unless score #c2n tmp matches 9 run function rlk:cm/nj/rig/rebuild
tag @e[tag=rlk_nj_this] add rlk_cmsync
function rlk:cm/nj/rig/face
execute if score @s frzT matches 1.. run return run function rlk:cm/nj/rig/frozen
function rlk:cm/nj/rig/choose
execute unless score @s cmAP = #c2p tmp run function rlk:cm/nj/rig/apply
scoreboard players operation @s cmAP = #c2p tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_nj_this,tag=rlk_nj_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_nj_this] remove rlk_nj_this
