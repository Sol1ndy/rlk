# the brain is gone (cm/clean hook, @s = anchor): the rig becomes a short-lived corpse, by cmId
function rlk:cm/rv/rig/select
tag @e[tag=rlk_rv_this] add rlk_rv_dying
tag @e[tag=rlk_rv_this] add rlk_cmsync
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_rv_this,tag=rlk_rv_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/rv/rig/pose/60
particle minecraft:flame ~ ~1 ~ 0.5 0.4 0.5 0.05 20
playsound minecraft:entity.phantom.death master @a ~ ~ ~ 0.9 0.7
tag @e[tag=rlk_rv_this] remove rlk_rv_this
