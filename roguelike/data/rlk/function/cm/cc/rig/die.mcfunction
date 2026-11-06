# the brain is gone (cm/clean hook, @s = anchor): the rig becomes a short-lived corpse, by cmId
function rlk:cm/cc/rig/select
tag @e[tag=rlk_cc_this] add rlk_cc_dying
tag @e[tag=rlk_cc_this] add rlk_cmsync
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_cc_this,tag=rlk_cc_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/cc/rig/pose/60
particle minecraft:witch ~ ~1.2 ~ 0.4 0.6 0.4 0 20
playsound minecraft:entity.evoker.death master @a ~ ~ ~ 0.8 1.2
tag @e[tag=rlk_cc_this] remove rlk_cc_this
