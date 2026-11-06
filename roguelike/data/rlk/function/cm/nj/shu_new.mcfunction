# @s = ninja brain; position/rotation = launch point and flight direction
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_nj_shu","rlk_cmlink","rlk_cmsync","rlk_c2new"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:1f,shadow_radius:0f,brightness:{sky:15,block:13},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/nj/shuriken"}}}
execute as @e[tag=rlk_c2new] run tp @s ~ ~ ~ ~ ~
scoreboard players operation @e[tag=rlk_c2new] cmId = #cid tmp
scoreboard players operation @e[tag=rlk_c2new] cmLv = @s mlv
scoreboard players set @e[tag=rlk_c2new] cmT 20
scoreboard players set @e[tag=rlk_c2new] cmAF 0
tag @e[tag=rlk_c2new] remove rlk_c2new
