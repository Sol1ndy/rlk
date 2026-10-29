# @s = bird brain; position / rotation = launch point and flight direction
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_rv_fe","rlk_cmlink","rlk_cmsync","rlk_c3new"],billboard:"fixed",item_display:"none",teleport_duration:1,interpolation_duration:1,view_range:1f,shadow_radius:0f,brightness:{sky:15,block:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.1f,1.1f,1.1f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/rv/feather"}}}
execute as @e[tag=rlk_c3new] run tp @s ~ ~ ~ ~ ~
scoreboard players operation @e[tag=rlk_c3new] cmId = #cid tmp
scoreboard players operation @e[tag=rlk_c3new] cmLv = @s mlv
scoreboard players set @e[tag=rlk_c3new] cmT 26
tag @e[tag=rlk_c3new] remove rlk_c3new
