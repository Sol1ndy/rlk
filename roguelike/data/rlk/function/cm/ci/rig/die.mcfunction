# the brain is gone (cm/clean hook, @s = anchor): the rig becomes a short-lived corpse, by cmId
function rlk:cm/ci/rig/select
tag @e[tag=rlk_ci_this] add rlk_ci_dying
tag @e[tag=rlk_ci_this] add rlk_cmsync
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_ci_this,tag=rlk_ci_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/ci/rig/pose/60
particle minecraft:electric_spark ~ ~0.5 ~ 0.25 0.25 0.25 0.12 14
playsound minecraft:entity.vex.death master @a ~ ~ ~ 0.6 1.6
tag @e[tag=rlk_ci_this] remove rlk_ci_this
