# D.1 cue "switch_hoop": visual (if any) + sound recipe. Run it at the cue spot.
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_fx","rlk_rd_fxnew","rlk_raiden_aux","rlk_room","rlk_rd_vnew"],billboard:"center",item_display:"none",view_range:2f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},interpolation_duration:0,teleport_duration:0,transformation:{translation:[0f,1.2f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.25f,1.25f,1.25f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/fx_hoop","minecraft:custom_model_data":{colors:[4862576]}}}}
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHLife 10
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
function rlk:boss/raiden/fx/snd/switch_hoop
