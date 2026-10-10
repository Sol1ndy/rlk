# As the newly initialized kind3 flower, after object_vfx/create assigned rdOvId.
execute unless score @s rdObjKind matches 3 run return 0
scoreboard players operation #rdOrbObject rd = @s rdObjId
execute as @e[tag=rlk_rd_objvisual] if score @s rdObjId = #rdOrbObject rd run kill @s
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_orb","rlk_rd_orb_new","rlk_rd_orb_body"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_orb/orb_0"}},item_display:"none",billboard:"fixed",brightness:{block:15,sky:15},width:3f,height:4f,shadow_radius:0f,interpolation_duration:3,start_interpolation:0,transformation:{translation:[0f,1.45f,0f],scale:[4f,4f,4f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}
scoreboard players operation @e[tag=rlk_rd_orb_new,limit=1] rdOvId = @s rdOvId
tag @e[tag=rlk_rd_orb_new] remove rlk_rd_orb_new
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_orb","rlk_rd_orb_new","rlk_rd_orb_gauge"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_orb/gauge_4"}},item_display:"none",billboard:"center",brightness:{block:15,sky:15},width:3f,height:4f,shadow_radius:0f,interpolation_duration:3,start_interpolation:0,transformation:{translation:[0f,2.63f,0f],scale:[4f,4f,4f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}
scoreboard players operation @e[tag=rlk_rd_orb_new,limit=1] rdOvId = @s rdOvId
scoreboard players set @e[tag=rlk_rd_orb_new,limit=1] rdObjHP -1
tag @e[tag=rlk_rd_orb_new] remove rlk_rd_orb_new
function rlk:boss/raiden/orb/tick
