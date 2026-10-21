# Whole-field tint (time stop, 만겁): a uniform 35 % violet over the arena floor (r 24.6, soft edge over the open water), {life} ticks.
# Run it at the arena centre.
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rd_fx","rlk_rd_sdecal","rlk_rd_sdecal_tint","rlk_rd_fxnew","rlk_raiden_aux","rlk_room","rlk_rd_vnew"],billboard:"fixed",item_display:"none",view_range:2f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},interpolation_duration:0,teleport_duration:0,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[24.6f,1f,24.6f],right_rotation:[0f,1f,0f,0f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:raiden/fx_hazard/dk_tint","minecraft:custom_model_data":{colors:[16777215]}}}}
tp @e[tag=rlk_rd_vnew,limit=1] ~ ~ ~ ~ 0
$scoreboard players set @e[tag=rlk_rd_vnew,limit=1] rdHLife $(life)
tag @e[tag=rlk_rd_vnew] remove rlk_rd_vnew
