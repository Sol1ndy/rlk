summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_object_fx","rlk_rd_ofnew"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",teleport_duration:0,brightness:{sky:15,block:15},view_range:3f,width:6f,height:6f,shadow_radius:0f,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_object/warn_slash"}},transformation:{translation:[0f,0f,0f],scale:[4f,4f,4f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}
data modify entity @e[tag=rlk_rd_ofnew,limit=1] Rotation set from entity @s Rotation
data modify entity @e[tag=rlk_rd_ofnew,limit=1] Rotation[1] set value 0f
scoreboard players set @e[tag=rlk_rd_ofnew] rdOvKind 5
scoreboard players set @e[tag=rlk_rd_ofnew] rdOvAge -1
scoreboard players set @e[tag=rlk_rd_ofnew] rdOvLife 32
scoreboard players operation @e[tag=rlk_rd_ofnew,limit=1] rdOvId = @s rdOvId
scoreboard players operation @e[tag=rlk_rd_ofnew,limit=1] rdObjId = @s rdObjId
tag @e[tag=rlk_rd_ofnew] remove rlk_rd_ofnew
