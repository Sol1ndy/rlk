# sb 리그 3부품 (실행 위치 = 발, 모델 중심 [8,8,8]); 새 부품은 rlk_c3this 로 남김
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_cmlink","rlk_c3pt","rlk_sb_pt","rlk_sb_body","rlk_c3new","rlk_c3root"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:3.6f,height:2.0f,shadow_radius:0f,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/c3/sb/body","minecraft:custom_model_data":{colors:[16777215]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_cmlink","rlk_c3pt","rlk_sb_pt","rlk_sb_tail","rlk_c3new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:3.6f,height:2.0f,shadow_radius:0f,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/c3/sb/tail","minecraft:custom_model_data":{colors:[16777215]}}}}
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_cmlink","rlk_c3pt","rlk_sb_pt","rlk_sb_mound","rlk_c3new"],NoGravity:1b,Invulnerable:1b,billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:1,view_range:1.5f,width:3.6f,height:2.0f,shadow_radius:0f,item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:cm/c3/sb/mound","minecraft:custom_model_data":{colors:[16777215]}}}}
scoreboard players operation @e[tag=rlk_c3new] cmId = #cid tmp
# 새 부품은 이번 틱 정리(cm/clean)에서 살아남게 표시(분열 · 다시 만들기는 cm/clean 안에서도 일어남)
tag @e[tag=rlk_c3new] add rlk_cmsync
tag @e[tag=rlk_c3new] add rlk_c3this
tag @e[tag=rlk_c3new] remove rlk_c3new
function rlk:cm/sb/rig/pose/0
