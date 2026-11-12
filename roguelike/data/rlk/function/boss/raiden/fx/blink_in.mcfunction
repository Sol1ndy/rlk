# D.1 cue "blink_in": visual (if any) + sound recipe. Run it at the cue spot.
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_fx","rlk_rd_fxnew","rlk_raiden_aux","rlk_room","rlk_rd_vnew","rlk_rd_fxa"],billboard:"center",item_display:"none",view_range:2f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},interpolation_duration:0,teleport_duration:0,transformation:{translation:[0f,1f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.3f,2.6f,0.3f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/fx_flash","minecraft:custom_model_data":{colors:[11832575]},"minecraft:custom_data":{d:3,to:{translation:[0f,1f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,1.8f,1.4f],right_rotation:[0f,1f,0f,0f]}}}}}
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHLife 5
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
function rlk:boss/raiden/fx/snd/blink_in
