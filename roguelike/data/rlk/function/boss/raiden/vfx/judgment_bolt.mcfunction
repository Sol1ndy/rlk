summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_raiden_aux","rlk_rd_sfx","rlk_rd_sfx_new"],item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_signature/sky_bolt_0"}},item_display:"none",brightness:{sky:15,block:15},view_range:4f,shadow_radius:0f,width:0f,height:0f,interpolation_duration:1,start_interpolation:0,transformation:{translation:[0f,0f,0f],scale:[16f,16f,16f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,1f,0f,0f]}}
scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxAge -1
scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxLife 7
scoreboard players set @e[tag=rlk_rd_sfx_new] rdSfxKind 9
execute if predicate {type:"minecraft:random_chance",chance:0.5} run data modify entity @e[tag=rlk_rd_sfx_new,limit=1] item.components."minecraft:item_model" set value "rlk:raiden/fx_signature/sky_bolt_1"
tag @e[tag=rlk_rd_sfx_new] remove rlk_rd_sfx_new
