# The 양육 models riding @s (the aux husk, at it): stalk, cap, cap_x, orb; then clip nurt_idle from tick 0
# (scale-in 0.85 -> 1 over the first 4 t). Call once, right after aux/spawn.
function rlk:boss/apep/om/nurt/kill
tag @s add rlk_ap_om_v
execute positioned ~ ~2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_stalk","rlk_ap_om_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:1.5f,width:0f,height:0f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,-2f,0f],left_rotation:[0f,0f,0f,1f],scale:[1.36f,1.36f,1.36f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/nurt_stalk_idle"}}}
execute positioned ~ ~2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_cap","rlk_ap_om_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:1.5f,width:0f,height:0f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,0.18f,-0.06f],left_rotation:[0.02823f,-0.0004f,-0.01411f,0.9995f],scale:[0.85f,0.85f,0.85f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/nurt_cap_idle"}}}
execute positioned ~ ~2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_cap_x","rlk_ap_om_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:1.5f,width:0f,height:0f,shadow_radius:0f,brightness:{block:14,sky:15},transformation:{translation:[0f,0.18f,-0.06f],left_rotation:[0.02068f,-0.38286f,-0.02384f,0.92327f],scale:[0.85f,0.85f,0.85f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/nurt_capx_idle"}}}
execute positioned ~ ~2 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_ap_om","rlk_ap_om_orb","rlk_ap_om_new"],billboard:"fixed",item_display:"none",interpolation_duration:1,teleport_duration:2,view_range:1.5f,width:0f,height:0f,shadow_radius:0f,brightness:{block:15,sky:15},transformation:{translation:[0f,0.06f,0.4f],left_rotation:[0f,0f,0f,1f],scale:[0.85f,0.85f,0.85f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/apep_om/nurt_orb_on"}}}
execute as @e[type=minecraft:item_display,tag=rlk_ap_om_new] run ride @s mount @e[tag=rlk_ap_om_v,limit=1]
tag @e[type=minecraft:item_display,tag=rlk_ap_om_new] remove rlk_ap_om_new
tag @s remove rlk_ap_om_v
function rlk:boss/apep/om/face
scoreboard players set @s apOI 6
scoreboard players set @s apOC 0
