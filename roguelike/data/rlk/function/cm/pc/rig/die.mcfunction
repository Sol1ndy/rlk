# the brain is gone (cm/clean hook, @s = anchor): the rig becomes a short-lived corpse, by cmId
function rlk:cm/pc/rig/select
tag @e[tag=rlk_pc_this] add rlk_pc_dying
tag @e[tag=rlk_pc_this] add rlk_cmsync
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_pc_this,tag=rlk_pc_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/pc/rig/pose/60
particle minecraft:end_rod ~ ~1.4 ~ 0.6 0.6 0.6 0.06 20
playsound minecraft:block.beacon.deactivate master @a ~ ~ ~ 1 0.6
playsound minecraft:block.stone.break master @a ~ ~ ~ 1 0.6
tag @e[tag=rlk_pc_this] remove rlk_pc_this
