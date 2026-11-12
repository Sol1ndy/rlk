# the brain is gone (cm/clean hook, @s = anchor): the rig becomes a short-lived corpse, by cmId
function rlk:cm/cs/rig/select
tag @e[tag=rlk_cs_this] add rlk_cs_dying
tag @e[tag=rlk_cs_this] add rlk_cmsync
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_cs_this,tag=rlk_cs_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/cs/rig/pose/60
particle minecraft:electric_spark ~ ~0.8 ~ 0.6 0.4 0.6 0.1 24
playsound minecraft:entity.spider.death master @a ~ ~ ~ 0.9 0.6
tag @e[tag=rlk_cs_this] remove rlk_cs_this
