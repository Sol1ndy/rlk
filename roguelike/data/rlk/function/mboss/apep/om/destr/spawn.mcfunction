# The 파괴 models riding @s (the aux husk, at it): shell, shell_x, face; then clip destr_roll from tick 0
# (scale-in 0.85 -> 1 over the first 4 t). Call once, right after aux/spawn.
function rlk:mboss/apep/om/destr/kill
tag @s add rlk_ap_om_v
execute positioned ~ ~2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_shell","rlk_ap_om_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:1.5f,width:0f,height:0f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,-1.38f,0f],left_rotation:[0f,0.70711f,0f,0.70711f],scale:[0.85f,0.85f,0.85f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/destr_shell_normal"}}}
execute positioned ~ ~2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_shell_x","rlk_ap_om_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:1.5f,width:0f,height:0f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,-1.38f,0f],left_rotation:[0.2706f,0.65328f,0.2706f,0.65328f],scale:[0.85f,0.85f,0.85f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/destr_shellx_normal"}}}
execute positioned ~ ~2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_face","rlk_ap_om_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:1.5f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,-1.38f,0f],left_rotation:[0f,0.70711f,0f,0.70711f],scale:[0.85f,0.85f,0.85f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/destr_face_on"}}}
execute as @e[type=minecraft:item_display,tag=rlk_ap_om_new] run ride @s mount @e[tag=rlk_ap_om_v,limit=1]
tag @e[type=minecraft:item_display,tag=rlk_ap_om_new] remove rlk_ap_om_new
tag @s remove rlk_ap_om_v
function rlk:mboss/apep/om/face
scoreboard players set @s apOI 16
scoreboard players set @s apOC 0
