# At the body: a travelling / follow / field hazard reached the player (dodged or not).
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_fx","rlk_rd_strike","rlk_rd_fxnew","rlk_raiden_aux","rlk_room","rlk_rd_vnew"],billboard:"center",item_display:"none",view_range:2f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},interpolation_duration:0,teleport_duration:0,transformation:{translation:[0f,1f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.4f,1.4f,1.4f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/fx_burst","minecraft:custom_model_data":{colors:[16777215]},"minecraft:custom_data":{after:"rlk:raiden/fx_hazard/fx_flash",fade:6970008}}}}
scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHLife 6
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
playsound minecraft:entity.lightning_bolt.impact hostile @a[tag=player] ~ ~ ~ 0.35 1.8 0.1
