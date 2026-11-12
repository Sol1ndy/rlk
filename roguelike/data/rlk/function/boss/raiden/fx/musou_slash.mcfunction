# D.1 cue "musou_slash": visual (if any) + sound recipe. Run it at the cue spot.
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_fx","rlk_rd_fxnew","rlk_raiden_aux","rlk_room","rlk_rd_vnew","rlk_rd_fxa"],billboard:"fixed",item_display:"none",view_range:2f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},interpolation_duration:0,teleport_duration:0,transformation:{translation:[0f,1.6f,0f],left_rotation:[0f,0f,0f,1f],scale:[4f,1f,4f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/fx_crescent","minecraft:custom_model_data":{colors:[15261951]},"minecraft:custom_data":{d:6,to:{translation:[0f,1.6f,0f],left_rotation:[0f,0f,0f,1f],scale:[19f,1f,19f],right_rotation:[0f,1f,0f,0f]}}}}}
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHLife 12
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_fx","rlk_rd_fxnew","rlk_raiden_aux","rlk_room","rlk_rd_vnew"],billboard:"center",item_display:"none",view_range:2f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},interpolation_duration:0,teleport_duration:0,transformation:{translation:[0f,2f,0f],left_rotation:[0f,0f,0f,1f],scale:[6f,6f,6f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/fx_flash","minecraft:custom_model_data":{colors:[16777215]}}}}
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHLife 8
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
function rlk:boss/raiden/fx/snd/musou_slash
