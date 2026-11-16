# D.1 cue "guard_shatter": visual (if any) + sound recipe. Run it at the cue spot.
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_fx","rlk_rd_fxnew","rlk_raiden_aux","rlk_room","rlk_rd_vnew","rlk_rd_fxa"],billboard:"center",item_display:"none",view_range:2f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},interpolation_duration:0,teleport_duration:0,transformation:{translation:[0f,1.2f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.5f,1.5f,1.5f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/fx_burst","minecraft:custom_model_data":{colors:[15918847]},"minecraft:custom_data":{d:4,to:{translation:[0f,1.2f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.4f,3.4f,3.4f],right_rotation:[0f,1f,0f,0f]}}}}}
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHLife 8
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_fx","rlk_rd_fxnew","rlk_raiden_aux","rlk_room","rlk_rd_vnew","rlk_rd_fxa"],billboard:"center",item_display:"none",view_range:2f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},interpolation_duration:0,teleport_duration:0,transformation:{translation:[0f,1.2f,0f],left_rotation:[0f,0f,0f,1f],scale:[3.4f,3.4f,3.4f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/fx_flash","minecraft:custom_model_data":{colors:[16777215]},"minecraft:custom_data":{d:4,to:{translation:[0f,1.2f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.6f,0.6f,0.6f],right_rotation:[0f,1f,0f,0f]}}}}}
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHLife 5
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
function rlk:boss/raiden/fx/snd/guard_shatter
