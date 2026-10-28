# @s = brain, at @s
scoreboard players operation #c2r tmp = @s cmId
# 1 item displays + a feet-origin anchor marker; model pivot [8,8,8]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_ci_rig","rlk_ci_anchor","rlk_cmlink","rlk_cmsync","rlk_ci_new"]}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_ci_rig","rlk_ci_part","rlk_ci_body","rlk_cmlink","rlk_cmsync","rlk_ci_new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:3f,height:3f,shadow_radius:0f,brightness:{sky:15,block:15},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/ci/f_up"}}}
scoreboard players operation @e[tag=rlk_ci_new] cmId = #c2r tmp
tag @e[tag=rlk_ci_new] add rlk_ci_this
tag @e[tag=rlk_ci_new] remove rlk_ci_new
function rlk:cm/ci/rig/pose/0
scoreboard players set @s cmAP -1
scoreboard players set @s cmAH 0
scoreboard players set @s cmAF 0
