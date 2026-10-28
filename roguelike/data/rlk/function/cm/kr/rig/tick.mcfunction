# @s = brain, at @s (from cm/vis). Keeps the displays synced, faced and posed; AI lives in cm/kr/tick
function rlk:cm/kr/rig/select
execute store result score #c2n tmp if entity @e[tag=rlk_kr_this]
execute unless score #c2n tmp matches 9 run function rlk:cm/kr/rig/rebuild
tag @e[tag=rlk_kr_this] add rlk_cmsync
function rlk:cm/kr/rig/face
execute if score @s frzT matches 1.. run return run function rlk:cm/kr/rig/frozen
function rlk:cm/kr/rig/choose
execute unless score @s cmAP = #c2p tmp run function rlk:cm/kr/rig/apply
scoreboard players operation @s cmAP = #c2p tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_kr_this,tag=rlk_kr_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_kr_this] remove rlk_kr_this
