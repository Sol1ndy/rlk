# the brain is gone (cm/clean hook, @s = anchor): the rig becomes a short-lived corpse, by cmId
function rlk:cm/nj/rig/select
tag @e[tag=rlk_nj_this] add rlk_nj_dying
tag @e[tag=rlk_nj_this] add rlk_cmsync
scoreboard players set @s cmAD 0
execute as @e[tag=rlk_nj_this,tag=rlk_nj_tint] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}
function rlk:cm/nj/rig/pose/60
playsound minecraft:entity.illusioner.mirror_move master @a ~ ~ ~ 0.8 0.8
tag @e[tag=rlk_nj_this] remove rlk_nj_this
