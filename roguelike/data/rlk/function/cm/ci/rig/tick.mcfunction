# @s = brain, at @s (from cm/vis). Keeps the displays synced, faced and posed; AI lives in cm/ci/tick
function rlk:cm/ci/rig/select
execute store result score #c2n tmp if entity @e[tag=rlk_ci_this]
execute unless score #c2n tmp matches 2 run function rlk:cm/ci/rig/rebuild
tag @e[tag=rlk_ci_this] add rlk_cmsync
function rlk:cm/ci/rig/face
execute if score @s frzT matches 1.. run return run function rlk:cm/ci/rig/frozen
function rlk:cm/ci/rig/choose
execute unless score @s cmAP = #c2p tmp run function rlk:cm/ci/rig/apply
scoreboard players operation @s cmAP = #c2p tmp
execute if score @s cmAH matches 1 as @e[tag=rlk_ci_this,tag=rlk_ci_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_ci_this] remove rlk_ci_this
