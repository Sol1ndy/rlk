# the brain is gone (cm/clean hook, @s = anchor): the rig becomes a short-lived corpse, by cmId
function rlk:cm/kr/rig/select
tag @e[tag=rlk_kr_this] add rlk_kr_dying
tag @e[tag=rlk_kr_this] add rlk_cmsync
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_kr_this,tag=rlk_kr_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/kr/rig/pose/60
particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.15 30
playsound minecraft:entity.wither_skeleton.death master @a ~ ~ ~ 0.7 0.9
tag @e[tag=rlk_kr_this] remove rlk_kr_this
